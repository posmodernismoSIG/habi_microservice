"""
Configuración del microservicio.
"""

import logging


class DatabaseConfig:
    """Configuración de base de datos."""
    HOST = "13.58.82.14"
    PORT = 3309
    USER = "pruebas"
    PASSWORD = "VGbt3Day5R"
    DATABASE = "habi_db"


class ServerConfig:
    """Configuración del servidor HTTP."""
    HOST = "0.0.0.0"
    PORT = 8000


def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )