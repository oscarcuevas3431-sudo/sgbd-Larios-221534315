"""Controlador para la gestión de préstamos."""

from datetime import datetime
from typing import List, Dict, Any
from models.prestamo import Prestamo
from repositories.sql_repository import SQLRepository


class PrestamoController:
    """Intermediario entre la UI de Préstamos y el Repositorio."""

    def __init__(self) -> None:
        self.repo = SQLRepository()

    def obtener_activos(self) -> List[Dict[str, Any]]:
        """Devuelve los préstamos activos con información enriquecida (unida)."""
        return self.repo.obtener_prestamos_activos()

    def prestar_libro(self, libro_id: int, usuario_id: int) -> Prestamo:
        """Verifica la disponibilidad y registra el préstamo transaccionalmente."""
        if not libro_id or not usuario_id:
            raise ValueError("Debes seleccionar un libro y un usuario válido.")
            
        nuevo_prestamo = Prestamo(
            libro_id=libro_id,
            usuario_id=usuario_id,
            fecha_prestamo=datetime.now()
        )
        return self.repo.registrar_prestamo_transaccion(nuevo_prestamo)

    def devolver_libro(self, prestamo_id: int) -> None:
        """Registra la devolución transaccionalmente."""
        if not prestamo_id:
            raise ValueError("Debes seleccionar un préstamo activo para devolver.")
            
        fecha_devolucion = datetime.now().isoformat()
        self.repo.registrar_devolucion_transaccion(prestamo_id, fecha_devolucion)
