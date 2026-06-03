from PIL import Image, ImageTk
from game.tablero import Tablero
from game.reglas import esta_en_jaque
from agentes.supervisor_agente import SupervisorAgente

class JuegoIA:

    def __init__(self, canvas):
        self.canvas = canvas

        self.jugador1 = "YO"
        self.jugador2 = "HACKERMATE"
        self.turno = self.jugador1

        self.fondo_original = Image.open("assets/imginicio/FONDO.png")
        self.logo_original = Image.open("assets/imginicio/LOGO.png")

        self.tablero = Tablero()
        self.seleccion = None
        self.juego_terminado = False
        self.ia_pensando = False
        self.ultima_estrategia = None
        self.mensaje_final = None
        self.estado_agentes = ""

        self.supervisor = SupervisorAgente(profundidad=3)

        self.cargar_imagenes()

        self.canvas.bind("<Configure>", self.dibujar)
        self.canvas.bind("<Button-1>", self.click)

        self.dibujar_inicial()

    def actualizar_estado_agente(self, mensaje):
        self.estado_agentes = mensaje
        self.canvas.after_idle(self.dibujar_inicial)

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

    def dibujar_inicial(self):
        class Fake:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
        self.dibujar(Fake())

    def click(self, event):
        if self.turno != self.jugador1 or self.juego_terminado or self.ia_pensando:
            return

        TAM = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 12
        ox = int(self.canvas.winfo_width() * 0.10)
        oy = int(self.canvas.winfo_height() * 0.15)

        col = (event.x - ox) // TAM
        fila = (event.y - oy) // TAM

        if 0 <= fila < 8 and 0 <= col < 8:
            pieza = self.tablero.obtener_pieza(fila, col)

            if self.seleccion is None:
                if pieza and pieza.color == "blanca":
                    self.seleccion = (fila, col)
            else:
                f1, c1 = self.seleccion
                if self.tablero.mover_pieza(f1, c1, fila, col):
                    self.turno = self.jugador2
                    color_ia = "oscura"
                    if not self.tablero.tiene_movimientos_validos(color_ia):
                        if esta_en_jaque(self.tablero, color_ia):
                            self.mensaje_final = "JAQUE MATE\nGanaste"
                        else:
                            self.mensaje_final = "TABLAS\nRey Ahogado"
                        self.juego_terminado = True
                    else:
                        self.programar_turno_ia()
                self.seleccion = None

            self.dibujar_inicial()

    def programar_turno_ia(self):
        self.ia_pensando = True
        self.dibujar_inicial()
        self.canvas.after(100, self.ejecutar_turno_ia)

    def ejecutar_turno_ia(self):
        try:
            color_ia = "oscura"
            resultado = self.supervisor.jugar_turno(self.tablero, color_ia, callback_estado=self.actualizar_estado_agente)

            if resultado and resultado.get("movimiento"):
                m = resultado["movimiento"]
                self.tablero.mover_pieza(
                    m["desde"][0], m["desde"][1],
                    m["hasta"][0], m["hasta"][1]
                )
                self.ultima_estrategia = resultado.get("estrategia")
                self.turno = self.jugador1

                color_humano = "blanca"
                if not self.tablero.tiene_movimientos_validos(color_humano):
                    if esta_en_jaque(self.tablero, color_humano):
                        self.mensaje_final = "JAQUE MATE\nGanó Hackermate"
                    else:
                        self.mensaje_final = "TABLAS\nRey Ahogado"
                    self.juego_terminado = True
            else:
                if esta_en_jaque(self.tablero, color_ia):
                    self.mensaje_final = "JAQUE MATE\nGanaste"
                else:
                    self.mensaje_final = "TABLAS\nRey Ahogado"
                self.juego_terminado = True
        except Exception as e:
            print(f"Error en turno IA: {e}")
            self.juego_terminado = True
        finally:
            self.ia_pensando = False
            self.dibujar_inicial()

    def dibujar(self, event):
        ancho = event.width
        alto = event.height

        self.canvas.delete("all")

        fondo = self.fondo_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self.fondo_tk = ImageTk.PhotoImage(fondo)
        self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")

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

        self.canvas.create_text(
            ox + 4*TAM, oy - 20,
            text=self.jugador2, fill="#00FF88",
            font=("Consolas", 14, "bold")
        )
        self.canvas.create_text(
            ox + 4*TAM, oy + 8*TAM + 20,
            text=self.jugador1, fill="#00FF88",
            font=("Consolas", 14, "bold")
        )

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

        if self.seleccion and not self.juego_terminado:
            f, c = self.seleccion
            self.canvas.create_rectangle(
                ox + c*TAM, oy + f*TAM,
                ox + (c+1)*TAM, oy + (f+1)*TAM,
                outline="yellow", width=3
            )

        px1 = int(ancho * 0.65)
        px2 = int(ancho * 0.95)

        logo_w = int((px2 - px1) * 0.5)
        ratio = self.logo_original.height / self.logo_original.width
        logo_h = int(logo_w * ratio)
        logo = self.logo_original.resize((logo_w, logo_h), Image.Resampling.NEAREST)
        self.logo_tk = ImageTk.PhotoImage(logo)
        self.canvas.create_image(
            (px1 + px2) // 2, int(alto * 0.18), image=self.logo_tk
        )

        ty1 = int(alto * 0.30)
        ty2 = int(alto * 0.45)

        color_actual = "oscura" if self.turno == self.jugador2 else "blanca"
        en_jaque = esta_en_jaque(self.tablero, color_actual)
        hay_movimientos = self.tablero.tiene_movimientos_validos(color_actual)

        texto_turno = f"Turno de:\n{self.turno}"
        color_texto = "#00FF88"
        color_borde = "#00FF88"

        if self.mensaje_final:
            texto_turno = self.mensaje_final
            color_texto = "#FFD700"
            color_borde = "#FFD700"
        elif en_jaque:
            texto_turno += "\nESTÁS EN JAQUE"
            color_texto = "#FF3333"
            color_borde = "#FF3333"

        self.canvas.create_rectangle(px1, ty1, px2, ty2, fill="black", outline=color_borde, width=2)
        self.canvas.create_text(
            px1 + 20, ty1 + 20,
            text=texto_turno, fill=color_texto,
            anchor="nw", font=("Consolas", 14, "bold")
        )

        iy1 = int(alto * 0.50)
        iy2 = int(alto * 0.88)

        self.canvas.create_rectangle(px1, iy1, px2, iy2, fill="black", outline="#00FF88")

        if self.ia_pensando and self.estado_agentes:
            self.canvas.create_text(
                px1 + 15, iy1 + 15,
                text="ESTADO DE LOS AGENTES",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 13, "bold")
            )
            self.canvas.create_text(
                px1 + 15, iy1 + 40,
                text=self.estado_agentes,
                fill="#00FF88", anchor="nw",
                font=("Consolas", 11)
            )
        elif self.ia_pensando:
            self.canvas.create_text(
                px1 + 20, iy1 + 20,
                text="Pensando...",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 16, "bold")
            )
        elif self.ultima_estrategia:
            plan = self.ultima_estrategia.get("plan", "?")
            prioridad = self.ultima_estrategia.get("prioridad", "?")
            seguridad = self.ultima_estrategia.get("seguridad_rey", "?")
            material = self.ultima_estrategia.get("ventaja_material", "?")
            self.canvas.create_text(
                px1 + 15, iy1 + 15,
                text=f"PLAN: {plan}",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 13, "bold")
            )
            self.canvas.create_text(
                px1 + 15, iy1 + 40,
                text=f"Prioridad: {prioridad}",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 11)
            )
            self.canvas.create_text(
                px1 + 15, iy1 + 60,
                text=f"Seguridad: {seguridad}%",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 11)
            )
            self.canvas.create_text(
                px1 + 15, iy1 + 80,
                text=f"Material: {material:+d}",
                fill="#00FF88", anchor="nw",
                font=("Consolas", 11)
            )
