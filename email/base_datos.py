import sqlite3
from datetime import datetime
from email.utils import parsedate_to_datetime

DB_NAME = 'correos.db'

def conectar():
    return sqlite3.connect(DB_NAME)

def inicializar_bd():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS correos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            remitente TEXT,
            destinatario TEXT,
            asunto TEXT,
            cuerpo TEXT,
            fecha TEXT,
            leido INTEGER DEFAULT 0,
            importante INTEGER DEFAULT 0,
            borrador INTEGER DEFAULT 0,
            spam INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            nombre TEXT,
            UNIQUE(email)
        )
    ''')

    conn.commit()
    conn.close()

def guardar_correo(remitente, destinatario, asunto, cuerpo, fecha=None, leido=0, importante=0, borrador=0, spam=0, message_id=None):
    if fecha is None:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if message_id is None:
        # Si no se proporciona, usa asunto+remitente+fecha como fallback (menos robusto)
        message_id = f"{asunto}_{remitente}_{fecha}"
    conn = conectar()
    cursor = conn.cursor()
    # Verifica si ya existe un correo con ese message_id
    cursor.execute('SELECT id FROM correos WHERE message_id=?', (message_id,))
    if cursor.fetchone():
        conn.close()
        return  # Ya existe, no insertar duplicado
    cursor.execute('''
        INSERT INTO correos (message_id, remitente, destinatario, asunto, cuerpo, fecha, leido, importante, borrador, spam)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (message_id, remitente, destinatario, asunto, cuerpo, fecha, leido, importante, borrador, spam))
    conn.commit()
    conn.close()

def eliminar_correo(correo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM correos WHERE id=?', (correo_id,))
    conn.commit()
    conn.close()

def marcar_leido(correo_id, leido=1):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE correos SET leido=? WHERE id=?', (leido, correo_id))
    conn.commit()
    conn.close()

# Llama a inicializar_bd() al inicio de tu app para crear la tabla si no existe
################################################

#•••••• FUNCIONES PARA FILTRAR CORREOS ••••••
def obtener_correos(filtro=None):
    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT * FROM correos"
    
    if filtro:
        query += f" WHERE {filtro}"
    
    query += " ORDER BY fecha DESC"

    cursor.execute(query)
    correos = cursor.fetchall()
    conn.close()
    
    return correos

# Función para buscar correos por texto en remitente, destinatario, asunto o cuerpo
def buscar_correos(texto):
    conn = conectar()
    cursor = conn.cursor()

    termino = f"%{(texto or '').strip()}%"
    cursor.execute(
        '''
        SELECT *
        FROM correos
        WHERE remitente LIKE ?
           OR destinatario LIKE ?
           OR asunto LIKE ?
        ORDER BY fecha DESC
        ''',
        (termino, termino, termino),
    )

    correos = cursor.fetchall()
    conn.close()
    return correos

# •••••• FILTROS POR HORARIO ••••••
def _obtener_hora_desde_fecha(fecha):
    if not fecha:
        return None

    fecha_str = str(fecha).strip()

    # Formato local guardado por la app: 2026-04-16 14:30:00
    try:
        return datetime.strptime(fecha_str[:19], "%Y-%m-%d %H:%M:%S").hour
    except ValueError:
        pass

    # Formato típico de cabecera de correo: Thu, 16 Apr 2026 14:30:00 -0500
    try:
        return parsedate_to_datetime(fecha_str).hour
    except (TypeError, ValueError):
        return None


def obtener_por_horario(tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM correos")
    correos = cursor.fetchall()

    resultado = []

    for correo in correos:
        fecha = correo[6]  # columna fecha

        hora = _obtener_hora_desde_fecha(fecha)
        if hora is None:
            continue

        if tipo == "mañana" and 6 <= hora < 12:
            resultado.append(correo)

        elif tipo == "tarde" and 12 <= hora < 19:
            resultado.append(correo)

        elif tipo == "noche" and (hora >= 19 or hora < 6):
            resultado.append(correo)

    conn.close()
    return resultado

# •••••• FUNCIONES PARA GESTIONAR CONTACTOS ••••••
def guardar_contacto(email, nombre=""):
    """Guarda un contacto en la base de datos si no existe ya"""
    conn = conectar()
    cursor = conn.cursor()
    
    # Verifica si el contacto ya existe
    cursor.execute('SELECT id FROM contactos WHERE email=?', (email,))
    if cursor.fetchone():
        conn.close()
        return False  # Ya existe
    
    cursor.execute('''
        INSERT INTO contactos (email, nombre)
        VALUES (?, ?)
    ''', (email, nombre))
    conn.commit()
    conn.close()
    return True  # Se agregó correctamente

def obtener_contactos():
    """Obtiene todos los contactos ordenados por nombre"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, nombre FROM contactos ORDER BY nombre ASC')
    contactos = cursor.fetchall()
    conn.close()
    return contactos

# Función para buscar contactos por email o nombre
def buscar_contactos(texto):
    conn = conectar()
    cursor = conn.cursor()

    termino = f"%{(texto or '').strip()}%"
    cursor.execute(
        '''
        SELECT id, email, nombre
        FROM contactos
        WHERE email LIKE ?
           OR nombre LIKE ?
        ORDER BY nombre ASC
        ''',
        (termino, termino),
    )

    contactos = cursor.fetchall()
    conn.close()
    return contactos

def obtener_contacto_por_email(email):
    """Obtiene un contacto específico por email"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, nombre FROM contactos WHERE email=?', (email,))
    contacto = cursor.fetchone()
    conn.close()
    return contacto

def actualizar_nombre_contacto(email, nombre):
    """Actualiza el nombre de un contacto"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE contactos SET nombre=? WHERE email=?', (nombre, email))
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado

def eliminar_contacto(email):
    """Elimina un contacto por email"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contactos WHERE email=?', (email,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado

