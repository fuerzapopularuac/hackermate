"""
Skills de movimiento para el Agente Ejecutor.
"""

from .skill_base import BaseSkill, SkillResultado
from .skills_analisis import VALORES_PIEZAS
from typing import Dict, Any, List, Tuple
import copy

class GenerarMovimientosSkill(BaseSkill):
    """Skill que genera todos los movimientos posibles para un color"""
    
    def __init__(self):
        super().__init__("generar_movimientos")
        self.descripcion = "Genera lista de todos los movimientos legales para un color"
    
    def ejecutar(self, tablero, color: str) -> Dict[str, Any]:
        movimientos = []
        
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza and pieza.color == color:
                    movimientos_pieza = tablero.obtener_movimientos_validos(fila, col)
                    for dest_f, dest_c in movimientos_pieza:
                        movimientos.append({
                            "desde": (fila, col),
                            "hasta": (dest_f, dest_c),
                            "pieza": pieza.tipo,
                            "color": color
                        })
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {"total": len(movimientos), "movimientos": movimientos},
            "error": None
        }


class EvaluarHeuristicaSkill(BaseSkill):
    """Skill que evalúa una posición del tablero con función heurística"""
    
    def __init__(self):
        super().__init__("evaluar_heuristica")
        self.descripcion = "Evalúa una posición con función heurística multi-factor"
        self._PESO_MATERIAL = 0.6
        self._PESO_CENTRO = 0.2
        self._PESO_MOVILIDAD = 0.2
    
    def ejecutar(self, tablero) -> Dict[str, Any]:
        material = self._evaluar_material(tablero)
        centro = self._evaluar_centro(tablero)
        movilidad = self._evaluar_movilidad(tablero)
        
        puntuacion = (material * self._PESO_MATERIAL + 
                      centro * self._PESO_CENTRO + 
                      movilidad * self._PESO_MOVILIDAD)
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {
                "puntuacion": puntuacion,
                "desglose": {"material": material, "centro": centro, "movilidad": movilidad}
            },
            "error": None
        }
    
    def _evaluar_material(self, tablero) -> int:
        blancas, negras = 0, 0
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza:
                    valor = VALORES_PIEZAS.get(pieza.tipo, 0)
                    if pieza.color == 'blanca':
                        blancas += valor
                    elif pieza.color == 'oscura':
                        negras += valor
        return blancas - negras
    
    def _evaluar_centro(self, tablero) -> int:
        centro_score = 0
        for fila, col in [(3,3), (3,4), (4,3), (4,4)]:
            pieza = tablero.obtener_pieza(fila, col)
            if pieza:
                centro_score += 5 if pieza.color == 'blanca' else -5 if pieza.color == 'oscura' else 0
        return centro_score
    
    def _evaluar_movilidad(self, tablero) -> int:
        gen_skill = GenerarMovimientosSkill()
        mov_blancas = gen_skill.ejecutar(tablero, 'blanca')
        mov_negras = gen_skill.ejecutar(tablero, 'oscura')
        return mov_blancas.get("datos", {}).get("total", 0) - mov_negras.get("datos", {}).get("total", 0)


class MinimaxBuscarSkill(BaseSkill):
    """Skill que ejecuta Minimax con poda Alpha-Beta"""
    
    def __init__(self):
        super().__init__("minimax_buscar")
        self.descripcion = "Busca el mejor movimiento usando Minimax"
        self._contador_nodos = 0
    
    def ejecutar(self, tablero, profundidad: int = 3, es_maximizador: bool = True,
                 alpha: float = -float('inf'), beta: float = float('inf')) -> Dict[str, Any]:
        
        if profundidad == 0:
            eval_skill = EvaluarHeuristicaSkill()
            resultado = eval_skill.ejecutar(tablero)
            return {
                "resultado": SkillResultado.EXITO,
                "datos": {"puntuacion": resultado.get("datos", {}).get("puntuacion", 0), "movimiento": None},
                "error": None
            }
        
        color_actual = 'blanca' if es_maximizador else 'oscura'
        gen_skill = GenerarMovimientosSkill()
        movimientos_res = gen_skill.ejecutar(tablero, color_actual)
        movimientos = movimientos_res.get("datos", {}).get("movimientos", [])
        
        if not movimientos:
            eval_skill = EvaluarHeuristicaSkill()
            resultado = eval_skill.ejecutar(tablero)
            return {
                "resultado": SkillResultado.EXITO,
                "datos": {"puntuacion": resultado.get("datos", {}).get("puntuacion", 0), "movimiento": None},
                "error": None
            }
        
        mejor_movimiento = None
        
        if es_maximizador:
            mejor_valor = -float('inf')
            for movimiento in movimientos:
                copia = copy.deepcopy(tablero)
                self._aplicar_movimiento(copia, movimiento)
                self._contador_nodos += 1
                
                resultado = self.ejecutar(copia, profundidad - 1, False, alpha, beta)
                valor = resultado.get("datos", {}).get("puntuacion", -float('inf'))
                
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
                
                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
        else:
            mejor_valor = float('inf')
            for movimiento in movimientos:
                copia = copy.deepcopy(tablero)
                self._aplicar_movimiento(copia, movimiento)
                self._contador_nodos += 1
                
                resultado = self.ejecutar(copia, profundidad - 1, True, alpha, beta)
                valor = resultado.get("datos", {}).get("puntuacion", float('inf'))
                
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento
                
                beta = min(beta, valor)
                if beta <= alpha:
                    break
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {
                "puntuacion": mejor_valor,
                "movimiento": mejor_movimiento,
                "nodos_evaluados": self._contador_nodos
            },
            "error": None
        }
    
    def _aplicar_movimiento(self, tablero, movimiento: dict):
        desde = movimiento["desde"]
        hasta = movimiento["hasta"]
        tablero.mover_pieza(desde[0], desde[1], hasta[0], hasta[1])