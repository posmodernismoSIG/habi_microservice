'''Punto de entrada del microservicio, funcion inicial que arranca todos los servicios
    python main - arranca microservicio
    python main test - ejecuta los test
'''
import sys 
from config import setup_logging
from presentation import PropertyMicroservice
import unittest


def run_test():
    '''Ejecutas las pruebas unitarias de test/'''
    print('🧪 Ejecutando pruebas unitarias...')
    
    # Descubrir y ejecutar tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    if result.wasSuccessful():
        print('✅ Todas las pruebas pasaron!')
    else:
        print('❌ Algunas pruebas fallaron')
        print(f'Errores: {len(result.errors)}')
        print(f'Fallos: {len(result.failures)}')
        
        
    pass
def run_microservice():
    setup_logging()
    microservice = PropertyMicroservice()
    microservice.start()

def main():
    '''funcion principal'''
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_test()
    else:
        run_microservice()


if __name__ == '__main__':
    main()
    
    