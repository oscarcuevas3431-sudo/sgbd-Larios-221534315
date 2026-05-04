# Registro de prompts usados en el proyecto

> Nota: Este archivo debe adaptarse con tu fecha/hora real y con lo que realmente hayas modificado. No conviene mentir; conviene explicar qué cambiaste.

---

## Tarea 1.1 — Configuración del entorno y repositorio

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 22:30  
**Prompt enviado:**  
Estoy haciendo un proyecto en Python llamado Sistema de Gestión de Biblioteca Digital. Ayúdame solo a crear la estructura inicial del proyecto con carpetas modelos, servicios, utils, datos y tests. Dame comandos de terminal, .gitignore y explicación simple de cada carpeta.

**Respuesta recibida (resumen):**  
La IA propuso una estructura modular para separar modelos, servicios, utilidades, datos y pruebas.

**Código adoptado / modificado:**  
Usé la estructura sugerida, agregué archivos `__init__.py`, `README.md`, `.gitignore` y `requirements.txt`.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que separar carpetas ayuda a que el proyecto no sea un cochinero. La IA no sabe exactamente cómo quiere el profe el repo, así que comparé con el documento.

**Temas de la materia que aplica este prompt:**  
Entorno de desarrollo, Git, estructura de proyecto.

---

## Tarea 1.2 — Constantes y validadores

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 22:40  
**Prompt enviado:**  
Ayúdame con `utils/constantes.py` y `utils/validadores.py`. Necesito constantes en SCREAMING_SNAKE_CASE y funciones `validar_isbn13` y `validar_email` con type hints y docstrings.

**Respuesta recibida (resumen):**  
La IA explicó cómo crear constantes y validar datos con `if`, `return`, `and`, `or`, `not` e `is`.

**Código adoptado / modificado:**  
Adopté la validación de ISBN-13, pero limpié guiones y espacios antes de validar.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que ISBN-13 usa un dígito verificador. También reforcé que las constantes van en mayúsculas.

**Temas de la materia que aplica este prompt:**  
Variables, constantes, operadores, control de flujo, strings.

---

## Tarea 1.3 — Operadores y sentencias de control

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 22:50  
**Prompt enviado:**  
Necesito `calcular_multa(dias_retraso, tipo_usuario)` con reglas: alumno 5 pesos por día, profesor 2, admin 0, y si supera 30 días aumenta 20%. Dame versión con if/elif/else y match/case.

**Respuesta recibida (resumen):**  
La IA generó dos funciones para calcular multas y ejemplos de prueba.

**Código adoptado / modificado:**  
Agregué constantes para evitar números mágicos y validé tipos de usuario inválidos con `ValueError`.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que `match/case` sirve como alternativa moderna a muchos `elif`.

**Temas de la materia que aplica este prompt:**  
Operadores aritméticos, relacionales, lógicos, if/elif/else, match/case.

---

## Tarea 1.4 — Manejo de strings

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:00  
**Prompt enviado:**  
Ayúdame con funciones de strings: `normalizar_titulo`, `generar_slug`, `formatear_reporte_libro` y `buscar_en_texto`. Usa métodos como strip, split, join, lower, upper, replace, find y f-strings.

**Respuesta recibida (resumen):**  
La IA propuso funciones para limpiar títulos, generar slugs y buscar texto sin importar mayúsculas.

**Código adoptado / modificado:**  
Agregué `unicodedata` y expresiones regulares para limpiar acentos y caracteres especiales.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que limpiar texto antes de guardarlo evita errores raros después.

**Temas de la materia que aplica este prompt:**  
Strings, f-strings, métodos de cadena, formato de texto.

---

## Tarea 2.1 — Clase Libro

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:10  
**Prompt enviado:**  
Ayúdame a crear `modelos/libro.py` con clase `Libro`, atributos privados, properties, validación de ISBN, validación de año, `__str__`, `__repr__`, `__eq__`, `to_dict` y `from_dict`.

**Respuesta recibida (resumen):**  
La IA dio una clase `Libro` encapsulada con getters, setters y métodos especiales.

**Código adoptado / modificado:**  
Adapté la clase para heredar de `Entidad` y para permitir guardar/cargar desde JSON.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que `@property` permite controlar cambios en atributos privados.

**Temas de la materia que aplica este prompt:**  
Clases, objetos, encapsulamiento, métodos, abstracción.

---

## Tarea 2.2 — Clases abstractas

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:20  
**Prompt enviado:**  
Explícame cómo usar ABC para crear `Entidad` y `Usuario` abstractos. Entidad debe tener id, fecha_creacion, `__str__` y `to_dict`. Usuario debe tener `puede_pedir_prestado`.

**Respuesta recibida (resumen):**  
La IA explicó `ABC`, `abstractmethod`, `uuid4` y `datetime`.

**Código adoptado / modificado:**  
Implementé `Entidad` con UUID automático y `Usuario` como clase abstracta heredada.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que una clase abstracta funciona como molde y no debe instanciarse directamente.

**Temas de la materia que aplica este prompt:**  
Abstracción, clases abstractas, herencia.

---

## Tarea 2.3 — Herencia

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:30  
**Prompt enviado:**  
Necesito implementar herencia: `LibroDigital`, `LibroFisico`, `Alumno`, `Profesor` y `Administrador`. Cada clase debe tener atributos propios, validaciones, `__str__` y `to_dict`.

**Respuesta recibida (resumen):**  
La IA propuso subclases usando `super().__init__()` y validaciones propias.

**Código adoptado / modificado:**  
Separé libros y usuarios en archivos diferentes para mantener modularidad.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que `super()` llama al constructor de la clase padre y evita repetir código.

**Temas de la materia que aplica este prompt:**  
Herencia, encapsulamiento, métodos, polimorfismo.

---

## Tarea 2.4 — Polimorfismo y duck typing

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:40  
**Prompt enviado:**  
Ayúdame con `utils/display.py`. Necesito `mostrar_info(item)` que use `__str__` y `generar_reporte(items)` que use duck typing con `to_dict`.

**Respuesta recibida (resumen):**  
La IA explicó que el polimorfismo permite usar objetos distintos con una misma función.

**Código adoptado / modificado:**  
Implementé funciones simples para imprimir objetos y generar reportes de cualquier objeto con `to_dict`.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que duck typing significa: si se comporta como lo necesito, lo puedo usar sin preguntar su clase exacta.

**Temas de la materia que aplica este prompt:**  
Polimorfismo, duck typing, métodos.

---

## Tarea 2.5 — Protocolo Buscable y Catálogo

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-03 23:50  
**Prompt enviado:**  
Necesito `modelos/catalogo.py` con un Protocol `Buscable` y una clase `Catalogo` que maneje listas de libros, diccionario de usuarios y lista de préstamos. Debe buscar, prestar, devolver, reportar, guardar y cargar JSON.

**Respuesta recibida (resumen):**  
La IA generó una clase gestora con listas, diccionarios, list comprehensions y persistencia JSON.

**Código adoptado / modificado:**  
Agregué validaciones de disponibilidad, límite de préstamos y búsqueda por ISBN.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que `Protocol` define qué método debe tener una clase, aunque no herede directamente.

**Temas de la materia que aplica este prompt:**  
Protocolos, interfaces, list, dict, JSON, colecciones.

---

## Tarea 2.6 — Colecciones avanzadas

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-04 00:00  
**Prompt enviado:**  
Ayúdame con `gestor_cola.py`, `historial.py` y `estadisticas.py`. Necesito cola FIFO con deque, pila LIFO con lista y estadísticas con Counter y defaultdict.

**Respuesta recibida (resumen):**  
La IA explicó diferencias entre `list`, `deque`, `Counter` y `defaultdict`.

**Código adoptado / modificado:**  
Implementé clases y funciones separadas para no mezclar responsabilidades.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que una cola atiende primero al que llegó primero y una pila saca primero lo último que entró.

**Temas de la materia que aplica este prompt:**  
Listas, pilas, colas, diccionarios, deque, Counter, defaultdict.

---

## Tarea 2.7 — Integración con main.py

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-04 00:10  
**Prompt enviado:**  
Ayúdame con `main.py`. Necesito menú de consola con `while True`, `match/case`, opciones para agregar, buscar, registrar, prestar, devolver, ver cola, reportes y salir. También cargar JSON al iniciar y guardar al salir.

**Respuesta recibida (resumen):**  
La IA generó un menú conectado con el catálogo, manejo de errores y datos demo.

**Código adoptado / modificado:**  
Agregué `seed_data`, historial y cola de espera cuando un préstamo no se puede completar.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí cómo conectar todas las clases en un programa real de consola.

**Temas de la materia que aplica este prompt:**  
Integración, control de flujo, archivos, excepciones, OOP.

---

## Reflexión final

Este proyecto me ayudó a entender que la IA puede ayudar a programar, pero no debe usarse como botón mágico. Tuve que dividir el problema por partes: primero estructura, luego funciones básicas, después clases, herencia, polimorfismo, colecciones y finalmente integración. También aprendí que documentar prompts sirve para demostrar el proceso, no solo el resultado.


---

## Extra — Interfaz gráfica con tkinter

### Prompt #1
**LLM usada:** ChatGPT  
**Fecha/Hora:** 2026-05-04 00:30  
**Prompt enviado:**  
Quiero agregar una GUI sencilla a mi proyecto de biblioteca en Python usando tkinter. Debe reutilizar mi clase Catalogo y permitir agregar libro, buscar libro, registrar usuario, prestar, devolver, ver reporte y guardar datos. No quiero librerías externas.

**Respuesta recibida (resumen):**  
La IA propuso un archivo `gui.py` con una ventana principal, botones, una tabla Treeview y cuadros de diálogo.

**Código adoptado / modificado:**  
Se integró la GUI con las clases existentes para no duplicar la lógica del sistema. La interfaz llama a los métodos del catálogo.

**Lo que aprendí / Lo que la IA no entendió:**  
Aprendí que la GUI debe ser solo la capa visual; la lógica importante sigue en las clases. Esto evita mezclar botones con reglas de negocio.

**Temas de la materia que aplica este prompt:**  
OOP, modularidad, eventos, reutilización de código, manejo de errores.
