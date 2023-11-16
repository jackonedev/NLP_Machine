import time
# import wrapper
from functools import wraps, partial


def cronometro(func):
    """Decorador para contabilizar el tiempo de ejecución de una función"""

    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        final_time = round(time_end - time_start, 2)
        print(f"Tiempo de ejecución de {func.__name__}: {final_time} seg")
        return result

    return wrapper




def soy_una_funcion(a, b="Hola"):
    return True
# abstraerme de los parámetros
lista = [soy_una_funcion, "Hola Mundo!"]
print( f"Soy {lista[0].__name__} ejecutada con a = 1 {lista[0](1)}" )





## La forma 1 on 1

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Estoy dentro del decorador")
        res = func(*args, **kwargs)
        return res

    return wrapper

@decorator
def func_2(a,b):
    return f"los {a} estan {b}"

print("Imprimiendo ejemplo 1 de decorador:\n")
# print(decorator(func_2))
print(func_2("valores","hardcodeados"))


