"""Repositorio para conectar con MongoDB y registrar bitácora de eventos."""

import os
try:
    from pymongo import MongoClient
    PYMONGO_DISPONIBLE = True
except ImportError:
    PYMONGO_DISPONIBLE = False

from models.evento import EventoSistema

# Ruta para el archivo de fallback si MongoDB no está disponible
FALLBACK_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "eventos_fallback.log")


class MongoRepository:
    """Clase para manejar el registro de eventos en MongoDB con fallback local."""

    def __init__(self, uri: str = "mongodb://localhost:27017/", db_name: str = "biblioteca_db"):
        self.conectado = False
        self.collection = None
        
        if PYMONGO_DISPONIBLE:
            try:
                # serverSelectionTimeoutMS corto (2s) para no congelar la app si Mongo está apagado
                self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
                # Forzar un ping para verificar si realmente está activo
                self.client.admin.command('ping')
                self.db = self.client[db_name]
                self.collection = self.db["eventos"]
                self.conectado = True
            except Exception as e:
                print(f"Advertencia: No se pudo conectar a MongoDB. Usando fallback local. Error: {e}")
                self.conectado = False
        else:
            print("Advertencia: 'pymongo' no está instalado. Usando fallback local.")

        # Asegurar que la carpeta 'data' exista
        os.makedirs(os.path.dirname(FALLBACK_LOG_PATH), exist_ok=True)

    def registrar_evento(self, evento: EventoSistema) -> None:
        """Guarda el evento en MongoDB o en un archivo log si no hay conexión."""
        if self.conectado and self.collection is not None:
            try:
                result = self.collection.insert_one(evento.to_dict())
                evento.id = str(result.inserted_id)
                return
            except Exception as e:
                print(f"Error al escribir en MongoDB ({e}). Cambiando a fallback local.")
                self.conectado = False
                
        # Fallback a archivo de texto
        self._registrar_fallback(evento)

    def _registrar_fallback(self, evento: EventoSistema) -> None:
        """Escribe el evento en un archivo plano."""
        try:
            with open(FALLBACK_LOG_PATH, "a", encoding="utf-8") as f:
                log_line = f"[{evento.fecha_hora}] [{evento.modulo}] {evento.tipo_evento}: {evento.descripcion}\n"
                f.write(log_line)
        except Exception as e:
            print(f"Error crítico: No se pudo registrar la bitácora: {e}")
