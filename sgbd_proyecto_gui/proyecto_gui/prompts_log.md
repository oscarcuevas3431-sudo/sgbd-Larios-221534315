# prompts_log.md

## Bitácora de uso de IA - Práctica Examen 2  
**Proyecto:** Sistema de Gestión de Biblioteca Digital  
**Herramienta usada:** Antigravity / Agent Code LLM  
**Repositorio:** sgbd_Larios-221534315  

> Nota: Esta bitácora registra el apoyo técnico usado durante el desarrollo. El equipo revisó, probó y ajustó el código antes de integrarlo al proyecto.

---

## Prompt 1: Revisión inicial del proyecto

**Tarea:** 3.1 Continuidad del repositorio y estructura del proyecto  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Estoy trabajando en el repositorio del Sistema de Gestión de Biblioteca Digital. Necesito revisar la estructura actual del proyecto y detectar qué archivos pueden reutilizarse para la nueva versión con interfaz gráfica, eventos, SQL, MongoDB, JSON/XML, hilos y reportes. No escribas código todavía; primero dame un diagnóstico y una propuesta de organización.

**Respuesta resumida:**  
La herramienta sugirió separar el proyecto por capas: interfaz, controladores, modelos, repositorios, servicios, eventos e hilos. También recomendó conservar los archivos existentes y agregar documentación técnica.

**Código adoptado/modificado:**  
No se integró código en esta etapa. Se tomó como base la propuesta de estructura.

**Qué corrigió el equipo:**  
El equipo decidió mantener el proyecto anterior y crear una versión organizada para GUI sin borrar los avances previos.

**Tema del curso implementado:**  
Organización modular del proyecto, control de versiones y continuidad del repositorio.

---

## Prompt 2: Creación de estructura modular

**Tarea:** 3.1 Continuidad del repositorio y estructura del proyecto  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Crea la estructura modular necesaria para la nueva versión del sistema. Debe incluir carpetas para ui, controllers, models, repositories, services, events, threads, data y tests. No borres archivos existentes. Si alguna carpeta queda vacía, agrega un archivo .gitkeep.

**Respuesta resumida:**  
Se propuso una estructura de carpetas compatible con el documento de la práctica y se explicó la función de cada módulo.

**Código adoptado/modificado:**  
Se crearon carpetas para separar interfaz, lógica, modelos, acceso a datos, servicios, eventos y tareas en segundo plano.

**Qué corrigió el equipo:**  
Se eliminaron carpetas duplicadas y se unificaron nombres para evitar confusiones entre carpetas en español e inglés.

**Tema del curso implementado:**  
Arquitectura de software, modularidad y mantenimiento del código.

---

## Prompt 3: Interfaz gráfica principal

**Tarea:** 3.2 GUI y fundamentos de programación orientada a eventos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Necesito crear la interfaz gráfica principal usando Tkinter y ttk. La aplicación debe tener una ventana principal con secciones para libros, usuarios, préstamos y reportes. En libros debe existir formulario, botones CRUD y una tabla Treeview. Separa la interfaz de la lógica y usa clases, type hints y docstrings.

**Respuesta resumida:**  
Se generó una ventana principal con pestañas y componentes básicos para administrar libros, usuarios, préstamos y reportes.

**Código adoptado/modificado:**  
Se integró la clase principal de la interfaz en la carpeta ui y se conectó con main.py.

**Qué corrigió el equipo:**  
Se revisaron nombres de widgets, distribución visual y separación entre la ventana y la lógica de negocio.

**Tema del curso implementado:**  
Diseño de interfaces gráficas y programación orientada a eventos.

---

## Prompt 4: Modelos del sistema

**Tarea:** 4.4 CRUD básico con Python, base de datos y eventos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Crea o adapta los modelos del sistema en la carpeta models. Necesito clases para Libro, Usuario, Prestamo y EventoSistema, usando type hints y docstrings. No coloques lógica de interfaz dentro de los modelos.

**Respuesta resumida:**  
Se propusieron clases para representar los datos principales del sistema y separar la lógica del dominio de la interfaz gráfica.

**Código adoptado/modificado:**  
Se crearon modelos para libros, usuarios, préstamos y eventos del sistema.

**Qué corrigió el equipo:**  
Se revisaron atributos, nombres y tipos de datos para que coincidieran con los formularios y la base de datos.

**Tema del curso implementado:**  
Programación orientada a objetos, clases, atributos y separación de responsabilidades.

---

## Prompt 5: Repositorio SQL

**Tarea:** 4.1 Base de datos relacional SQL  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Implementa persistencia SQL usando SQLite. Crea tablas para libros, usuarios y préstamos. Usa consultas parametrizadas y agrega CRUD completo para libros. La base debe guardarse en data/biblioteca.db y el código debe estar en repositories.

**Respuesta resumida:**  
Se generó un repositorio SQL con funciones para inicializar la base de datos, crear tablas y realizar operaciones básicas.

**Código adoptado/modificado:**  
Se integró el archivo sql_repository.py con conexión SQLite y métodos CRUD.

**Qué corrigió el equipo:**  
Se revisaron las consultas para evitar concatenación insegura y se ajustaron rutas para que funcionaran desde main.py.

**Tema del curso implementado:**  
Bases de datos relacionales, consultas parametrizadas y persistencia de datos.

---

## Prompt 6: Conexión del CRUD con la GUI

**Tarea:** 4.4 CRUD con GUI y eventos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Conecta la pestaña de libros de la GUI con SQLite. Al iniciar la app debe cargar libros en la tabla. Los botones Agregar, Editar, Eliminar, Limpiar y Buscar deben funcionar desde la interfaz. Usa try/except y messagebox para mostrar mensajes claros.

**Respuesta resumida:**  
Se conectaron los botones de la interfaz con las funciones del repositorio SQL y se actualizó la tabla después de cada operación.

**Código adoptado/modificado:**  
Se modificaron controladores y handlers de la pestaña de libros.

**Qué corrigió el equipo:**  
Se corrigieron validaciones de campos vacíos y actualización de la tabla después de agregar o editar.

**Tema del curso implementado:**  
CRUD, eventos GUI, validaciones y manejo de errores.

---

## Prompt 7: Eventos obligatorios

**Tarea:** 3.4 Eventos obligatorios  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Implementa eventos obligatorios en la GUI: mouse, teclado, temporizador, carga, foco, cierre de ventana, botones GUI y un evento personalizado llamado datos_actualizados. Documenta el origen, handler y efecto de cada evento.

**Respuesta resumida:**  
Se añadieron eventos de interacción del usuario, eventos automáticos y un evento personalizado para actualizar información del sistema.

**Código adoptado/modificado:**  
Se agregaron bindings de teclado y mouse, actualización de reloj con after(), evento de cierre seguro y evento personalizado.

**Qué corrigió el equipo:**  
Se ajustó el cierre de la ventana para cancelar correctamente tareas programadas con after() y evitar errores al cerrar la app.

**Tema del curso implementado:**  
Programación orientada a eventos, handlers, eventos personalizados y ciclo de vida de la GUI.

---

## Prompt 8: Callbacks y lambdas

**Tarea:** 3.3 Delegados, callbacks y métodos anónimos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Refactoriza la GUI para demostrar callbacks y métodos anónimos. Necesito al menos tres callbacks claros y tres lambdas justificadas para acciones simples. No uses lambdas para lógica larga.

**Respuesta resumida:**  
Se identificaron funciones callback para botones y selección de tabla. También se agregaron lambdas para operaciones simples de interfaz.

**Código adoptado/modificado:**  
Se ajustaron comandos de botones, bindings y handlers en la interfaz.

**Qué corrigió el equipo:**  
Se evitó poner lógica extensa dentro de lambdas y se movieron acciones importantes a métodos separados.

**Tema del curso implementado:**  
Callbacks, métodos anónimos y separación entre vista y controlador.

---

## Prompt 9: Usuarios y préstamos

**Tarea:** 4.4 CRUD básico con Python, BD y eventos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Implementa las secciones de usuarios y préstamos. Usuarios debe tener formulario, tabla y botones CRUD. Préstamos debe permitir seleccionar usuario y libro, registrar préstamo, registrar devolución y actualizar disponibilidad del libro.

**Respuesta resumida:**  
Se ampliaron los módulos de usuarios y préstamos, conectándolos con SQLite y con la interfaz gráfica.

**Código adoptado/modificado:**  
Se agregaron métodos SQL para usuarios y préstamos, además de formularios y tablas en la GUI.

**Qué corrigió el equipo:**  
Se verificó que un libro prestado cambiara su disponibilidad y que al devolverlo volviera a estar disponible.

**Tema del curso implementado:**  
Relaciones entre datos, validaciones de negocio y actualización de interfaz por eventos.

---

## Prompt 10: MongoDB y bitácora

**Tarea:** 4.2 Base de datos no relacional MongoDB  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Agrega MongoDB para registrar eventos del sistema. Debe registrar acciones como app_iniciada, libro_creado, usuario_creado, prestamo_creado, exportaciones y app_cerrada. Si MongoDB no está disponible, la app debe usar un respaldo local y seguir funcionando.

**Respuesta resumida:**  
Se propuso guardar la bitácora en MongoDB y usar un archivo local como respaldo cuando no hubiera conexión.

**Código adoptado/modificado:**  
Se agregó un repositorio para eventos y un mecanismo de fallback local.

**Qué corrigió el equipo:**  
Se modificó el manejo de conexión para que MongoDB fuera opcional y no detuviera el funcionamiento de la aplicación.

**Tema del curso implementado:**  
Persistencia no relacional, bitácora, tolerancia a fallos y manejo de excepciones.

---

## Prompt 11: JSON y XML

**Tarea:** 4.3 Serialización en JSON y XML  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Implementa importación y exportación de libros en JSON y XML desde la interfaz. Crea un servicio de serialización, valida estructura básica y maneja errores de archivo o formato inválido.

**Respuesta resumida:**  
Se crearon funciones para exportar e importar datos en JSON y XML y se conectaron a botones de la GUI.

**Código adoptado/modificado:**  
Se agregó serialization_service.py y botones para importar/exportar archivos.

**Qué corrigió el equipo:**  
Se revisaron rutas de guardado, validación de datos y mensajes de error cuando el archivo no era válido.

**Tema del curso implementado:**  
Manejo de archivos, serialización, JSON, XML y validación de estructura.

---

## Prompt 12: Hilos y workers

**Tarea:** 3.6 Hilos y tareas en segundo plano  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Implementa hilos para que las tareas largas no congelen la GUI. Necesito mínimo dos operaciones: generación de reportes y respaldo de datos. La interfaz debe actualizarse de forma segura usando after().

**Respuesta resumida:**  
Se agregó un worker para ejecutar tareas en segundo plano y actualizar la interfaz al terminar.

**Código adoptado/modificado:**  
Se creó worker.py y se conectaron procesos de reportes o respaldos con la interfaz.

**Qué corrigió el equipo:**  
Se verificó que la ventana siguiera respondiendo mientras se ejecutaban tareas largas.

**Tema del curso implementado:**  
Concurrencia, hilos, workers y actualización segura de GUI.

---

## Prompt 13: Reportes y gráficas

**Tarea:** 4.5 Tablas y gráficos de datos  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Crea el panel de reportes con una tabla Treeview y dos gráficas usando matplotlib. Las gráficas deben mostrar libros por género y préstamos por tipo de usuario usando datos reales de SQLite.

**Respuesta resumida:**  
Se generó un panel de reportes con tabla y gráficas alimentadas desde la base de datos.

**Código adoptado/modificado:**  
Se agregaron consultas estadísticas y visualización con matplotlib.

**Qué corrigió el equipo:**  
Se manejaron casos sin datos y se actualizó el reporte después de operaciones importantes.

**Tema del curso implementado:**  
Tablas, gráficas, estadísticas y consulta de datos.

---

## Prompt 14: Datos demo

**Tarea:** 4.6 Integración final y demostración del flujo completo  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Agrega datos demo con una función seed_data(). Debe insertar libros, usuarios y préstamos solo si la base está vacía, para facilitar la revisión del profesor. No debe duplicar datos.

**Respuesta resumida:**  
Se agregó una función de carga inicial de datos para probar el sistema rápidamente.

**Código adoptado/modificado:**  
Se integró seed_data() y validación para evitar duplicados.

**Qué corrigió el equipo:**  
Se revisó que la función no repitiera registros al ejecutar varias veces el programa.

**Tema del curso implementado:**  
Datos de prueba, inicialización del sistema e integración de módulos.

---

## Prompt 15: Documentación técnica

**Tarea:** 7. Entregables y estructura del repositorio  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Actualiza README.md y arquitectura.md. Incluye descripción del proyecto, instalación, ejecución, estructura de carpetas, eventos implementados, SQL, MongoDB, JSON/XML, hilos, gráficas y flujo general del sistema.

**Respuesta resumida:**  
Se generó documentación para explicar el funcionamiento general del proyecto y su arquitectura.

**Código adoptado/modificado:**  
Se modificaron README.md y arquitectura.md.

**Qué corrigió el equipo:**  
Se revisó que la documentación coincidiera con lo realmente implementado y no incluyera funciones inexistentes.

**Tema del curso implementado:**  
Documentación técnica, trazabilidad del proyecto y preparación de entrega.

---

## Prompt 16: Revisión contra rúbrica

**Tarea:** 6. Rúbrica de evaluación  
**LLM usada:** Antigravity Agent  
**Integrante:** [Nombre del integrante]  
**Fecha/hora:** [Fecha y hora real]  

**Prompt enviado:**  
Revisa el proyecto completo contra la rúbrica de la práctica-examen parte 2. Verifica estructura, GUI, callbacks, eventos, excepciones, hilos, archivos, SQL, Mongo, JSON/XML, CRUD, tablas, gráficas e integración final. No modifiques código todavía; primero dame diagnóstico.

**Respuesta resumida:**  
Se generó una lista de puntos cumplidos y pendientes para revisar antes de la entrega.

**Código adoptado/modificado:**  
No se modificó código en esta revisión inicial.

**Qué corrigió el equipo:**  
El equipo revisó los puntos pendientes y aplicó correcciones manuales antes de subir el proyecto.

**Tema del curso implementado:**  
Validación, pruebas manuales, revisión de rúbrica y control de calidad.

---

## Checklist final de revisión

- [ ] La aplicación abre desde `main.py`.
- [ ] La GUI funciona sin depender de consola.
- [ ] El CRUD de libros funciona.
- [ ] El CRUD de usuarios funciona.
- [ ] El módulo de préstamos actualiza disponibilidad.
- [ ] Hay eventos de mouse, teclado, tiempo, carga, foco, cierre, GUI y personalizado.
- [ ] Existen callbacks y lambdas documentadas.
- [ ] SQLite guarda libros, usuarios y préstamos.
- [ ] MongoDB registra eventos o usa fallback local.
- [ ] JSON y XML exportan/importan datos.
- [ ] Hay al menos dos operaciones con hilos.
- [ ] Hay tabla de reportes y dos gráficas.
- [ ] README.md está actualizado.
- [ ] arquitectura.md explica la estructura y eventos.
- [ ] requirements.txt contiene dependencias externas.
- [ ] El repositorio tiene commits significativos.
