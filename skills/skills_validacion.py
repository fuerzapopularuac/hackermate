"""
Skills de validación para el Agente Validador.
"""

from .skill_base import BaseSkill, SkillResultado
from typing import Dict, Any, Tuple
import copy

class ValidarLegalidadSkill(BaseSkill):
    """Skill que valida si un movimiento es legal"""
    
    def __init__(self):
        super().__init__("validar_legalidad")
        self.descripcion = "Valida si un movimiento específico es legal"
    
    def ejecutar(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int], color: str) -> Dict[str, Any]:
        pieza = tablero.obtener_pieza(desde[0], desde[1])
        
        if not pieza:
            return {"resultado": SkillResultado.FALLO, "datos": {"legal": False, "razon": "No hay pieza"}, "error": None}
        
        if pieza.color != color:
            return {"resultado": SkillResultado.FALLO, "datos": {"legal": False, "razon": "Color incorrecto"}, "error": None}
        
        if not tablero.es_movimiento_valido(desde[0], desde[1], hasta[0], hasta[1]):
            return {"resultado": SkillResultado.FALLO, "datos": {"legal": False, "razon": "Movimiento inválido"}, "error": None}
        
        if self._causa_auto_jaque(tablero, desde, hasta, color):
            return {"resultado": SkillResultado.FALLO, "datos": {"legal": False, "razon": "Auto-jaque"}, "error": None}
        
        return {"resultado": SkillResultado.EXITO, "datos": {"legal": True, "razon": None}, "error": None}
    
    def _causa_auto_jaque(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int], color: str) -> bool:
        copia = copy.deepcopy(tablero)
        copia.mover_pieza(desde[0], desde[1], hasta[0], hasta[1])
        
        rey_pos = None
        for fila in range(8):
            for col in range(8):
                p = copia.obtener_pieza(fila, col)
                if p and p.tipo == 'rey' and p.color == color:
                    rey_pos = (fila, col)
                    break
            if rey_pos:
                break
        
        if not rey_pos:
            return True
        
        color_oponente = 'oscura' if color == 'blanca' else 'blanca'
        
        for f in range(8):
            for c in range(8):
                p = copia.obtener_pieza(f, c)
                if p and p.color == color_oponente:
                    if copia.es_movimiento_valido(f, c, rey_pos[0], rey_pos[1]):
                        return True
        return False


class SimularMovimientoSkill(BaseSkill):
    """Skill que simula un movimiento sin modificar el original"""
    
    def __init__(self):
        super().__init__("simular_movimiento")
        self.descripcion = "Simula un movimiento y retorna el tablero resultante"
    
    def ejecutar(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int]) -> Dict[str, Any]:
        copia = copy.deepcopy(tablero)
        pieza = copia.obtener_pieza(desde[0], desde[1])
        
        if not pieza:
            return {"resultado": SkillResultado.FALLO, "datos": {"tablero_simulado": None}, "error": "No hay pieza"}
        
        copia.mover_pieza(desde[0], desde[1], hasta[0], hasta[1])
        
        return {"resultado": SkillResultado.EXITO, "datos": {"tablero_simulado": copia}, "error": None}


class VerificarAutoJaqueSkill(BaseSkill):
    """Skill específica para verificar auto-jaque"""
    
    def __init__(self):
        super().__init__("verificar_auto_jaque")
        self.descripcion = "Verifica si un movimiento deja al rey en jaque"
    
    def ejecutar(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int], color: str) -> Dict[str, Any]:
        sim_skill = SimularMovimientoSkill()
        resultado_sim = sim_skill.ejecutar(tablero, desde, hasta)
        
        if resultado_sim["resultado"] == SkillResultado.FALLO:
            return {"resultado": SkillResultado.EXITO, "datos": {"auto_jaque": True}, "error": None}
        
        tablero_sim = resultado_sim["datos"]["tablero_simulado"]
        
        rey_pos = None
        for fila in range(8):
            for col in range(8):
                pieza = tablero_sim.obtener_pieza(fila, col)
                if pieza and pieza.tipo == 'rey' and pieza.color == color:
                    rey_pos = (fila, col)
                    break
            if rey_pos:
                break
        
        if not rey_pos:
            return {"resultado": SkillResultado.EXITO, "datos": {"auto_jaque": True}, "error": None}
        
        color_oponente = 'oscura' if color == 'blanca' else 'blanca'
        
        for f in range(8):
            for c in range(8):
                p = tablero_sim.obtener_pieza(f, c)
                if p and p.color == color_oponente:
                    if tablero_sim.es_movimiento_valido(f, c, rey_pos[0], rey_pos[1]):
                        return {"resultado": SkillResultado.EXITO, "datos": {"auto_jaque": True}, "error": None}
        
        return {"resultado": SkillResultado.EXITO, "datos": {"auto_jaque": False}, "error": None}


class DetectarFinJuegoSkill(BaseSkill):
    """Skill que detecta si el juego ha terminado"""
    
    def __init__(self):
        super().__init__("detectar_fin_juego")
        self.descripcion = "Detecta jaque mate o ahogado"
    
    def ejecutar(self, tablero, color: str) -> Dict[str, Any]:
        from .skills_movimiento import GenerarMovimientosSkill
        
        gen_skill = GenerarMovimientosSkill()
        movimientos_res = gen_skill.ejecutar(tablero, color)
        tiene_movimientos = movimientos_res.get("datos", {}).get("total", 0) > 0
        
        # Usar reglas existente si está disponible
        try:
            from game.reglas import esta_en_jaque
            en_jaque = esta_en_jaque(tablero, color)
        except ImportError:
            en_jaque = self._verificar_jaque_simple(tablero, color)
        
        if not tiene_movimientos:
            if en_jaque:
                return {
                    "resultado": SkillResultado.EXITO,
                    "datos": {"fin_juego": True, "tipo": "jaque_mate", "ganador": 'oscura' if color == 'blanca' else 'blanca'},
                    "error": None
                }
            else:
                return {
                    "resultado": SkillResultado.EXITO,
                    "datos": {"fin_juego": True, "tipo": "ahogado", "ganador": None},
                    "error": None
                }
        
        return {
            "resultado": SkillResultado.EXITO,
            "datos": {"fin_juego": False, "tipo": "en_juego", "ganador": None},
            "error": None
        }
    
    def _verificar_jaque_simple(self, tablero, color: str) -> bool:
        rey_pos = None
        for fila in range(8):
            for col in range(8):
                pieza = tablero.obtener_pieza(fila, col)
                if pieza and pieza.tipo == 'rey' and pieza.color == color:
                    rey_pos = (fila, col)
                    break
            if rey_pos:
                break
        
        if not rey_pos:
            return False
        
        color_oponente = 'oscura' if color == 'blanca' else 'blanca'
        
        for f in range(8):
            for c in range(8):
                pieza = tablero.obtener_pieza(f, c)
                if pieza and pieza.color == color_oponente:
                    if tablero.es_movimiento_valido(f, c, rey_pos[0], rey_pos[1]):
                        return True
        return False