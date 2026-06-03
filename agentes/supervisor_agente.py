from typing import Dict, Any, Optional
from .agente_estratega import AgenteEstratega
from .agente_ejecutor import AgenteEjecutor
from .agente_validador import AgenteValidador

class SupervisorAgente:
    def __init__(self, profundidad: Optional[int] = None):
        self.estratega = AgenteEstratega()
        self.ejecutor = AgenteEjecutor()
        self.validador = AgenteValidador()
        self.profundidad = profundidad
        self.ultima_estrategia = None

    def jugar_turno(self, tablero, mi_color: str, callback_estado=None) -> Optional[Dict[str, Any]]:
        if callback_estado:
            callback_estado("🤖 Supervisor: coordinando turno de IA")
            callback_estado("🧠 Estratega: analizando centro...")
        estrategia = self.estratega.analizar(tablero, mi_color)
        if self.profundidad is not None:
            estrategia["profundidad"] = self.profundidad
        self.ultima_estrategia = estrategia

        if callback_estado:
            callback_estado("🎯 Ejecutor: generando movimientos...")
            callback_estado(f"🎯 Ejecutor: ejecutando Minimax (profundidad {estrategia.get('profundidad', '?')})...")
        movimiento = self.ejecutor.elegir_movimiento(tablero, mi_color, estrategia)

        if not movimiento:
            return None

        if callback_estado:
            callback_estado("✅ Validador: verificando legalidad...")
        legal, razon = self.validador.validar_movimiento(
            tablero, movimiento["desde"], movimiento["hasta"], mi_color
        )

        if not legal:
            return None

        if callback_estado:
            callback_estado("✅ Validador: comprobando auto-jaque...")
        fin_juego = self.validador.detectar_fin_juego(tablero, mi_color)

        return {
            "movimiento": movimiento,
            "estrategia": estrategia,
            "fin_juego": fin_juego
        }

    def obtener_info(self) -> Dict[str, Any]:
        return {
            "estratega_skills": self.estratega.listar_skills(),
            "ejecutor_skills": self.ejecutor.listar_skills(),
            "validador_skills": self.validador.listar_skills(),
            "ultima_estrategia": self.ultima_estrategia
        }
