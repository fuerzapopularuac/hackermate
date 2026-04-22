from game.piezas import Pieza
from game.reglas import movimiento_valido

class Tablero:

    def __init__(self):
        self.matriz = self.crear_tablero()

    # -------------------------
    # CREAR TABLERO INICIAL
    # -------------------------
    def crear_tablero(self):

        tablero = [[None for _ in range(8)] for _ in range(8)]

        # -------------------------
        # PEONES
        # -------------------------
        for i in range(8):
            tablero[1][i] = Pieza("peon", "oscura")
            tablero[6][i] = Pieza("peon", "blanca")

        # -------------------------
        # TORRES
        # -------------------------
        tablero[0][0] = Pieza("torre", "oscura")
        tablero[0][7] = Pieza("torre", "oscura")
        tablero[7][0] = Pieza("torre", "blanca")
        tablero[7][7] = Pieza("torre", "blanca")

        # -------------------------
        # CABALLOS
        # -------------------------
        tablero[0][1] = Pieza("caballo", "oscura")
        tablero[0][6] = Pieza("caballo", "oscura")
        tablero[7][1] = Pieza("caballo", "blanca")
        tablero[7][6] = Pieza("caballo", "blanca")

        # -------------------------
        # ALFILES
        # -------------------------
        tablero[0][2] = Pieza("alfil", "oscura")
        tablero[0][5] = Pieza("alfil", "oscura")
        tablero[7][2] = Pieza("alfil", "blanca")
        tablero[7][5] = Pieza("alfil", "blanca")

        # -------------------------
        # REINAS
        # -------------------------
        tablero[0][3] = Pieza("reina", "oscura")
        tablero[7][3] = Pieza("reina", "blanca")

        # -------------------------
        # REYES
        # -------------------------
        tablero[0][4] = Pieza("rey", "oscura")
        tablero[7][4] = Pieza("rey", "blanca")

        return tablero

    # -------------------------
    # OBTENER PIEZA
    # -------------------------
    def obtener_pieza(self, fila, col):
        return self.matriz[fila][col]

    # -------------------------
    # MOVER PIEZA CON VALIDACIÓN
    # -------------------------
    def mover_pieza(self, f1, c1, f2, c2):

        pieza = self.matriz[f1][c1]

        # no hay pieza
        if pieza is None:
            return False

        # validar movimiento
        if movimiento_valido(self, pieza, f1, c1, f2, c2):

            self.matriz[f2][c2] = pieza
            self.matriz[f1][c1] = None

            return True

        return False