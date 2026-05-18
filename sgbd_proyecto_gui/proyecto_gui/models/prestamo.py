"""Módulo de la entidad Prestamo."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Prestamo:
    """
    Representa el préstamo de un libro a un usuario.
    
    Atributos:
        libro_id (int): Clave foránea al ID del libro prestado.
        usuario_id (int): Clave foránea al ID del usuario que solicita el préstamo.
        fecha_prestamo (datetime): Fecha y hora en la que se realizó el préstamo.
        estado (str): Estado actual del préstamo (ej. 'activo', 'devuelto', 'atrasado').
        fecha_devolucion (Optional[datetime]): Fecha esperada o real de devolución.
        id (Optional[int]): Identificador único del préstamo (autogenerado por SQL).
    """
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    estado: str = "activo"
    fecha_devolucion: Optional[datetime] = None
    id: Optional[int] = None
