"""Clases relacionadas con libros."""

from datetime import datetime

from modelos.entidad import Entidad
from utils.constantes import FORMATOS_VALIDOS
from utils.validadores import validar_isbn13, validar_url


class Libro(Entidad):
    """Representa un libro general."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        disponible: bool = True,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa un libro."""
        super().__init__(id_entidad, fecha_creacion)
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio = anio
        self.genero = genero
        self.disponible = disponible

    @property
    def titulo(self) -> str:
        """Devuelve el título."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    @property
    def autor(self) -> str:
        """Devuelve el autor."""
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El autor no puede estar vacío.")
        self._autor = valor.strip()

    @property
    def isbn(self) -> str:
        """Devuelve el ISBN."""
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        isbn_limpio = valor.replace("-", "").replace(" ", "")
        if not validar_isbn13(isbn_limpio):
            raise ValueError("ISBN-13 inválido.")
        self._isbn = isbn_limpio

    @property
    def anio(self) -> int:
        """Devuelve el año."""
        return self._anio

    @anio.setter
    def anio(self, valor: int) -> None:
        anio_actual = datetime.now().year
        if valor < 1440 or valor > anio_actual:
            raise ValueError("El año debe estar entre 1440 y el año actual.")
        self._anio = valor

    @property
    def genero(self) -> str:
        """Devuelve el género."""
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El género no puede estar vacío.")
        self._genero = valor.strip()

    @property
    def disponible(self) -> bool:
        """Indica si está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    def __str__(self) -> str:
        """Representación legible."""
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.titulo} - {self.autor} ({self.anio}) [{estado}]"

    def __repr__(self) -> str:
        """Representación técnica."""
        return (
            f"Libro(titulo={self.titulo!r}, autor={self.autor!r}, "
            f"isbn={self.isbn!r})"
        )

    def __eq__(self, otro: object) -> bool:
        """Compara libros por ISBN."""
        if not isinstance(otro, Libro):
            return False
        return self.isbn == otro.isbn

    def to_dict(self) -> dict:
        """Convierte el libro a diccionario."""
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "fecha_creacion": self.fecha_creacion,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "anio": self.anio,
            "genero": self.genero,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Libro":
        """Crea un libro desde diccionario."""
        tipo = data.get("tipo", "Libro")
        if tipo == "LibroDigital":
            return LibroDigital.from_dict(data)
        if tipo == "LibroFisico":
            return LibroFisico.from_dict(data)

        return cls(
            titulo=data["titulo"],
            autor=data["autor"],
            isbn=data["isbn"],
            anio=int(data["anio"]),
            genero=data["genero"],
            disponible=bool(data.get("disponible", True)),
            id_entidad=data.get("id"),
            fecha_creacion=data.get("fecha_creacion"),
        )


class LibroDigital(Libro):
    """Representa un libro digital."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        formato: str,
        tamano_mb: float,
        url_descarga: str,
        disponible: bool = True,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa un libro digital."""
        super().__init__(
            titulo, autor, isbn, anio, genero, disponible,
            id_entidad, fecha_creacion
        )
        self.formato = formato
        self.tamano_mb = tamano_mb
        self.url_descarga = url_descarga

    @property
    def formato(self) -> str:
        """Devuelve el formato."""
        return self._formato

    @formato.setter
    def formato(self, valor: str) -> None:
        valor = valor.upper().strip()
        if valor not in FORMATOS_VALIDOS:
            raise ValueError("Formato inválido.")
        self._formato = valor

    @property
    def tamano_mb(self) -> float:
        """Devuelve el tamaño."""
        return self._tamano_mb

    @tamano_mb.setter
    def tamano_mb(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El tamaño debe ser mayor a 0.")
        self._tamano_mb = float(valor)

    @property
    def url_descarga(self) -> str:
        """Devuelve la URL."""
        return self._url_descarga

    @url_descarga.setter
    def url_descarga(self, valor: str) -> None:
        if not validar_url(valor):
            raise ValueError("URL inválida.")
        self._url_descarga = valor

    def __str__(self) -> str:
        """Representación legible."""
        return f"{super().__str__()} - Digital {self.formato}"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        data = super().to_dict()
        data.update({
            "formato": self.formato,
            "tamano_mb": self.tamano_mb,
            "url_descarga": self.url_descarga,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "LibroDigital":
        """Crea libro digital desde diccionario."""
        return cls(
            titulo=data["titulo"],
            autor=data["autor"],
            isbn=data["isbn"],
            anio=int(data["anio"]),
            genero=data["genero"],
            formato=data["formato"],
            tamano_mb=float(data["tamano_mb"]),
            url_descarga=data["url_descarga"],
            disponible=bool(data.get("disponible", True)),
            id_entidad=data.get("id"),
            fecha_creacion=data.get("fecha_creacion"),
        )


class LibroFisico(Libro):
    """Representa un libro físico."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio: int,
        genero: str,
        ubicacion: str,
        num_ejemplares: int,
        disponible: bool = True,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa libro físico."""
        super().__init__(
            titulo, autor, isbn, anio, genero, disponible,
            id_entidad, fecha_creacion
        )
        self.ubicacion = ubicacion
        self.num_ejemplares = num_ejemplares

    @property
    def ubicacion(self) -> str:
        """Devuelve ubicación."""
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La ubicación no puede estar vacía.")
        self._ubicacion = valor.strip()

    @property
    def num_ejemplares(self) -> int:
        """Devuelve número de ejemplares."""
        return self._num_ejemplares

    @num_ejemplares.setter
    def num_ejemplares(self, valor: int) -> None:
        if valor < 1:
            raise ValueError("Debe haber al menos 1 ejemplar.")
        self._num_ejemplares = int(valor)

    def __str__(self) -> str:
        """Representación legible."""
        return f"{super().__str__()} - Físico en {self.ubicacion}"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        data = super().to_dict()
        data.update({
            "ubicacion": self.ubicacion,
            "num_ejemplares": self.num_ejemplares,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "LibroFisico":
        """Crea libro físico desde diccionario."""
        return cls(
            titulo=data["titulo"],
            autor=data["autor"],
            isbn=data["isbn"],
            anio=int(data["anio"]),
            genero=data["genero"],
            ubicacion=data["ubicacion"],
            num_ejemplares=int(data["num_ejemplares"]),
            disponible=bool(data.get("disponible", True)),
            id_entidad=data.get("id"),
            fecha_creacion=data.get("fecha_creacion"),
        )
