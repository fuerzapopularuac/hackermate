from typing import Dict, Any, Optional
from skills.skills_movimiento import (
    GenerarMovimientosSkill, EvaluarHeuristicaSkill, MinimaxBuscarSkill
)
from .base_agente import BaseAgente

class AgenteEjecutor(BaseAgente):
    def __init__(self):
        super().__init__("Ejecutor")
        self.registrar_skill("generar_movimientos", GenerarMovimientosSkill())
        self.registrar_skill("evaluar_heuristica", EvaluarHeuristicaSkill())
        self.registrar_skill("minimax_buscar", MinimaxBuscarSkill())

    def elegir_movimiento(self, tablero, mi_color: str, estrategia: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        profundidad = estrategia.get("profundidad", 3)
        es_maximizador = (mi_color == "blanca")

        minimax_res = self.ejecutar_skill(
            "minimax_buscar",
            tablero=tablero,
            profundidad=profundidad,
            es_maximizador=es_maximizador
        )

        movimiento = minimax_res.get("datos", {}).get("movimiento")

        if not movimiento:
            gen_res = self.ejecutar_skill("generar_movimientos", tablero=tablero, color=mi_color)
            movimientos = gen_res.get("datos", {}).get("movimientos", [])
            if movimientos:
                movimiento = movimientos[0]

        return movimiento
