from flask import Flask, render_template, request, redirect, url_for, flash, session
from docente import docente_bp
from db import get_db_connection  # Ahora importamos desde db.p
from collections import Counter
import json
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage
from generar2 import generar2_bp  # importa este archivo
from generar3 import generar3_bp  # importar el nuevo blueprint
from estado_estudiantil import estado_estudiantil
from functools import wraps


# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Decorador para verificar sesión de usuario
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Debes iniciar sesión para acceder a esta sección.", "error")
            return redirect(url_for('login'))  # Asegúrate de que exista esta ruta
        return f(*args, **kwargs)
    return decorated_function
app.secret_key = 'Dumes'  # Clave secreta para la sesión

# Credenciales del administrador (no se pueden cambiar)
ADMIN_USUARIO = "odin"
ADMIN_CONTRASENA = "odin"
ADMIN_ROL = "Administrador"

# Registrar los blueprints
app.register_blueprint(docente_bp)
app.register_blueprint(generar2_bp)
app.register_blueprint(generar3_bp)
app.register_blueprint(estado_estudiantil)





@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('username')  # Campo nuevo
        password = request.form.get('password')
        
        # Validar credenciales del administrador (odin)
        if usuario == ADMIN_USUARIO and password == ADMIN_CONTRASENA:
            session['usuario'] = ADMIN_USUARIO
            session['rol'] = ADMIN_ROL
            session['nombres'] = "Odin"
            session['apellidos'] = "Administrador"
            session['correo'] = "odin@example.com"
            return redirect(url_for('module'))

        # Validar credenciales de usuarios normales
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT Rol, NombresCompletos, ApellidosUsuario, Contrasena, CorreoElectronico, NoCedula FROM Usuarios 
            WHERE usuario = ? AND Contrasena = ? 
        ''', (usuario, password))  # Ahora valida "usuario" y "contraseña"
        usuario_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario_data:
            session['usuario'] = usuario
            session['rol'] = usuario_data[0]
            session['nombres'] = usuario_data[1]
            session['apellidos'] = usuario_data[2]
            session['correo'] = usuario_data[4]

            # Redirigir según el rol
            if usuario_data[0] == "Acudiente":
                return redirect(url_for('Acudiente'))
            elif usuario_data[0] == "Docente":
                return redirect(url_for('docente.docente'))
            else:
                return redirect(url_for('module'))
        else:
            flash("Credenciales incorrectas. Intenta nuevamente.", "error")

    return render_template('login.html')


from flask import request, render_template, redirect, url_for, flash
from collections import Counter
import json

@app.route('/module', methods=['GET', 'POST'])
def module():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
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

            # Insertar en la base de datos
            cursor.execute('''
                INSERT INTO Estudiantes (
                    TipoDocumento, NumeroDocumento, NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
                    IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente, docente
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (tipo_documento, numero_documento, nombres_estudiante, apellidos_estudiante, grado, seccion, jornada,
                  id_acudiente, nombre_acudiente, apellido_acudiente, telefono, correo, profesor))
            
            conn.commit()
            flash("¡Estudiante registrado exitosamente!", "success")

        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar estudiante: {str(e)}", "danger")

    # Obtener estudiantes
    cursor.execute('''
        SELECT NombresEstudiante, ApellidosEstudiante, Grado, Seccion, Jornada, 
               IdAcudiente, NombreAcudiente, ApellidoAcudiente, TelefonoAcudiente, CorreoAcudiente
        FROM Estudiantes
    ''')
    estudiantes = cursor.fetchall()

    # Obtener docentes (usuarios con rol docente)
    cursor.execute('''
        SELECT NombresCompletos, ApellidosUsuario 
        FROM Usuarios 
        WHERE Rol = 'docente'
    ''')
    docentes = cursor.fetchall()

    # Contar por grado
    grados = [est[2] for est in estudiantes]
    conteo_grados = dict(Counter(grados))

    # Contar por jornada
    jornadas = [est[4] for est in estudiantes]
    conteo_jornadas = dict(Counter(jornadas))

    cursor.close()
    conn.close()

    return render_template('module.html',
                           estudiantes=estudiantes,
                           docentes=docentes,
                           conteo_grados=json.dumps(conteo_grados),
                           conteo_jornadas=json.dumps(conteo_jornadas))

@app.route('/module2')
def module2():
    # Verificar si el usuario es administrador
    # Obtener todos los usuarios registrados
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ID, Rol, NombresCompletos, ApellidosUsuario, Contrasena, NumeroTelefono, CorreoElectronico, usuario, Nocedula, tipocedula FROM Usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('module2.html', usuarios=usuarios)

@app.route('/insertar_usuario', methods=['POST'])
def insertar_usuario():

    try:
        rol = request.form['rol']
        cedula = request.form['cedulacudiente']
        tipocedula = request.form['tipocedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']
        correo = request.form['correo']
        



        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
            INSERT INTO Usuarios (Rol, NombresCompletos, ApellidosUsuario, Contrasena, NumeroTelefono, CorreoElectronico,usuario, NoCedula, tipocedula)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        cursor.execute(query, (rol, nombres, apellidos, contrasena, telefono, correo,  usuario, cedula, tipocedula))
        conn.commit()
        cursor.close()
        conn.close()

        flash("¡Usuario registrado exitosamente!", "success")
        return redirect(url_for('module2'))

    except Exception as e:
        flash(f"Error al insertar el usuario: {str(e)}", "error")
        print("Error al insertar usuario:", str(e))  # Esto va en la terminal
        return redirect(url_for('module2'))
    
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE ID = ?', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for('module2'))  # o a donde vayas luego de borrar

@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        correo = request.form['correo']
        usuario_nombre = request.form['usuario']    
        contrasena = request.form['contrasena']

        try:
            # Iniciar transacción
            conn.autocommit = False
            
            # Actualizar datos en la tabla Usuarios
            query_usuarios = '''
                UPDATE Usuarios
                SET NombresCompletos = ?, ApellidosUsuario = ?, 
                    NumeroTelefono = ?, CorreoElectronico = ?, 
                    Usuario = ?, Contrasena = ?
                WHERE ID = ?
            '''
            cursor.execute(query_usuarios, (nombres, apellidos, telefono, correo, usuario_nombre, contrasena, id))
            
            # Actualizar campos en la tabla Estudiantes
            query_estudiantes = '''
                UPDATE Estudiantes
                SET CorreoAcudiente = ?, NombreAcudiente = ?, ApellidoAcudiente = ?, TelefonoAcudiente = ?
                WHERE IdAcudiente = ?
            '''
            cursor.execute(query_estudiantes, (correo, nombres, apellidos, telefono, cedula))

            # Actualizar campos en la tabla proceso_1
            query_proceso_1 = '''
                UPDATE proceso_1
                SET nombre_acudiente = ?, apellidos_acudiente = ?, correoacudiente = ?, telefono = ?
                WHERE idacudiente = ?
            '''
            cursor.execute(query_proceso_1, (nombres, apellidos, correo, telefono, cedula))

            # Actualizar campos en la tabla proceso_2
            query_proceso_2 = '''
                UPDATE proceso_2
                SET nombre_acudiente = ?, apellidos_acudiente = ?, correoacudiente = ?, telefono = ?
                WHERE idacudiente = ?
            '''
            cursor.execute(query_proceso_2, (nombres, apellidos, correo, telefono, cedula))
            
            # Actualizar campos en la tabla proceso_3
            query_proceso_3 = '''
                UPDATE proceso_3
                SET nombre_acudiente = ?, apellidos_acudiente = ?, correoacudiente = ?, telefono = ?
                WHERE idacudiente = ?
            '''
            cursor.execute(query_proceso_3, (nombres, apellidos, correo, telefono, cedula))
            
            # Confirmar transacción
            conn.commit()
            flash("Usuario actualizado correctamente en todas las tablas.", "success")
            
        except Exception as e:
            # Revertir transacción en caso de error
            conn.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")
            
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('module2'))

    else:
        # Método GET - Mostrar formulario con datos actuales
        cursor.execute('''
            SELECT ID, NoCedula, NombresCompletos, ApellidosUsuario, 
                   NumeroTelefono, CorreoElectronico, Usuario 
            FROM Usuarios 
            WHERE ID = ?
        ''', (id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('module2.html', usuario=usuario)



@app.route('/Acudiente')
def Acudiente():

    nombre = session.get('nombres')
    apellidos = session.get('apellidos')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta en proceso_1
    cursor.execute('''
        SELECT * FROM proceso_1 
        WHERE nombre_acudiente = ? AND apellidos_acudiente = ?
    ''', (nombre, apellidos))
    datos_proceso1 = cursor.fetchall()

    # Consulta en proceso_2
    cursor.execute('''
        SELECT * FROM proceso_2 
        WHERE nombre_acudiente = ? AND apellidos_acudiente = ?
    ''', (nombre, apellidos))
    datos_proceso2 = cursor.fetchall()

    # Consulta en proceso_3
    cursor.execute('''
        SELECT * FROM proceso_3 
        WHERE nombre_acudiente = ? AND apellidos_acudiente = ?
    ''', (nombre, apellidos))
    datos_proceso3 = cursor.fetchall()

    cursor.close()
    conn.close()

    if not (datos_proceso1 or datos_proceso2 or datos_proceso3):
        flash("No se encontraron datos asociados al acudiente logueado.", "warning")

    return render_template('Acudiente.html',
                           datos1=datos_proceso1,
                           datos2=datos_proceso2,
                           datos3=datos_proceso3)


@app.route('/module3')
def module3():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, ID,
               'fase_2' AS origen
        FROM proceso_2
        WHERE estado = 'Activo'
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, id,
               'fase_1' AS origen
        FROM proceso_1
        WHERE estado = 'Activo'
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, ID,
               'fase_3' AS origen
        FROM proceso_3
        WHERE estado = 'Activo'
    ''')
    estudiantes = cursor.fetchall()
    cantidad_casos = len(estudiantes)

    cursor.close()
    conn.close()

    return render_template('module3.html', estudiantes=estudiantes, cantidad_casos=cantidad_casos)

@app.route('/historico')
def historico():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, ID,
               'fase_2' AS origen
        FROM proceso_2
        WHERE estado = 'Cerrado'
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, id,
               'fase_1' AS origen
        FROM proceso_1
        WHERE estado = 'Cerrado'
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, ID,
               'fase_3' AS origen
        FROM proceso_3
        WHERE estado = 'Cerrado'    ''')
    cerrados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('historico.html', cerrados=cerrados)





@app.route('/cerrar_proceso/<int:identificacion>', methods=['POST'])
def cerrar_proceso(identificacion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE proceso_1 SET estado = 'Cerrado' WHERE identificacion = ?", (identificacion,))
    cursor.execute("UPDATE proceso_2 SET estado = 'Cerrado' WHERE identificacion = ?", (identificacion,))
    cursor.execute("UPDATE proceso_3 SET estado = 'Cerrado' WHERE identificacion = ?", (identificacion,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return '', 204  # Sin contenido


@app.route('/module4')
def module4():
    return render_template('module4.html')

@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/observaciones_co')
def ver_observaciones2():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                o.tipo_documento, o.numero_documento, o.nombre_estudiante, o.apellido_estudiante,
                o.grado, o.fecha, o.observacion,
                (SELECT COUNT(*) FROM Observaciones WHERE numero_documento = o.numero_documento) AS total_observaciones
            FROM Observaciones o
            ORDER BY o.fecha DESC
        ''')
        observaciones = cursor.fetchall()

        cursor.close()
        conn.close()    

        return render_template('completas.html', observaciones=observaciones)

    except Exception as e:
        flash("Ocurrió un error al cargar las observaciones.", "error")
        # Renderiza la misma plantilla con una lista vacía
        return render_template('completas.html', observaciones=[])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
