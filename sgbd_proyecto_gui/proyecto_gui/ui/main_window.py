"""Módulo de la ventana principal de la interfaz gráfica."""

import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.libro_controller import LibroController
from controllers.usuario_controller import UsuarioController
from controllers.prestamo_controller import PrestamoController

from repositories.mongo_repository import MongoRepository
from models.evento import EventoSistema
from threads.worker import BackgroundWorker
from services.export_service import ExportService

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False


class MainWindow(tk.Tk):
    """Ventana principal del Sistema de Gestión de Biblioteca Digital."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de Gestión de Biblioteca Digital")
        self.geometry("900x700")
        self.minsize(900, 700)

        # Controladores y Repositorios Especiales
        self.libro_controller = LibroController()
        self.usuario_controller = UsuarioController()
        self.prestamo_controller = PrestamoController()
        self.mongo_logger = MongoRepository()

        # Selección de estado
        self.libro_id_seleccionado = None
        self.usuario_id_seleccionado = None
        self.prestamo_id_seleccionado = None

        # Diccionarios para mapear nombres de combobox a IDs
        self.map_usuarios_combo = {}
        self.map_libros_combo = {}

        # Callbacks (Delegados)
        self.cb_guardar_libro = self.libro_controller.agregar_libro
        self.cb_eliminar_libro = self.libro_controller.eliminar_libro
        self.cb_seleccionar_libro = self.libro_controller.obtener_por_id

        self._setup_ui()
        self._setup_eventos_globales()
        
        # Registrar evento de inicio en bitácora MongoDB
        self._log_evento("app_iniciada", "La aplicación GUI ha sido iniciada.", "Sistema")

    def _log_evento(self, tipo_evento: str, descripcion: str, modulo: str) -> None:
        """Función auxiliar para construir y registrar un evento en MongoDB."""
        evento = EventoSistema(tipo_evento=tipo_evento, descripcion=descripcion, modulo=modulo)
        self.mongo_logger.registrar_evento(evento)

    def _setup_ui(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_reloj = ttk.Label(frame_top, text="Hora: --:--:--", font=("Helvetica", 10, "bold"))
        self.lbl_reloj.pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.tab_reportes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_libros, text="Libros")
        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_prestamos, text="Préstamos")
        self.notebook.add(self.tab_reportes, text="Reportes")

        self._setup_tab_libros()
        self._setup_tab_usuarios()
        self._setup_tab_prestamos()
        self._setup_tab_reportes()

        self.lbl_estado = ttk.Label(self, text="Listo.", relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_eventos_globales(self) -> None:
        self._actualizar_reloj()
        self.protocol("WM_DELETE_WINDOW", self._on_cerrar_ventana)
        
        # Sincronización cruzada: Si cambia un modelo, se actualizan las vistas dependientes
        self.bind("<<LibroGuardado>>", lambda e: self._on_datos_actualizados())
        self.bind("<<UsuarioGuardado>>", lambda e: self._on_datos_actualizados())
        self.bind("<<PrestamoGuardado>>", lambda e: self._on_datos_actualizados())

    def _on_datos_actualizados(self) -> None:
        """Refresca todos los componentes cuando hay un cambio en la BD."""
        self._cargar_tabla_libros()
        self._cargar_tabla_usuarios()
        self._cargar_tabla_prestamos()
        self._cargar_comboboxes_prestamos()
        self.lbl_estado.config(text="Datos sincronizados.")

    # ==========================
    # PESTAÑA: LIBROS
    # ==========================
    def _setup_tab_libros(self) -> None:
        frame_form = ttk.LabelFrame(self.tab_libros, text="Datos del Libro", padding=10)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_isbn = tk.StringVar()
        self.var_anio = tk.StringVar()
        self.var_genero = tk.StringVar()
        self.var_disponible = tk.StringVar(value="Sí")

        ttk.Label(frame_form, text="Título:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_titulo, width=30).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_form, text="Autor:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_autor, width=30).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(frame_form, text="ISBN:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_isbn, width=30).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame_form, text="Año:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_anio, width=30).grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(frame_form, text="Género:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_genero, width=30).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(frame_form, text="Disponibilidad:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(frame_form, textvariable=self.var_disponible, values=["Sí", "No"], state="readonly", width=27).grid(row=2, column=3, padx=5, pady=5)

        frame_botones = ttk.Frame(self.tab_libros)
        frame_botones.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_botones, text="Agregar", command=self._agregar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Editar", command=self._editar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=lambda: self._limpiar_formulario_libros()).pack(side=tk.LEFT, padx=5)
        
        self.var_busqueda = tk.StringVar()
        ttk.Button(frame_botones, text="Buscar", command=self._buscar_libro).pack(side=tk.RIGHT, padx=5)
        entry_busqueda = ttk.Entry(frame_botones, textvariable=self.var_busqueda, width=20)
        entry_busqueda.pack(side=tk.RIGHT, padx=5)
        ttk.Label(frame_botones, text="Buscar:").pack(side=tk.RIGHT)
        entry_busqueda.bind("<Return>", lambda e: self._buscar_libro())

        frame_tabla = ttk.Frame(self.tab_libros)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("titulo", "autor", "isbn", "anio", "genero", "disponible")
        self.tabla_libros = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_libros.heading(col, text=col.capitalize())
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_libros.yview)
        self.tabla_libros.configure(yscroll=scrollbar.set)
        self.tabla_libros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla_libros.bind("<Double-1>", self._on_libro_doble_clic)
        self._cargar_tabla_libros()

    # ==========================
    # PESTAÑA: USUARIOS
    # ==========================
    def _setup_tab_usuarios(self) -> None:
        frame_form = ttk.LabelFrame(self.tab_usuarios, text="Datos del Usuario", padding=10)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        self.var_usuario_nombre = tk.StringVar()
        self.var_usuario_email = tk.StringVar()
        self.var_usuario_tipo = tk.StringVar()

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_usuario_nombre, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Email:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.var_usuario_email, width=30).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Tipo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(
            frame_form, textvariable=self.var_usuario_tipo, 
            values=["Alumno", "Profesor", "Administrador"], state="readonly", width=27
        ).grid(row=1, column=1, padx=5, pady=5)

        frame_botones = ttk.Frame(self.tab_usuarios)
        frame_botones.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_botones, text="Agregar", command=self._agregar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Editar", command=self._editar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=lambda: self._limpiar_formulario_usuarios()).pack(side=tk.LEFT, padx=5)

        frame_tabla = ttk.Frame(self.tab_usuarios)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=("nombre", "email", "tipo"), show="headings")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("email", text="Email")
        self.tabla_usuarios.heading("tipo", text="Tipo")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscroll=scrollbar.set)
        self.tabla_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla_usuarios.bind("<Double-1>", self._on_usuario_doble_clic)
        self._cargar_tabla_usuarios()

    # ==========================
    # PESTAÑA: PRÉSTAMOS
    # ==========================
    def _setup_tab_prestamos(self) -> None:
        frame_form = ttk.LabelFrame(self.tab_prestamos, text="Registrar Nuevo Préstamo", padding=10)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        self.var_prestamo_usuario = tk.StringVar()
        self.var_prestamo_libro = tk.StringVar()

        ttk.Label(frame_form, text="Usuario:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_prestamo_usuario = ttk.Combobox(frame_form, textvariable=self.var_prestamo_usuario, state="readonly", width=50)
        self.combo_prestamo_usuario.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Libro (Disponibles):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_prestamo_libro = ttk.Combobox(frame_form, textvariable=self.var_prestamo_libro, state="readonly", width=50)
        self.combo_prestamo_libro.grid(row=1, column=1, padx=5, pady=5)

        frame_botones = ttk.Frame(self.tab_prestamos)
        frame_botones.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_botones, text="Registrar Préstamo", command=self._prestar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Registrar Devolución (Seleccionar de tabla)", command=self._devolver_libro).pack(side=tk.LEFT, padx=5)

        frame_tabla = ttk.Frame(self.tab_prestamos)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tabla_prestamos = ttk.Treeview(frame_tabla, columns=("id", "libro", "usuario", "fecha"), show="headings")
        self.tabla_prestamos.heading("id", text="ID")
        self.tabla_prestamos.heading("libro", text="Libro")
        self.tabla_prestamos.heading("usuario", text="Usuario")
        self.tabla_prestamos.heading("fecha", text="Fecha de Préstamo")
        
        self.tabla_prestamos.column("id", width=50)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_prestamos.yview)
        self.tabla_prestamos.configure(yscroll=scrollbar.set)
        self.tabla_prestamos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tabla_prestamos.bind("<Double-1>", self._on_prestamo_doble_clic)

        self._cargar_comboboxes_prestamos()
        self._cargar_tabla_prestamos()

    def _setup_tab_reportes(self) -> None:
        frame_main = ttk.Frame(self.tab_reportes, padding=20)
        frame_main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_main, text="Generación de Reportes y Exportaciones", font=("Helvetica", 14, "bold")).pack(pady=10)
        ttk.Label(frame_main, text="Las siguientes operaciones son intensivas y se ejecutarán en segundo plano (Hilos).").pack(pady=5)

        self.btn_estadisticas = ttk.Button(frame_main, text="Generar Estadísticas", command=self._on_btn_estadisticas)
        self.btn_estadisticas.pack(pady=5, ipadx=10, ipady=5)

        self.btn_respaldo = ttk.Button(frame_main, text="Realizar Respaldo Pesado", command=self._on_btn_respaldo)
        self.btn_respaldo.pack(pady=5, ipadx=10, ipady=5)
        
        self.btn_export_json = ttk.Button(frame_main, text="Exportar Catálogo a JSON", command=self._on_export_json)
        self.btn_export_json.pack(pady=5, ipadx=10, ipady=5)
        
        self.btn_export_xml = ttk.Button(frame_main, text="Exportar Catálogo a XML", command=self._on_export_xml)
        self.btn_export_xml.pack(pady=5, ipadx=10, ipady=5)
        
        ttk.Separator(frame_main, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        self.btn_graficas = ttk.Button(frame_main, text="Visualizar Gráficas Estadísticas", command=self._mostrar_graficas)
        self.btn_graficas.pack(pady=5, ipadx=10, ipady=5)

    def _cambiar_estado_botones(self, estado: str) -> None:
        self.btn_estadisticas.config(state=estado)
        self.btn_respaldo.config(state=estado)
        self.btn_export_json.config(state=estado)
        self.btn_export_xml.config(state=estado)
        self.btn_graficas.config(state=estado)

    def _on_btn_estadisticas(self) -> None:
        self._cambiar_estado_botones(tk.DISABLED)
        self.lbl_estado.config(text="Procesando estadísticas... por favor espera.")
        
        worker = BackgroundWorker(
            target=self._generar_estadisticas_pesadas,
            ui_after_method=self.after,
            on_success=self._on_estadisticas_success,
            on_error=self._on_worker_error
        )
        worker.start()

    def _generar_estadisticas_pesadas(self) -> str:
        time.sleep(3)
        libros = self.libro_controller.obtener_todos()
        prestamos = self.prestamo_controller.obtener_activos()
        return f"Estadísticas calculadas:\n- Total Libros: {len(libros)}\n- Préstamos Activos: {len(prestamos)}"

    def _on_estadisticas_success(self, resultado: str) -> None:
        self._cambiar_estado_botones(tk.NORMAL)
        self.lbl_estado.config(text="Listo.")
        messagebox.showinfo("Reporte Generado", resultado)

    def _on_btn_respaldo(self) -> None:
        self._cambiar_estado_botones(tk.DISABLED)
        self.lbl_estado.config(text="Procesando respaldo profundo... por favor espera.")
        
        worker = BackgroundWorker(
            target=self._realizar_respaldo_pesado,
            ui_after_method=self.after,
            on_success=self._on_respaldo_success,
            on_error=self._on_worker_error
        )
        worker.start()

    def _realizar_respaldo_pesado(self) -> str:
        time.sleep(3)
        self.libro_controller.respaldar_datos()
        return "El respaldo de la base de datos se ha completado exitosamente."

    def _on_respaldo_success(self, resultado: str) -> None:
        self._cambiar_estado_botones(tk.NORMAL)
        self.lbl_estado.config(text="Listo.")
        messagebox.showinfo("Respaldo Terminado", resultado)
        
    def _on_export_json(self) -> None:
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if not ruta:
            return
            
        self._cambiar_estado_botones(tk.DISABLED)
        self.lbl_estado.config(text="Exportando a JSON... por favor espera.")
        libros = self.libro_controller.obtener_todos()
        
        worker = BackgroundWorker(
            target=ExportService.exportar_a_json,
            args=(libros, ruta),
            ui_after_method=self.after,
            on_success=lambda r: self._on_export_success(r, "exportacion_json", ruta),
            on_error=self._on_worker_error
        )
        worker.start()

    def _on_export_xml(self) -> None:
        ruta = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Archivos XML", "*.xml")])
        if not ruta:
            return
            
        self._cambiar_estado_botones(tk.DISABLED)
        self.lbl_estado.config(text="Exportando a XML... por favor espera.")
        libros = self.libro_controller.obtener_todos()
        
        worker = BackgroundWorker(
            target=ExportService.exportar_a_xml,
            args=(libros, ruta),
            ui_after_method=self.after,
            on_success=lambda r: self._on_export_success(r, "exportacion_xml", ruta),
            on_error=self._on_worker_error
        )
        worker.start()

    def _on_export_success(self, resultado: str, tipo_evento: str, ruta: str) -> None:
        self._cambiar_estado_botones(tk.NORMAL)
        self.lbl_estado.config(text="Listo.")
        self._log_evento(tipo_evento, f"Catálogo exportado exitosamente a {ruta}", "Reportes")
        messagebox.showinfo("Exportación Completa", resultado)

    def _on_worker_error(self, error: Exception) -> None:
        self._cambiar_estado_botones(tk.NORMAL)
        self.lbl_estado.config(text="Error durante el procesamiento.")
        messagebox.showerror("Error de Hilo", f"La operación en segundo plano falló:\n{str(error)}")

    def _mostrar_graficas(self) -> None:
        if not MATPLOTLIB_DISPONIBLE:
            messagebox.showerror("Error", "La biblioteca 'matplotlib' no está instalada.\nEjecuta: pip install matplotlib")
            return
            
        libros = self.libro_controller.obtener_todos()
        usuarios = self.usuario_controller.obtener_todos()
        
        if not libros and not usuarios:
            messagebox.showinfo("Aviso", "No hay datos suficientes para generar las gráficas.")
            return

        ventana_graficas = tk.Toplevel(self)
        ventana_graficas.title("Gráficas Estadísticas del Sistema")
        ventana_graficas.geometry("800x400")
        ventana_graficas.minsize(600, 400)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        
        # Gráfica 1: Disponibilidad de Libros (Pastel)
        disponibles = sum(1 for l in libros if l.disponibilidad)
        prestados = len(libros) - disponibles
        
        if len(libros) > 0:
            ax1.pie([disponibles, prestados], labels=["Disponibles", "Prestados"], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'], startangle=90)
            ax1.set_title("Estado del Catálogo de Libros")
        else:
            ax1.text(0.5, 0.5, "Sin registros de libros", ha='center')
            
        # Gráfica 2: Tipos de Usuario (Barras)
        tipos = {}
        for u in usuarios:
            tipos[u.tipo_usuario] = tipos.get(u.tipo_usuario, 0) + 1
            
        if tipos:
            nombres = list(tipos.keys())
            valores = list(tipos.values())
            colores = ['#2196F3', '#FF9800', '#9C27B0', '#00BCD4'][:len(nombres)]
            
            ax2.bar(nombres, valores, color=colores)
            ax2.set_title("Distribución de Usuarios")
            ax2.set_ylabel("Cantidad de Usuarios")
            
            # Forzar valores enteros en el eje Y
            max_y = max(valores) if valores else 1
            ax2.set_yticks(range(0, max_y + 2))
        else:
            ax2.text(0.5, 0.5, "Sin registros de usuarios", ha='center')
            
        fig.tight_layout()
        
        # Incrustar Matplotlib en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_graficas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==========================
    # EVENTOS COMPARTIDOS
    # ==========================
    def _actualizar_reloj(self) -> None:
        self.lbl_reloj.config(text=f"Hora: {time.strftime('%H:%M:%S')}")
        self.after(1000, self._actualizar_reloj)

    def _on_cerrar_ventana(self) -> None:
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación y respaldar la BD?"):
            self.lbl_estado.config(text="Creando respaldo...")
            self.update()
            self.libro_controller.respaldar_datos()
            self._log_evento("app_cerrada", "El usuario cerró la aplicación y respaldó BD.", "Sistema")
            self.destroy()


    # ==========================
    # ACCIONES: LIBROS
    # ==========================
    def _cargar_tabla_libros(self, libros=None) -> None:
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)
        try:
            if libros is None:
                libros = self.libro_controller.obtener_todos()
            for libro in libros:
                self.tabla_libros.insert("", tk.END, iid=str(libro.id),
                    values=(libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero, "Sí" if libro.disponibilidad else "No"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_formulario_libros(self) -> None:
        self.libro_id_seleccionado = None
        self.var_titulo.set("")
        self.var_autor.set("")
        self.var_isbn.set("")
        self.var_anio.set("")
        self.var_genero.set("")
        self.var_disponible.set("Sí")

    def _on_libro_doble_clic(self, event) -> None:
        seleccion = self.tabla_libros.selection()
        if seleccion and self.cb_seleccionar_libro:
            self.libro_id_seleccionado = int(seleccion[0])
            try:
                libro = self.cb_seleccionar_libro(self.libro_id_seleccionado)
                self.var_titulo.set(libro.titulo)
                self.var_autor.set(libro.autor)
                self.var_isbn.set(libro.isbn)
                self.var_anio.set(str(libro.anio))
                self.var_genero.set(libro.genero)
                self.var_disponible.set("Sí" if libro.disponibilidad else "No")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _agregar_libro(self) -> None:
        titulo = self.var_titulo.get().strip()
        try:
            self.cb_guardar_libro(titulo, self.var_autor.get(), self.var_isbn.get(),
                                  self.var_anio.get(), self.var_genero.get(), self.var_disponible.get())
            messagebox.showinfo("Éxito", "Libro agregado.")
            self._log_evento("libro_creado", f"Libro registrado: {titulo}", "Libros")
            self._limpiar_formulario_libros()
            self.event_generate("<<LibroGuardado>>")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _editar_libro(self) -> None:
        if not self.libro_id_seleccionado:
            return messagebox.showwarning("Atención", "Selecciona un libro.")
        try:
            self.libro_controller.actualizar_libro(
                self.libro_id_seleccionado, self.var_titulo.get(), self.var_autor.get(),
                self.var_isbn.get(), self.var_anio.get(), self.var_genero.get(), self.var_disponible.get()
            )
            messagebox.showinfo("Éxito", "Libro actualizado.")
            self._log_evento("libro_actualizado", f"Libro actualizado. ID: {self.libro_id_seleccionado}", "Libros")
            self._limpiar_formulario_libros()
            self.event_generate("<<LibroGuardado>>")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_libro(self) -> None:
        if not self.libro_id_seleccionado:
            return messagebox.showwarning("Atención", "Selecciona un libro.")
        if messagebox.askyesno("Confirmar", "¿Eliminar este libro?"):
            try:
                self.cb_eliminar_libro(self.libro_id_seleccionado)
                messagebox.showinfo("Éxito", "Libro eliminado.")
                self._log_evento("libro_eliminado", f"Libro eliminado. ID: {self.libro_id_seleccionado}", "Libros")
                self._limpiar_formulario_libros()
                self.event_generate("<<LibroGuardado>>")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _buscar_libro(self) -> None:
        termino = self.var_busqueda.get().strip()
        if not termino:
            return self._cargar_tabla_libros()
        try:
            resultados = self.libro_controller.buscar_libros(termino)
            self._cargar_tabla_libros(libros=resultados)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # ACCIONES: USUARIOS
    # ==========================
    def _cargar_tabla_usuarios(self) -> None:
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        try:
            usuarios = self.usuario_controller.obtener_todos()
            for u in usuarios:
                self.tabla_usuarios.insert("", tk.END, iid=str(u.id), values=(u.nombre, u.email, u.tipo_usuario))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_formulario_usuarios(self) -> None:
        self.usuario_id_seleccionado = None
        self.var_usuario_nombre.set("")
        self.var_usuario_email.set("")
        self.var_usuario_tipo.set("")

    def _on_usuario_doble_clic(self, event) -> None:
        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            self.usuario_id_seleccionado = int(seleccion[0])
            valores = self.tabla_usuarios.item(seleccion[0], "values")
            self.var_usuario_nombre.set(valores[0])
            self.var_usuario_email.set(valores[1])
            self.var_usuario_tipo.set(valores[2])

    def _agregar_usuario(self) -> None:
        nombre = self.var_usuario_nombre.get().strip()
        try:
            self.usuario_controller.agregar_usuario(
                nombre,
                self.var_usuario_email.get().strip(),
                self.var_usuario_tipo.get().strip()
            )
            messagebox.showinfo("Éxito", "Usuario agregado.")
            self._log_evento("usuario_creado", f"Usuario creado: {nombre}", "Usuarios")
            self._limpiar_formulario_usuarios()
            self.event_generate("<<UsuarioGuardado>>")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _editar_usuario(self) -> None:
        if not self.usuario_id_seleccionado:
            return messagebox.showwarning("Atención", "Selecciona un usuario.")
        try:
            self.usuario_controller.actualizar_usuario(
                self.usuario_id_seleccionado,
                self.var_usuario_nombre.get().strip(),
                self.var_usuario_email.get().strip(),
                self.var_usuario_tipo.get().strip()
            )
            messagebox.showinfo("Éxito", "Usuario actualizado.")
            self._log_evento("usuario_actualizado", f"Usuario ID: {self.usuario_id_seleccionado} modificado", "Usuarios")
            self._limpiar_formulario_usuarios()
            self.event_generate("<<UsuarioGuardado>>")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_usuario(self) -> None:
        if not self.usuario_id_seleccionado:
            return messagebox.showwarning("Atención", "Selecciona un usuario.")
        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            try:
                self.usuario_controller.eliminar_usuario(self.usuario_id_seleccionado)
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self._log_evento("usuario_eliminado", f"Usuario ID: {self.usuario_id_seleccionado} eliminado", "Usuarios")
                self._limpiar_formulario_usuarios()
                self.event_generate("<<UsuarioGuardado>>")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ==========================
    # ACCIONES: PRÉSTAMOS
    # ==========================
    def _cargar_comboboxes_prestamos(self) -> None:
        try:
            usuarios = self.usuario_controller.obtener_todos()
            libros = self.libro_controller.obtener_todos()

            self.map_usuarios_combo = {f"{u.nombre} ({u.email})": u.id for u in usuarios}
            self.map_libros_combo = {f"{l.titulo} - {l.autor}": l.id for l in libros if l.disponibilidad}

            self.combo_prestamo_usuario["values"] = list(self.map_usuarios_combo.keys())
            self.combo_prestamo_libro["values"] = list(self.map_libros_combo.keys())
            
            self.var_prestamo_usuario.set("")
            self.var_prestamo_libro.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar listas: {str(e)}")

    def _cargar_tabla_prestamos(self) -> None:
        for item in self.tabla_prestamos.get_children():
            self.tabla_prestamos.delete(item)
        try:
            prestamos = self.prestamo_controller.obtener_activos()
            for p in prestamos:
                self.tabla_prestamos.insert("", tk.END, iid=str(p["id"]), values=(p["id"], p["libro"], p["usuario"], p["fecha_prestamo"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_prestamo_doble_clic(self, event) -> None:
        seleccion = self.tabla_prestamos.selection()
        if seleccion:
            self.prestamo_id_seleccionado = int(seleccion[0])
            self.lbl_estado.config(text=f"Préstamo #{self.prestamo_id_seleccionado} seleccionado. Listo para devolver.")

    def _prestar_libro(self) -> None:
        usuario_key = self.var_prestamo_usuario.get()
        libro_key = self.var_prestamo_libro.get()

        if not usuario_key or not libro_key:
            return messagebox.showwarning("Atención", "Selecciona usuario y libro.")

        usuario_id = self.map_usuarios_combo.get(usuario_key)
        libro_id = self.map_libros_combo.get(libro_key)

        try:
            self.prestamo_controller.prestar_libro(libro_id, usuario_id)
            messagebox.showinfo("Éxito", "Préstamo registrado. El libro ya no está disponible.")
            self._log_evento("prestamo_creado", f"Libro ID {libro_id} prestado a Usuario ID {usuario_id}", "Préstamos")
            self.event_generate("<<PrestamoGuardado>>")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _devolver_libro(self) -> None:
        if not self.prestamo_id_seleccionado:
            return messagebox.showwarning("Atención", "Selecciona un préstamo activo en la tabla dando doble clic.")

        if messagebox.askyesno("Confirmar", "¿Deseas registrar la devolución de este libro?"):
            try:
                self.prestamo_controller.devolver_libro(self.prestamo_id_seleccionado)
                messagebox.showinfo("Éxito", "Libro devuelto. Ahora vuelve a estar disponible.")
                self._log_evento("devolucion_registrada", f"Devolución del préstamo ID: {self.prestamo_id_seleccionado}", "Préstamos")
                self.prestamo_id_seleccionado = None
                self.event_generate("<<PrestamoGuardado>>")
            except Exception as e:
                messagebox.showerror("Error", str(e))
