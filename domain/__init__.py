'''Definicion del folder como paquete y abreviacion de la importacion de las clases'''

from .entities import Property
from .value_objects import PropertyState, PropertyFilter
'''Exportacion de las clases'''
__all__ = ['Property', 'PropertyState', 'PropertyFilter']