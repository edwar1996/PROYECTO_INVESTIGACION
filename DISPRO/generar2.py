from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
import pyodbc
from flask import Flask

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Blueprint
generar2_bp = Blueprint('generar2', __name__)

# Configuración de email
EMAIL_CONFIG = {
    'remitente': 'disproiem02@gmail.com',
    'password': 'qnsd gtce chyo lhnf',
    'servidor': 'smtp.gmail.com',
    'puerto': 587,
    'asunto': 'Notificación de proceso disciplinario'
}

# Conexión a BD
def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\baselocal;DATABASE=Dispro;UID=baselocal;PWD=baselocal1085'
    )

def fetch_all_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Enviar correo
def enviar_correo(destinatario, estudiante_nombre, estudiante_apellido, grado, seccion, falta_cometida, descargos, compromiso):
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_CONFIG['remitente']
    mensaje['To'] = destinatario
    mensaje['Subject'] = EMAIL_CONFIG['asunto']

    html = f"""
    <html lang="es">
  <body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; text-align: center;">
        
        <!-- Imagen redonda -->
        <img src="https://www.campusvirtual.inempasto.edu.co/wp-content/uploads/2022/07/covid-19-banner_6.png" alt="Logo INEM" 
             style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin-bottom: 20px;">
        
        <h2 style="color: #2c3e50;">Notificación de proceso disciplinario 2</h2>

        <p style="text-align: left;">Estimado acudiente,</p>

        <p>El estudiante <strong>{estudiante_nombre} {estudiante_apellido}</strong> del grado {grado} y sección:{seccion} ha sido registrado en un proceso disciplinario.</p>
      <ul style="text-align: left;">
        <li>
            El estudiante reconoce haber incurrido en faltas al Pacto Social de Convivencia Institucional. En consecuencia, se compromete a cumplir estrictamente con lo establecido en dicho pacto, a realizar el trabajo pedagógico asignado y a socializarlo de manera adecuada.
        </li>
        <li>
            El docente, el equipo de coordinación y los mediadores se comprometen a realizar el seguimiento pertinente, así como a llevar a cabo las acciones preventivas y correctivas necesarias. En caso de que el estudiante incurra nuevamente en las mismas faltas, el proceso disciplinario continuará a su siguiente fase.
        </li>
    </ul>
        <p>Por favor contacte a la institución para más información.</p>
        <p><small>Este es un mensaje automático, no responda.</small></p>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(EMAIL_CONFIG['servidor'], EMAIL_CONFIG['puerto']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['remitente'], EMAIL_CONFIG['password'])
            server.send_message(mensaje)
        current_app.logger.info(f"Correo enviado a {destinatario}")
        return True
    except Exception as e:
        current_app.logger.error(f"Fallo al enviar correo: {str(e)}")
        return False

# Ruta: Registrar proceso disciplinario
@generar2_bp.route('/registrar_proceso2', methods=['POST'])
def registrar_proceso2():
    data = request.form
    try:
        foto = request.files.get('rutafoto')
        rutafoto = None

        if foto and foto.filename:
            filename = secure_filename(foto.filename)
            folder = os.path.join(current_app.root_path, 'static', 'evidencia_fotos_2')
            os.makedirs(folder, exist_ok=True)
            foto_path = os.path.join(folder, filename)
            foto.save(foto_path)
            rutafoto = f'static/evidencia_fotos_2/{filename}'
            logger.debug(f"Imagen guardada: {rutafoto}")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proceso_2 (
                    identificacion, nombres, apellidos, grado, seccion, jornada,
                    idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente,
                    telefono, estado, falta_cometida, rutafoto, mediador1, mediador2, docente
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Activo', ?, ?, ?, ?, ?)
            """, (
                data.get('numeroTI'), data.get('nombresEstudiante'), data.get('apellidosEstudiante'),
                data.get('grado'), data.get('seccion'), data.get('jornada'),
                data.get('idacu'), data.get('nom_acu'), data.get('ape_acu'),
                data.get('cor_acu'), data.get('tel_acu'), data.get('faltaCometida'),
                rutafoto, data.get('mediador1'), data.get('mediador2'), data.get('profesor')
            ))
            conn.commit()
            logger.info("Proceso registrado en 'proceso_2'.")

        # Enviar correo
        if data.get('cor_acu'):
            enviar_correo(
                data.get('cor_acu'),
                data.get('nombresEstudiante'),
                data.get('apellidosEstudiante'),
                data.get('grado'),
                data.get('seccion'),
                data.get('faltaCometida'),
                '---', '---'
            )

        flash("Proceso registrado exitosamente.", "success")
        return redirect(url_for('generar2.generar'))

    except Exception as e:
        logger.error(f"Error al registrar proceso: {str(e)}")
        flash(f"Error al registrar: {str(e)}", "danger")
        return redirect(url_for('generar2.generar'))

# Ruta: Buscar estudiante en proceso_2
@generar2_bp.route('/buscar_estudiante_pdf2', methods=['GET'])
def buscar_estudiante_pdf2():
    numero_documento = request.args.get('numero_documento')
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
        SELECT NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
               IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente
        FROM Estudiantes
        WHERE NumeroDocumento = ?
            """, (numero_documento,))
            estudiante = cursor.fetchone()
            
        nombre_docente = request.args.get('docente', 'Nombre Docente Desconocido')
        print("Docente recibido:", nombre_docente)
        if estudiante:
            return jsonify({
            'nombres_estudiante': estudiante[0],
            'apellidos_estudiante': estudiante[1],
            'grado': estudiante[2],
            'seccion': estudiante[3],
            'jornada': estudiante[4],
            'idacu': estudiante[5],  # Nuevo
            'nom_acu': estudiante[6],
            'ape_acu': estudiante[7],
            'tel_acu': estudiante[8],
            'cor_acu': estudiante[9],
            'nombre_docente': nombre_docente
            
            })

        return jsonify({})
    except Exception as e:
        return jsonify({'error': str(e)})


    
@generar2_bp.route('/generarp', methods=['GET'])
def generar():
    registros = ver_proceso_2()
    return render_template('generar2.html', registros=registros)

def ver_proceso_2():
    try:
        if 'nombres' not in session or 'apellidos' not in session:
            flash("Sesión expirada o inválida. Inicia sesión nuevamente.", "danger")
            return None

        profesor = f"{session['nombres']} {session['apellidos']}"

        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
        SELECT * 
        FROM proceso_2
        WHERE estado = 'Activo' AND docente = ?
        '''
        cursor.execute(query, (profesor,))
        registros = cursor.fetchall()

        if not registros:
            print("No se encontraron registros en la base de datos.")
        else:
            print(f"Se encontraron {len(registros)} registros.")

        cursor.close()
        conn.close()
        return registros

    except Exception as e:
        flash(f'Error al consultar los datos de proceso_2: {str(e)}', 'danger')
        return None

@generar2_bp.route('/api/proceso_2', methods=['GET'])
def obtener_proceso_2():
    try:
        registros = ver_proceso_2()
        if registros is None:
            return jsonify({'error': 'No se encontraron registros'}), 404

        lista_registros = []
        for r in registros:
            registro_dict = {
                'id': r[0],
                'cedula': r[1],
                'nombres_estudiante': r[2],
                'apellidos_estudiante': r[3],
                'grado': r[4],
                'seccion': r[5],
                'jornada': r[6],
                'falta_cometida': r[7],
                'descargos': r[8],
                'compromiso': r[9],
                'docente': r[10],
                'estudiante1': r[15],
                'estudiante2': r[16]
                
                # agrega más campos si es necesario
            }
            lista_registros.append(registro_dict)

        return jsonify(lista_registros)
    except Exception as e:
        return jsonify({'error': str(e)}), 500