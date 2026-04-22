from PIL import Image, ImageTk
from screens.juego_ia import JuegoIA

class MenuScreen:

    def __init__(self, canvas):
        self.canvas = canvas

        # imágenes
        self.fondo_original = Image.open("assets/imginicio/FONDO.png")
        self.logo_original = Image.open("assets/imginicio/LOGO.png")

        self.btn_ia = Image.open("assets/imginicio/BOTONJVSIA.png")
        self.btn_pvp = Image.open("assets/imginicio/PVP.png")
        self.btn_creditos = Image.open("assets/imginicio/CREDI.png")
        self.btn_extra = Image.open("assets/imginicio/ADI.png")

        self.fondo_tk = None
        self.logo_tk = None

        self.canvas.bind("<Configure>", self.redimensionar)

    # -------------------------
    def redimensionar(self, event):
        self.ancho = event.width
        self.alto = event.height

        self.canvas.delete("all")

        # FONDO
        fondo = self.fondo_original.resize(
            (self.ancho, self.alto),
            Image.Resampling.LANCZOS
        )
        self.fondo_tk = ImageTk.PhotoImage(fondo)
        self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")

        # LOGO
        logo_ancho = int(self.ancho * 0.30)
        ratio = self.logo_original.height / self.logo_original.width
        logo_alto = int(logo_ancho * ratio)

        logo = self.logo_original.resize(
            (logo_ancho, logo_alto),
            Image.Resampling.LANCZOS
        )
        self.logo_tk = ImageTk.PhotoImage(logo)

        self.canvas.create_image(
            self.ancho // 2,
            int(self.alto * 0.18),
            image=self.logo_tk
        )

        # BOTONES
        btn_width = int(self.ancho * 0.28)

        def crear_boton(img_original, x, y, accion):
            ratio = img_original.height / img_original.width
            alto = int(btn_width * ratio)

            img = img_original.resize(
                (btn_width, alto),
                Image.Resampling.LANCZOS
            )
            img_tk = ImageTk.PhotoImage(img)

            boton = self.canvas.create_image(x, y, image=img_tk)
            self.canvas.tag_bind(boton, "<Button-1>", accion)

            return img_tk

        # posiciones
        x_left = int(self.ancho * 0.30)
        x_right = int(self.ancho * 0.70)

        y_top = int(self.alto * 0.50)
        y_bottom = int(self.alto * 0.70)

        # crear botones
        self.img_ia = crear_boton(self.btn_ia, x_left, y_top, self.ir_juego_ia)
        self.img_creditos = crear_boton(self.btn_creditos, x_right, y_top, self.ir_creditos)
        self.img_pvp = crear_boton(self.btn_pvp, x_left, y_bottom, self.ir_pvp)
        self.img_extra = crear_boton(self.btn_extra, x_right, y_bottom, self.ir_extra)

    # -------------------------
    # ACCIONES
    # -------------------------

    def ir_juego_ia(self, event=None):
        self.canvas.delete("all")
        self.canvas.unbind("<Configure>")
        JuegoIA(self.canvas)

    def ir_pvp(self, event=None):
        self.canvas.delete("all")
        self.canvas.unbind("<Configure>")

        from screens.juego_pvp_config import ConfigPVP
        ConfigPVP(self.canvas)

    def ir_creditos(self, event=None):
        print("CRÉDITOS")

    def ir_extra(self, event=None):
        print("ADICIONALES")