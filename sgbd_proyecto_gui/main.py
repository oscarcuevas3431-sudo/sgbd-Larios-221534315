"""Punto de entrada del Sistema de Gestión de Biblioteca Digital."""

from modelos.catalogo import Catalogo
from modelos.libro import Libro, LibroDigital, LibroFisico
from modelos.usuario import Administrador, Alumno, Profesor
from servicios.gestor_cola import GestorCola
from servicios.historial import Historial

RUTA_DATOS = "datos/biblioteca.json"


def seed_data(catalogo: Catalogo) -> None:
    """Inserta datos de prueba si el catálogo está vacío."""
    if catalogo.libros or catalogo.usuarios:
        return

    libros = [
        Libro(
            "Python Básico", "Ana López", "9780306406157", 2022,
            "programacion"
        ),
        LibroFisico(
            "Clean Code", "Robert Martin", "9780132350884", 2008,
            "programacion", "Estante A-1", 2
        ),
        LibroDigital(
            "Aprende SQL", "Luis Pérez", "9783161484100", 2021,
            "educativo", "PDF", 5.4, "https://ejemplo.com/sql.pdf"
        ),
        Libro(
            "Historia Universal", "María Ruiz", "9788437604947", 2019,
            "historia"
        ),
        LibroFisico(
            "El Principito", "Antoine de Saint-Exupéry", "9780156012195",
            1943, "novela", "Estante B-2", 3
        ),
    ]

    usuarios = [
        Alumno(
            "Sofía García", "sofia@udg.mx", "1234",
            "Ingeniería", 2, "A123"
        ),
        Profesor(
            "Carlos Méndez", "carlos@udg.mx", "1234",
            "Programación"
        ),
        Administrador(
            "Admin Principal", "admin@udg.mx", "1234",
            "total"
        ),
    ]

    for libro in libros:
        catalogo.agregar_libro(libro)

    for usuario in usuarios:
        catalogo.registrar_usuario(usuario)

    catalogo.registrar_prestamo("sofia@udg.mx", "9780306406157")
    catalogo.registrar_prestamo("carlos@udg.mx", "9780132350884")


def mostrar_menu() -> None:
    """Muestra opciones del menú."""
    print("\n=== SISTEMA DE BIBLIOTECA DIGITAL ===")
    print("[1] Agregar libro")
    print("[2] Buscar libro")
    print("[3] Registrar usuario")
    print("[4] Prestar libro")
    print("[5] Devolver libro")
    print("[6] Ver cola de espera")
    print("[7] Reportes")
    print("[0] Salir")


def agregar_libro_menu(catalogo: Catalogo) -> None:
    """Agrega un libro desde consola."""
    titulo = input("Título: ")
    autor = input("Autor: ")
    isbn = input("ISBN-13: ")
    anio = int(input("Año: "))
    genero = input("Género: ")

    libro = Libro(titulo, autor, isbn, anio, genero)
    catalogo.agregar_libro(libro)
    print("Libro agregado correctamente.")


def registrar_usuario_menu(catalogo: Catalogo) -> None:
    """Registra un usuario desde consola."""
    print("Tipo: 1 Alumno | 2 Profesor | 3 Admin")
    tipo = input("Opción: ")
    nombre = input("Nombre: ")
    email = input("Email: ")
    contrasena = input("Contraseña: ")

    match tipo:
        case "1":
            carrera = input("Carrera: ")
            semestre = int(input("Semestre: "))
            matricula = input("Matrícula: ")
            usuario = Alumno(
                nombre, email, contrasena, carrera, semestre, matricula
            )
        case "2":
            departamento = input("Departamento: ")
            usuario = Profesor(nombre, email, contrasena, departamento)
        case "3":
            nivel = input("Nivel de acceso: ")
            usuario = Administrador(nombre, email, contrasena, nivel)
        case _:
            raise ValueError("Tipo de usuario inválido.")

    catalogo.registrar_usuario(usuario)
    print("Usuario registrado correctamente.")


def main() -> None:
    """Ejecuta el programa principal."""
    catalogo = Catalogo()
    cola = GestorCola()
    historial = Historial()

    try:
        catalogo.cargar_json(RUTA_DATOS)
        print("Datos cargados correctamente.")
    except FileNotFoundError:
        print("No había datos guardados. Se crearán datos demo.")
        seed_data(catalogo)

    while True:
        try:
            mostrar_menu()
            opcion = input("Elige una opción: ").strip()

            match opcion:
                case "1":
                    agregar_libro_menu(catalogo)
                    historial.registrar("Se agregó un libro.")

                case "2":
                    query = input("Buscar: ")
                    resultados = catalogo.buscar(query)
                    if not resultados:
                        print("No se encontraron libros.")
                    for libro in resultados:
                        print(libro)

                case "3":
                    registrar_usuario_menu(catalogo)
                    historial.registrar("Se registró un usuario.")

                case "4":
                    email = input("Email del usuario: ").strip().lower()
                    isbn = input("ISBN del libro: ").strip()
                    try:
                        prestamo = catalogo.registrar_prestamo(email, isbn)
                        print(f"Préstamo registrado: {prestamo}")
                    except ValueError as error:
                        print(error)
                        cola.encolar_solicitud(email, isbn)
                        print("Solicitud enviada a cola de espera.")

                case "5":
                    email = input("Email del usuario: ").strip().lower()
                    isbn = input("ISBN del libro: ").strip()
                    dias = int(input("Días de retraso: "))
                    prestamo = catalogo.procesar_devolucion(email, isbn, dias)
                    print(f"Devolución procesada. Multa: ${prestamo.multa}")

                case "6":
                    print("Cola de espera:")
                    for solicitud in cola.ver_cola():
                        print(solicitud)

                case "7":
                    print(catalogo.generar_reporte())
                    print("Historial:", historial.ver_historial())

                case "0":
                    catalogo.guardar_json(RUTA_DATOS)
                    print("Datos guardados. Bye.")
                    break

                case _:
                    print("Opción no válida.")

        except ValueError as error:
            print(f"Error de valor: {error}")
        except KeyError as error:
            print(f"No encontrado: {error}")
        except Exception as error:
            print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()
