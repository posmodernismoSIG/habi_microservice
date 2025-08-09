'''
Pruebas unitarias para la capa de dominio.
'''

import unittest
from domain import Property, PropertyFilter, PropertyStatus


class TestPropertyFilter(unittest.TestCase):
    '''Pruebas para la clase PropertyFilter.'''
    
    def test_has_filters_when_empty(self):
        '''Test cuando no hay filtros aplicados.'''
        filter_obj = PropertyFilter()
        self.assertFalse(filter_obj.has_filters())
    
    def test_has_filters_when_has_year(self):
        '''Test cuando hay filtro de año.'''
        filter_obj = PropertyFilter(year=2020)
        self.assertTrue(filter_obj.has_filters())
    
    def test_has_filters_when_has_city(self):
        '''Test cuando hay filtro de ciudad.'''
        filter_obj = PropertyFilter(city='bogota')
        self.assertTrue(filter_obj.has_filters())
    
    def test_has_filters_when_has_state(self):
        '''Test cuando hay filtro de estado.'''
        filter_obj = PropertyFilter(state=PropertyStatus.EN_VENTA)
        self.assertTrue(filter_obj.has_filters())


class TestProperty(unittest.TestCase):
    '''Pruebas para la entidad Property.'''
    
    def test_property_creation(self):
        '''Test creación de propiedad.'''
        prop = Property(
            id=1,
            address='Calle 123',
            city='Bogotá', 
            state=PropertyStatus.EN_VENTA,
            price=150000000,
            description='Casa hermosa',
            year=2020
        )
        self.assertEqual(prop.id, 1)
        self.assertEqual(prop.address, 'Calle 123')
        self.assertEqual(prop.state, PropertyStatus.EN_VENTA)
        self.assertEqual(prop.price, 150000000)
    
    def test_property_to_dict(self):
        '''Test conversión de propiedad a diccionario.'''
        prop = Property(
            id=1,
            address='Calle 123',
            city='Bogotá',
            state=PropertyStatus.EN_VENTA,
            price=150000000,
            description='Casa hermosa',
            year=2020
        )
        
        expected = {
            'id': 1,
            'address': 'Calle 123',
            'city': 'Bogotá',
            'state': 'en_venta',
            'price': 150000000,
            'description': 'Casa hermosa',
            'year': 2020
        }
        
        self.assertEqual(prop.to_dict(), expected)
    
    def test_property_with_none_values(self):
        '''Test propiedad con valores None.'''
        prop = Property(
            id=1,
            address='Calle 123',
            city='Bogotá',
            state=PropertyStatus.EN_VENTA,
            price=150000000,
            description=None,
            year=None
        )
        
        result = prop.to_dict()
        self.assertIsNone(result['description'])
        self.assertIsNone(result['year'])


class TestPropertyStatus(unittest.TestCase):
    '''Pruebas para el enum PropertyStatus.'''
    
    def test_status_values(self):
        '''Test valores del enum.'''
        self.assertEqual(PropertyStatus.PRE_VENTA.value, 'pre_venta')
        self.assertEqual(PropertyStatus.EN_VENTA.value, 'en_venta')
        self.assertEqual(PropertyStatus.VENDIDO.value, 'vendido')
    
    def test_status_from_string(self):
        '''Test creación de status desde string.'''
        status = PropertyStatus('en_venta')
        self.assertEqual(status, PropertyStatus.EN_VENTA)
    
    def test_invalid_status_raises_error(self):
        '''Test que status inválido levanta error.'''
        with self.assertRaises(ValueError):
            PropertyStatus('estado_invalido')


if __name__ == '__main__':
    unittest.main()