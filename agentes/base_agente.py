from typing import Dict, Any
from skills.skill_base import BaseSkill, SkillResultado

class BaseAgente:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._skills: Dict[str, BaseSkill] = {}

    def registrar_skill(self, nombre: str, skill: BaseSkill):
        self._skills[nombre] = skill

    def ejecutar_skill(self, nombre: str, **kwargs) -> Dict[str, Any]:
        skill = self._skills.get(nombre)
        if not skill:
            return {
                "resultado": SkillResultado.FALLO,
                "datos": {},
                "error": f"Skill '{nombre}' no encontrada"
            }
        return skill.ejecutar(**kwargs)

    def listar_skills(self) -> Dict[str, Any]:
        return {nombre: skill.get_metadata() for nombre, skill in self._skills.items()}
