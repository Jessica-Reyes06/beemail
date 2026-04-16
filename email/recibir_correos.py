import imaplib
import email
from email.header import decode_header
import os
from base_datos import guardar_correo, guardar_contacto
import re

def extraer_email(direccion):
    """Extrae el email de una dirección que puede estar en formato 'Nombre <email@example.com>' o solo 'email@example.com'"""
    if not direccion:
        return None
    
    # Busca email en formato <email@example.com>
    match = re.search(r'<([^>]+)>', direccion)
    if match:
        return match.group(1).strip()
    
    # Si no encuentra entre < >, intenta extraer directamente
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, direccion)
    if match:
        return match.group()
    
    return direccion.strip()  # Si no encuentra patrón, devuelve la dirección completa

def extraer_nombre(direccion):
    """Extrae el nombre de una dirección de email"""
    if not direccion:
        return ""
    
    # Si está en formato "Nombre <email@example.com>", extrae el nombre
    match = re.match(r'^([^<]+)<', direccion)
    if match:
        return match.group(1).strip()
    
    return ""  # Devuelve vacío si no hay nombre

def recibir_correos(remitente, password, n=10):
    # Conexión a Gmail IMAP
    imap_host = 'imap.gmail.com'
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(remitente, password)
    # --- INBOX ---
    imap.select('inbox')
    status, messages = imap.search(None, 'ALL')
    if status == 'OK':
        mail_ids = messages[0].split()
        ultimos = mail_ids[-n:]
        for num in reversed(ultimos):
            result = imap.fetch(num, '(RFC822)')
            if result[0] != 'OK':
                print(f"Error al recuperar el correo {num}")
                continue
            msg_data = result[1]
            msg = email.message_from_bytes(msg_data[0][1])
            remitente_ = msg.get('From', '')
            destinatario_ = msg.get('To', '')
            asunto_, encoding = decode_header(msg.get('Subject', ''))[0]
            if isinstance(asunto_, bytes):
                asunto_ = asunto_.decode(encoding or 'utf-8', errors='ignore')
            cuerpo = ''
            if msg.is_multipart():
                for part in msg.walk():
                    tipo_contenido = part.get_content_type()
                    disposicion_contenido = str(part.get('Content-Disposition'))
                    if tipo_contenido == 'text/plain' and 'attachment' not in disposicion_contenido:
                        try:
                            cuerpo = part.get_payload(decode=True).decode()
                        except:
                            cuerpo = ''
                        break
            else:
                try:
                    cuerpo = msg.get_payload(decode=True).decode()
                except:
                    cuerpo = ''
            fecha = msg.get('Date', '')
            guardar_correo(remitente_, destinatario_, asunto_, cuerpo, fecha)
            
            # Extraer email y nombre del remitente para guardarlo como contacto
            email_remitente = extraer_email(remitente_)
            if email_remitente:
                guardar_contacto(email_remitente, "")

    # --- BORRADORES ---
    try:
        imap.select('"[Gmail]/Drafts"')
    except:
        try:
            imap.select('Drafts')
        except:
            print('No se pudo acceder a la carpeta de borradores.')
            return
    status, messages = imap.search(None, 'ALL')
    if status == 'OK':
        mail_ids = messages[0].split()
        ultimos = mail_ids[-n:]
        for num in reversed(ultimos):
            result = imap.fetch(num, '(RFC822)')
            if result[0] != 'OK':
                print(f"Error al recuperar el borrador {num}")
                continue
            msg_data = result[1]
            msg = email.message_from_bytes(msg_data[0][1])
            remitente_ = msg.get('From', '')
            destinatario_ = msg.get('To', '')
            asunto_, encoding = decode_header(msg.get('Subject', ''))[0]
            if isinstance(asunto_, bytes):
                asunto_ = asunto_.decode(encoding or 'utf-8', errors='ignore')
            cuerpo = ''
            if msg.is_multipart():
                for part in msg.walk():
                    tipo_contenido = part.get_content_type()
                    disposicion_contenido = str(part.get('Content-Disposition'))
                    if tipo_contenido == 'text/plain' and 'attachment' not in disposicion_contenido:
                        try:
                            cuerpo = part.get_payload(decode=True).decode()
                        except:
                            cuerpo = ''
                        break
            else:
                try:
                    cuerpo = msg.get_payload(decode=True).decode()
                except:
                    cuerpo = ''
            fecha = msg.get('Date', '')
            guardar_correo(remitente_, destinatario_, asunto_, cuerpo, fecha, borrador=1)
            
            # Extraer email y nombre del remitente para guardarlo como contacto
            email_remitente = extraer_email(remitente_)
            if email_remitente:
                guardar_contacto(email_remitente, "")
    imap.logout()
