# PRUEBA TÉCNICA JOAN SEBASTIAN DIAZ G. - Microservicio de Inmuebles Habi

##  1. Análisis Inicial del Requerimiento

**Objetivo:** Desarrollar un microservicio que permita consultar inmuebles disponibles para la venta con capacidad de filtrado.


---

## 2. Tecnologías Seleccionadas

### Lenguaje Base
- **Python 3.10* 
  - *Planeo usar Python como lenguage, por que tiene una Sintaxis clara, es excelente para desarrollo rápido, tiene un amplio ecosistema y es el lenguage que mas he usado

### Base de Datos
- **MySQL** 
  - *El sistema ya existente en Habi, y fue el insumo para la prueba

### Dependencias
- **mysql-connector-python**: Para una conexión directa sin ORM para control total
- **python-dotenv**: Para una gestión segura de configuraciones, y protección de información sensible
- **Sin frameworks web externos**: Usar `http.server` nativo para demostrar conocimientos fundamentales

--

## 3. Arquitectura Planificada

### Patrón Arquitectónico: **Arquitectura Hexagonal** dividdo en 4 capas con responsabilidades separadas, siguiendo principios SOLID

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION                          │
│  HTTP Handlers, Controllers, Request/Response parsing   │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                   APPLICATION                           │
│     Services, Business Logic, Use Cases                 │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE                         │
│    Repositories, Database, External Services            │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                     DOMAIN                              │
│       Entities, Value Objects, Business Rules           │
└─────────────────────────────────────────────────────────┘
```

### 4. Justificación de la Arquitectura
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Testabilidad**: Dependencias invertidas permiten mocking fácil
- **Mantenibilidad**: Cambios en una capa no afectan otras
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

--

## 5. Principios SOLID - Aplicación Planificada

### **S - Single Responsibility**
- `PropertyController`: Solo manejo HTTP
- `PropertyService`: Solo lógica de negocio  
- `PropertyRepository`: Solo acceso a datos
- `Property`: Solo representación de inmueble

### **O - Open/Closed**
- Nuevos filtros extenderán `PropertyFilter`
- Nuevos repositorios implementarán `PropertyRepositoryInterface`

### **L - Liskov Substitution**
- Cualquier implementación de `PropertyRepositoryInterface` será intercambiable

### **I - Interface Segregation**
- Interfaces específicas y cohesivas (no métodos innecesarios)

### **D - Dependency Inversion**
- Services dependen de abstracciones, no implementaciones concretas
- Inyección de dependencias manual en el microservicio

--


## 6. Estrategia de Testing

### Cobertura Planificada
- **Domain Layer**: Tests de entidades y value objects
- **Application Layer**: Tests de servicios con mocking
- **Presentation Layer**: Tests de controladores y parsing
- **Integration**: Tests end-to-end mínimos

### Herramientas
- `unittest` (estándar de Python)
- `unittest.mock` para dependencias


## 7. Configuración del Entorno

### Variables de Entorno Requeridas
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=habi_user
DB_PASSWORD=secure_password
DB_DATABASE=habi_db

# Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```


---
## 9. Query SQL 
```bash

SELECT 
    p.id, p.address, p.city, p.price, p.description, p.year,
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
```
adicionando a la Capsula WHERE los filtros adicionales

```bash
  AND p.year = %s 
  AND LOWER(p.city) = LOWER(%s) 
  AND s.name = %s

```
--


# Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio

```bash
git clone https://github.com/posmodernismoSIG/habi_microservice/
cd habi_microservice
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Editar .env con tus credenciales
nano .env
```

Configurar las siguientes variables en `.env`:

```env
# Base de datos
DB_HOST=tu_host_mysql
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_DATABASE=habi_db

# Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Aplicación
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 5. Ejecutar el microservicio

```bash
python main.py
```

### 6. Ejecutar pruebas (opcional)

```bash
python main.py test
```

---


# SEGUNDO PUNTO - REQUERIMIENTO CONCEPTUAL DE SERVICIO DE "ME GUSTA" 
## 2.1 Modelamiento DB

Para implementar el sistema de “me gusta”, yo personalmente optaría por crear dos tablas nuevas que trabajen en conjunto: una para registrar los likes y otra para almacenar un cache de rankings, evitando sobrecargar el sistema con consultas costosas.

La primera tabla sería property_likes, que funciona como tabla de unión entre usuarios y propiedades. Aquí registraría qué usuario dio “me gusta” a qué propiedad, cuándo lo hizo y, mediante una restricción única, impediría que un mismo usuario pueda dar más de un “like” a la misma propiedad. También establecería claves foráneas con ON DELETE CASCADE para que, si se elimina un usuario o una propiedad, sus registros asociados se eliminen automáticamente.

La segunda tabla sería property_ranking_cache, pensada como un sistema de cache que almacena el total de likes y la posición en el ranking de cada propiedad. De esta forma, se evitaría tener que recalcular los conteos y rankings en cada consulta, mejorando significativamente el rendimiento. Esta tabla tendría una relación 1:1 con la tabla de propiedades, y se actualizaría cada vez que un like es añadido o eliminado.

El SQL para crear estas tablas sería el siguiente:

```bash

-- 1️⃣ TABLA PRINCIPAL: property_likes
CREATE TABLE property_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Un usuario solo puede dar un like por propiedad
    UNIQUE KEY uk_user_property (user_id, property_id),
    
    -- Relaciones con tablas existentes
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- 2️⃣ TABLA DE CACHE: property_ranking_cache
CREATE TABLE property_ranking_cache (
    property_id INT PRIMARY KEY,
    total_likes INT DEFAULT 0,
    ranking_position INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Relación con tabla existente
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

```
Relaciones entre tablas:

### property_likes

user_id → auth_user(id): un usuario puede dar muchos likes (relación 1:N).
property_id → property(id): una propiedad puede recibir muchos likes (relación 1:N).
Restricción única UNIQUE(user_id, property_id) para impedir likes duplicados del mismo usuario.

### property_ranking_cache

property_id → property(id): una propiedad tiene un único registro de ranking (relación 1:1).

En resumen, property_likes registra los likes, guarda cuándo se dieron y evita duplicados, y property_ranking_cache almacena la cantidad total de likes, mantiene la posición en el ranking y acelera las consultas evitando contar cada vez. Con estas dos tablas se obtiene un sistema completo de “me gusta” y rankings sin modificar ninguna tabla existente, manteniendo integridad, rendimiento y escalabilidad.

# 2.2 Modelos Entidad - Relación

## Modelo Actual
--
<img width="1012" height="616" alt="image" src="https://github.com/user-attachments/assets/c33dc99e-5124-4901-a1cd-a21cbdfd942a" />

## Modelo con las tablas adicionales para agregar logica de Likes 
--
<img width="1207" height="483" alt="image" src="https://github.com/user-attachments/assets/811d835f-6333-45dd-bb95-0eada39d7930" />

---
## 2.2 Modelamiento Micro Servicio 


Para llevar a cabo la implementación del endpoint de “like” en el microservicio, decidí estructurar el trabajo en cuatro pasos, uno por cada capa de la arquitectura, asegurando así mantener la separación de responsabilidades y un código limpio y escalable.

### Paso 1: Domain Layer
En el dominio, mi objetivo fue representar el “like” como una entidad inmutable y exponerla junto al resto de objetos de negocio.

```bash 
# domain/entities.py - AGREGAR al final
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PropertyLike:
    id: int
    user_id: int  
    property_id: int
    created_at: datetime

```
Luego, la exporté para que estuviera disponible en el resto de la aplicación:

```bash 
# domain/__init__.py - MODIFICAR
from .entities import Property, PropertyLike
from .value_objects import PropertyState, PropertyFilter

__all__ = ['Property', 'PropertyLike', 'PropertyState', 'PropertyFilter']
```

### Paso 2: Infrastructure Layer
En esta capa, extendí la interfaz del repositorio para soportar operaciones de “like”, “unlike” y verificación de si un usuario ya dio “like” a una propiedad.
```bash 
# infrastructure/repository.py - AGREGAR métodos
class PropertyRepositoryInterface(ABC):
    @abstractmethod
    def add_like(self, user_id: int, property_id: int) -> PropertyLike:
        pass
    
    @abstractmethod
    def remove_like(self, user_id: int, property_id: int) -> bool:
        pass
    
    @abstractmethod
    def user_has_liked(self, user_id: int, property_id: int) -> bool:
        pass

```
Después implementé estos métodos en MySQLPropertyRepository:

```bash 
# infrastructure/repository.py - AGREGAR en MySQLPropertyRepository
def add_like(self, user_id: int, property_id: int) -> PropertyLike:
    query = "INSERT INTO property_likes (user_id, property_id) VALUES (%s, %s)"
    with self.db_connection.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, property_id))
        like_id = cursor.lastrowid
        connection.commit()
        return PropertyLike(like_id, user_id, property_id, datetime.now())

def remove_like(self, user_id: int, property_id: int) -> bool:
    query = "DELETE FROM property_likes WHERE user_id = %s AND property_id = %s"
    with self.db_connection.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, property_id))
        connection.commit()
        return cursor.rowcount > 0

def user_has_liked(self, user_id: int, property_id: int) -> bool:
    query = "SELECT 1 FROM property_likes WHERE user_id = %s AND property_id = %s"
    with self.db_connection.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, property_id))
        return cursor.fetchone() is not None

```


### Paso 3: Application Layer
Aquí creé un nuevo servicio que encapsula la lógica de alternar entre “like” y “unlike”, de manera que la capa de presentación no tenga que preocuparse por la implementación interna.

```bash 
# application/services.py - AGREGAR nueva clase
class PropertyLikeService:
    def __init__(self, property_repository: PropertyRepositoryInterface):
        self.property_repository = property_repository
    
    def toggle_like(self, user_id: int, property_id: int) -> Dict[str, Any]:
        try:
            has_liked = self.property_repository.user_has_liked(user_id, property_id)
            
            if has_liked:
                self.property_repository.remove_like(user_id, property_id)
                action = "unliked"
            else:
                self.property_repository.add_like(user_id, property_id)
                action = "liked"
            
            return {
                'success': True,
                'action': action
            }
        except Exception as e:
            logging.error(f'Error en toggle like: {e}')
            raise

```


Luego lo exporté para poder inyectarlo donde fuera necesario:

```bash 
# application/__init__.py - MODIFICAR
from .services import PropertyService, PropertyLikeService

__all__ = ['PropertyService', 'PropertyLikeService']

```

Paso 4: Presentation Layer
Por último, añadí la integración con el controlador y el handler HTTP para exponer el endpoint al exterior.

```bash 
# presentation/controllers.py - AGREGAR método
class PropertyController:
    def __init__(self, property_service: PropertyService, like_service: PropertyLikeService):
        self.property_service = property_service
        self.like_service = like_service
    
    def post_property_like(self, property_id: int, user_id: int) -> Dict[str, Any]:
        try:
            result = self.like_service.toggle_like(user_id, property_id)
            return result
        except Exception as e:
            logging.error(f'Error en controlador like: {e}')
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR'


# presentation/handlers.py - MODIFICAR do_POST
class PropertyHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_url = urlparse(self.path)
        
        # Nuevo endpoint: POST /properties/{id}/like
        if parsed_url.path.startswith('/properties/') and parsed_url.path.endswith('/like'):
            property_id = int(parsed_url.path.split('/')[2])
            # TODO: Extraer user_id del token de autorización
            user_id = 1  # Placeholder - implementar auth real
            response = self.server.property_controller.post_property_like(property_id, user_id)
            self._send_json_response(response)
        else:
            self._send_error_response(404, 'Endpoint no encontrado')

```

Finalmente, inyecté las dependencias necesarias en el microservicio:

```bash 
# presentation/handlers.py - MODIFICAR PropertyMicroservice
class PropertyMicroservice:
    def __init__(self, host: str = None, port: int = None):
        # ... código existente ...
        
        # Nueva inyección de dependencia
        self.like_service = PropertyLikeService(self.property_repository)
        self.property_controller = PropertyController(self.property_service, self.like_service)

```


Con estos cuatro pasos, el endpoint POST /properties/{id}/like queda completamente funcional, gestionando altas y bajas de “likes” con consistencia en todas las capas, manteniendo un diseño limpio y fácil de extender.



