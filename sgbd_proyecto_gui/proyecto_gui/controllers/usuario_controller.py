"""Controlador para la gestión de usuarios."""

from typing import List
from models.usuario import Usuario
from repositories.sql_repository import SQLRepository


class UsuarioController:
    """Intermediario entre la UI de Usuarios y el Repositorio."""

    def __init__(self) -> None:
        self.repo = SQLRepository()

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene la lista de todos los usuarios."""
        return self.repo.obtener_usuarios()

    def agregar_usuario(self, nombre: str, email: str, tipo_usuario: str) -> Usuario:
        """Valida y agrega un usuario."""
        if not nombre or not email or not tipo_usuario:
            raise ValueError("Todos los campos (Nombre, Email, Tipo) son obligatorios.")
            
        nuevo_usuario = Usuario(nombre=nombre, email=email, tipo_usuario=tipo_usuario)
        return self.repo.crear_usuario(nuevo_usuario)

    def actualizar_usuario(self, usuario_id: int, nombre: str, email: str, tipo_usuario: str) -> None:
        """Valida y actualiza un usuario existente."""
        if not nombre or not email or not tipo_usuario:
            raise ValueError("Todos los campos son obligatorios.")
            
        usuario_actualizado = Usuario(
            id=usuario_id,
            nombre=nombre,
            email=email,
            tipo_usuario=tipo_usuario
        )
        self.repo.actualizar_usuario(usuario_actualizado)

    def eliminar_usuario(self, usuario_id: int) -> None:
        """Elimina un usuario de la BD."""
        self.repo.eliminar_usuario(usuario_id)
