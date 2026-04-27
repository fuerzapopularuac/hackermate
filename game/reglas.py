def movimiento_valido(tablero, pieza, f1, c1, f2, c2):

    # fuera del tablero
    if not (0 <= f2 < 8 and 0 <= c2 < 8):
        return False

    destino = tablero.obtener_pieza(f2, c2)

    # no comer tu propia pieza
    if destino and destino.color == pieza.color:
        return False

    # -------------------------
    # PEON
    # -------------------------
    if pieza.tipo == "peon":

        direccion = -1 if pieza.color == "blanca" else 1

        if c1 == c2 and destino is None:
            if f2 == f1 + direccion:
                return True

            if (pieza.color == "blanca" and f1 == 6) or (pieza.color == "oscura" and f1 == 1):
                if f2 == f1 + 2 * direccion and tablero.obtener_pieza(f1 + direccion, c1) is None:
                    return True

        if abs(c2 - c1) == 1 and f2 == f1 + direccion:
            if destino and destino.color != pieza.color:
                return True

        return False

    # -------------------------
    # TORRE
    # -------------------------
    if pieza.tipo == "torre":

        if f1 == f2 or c1 == c2:

            paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
            paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

            f, c = f1 + paso_f, c1 + paso_c

            while (f, c) != (f2, c2):
                if tablero.obtener_pieza(f, c):
                    return False
                f += paso_f
                c += paso_c

            return True

        return False

    # -------------------------
    # CABALLO
    # -------------------------
    if pieza.tipo == "caballo":
        return (abs(f2 - f1), abs(c2 - c1)) in [(2,1), (1,2)]

    # -------------------------
    # ALFIL
    # -------------------------
    if pieza.tipo == "alfil":

        if abs(f2 - f1) == abs(c2 - c1):

            paso_f = 1 if f2 > f1 else -1
            paso_c = 1 if c2 > c1 else -1

            f, c = f1 + paso_f, c1 + paso_c

            while (f, c) != (f2, c2):
                if tablero.obtener_pieza(f, c):
                    return False
                f += paso_f
                c += paso_c

            return True

        return False

    # -------------------------
    # REINA (ARREGLADA 🔥)
    # -------------------------
    if pieza.tipo == "reina":

        # como torre
        if f1 == f2 or c1 == c2:

            paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
            paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)

            f, c = f1 + paso_f, c1 + paso_c

            while (f, c) != (f2, c2):
                if tablero.obtener_pieza(f, c):
                    return False
                f += paso_f
                c += paso_c

            return True

        # como alfil
        if abs(f2 - f1) == abs(c2 - c1):

            paso_f = 1 if f2 > f1 else -1
            paso_c = 1 if c2 > c1 else -1

            f, c = f1 + paso_f, c1 + paso_c

            while (f, c) != (f2, c2):
                if tablero.obtener_pieza(f, c):
                    return False
                f += paso_f
                c += paso_c

            return True

        return False

    # -------------------------
    # REY
    # -------------------------
    if pieza.tipo == "rey":
        # Movimiento normal de 1 casilla
        if abs(f2 - f1) <= 1 and abs(c2 - c1) <= 1:
            return True

        #  SPRINT 3: LÓGICA DE ENROQUE 
        # Si el rey no se ha movido, se mueve en la misma fila, y salta 2 columnas
        if not pieza.ha_movido and f1 == f2 and abs(c2 - c1) == 2:
            
            # Determinar si es enroque corto (derecha) o largo (izquierda)
            if c2 > c1: 
                c_torre = 7
                paso = 1
            else:       
                c_torre = 0
                paso = -1
                
            torre = tablero.obtener_pieza(f1, c_torre)
            
            # Verificamos que sea la torre y no se haya movido
            if torre and torre.tipo == "torre" and not torre.ha_movido:
                
                # 1. Verificar que no haya piezas en medio
                c_actual = c1 + paso
                while c_actual != c_torre:
                    if tablero.obtener_pieza(f1, c_actual):
                        return False
                    c_actual += paso
                    
                # 2. Verificar que el rey no esté en jaque actualmente
                if esta_en_jaque(tablero, pieza.color):
                    return False
                    
                # 3. Verificar que el rey no pase por una casilla amenazada (simulación rápida)
                tablero.matriz[f1][c1+paso] = pieza
                tablero.matriz[f1][c1] = None
                jaque_intermedio = esta_en_jaque(tablero, pieza.color)
                
                # Revertimos la simulación
                tablero.matriz[f1][c1] = pieza
                tablero.matriz[f1][c1+paso] = None
                
                if jaque_intermedio:
                    return False
                    
                return True

        return False

#  SPRINT 3: DETECCIÓN DE JAQUE 
def esta_en_jaque(tablero, color_rey):
    f_rey = -1
    c_rey = -1
    
    # 1. Encontrar la posición del rey de este color
    for f in range(8):
        for c in range(8):
            p = tablero.obtener_pieza(f, c)
            if p and p.tipo == "rey" and p.color == color_rey:
                f_rey, c_rey = f, c
                break
        if f_rey != -1:
            break
            
    if f_rey == -1:
        return False # Por si acaso
        
    # 2. Verificar si alguna pieza enemiga puede llegar al rey
    for f in range(8):
        for c in range(8):
            p = tablero.obtener_pieza(f, c)
            if p and p.color != color_rey:
                # Si un enemigo tiene un movimiento válido hacia el rey, es jaque
                if movimiento_valido(tablero, p, f, c, f_rey, c_rey):
                    return True
                    
    return False