from typing import Dict, Any
from skills.skills_analisis import (
    AnalizarCentroSkill, DetectarAmenazasSkill,
    CalcularMaterialSkill, EvaluarSeguridadReySkill
)
from .base_agente import BaseAgente

class AgenteEstratega(BaseAgente):
    def __init__(self):
        super().__init__("Estratega")
        self.registrar_skill("analizar_centro", AnalizarCentroSkill())
        self.registrar_skill("detectar_amenazas", DetectarAmenazasSkill())
        self.registrar_skill("calcular_material", CalcularMaterialSkill())
        self.registrar_skill("evaluar_seguridad_rey", EvaluarSeguridadReySkill())

    def analizar(self, tablero, mi_color: str) -> Dict[str, Any]:
        centro_res = self.ejecutar_skill("analizar_centro", tablero=tablero, color_analizar=mi_color)
        amenazas_res = self.ejecutar_skill("detectar_amenazas", tablero=tablero, color_defensor=mi_color)
        material_res = self.ejecutar_skill("calcular_material", tablero=tablero)
        seguridad_res = self.ejecutar_skill("evaluar_seguridad_rey", tablero=tablero)

        datos_centro = centro_res.get("datos", {})
        datos_amenazas = amenazas_res.get("datos", {})
        datos_material = material_res.get("datos", {})
        datos_seguridad = seguridad_res.get("datos", {})

        if mi_color == "blanca":
            seguridad = datos_seguridad.get("seguridad_blancas", 50)
            ventaja_material = datos_material.get("ventaja_blancas", 0)
        else:
            seguridad = datos_seguridad.get("seguridad_negras", 50)
            ventaja_material = -datos_material.get("ventaja_blancas", 0)

        total_amenazas = datos_amenazas.get("total_amenazas", 0)

        if seguridad < 30:
            plan = "DEFENDER"
            profundidad = 3
            prioridad = "seguridad"
        elif ventaja_material > 100:
            plan = "ATACAR"
            profundidad = 4
            prioridad = "material"
        elif total_amenazas > 2:
            plan = "DEFENDER"
            profundidad = 3
            prioridad = "seguridad"
        elif ventaja_material > 0 or datos_centro.get("puntuacion", 0) > 0:
            plan = "ATACAR"
            profundidad = 3
            prioridad = "centro"
        else:
            plan = "DESARROLLAR"
            profundidad = 2
            prioridad = "centro"

        return {
            "plan": plan,
            "prioridad": prioridad,
            "profundidad": profundidad,
            "seguridad_rey": seguridad,
            "ventaja_material": ventaja_material,
            "total_amenazas": total_amenazas,
            "detalles": {
                "centro": datos_centro,
                "amenazas": datos_amenazas,
                "material": datos_material,
                "seguridad": datos_seguridad
            }
        }
