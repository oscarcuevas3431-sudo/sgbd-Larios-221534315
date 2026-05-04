"""Clase abstracta base para entidades del sistema."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class Entidad(ABC):
    """Clase base abstracta con id y fecha de creación."""

    def __init__(self, id_entidad: str | None = None,
                 fecha_creacion: str | None = None) -> None:
        """Inicializa una entidad."""
        self._id = id_entidad if id_entidad else str(uuid4())
        self._fecha_creacion = (
            fecha_creacion if fecha_creacion else datetime.now().isoformat()
        )

    @property
    def id(self) -> str:
        """Devuelve el ID."""
        return self._id

    @property
    def fecha_creacion(self) -> str:
        """Devuelve la fecha de creación."""
        return self._fecha_creacion

    @abstractmethod
    def __str__(self) -> str:
        """Representación legible."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario."""
        raise NotImplementedError
