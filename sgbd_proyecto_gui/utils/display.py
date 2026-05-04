"""Funciones de visualización y reportes."""


def mostrar_info(item: object) -> None:
    """Muestra información usando polimorfismo."""
    print(item)


def generar_reporte(items: list) -> str:
    """Genera reporte usando duck typing con to_dict()."""
    lineas = []
    for item in items:
        data = item.to_dict()
        partes = [f"{clave}: {valor}" for clave, valor in data.items()]
        lineas.append(" | ".join(partes))
    return "\n".join(lineas)
