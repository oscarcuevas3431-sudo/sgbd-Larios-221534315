"""Funciones para limpiar y formatear textos."""

import re
import unicodedata


def normalizar_titulo(titulo: str) -> str:
    """Limpia y capitaliza un título."""
    if not titulo:
        return ""

    titulo = titulo.strip()
    titulo = re.sub(r"[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 ,]", "", titulo)
    palabras = titulo.split()
    return " ".join(palabras).title()


def generar_slug(texto: str) -> str:
    """Convierte texto a formato slug."""
    if not texto:
        return ""

    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    texto = "-".join(texto.split())
    return texto


def formatear_reporte_libro(libro_dict: dict) -> str:
    """Genera reporte de un libro usando f-strings."""
    return (
        f"{'Título':<15}: {libro_dict.get('titulo', 'N/A')}\n"
        f"{'Autor':<15}: {libro_dict.get('autor', 'N/A')}\n"
        f"{'ISBN':<15}: {libro_dict.get('isbn', 'N/A')}\n"
        f"{'Año':<15}: {libro_dict.get('anio', 'N/A')}\n"
        f"{'Género':<15}: {libro_dict.get('genero', 'N/A')}\n"
        f"{'Disponible':<15}: {libro_dict.get('disponible', 'N/A')}"
    )


def buscar_en_texto(haystack: str, needle: str) -> bool:
    """Busca texto sin importar mayúsculas/minúsculas."""
    if haystack is None or needle is None:
        return False
    return haystack.lower().find(needle.lower()) != -1
