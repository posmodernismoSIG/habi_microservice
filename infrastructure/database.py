''' Manejo de conexiones con bases de datos'''

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import logging 
from config import DatabaseConfig

class DatabaseConnect:
    '''Entidad de conexion a la base de datos 
    Implementar SinlgeTone para asegurarse de que solo se haga una conexion a la vez'''
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @contextmanager
    def get_connection(self):
        '''Funcion de conexion con el decorador `@contextmanager` actúa como un envoltorio que gestiona automáticamente la apertura y cierre de recursos '''
        connection = False
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE
            )
            yield connection
        except Error as e:
            logging.error(f"Error de conexión a la base de datos: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
        
