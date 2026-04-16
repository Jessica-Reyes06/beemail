
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from clases import RedactarCorreo
from PIL import Image
from base_datos import *
from funciones import obtener_cuentas_configuradas
from recibir_correos import recibir_correos
from base import VentanaBase
import os
import sys
import subprocess


class VentanaPrincipal(VentanaBase):
    def __init__(self, master=None, correo_actual="", password="", cuentas_configuradas=None, callback_regresar=None):
        super().__init__(titulo="Correos WhiteTower", correo_actual=correo_actual, password=password, cuentas_configuradas=cuentas_configuradas)
        inicializar_bd()

        # •••••• FILTROS SUPERIORES ••••••
        self.barra_nav = CTkFrame(self.ventana)
        self.barra_nav.grid(row=0, column=0, padx=(200, 0), pady=(90, 50), sticky="n")
        for i in range(5):
            self.barra_nav.grid_columnconfigure(i, weight=1)

        self.boton_actualizar = CTkButton(
            self.barra_nav,
            text="🔄",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.actualizar_bandeja,
        )
        self.boton_actualizar.grid(row=0, column=0, padx=10, pady=5)

        self.lista_filtros = CTkOptionMenu(
            self.barra_nav,
            values=["ᯤ", "No leídos", "Importantes", "Borradores", "Spam"],
            font=self.subtitulo,
            text_color="white",
            width=80,
            fg_color="#839ab5",
            dynamic_resizing=False,
            command=self.filtrar_correos
        )
        self.lista_filtros.grid(row=0, column=1, padx=10, pady=5)

        self.lista_horario = CTkOptionMenu(
            self.barra_nav,
            values=["🌓", "mañana", "tarde", "noche"],
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            dynamic_resizing=False,
            command=self.filtrar_horario
        )
        self.lista_horario.grid(row=0, column=2, padx=10, pady=5)

        self.boton_inbox = CTkButton(
            self.barra_nav,
            text="✉️+",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=lambda: RedactarCorreo(self.frame_redactar, self.correo_actual, self.password, self.cuentas_configuradas)
        )
        self.boton_inbox.grid(row=0, column=3, padx=10, pady=5)

        self.boton_contactos = CTkButton(
            self.barra_nav,
            text="👥",
            font=self.subtitulo,
            width=80,
            fg_color="#839ab5",
            command=self.abrir_contactos
        )
        self.boton_contactos.grid(row=0, column=4, padx=10, pady=5)

        # •••••• BARRA DE BÚSQUEDA ••••••
        self.barrita = CTkEntry(self.ventana, placeholder_text="🔍 Buscar en Correos", width=600, height=50, fg_color="#fdfdfd", text_color="black")
        self.barrita.grid(row=0, column=1, padx=10, pady=(90,50), sticky="nw")
        self.barrita.bind("<Return>", self.buscar_en_barra)

        # •••••• FRAME CORREOS ••••••
        self.frame_correos = CTkFrame(self.ventana, width=450, height=800)
        self.frame_correos.grid(row=2, column=0, padx=50, pady=(0, 50), sticky="n")
        self.frame_correos.grid_propagate(False)

        self.fondo_correos = CTkImage(Image.open("imagenes/fondo_correo1.jpeg"), size=(450, 800))
        self.label_fondo_correos = CTkLabel(self.frame_correos, image=self.fondo_correos, text="")
        self.label_fondo_correos.place(x=0, y=0, relwidth=1, relheight=1)

        self.scroll_correos = CTkScrollableFrame(self.frame_correos, width=400, height=700, fg_color="transparent")
        self.scroll_correos.place(x=10, y=20)

        # •••••• FRAME REDACTAR ••••••
        self.frame_redactar = CTkScrollableFrame(self.ventana, width=750, height=800, corner_radius=20)
        self.frame_redactar.grid(row=2, column=1, padx=(0, 50), pady=(0, 50), sticky="n")

        self.fondo_redactar = CTkImage(Image.open("imagenes/fondo33.jpeg"), size=(750, 800))
        self.label_fondo_redactar = CTkLabel(self.frame_redactar, image=self.fondo_redactar, text="")
        self.label_fondo_redactar.place(x=0, y=0, relwidth=1, relheight=1)

        # •••••• ICONO DE USUARIO ••••••
        self.usuario = CTkImage(Image.open("imagenes/usuario.png"), size=(100, 100))
        self.label_usuario = CTkLabel(
            self.ventana,
            image=self.usuario,
            text="",
            fg_color="transparent",
            cursor="hand2"
        )
        self.label_usuario.grid(row=0, column=1, padx=40, pady=40, sticky="ne")
        self.label_usuario.bind("<Button-1>", self.seleccionar_icon)

        self.actualizar_bandeja()

    # •••••• NAVEGACIÓN ••••••
    def abrir_contactos(self):
        self.ventana.destroy()
        ruta_contactos = os.path.join(os.path.dirname(__file__), "contactos.py")
        subprocess.Popen([sys.executable, ruta_contactos,
                         self.correo_actual, self.password])

    def cambiar_cuenta(self):
        self.ventana.destroy()
        ruta_login = os.path.join(os.path.dirname(__file__), "login.py")
        subprocess.Popen([sys.executable, ruta_login])

    def seleccionar_icon(self, event=None):
        self.ver_perfil()

    # •••••• PERFIL ••••••
    def _obtener_nombre_usuario(self):
        if not self.correo_actual:
            return "Usuario"

        correo = self.correo_actual.strip()
        if "<" in correo and ">" in correo:
            nombre = correo.split("<", 1)[0].strip().strip('"')
            if nombre:
                return nombre
            correo = correo.split("<", 1)[1].split(">", 1)[0].strip()

        local = correo.split("@", 1)[0]
        local = local.replace(".", " ").replace("_", " ").replace("-", " ")
        local = " ".join(local.split())
        return local.title() if local else "Usuario"

    def ver_perfil(self):
        ventana_perfil = CTkToplevel(self.ventana)
        ventana_perfil.overrideredirect(True)
        ventana_perfil.geometry("250x200+1100+200")
        ventana_perfil.configure(fg_color="#f7f8f0")
        ventana_perfil.resizable(False, False)
        ventana_perfil.grid_columnconfigure(0, weight=1)

        CTkButton(
            ventana_perfil,
            text="✕",
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="#f0ff7d",
            text_color="gray",
            command=ventana_perfil.destroy,
        ).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ne")

        CTkLabel(
            ventana_perfil,
            text=self._obtener_nombre_usuario(),
            font=CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="transparent",
        ).grid(row=1, column=0, pady=10)

        CTkLabel(
            ventana_perfil,
            text=f"Correo: {self.correo_actual or 'No configurado'}",
            font=CTkFont(family="Arial", size=12),
            fg_color="transparent",
        ).grid(row=2, column=0, pady=10, padx=10)

        CTkButton(
            ventana_perfil,
            text="Cambiar cuenta",
            font=CTkFont(family="Arial", size=14),
            width=100,
            fg_color="#A77E0F",
            command=self.cambiar_cuenta,
        ).grid(row=3, column=0, pady=30)

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

        self.mostrar_correos(self._filtrar_correos_de_cuenta(correos))

    def filtrar_horario(self, opcion):
        if opcion == "mañana":
            correos = obtener_por_horario("mañana")
        elif opcion == "tarde":
            correos = obtener_por_horario("tarde")
        elif opcion == "noche":
            correos = obtener_por_horario("noche")
        else:
            correos = obtener_correos()

        self.mostrar_correos(self._filtrar_correos_de_cuenta(correos))

    def _filtrar_correos_de_cuenta(self, correos):
        if not self.correo_actual:
            return correos

        cuenta = self.correo_actual.lower()
        filtrados = []
        for correo in correos:
            remitente = (correo[2] or "").lower()
            destinatario = (correo[3] or "").lower()
            if cuenta in remitente or cuenta in destinatario:
                filtrados.append(correo)
        return filtrados

    def buscar_en_barra(self, event=None):
        texto = self.barrita.get().strip()

        if not texto:
            correos = obtener_correos()
        else:
            correos = buscar_correos(texto)

        self.mostrar_correos(self._filtrar_correos_de_cuenta(correos))

    # •••••• BANDEJA ••••••
    def actualizar_bandeja(self):
        if self.correo_actual and self.password:
            recibir_correos(self.correo_actual, self.password, n=10)
        self.mostrar_correos(self._filtrar_correos_de_cuenta(obtener_correos()))

    def mostrar_correos(self, correos):
        for widget in self.scroll_correos.winfo_children():
            widget.destroy()

        CTkLabel(self.scroll_correos, text="Bandeja de entrada", font=self.titulos, fg_color="transparent").pack(pady=10)

        if not correos:
            CTkLabel(self.scroll_correos, text="No hay correos", font=self.subtitulo).pack(pady=20)
            return

        for correo in correos:
            _, _, remitente, destinatario, asunto, cuerpo, fecha, _, _, _, _ = correo
            texto = f"De: {remitente}\nAsunto: {asunto}\nFecha: {fecha}"
            CTkButton(
                self.scroll_correos,
                text=texto,
                font=self.subtitulo,
                width=400,
                height=60,
                anchor="w",
                fg_color="#313e4c",
                command=lambda c=correo: self.ver_correo(c),
            ).pack(pady=5, padx=10, anchor="w")

    def ver_correo(self, correo):
        for widget in self.frame_redactar.winfo_children():
            widget.destroy()

        CTkLabel(self.frame_redactar, image=self.fondo_redactar, text="").place(x=0, y=0, relwidth=1, relheight=1)

        _, _, remitente, destinatario, asunto, cuerpo, fecha, _, _, _, _ = correo

        CTkLabel(self.frame_redactar, text="Detalle del correo", font=self.titulos, fg_color="transparent").pack(
            pady=(20, 10), padx=20, anchor="w"
        )
        CTkLabel(
            self.frame_redactar,
            text=f"De: {remitente}\nPara: {destinatario}\nAsunto: {asunto}\nFecha: {fecha}",
            font=self.subtitulo,
            justify="left",
            anchor="w",
            wraplength=680,
            fg_color="transparent",
        ).pack(pady=5, padx=20, anchor="w")

        cuerpo_texto = CTkTextbox(
            self.frame_redactar,
            width=680,
            height=560,
            fg_color="transparent",
            text_color="black",
            font=self.subtitulo,
        )
        cuerpo_texto.pack(pady=10, padx=20, anchor="w")
        cuerpo_texto.insert("1.0", cuerpo)
        cuerpo_texto.configure(state="disabled")

    def mostrar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    correo = sys.argv[1] if len(sys.argv) > 1 else ""
    password = sys.argv[2] if len(sys.argv) > 2 else ""
    app = VentanaPrincipal(correo_actual=correo, password=password)
    app.mostrar()