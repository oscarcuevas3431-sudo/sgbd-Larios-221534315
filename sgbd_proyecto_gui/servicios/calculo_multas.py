"""Cálculo de multas por retraso."""

from utils.constantes import (
    DIAS_RETRASO_LARGO,
    MULTA_DIARIA_ADMIN_MXN,
    MULTA_DIARIA_ALUMNO_MXN,
    MULTA_DIARIA_PROFESOR_MXN,
    PENALIZACION_RETRASO_LARGO,
)


def calcular_multa(dias_retraso: int, tipo_usuario: str) -> float:
    """Calcula multa usando if/elif/else.

    Args:
        dias_retraso: Días de retraso.
        tipo_usuario: alumno, profesor o admin.

    Returns:
        Monto de multa.
    """
    if dias_retraso <= 0:
        return 0.0

    tipo = tipo_usuario.lower().strip()

    if tipo == "alumno":
        tarifa = MULTA_DIARIA_ALUMNO_MXN
    elif tipo == "profesor":
        tarifa = MULTA_DIARIA_PROFESOR_MXN
    elif tipo == "admin":
        tarifa = MULTA_DIARIA_ADMIN_MXN
    else:
        raise ValueError("Tipo de usuario no válido.")

    multa = dias_retraso * tarifa

    if dias_retraso > DIAS_RETRASO_LARGO and tarifa != 0:
        multa += multa * PENALIZACION_RETRASO_LARGO

    return float(multa)


def calcular_multa_match(dias_retraso: int, tipo_usuario: str) -> float:
    """Calcula multa usando match/case."""
    if dias_retraso <= 0:
        return 0.0

    match tipo_usuario.lower().strip():
        case "alumno":
            tarifa = MULTA_DIARIA_ALUMNO_MXN
        case "profesor":
            tarifa = MULTA_DIARIA_PROFESOR_MXN
        case "admin":
            tarifa = MULTA_DIARIA_ADMIN_MXN
        case _:
            raise ValueError("Tipo de usuario no válido.")

    multa = dias_retraso * tarifa

    if dias_retraso > DIAS_RETRASO_LARGO and tarifa != 0:
        multa *= 1 + PENALIZACION_RETRASO_LARGO

    return float(multa)


if __name__ == "__main__":
    print(calcular_multa(0, "alumno"))
    print(calcular_multa(5, "alumno"))
    print(calcular_multa(5, "profesor"))
    print(calcular_multa(5, "admin"))
    print(calcular_multa(31, "alumno"))
    print(calcular_multa_match(31, "profesor"))
