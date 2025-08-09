

"""
Entidades del dominio de inmuebles.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from .value_objects import PropertyState


@dataclass(frozen=True)
class Property:
    '''entidad inmutable que representa una propiedad de la base de datos, es inmutable para garantizar la integiradad de los datos'''
    id: int
    address : str
    city : str
    price : int
    state : PropertyState
    description : Optional[str] = None
    year : Optional[int] = None
    
    
    
    def serializer(self) -> Dict[str,any]:
        '''Serializa los datos de la entidad (los convierte a Diccionarios o Json)'''
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'state': self.state.value,
            'price': self.price,
            'description': self.description,
            'year': self.year
        }
        
        
        
    