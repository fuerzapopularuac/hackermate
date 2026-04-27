from game.piezas import Pieza
from game.reglas import movimiento_valido, esta_en_jaque

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
    # MOVER PIEZA CON VALIDACIÓN Y SIMULACIÓN
    # -------------------------
    def mover_pieza(self, f1, c1, f2, c2):

        pieza = self.matriz[f1][c1]

        # no hay pieza
        if pieza is None:
            return False

        # validar movimiento geométrico
        if movimiento_valido(self, pieza, f1, c1, f2, c2):

            # 🔥 SPRINT 3: SIMULACIÓN DE AUTO-JAQUE 🔥
            # 1. Guardamos la pieza de destino (por si nos comemos una)
            pieza_destino_temp = self.matriz[f2][c2]
            
            # 2. Movemos temporalmente en la matriz
            self.matriz[f2][c2] = pieza
            self.matriz[f1][c1] = None
            
            # 3. Verificamos si este movimiento nos deja en jaque
            en_jaque = esta_en_jaque(self, pieza.color)
            
            # 4. Deshacemos la simulación
            self.matriz[f1][c1] = pieza
            self.matriz[f2][c2] = pieza_destino_temp
            
            # 5. Si el movimiento nos dejó en jaque, es ilegal y lo bloqueamos
            if en_jaque:
                return False

            # 🔥 SI PASÓ LA PRUEBA, APLICAMOS EL MOVIMIENTO REAL 🔥
            self.matriz[f2][c2] = pieza
            self.matriz[f1][c1] = None

            # SPRINT 3: PROMOCIÓN DEL PEÓN
            if pieza.tipo == "peon":
                if (pieza.color == "blanca" and f2 == 0) or (pieza.color == "oscura" and f2 == 7):
                    pieza.tipo = "reina"  

            return True

        return False