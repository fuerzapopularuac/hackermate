from typing import Dict, Any, Tuple, Optional
from skills.skills_validacion import (
    ValidarLegalidadSkill, DetectarFinJuegoSkill,
    VerificarAutoJaqueSkill, SimularMovimientoSkill
)
from .base_agente import BaseAgente

class AgenteValidador(BaseAgente):
    def __init__(self):
        super().__init__("Validador")
        self.registrar_skill("validar_legalidad", ValidarLegalidadSkill())
        self.registrar_skill("detectar_fin_juego", DetectarFinJuegoSkill())
        self.registrar_skill("verificar_auto_jaque", VerificarAutoJaqueSkill())
        self.registrar_skill("simular_movimiento", SimularMovimientoSkill())

    def validar_movimiento(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int], color: str) -> Tuple[bool, Optional[str]]:
        res = self.ejecutar_skill("validar_legalidad", tablero=tablero, desde=desde, hasta=hasta, color=color)
        datos = res.get("datos", {})
        return datos.get("legal", False), datos.get("razon")

    def detectar_fin_juego(self, tablero, color: str) -> Dict[str, Any]:
        res = self.ejecutar_skill("detectar_fin_juego", tablero=tablero, color=color)
        return res.get("datos", {})

    def verificar_auto_jaque(self, tablero, desde: Tuple[int, int], hasta: Tuple[int, int], color: str) -> bool:
        res = self.ejecutar_skill("verificar_auto_jaque", tablero=tablero, desde=desde, hasta=hasta, color=color)
        return res.get("datos", {}).get("auto_jaque", True)
