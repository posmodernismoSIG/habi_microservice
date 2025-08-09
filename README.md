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

---

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

---

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

---


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

### Comandos de Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar microservicio
python main.py

# Ejecutar tests
python main.py test
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

