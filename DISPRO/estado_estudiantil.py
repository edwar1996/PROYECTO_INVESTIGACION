from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from db import get_db_connection
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

estado_estudiantil = Blueprint('estado_estudiantil', __name__, url_prefix='/estado_estudiantil')
@estado_estudiantil.route('/casos')
def mostrar_casos():
    conn = get_db_connection()
    cursor = conn.cursor()

    nombres_docente = session.get('nombres')
    apellidos_docente = session.get('apellidos')
    nombre_completo_docente = f"{nombres_docente} {apellidos_docente}"

    cursor.execute('''
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, falta_cometida,
               'fase_2' AS origen
        FROM proceso_2
        WHERE estado = 'Activo' AND docente = ?
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, falta_cometida,
               'fase_1' AS origen
        FROM proceso_1
        WHERE estado = 'Activo' AND docente = ?
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, descargos,
               'fase_3' AS origen
        FROM proceso_3
        WHERE estado = 'Activo' AND docente = ?
    ''', (nombre_completo_docente, nombre_completo_docente, nombre_completo_docente))
    
    estudiantes = cursor.fetchall()
    cantidad_casos = len(estudiantes)

    cursor.close()
    conn.close()

    return render_template('estado_estudiantil.html', estudiantes=estudiantes, cantidad_casos=cantidad_casos)


@estado_estudiantil.route('/historico')
def mostrar_historico():
    conn = get_db_connection()
    cursor = conn.cursor()

    nombres_docente = session.get('nombres')
    apellidos_docente = session.get('apellidos')
    nombre_completo_docente = f"{nombres_docente} {apellidos_docente}"

    cursor.execute('''
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, falta_cometida,
               'fase_2' AS origen
        FROM proceso_2
        WHERE estado = 'Cerrado' AND docente = ?
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, falta_cometida,
               'fase_1' AS origen
        FROM proceso_1
        WHERE estado = 'Cerrado' AND docente = ?
        UNION ALL
        SELECT identificacion, nombres, apellidos, grado, seccion, jornada, 
               idacudiente, nombre_acudiente, apellidos_acudiente, correoacudiente, 
               telefono, estado, descargos,
               'fase_3' AS origen
        FROM proceso_3
        WHERE estado = 'Cerrado' AND docente = ?
    ''', (nombre_completo_docente, nombre_completo_docente, nombre_completo_docente))

    cerrados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('historico_doc.html', cerrados=cerrados)


@estado_estudiantil.route('/cerrar_proceso2/<int:identificacion>', methods=['POST'])
def cerrar_proceso2(identificacion):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener nombre completo del docente desde la sesión
    nombres_docente = session.get('nombres')
    apellidos_docente = session.get('apellidos')
    nombre_completo_docente = f"{nombres_docente} {apellidos_docente}"

    # Actualizar estado en proceso_3
    cursor.execute('''
        UPDATE proceso_3
        SET estado = 'Cerrado'
        WHERE identificacion = ? AND docente = ?
    ''', (identificacion, nombre_completo_docente))

    # Actualizar estado en proceso_2
    cursor.execute('''
        UPDATE proceso_2
        SET estado = 'Cerrado'
        WHERE identificacion = ? AND docente = ?
    ''', (identificacion, nombre_completo_docente))

    # Actualizar estado en proceso_1
    cursor.execute('''
        UPDATE proceso_1
        SET estado = 'Cerrado'
        WHERE identificacion = ? AND docente = ?
    ''', (identificacion, nombre_completo_docente))

    conn.commit()
    cursor.close()
    conn.close()

    return '', 204  # Éxito sin contenido

