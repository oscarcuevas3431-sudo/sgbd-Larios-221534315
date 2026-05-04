"""Clases de usuarios del sistema."""

from abc import abstractmethod

from modelos.entidad import Entidad
from servicios.calculo_multas import calcular_multa
from utils.constantes import MAX_LIBROS_ALUMNO, MAX_LIBROS_PROFESOR
from utils.validadores import validar_email


class Usuario(Entidad):
    """Clase abstracta para usuarios."""

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str,
        prestamos_activos: int = 0,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa usuario."""
        super().__init__(id_entidad, fecha_creacion)
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.prestamos_activos = prestamos_activos

    @property
    def nombre(self) -> str:
        """Devuelve nombre."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        """Devuelve email."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if not validar_email(valor):
            raise ValueError("Email inválido.")
        self._email = valor.strip().lower()

    @property
    def contrasena(self) -> str:
        """Devuelve contraseña."""
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor or len(valor) < 4:
            raise ValueError("La contraseña debe tener mínimo 4 caracteres.")
        self._contrasena = valor

    @property
    def prestamos_activos(self) -> int:
        """Devuelve préstamos activos."""
        return self._prestamos_activos

    @prestamos_activos.setter
    def prestamos_activos(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("No puede haber préstamos negativos.")
        self._prestamos_activos = int(valor)

    @abstractmethod
    def puede_pedir_prestado(self) -> bool:
        """Indica si puede pedir prestado."""
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "fecha_creacion": self.fecha_creacion,
            "nombre": self.nombre,
            "email": self.email,
            "contrasena": self.contrasena,
            "prestamos_activos": self.prestamos_activos,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Crea usuario desde diccionario."""
        tipo = data.get("tipo", "Alumno")
        clases = {
            "Alumno": Alumno,
            "Profesor": Profesor,
            "Administrador": Administrador,
        }
        clase = clases.get(tipo)
        if clase is None:
            raise ValueError("Tipo de usuario inválido.")
        return clase.from_dict(data)


class Alumno(Usuario):
    """Usuario alumno."""

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str,
        carrera: str,
        semestre: int,
        matricula: str,
        prestamos_activos: int = 0,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa alumno."""
        super().__init__(
            nombre, email, contrasena, prestamos_activos,
            id_entidad, fecha_creacion
        )
        self.carrera = carrera
        self.semestre = semestre
        self.matricula = matricula

    def puede_pedir_prestado(self) -> bool:
        """Valida límite de préstamos."""
        return self.prestamos_activos < MAX_LIBROS_ALUMNO

    def calcular_multa(self, dias_retraso: int) -> float:
        """Calcula multa del alumno."""
        return calcular_multa(dias_retraso, "alumno")

    def __str__(self) -> str:
        """Representación legible."""
        return f"Alumno: {self.nombre} ({self.email})"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        data = super().to_dict()
        data.update({
            "carrera": self.carrera,
            "semestre": self.semestre,
            "matricula": self.matricula,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Alumno":
        """Crea alumno desde diccionario."""
        return cls(
            data["nombre"], data["email"], data["contrasena"],
            data["carrera"], int(data["semestre"]), data["matricula"],
            int(data.get("prestamos_activos", 0)),
            data.get("id"), data.get("fecha_creacion")
        )


class Profesor(Usuario):
    """Usuario profesor."""

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str,
        departamento: str,
        max_libros: int = MAX_LIBROS_PROFESOR,
        prestamos_activos: int = 0,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa profesor."""
        super().__init__(
            nombre, email, contrasena, prestamos_activos,
            id_entidad, fecha_creacion
        )
        self.departamento = departamento
        self.max_libros = max_libros

    def puede_pedir_prestado(self) -> bool:
        """Valida límite de préstamos."""
        return self.prestamos_activos < self.max_libros

    def calcular_multa(self, dias_retraso: int) -> float:
        """Calcula multa del profesor."""
        return calcular_multa(dias_retraso, "profesor")

    def __str__(self) -> str:
        """Representación legible."""
        return f"Profesor: {self.nombre} ({self.email})"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        data = super().to_dict()
        data.update({
            "departamento": self.departamento,
            "max_libros": self.max_libros,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Profesor":
        """Crea profesor desde diccionario."""
        return cls(
            data["nombre"], data["email"], data["contrasena"],
            data["departamento"], int(data.get("max_libros", MAX_LIBROS_PROFESOR)),
            int(data.get("prestamos_activos", 0)),
            data.get("id"), data.get("fecha_creacion")
        )


class Administrador(Usuario):
    """Usuario administrador."""

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str,
        nivel_acceso: str,
        prestamos_activos: int = 0,
        id_entidad: str | None = None,
        fecha_creacion: str | None = None,
    ) -> None:
        """Inicializa administrador."""
        super().__init__(
            nombre, email, contrasena, prestamos_activos,
            id_entidad, fecha_creacion
        )
        self.nivel_acceso = nivel_acceso

    def puede_pedir_prestado(self) -> bool:
        """El administrador puede pedir prestado."""
        return True

    def calcular_multa(self, dias_retraso: int) -> float:
        """Admin no paga multa."""
        return 0.0

    def __str__(self) -> str:
        """Representación legible."""
        return f"Administrador: {self.nombre} ({self.nivel_acceso})"

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        data = super().to_dict()
        data.update({"nivel_acceso": self.nivel_acceso})
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Administrador":
        """Crea administrador desde diccionario."""
        return cls(
            data["nombre"], data["email"], data["contrasena"],
            data["nivel_acceso"],
            int(data.get("prestamos_activos", 0)),
            data.get("id"), data.get("fecha_creacion")
        )
