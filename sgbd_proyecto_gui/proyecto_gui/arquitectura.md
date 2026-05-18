# Arquitectura del Sistema de Gestión de Biblioteca Digital (Parte 2)

## 1. Arquitectura General del Sistema
El sistema emplea un patrón de arquitectura **Modelo-Vista-Controlador (MVC)**, complementado con el **Patrón Repositorio** para la persistencia de datos. Esta arquitectura promueve un bajo acoplamiento, permitiendo que la interfaz gráfica interactúe con los datos de forma abstracta sin conocer los detalles intrínsecos de las consultas SQL o llamadas a bases de datos documentales.

## 2. Separación por Capas
La modularidad del sistema se refleja en la siguiente estructura de directorios:
- **`ui/` (Capa de Presentación):** Contiene la lógica visual (Tkinter). Es una capa pasiva; dibuja elementos y captura interacciones.
- **`controllers/` (Capa Intermediaria):** Reciben las peticiones de la UI, aplican reglas de negocio y actúan como puente hacia la persistencia.
- **`models/` (Entidades de Dominio):** Representan los objetos del negocio mediante constructores y `dataclasses` (ej. `Libro`, `Usuario`, `Prestamo`, `EventoSistema`).
- **`repositories/` (Capa de Acceso a Datos):** Centraliza y aísla la lógica de conexión y comandos a las bases de datos (SQLite, MongoDB).
- **`services/` (Lógica Auxiliar):** Destinado a algoritmos complejos de procesamiento.
- **`events/`:** Gestores de enrutamiento asíncrono y notificaciones del sistema.
- **`threads/`:** Define rutinas (Workers) para ejecutar operaciones concurrentes, protegiendo el hilo principal de la GUI.
- **`data/`:** Contenedor local para bases de datos relacionales y registros planos (fallback logs).

## 3. Flujo de Datos
1. **Acción:** El usuario interactúa con un control en la `ui` (ej. clic en "Prestar").
2. **Delegación:** La UI invoca un *callback* (método delegado) inyectado por el `controller`.
3. **Validación:** El controlador recibe y limpia los datos.
4. **Persistencia:** El controlador solicita al `repository` ejecutar la transacción en SQLite.
5. **Auditoría:** En paralelo, se invoca al repositorio de MongoDB para escribir en bitácora el evento acontecido.
6. **Sincronización:** Si hay éxito, la UI detona un evento virtual local que recarga automáticamente las tablas dependientes, reflejando el nuevo estado.

## 4. Mapa de Eventos
La interfaz desarrollada en Tkinter se rige por la programación orientada a eventos. A continuación, el mapa de interacciones principales:

| Tipo de Evento | Widget Origen | Handler (Método) | Efecto Funcional |
| :--- | :--- | :--- | :--- |
| **Mouse (`<Double-1>`)** | Tablas `ttk.Treeview` | `_on_libro_doble_clic` | Identifica la fila, consulta la base de datos y carga los datos en el formulario de edición. |
| **Teclado (`<Return>`)** | `ttk.Entry` (Búsqueda) | `_buscar_libro` | Lanza una consulta de filtrado al presionar la tecla Enter en la barra de búsqueda. |
| **Tiempo (`after`)** | Ciclo `mainloop` Tkinter | `_actualizar_reloj` | Invocación recursiva cada 1,000 ms para actualizar la hora del sistema en tiempo real. |
| **Carga / Foco** | Inicio de Pestaña | `_setup_tab_libros` | Extrae el catálogo inicial desde SQLite y lo vierte en la interfaz al arrancar. |
| **Destrucción (`WM_DELETE_WINDOW`)**| Barra de Título | `_on_cerrar_ventana` | Intercepta el cierre de la ventana para ejecutar copias de seguridad antes de matar el proceso. |
| **GUI Botones (`command=`)** | `ttk.Button` | Acciones CRUD | Transmite los datos contenidos en las variables dinámicas de Tkinter hacia la lógica de negocio. |
| **Evento de Programador (Virtual)** | Sistema interno | `<<PrestamoGuardado>>` | Eventos diseñados a medida. Si cambia un préstamo, fuerza a la tabla "Libros" a actualizar su columna de disponibilidad. |

## 5. Callbacks y Lambdas Usados
La aplicación aplica paradigmas de programación funcional en la UI:
- **Callbacks (Delegados):** La interfaz ignora a los controladores. Durante la construcción de la ventana, se mapean referencias directas a memoria (ej. `self.cb_guardar_libro = self.libro_controller.agregar_libro`). Al accionar un botón, la UI solo ejecuta su callback, lo que mantiene el desacoplamiento estricto.
- **Funciones Anónimas (`lambda`):** Utilizadas ampliamente para dos fines:
  1. Diferir ejecución: En `command=lambda: self._limpiar_formulario()`, evita que la función se dispare durante el renderizado.
  2. Adaptadores de eventos: En `bind("<Return>", lambda e: self._buscar_libro())`, absorbe el argumento inyectado automáticamente por Tkinter que de lo contrario causaría un error de firma.

## 6. Persistencia Políglota: SQL vs MongoDB
El proyecto maximiza el rendimiento utilizando la herramienta adecuada para cada paradigma de datos:
- **SQLite (Base de Datos Relacional):**
  - Almacena la médula transaccional del negocio (Libros, Usuarios, Préstamos).
  - **Justificación:** Otorga cumplimiento **ACID**. Por ejemplo, el registro de un préstamo exige insertar el registro y cambiar la disponibilidad del libro como una única operación atómica; si algo falla, SQLite aplica un *rollback*, previniendo inconsistencias e huerfanos referenciales.
- **MongoDB (Base de Datos NoSQL):**
  - Ejerce como bitácora profunda y auditoría.
  - **Justificación:** Los sistemas de logs sufren escrituras constantes y exigen flexibilidad de metadatos (schema-less). Mongo asimila los eventos velozmente en formato JSON. Como contingencia, el módulo detecta si el servidor está inactivo y redirige la auditoría a texto plano sin alertar al usuario.

## 7. Manejo de JSON / XML
La arquitectura cuenta con el módulo `services/export_service.py` dedicado a la exportación de catálogos masivos. Este módulo recibe las listas de objetos `Libro` y las transforma de manera agnóstica a la UI.
Para la conversión se priorizan librerías estándar nativas (`json` y `xml.etree.ElementTree`) evitando dependencias de terceros. La ejecución se acopla a la arquitectura asíncrona mediante hilos para asegurar que la exportación profunda de grandes volúmenes de datos no ralentice al cliente final.

## 8. Tareas en Segundo Plano (Hilos Implementados)
Se recurre al módulo nativo `threading` orquestado por la clase `BackgroundWorker` (`threads/worker.py`).
- **Problema:** Tkinter opera bajo un hilo maestro (*Main Thread*). Un cálculo denso (ej. generar un informe) monopoliza este hilo, congelando el pintado de la interfaz y causando el error *Application Not Responding (ANR)*.
- **Solución:** Tareas pesadas como las "Estadísticas" y "Respaldos Profundos" se bifurcan hacia un hilo secundario asíncrono.
- **Manejo Seguro:** Como las GUIs no son *thread-safe*, el hilo trabajador no altera la pantalla, sino que inyecta sus resultados a la cola de mensajes del ciclo principal valiédose del despachador `self.after(0, ...)`.

## 9. Visualización de Datos (Matplotlib)
Para cumplir con el análisis estadístico del sistema, se integró la biblioteca `matplotlib` de manera embebida.
- En lugar de generar imágenes estáticas o lanzar ventanas externas desvinculadas de la app, se utilizó `FigureCanvasTkAgg`, una clase adaptadora que convierte las parcelas de Matplotlib (`plt.subplots`) en un *Widget* nativo de Tkinter, permitiendo mostrar el *pie chart* de disponibilidad y el *bar chart* de tipos de usuario dentro de una ventana controlada (`Toplevel`).

## 10. Manejo de Excepciones
Toda la ruta de ejecución cuenta con barreras de control de errores. Las capas inferiores (Repositories, Models) atrapan problemas de conexión o validación de reglas de negocio y arrojan excepciones estándar de Python (`ValueError`, `Exception`).
La capa de presentación (UI) envuelve todos sus despachos en bloques `try/except`. En vez de quebrar el software imprimiendo *tracebacks* terminales, traduce la excepción a cajas de diálogo amistosas informando al usuario (ej. `messagebox.showerror`).

## 10. Explicación de Ejecución
El proyecto es portátil e inicia su ciclo vital al ejecutar `python main.py` desde la raíz.
1. Python ensambla la estructura MVC e inicializa la raíz visual de Tkinter `tk.Tk()`.
2. Durante el constructor, se invocan a los repositorios locales para inflar las tablas con la información preexistente.
3. El programa entra en un estado inerte e infinito invocado por `mainloop()`. Aquí, el sistema deja de consumir ciclos pesados de CPU y se dedica únicamente a escuchar los dispositivos de entrada (mouse, teclado) esperando que los eventos (descritos en la tabla superior) despierten y despachen fragmentos de código específicos.
