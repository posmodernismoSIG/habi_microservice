"""
Servicios de aplicación para inmuebles.
"""

from typing import List
import logging

from domain import Property, PropertyFilter
from infrastructure import PropertyRepositoryInterface
from datetime import datetime

class PropertyService:
    """
    Servicio de aplicación para inmuebles.
    Encapsula la lógica de negocio y coordina entre capas.
    """
    
    def __init__(self, property_repository: PropertyRepositoryInterface):
        self.property_repository = property_repository
    
    def get_available_properties(self, filters: PropertyFilter) -> List[Property]:
        """
        Obtiene inmuebles disponibles aplicando filtros.
        Valida filtros y maneja excepciones.
        """
        self._validate_filters(filters)
        
        try:
            properties = self.property_repository.find_available_properties(filters)
            logging.info(f"Se encontraron {len(properties)} inmuebles")
            return properties
            
        except Exception as e:
            logging.error(f"Error en servicio de inmuebles: {e}")
            raise
    
    def _validate_filters(self, filters: PropertyFilter) -> None:
        """Valida los filtros de entrada."""
        if filters.year is not None:
            current_year = datetime.now().year
            
            if filters.year < 1800 or filters.year > current_year:
                raise ValueError(f"El año debe estar entre 1800 y {current_year}")
            
        if filters.city is not None and len(filters.city.strip()) == 0:
            raise ValueError("La ciudad no puede estar vacía")