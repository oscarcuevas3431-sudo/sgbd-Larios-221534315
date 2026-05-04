"""Historial de acciones como pila LIFO."""


class Historial:
    """Pila de acciones usando lista."""

    def __init__(self) -> None:
        """Inicializa historial."""
        self._acciones = []

    def registrar(self, accion: str) -> None:
        """Agrega acción."""
        self._acciones.append(accion)

    def deshacer(self) -> str | None:
        """Quita la última acción."""
        if not self._acciones:
            return None
        return self._acciones.pop()

    def ver_historial(self) -> list:
        """Devuelve historial."""
        return list(self._acciones)
