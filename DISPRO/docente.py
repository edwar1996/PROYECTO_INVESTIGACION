from flask import Blueprint, render_template,session, request, redirect, url_for, flash, jsonify, current_app
from db import get_db_connection  # Importar la función de conexión
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps


# Definir el Blueprint para 'docente'
docente_bp = Blueprint('docente', __name__)

# Decorador para verificar sesión de usuario
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Debes iniciar sesión para acceder a esta sección.", "error")
            return redirect(url_for('login'))  # Asegúrate de que exista esta ruta
        return f(*args, **kwargs)
    return decorated_function

# Configuración del correo (ajusta estos valores)
EMAIL_CONFIG = {
    'remitente': 'disproiem02@gmail.com',
    'password': 'qnsd gtce chyo lhnf',
    'servidor': 'smtp.gmail.com',
    'puerto': 587,
    'asunto': 'Notificación de proceso disciplinario'
}

def enviar_correo(destinatario, estudiante_nombre, estudiante_apellido, grado, seccion, falta_cometida, descargos, compromiso):
    """Función para enviar correo electrónico al acudiente"""
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
        
        <h2 style="color: #2c3e50;">Notificación de proceso disciplinario</h2>

        <p style="text-align: left;">Estimado acudiente,</p>

        <p style="text-align: left;">
            El estudiante <strong>{estudiante_nombre} {estudiante_apellido}</strong> del grado {grado}-{seccion} 
            ha sido registrado en un proceso disciplinario.
        </p>
        
        <h3 style="color: #2c3e50; text-align: left;">Detalles del proceso:</h3>
        <ul style="text-align: left;">
            <li><strong>Falta cometida:</strong> {falta_cometida}</li>
            <li><strong>Descargos del estudiante:</strong> {descargos}</li>
            <li><strong>Compromisos adquiridos:</strong> {compromiso}</li>
        </ul>
        
        <p style="margin-top: 20px; text-align: left;">
            Por favor contacte a la institución para más información sobre este proceso.
        </p>

        <p style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; text-align: left;">
            Atentamente,<br>
            <strong>Institución Educativa INEM</strong><br>
            <small>Este es un mensaje automático, por favor no responder</small>
        </p>
    </div>
</body>

    </html>
    """
    
    mensaje.attach(MIMEText(html, 'html'))
    
    try:
        server = smtplib.SMTP(EMAIL_CONFIG['servidor'], EMAIL_CONFIG['puerto'])
        server.starttls()
        server.login(EMAIL_CONFIG['remitente'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['remitente'], destinatario, mensaje.as_string())
        server.quit()
        current_app.logger.info(f"Correo enviado exitosamente a {destinatario}")
        return True
    except Exception as e:
        current_app.logger.error(f"Error al enviar correo: {str(e)}")
        return False

# Ruta para la página 'generar'
@docente_bp.route('/generar', methods=['GET'])
def generar():
    registros = ver_proceso_1()
    return render_template('generar.html', registros=registros)

def ver_proceso_1():
    try:

        # Obtener el nombre completo del docente desde la sesión
        profesor = f"{session['nombres']} {session['apellidos']}"

        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, falta_cometida, descargos, compromiso, rutafoto
        FROM proceso_1
        WHERE docente = ?
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
        flash(f'Error al consultar los datos de proceso_1: {str(e)}', 'danger')
        return None
    
@docente_bp.route('/generar2')
def generar2():
    return render_template('generar2.html')

@docente_bp.route('/generar3')
def generar3():
    return render_template('generar3.html')

@docente_bp.route('/docente', methods=['GET', 'POST'])
def docente():
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            conn = get_db_connection()
            cursor = conn.cursor()

            if action == 'delete':
                tipo_documento = request.form['tipo_documento']
                numero_documento = request.form['numero_documento']
                query = '''
                    DELETE FROM Estudiantes
                    WHERE TipoDocumento = ? AND NumeroDocumento = ?
                '''
                cursor.execute(query, (tipo_documento, numero_documento))
                flash("¡Estudiante eliminado exitosamente!", "success")

            elif action == 'registrar_observacion':
                tipo_documento = request.form['tipo_documento']
                numero_documento = request.form['numero_documento']
                nombre_estudiante = request.form['nombre_estudiante']
                apellido_estudiante = request.form['apellido_estudiante']
                grado = request.form['grado']
                observacion = request.form['observacion']
                profesor = request.form['profesor']

                if not all([tipo_documento, numero_documento, nombre_estudiante, apellido_estudiante, grado, observacion]):
                    flash("Faltan datos necesarios para registrar la observación.", "error")
                    return redirect(url_for('docente.docente'))

              

            


                cursor.execute('SELECT COUNT(*) FROM Observaciones WHERE numero_documento = ?', (numero_documento,))
                observaciones_count = cursor.fetchone()[0]

                if observaciones_count >= 3:
                    flash("No se pueden registrar más de 3 observaciones para este estudiante.", "error")
                    return redirect(url_for('docente.docente'))

                cursor.execute('''
                    INSERT INTO Observaciones (
                        tipo_documento, numero_documento, nombre_estudiante, apellido_estudiante, grado, fecha, observacion, profesor
                    ) VALUES (?, ?, ?, ?, ?, GETDATE(), ?, ?)
                ''', (tipo_documento, numero_documento, nombre_estudiante, apellido_estudiante, grado, observacion, profesor))


                conn.commit()
                flash("¡Observación registrada exitosamente!", "success")
                return redirect(url_for('docente.docente'))



            elif action == 'edit':
                tipo_documento = request.form['tipo_documento']
                numero_documento = request.form['numero_documento']
                tipo_documento_original = request.form.get('tipo_documento_original')
                nombres_estudiante = request.form['nombres_estudiante']
                apellidos_estudiante = request.form['apellidos_estudiante']
                grado = request.form['grado']
                seccion = request.form['seccion']
                jornada = request.form['jornada']
                id_acudiente = request.form['id_acudiente']
                nombre_acudiente = request.form['nombre_acudiente']
                apellido_acudiente = request.form['apellido_acudiente']
                telefono = request.form['telefono']
                correo = request.form['correo']

                cursor.execute('''
                    UPDATE Estudiantes
                    SET TipoDocumento=?, NumeroDocumento=?, NombresEstudiante=?, ApellidosEstudiante=?, Grado=?, Seccion=?, Jornada=?, 
                        IdAcudiente=?, NombreAcudiente=?, ApellidoAcudiente=?, TelefonoAcudiente=?, CorreoAcudiente=?
                    WHERE TipoDocumento=? AND NumeroDocumento=?
                ''', (tipo_documento, numero_documento, nombres_estudiante, apellidos_estudiante, grado, seccion, jornada,
                      id_acudiente, nombre_acudiente, apellido_acudiente, telefono, correo,
                      tipo_documento_original, numero_documento))
                flash("¡Estudiante actualizado exitosamente!", "success")

            else:
                tipo_documento = request.form['tipo_documento']
                numero_documento = request.form['numero_documento']
                nombres_estudiante = request.form['nombres_estudiante']
                apellidos_estudiante = request.form['apellidos_estudiante']
                grado = request.form['grado']
                seccion = request.form['seccion']
                jornada = request.form['jornada']
                id_acudiente = request.form['id_acudiente']
                nombre_acudiente = request.form['nombre_acudiente']
                apellido_acudiente = request.form['apellido_acudiente']
                telefono = request.form['telefono']
                correo = request.form['correo']
                profesor = request.form['profesor']

                cursor.execute('''
                    INSERT INTO Estudiantes (
                        TipoDocumento, NumeroDocumento, NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
                        IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente, docente
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (tipo_documento, numero_documento, nombres_estudiante, apellidos_estudiante, grado, seccion, jornada,
                      id_acudiente, nombre_acudiente, apellido_acudiente, telefono, correo, profesor))
                flash("¡Estudiante registrado exitosamente!", "success")

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('docente.docente'))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('docente.docente'))

    try:

        profesor = f"{session['nombres']} {session['apellidos']}"
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT TipoDocumento, NumeroDocumento, NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
                   IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente
            FROM Estudiantes
            WHERE docente = ?
        ''', (profesor,))
        estudiantes = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('docente.html', estudiantes=estudiantes, profesor=profesor)

    except Exception as e:
        flash("Ocurrió un error al cargar la página del docente.", "error")
        return redirect(url_for('login'))
    
@docente_bp.route('/observaciones')
def ver_observaciones():
    try:

        profesor = f"{session['nombres']} {session['apellidos']}"
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                o.tipo_documento, o.numero_documento, o.nombre_estudiante, o.apellido_estudiante,
                o.grado, o.fecha, o.observacion,
                (SELECT COUNT(*) FROM Observaciones WHERE numero_documento = o.numero_documento) AS total_observaciones
            FROM Observaciones o
            WHERE o.profesor = ?
            ORDER BY o.fecha DESC
        ''', (profesor,))
        observaciones = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('observaciones.html', observaciones=observaciones, profesor=profesor)

    except Exception as e:
        flash("Ocurrió un error al cargar las observaciones.", "error")
        return redirect(url_for('docente'))
  

@docente_bp.route('/buscar_estudiante', methods=['GET', 'POST'])
def buscar_estudiante():
    if request.method == 'POST':
        numero_ti = request.form.get('numeroTI')
        nombres_estudiante = request.form.get('nombresEstudiante')
        apellidos_estudiante = request.form.get('apellidosEstudiante')
        grado = request.form.get('grado')
        seccion = request.form.get('seccion')
        jornada = request.form.get('jornada')
        idacu = request.form.get('idacu')
        nom_acu = request.form.get('nom_acu')
        ape_acu = request.form.get('ape_acu')
        tel_acu = request.form.get('tel_acu')
        cor_acu = request.form.get('cor_acu')
        falta_cometida = request.form.get('faltaCometida')
        descargos = request.form.get('descargos')
        compromisso_estudante = request.form.get('compromissoEstudante')
      

        foto = request.files.get('rutafoto')
        rutafoto = None

        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            folder_path = os.path.join(current_app.root_path, 'static', 'evidencia_fotos')
            os.makedirs(folder_path, exist_ok=True)
            foto_path = os.path.join(folder_path, filename)
            foto.save(foto_path)
            rutafoto = f'static/evidencia_fotos/{filename}'
        profesor = request.form.get('profesor')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = '''
            INSERT INTO proceso_1 (
                identificacion, nombres, apellidos, grado, seccion, jornada, 
                idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
                telefono, estado, falta_cometida, descargos, compromiso, rutafoto, docente
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Activo', ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (
                numero_ti, nombres_estudiante, apellidos_estudiante, grado, seccion, jornada,
                idacu, nom_acu, ape_acu, cor_acu, tel_acu, falta_cometida, descargos, compromisso_estudante, rutafoto, profesor
            ))
            conn.commit()

            # Enviar correo al acudiente después de insertar el registro
            if cor_acu:
                if enviar_correo(
                    destinatario=cor_acu,
                    estudiante_nombre=nombres_estudiante,
                    estudiante_apellido=apellidos_estudiante,
                    grado=grado,
                    seccion=seccion,
                    falta_cometida=falta_cometida,
                    descargos=descargos,
                    compromiso=compromisso_estudante
                ):
                    flash('Correo enviado exitosamente al acudiente', 'success')
                else:
                    flash('Registro guardado pero no se pudo enviar el correo', 'warning')

            cursor.close()
            conn.close()

            flash('Datos insertados correctamente.', 'success')
            return redirect(url_for('docente.generar'))

        except Exception as e:
            flash(f'Error al insertar los datos: {str(e)}', 'danger')
            return redirect(url_for('docente.generar'))

    # GET: búsqueda de estudiante
    numero_documento = request.args.get('numero_documento')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = '''
        SELECT NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
               IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente
        FROM Estudiantes
        WHERE NumeroDocumento = ?
        '''
        cursor.execute(query, (numero_documento,))
        estudiante = cursor.fetchone()
        cursor.close()
        conn.close()

        if estudiante:
            return jsonify({
                'nombres_estudiante': estudiante[0],
                'apellidos_estudiante': estudiante[1],
                'grado': estudiante[2],
                'seccion': estudiante[3],
                'jornada': estudiante[4],
                'idacu': estudiante[5],
                'nom_acu': estudiante[6],
                'ape_acu': estudiante[7],
                'tel_acu': estudiante[8],
                'cor_acu': estudiante[9]
            })
        else:
            return jsonify({key: None for key in [
                'nombres_estudiante', 'apellidos_estudiante', 'grado', 'seccion', 'jornada',
                'idacu', 'nom_acu', 'ape_acu', 'tel_acu', 'cor_acu'
            ]})
    except Exception as e:
        flash(f'Error al consultar el estudiante: {str(e)}', 'danger')
        return jsonify({key: None for key in [
            'nombres_estudiante', 'apellidos_estudiante', 'grado', 'seccion', 'jornada',
            'idacu', 'nom_acu', 'ape_acu', 'tel_acu', 'cor_acu'
        ]})

@docente_bp.route('/buscar_estudiante_pdf', methods=['GET'])
def buscar_estudiante_pdf():
    numero_documento = request.args.get('numero_documento')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = '''
        SELECT nombres, apellidos, grado, seccion, jornada, 
               nombre_acudiente, apellidos_acudiente, telefono, correoacudiente,
               falta_cometida, descargos, compromiso, rutafoto
        FROM proceso_1
        WHERE identificacion = ?
        '''
        cursor.execute(query, (numero_documento,))
        estudiante = cursor.fetchone()
        cursor.close()
        conn.close()

        if estudiante:
            return jsonify({
                'nombres_estudiante': estudiante[0],
                'apellidos_estudiante': estudiante[1],
                'grado': estudiante[2],
                'seccion': estudiante[3],
                'jornada': estudiante[4],
                'nom_acu': estudiante[5],
                'ape_acu': estudiante[6],
                'tel_acu': estudiante[7],
                'cor_acu': estudiante[8],
                'falta_cometida': estudiante[9],
                'descargos': estudiante[10],
                'compromiso': estudiante[11],
                'rutafoto': estudiante[12]
            })
        else:
            return jsonify({})
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@docente_bp.route('/buscar_acudiente', methods=['GET'])
def buscar_acudiente():
    cedula = request.args.get('cedula')
    if not cedula:
        return jsonify({'status': 'error', 'message': 'No se proporcionó cédula'})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT NombresCompletos, ApellidosUsuario, NumeroTelefono, CorreoElectronico
        FROM Usuarios
        WHERE Rol = 'Acudiente' AND NoCedula = ?
    ''', (cedula,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            'status': 'success',
            'nombre': row[0],
            'apellido': row[1],
            'telefono': row[2],
            'correo': row[3]
        })
    else:
        return jsonify({'status': 'not_found'})

    
    
