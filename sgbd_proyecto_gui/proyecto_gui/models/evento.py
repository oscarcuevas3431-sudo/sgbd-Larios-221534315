"""Módulo de la entidad EventoSistema para bitácora (MongoDB)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class EventoSistema:
    """
    Representa un evento registrado en la bitácora del sistema (MongoDB).
    
    Atributos:
        tipo_evento (str): Nombre/Categoría del evento (ej. 'app_iniciada', 'libro_creado').
        descripcion (str): Detalles del evento.
        modulo (str): Módulo donde ocurrió el evento (ej. 'UI', 'Libros', 'Usuarios').
        fecha_hora (str): Fecha y hora exacta en formato ISO.
        id (Optional[str]): Identificador único autogenerado por MongoDB.
    """
    tipo_evento: str
    descripcion: str
    modulo: str
    fecha_hora: str = field(default_factory=lambda: datetime.now().isoformat())
    id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para insertarlo en MongoDB."""
        return {
            "tipo_evento": self.tipo_evento,
            "descripcion": self.descripcion,
            "modulo": self.modulo,
            "fecha_hora": self.fecha_hora
        }
