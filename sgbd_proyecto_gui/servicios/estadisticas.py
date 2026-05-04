"""Funciones de estadísticas del sistema."""

from collections import Counter, defaultdict


def libro_mas_prestado(prestamos: list) -> tuple | None:
    """Obtiene el ISBN más prestado."""
    contador = Counter(prestamo.libro.isbn for prestamo in prestamos)
    if not contador:
        return None
    return contador.most_common(1)[0]


def usuario_con_mas_prestamos(prestamos: list) -> tuple | None:
    """Obtiene usuario con más préstamos."""
    contador = Counter(prestamo.usuario.email for prestamo in prestamos)
    if not contador:
        return None
    return contador.most_common(1)[0]


def multa_promedio(prestamos: list) -> float:
    """Calcula multa promedio."""
    multas = [prestamo.multa for prestamo in prestamos]
    if not multas:
        return 0.0
    return sum(multas) / len(multas)


def distribucion_por_genero(libros: list) -> dict:
    """Agrupa libros por género usando defaultdict."""
    distribucion = defaultdict(list)
    for libro in libros:
        distribucion[libro.genero].append(libro.titulo)
    return dict(distribucion)
