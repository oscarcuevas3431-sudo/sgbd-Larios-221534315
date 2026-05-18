"""Punto de entrada de la interfaz gráfica del Sistema de Gestión."""

from ui.main_window import MainWindow


def main() -> None:
    """Inicia la aplicación gráfica principal."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
