'''Value Object para los filtros de los usuarios'''

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PropertyState(Enum):
    '''Estados por los que pueden consular los clientes'''
    PRE_VENTA = 'pre_venta'
    VENTA = 'en_venta'
    VENDIDO = 'vendido'
    

@dataclass
class PropertyFilter:
    '''Entidad que representa los filtros'''
    year : Optional [int] = None
    city : Optional [str] = None
    state : Optional [PropertyState] = None 
    
    def has_filter(self) -> bool:
        '''Describe si hay o no filtros aplicados'''
        return any([self.state is not None, self.city is not None, self.state is not None])
        
    