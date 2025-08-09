'''
Configuración del microservicio.
'''
import os
from dotenv import load_dotenv
import logging
load_dotenv()

class DatabaseConfig:
    '''Configuración de base de datos.'''
    HOST = os.getenv('DB_HOST')
    PORT = int(os.getenv('DB_PORT'))
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE = os.getenv('DB_DATABASE')


class ServerConfig:
    '''Configuración del servidor HTTP.'''
    HOST =  os.getenv('SERVER_HOST')
    PORT =  int(os.getenv('SERVER_PORT'))
    


def setup_logging():
    '''Configura el sistema de logging.'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )