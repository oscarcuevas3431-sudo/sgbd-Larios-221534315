"""Controlador para la gestión de libros."""

from typing import List
from models.libro import Libro
from repositories.sql_repository import SQLRepository


class LibroController:
    """
    Controlador que actúa como intermediario entre la Interfaz Gráfica (UI) 
    y el Repositorio de base de datos para la entidad Libro.
    """

    def __init__(self) -> None:
        """Inicializa el controlador instanciando el repositorio."""
        self.repo = SQLRepository()

    def obtener_todos(self) -> List[Libro]:
        """Obtiene la lista de todos los libros desde la base de datos."""
        return self.repo.obtener_libros()

    def obtener_por_id(self, libro_id: int) -> Libro:
        """Obtiene un libro por ID. Útil para el callback de selección."""
        libro = self.repo.obtener_libro_por_id(libro_id)
        if not libro:
            raise ValueError(f"No se encontró el libro con ID {libro_id}")
        return libro

    def agregar_libro(self, titulo: str, autor: str, isbn: str, anio: str, genero: str, disponible: str) -> Libro:
        """Valida los datos recibidos de la vista y crea un nuevo libro."""
        self._validar_campos(titulo, autor, isbn, anio)
        
        anio_int = int(anio)
        disp_bool = (disponible == "Sí")
        
        nuevo_libro = Libro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            anio=anio_int,
            genero=genero,
            disponibilidad=disp_bool
        )
        return self.repo.crear_libro(nuevo_libro)

    def actualizar_libro(self, libro_id: int, titulo: str, autor: str, isbn: str, anio: str, genero: str, disponible: str) -> None:
        """Valida los datos y actualiza un libro existente."""
        self._validar_campos(titulo, autor, isbn, anio)
            
        anio_int = int(anio)
        disp_bool = (disponible == "Sí")
        
        libro_actualizado = Libro(
            id=libro_id,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            anio=anio_int,
            genero=genero,
            disponibilidad=disp_bool
        )
        self.repo.actualizar_libro(libro_actualizado)

    def eliminar_libro(self, libro_id: int) -> None:
        """Elimina un libro de la base de datos dado su ID."""
        self.repo.eliminar_libro(libro_id)

    def buscar_libros(self, termino: str) -> List[Libro]:
        """Busca libros que coincidan con el término (título o autor)."""
        return self.repo.buscar_libros(termino)

    def respaldar_datos(self) -> None:
        """Llama al repositorio para generar un respaldo de la base de datos."""
        self.repo.respaldar_bd()

    def _validar_campos(self, titulo: str, autor: str, isbn: str, anio: str) -> None:
        """Valida que los campos obligatorios no estén vacíos y tengan formatos correctos."""
        if not titulo or not autor or not isbn or not anio:
            raise ValueError("Los campos Título, Autor, ISBN y Año son obligatorios.")
        
        try:
            int(anio)
        except ValueError:
            raise ValueError("El año debe ser un número entero válido (ej. 2023).")
