"""Repositorio de acceso a datos SQL para el Sistema de Gestión."""

import sqlite3
import os
from typing import List, Optional

from models.libro import Libro
from models.usuario import Usuario
from models.prestamo import Prestamo

# Ruta por defecto: guarda biblioteca.db dentro de la carpeta 'data'
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "biblioteca.db")


class SQLRepository:
    """Clase para manejar las operaciones CRUD con la base de datos SQLite."""

    def __init__(self, db_path: str = DB_PATH) -> None:
        """Inicializa el repositorio y crea las tablas si no existen."""
        self.db_path = db_path
        self._inicializar_bd()

    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos configurada."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
            # Habilitar soporte de llaves foráneas en SQLite (por defecto viene apagado)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al conectar con la BD: {e}")

    def _inicializar_bd(self) -> None:
        """Crea las tablas de libros, usuarios y préstamos si no existen."""
        script_creacion = """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            anio INTEGER NOT NULL,
            genero TEXT NOT NULL,
            disponibilidad INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            tipo_usuario TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            estado TEXT NOT NULL DEFAULT 'activo',
            FOREIGN KEY (libro_id) REFERENCES libros(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """
        try:
            with self._get_connection() as conn:
                conn.executescript(script_creacion)
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al inicializar la base de datos: {e}")

    def respaldar_bd(self) -> None:
        """Crea una copia de seguridad de la base de datos."""
        import shutil
        backup_path = self.db_path + ".bak"
        try:
            shutil.copy2(self.db_path, backup_path)
        except Exception as e:
            print(f"Error al crear respaldo de la BD: {e}")

    # ==========================
    # CRUD COMPLETO PARA LIBROS
    # ==========================

    def crear_libro(self, libro: Libro) -> Libro:
        """Inserta un nuevo libro en la base de datos usando consultas parametrizadas."""
        query = """
            INSERT INTO libros (titulo, autor, isbn, anio, genero, disponibilidad)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # Convertimos booleano a entero para SQLite (1 o 0)
        disp_int = 1 if libro.disponibilidad else 0
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query, 
                    (libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero, disp_int)
                )
                conn.commit()
                libro.id = cursor.lastrowid
                return libro
        except sqlite3.IntegrityError:
            raise ValueError(f"Ya existe un libro registrado con el ISBN {libro.isbn}.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al crear el libro en la base de datos: {e}")

    def obtener_libros(self) -> List[Libro]:
        """Obtiene todos los libros registrados."""
        query = "SELECT * FROM libros"
        libros = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for row in cursor.execute(query):
                    libro = Libro(
                        id=row["id"],
                        titulo=row["titulo"],
                        autor=row["autor"],
                        isbn=row["isbn"],
                        anio=row["anio"],
                        genero=row["genero"],
                        disponibilidad=bool(row["disponibilidad"])
                    )
                    libros.append(libro)
            return libros
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al obtener los libros: {e}")

    def obtener_libro_por_id(self, id_libro: int) -> Optional[Libro]:
        """Obtiene un libro específico por su ID."""
        query = "SELECT * FROM libros WHERE id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_libro,))
                row = cursor.fetchone()
                if row:
                    return Libro(
                        id=row["id"],
                        titulo=row["titulo"],
                        autor=row["autor"],
                        isbn=row["isbn"],
                        anio=row["anio"],
                        genero=row["genero"],
                        disponibilidad=bool(row["disponibilidad"])
                    )
                return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al obtener libro por ID: {e}")

    def actualizar_libro(self, libro: Libro) -> None:
        """Actualiza la información de un libro existente."""
        if not libro.id:
            raise ValueError("El libro no tiene un ID asignado para actualizar.")
            
        query = """
            UPDATE libros
            SET titulo = ?, autor = ?, isbn = ?, anio = ?, genero = ?, disponibilidad = ?
            WHERE id = ?
        """
        disp_int = 1 if libro.disponibilidad else 0
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query, 
                    (libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero, disp_int, libro.id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError(f"No se encontró ningún libro con el ID {libro.id}.")
        except sqlite3.IntegrityError:
            raise ValueError(f"El ISBN {libro.isbn} ya pertenece a otro libro.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al actualizar el libro: {e}")

    def eliminar_libro(self, id_libro: int) -> None:
        """Elimina un libro por su ID."""
        query = "DELETE FROM libros WHERE id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_libro,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError(f"No se encontró ningún libro con el ID {id_libro} para eliminar.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al eliminar el libro: {e}")

    def buscar_libros(self, termino: str) -> List[Libro]:
        """Busca libros cuyo título o autor coincidan parcialmente con el término."""
        query = "SELECT * FROM libros WHERE titulo LIKE ? OR autor LIKE ?"
        termino_like = f"%{termino}%"
        libros = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for row in cursor.execute(query, (termino_like, termino_like)):
                    libro = Libro(
                        id=row["id"],
                        titulo=row["titulo"],
                        autor=row["autor"],
                        isbn=row["isbn"],
                        anio=row["anio"],
                        genero=row["genero"],
                        disponibilidad=bool(row["disponibilidad"])
                    )
                    libros.append(libro)
            return libros
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al buscar libros: {e}")

    # ==========================
    # FUNCIONES BASE PARA USUARIOS Y PRÉSTAMOS
    # ==========================
    
    def crear_usuario(self, usuario: Usuario) -> Usuario:
        """Inserta un nuevo usuario (Función base)."""
        query = "INSERT INTO usuarios (nombre, email, tipo_usuario) VALUES (?, ?, ?)"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario.nombre, usuario.email, usuario.tipo_usuario))
                conn.commit()
                usuario.id = cursor.lastrowid
                return usuario
        except sqlite3.IntegrityError:
            raise ValueError(f"Ya existe un usuario con el email {usuario.email}.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al crear el usuario: {e}")

    def obtener_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        query = "SELECT * FROM usuarios"
        usuarios = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for row in cursor.execute(query):
                    usuarios.append(Usuario(id=row["id"], nombre=row["nombre"], email=row["email"], tipo_usuario=row["tipo_usuario"]))
            return usuarios
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al obtener usuarios: {e}")

    def actualizar_usuario(self, usuario: Usuario) -> None:
        """Actualiza un usuario."""
        if not usuario.id:
            raise ValueError("ID requerido.")
        query = "UPDATE usuarios SET nombre = ?, email = ?, tipo_usuario = ? WHERE id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario.nombre, usuario.email, usuario.tipo_usuario, usuario.id))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError("Usuario no encontrado.")
        except sqlite3.IntegrityError:
            raise ValueError(f"Ya existe un usuario con el email {usuario.email}.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al actualizar usuario: {e}")

    def eliminar_usuario(self, id_usuario: int) -> None:
        """Elimina un usuario. Falla si tiene préstamos activos (llave foránea)."""
        query = "DELETE FROM usuarios WHERE id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_usuario,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError("Usuario no encontrado.")
        except sqlite3.IntegrityError:
            raise ValueError("No se puede eliminar el usuario porque tiene préstamos asociados.")
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al eliminar usuario: {e}")

    # ==========================
    # TRANSACCIONES PARA PRÉSTAMOS
    # ==========================

    def registrar_prestamo_transaccion(self, prestamo: Prestamo) -> Prestamo:
        """Registra un préstamo y actualiza la disponibilidad del libro en una transacción."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. Verificar disponibilidad
                cursor.execute("SELECT disponibilidad FROM libros WHERE id = ?", (prestamo.libro_id,))
                row = cursor.fetchone()
                if not row:
                    raise ValueError(f"El libro con ID {prestamo.libro_id} no existe.")
                if row["disponibilidad"] == 0:
                    raise ValueError("El libro no está disponible actualmente.")
                    
                # 2. Insertar préstamo
                query_insert = "INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, estado) VALUES (?, ?, ?, ?)"
                cursor.execute(query_insert, (prestamo.libro_id, prestamo.usuario_id, prestamo.fecha_prestamo.isoformat(), prestamo.estado))
                prestamo.id = cursor.lastrowid
                
                # 3. Actualizar disponibilidad
                cursor.execute("UPDATE libros SET disponibilidad = 0 WHERE id = ?", (prestamo.libro_id,))
                
                conn.commit()
                return prestamo
        except sqlite3.Error as e:
            raise RuntimeError(f"Error en transacción de préstamo: {e}")

    def registrar_devolucion_transaccion(self, prestamo_id: int, fecha_devolucion: str) -> None:
        """Registra la devolución y actualiza el libro a disponible."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del libro
                cursor.execute("SELECT libro_id FROM prestamos WHERE id = ?", (prestamo_id,))
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Préstamo no encontrado.")
                libro_id = row["libro_id"]
                
                # Actualizar préstamo
                cursor.execute("UPDATE prestamos SET estado = 'devuelto', fecha_devolucion = ? WHERE id = ?", (fecha_devolucion, prestamo_id))
                
                # Actualizar libro
                cursor.execute("UPDATE libros SET disponibilidad = 1 WHERE id = ?", (libro_id,))
                
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Error en transacción de devolución: {e}")

    def obtener_prestamos_activos(self) -> List[dict]:
        """Obtiene una lista de préstamos activos con datos unidos."""
        query = """
            SELECT p.id, l.titulo as libro, u.nombre as usuario, p.fecha_prestamo 
            FROM prestamos p
            JOIN libros l ON p.libro_id = l.id
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.estado = 'activo'
        """
        prestamos = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for row in cursor.execute(query):
                    prestamos.append({
                        "id": row["id"],
                        "libro": row["libro"],
                        "usuario": row["usuario"],
                        "fecha_prestamo": row["fecha_prestamo"]
                    })
            return prestamos
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al obtener préstamos activos: {e}")
