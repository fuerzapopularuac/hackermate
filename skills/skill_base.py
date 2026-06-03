"""
Base para todas las skills del sistema multiagente.
Toda skill debe heredar de esta clase.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime

class SkillResultado(Enum):
    """Posibles resultados al ejecutar una skill"""
    EXITO = "exito"
    FALLO = "fallo"
    PARCIAL = "parcial"
    NO_APLICA = "no_aplica"

class BaseSkill(ABC):
    """Clase base abstracta para todas las skills"""
    
    def __init__(self, nombre: str, version: str = "1.0"):
        self.nombre = nombre
        self.version = version
        self.descripcion = ""
        self._historial_ejecucion = []
    
    @abstractmethod
    def ejecutar(self, **kwargs) -> Dict[str, Any]:
        """
        Ejecuta la skill con los parámetros dados.
        
        Returns:
            Dict con: 
                - 'resultado': SkillResultado
                - 'datos': información específica
                - 'error': mensaje de error (si aplica)
        """
        pass
    
    def validar_parametros(self, **kwargs) -> tuple:
        """Valida que los parámetros sean correctos. Sobrescribir en skills hijas."""
        return True, None
    
    def get_metadata(self) -> Dict[str, Any]:
        """Retorna metadata de la skill para el supervisor"""
        return {
            "nombre": self.nombre,
            "version": self.version,
            "descripcion": self.descripcion,
            "parametros_requeridos": self._get_parametros_requeridos(),
            "parametros_opcionales": self._get_parametros_opcionales()
        }
    
    def _get_parametros_requeridos(self) -> list:
        return []
    
    def _get_parametros_opcionales(self) -> dict:
        return {}
    
    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")