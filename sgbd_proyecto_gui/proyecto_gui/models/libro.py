"""Módulo de la entidad Libro."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Libro:
    """
    Representa un libro dentro de la biblioteca.
    
    Atributos:
        titulo (str): Título de la obra.
        autor (str): Nombre del autor.
        isbn (str): Código ISBN del libro.
        anio (int): Año de publicación.
        genero (str): Género o categoría literaria.
        disponibilidad (bool): True si está disponible, False si está prestado.
        id (Optional[int]): Identificador único del libro (autogenerado por la BD SQL).
    """
    titulo: str
    autor: str
    isbn: str
    anio: int
    genero: str
    disponibilidad: bool = True
    id: Optional[int] = None
