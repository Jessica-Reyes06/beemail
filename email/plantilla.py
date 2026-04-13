from customtkinter import *
from clases import RedactarCorreo
from PIL import Image
from base_datos import *
from recibir_correos import recibir_correos
import os

class VentanaPrincipal:
    def __init__(self):
        # •••••• VENTANA PRINCIPAL ••••••
        set_appearance_mode("light")
        inicializar_bd()
        self.ventana = CTk()
        self.ventana.title(" Correos WhiteTower")
        self.ancho = self.ventana.winfo_screenwidth() # Obtener el ancho de la pantalla
        self.alto = self.ventana.winfo_screenheight() # Obtener el alto de la pantalla
        self.ventana.geometry(f"{self.ancho}x{self.alto}")

        self.imagen_fondo = CTkImage(Image.open("imagenes/fondo0.jpg"), size=(self.ancho, self.alto))
        self.fondo_label = CTkLabel(self.ventana, image=self.imagen_fondo, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.titulos = CTkFont(family="Arial", size=20, weight="bold")
        self.subtitulo = CTkFont(family="Arial", size=16)

        self.logo = CTkImage(Image.open("imagenes/abejita3.png"), size=(200, 110))
        self.label_logo = CTkLabel(self.ventana, image=self.logo, text="")
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20,0), sticky="nw")
        
        
        # •••••• FILTROS SUPERIORES ••••••
        self.barra_nav = CTkFrame(self.ventana)
        self.barra_nav.grid(row=0, column=0, padx=(200,0), pady=(90,50), sticky="n")
        for i in range(5):
            self.barra_nav.grid_columnconfigure(i, weight=1)

        self.boton_actualizar = CTkButton(
            self.barra_nav,
            text="🔄 ",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.actualizar_bandeja
        )
        self.boton_actualizar.grid(row=0, column=0, padx=10, pady=5)

        # •••••• FILTROS ••••••
        self.lista_filtros = CTkOptionMenu(
            self.barra_nav,
            values=["ᯤ", "No leídos", "Importantes","Borradores", "Spam"],
            font=self.subtitulo,
            text_color="white",
            width=80,
            fg_color="#839ab5",
            command=self.filtrar_correos
        )
        self.lista_filtros.grid(row=0, column=1, padx=10, pady=5)

        self.lista_horario = CTkOptionMenu(
            self.barra_nav,
            values=["🌓", "mañana", "tarde", "noche"],
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.filtrar_horario
        )
        self.lista_horario.grid(row=0, column=2, padx=10, pady=5)

        self.frame_redactar = CTkFrame(self.ventana, width=750, height=800, corner_radius=20)
        self.frame_redactar.grid(row=2, column=1, padx=(0,50),pady=(0,50), sticky="n")
        self.frame_redactar.grid_propagate(False)

        self.boton_inbox = CTkButton(
            self.barra_nav,
            text="✍️✉️",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=lambda: RedactarCorreo(self.frame_redactar)
        )
        self.boton_inbox.grid(row=0, column=3, padx=10, pady=5)

        self.boton_contactos = CTkButton(self.barra_nav, text="👥", font=self.subtitulo, width=80, fg_color="#839ab5")
        self.boton_contactos.grid(row=0, column=4, padx=10, pady=5)

        # •••••• BARRA DE BÚSQUEDA ••••••
        self.barrita = CTkEntry(self.ventana, placeholder_text="🔍 Buscar en Correos", width=600,
            height=50, fg_color="#fdfdfd", text_color="white")
        self.barrita.grid(row=0, column=1, padx=10, pady=(90,50), sticky="nw")

        # •••••• FRAME CORREOS ••••••
        self.frame_correos = CTkFrame(self.ventana, width=450, height=800)
        self.frame_correos.grid(row=2, column=0, padx=50, pady=(0, 50), sticky="n")
        self.frame_correos.grid_propagate(False)

        self.fondo_correos = CTkImage(Image.open("imagenes/fondo_correo1.jpeg"), size=(450, 800))
        self.label_fondo_correos = CTkLabel(self.frame_correos, image=self.fondo_correos, text="")
        self.label_fondo_correos.place(x=0, y=0, relwidth=1, relheight=1)

        # Scroll interno para los correos
        self.scroll_correos = CTkScrollableFrame(self.frame_correos, width=400, height=700, fg_color="transparent")
        self.scroll_correos.place(x=10, y=20)

        # •••••• REDACTAR ••••••
        self.fondo_redactar = CTkImage(Image.open("imagenes/fondo33.jpeg"), size=(750, 800))
        self.label_fondo_redactar = CTkLabel(self.frame_redactar, image=self.fondo_redactar, text="")
        self.label_fondo_redactar.place(x=0, y=0, relwidth=1, relheight=1)

        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(1, weight=0)
        self.ventana.grid_rowconfigure(2, weight=1)

        self.usuario = CTkImage(Image.open("imagenes/usuario.png"), size=(100, 100))
        self.label_usuario = CTkLabel(self.ventana, image=self.usuario, text="")
        self.label_usuario.grid(row=0, column=1, padx=40, pady=40, sticky="ne")

        # Descargar correos y mostrar bandeja al iniciar la app
        self.actualizar_bandeja()

    # •••••• FILTROS ••••••
    def filtrar_correos(self, opcion):

        if opcion == "No leídos":
            correos = obtener_correos("leido=0")

        elif opcion == "Importantes":
            correos = obtener_correos("importante=1")

        elif opcion == "Borradores":
            correos = obtener_correos("borrador=1")

        elif opcion == "Spam":
            correos = obtener_correos("spam=1")

        else:
            correos = obtener_correos()

        self.mostrar_correos(correos)

    def filtrar_horario(self, opcion):

        if opcion == "mañana":
            correos = obtener_por_horario("mañana")

        elif opcion == "tarde":
            correos = obtener_por_horario("tarde")

        elif opcion == "noche":
            correos = obtener_por_horario("noche")

        else:
            correos = obtener_correos()

        self.mostrar_correos(correos)

    def actualizar_bandeja(self):
        remitente = os.environ.get("EMAIL_USER_1", "")
        password = os.environ.get("EMAIL_PASS_1", "")
        if remitente and password:
            recibir_correos(remitente, password, n=10)
        self.mostrar_correos(obtener_correos())

    def mostrar_correos(self, correos):

        # Limpia el frame de correos
        for widget in self.scroll_correos.winfo_children():
            widget.destroy()

        # Título
        CTkLabel(self.scroll_correos, text="Bandeja de entrada", font=self.titulos, fg_color="transparent").pack(pady=10)

        if not correos:
            CTkLabel(self.scroll_correos, text="No hay correos", font=self.subtitulo).pack(pady=20)
            return

        # Mostrar cada correo como un botón o etiqueta
        for correo in correos:

            id_, message_id, remitente, destinatario, asunto, cuerpo, fecha, leido, importante, borrador, spam = correo

            texto = f"De: {remitente}\nAsunto: {asunto}\nFecha: {fecha}"

            btn = CTkButton(
                self.scroll_correos,
                text=texto,
                font=self.subtitulo,
                width=400,
                height=60,
                anchor="w",
                fg_color="#313e4c"
            )

            btn.pack(pady=5, padx=10, anchor="w")

    def mostrar(self):
        self.ventana.mainloop()

"""ventanita=VentanaPrincipal()
ventanita.mostrar()"""