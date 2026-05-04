"""Catálogo principal y protocolo Buscable."""

import json
from pathlib import Path
from typing import Protocol

from modelos.libro import Libro
from modelos.prestamo import Prestamo
from modelos.usuario import Usuario


class Buscable(Protocol):
    """Protocolo para objetos que pueden buscar."""

    def buscar(self, query: str) -> list:
        """Busca coincidencias."""
        ...


class Catalogo:
    """Gestiona libros, usuarios y préstamos."""

    def __init__(self) -> None:
        """Inicializa catálogo."""
        self.libros: list[Libro] = []
        self.usuarios: dict[str, Usuario] = {}
        self.prestamos: list[Prestamo] = []

    def agregar_libro(self, libro: Libro) -> None:
        """Agrega libro al catálogo."""
        if any(actual.isbn == libro.isbn for actual in self.libros):
            raise ValueError("Ya existe un libro con ese ISBN.")
        self.libros.append(libro)

    def eliminar_libro(self, isbn: str) -> None:
        """Elimina libro por ISBN."""
        antes = len(self.libros)
        self.libros = [libro for libro in self.libros if libro.isbn != isbn]
        if len(self.libros) == antes:
            raise KeyError("No se encontró el libro.")

    def buscar(self, query: str) -> list[Libro]:
        """Busca por título, autor o ISBN."""
        texto = query.lower().strip()
        return [
            libro for libro in self.libros
            if texto in libro.titulo.lower()
            or texto in libro.autor.lower()
            or texto in libro.isbn.lower()
        ]

    def listar_disponibles(self) -> list[Libro]:
        """Lista libros disponibles."""
        return [libro for libro in self.libros if libro.disponible]

    def registrar_usuario(self, usuario: Usuario) -> None:
        """Registra usuario por email."""
        if usuario.email in self.usuarios:
            raise ValueError("Ya existe un usuario con ese email.")
        self.usuarios[usuario.email] = usuario

    def registrar_prestamo(self, email: str, isbn: str) -> Prestamo:
        """Registra un préstamo."""
        if email not in self.usuarios:
            raise KeyError("Usuario no encontrado.")

        usuario = self.usuarios[email]
        libro = self._buscar_libro_por_isbn(isbn)

        if not libro.disponible:
            raise ValueError("El libro no está disponible.")

        if not usuario.puede_pedir_prestado():
            raise ValueError("El usuario llegó al límite de préstamos.")

        libro.disponible = False
        usuario.prestamos_activos += 1
        prestamo = Prestamo(usuario, libro)
        self.prestamos.append(prestamo)
        return prestamo

    def procesar_devolucion(self, email: str, isbn: str,
                            dias_retraso: int = 0) -> Prestamo:
        """Procesa devolución de un libro."""
        for prestamo in self.prestamos:
            if (
                prestamo.usuario.email == email
                and prestamo.libro.isbn == isbn
                and not prestamo.devuelto
            ):
                prestamo.cerrar(dias_retraso)
                return prestamo

        raise KeyError("Préstamo activo no encontrado.")

    def generar_reporte(self) -> str:
        """Genera reporte general."""
        activos = [p for p in self.prestamos if not p.devuelto]
        return (
            "REPORTE DE BIBLIOTECA\n"
            f"Libros totales: {len(self.libros)}\n"
            f"Libros disponibles: {len(self.listar_disponibles())}\n"
            f"Usuarios registrados: {len(self.usuarios)}\n"
            f"Préstamos totales: {len(self.prestamos)}\n"
            f"Préstamos activos: {len(activos)}"
        )

    def guardar_json(self, ruta: str) -> None:
        """Guarda catálogo en JSON."""
        path = Path(ruta)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "libros": [libro.to_dict() for libro in self.libros],
            "usuarios": [
                usuario.to_dict() for usuario in self.usuarios.values()
            ],
            "prestamos": [prestamo.to_dict() for prestamo in self.prestamos],
        }
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=4)

    def cargar_json(self, ruta: str) -> None:
        """Carga catálogo desde JSON."""
        from modelos.usuario import Usuario

        path = Path(ruta)
        with open(path, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        self.libros = [Libro.from_dict(item) for item in data.get("libros", [])]
        self.usuarios = {
            usuario.email: usuario
            for usuario in [
                Usuario.from_dict(item) for item in data.get("usuarios", [])
            ]
        }

        self.prestamos = []
        for item in data.get("prestamos", []):
            usuario = self.usuarios.get(item["usuario_email"])
            libro = self._buscar_libro_por_isbn(item["libro_isbn"])
            if usuario and libro:
                prestamo = Prestamo(
                    usuario=usuario,
                    libro=libro,
                    fecha_prestamo=item.get("fecha_prestamo"),
                    fecha_devolucion=item.get("fecha_devolucion"),
                    devuelto=bool(item.get("devuelto", False)),
                    multa=float(item.get("multa", 0.0)),
                    id_entidad=item.get("id"),
                    fecha_creacion=item.get("fecha_creacion"),
                )
                self.prestamos.append(prestamo)

    def _buscar_libro_por_isbn(self, isbn: str) -> Libro:
        """Busca libro por ISBN."""
        isbn = isbn.replace("-", "").replace(" ", "")
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        raise KeyError("Libro no encontrado.")
