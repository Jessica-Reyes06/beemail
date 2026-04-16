from CTkMessagebox import CTkMessagebox
from customtkinter import *
from PIL import Image
from base_datos import *
from funciones import obtener_cuentas_configuradas
import os
import sys
import subprocess
import re


class VentanaContactos:
    def __init__(self, correo_actual="", password="", cuentas_configuradas=None):
        set_appearance_mode("light")
        deactivate_automatic_dpi_awareness()
        set_widget_scaling(1.0)
        set_window_scaling(1.0)
        inicializar_bd()

        self.cuentas_configuradas = cuentas_configuradas or obtener_cuentas_configuradas()
        self.correo_actual = correo_actual or os.environ.get("EMAIL_USER_1", "")
        self.password = password or self.cuentas_configuradas.get(self.correo_actual, "") or os.environ.get("EMAIL_PASS_1", "")

        self.ventana = CTk()
        self.ventana.title("Contactos WhiteTower")
        self.ancho = self.ventana.winfo_screenwidth()
        self.alto = self.ventana.winfo_screenheight()
        self.ventana.geometry(f"{self.ancho}x{self.alto}")

        self.imagen_fondo = CTkImage(Image.open("imagenes/fondo0.jpg"), size=(self.ancho, self.alto))
        self.fondo_label = CTkLabel(self.ventana, image=self.imagen_fondo, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.titulos = CTkFont(family="Arial", size=20, weight="bold")
        self.subtitulo = CTkFont(family="Arial", size=16)

        self.logo = CTkImage(Image.open("imagenes/abejita3.png"), size=(200, 110))
        self.label_logo = CTkLabel(self.ventana, image=self.logo, text="")
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nw")

        self.barra_sup = CTkFrame(self.ventana)
        self.barra_sup.grid(row=0, column=0, padx=(200, 0), pady=(90, 50), sticky="n")

        for i in range(5):
            self.barra_sup.grid_columnconfigure(i, weight=1)

        self.boton_actualizar = CTkButton(
            self.barra_sup,
            text="🔄",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.actualizar_lista
        )
        self.boton_actualizar.grid(row=0, column=0, padx=10, pady=5)

        self.boton_regresar = CTkButton(
            self.barra_sup,
            text="📬",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.regresar_correos
        )
        self.boton_regresar.grid(row=0, column=3, padx=10, pady=5)

        self.boton_nuevo = CTkButton(
            self.barra_sup,
            text="👤+",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.limpiar_formulario
        )
        self.boton_nuevo.grid(row=0, column=4, padx=10, pady=5)

        self.barrita = CTkEntry(
            self.ventana,
            placeholder_text="🔍 Buscar Contacto",
            width=600,
            height=50,
            fg_color="#fdfdfd",
            text_color="white",
        )
        self.barrita.grid(row=0, column=1, padx=10, pady=(90, 50), sticky="nw")

        self.frame_contactos = CTkFrame(self.ventana, width=450, height=800)
        self.frame_contactos.grid(row=2, column=0, padx=50, pady=(0, 50), sticky="n")
        self.frame_contactos.grid_propagate(False)

        self.fondo_contactos = CTkImage(Image.open("imagenes/fondo_correo1.jpeg"), size=(450, 800))
        self.label_fondo_contactos = CTkLabel(self.frame_contactos, image=self.fondo_contactos, text="")
        self.label_fondo_contactos.place(x=0, y=0, relwidth=1, relheight=1)

        self.scroll_contactos = CTkScrollableFrame(
            self.frame_contactos,
            width=400,
            height=700,
            fg_color="transparent",
        )
        self.scroll_contactos.place(x=10, y=20)

        self.frame_registrar = CTkFrame(self.ventana, width=750, height=800, corner_radius=20)
        self.frame_registrar.grid(row=2, column=1, padx=(0, 50), pady=(0, 50), sticky="n")
        self.frame_registrar.grid_propagate(False)

        self.fondo_registrar = CTkImage(Image.open("imagenes/fondo33.jpeg"), size=(750, 800))
        self.label_fondo_registrar = CTkLabel(self.frame_registrar, image=self.fondo_registrar, text="")
        self.label_fondo_registrar.place(x=0, y=0, relwidth=1, relheight=1)

        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(1, weight=0)
        self.ventana.grid_rowconfigure(2, weight=1)

        self.contacto_seleccionado_email = None
        self._construir_formulario()
        self.actualizar_lista()

    def _construir_formulario(self):
        self.encabezado = CTkLabel(
            self.frame_registrar,
            text="Registrar nuevo contacto",
            font=self.titulos,
            fg_color="transparent",
        )
        self.encabezado.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        CTkLabel(
            self.frame_registrar,
            text="Nombre:",
            font=self.subtitulo,
            fg_color="transparent",
        ).grid(row=1, column=0, padx=20, pady=(50, 10), sticky="w")

        self.entrada_nombre = CTkEntry(self.frame_registrar, width=400, fg_color="white", font=self.subtitulo)
        self.entrada_nombre.grid(row=1, column=1, padx=0, pady=20, sticky="w")

        CTkLabel(
            self.frame_registrar,
            text="Correo:",
            font=self.subtitulo,
            fg_color="transparent",
        ).grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.entrada_correo = CTkEntry(self.frame_registrar, width=400, fg_color="white", font=self.subtitulo)
        self.entrada_correo.grid(row=2, column=1, padx=0, pady=20, sticky="w")

        self.frame_botones = CTkFrame(self.frame_registrar, fg_color="transparent")
        self.frame_botones.grid(row=3, column=0, columnspan=2, pady=20, padx=30, sticky="ew")

        self.boton_guardar = CTkButton(
            self.frame_botones,
            text="Guardar",
            font=self.subtitulo,
            width=100,
            fg_color="#A77E0F",
            command=self.guardar_contacto,
        )
        self.boton_guardar.grid(row=0, column=0, padx=20, pady=20)

        self.boton_editar = CTkButton(
            self.frame_botones,
            text="Editar",
            font=self.subtitulo,
            width=100,
            fg_color="#A77E0F",
            command=self.editar_contacto,
        )
        self.boton_editar.grid(row=0, column=1, padx=20, pady=20)

        self.boton_eliminar = CTkButton(
            self.frame_botones,
            text="Eliminar",
            font=self.subtitulo,
            width=100,
            fg_color="#A77E0F",
            command=self.eliminar_contacto_actual,
        )
        self.boton_eliminar.grid(row=0, column=2, padx=20, pady=20)

    def _correo_valido(self, correo):
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(patron, correo) is not None

    def _nombre_desde_email(self, email_contacto):
        local = (email_contacto or "").split("@", 1)[0]
        local = local.replace(".", " ").replace("_", " ").replace("-", " ")
        local = " ".join(local.split())
        return local.title() if local else "Sin nombre"

    def _normalizar_contacto(self, contacto):
        if len(contacto) == 3:
            contacto_id, email_contacto, nombre_contacto = contacto
            nombre_mostrar = (nombre_contacto or "").strip() or self._nombre_desde_email(email_contacto)
            return contacto_id, email_contacto, nombre_contacto, nombre_mostrar
        return None

    def actualizar_lista(self):
        contactos = obtener_contactos()
        self.mostrar_contactos(contactos)

    def mostrar_contactos(self, contactos):
        for widget in self.scroll_contactos.winfo_children():
            widget.destroy()

        CTkLabel(
            self.scroll_contactos,
            text="Lista de contactos",
            font=self.titulos,
            fg_color="transparent",
        ).pack(pady=10)

        if not contactos:
            CTkLabel(self.scroll_contactos, text="No hay contactos", font=self.subtitulo).pack(pady=20)
            return

        for contacto in contactos:
            data = self._normalizar_contacto(contacto)
            if not data:
                continue

            contacto_id, email_contacto, _, nombre_mostrar = data
            texto = f"ID: {contacto_id} | {nombre_mostrar}\n{email_contacto}"

            CTkButton(
                self.scroll_contactos,
                text=texto,
                font=self.subtitulo,
                width=400,
                height=60,
                anchor="w",
                fg_color="#313e4c",
                command=lambda c=contacto: self.ver_contacto(c),
            ).pack(pady=5, padx=10, anchor="w")

    def ver_contacto(self, contacto):
        data = self._normalizar_contacto(contacto)
        if not data:
            return

        _, email_contacto, nombre_contacto, _ = data
        self.contacto_seleccionado_email = email_contacto
        self.entrada_nombre.delete(0, END)
        self.entrada_correo.delete(0, END)
        self.entrada_nombre.insert(0, nombre_contacto or "")
        self.entrada_correo.insert(0, email_contacto or "")
        self.encabezado.configure(text="Editar contacto")

    def limpiar_formulario(self):
        self.contacto_seleccionado_email = None
        self.entrada_nombre.delete(0, END)
        self.entrada_correo.delete(0, END)
        self.encabezado.configure(text="Registrar nuevo contacto")

    def guardar_contacto(self):
        nombre = self.entrada_nombre.get().strip()
        correo = self.entrada_correo.get().strip().lower()

        if not correo:
            CTkMessagebox(title="Error", message="Debes ingresar un correo.", icon="cancel")
            return

        if not self._correo_valido(correo):
            CTkMessagebox(title="Error", message="El correo no tiene un formato valido.", icon="cancel")
            return

        agregado = guardar_contacto(correo, nombre)
        if not agregado:
            CTkMessagebox(title="Aviso", message="Ese contacto ya existe.", icon="warning")
            return

        CTkMessagebox(title="Exito", message="Contacto guardado correctamente.", icon="check")
        self.limpiar_formulario()
        self.actualizar_lista()

    def editar_contacto(self):
        nombre = self.entrada_nombre.get().strip()
        correo = self.entrada_correo.get().strip().lower()

        if not correo:
            CTkMessagebox(title="Error", message="Debes ingresar un correo.", icon="cancel")
            return

        if not self._correo_valido(correo):
            CTkMessagebox(title="Error", message="El correo no tiene un formato valido.", icon="cancel")
            return

        actualizado = actualizar_nombre_contacto(correo, nombre)
        if not actualizado:
            CTkMessagebox(title="Aviso", message="No se pudo actualizar el contacto.", icon="warning")
            return

        CTkMessagebox(title="Exito", message="Contacto actualizado correctamente.", icon="check")
        self.actualizar_lista()

    def eliminar_contacto_actual(self):
        correo = self.entrada_correo.get().strip().lower()
        if not correo:
            CTkMessagebox(title="Error", message="No hay contacto para eliminar.", icon="cancel")
            return

        eliminado = eliminar_contacto(correo)
        if not eliminado:
            CTkMessagebox(title="Aviso", message="No se encontro el contacto para eliminar.", icon="warning")
            return

        CTkMessagebox(title="Exito", message="Contacto eliminado correctamente.", icon="check")
        self.limpiar_formulario()
        self.actualizar_lista()

    def mostrar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    ventanita = VentanaContactos()
    ventanita.mostrar()
