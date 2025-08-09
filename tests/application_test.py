'''
Pruebas unitarias para la capa de aplicación.
'''

import unittest
from unittest.mock import Mock

from domain import Property, PropertyFilter, PropertyStatus
from infrastructure import PropertyRepositoryInterface
from application import PropertyService


class TestPropertyService(unittest.TestCase):
    '''Pruebas para PropertyService.'''
    
    def setUp(self):
        '''Configuración previa a cada test.'''
        self.mock_repository = Mock(spec=PropertyRepositoryInterface)
        self.service = PropertyService(self.mock_repository)
    
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
        self.mock_repository.find_available_properties.return_value = [mock_property]
        
        # Act
        filters = PropertyFilter(year=2020)
        result = self.service.get_available_properties(filters)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].year, 2020)
        self.mock_repository.find_available_properties.assert_called_once_with(filters)
    
    def test_get_properties_empty_result(self):
        '''Test cuando no hay propiedades.'''
        # Arrange
        self.mock_repository.find_available_properties.return_value = []
        
        # Act
        filters = PropertyFilter(city='ciudad_inexistente')
        result = self.service.get_available_properties(filters)
        
        # Assert
        self.assertEqual(len(result), 0)
        self.mock_repository.find_available_properties.assert_called_once_with(filters)
    
    def test_validate_filters_invalid_year_low(self):
        '''Test validación de año muy bajo.'''
        filters = PropertyFilter(year=1500)
        
        with self.assertRaises(ValueError) as context:
            self.service.get_available_properties(filters)
        
        self.assertIn('año debe estar entre', str(context.exception))
    
    def test_validate_filters_invalid_year_high(self):
        '''Test validación de año muy alto.'''
        filters = PropertyFilter(year=2050)
        
        with self.assertRaises(ValueError) as context:
            self.service.get_available_properties(filters)
        
        self.assertIn('año debe estar entre', str(context.exception))
    
    def test_validate_filters_empty_city(self):
        '''Test validación de ciudad vacía.'''
        filters = PropertyFilter(city='   ')
        
        with self.assertRaises(ValueError) as context:
            self.service.get_available_properties(filters)
        
        self.assertIn('ciudad no puede estar vacía', str(context.exception))
    
    def test_validate_filters_valid_data(self):
        '''Test validación con datos válidos.'''
        # Arrange
        self.mock_repository.find_available_properties.return_value = []
        
        # Act & Assert - No debe lanzar excepción
        filters = PropertyFilter(year=2020, city='bogota', state=PropertyStatus.EN_VENTA)
        result = self.service.get_available_properties(filters)
        
        self.assertEqual(len(result), 0)
    
    def test_repository_exception_propagation(self):
        '''Test que las excepciones del repositorio se propagan.'''
        # Arrange
        self.mock_repository.find_available_properties.side_effect = RuntimeError('DB Error')
        
        # Act & Assert
        filters = PropertyFilter()
        with self.assertRaises(RuntimeError):
            self.service.get_available_properties(filters)


if __name__ == '__main__':
    unittest.main()