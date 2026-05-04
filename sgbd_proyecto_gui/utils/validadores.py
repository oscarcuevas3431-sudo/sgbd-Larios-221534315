"""Funciones de validación para datos del sistema."""


def validar_isbn13(isbn: str) -> bool:
    """Valida un ISBN-13 usando longitud, dígitos y dígito verificador.

    Args:
        isbn: Cadena que representa el ISBN.

    Returns:
        True si el ISBN-13 es válido, False en caso contrario.
    """
    if isbn is None:
        return False

    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) != 13 or not isbn.isdigit():
        return False

    suma = 0
    for indice, caracter in enumerate(isbn[:-1]):
        digito = int(caracter)
        if indice % 2 == 0:
            suma += digito
        else:
            suma += digito * 3

    digito_verificador = (10 - (suma % 10)) % 10
    return digito_verificador == int(isbn[-1])


def validar_email(email: str) -> bool:
    """Valida un email de forma básica.

    Args:
        email: Correo electrónico.

    Returns:
        True si parece un email válido.
    """
    if email is None or not isinstance(email, str):
        return False

    email = email.strip()

    if "@" not in email:
        return False

    usuario, dominio = email.split("@", 1)

    return (
        usuario != ""
        and dominio != ""
        and "." in dominio
        and not dominio.startswith(".")
        and not dominio.endswith(".")
    )


def validar_url(url: str) -> bool:
    """Valida una URL básica."""
    if not url:
        return False
    return url.startswith("http://") or url.startswith("https://")
