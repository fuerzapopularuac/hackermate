from PIL import Image, ImageTk
from game.tablero import Tablero

class JuegoIA:

    def __init__(self, canvas):
        self.canvas = canvas

        self.jugador1 = "YO"
        self.jugador2 = "HACKERMATE"

        self.turno = self.jugador1  # 🔥 siempre empieza el jugador

        self.fondo_original = Image.open("assets/imginicio/FONDO.png")
        self.logo_original = Image.open("assets/imginicio/LOGO.png")

        self.tablero = Tablero()
        self.seleccion = None

        self.cargar_imagenes()

        self.canvas.bind("<Configure>", self.dibujar)
        self.canvas.bind("<Button-1>", self.click)

        self.dibujar_inicial()

    # -------------------------
    def cargar_imagenes(self):

        self.imagenes = {}

        rutas = {
            ("peon","blanca"): "assets/piezas/blancas/peon.png",
            ("torre","blanca"): "assets/piezas/blancas/torre.png",
            ("caballo","blanca"): "assets/piezas/blancas/caballo.png",
            ("alfil","blanca"): "assets/piezas/blancas/alfil.png",
            ("reina","blanca"): "assets/piezas/blancas/reina.png",
            ("rey","blanca"): "assets/piezas/blancas/rey.png",

            ("peon","oscura"): "assets/piezas/oscuras/peon.png",
            ("torre","oscura"): "assets/piezas/oscuras/torre.png",
            ("caballo","oscura"): "assets/piezas/oscuras/caballo.png",
            ("alfil","oscura"): "assets/piezas/oscuras/alfil.png",
            ("reina","oscura"): "assets/piezas/oscuras/reina.png",
            ("rey","oscura"): "assets/piezas/oscuras/rey.png",
        }

        for clave, ruta in rutas.items():
            self.imagenes[clave] = Image.open(ruta)

    # -------------------------
    def dibujar_inicial(self):
        class Fake:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
        self.dibujar(Fake())

    # -------------------------
    def click(self, event):

        # 🔥 SOLO EL JUGADOR HUMANO PUEDE MOVER
        if self.turno != self.jugador1:
            return

        TAM = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 12
        ox = int(self.canvas.winfo_width() * 0.10)
        oy = int(self.canvas.winfo_height() * 0.15)

        col = (event.x - ox) // TAM
        fila = (event.y - oy) // TAM

        if 0 <= fila < 8 and 0 <= col < 8:

            pieza = self.tablero.obtener_pieza(fila, col)

            if self.seleccion is None:

                if pieza and pieza.color == "blanca":  # 🔥 solo blancas
                    self.seleccion = (fila, col)

            else:
                f1, c1 = self.seleccion

                if self.tablero.mover_pieza(f1, c1, fila, col):
                    self.turno = self.jugador2  # 🔥 turno IA

                self.seleccion = None

            self.dibujar_inicial()

    # -------------------------
    def dibujar(self, event):

        ancho = event.width
        alto = event.height

        self.canvas.delete("all")

        # -------------------------
        # FONDO
        # -------------------------
        fondo = self.fondo_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self.fondo_tk = ImageTk.PhotoImage(fondo)
        self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")

        # -------------------------
        # TABLERO
        # -------------------------
        TAM = min(ancho, alto) // 12
        ox = int(ancho * 0.10)
        oy = int(alto * 0.15)

        for f in range(8):
            for c in range(8):
                color = "#1BFFB2" if (f+c)%2==0 else "#0A1F1C"
                self.canvas.create_rectangle(
                    ox + c*TAM, oy + f*TAM,
                    ox + (c+1)*TAM, oy + (f+1)*TAM,
                    fill=color, outline="#00FF88"
                )

        # -------------------------
        # NOMBRES
        # -------------------------
        self.canvas.create_text(
            ox + 4*TAM,
            oy - 20,
            text=self.jugador2,
            fill="#00FF88",
            font=("Consolas", 14, "bold")
        )

        self.canvas.create_text(
            ox + 4*TAM,
            oy + 8*TAM + 20,
            text=self.jugador1,
            fill="#00FF88",
            font=("Consolas", 14, "bold")
        )

        # -------------------------
        # PIEZAS
        # -------------------------
        self.imagenes_tk = {}
        tamaño = int(TAM * 0.85)

        for clave, img in self.imagenes.items():
            img_resized = img.resize((tamaño, tamaño), Image.Resampling.NEAREST)
            self.imagenes_tk[clave] = ImageTk.PhotoImage(img_resized)

        for f in range(8):
            for c in range(8):
                pieza = self.tablero.obtener_pieza(f, c)
                if pieza:
                    x = ox + c*TAM + TAM//2
                    y = oy + f*TAM + TAM//2
                    clave = (pieza.tipo, pieza.color)
                    self.canvas.create_image(x, y, image=self.imagenes_tk[clave])

        # -------------------------
        # SELECCIÓN
        # -------------------------
        if self.seleccion:
            f, c = self.seleccion
            self.canvas.create_rectangle(
                ox + c*TAM, oy + f*TAM,
                ox + (c+1)*TAM, oy + (f+1)*TAM,
                outline="yellow",
                width=3
            )

        # -------------------------
        # PANEL DERECHO
        # -------------------------
        px1 = int(ancho * 0.65)
        px2 = int(ancho * 0.95)

        # LOGO
        logo_w = int((px2 - px1) * 0.5)
        ratio = self.logo_original.height / self.logo_original.width
        logo_h = int(logo_w * ratio)

        logo = self.logo_original.resize((logo_w, logo_h), Image.Resampling.NEAREST)
        self.logo_tk = ImageTk.PhotoImage(logo)

        self.canvas.create_image(
            (px1 + px2) // 2,
            int(alto * 0.18),
            image=self.logo_tk
        )

        # PANEL TURNO
        ty1 = int(alto * 0.30)
        ty2 = int(alto * 0.45)

        self.canvas.create_rectangle(px1, ty1, px2, ty2, fill="black", outline="#00FF88")

        self.canvas.create_text(
            px1 + 20, ty1 + 20,
            text=f"Turno de:\n{self.turno}",
            fill="#00FF88",
            anchor="nw",
            font=("Consolas", 14, "bold")
        )

        # -------------------------
        # PANEL VACÍO (IA FUTURA)
        # -------------------------
        iy1 = int(alto * 0.50)
        iy2 = int(alto * 0.85)

        self.canvas.create_rectangle(px1, iy1, px2, iy2, fill="black", outline="#00FF88")