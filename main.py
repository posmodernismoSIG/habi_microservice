'''Punto de entrada del microservicio, funcion inicial que arranca todos los servicios
    python main - arranca microservicio
    python main test - ejecuta los test
'''
import sys 
from config import setup_logging
from presentation import PropertyMicroservice
def run_test():
    pass
def run_microservice():
    setup_logging()
    microservice = PropertyMicroservice()
    microservice.start()

def main():
    '''funcion principal'''
    if len(sys.argv) > 1 and sys.argv == 'test':
        run_test()
    else:
        run_microservice()


if __name__ == "__main__":
    main()
    
    