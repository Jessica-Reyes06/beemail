import smtplib #Simple Mail Transfer Protocol
from customtkinter import *
import os
from email.message import EmailMessage

def validar_login(email, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) #clase que implementa SMTP
        server.starttls()   #iniciar el modo seguro (TLS) para cifrar la conexión
        server.login(email, password)
        server.quit() #cerrar la conexión con el servidor SMTP
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Error de autenticación: {str(e)}")
        return False
    except Exception as e:
        print(f"Error al conectar con el servidor SMTP: {str(e)}")
        return False

def cambiar_modo():
    if get_appearance_mode() == "Light":
        set_appearance_mode("dark")
    else:
        set_appearance_mode("light")

# Checkbox para mostrar/ocultar contraseña
def show_password(password_entry, variable):
	if variable.get():
		password_entry.configure(show="")
	else:
		password_entry.configure(show="*")

def obtener_cuentas_configuradas() -> dict[str, str]:
    cuentas = {}
    for idx in (1, 2):
        correo = os.environ.get(f"EMAIL_USER_{idx}", "").strip()
        password = os.environ.get(f"EMAIL_PASS_{idx}", "")
        if correo and password:
            cuentas[correo] = password
    return cuentas

def enviar_correo(remitente, password, destinatario, asunto, cuerpo, archivos=None):
    msg = EmailMessage()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.set_content(cuerpo)

    # Adjuntar archivos si existen
    if archivos:
        for archivo in archivos:
            with open(archivo, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(archivo)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
    


