"""
Skills de análisis para el Agente Estratega.
Evalúan diferentes aspectos del tablero sin modificarlo.
"""

from .skill_base import BaseSkill, SkillResultado
from typing import Dict, Any, List, Tuple

# Constantes de valores de piezas
VALORES_PIEZAS = {
    'peon': 10,
    'caballo': 30,
    'alfil': 30,
    'torre': 50,
    'reina': 90,
    'rey': 900
}

class AnalizarCentroSkill(BaseSkill):
    """Skill que analiza el control del centro del tablero"""
    
    def __init__(self):
        super().__init__("analizar_centro")
        self.descripcion = "Evalúa qué jugador controla más el centro del tablero"
        self._CASILLAS_CENTRO = [(3,3), (3,4), (4,3), (4,4)]
        self._PESO_CENTRO = 10
        self._CASILLAS_EXTENDIDAS = [(2,2), (2,3), (2,4), (2,5), (3,2), (3,5), (4,2), (4,5), (5,2), (5,3), (5,4), (5,5)]
        self._PESO_EXTENDIDO = 5
    
    def ejecutar(self, tablero, color_analizar: str = None) -> Dict[str, Any]:
        score_blancas = 0
        score_negras = 0
        
        for fila, col in self._CASILLAS_CENTRO:
            pieza = tablero.obtener_pieza(fila, col)
            if pieza:
                if pieza.color == 'blanca':
                    score_blancas += self._PESO_CENTRO
                elif pieza.color == 'oscura':
                    score_negras += self._PESO_CENTRO
        
        for fila, col in self._CASILLAS_EXTENDIDAS:
            pieza = tablero.obtener_pieza(fila, col)
            if pieza:
                if pieza.color == 'blanca':
                    score_blancas += self._PESO_EXTENDIDO
                elif pieza.color == 'oscura':
                    score_negras += self._PESO_EXTENDIDO

        resultado = {
            "control_blancas": score_blancas,
            "control_negras": score_negras,
            "ventaja_blancas": score_blancas - score_negras,
            "dominio_centro": "blancas" if score_blancas > score_negras else "negras" if score_negras > score_blancas else "equilibrado"
        }
        
        if color_analizar:
            resultado["puntuacion"] = score_blancas if color_analizar == 'blanca' else score_negras
        
        return {"resultado": SkillResultado.EXITO, "datos": resultado, "error": None}


class DetectarAmenazasSkill(BaseSkill):
    """Skill que detecta piezas que están siendo atacadas"""
    
    def __init__(self):
        super().__init__("detectar_amenazas")
        self.descripcion = "Detecta qué piezas están siendo amenazadas por el oponente"
    
    def ejecutar(self, tablero, color_defensor: str) -> Dict[str, Any]:
        color_atacante = 'oscura' if color_defensor == 'blanca' else 'blanca'
        amenazas = []
        
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza and pieza.color == color_defensor:
                    if self._casilla_atacada(tablero, fila, col, color_atacante):
                        amenazas.append({
                            "pieza": pieza.tipo,
                            "color": pieza.color,
                            "posicion": (fila, col),
                            "valor": VALORES_PIEZAS.get(pieza.tipo, 0)
                        })
        
        amenazas.sort(key=lambda x: x["valor"], reverse=True)
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {
                "total_amenazas": len(amenazas),
                "amenazas": amenazas,
                "peligro_maximo": amenazas[0] if amenazas else None
            },
            "error": None
        }
    
    def _casilla_atacada(self, tablero, fila: int, col: int, color_atacante: str) -> bool:
        # Implementación básica - verifica si alguna pieza enemiga puede mover a esta casilla
        for f in range(8):
            for c in range(8):
                pieza = tablero.obtener_pieza(f, c)
                if pieza and pieza.color == color_atacante:
                    if tablero.es_movimiento_valido(f, c, fila, col):
                        return True
        return False


class CalcularMaterialSkill(BaseSkill):
    """Skill que calcula el valor total del material en el tablero"""
    
    def __init__(self):
        super().__init__("calcular_material")
        self.descripcion = "Calcula el valor total de piezas de cada jugador"
    
    def ejecutar(self, tablero) -> Dict[str, Any]:
        total_blancas = 0
        total_negras = 0
        
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza:
                    valor = VALORES_PIEZAS.get(pieza.tipo, 0)
                    if pieza.color == 'blanca':
                        total_blancas += valor
                    elif pieza.color == 'oscura':
                        total_negras += valor
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {
                "blancas": total_blancas,
                "negras": total_negras,
                "ventaja_blancas": total_blancas - total_negras
            },
            "error": None
        }


class EvaluarSeguridadReySkill(BaseSkill):
    """Skill que evalúa qué tan seguro está el rey de cada color"""
    
    def __init__(self):
        super().__init__("evaluar_seguridad_rey")
        self.descripcion = "Evalúa la seguridad del rey"
    
    def ejecutar(self, tablero) -> Dict[str, Any]:
        seguridad_blancas = self._evaluar_rey(tablero, 'blanca')
        seguridad_negras = self._evaluar_rey(tablero, 'oscura')
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {
                "seguridad_blancas": seguridad_blancas,
                "seguridad_negras": seguridad_negras,
                "rey_blancos_amenazado": seguridad_blancas < 50,
                "rey_negros_amenazado": seguridad_negras < 50
            },
            "error": None
        }
    
    def _evaluar_rey(self, tablero, color: str) -> int:
        pos_rey = None
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza and pieza.tipo == 'rey' and pieza.color == color:
                    pos_rey = (fila, col)
                    break
            if pos_rey:
                break
        
        if not pos_rey:
            return 0
        
        score = 50
        color_oponente = 'oscura' if color == 'blanca' else 'blanca'
        
        if self._casilla_atacada(tablero, pos_rey[0], pos_rey[1], color_oponente):
            score -= 30
        
        return max(0, min(100, score))
    
    def _casilla_atacada(self, tablero, fila: int, col: int, color_atacante: str) -> bool:
        for f in range(8):
            for c in range(8):
                pieza = tablero.obtener_pieza(f, c)
                if pieza and pieza.color == color_atacante:
                    if tablero.es_movimiento_valido(f, c, fila, col):
                        return True
        return False