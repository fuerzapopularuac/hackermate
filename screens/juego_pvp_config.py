import tkinter as tk
from PIL import Image, ImageTk
from screens.juego_pvp import JuegoPVP

class ConfigPVP:

    def __init__(self, canvas):
        self.canvas = canvas
        self.root = canvas.master

        # limpiar canvas
        self.canvas.delete("all")

        # -------------------------
        # FONDO
        # -------------------------
        self.fondo_original = Image.open("assets/imginicio/FONDO.png")

        self.ancho = self.canvas.winfo_width()
        self.alto = self.canvas.winfo_height()

        fondo = self.fondo_original.resize(
            (self.ancho, self.alto),
            Image.Resampling.LANCZOS
        )
        self.fondo_tk = ImageTk.PhotoImage(fondo)

        self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")

        # -------------------------
        # IMAGEN SALUDO (ARRIBA)
        # -------------------------
        self.saludo_original = Image.open("assets/imginicio/saludo.png")

        # tamaño responsivo
        saludo_ancho = int(self.ancho * 0.25)
        ratio = self.saludo_original.height / self.saludo_original.width
        saludo_alto = int(saludo_ancho * ratio)

        saludo = self.saludo_original.resize(
            (saludo_ancho, saludo_alto),
            Image.Resampling.NEAREST  # mantiene pixel art 🔥
        )

        self.saludo_tk = ImageTk.PhotoImage(saludo)

        # posición centrada arriba
        self.canvas.create_image(
            self.ancho // 2,
            int(self.alto * 0.20),
            image=self.saludo_tk
        )

        # -------------------------
        # ESTILO PIXEL
        # -------------------------
        COLOR = "#00FF88"
        FONT = ("Press Start 2P", 12)
        FONT_SMALL = ("Press Start 2P", 10)

        # -------------------------
        # FRAME CENTRAL (BAJAMOS UN POCO)
        # -------------------------
        self.frame = tk.Frame(
            self.root,
            bg="black"
        )

        # 🔥 BAJAMOS EL FORMULARIO
        self.frame.place(relx=0.5, rely=0.60, anchor="center")

        # -------------------------
        # JUGADOR 1
        # -------------------------
        self.label1 = tk.Label(
            self.frame,
            text="JUGADOR 1",
            fg=COLOR,
            bg="black",
            font=FONT
        )
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.entry1 = tk.Entry(
            self.frame,
            font=FONT_SMALL,
            bg="#0A1F1C",
            fg="#00FF88",
            insertbackground="#00FF88",
            width=18
        )
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        # -------------------------
        # JUGADOR 2
        # -------------------------
        self.label2 = tk.Label(
            self.frame,
            text="JUGADOR 2",
            fg=COLOR,
            bg="black",
            font=FONT
        )
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        self.entry2 = tk.Entry(
            self.frame,
            font=FONT_SMALL,
            bg="#0A1F1C",
            fg="#00FF88",
            insertbackground="#00FF88",
            width=18
        )
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        # -------------------------
        # BOTÓN
        # -------------------------
        self.boton = tk.Button(
            self.frame,
            text="INICIAR PARTIDA",
            fg="#00FF88",
            bg="black",
            font=FONT_SMALL,
            activebackground="#0A1F1C",
            command=self.iniciar
        )
        self.boton.grid(row=2, column=0, columnspan=2, pady=20)

    # -------------------------
    def iniciar(self):
        nombre1 = self.entry1.get()
        nombre2 = self.entry2.get()

        if not nombre1:
            nombre1 = "Jugador 1"
        if not nombre2:
            nombre2 = "Jugador 2"

        # limpiar widgets
        self.frame.destroy()

        # ir al juego
        JuegoPVP(self.canvas, nombre1, nombre2)