import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


from app.main.main import tokenizador_i
from tools.feed import crear_directorio, procesar_file_csv
#import tools

def main(verbose = True):
    print("Ejecutando tokenizadores/main.py\n")
    resources = tokenizador_i()
    feed = resources["main_feed"]
    
    file_name = input("> nombre archivo: ")
    if not file_name:
        print("Ejecución interrumpida de forma segura.")
        exit()

    nombre, archivo = procesar_file_csv(file_name)
    
    df = feed(archivo)
    return df, nombre
    


if __name__ == "__main__":
    df, nombre = main()
    df