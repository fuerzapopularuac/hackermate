from PIL import Image, ImageTk
from game.tablero import Tablero
from game.reglas import esta_en_jaque

class JuegoPVP:

    def __init__(self, canvas, jugador1, jugador2):
        self.canvas = canvas
        self.jugador1 = jugador1
        self.jugador2 = jugador2

        self.turno = jugador1

        self.fondo_original = Image.open("assets/imginicio/FONDO.png")
        self.logo_original = Image.open("assets/imginicio/LOGO.png")

        self.tablero = Tablero()
        self.seleccion = None

        # -------------------------
        # CARAS (ROTACIÓN)
        # -------------------------
        self.caras_list = [
            Image.open("assets/caras/feliz.png"),
            Image.open("assets/caras/eno.png"),
            Image.open("assets/caras/sor.png"),
            Image.open("assets/caras/triste.png"),
            Image.open("assets/caras/euf.png"),
        ]

        self.indice_cara = 0

        self.cargar_imagenes()

        self.canvas.bind("<Configure>", self.dibujar)
        self.canvas.bind("<Button-1>", self.click)

        self.dibujar_inicial()
        self.loop_rotacion()

    # -------------------------
    def loop_rotacion(self):
        self.indice_cara = (self.indice_cara + 1) % len(self.caras_list)
        self.dibujar_inicial()
        self.canvas.after(3000, self.loop_rotacion)

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
    # -------------------------
    def click(self, event):

        TAM = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 12
        ox = int(self.canvas.winfo_width() * 0.10)
        oy = int(self.canvas.winfo_height() * 0.15)

        col = (event.x - ox) // TAM
        fila = (event.y - oy) // TAM

        # 🔥 BLOQUEAR CLICS SI EL JUEGO TERMINÓ
        color_actual = "blanca" if self.turno == self.jugador1 else "oscura"
        if not self.tablero.tiene_movimientos_validos(color_actual):
            return

        if 0 <= fila < 8 and 0 <= col < 8:

            pieza = self.tablero.obtener_pieza(fila, col)

            if self.seleccion is None:

                if pieza:
                    if (pieza.color == "blanca" and self.turno == self.jugador1) or \
                       (pieza.color == "oscura" and self.turno == self.jugador2):

                        self.seleccion = (fila, col)

            else:
                f1, c1 = self.seleccion

                if self.tablero.mover_pieza(f1, c1, fila, col):
                    self.turno = self.jugador2 if self.turno == self.jugador1 else self.jugador1

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

        # 🔥 LOGO BIEN POSICIONADO
        logo_w = int((px2 - px1) * 0.5)
        ratio = self.logo_original.height / self.logo_original.width
        logo_h = int(logo_w * ratio)

        logo = self.logo_original.resize((logo_w, logo_h), Image.Resampling.NEAREST)
        self.logo_tk = ImageTk.PhotoImage(logo)

        logo_y = int(alto * 0.18)

        self.canvas.create_image(
            (px1 + px2) // 2,
            logo_y,
            image=self.logo_tk
        )

        # -------------------------
        # PANEL TURNO (BAJADO)
        # -------------------------
        ty1 = int(alto * 0.30)
        ty2 = int(alto * 0.45)

        # 🔥 SPRINT 3: LÓGICA VISUAL DE JAQUE MATE 🔥
        color_actual = "blanca" if self.turno == self.jugador1 else "oscura"
        en_jaque = esta_en_jaque(self.tablero, color_actual)
        hay_movimientos = self.tablero.tiene_movimientos_validos(color_actual)

        texto_turno = f"Turno de:\n{self.turno}"
        color_texto = "#00FF88"
        color_borde = "#00FF88"

        if not hay_movimientos:
            if en_jaque:
                texto_turno = f"¡JAQUE MATE!\nGanó el rival"
                color_texto = "#FFD700"  # Dorado de victoria
                color_borde = "#FFD700"
            else:
                texto_turno = f"¡TABLAS!\nRey Ahogado"
                color_texto = "#AAAAAA"  # Gris de empate
                color_borde = "#AAAAAA"
        elif en_jaque:
            texto_turno += "\n¡ESTÁS EN JAQUE!"
            color_texto = "#FF3333"  # Rojo de peligro
            color_borde = "#FF3333"

        self.canvas.create_rectangle(px1, ty1, px2, ty2, fill="black", outline=color_borde, width=2)

        self.canvas.create_text(
            px1 + 20, ty1 + 20,
            text=texto_turno,
            fill=color_texto,
            anchor="nw",
            font=("Consolas", 14, "bold")
        )
        # -------------------------
        # PANEL CARA
        # -------------------------
        iy1 = int(alto * 0.50)
        iy2 = int(alto * 0.85)

        self.canvas.create_rectangle(px1, iy1, px2, iy2, fill="black", outline="#00FF88")

        # CARA ROTANDO
        img = self.caras_list[self.indice_cara]

        img_w = int((px2 - px1) * 0.8)
        ratio = img.height / img.width
        img_h = int(img_w * ratio)

        img_resized = img.resize((img_w, img_h), Image.Resampling.NEAREST)
        self.cara_tk = ImageTk.PhotoImage(img_resized)

        self.canvas.create_image(
            (px1+px2)//2,
            (iy1+iy2)//2,
            image=self.cara_tk
        )