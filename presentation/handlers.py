'''
Handlers HTTP y servidor del microservicio.
'''

from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
import json

from .controllers import PropertyController
from application import PropertyService
from infrastructure import DatabaseConnect, MySQLPropertyRepository
from config import ServerConfig


class PropertyHTTPHandler(BaseHTTPRequestHandler):
    '''Handler HTTP que delega al controlador apropiado.'''
    
    def do_GET(self):
        '''Maneja requests GET.'''
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/properties':
            query_params = parse_qs(parsed_url.query)
            response = self.server.property_controller.get_properties(query_params)
            self._send_json_response(response)
        
        elif parsed_url.path == '/health':
            self._send_json_response({'status': 'healthy'})
        
        else:
            self._send_error_response(404, 'Endpoint no encontrado')
    
    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        '''Envía respuesta JSON.'''
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _send_error_response(self, status_code: int, message: str):
        '''Envía respuesta de error.'''
        self._send_json_response({
            'success': False,
            'error': message
        }, status_code)
    
    def log_message(self, format, *args):
        '''Suprime logs automáticos del servidor.'''
        pass


class PropertyMicroservice:
    '''
    Clase principal del microservicio.
    Ensambla todas las dependencias (Dependency Injection).
    '''
    
    def __init__(self, host: str = None, port: int = None):
        self.host = host or ServerConfig.HOST
        self.port = port or ServerConfig.PORT
        self.server = None
        
        # Dependency Injection - Ensamblado de dependencias
        self.db_connection = DatabaseConnect()
        self.property_repository = MySQLPropertyRepository(self.db_connection)
        self.property_service = PropertyService(self.property_repository)
        self.property_controller = PropertyController(self.property_service)
    
    def start(self):
        '''Inicia el servidor HTTP.'''
        self.server = HTTPServer((self.host, self.port), PropertyHTTPHandler)
        self.server.property_controller = self.property_controller
        
        print(f'🚀 Microservicio iniciado en http://{self.host}:{self.port}')
        print('📋 Endpoints disponibles:')
        print(f'  GET /properties - Consultar inmuebles')
        print(f'  GET /health - Estado del servicio')
        print('📖 Filtros disponibles: ?year=2020&city=bogota&state=en_venta')
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print('\n🛑 Deteniendo servidor...')
            self.stop()
    
    def stop(self):
        '''Detiene el servidor.'''
        if self.server:
            self.server.shutdown()
            self.server.server_close()