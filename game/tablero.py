from game.piezas import Pieza
from game.reglas import movimiento_valido, esta_en_jaque
import copy

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
    # ES MOVIMIENTO VÁLIDO (geométrico)
    # -------------------------
    def es_movimiento_valido(self, f1, c1, f2, c2):
        pieza = self.obtener_pieza(f1, c1)
        if not pieza:
            return False
        return movimiento_valido(self, pieza, f1, c1, f2, c2)

    # -------------------------
    # CASILLA ATACADA POR UN COLOR
    # -------------------------
    def casilla_atacada_por(self, fila, col, color_atacante):
        for f in range(8):
            for c in range(8):
                p = self.obtener_pieza(f, c)
                if p and p.color == color_atacante:
                    if self.es_movimiento_valido(f, c, fila, col):
                        return True
        return False

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

            # 🔥 SPRINT 3: APLICAR EL ENROQUE (MOVER LA TORRE) 🔥
            if pieza.tipo == "rey" and abs(c2 - c1) == 2:
                if c2 > c1: # Enroque Corto (hacia la derecha)
                    torre = self.matriz[f2][7]
                    self.matriz[f2][5] = torre  # La torre pasa al lado del rey
                    self.matriz[f2][7] = None
                    torre.ha_movido = True
                else: # Enroque Largo (hacia la izquierda)
                    torre = self.matriz[f2][0]
                    self.matriz[f2][3] = torre  # La torre pasa al lado del rey
                    self.matriz[f2][0] = None
                    torre.ha_movido = True

            # SPRINT 3: PROMOCIÓN DEL PEÓN
            if pieza.tipo == "peon":
                if (pieza.color == "blanca" and f2 == 0) or (pieza.color == "oscura" and f2 == 7):
                    pieza.tipo = "reina"  # Promoción automática a reina

            # Registrar que la pieza ya se movió (para bloquear futuros enroques)
            pieza.ha_movido = True

            return True

        return False
    
    # -------------------------
    # 🔥 SPRINT 3: DETECCIÓN DE JAQUE MATE / AHOGADO 🔥
    # -------------------------
    def tiene_movimientos_validos(self, color):
        for f1 in range(8):
            for c1 in range(8):
                pieza = self.matriz[f1][c1]
                if pieza and pieza.color == color:
                    # Probar mover esta pieza a todas las casillas posibles
                    for f2 in range(8):
                        for c2 in range(8):
                            if movimiento_valido(self, pieza, f1, c1, f2, c2):
                                # Simulamos el movimiento
                                pieza_destino_temp = self.matriz[f2][c2]
                                self.matriz[f2][c2] = pieza
                                self.matriz[f1][c1] = None
                                
                                en_jaque = esta_en_jaque(self, color)
                                
                                # Deshacemos la simulación
                                self.matriz[f1][c1] = pieza
                                self.matriz[f2][c2] = pieza_destino_temp
                                
                                # Si encontramos al menos UN movimiento que no termine en jaque, el juego sigue
                                if not en_jaque:
                                    return True
        # Si revisamos TODO y nada nos salva... no hay movimientos válidos
        return False

    # -------------------------
    # ES MOVIMIENTO SEGURO (no deja al rey en jaque)
    # -------------------------
    def es_movimiento_seguro(self, orig_f, orig_c, dest_f, dest_c, color):
        copia = copy.deepcopy(self)
        copia.mover_pieza(orig_f, orig_c, dest_f, dest_c)

        rey_pos = None
        for fila in range(8):
            for col in range(8):
                pieza = copia.obtener_pieza(fila, col)
                if pieza and pieza.tipo == 'rey' and pieza.color == color:
                    rey_pos = (fila, col)
                    break
            if rey_pos:
                break

        if not rey_pos:
            return False

        color_oponente = 'oscura' if color == 'blanca' else 'blanca'
        return not copia.casilla_atacada_por(rey_pos[0], rey_pos[1], color_oponente)

    # -------------------------
    # OBTENER MOVIMIENTOS VÁLIDOS PARA UNA PIEZA
    # -------------------------
    def obtener_movimientos_validos(self, fila, col):
        movimientos = []
        pieza = self.obtener_pieza(fila, col)
        if not pieza:
            return movimientos

        # Fallback: probar todas las casillas geométricamente válidas
        geometricos = []
        for dest_f in range(8):
            for dest_c in range(8):
                if self.es_movimiento_valido(fila, col, dest_f, dest_c):
                    geometricos.append((dest_f, dest_c))

        for dest_f, dest_c in geometricos:
            if self.es_movimiento_seguro(fila, col, dest_f, dest_c, pieza.color):
                movimientos.append((dest_f, dest_c))

        return movimientos