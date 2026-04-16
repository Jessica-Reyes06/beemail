import sys

from utils import resource_path

from customtkinter import *
from PIL import Image
from funciones import obtener_cuentas_configuradas
import os

class VentanaBase:
    def __init__(self, titulo, correo_actual="", password="", cuentas_configuradas=None):
        set_appearance_mode("light")
        deactivate_automatic_dpi_awareness()
        set_widget_scaling(1.0)
        set_window_scaling(1.0)
        # Cuentas y credenciales
        self.cuentas_configuradas = cuentas_configuradas or obtener_cuentas_configuradas()
        self.correo_actual = correo_actual or os.environ.get("EMAIL_USER_1", "")
        self.password = password or self.cuentas_configuradas.get(self.correo_actual, "") or os.environ.get("EMAIL_PASS_1", "")

        # Ventana principal
        self.ventana = CTk()
        self.ventana.title(titulo)
        self.ancho = self.ventana.winfo_screenwidth()
        self.alto = self.ventana.winfo_screenheight()
        self.ventana.geometry(f"{self.ancho}x{self.alto}")

        # Fondo general
        self.imagen_fondo = CTkImage(Image.open(resource_path("imagenes/fondo0.jpg")), size=(self.ancho, self.alto))
        self.fondo_label = CTkLabel(self.ventana, image=self.imagen_fondo, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Fuentes
        self.titulos = CTkFont(family="Arial", size=20, weight="bold")
        self.subtitulo = CTkFont(family="Arial", size=16)

        # Logo
        self.logo = CTkImage(Image.open(resource_path("imagenes/abejita3.png")), size=(200, 110))
        self.label_logo = CTkLabel(self.ventana, image=self.logo, text="")
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nw")

        # Frame contactos (opcional, puede ser usado o no por la subclase)
        self.frame_contactos = CTkFrame(self.ventana, width=450, height=800)
        self.frame_contactos.grid(row=2, column=0, padx=50, pady=(0, 50), sticky="n")
        self.frame_contactos.grid_propagate(False)
        self.fondo_contactos = CTkImage(Image.open(resource_path("imagenes/fondo_correo1.jpeg")), size=(450, 800))
        self.label_fondo_contactos = CTkLabel(self.frame_contactos, image=self.fondo_contactos, text="")
        self.label_fondo_contactos.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame registrar/redactar (opcional, puede ser usado o no por la subclase)
        self.frame_registrar = CTkFrame(self.ventana, width=750, height=800, corner_radius=20)
        self.frame_registrar.grid(row=2, column=1, padx=(0, 50), pady=(0, 50), sticky="n")
        self.frame_registrar.grid_propagate(False)
        self.fondo_registrar = CTkImage(Image.open(resource_path("imagenes/fondo33.jpeg")), size=(750, 800))
        self.label_fondo_registrar = CTkLabel(self.frame_registrar, image=self.fondo_registrar, text="")
        self.label_fondo_registrar.place(x=0, y=0, relwidth=1, relheight=1)

        # Configuración de grid general
        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(1, weight=0)
        self.ventana.grid_rowconfigure(2, weight=1)

    def mostrar(self):
        self.ventana.mainloop()
