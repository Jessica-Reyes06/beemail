from CTkMessagebox import CTkMessagebox
from funciones import enviar_correo
import os
from customtkinter import *
from datetime import datetime
from tkinter import filedialog

class RedactarCorreo:
    def __init__(self, frame_redactar: CTkFrame):
        self.frame = frame_redactar

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.encabezado = CTkFrame(self.frame, width=400, height=50, fg_color="#FFF7CF")
        self.encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", padx=50, pady=(50,10))
        self.encabezado.grid_columnconfigure(0, weight=1)
        self.encabezado.grid_columnconfigure(1, weight=1)
        self.boton_cerrar = CTkButton(
            self.encabezado,
            text="✖",
            text_color="#192f4a",
            font=CTkFont(family="Arial", size=16),
            width=30,
            fg_color="#faf9f3",
            command=self.confirmar_borrador,
        )
        self.boton_cerrar.grid(row=0, column=1, pady=10, padx=5, sticky="e")
        
        self.de = CTkLabel(
            self.frame,
            text="  De:",
            font=CTkFont(family="Arial", size=20),
            width=500,
            height=30,
            fg_color="#fcfcfc",
            text_color="gray", anchor="w", corner_radius=15)
        self.de.grid(row=2, column=0, pady=5, padx=50, columnspan=2, sticky="ew")

        self.remitente = CTkOptionMenu(
            self.frame,
            values=["jessica8706m@gmail.com", " otro@example.com"],
            font=CTkFont(family="Arial", size=20),
            width=550,
            fg_color="#fcfcfc",
            text_color="gray")
        self.remitente.grid(row=2, column=1, pady=10, padx=(10, 50), sticky="e")
        self.para = CTkEntry(
            self.frame,
            placeholder_text="Para:",
            font=CTkFont(family="Arial", size=20),
            width=400,
            height=30,
            fg_color="#f5f8fa",
            text_color="gray",
        )
        self.para.grid(row=3, column=0, columnspan=2, pady=10, padx=50, sticky="ew")

        self.asunto = CTkEntry(
            self.frame,
            placeholder_text="Asunto:",
            font=CTkFont(family="Arial", size=20),
            width=400,
            height=30,
            fg_color="#f5f8fa",
            text_color="gray",
        )
        self.asunto.grid(row=4, column=0, columnspan=2, pady=10, padx=50, sticky="ew")

        self.cuerpo = CTkTextbox(
            self.frame,
            width=400,
            height=300,
            fg_color="#f5f7ed",
            text_color="gray",
        )
        self.cuerpo.grid(row=5, column=0, columnspan=2, pady=(10,0), padx=50, sticky="ew")
        
        # Frame para mostrar archivos adjuntos
        self.frame_adjuntos = CTkFrame(self.frame, fg_color="#f5f7ed", height=80)
        self.frame_adjuntos.grid(row=6, column=0, columnspan=2, pady=(0,10),padx=50, sticky="ew")

        self.contenedor_botones=CTkFrame(self.frame, width=400, height=50, fg_color="#FFF7CF")
        self.contenedor_botones.grid(row=7, column=0, columnspan=2, padx=50, sticky="ew")
        self.contenedor_botones.grid_columnconfigure(0, weight=1)
        self.contenedor_botones.grid_columnconfigure(1, weight=1)
        self.contenedor_botones.grid_columnconfigure(2, weight=1)

        self.archivos_adjuntos = []  # Lista para guardar archivos seleccionados
        self.adjuntar_archivo = CTkButton(
            self.contenedor_botones,
            text="🖇️ Adjuntar",
            font=CTkFont(family="Arial", size=16),
            width=100,
            text_color="#192f4a",
            fg_color="#fbfcf7",
            command=self.adjuntar_archivo
        )
        self.adjuntar_archivo.grid(row=0, column=0, pady=10, padx=10)

        self.boton_enviar = CTkButton(
            self.contenedor_botones,
            text="⌯⌲ Enviar",
            text_color="white",
            font=CTkFont(family="Arial", size=16),
            width=100,
            fg_color="#6e664a",
            command=self.enviar
        )
        self.boton_enviar.grid(row=0, column=2, pady=10, padx=50, sticky="e")
    def enviar(self):
        remitente = self.remitente.get()
        destinatario = self.para.get()
        asunto = self.asunto.get()
        cuerpo = self.cuerpo.get("1.0", "end-1c")
        archivos = self.archivos_adjuntos
        # Obtener la contraseña del remitente desde variable de entorno 
        password = os.environ.get("EMAIL_PASS_1", "")
        if not remitente or not destinatario:
            CTkMessagebox(title="Error", message="Remitente y destinatario son obligatorios", icon="cancel")
            return 
        exito = enviar_correo(remitente, password, destinatario, asunto, cuerpo, archivos)
        if exito:
            CTkMessagebox(title="Éxito", message="Correo enviado correctamente", icon="check")
            self.salir()
        else:
            CTkMessagebox(title="Error", message="No se pudo enviar el correo", icon="cancel")
            

    def adjuntar_archivo(self):
        archivo = filedialog.askopenfilename()
        if archivo:
            if archivo not in self.archivos_adjuntos:
                self.archivos_adjuntos.append(archivo)
                self.actualizar_lista_adjuntos()
############################################
    def actualizar_lista_adjuntos(self):
        # Limpia el frame de adjuntos
        for widget in self.frame_adjuntos.winfo_children():
            widget.destroy()
        col = 0
        for idx, archivo in enumerate(self.archivos_adjuntos):
            nombre = archivo.split("/")[-1]
            label = CTkLabel(self.frame_adjuntos, text=nombre, text_color="gray")
            label.grid(row=0, column=col, sticky="w", padx=(0,2))
            col += 1
            btn = CTkButton(self.frame_adjuntos, text="✖", width=25, fg_color="#f7dada", text_color="#a00", command=lambda i=idx: self.eliminar_adjunto(i))
            btn.grid(row=0, column=col, padx=(0,8))
            col += 1
############################################

    def eliminar_adjunto(self, idx):
        if 0 <= idx < len(self.archivos_adjuntos):
            del self.archivos_adjuntos[idx]
            self.actualizar_lista_adjuntos()

    def fecha_correo(self):
        tiempo_actual = datetime.now()
        fecha_formateada = tiempo_actual.strftime("%d/%m/%Y %H:%M:%S")
        return fecha_formateada

    def salir(self) -> None:
        self.encabezado.grid_forget()
        self.de.grid_forget()
        self.remitente.grid_forget()
        self.para.grid_forget()
        self.asunto.grid_forget()
        self.cuerpo.grid_forget()
        self.boton_cerrar.grid_forget()
        self.boton_enviar.grid_forget()
        self.adjuntar_archivo.grid_forget()
        self.contenedor_botones.grid_forget()
        self.frame_adjuntos.grid_forget()

    def confirmar_borrador(self) -> None:
        if (
            self.para.get().strip()
            or self.asunto.get().strip()
            or self.cuerpo.get("1.0", "end-1c").strip()
        ):
            confirmacion = CTkMessagebox(
                title="Confirmación",
                message="¿Deseas guardar el borrador?",
                icon="question",
                option_1="Sí",
                option_2="No",
            ).get()

            if confirmacion == "Sí":
                # aquí podrías crear/guardar el borrador
                self.salir()
            else:
                self.salir()
        else:
            self.salir()