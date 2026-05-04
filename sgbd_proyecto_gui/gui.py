"""Interfaz gráfica básica para el Sistema de Gestión de Biblioteca Digital.

Ejecutar con:
    python gui.py
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from modelos.catalogo import Catalogo
from modelos.libro import Libro
from modelos.usuario import Administrador, Alumno, Profesor
from main import RUTA_DATOS, seed_data


class BibliotecaGUI:
    """Ventana principal del sistema de biblioteca."""

    def __init__(self, root: tk.Tk) -> None:
        """Inicializa la interfaz."""
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca Digital")
        self.root.geometry("850x550")

        self.catalogo = Catalogo()

        try:
            self.catalogo.cargar_json(RUTA_DATOS)
        except FileNotFoundError:
            seed_data(self.catalogo)

        self.crear_widgets()
        self.actualizar_tabla()

    def crear_widgets(self) -> None:
        """Crea botones, tabla y cajas de la ventana."""
        titulo = tk.Label(
            self.root,
            text="Sistema de Gestión de Biblioteca Digital",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=10)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        botones = [
            ("Agregar libro", self.agregar_libro),
            ("Buscar libro", self.buscar_libro),
            ("Registrar usuario", self.registrar_usuario),
            ("Prestar libro", self.prestar_libro),
            ("Devolver libro", self.devolver_libro),
            ("Reporte", self.mostrar_reporte),
            ("Guardar y salir", self.guardar_y_salir),
        ]

        for texto, comando in botones:
            tk.Button(
                frame_botones,
                text=texto,
                width=18,
                command=comando,
            ).pack(side=tk.LEFT, padx=4)

        columnas = ("titulo", "autor", "isbn", "anio", "genero", "estado")
        self.tabla = ttk.Treeview(
            self.root,
            columns=columnas,
            show="headings",
            height=15,
        )

        for columna in columnas:
            self.tabla.heading(columna, text=columna.capitalize())
            self.tabla.column(columna, width=120)

        self.tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def actualizar_tabla(self, libros: list | None = None) -> None:
        """Actualiza la tabla de libros."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        libros_mostrar = libros if libros is not None else self.catalogo.libros

        for libro in libros_mostrar:
            estado = "Disponible" if libro.disponible else "Prestado"
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    libro.titulo,
                    libro.autor,
                    libro.isbn,
                    libro.anio,
                    libro.genero,
                    estado,
                ),
            )

    def agregar_libro(self) -> None:
        """Abre formulario para agregar libro."""
        try:
            titulo = simpledialog.askstring("Agregar libro", "Título:")
            autor = simpledialog.askstring("Agregar libro", "Autor:")
            isbn = simpledialog.askstring("Agregar libro", "ISBN-13:")
            anio = simpledialog.askinteger("Agregar libro", "Año:")
            genero = simpledialog.askstring("Agregar libro", "Género:")

            if None in (titulo, autor, isbn, anio, genero):
                return

            libro = Libro(titulo, autor, isbn, anio, genero)
            self.catalogo.agregar_libro(libro)
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Libro agregado correctamente.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def buscar_libro(self) -> None:
        """Busca libros por título, autor o ISBN."""
        query = simpledialog.askstring("Buscar libro", "Buscar:")
        if query is None:
            return

        resultados = self.catalogo.buscar(query)
        self.actualizar_tabla(resultados)

        if not resultados:
            messagebox.showinfo("Resultado", "No se encontraron libros.")

    def registrar_usuario(self) -> None:
        """Registra alumno, profesor o administrador."""
        try:
            tipo = simpledialog.askstring(
                "Registrar usuario",
                "Tipo de usuario: alumno / profesor / admin",
            )
            if tipo is None:
                return

            tipo = tipo.lower().strip()
            nombre = simpledialog.askstring("Registrar usuario", "Nombre:")
            email = simpledialog.askstring("Registrar usuario", "Email:")
            contrasena = simpledialog.askstring("Registrar usuario", "Contraseña:")

            if None in (nombre, email, contrasena):
                return

            if tipo == "alumno":
                carrera = simpledialog.askstring("Alumno", "Carrera:")
                semestre = simpledialog.askinteger("Alumno", "Semestre:")
                matricula = simpledialog.askstring("Alumno", "Matrícula:")
                usuario = Alumno(
                    nombre,
                    email,
                    contrasena,
                    carrera or "Sin carrera",
                    semestre or 1,
                    matricula or "Sin matrícula",
                )

            elif tipo == "profesor":
                departamento = simpledialog.askstring("Profesor", "Departamento:")
                usuario = Profesor(
                    nombre,
                    email,
                    contrasena,
                    departamento or "Sin departamento",
                )

            elif tipo == "admin":
                nivel = simpledialog.askstring("Admin", "Nivel de acceso:")
                usuario = Administrador(
                    nombre,
                    email,
                    contrasena,
                    nivel or "básico",
                )

            else:
                raise ValueError("Tipo de usuario inválido.")

            self.catalogo.registrar_usuario(usuario)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def prestar_libro(self) -> None:
        """Registra préstamo."""
        try:
            email = simpledialog.askstring("Prestar libro", "Email del usuario:")
            isbn = simpledialog.askstring("Prestar libro", "ISBN del libro:")

            if email is None or isbn is None:
                return

            prestamo = self.catalogo.registrar_prestamo(
                email.strip().lower(),
                isbn.strip(),
            )
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", f"Préstamo registrado:\n{prestamo}")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def devolver_libro(self) -> None:
        """Procesa devolución."""
        try:
            email = simpledialog.askstring("Devolver libro", "Email del usuario:")
            isbn = simpledialog.askstring("Devolver libro", "ISBN del libro:")
            dias = simpledialog.askinteger("Devolver libro", "Días de retraso:")

            if email is None or isbn is None or dias is None:
                return

            prestamo = self.catalogo.procesar_devolucion(
                email.strip().lower(),
                isbn.strip(),
                dias,
            )
            self.actualizar_tabla()
            messagebox.showinfo(
                "Éxito",
                f"Devolución procesada.\nMulta: ${prestamo.multa}",
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_reporte(self) -> None:
        """Muestra reporte general."""
        messagebox.showinfo("Reporte", self.catalogo.generar_reporte())

    def guardar_y_salir(self) -> None:
        """Guarda datos y cierra ventana."""
        self.catalogo.guardar_json(RUTA_DATOS)
        self.root.destroy()


def main() -> None:
    """Ejecuta la GUI."""
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
