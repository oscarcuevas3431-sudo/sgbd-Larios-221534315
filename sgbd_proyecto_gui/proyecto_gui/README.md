# 1. Sistema de Gestión de Biblioteca Digital (Parte 2)

## 2. Descripción General
Esta aplicación es la segunda etapa evolutiva del Sistema de Gestión de Biblioteca Digital. Ha transicionado de una aplicación de consola a una robusta interfaz gráfica de escritorio (GUI) desarrollada bajo el patrón de arquitectura MVC. El proyecto implementa persistencia de datos avanzada (SQL y NoSQL), programación orientada a eventos, uso de delegados (callbacks) e hilos de ejecución (multithreading) para garantizar operaciones no bloqueantes.

## 3. Requisitos
- Python 3.10 o superior.
- Gestor de paquetes `pip`.
- Entorno local o servidor activo de MongoDB (puerto 27017 por defecto).

## 4. Instalación
1. Clona o descarga el repositorio en tu máquina local.
2. Abre una terminal en la carpeta raíz del proyecto.
3. Instala las dependencias requeridas ejecutando:
   ```bash
   pip install -r requirements.txt
   ```
*(Nota: La única dependencia externa requerida es `pymongo`. El resto de las bibliotecas como `tkinter`, `sqlite3` y `threading` son nativas de Python).*

## 5. Cómo ejecutar la aplicación
Desde la terminal, ubicado en la raíz del proyecto, ejecuta el siguiente comando:
```bash
python main.py
```
*(Nota: El archivo `main.py` original de consola se ha conservado, pero todo el código se portó para que ahora inicie la interfaz gráfica moderna automáticamente).*

## 6. Estructura de Carpetas
La arquitectura del proyecto fomenta el bajo acoplamiento y la alta cohesión:
- `ui/`: Contiene la capa de presentación, incluyendo la Ventana Principal (`main_window.py`).
- `controllers/`: Aloja la lógica de intermediación entre la vista y los datos (`libro_controller.py`, `usuario_controller.py`, etc.).
- `models/`: Definición de entidades de dominio mediante dataclasses (`libro.py`, `usuario.py`, `prestamo.py`, `evento.py`).
- `repositories/`: Capa de persistencia. Implementa el patrón Repositorio para SQLite y MongoDB.
- `threads/`: Lógica de tareas en segundo plano (`worker.py`).
- `data/`: Almacenamiento local para bases de datos (`biblioteca.db`) y archivos de fallback de logs.

## 7. Funcionalidades Implementadas
- **Módulo de Libros:** CRUD completo con tabla interactiva.
- **Módulo de Usuarios:** Registro y gestión de perfiles (Alumno, Profesor, Administrador).
- **Módulo de Préstamos:** Sistema transaccional para prestar y devolver libros, con validación de disponibilidad en tiempo real.
- **Módulo de Reportes:** Generación de estadísticas y respaldos asíncronos.
- **Delegación de Eventos:** Interfaz gráfica completamente desacoplada de la base de datos usando callbacks pasados a los controladores.

## 8. Eventos Implementados
Se implementó programación orientada a eventos usando Tkinter:
1. **Mouse (`<Double-1>`):** Carga datos a formularios al dar doble clic en una tabla.
2. **Teclado (`<Return>`):** Búsqueda rápida al presionar Enter.
3. **Tiempo (`after`):** Reloj de sistema que se actualiza cada segundo.
4. **Carga (`__init__`):** Lectura automática de base de datos al abrir la app.
5. **Foco (`<FocusIn>` / `<FocusOut>`):** Ayuda dinámica en la barra de estado inferior.
6. **Cierre (`WM_DELETE_WINDOW`):** Respaldo automático de base de datos al salir de la aplicación.
7. **GUI (`command=`):** Interacciones estándar con botones.
8. **Personalizado (`<<LibroGuardado>>`, etc.):** Sincronización cruzada automática entre pestañas sin reiniciar la aplicación.

## 9. Uso de SQL (SQLite)
Se utiliza una base de datos relacional (SQLite) alojada en `data/biblioteca.db` para almacenar de forma persistente y segura la información de Libros, Usuarios y Préstamos. Se aplican **Transacciones (ACID)** y consultas parametrizadas para evitar inyecciones SQL y garantizar que la disponibilidad de los libros cambie atómicamente al registrar préstamos.

## 10. Uso de MongoDB
Siguiendo un modelo de **Persistencia Políglota**, se integró MongoDB como bitácora de eventos del sistema (auditoría). Guarda metadatos de formato flexible cada vez que se agrega, edita o elimina información. Posee un sistema de contingencia (Fallback) que redirige los logs a un archivo de texto si el servidor de Mongo se apaga, evitando la caída del sistema.

## 11. JSON / XML
Se implementó el servicio `ExportService` que toma los objetos del catálogo y los serializa a archivos estructurados. 
- **JSON:** Usa el módulo nativo `json` de Python.
- **XML:** Usa `xml.etree.ElementTree` complementado con `minidom` para generar una estructura anidada y legible por humanos (pretty print).
Ambas exportaciones abren un explorador de archivos nativo para que el usuario elija la ruta de guardado, corriendo la tarea asíncronamente en segundo plano.

## 12. Hilos (Multithreading)
Se usa el módulo nativo `threading` para evitar que la interfaz gráfica se congele (error *Application Not Responding*) durante operaciones pesadas. Las exportaciones profundas y la generación de reportes ocurren en la clase `BackgroundWorker` (hilos en segundo plano) retornando notificaciones seguras al Main Thread de Tkinter mediante `self.after()`.

## 13. Gráficas
Integración con la biblioteca externa `matplotlib` para la visualización de datos estadísticos. Se utiliza `FigureCanvasTkAgg` para incrustar figuras directamente dentro del ciclo de vida de Tkinter. Genera:
1. Gráfica de pastel de disponibilidad (libros disponibles vs prestados).
2. Gráfica de barras contabilizando el volumen de los distintos tipos de usuarios registrados en el sistema.

## 14. Integrantes del Equipo
[Escribe tu nombre aquí] 

## 15. Evidencia de uso de IA
Durante el desarrollo se ha documentado paso a paso la interacción con la inteligencia artificial, justificando las decisiones arquitectónicas de persistencia, eventos e hilos. El registro de prompts y análisis puede consultarse en el archivo adjunto `prompts_log.md` y `arquitectura.md`.
