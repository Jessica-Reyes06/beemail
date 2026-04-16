from customtkinter import *
from PIL import Image
from funciones import validar_login, show_password
from plantilla import VentanaPrincipal

# •••••• VENTANA LOGIN••••••
login=CTk()
login.title("Login")
login.geometry("500x400+300+200")
login.resizable(False, False)
login.rowconfigure(0, weight=1)
login.rowconfigure(1, weight=1)

fondo = CTkImage(Image.open("imagenes/login.jpg"), size=(500, 400))

label_fondo = CTkLabel(login, image=fondo, text="")
label_fondo.grid(row=0, column=0, rowspan=2, sticky="nsew")

frame_login = CTkFrame(login, fg_color="#eef3f9", corner_radius=0)
frame_login.grid(row=1, column=0)
frame_login.grid_columnconfigure(0, weight=1)
frame_login.grid_rowconfigure(0, weight=1)
frame_login.grid_rowconfigure(1, weight=1)
frame_login.grid_rowconfigure(2, weight=1)
frame_login.grid_rowconfigure(3, weight=1)
frame_login.grid_rowconfigure(4, weight=1)

logo=CTkImage(Image.open("imagenes/abejita1.png"), size=(220, 80))
label_logo=CTkLabel(login, image=logo, text="")
label_logo.grid(row=0, column=0, padx=10)
#6d8eb9
bienvenida =CTkLabel(frame_login, text="Welcome!", text_color="black", bg_color= "#eef3f9",font=CTkFont(family="Arial", size=20))
bienvenida.grid(row=1, column=0, padx=10, pady=5)
email=CTkEntry(frame_login, placeholder_text="Email",text_color="#305177",  width=200, fg_color="white", font=CTkFont(family="Arial", size=16))
email.grid(row=2, column=0, padx=20, pady=10)

password=CTkEntry(frame_login, placeholder_text="Password", width=200, fg_color="white", font=CTkFont(family="Arial", size=16), show="*", text_color="#305177")
password.grid(row=3, column=0, padx=20, pady=10)

mostrar_contra = BooleanVar()
checkbox_mostrar = CTkCheckBox(frame_login, text="Mostrar contraseña",text_color="#305177", variable=mostrar_contra, command=lambda: show_password(password, mostrar_contra))
checkbox_mostrar.grid(row=4, column=0, padx=20, pady=(0,10), sticky="w")

mensaje_error = CTkLabel(frame_login, text="", text_color="red", bg_color="#eef3f9", font=CTkFont(family="Arial", size=12))
mensaje_error.grid(row=6, column=0, padx=20, pady=(0,10))

def intentar_login():
    correo = email.get().strip()
    clave = password.get()

    if validar_login(correo, clave) == False:
        mensaje_error.configure(text="Credenciales incorrectas")
    else:
        mensaje_error.configure(text="")
        login.destroy()
        app = VentanaPrincipal(correo_actual=correo, password=clave)
        app.mostrar()

boton_login = CTkButton(frame_login, text="Iniciar sesión", font=CTkFont(family="Arial", size=16), width=150, fg_color="#305177", command=intentar_login)
boton_login.grid(row=5, column=0, padx=20, pady=20)

login.mainloop()