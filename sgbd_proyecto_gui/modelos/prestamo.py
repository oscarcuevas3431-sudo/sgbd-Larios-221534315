"""Clase Prestamo."""

from datetime import date, datetime

from modelos.entidad import Entidad
from modelos.libro import Libro
from modelos.usuario import Usuario


class Prestamo(Entidad):
    """Representa un préstamo de libro."""

    def __init__(
        self,
        usuario: Usuario,
        libro: Libro,
        fecha_prestamo: str | None = None,
        fecha_devolucion: str | None = None,
        devuelto: bool = False,
        multa: float = 0.0,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa préstamo."""
        super().__init__(id_entidad, fecha_creacion)
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo or date.today().isoformat()
        self.fecha_devolucion = fecha_devolucion
        self.devuelto = devuelto
        self.multa = multa

    def cerrar(self, dias_retraso: int = 0) -> None:
        """Cierra préstamo y calcula multa."""
        self.fecha_devolucion = date.today().isoformat()
        self.devuelto = True
        self.libro.disponible = True
        self.usuario.prestamos_activos -= 1

        if hasattr(self.usuario, "calcular_multa"):
            self.multa = self.usuario.calcular_multa(dias_retraso)

    def __str__(self) -> str:
        """Representación legible."""
        estado = "Devuelto" if self.devuelto else "Activo"
        return f"Préstamo: {self.usuario.email} -> {self.libro.titulo} [{estado}]"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        return {
            "id": self.id,
            "fecha_creacion": self.fecha_creacion,
            "usuario_email": self.usuario.email,
            "libro_isbn": self.libro.isbn,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_devolucion": self.fecha_devolucion,
            "devuelto": self.devuelto,
            "multa": self.multa,
        }
