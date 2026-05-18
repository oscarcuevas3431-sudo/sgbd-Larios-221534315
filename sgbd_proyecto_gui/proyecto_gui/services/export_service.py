"""Servicio para la exportación de datos a diferentes formatos."""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
from typing import List, Any

class ExportService:
    """Maneja la exportación del catálogo a formatos JSON y XML."""

    @staticmethod
    def exportar_a_json(libros: List[Any], ruta_archivo: str) -> str:
        """
        Exporta una lista de objetos Libro a un archivo JSON.
        Se añade un retardo simulado para forzar la asincronía visual con hilos.
        """
        time.sleep(2)  # Simular exportación masiva
        
        datos = []
        for libro in libros:
            datos.append({
                "id": libro.id,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "isbn": libro.isbn,
                "anio": libro.anio,
                "genero": libro.genero,
                "disponibilidad": libro.disponibilidad
            })
            
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            
        return f"Catálogo JSON exportado con éxito."

    @staticmethod
    def exportar_a_xml(libros: List[Any], ruta_archivo: str) -> str:
        """
        Exporta una lista de objetos Libro a un archivo XML.
        Se añade un retardo simulado para forzar la asincronía visual con hilos.
        """
        time.sleep(2)  # Simular exportación masiva
        
        root = ET.Element("catalogo")
        
        for libro in libros:
            libro_elem = ET.SubElement(root, "libro", id=str(libro.id))
            ET.SubElement(libro_elem, "titulo").text = str(libro.titulo)
            ET.SubElement(libro_elem, "autor").text = str(libro.autor)
            ET.SubElement(libro_elem, "isbn").text = str(libro.isbn)
            ET.SubElement(libro_elem, "anio").text = str(libro.anio)
            ET.SubElement(libro_elem, "genero").text = str(libro.genero)
            ET.SubElement(libro_elem, "disponibilidad").text = "Sí" if libro.disponibilidad else "No"
            
        # Formatear XML para que sea legible (pretty print)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(xmlstr)
            
        return f"Catálogo XML exportado con éxito."
