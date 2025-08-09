'''Repositorio de conexion a la base de datos'''

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
from mysql.connector import Error

from domain import Property, PropertyFilter, PropertyState
from .database import DatabaseConnect


class PropertyRepositoryInterface(ABC):
    '''Interfaz para el repositorio de inmuebles (Dependency Inversion).'''
    
    @abstractmethod
    def find_available_properties(self, filters: PropertyFilter) -> List[Property]:
        '''Encuentra inmuebles disponibles aplicando filtros.'''
        pass


class MySQLPropertyRepository(PropertyRepositoryInterface):
    '''
    Implementación del repositorio para MySQL.
    Responsabilidad única: acceso a datos de inmuebles.
    '''
    
    def __init__(self, db_connection: DatabaseConnect):
        self.db_connection = db_connection
        
    def find_available_properties(self, filters: PropertyFilter) -> List[Property]:
        '''
        Encuentra inmuebles disponibles con el último estado válido.
        Solo retorna inmuebles con estados: pre_venta, en_venta, vendido.
        '''
        query = self._build_query(filters)
        params = self._build_params(filters)
        
        try:
            with self.db_connection.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                results = cursor.fetchall()
                cursor.close()
                
                return [self._map_to_property(row) for row in results]
                
        except Error as e:
            logging.error(f'Error al consultar inmuebles: {e}')
            raise RuntimeError(f'Error al consultar inmuebles: {e}')
    
    def _build_query(self, filters: PropertyFilter) -> str:
        '''Construye la consulta SQL con subconsulta para obtener el último estado.'''
        base_query = """
        SELECT 
            p.id,
            p.address,
            p.city,
            p.price,
            p.description,
            p.year,
            s.name as status_name
        FROM property p
        INNER JOIN (
            SELECT 
                property_id,
                status_id,
                ROW_NUMBER() OVER (PARTITION BY property_id ORDER BY update_date DESC) as rn
            FROM status_history
        ) latest_status ON p.id = latest_status.property_id AND latest_status.rn = 1
        INNER JOIN status s ON latest_status.status_id = s.id
        WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')
        """
        
        conditions = []
        
        if filters.year is not None:
            conditions.append('p.year = %s')
            
        if filters.city is not None:
            conditions.append('LOWER(p.city) = LOWER(%s)')
            
        if filters.state is not None:
            conditions.append('s.name = %s')
        
        if conditions:
            base_query += ' AND ' + ' AND '.join(conditions)
            
        base_query += ' ORDER BY p.id'
        
        return base_query
    
    def _build_params(self, filters: PropertyFilter) -> tuple:
        '''Construye los parámetros para la consulta.'''
        params = []
        
        if filters.year is not None:
            params.append(filters.year)
            
        if filters.city is not None:
            params.append(filters.city)
            
        if filters.state is not None:
            params.append(filters.state.value)
            
        return tuple(params)
    
    def _map_to_property(self, row: Dict[str, Any]) -> Property:
        '''Mapea una fila de la BD a una entidad Property.'''
        try:
            status = PropertyState(row['status_name'])
        except ValueError:
            # Manejo de inconsistencias en los datos
            logging.warning(f'Estado inválido encontrado: {row['status_name']} para propiedad {row['id']}')
            raise ValueError(f'Estado inválido: {row['status_name']}')
            
        return Property(
            id=row['id'],
            address=row['address'] or '',
            city=row['city'] or '',
            state=status,
            price=row['price'] or 0,
            description=row['description'],
            year=row['year']
        )