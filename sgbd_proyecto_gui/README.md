# Sistema de Gestión de Biblioteca Digital

Proyecto de consola en Python para administrar libros, usuarios y préstamos.

## Requisitos
- Python 3.10 o superior
- VS Code o Antigravity
- Git

## Cómo ejecutar
Desde la carpeta raíz del proyecto:

```bash
python main.py
```

## Estructura
- `main.py`: menú principal del sistema.
- `modelos/`: clases principales como Libro, Usuario, Prestamo y Catalogo.
- `servicios/`: lógica auxiliar como multas, cola, historial y estadísticas.
- `utils/`: validadores, constantes y formato de texto.
- `datos/`: archivos JSON generados automáticamente.
- `tests/`: pruebas opcionales.

## Uso de IA
El archivo `prompts_log.md` contiene el registro de prompts usados como apoyo para construir el proyecto.


## Cómo ejecutar con GUI

```bash
python gui.py
```

Esta versión usa `tkinter`, que viene incluido con Python. No necesita instalar librerías externas.
