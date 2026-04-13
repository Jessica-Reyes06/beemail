import sqlite3
from datetime import datetime

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

def obtener_correos(filtro=None):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute(f'SELECT * FROM correos WHERE {filtro}')
    else:
        cursor.execute('SELECT * FROM correos ORDER BY fecha DESC')
    correos = cursor.fetchall()
    conn.close()
    return correos

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

# •••••• FILTROS POR HORARIO ••••••
def obtener_por_horario(tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM correos")
    correos = cursor.fetchall()

    resultado = []

    for correo in correos:
        fecha = correo[6]  # columna fecha

        try:
            hora = datetime.strptime(fecha[:19], "%Y-%m-%d %H:%M:%S").hour
        except:
            continue

        if tipo == "mañana" and 6 <= hora < 12:
            resultado.append(correo)

        elif tipo == "tarde" and 12 <= hora < 19:
            resultado.append(correo)

        elif tipo == "noche" and (hora >= 19 or hora < 6):
            resultado.append(correo)

    conn.close()
    return resultado

