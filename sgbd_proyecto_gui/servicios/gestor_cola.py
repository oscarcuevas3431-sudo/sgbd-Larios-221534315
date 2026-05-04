"""Gestor de cola de espera FIFO."""

from collections import deque


class GestorCola:
    """Cola de espera usando deque."""

    def __init__(self) -> None:
        """Inicializa la cola."""
        self._cola = deque()

    def encolar_solicitud(self, usuario_email: str, isbn: str) -> None:
        """Agrega una solicitud al final de la cola."""
        self._cola.append((usuario_email, isbn))

    def atender_siguiente(self) -> tuple | None:
        """Atiende la primera solicitud."""
        if not self._cola:
            return None
        return self._cola.popleft()

    def ver_cola(self) -> list:
        """Devuelve la cola como lista."""
        return list(self._cola)
