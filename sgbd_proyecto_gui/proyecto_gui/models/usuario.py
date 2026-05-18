"""Módulo de la entidad Usuario."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    """
    Representa un usuario del sistema.
    
    Atributos:
        nombre (str): Nombre completo del usuario.
        email (str): Correo electrónico (único).
        tipo_usuario (str): Rol del usuario (ej. 'alumno', 'profesor', 'admin').
        id (Optional[int]): Identificador único del usuario (autogenerado por la BD SQL).
    """
    nombre: str
    email: str
    tipo_usuario: str
    id: Optional[int] = None
