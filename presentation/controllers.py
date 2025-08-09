'''
Controladores HTTP para manejo de requests.
'''

from typing import Dict, List, Any
import logging

from domain import PropertyFilter, PropertyState
from application import PropertyService


class PropertyController:
    '''
    Controlador para manejo de requests HTTP de inmuebles.
    Responsabilidad única: manejo de la capa de presentación.
    '''
    
    def __init__(self, property_service: PropertyService):
        self.property_service = property_service
    
    def get_properties(self, query_params: Dict[str, List[str]]) -> Dict[str, Any]:
        '''Maneja GET /properties con parámetros de consulta.'''
        try:
            filters = self._parse_filters(query_params)
            properties = self.property_service.get_available_properties(filters)
            
            return {
                'success': True,
                'data': [prop.serializer() for prop in properties],
                'count': len(properties)
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            logging.error(f'Error en controlador: {e}')
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR'
            }
    
    def _parse_filters(self, query_params: Dict[str, List[str]]) -> PropertyFilter:
        '''Parsea los parámetros de consulta a filtros.'''
        year = None
        if 'year' in query_params and query_params['year']:
            try:
                year = int(query_params['year'][0])
            except ValueError:
                raise ValueError('El año debe ser un número entero')
        
        city = None
        if 'city' in query_params and query_params['city']:
            city = query_params['city'][0].strip()
        
        state = None
        if 'state' in query_params and query_params['state']:
            state_value = query_params['state'][0].strip()
            try:
                state = PropertyState(state_value)
            except ValueError:
                valid_states = [s.value for s in PropertyState]
                raise ValueError(f'Estado inválido. Estados válidos: {valid_states}')
        
        return PropertyFilter(year=year, city=city, state=state)