from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import pyodbc
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Blueprint
generar3_bp = Blueprint('generar3', __name__)

# Email config
EMAIL_CONFIG = {
    'remitente': 'disproiem02@gmail.com',
    'password': 'qnsd gtce chyo lhnf',
    'servidor': 'smtp.gmail.com',
    'puerto': 587,
    'asunto': 'Notificación de proceso disciplinario'
}

def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\baselocal;DATABASE=Dispro;UID=baselocal;PWD=baselocal1085'
    )

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
        
        <h2 style="color: #2c3e50;">Notificación de proceso disciplinario numero tres</h2>

        <p style="text-align: left;">Estimado acudiente,</p>
        <p style="color: #333; font-size: 16px; margin: 10px 0;">
            El estudiante <strong style="color: red;">{estudiante_nombre} {estudiante_apellido}</strong> del grado {grado}-{seccion} ha sido registrado en un proceso disciplinario.
        </p>

        <p style="color: #333; font-size: 16px; margin: 10px 0;">
            Teniendo en cuenta los descargos presentados y el análisis del caso, se concluye que el estudiante incurrió en faltas al Pacto Social de Convivencia Institucional. Por lo tanto, se procede con la presente <strong style="color: red;">Amonestación Escrita</strong>, la cual, en caso de no ser atendida, dará lugar a la aplicación de la siguiente fase del proceso disciplinario.
        </p>

        <p style="color: #333; font-size: 16px; margin: 10px 0;">Este es un mensaje automático. Por favor no responder.</p>

        <div style="text-align: center; font-size: 12px; color: #888; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px;">
            <p>Institución Educativa INEM</p>
        </div>
    </div>
</body>
</html>


    """
    mensaje.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(EMAIL_CONFIG['servidor'], EMAIL_CONFIG['puerto']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['remitente'], EMAIL_CONFIG['password'])
            server.send_message(mensaje)
        return True
    except Exception as e:
        current_app.logger.error(f"Error al enviar correo: {str(e)}")
        return False

@generar3_bp.route('/registrar_proceso3', methods=['POST'])
def registrar_proceso3():
    data = request.form
    try:
        foto = request.files.get('rutafoto')
        estudio_caso = None

        if foto and foto.filename:
            filename = secure_filename(foto.filename)
            folder = os.path.join(current_app.root_path, 'static', 'evidencia_fotos_3')
            os.makedirs(folder, exist_ok=True)
            foto_path = os.path.join(folder, filename)
            foto.save(foto_path)
            estudio_caso = f'static/evidencia_fotos_3/{filename}'

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proceso_3 (
                    identificacion, nombres, apellidos, grado, seccion, jornada,
                    idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente,
                    telefono, estado, pacto_social, descargos, estudio_caso, jefe_seccion, docente
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Activo', ?, ?, ?, ?, ?)
            """, (
                data.get('numeroTI'), data.get('nombresEstudiante'), data.get('apellidosEstudiante'),
                data.get('grado'), data.get('seccion'), data.get('jornada'),
                data.get('idacu'), data.get('nom_acu'), data.get('ape_acu'),
                data.get('cor_acu'), data.get('tel_acu'),
                data.get('pactosocial'),
                data.get('descargos'),
                data.get('caso'),
                data.get('jefe'), 
                data.get('docente')
                
            ))
            conn.commit()

        if data.get('cor_acu'):
            enviar_correo(
                data.get('cor_acu'),
                data.get('nombresEstudiante'),
                data.get('apellidosEstudiante'),
                data.get('grado'),
                data.get('seccion'),
                data.get('pactosocial'),
                data.get('descargos'),
                'Evidencia cargada' if estudio_caso else 'Sin evidencia'
            )

        flash("Proceso registrado exitosamente.", "success")
        return redirect(url_for('generar3.generarf'))

    except Exception as e:
        flash(f"Error al registrar: {str(e)}", "danger")
        return redirect(url_for('generar3.generarf'))

@generar3_bp.route('/generarf', methods=['GET'])
def generarf():
    registros = ver_proceso_3()
    return render_template('generar3.html', registros=registros)

def ver_proceso_3():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
        SELECT * 
        FROM proceso_3
        WHERE estado = 'Activo'
        '''
        cursor.execute(query)
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
# Ruta: Buscar estudiante en proceso_2
@generar3_bp.route('/buscar_estudiante_generar3', methods=['GET'])
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
    
    
@generar3_bp.route('/api/proceso_3', methods=['GET'])
def obtener_proceso_3():
    try:
        registros = ver_proceso_3()
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
                'idacudiente': r[7],
                'nombre_acudiente': r[8],
                'apellidos_acudiente': r[9],
                'correo_acudiente': r[10],
                'pactosocial': r[13],
                'descargos': r[14],
                'estudio_caso': r[14],
                'jefe_seccion': r[16],
                'docente': r[17]
                
                # agrega más campos si es necesario
            }
            lista_registros.append(registro_dict)

        return jsonify(lista_registros)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
