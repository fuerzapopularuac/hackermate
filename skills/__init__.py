# Inicializador del paquete skills
from .skill_base import BaseSkill, SkillResultado
from .skills_analisis import AnalizarCentroSkill, DetectarAmenazasSkill, CalcularMaterialSkill, EvaluarSeguridadReySkill
from .skills_movimiento import GenerarMovimientosSkill, EvaluarHeuristicaSkill, MinimaxBuscarSkill
from .skills_validacion import ValidarLegalidadSkill, SimularMovimientoSkill, VerificarAutoJaqueSkill, DetectarFinJuegoSkill

__all__ = [
    'BaseSkill',
    'SkillResultado',
    'AnalizarCentroSkill',
    'DetectarAmenazasSkill',
    'CalcularMaterialSkill',
    'EvaluarSeguridadReySkill',
    'GenerarMovimientosSkill',
    'EvaluarHeuristicaSkill',
    'MinimaxBuscarSkill',
    'ValidarLegalidadSkill',
    'SimularMovimientoSkill',
    'VerificarAutoJaqueSkill',
    'DetectarFinJuegoSkill'
]