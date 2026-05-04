"""Pruebas básicas opcionales."""

from modelos.libro import Libro
from servicios.calculo_multas import calcular_multa
from utils.validadores import validar_email, validar_isbn13


def test_validar_email() -> None:
    """Prueba email."""
    assert validar_email("test@udg.mx")
    assert not validar_email("correo_mal")


def test_validar_isbn13() -> None:
    """Prueba ISBN."""
    assert validar_isbn13("9780306406157")


def test_calcular_multa() -> None:
    """Prueba multa."""
    assert calcular_multa(2, "alumno") == 10.0
    assert calcular_multa(2, "profesor") == 4.0
    assert calcular_multa(2, "admin") == 0.0


def test_libro() -> None:
    """Prueba libro."""
    libro = Libro("Python", "Autor", "9780306406157", 2020, "programacion")
    assert libro.titulo == "Python"
    assert libro.disponible
