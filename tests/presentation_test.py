'''
Pruebas unitarias para la capa de presentación.
'''

import unittest
from unittest.mock import Mock

from domain import Property, PropertyFilter, PropertyStatus
from application import PropertyService
from presentation import PropertyController


class TestPropertyController(unittest.TestCase):
    '''Pruebas para PropertyController.'''
    
    def setUp(self):
        '''Configuración previa a cada test.'''
        self.mock_service = Mock(spec=PropertyService)
        self.controller = PropertyController(self.mock_service)
    
    def test_get_properties_success(self):
        '''Test obtener propiedades exitosamente.'''
        # Arrange
        mock_property = Property(
            id=1, 
            address='Test Address', 
            city='Test City',
            state=PropertyStatus.EN_VENTA, 
            price=100000,
            description=None, 
            year=2020
        )
        self.mock_service.get_available_properties.return_value = [mock_property]
        
        # Act
        query_params = {'year': ['2020'], 'city': ['bogota']}
        result = self.controller.get_properties(query_params)
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['id'], 1)
        self.assertEqual(result['data'][0]['year'], 2020)
    
    def test_get_properties_empty_result(self):
        '''Test cuando no hay propiedades.'''
        # Arrange
        self.mock_service.get_available_properties.return_value = []
        
        # Act
        query_params = {'city': ['ciudad_inexistente']}
        result = self.controller.get_properties(query_params)
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['data']), 0)
    
    def test_get_properties_invalid_year(self):
        '''Test con año inválido.'''
        query_params = {'year': ['invalid_year']}
        result = self.controller.get_properties(query_params)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], 'VALIDATION_ERROR')
        self.assertIn('número entero', result['error'])
    
    def test_get_properties_invalid_state(self):
        '''Test con estado inválido.'''
        query_params = {'state': ['estado_invalido']}
        result = self.controller.get_properties(query_params)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], 'VALIDATION_ERROR')
        self.assertIn('Estado inválido', result['error'])
    
    def test_get_properties_service_error(self):
        '''Test cuando el servicio lanza excepción.'''
        # Arrange
        self.mock_service.get_available_properties.side_effect = Exception('Service Error')
        
        # Act
        query_params = {}
        result = self.controller.get_properties(query_params)
        
        # Assert
        self.assertFalse(result['success'])
        self.assertEqual(result['code'], 'INTERNAL_ERROR')
        self.assertEqual(result['error'], 'Error interno del servidor')
    
    def test_parse_filters_all_params(self):
        '''Test parseo de todos los parámetros.'''
        query_params = {
            'year': ['2020'],
            'city': ['bogota'],
            'state': ['en_venta']
        }
        
        filters = self.controller._parse_filters(query_params)
        
        self.assertEqual(filters.year, 2020)
        self.assertEqual(filters.city, 'bogota')
        self.assertEqual(filters.state, PropertyStatus.EN_VENTA)
    
    def test_parse_filters_empty_params(self):
        '''Test parseo sin parámetros.'''
        query_params = {}
        
        filters = self.controller._parse_filters(query_params)
        
        self.assertIsNone(filters.year)
        self.assertIsNone(filters.city)
        self.assertIsNone(filters.state)
    
    def test_parse_filters_whitespace_city(self):
        '''Test parseo de ciudad con espacios.'''
        query_params = {'city': ['  bogota  ']}
        
        filters = self.controller._parse_filters(query_params)
        
        self.assertEqual(filters.city, 'bogota')
    
    def test_parse_filters_valid_states(self):
        '''Test parseo de todos los estados válidos.'''
        states = ['pre_venta', 'en_venta', 'vendido']
        expected_states = [PropertyStatus.PRE_VENTA, PropertyStatus.EN_VENTA, PropertyStatus.VENDIDO]
        
        for state_str, expected_state in zip(states, expected_states):
            query_params = {'state': [state_str]}
            filters = self.controller._parse_filters(query_params)
            self.assertEqual(filters.state, expected_state)


if __name__ == '__main__':
    unittest.main()