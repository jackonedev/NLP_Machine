## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle, ast
from pathlib import Path
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
sys.path.insert(0, project_root)


## Aplicaciones propias
from app.main.main import wordcloud
try:
    from app.word_cloud.main import limpieza_txt
    from app.word_cloud.schemas.config_mascara import WordCloudConfig
except:
    from main import limpieza_txt
    from schemas.config_mascara import WordCloudConfig

## Librerías propias
from tools.feed import procesar_file_csv, procesar_file_png



  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###
###  ###  ###  ###  ###  ###  PROGRAMA PRINCIPAL  ###  ###  ###  ###  ###  ###
  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###
"""Notas:
23/10: Se agrego hardcodeo para el color de las lineas de contorno y el color del contorno
        Lineas entre 325 y 340
"""  
  
## VARIABLES GENERALES
print("Cargando configuración...")
path_utils = os.path.join(project_root, "app", "word_cloud_utils")
resoruces = wordcloud()
remover_palabra = resoruces["wordcloud_remover_palabra"]
filtrado_palabras = resoruces["wordcloud_filtrado_palabras"]






#######################################################################################
#                       ###   MODULO DE CARGA DE DATOS   ###                          #
#######################################################################################

## USER INPUT
file_name = input("> nombre archivo: ").lower()
if not file_name:
    print("Ejecución interrumpida de forma segura.")
    exit()
    
nombre, archivo = procesar_file_csv(file_name) ## USAR: nombre para el formato de output de salida

# sistema, ingresar a la carpeta de outputs para buscar una carpeta con el nombre del archivo
output_dir = os.path.join(project_root , "output", nombre)

if os.path.isdir(output_dir):
    folders = os.listdir(output_dir)
else:
    print("No se encontró un output procesado para dicho archivo.")
    print("Ejecución interrumpida de forma segura.")
    exit()

folders = sorted(folders)
default = folders[-1]

# sistema, devolverle al usuario un listado de carpetas dentro del output del archivo
msg = """Elija una carpeta de salida: 
\t\t - {}

default: {}   (presione enter para seleccionar el default)
seleccionar carpeta: """

# usuario, tener por default el último archivo que se haya procesado 
# y solicitar al usuario una respuesta
user_input = input(msg.format("\n\t\t - ".join(folders), default))
if not user_input:
    user_input = default
if user_input not in folders:
    print("Input ingresado es erróneo.")
    print("Ejecución interrumpida de forma segura.")
    exit()

###  ACTUALIZACION DEL output_dir   ###
output_dir = os.path.join(output_dir, user_input)
print("\nDirectorio seleccionado: {}".format(output_dir))

# sistema, cargar archivo pickle del directorio seleccionado
output_files = os.listdir(output_dir)#DRY
output_files = [file for file in output_files if file.endswith(".pickle")]


### (!) WARNING (!)
#TODO:
# Si en la carpeta correspondiente, existe un 2do archivo 
# con extensión ".pickle", se rompe el código.

if len(output_files) == 1: # en teoría siempre debería ser 1 WordCloud.py solo devuelve 1 pickle
    file = output_files[0]
elif len(output_files) == 0:
    print("No se encontró un archivo pickle en el directorio seleccionado.")
    print("Ejecución interrumpida de forma segura.")
    exit()# DRY

###  CARGAMOS EL BATCH  ###
with open(os.path.join(output_dir, file), "rb") as file:
    batch = pickle.load(file)

# sistema, confirmar que leiste el archivo pickle
assert type(batch) == list, "El archivo pickle no es un list."
assert len(batch) > 0, "El archivo pickle está vacío."
print("Input leído exitosamente.\n")
    
#######################################################################################

if len(batch) == 2:
    token = True
    batch_content, batch_token = batch

elif len(batch) == 1:
    token = False
    batch_content = batch[0]

else:
    print("Error en el formato del archivo pickle.")
    print("Ejecución interrumpida de forma segura.")
    exit()

#######################################################################################















## PARAMETROS DEL WORDCLOUD
print("Definición formato final de WordCloud.")

# usuario, ingresar parametros de wordcloud (mascara, colores, etc)
# user_input = input("¿Implementar configuración con Máscara? [n/Y]: Y\n")

user_input = "Y"

if user_input.lower() == "y" or user_input == '':#bucle obligatorio
    
    with open(os.path.join(path_utils, "wordcloud_mask_config.txt"), "r", encoding="UTF-8") as file:
        wc_params = file.read()
    
    try:
        wc_params = ast.literal_eval(wc_params)
        wc_params["mascara"] = Path(os.path.join(path_utils, wc_params["mascara"]))
        
        ##Esquema de validación Pydantic
        validation_schema = WordCloudConfig(**wc_params)
        wc_parmams = validation_schema.model_dump()
        
        
        
    except Exception as e:
        print("Error en el formato del archivo de configuración.")
        print(e)
        print("Ejecución interrumpida de forma segura.")
        exit()# DRY
    
    ## Abrimos el archivo png de la mascara
    try:
        print(f"Implementando configuración con Máscara: {wc_params['mascara']}")
        # mascara_wordcloud = np.array(Image.open(os.path.join(path_utils, wc_params["mascara"])))
        mascara_wordcloud = np.array(Image.open(wc_params["mascara"]))
        wc_params.pop("mascara")
    except FileNotFoundError as e:
        print("VARIABLE ANULADA: No se encontró el archivo de máscara.")



else:# bucle anulado
    with open(os.path.join(path_utils, "wordcloud_rectangle_config.txt"), "r", encoding="UTF-8") as file:
        wc_params = file.read()
    print("TODO: Implementar configuración con rectángulo.")
    print("programa cerrado forzozamente de manera segura. TODO:")
    exit()






  
    

### LIMPIEZA ITERATIVA DEL BATCH  ###
# usuario, ingresar si desea aplicar filtro de palabras
user_input = input("¿Aplicar filtro de palabras? [n/Y]: n\n")
if user_input.lower() == "y":
    # sistema, leer archivos txt de configuracion y correr modulo de filtrado
    utils_files = os.listdir(path_utils)
    file = "eliminar_palabras_que_comiencen_con.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        eliminar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo 'eliminar_palabras_que_comiencen_con.txt' en el directorio de APP_utils")
        eliminar_palabras = []
    
    file = "eliminar_palabras_wordcloud.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        filtrar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo 'eliminar_palabras_wordcloud.txt' en el directorio de APP_utils")
        filtrar_palabras = []
        
    # sistema, aplicar filtros
    batch_content = remover_palabra(batch_content, eliminar_palabras)
    batch_content = filtrado_palabras(batch_content, filtrar_palabras)
    if token:
        batch_token = remover_palabra(batch_token, eliminar_palabras)
        batch_token = filtrado_palabras(batch_token, filtrar_palabras)
        
        if filtrar_palabras[0] in batch_token:
            raise Exception("Error en el filtrado de palabras.")
    print(f"\nEliminadas palabras: {eliminar_palabras}\nFiltradas palabras: {filtrar_palabras}\n")
    
else:
    print("Filtro de palabras no aplicado.")
    


















###  IDENTIFICACION DEL ULTIMO WORDCLOUD CREADO  ###
# sistema, verificar la existencia de archivos de salida previos
output_files = os.listdir(output_dir)
output_files = [file for file in output_files if file.endswith(".png")]
if len(output_files) == 0:
    N = 1
else:
    N = [elemento.split("_")[-1] for elemento in output_files]
    N = [elemento.split(".")[0] for elemento in N]
    N = [int(elemento) for elemento in N if elemento.isdigit()]
    N = max(N) + 1

output_name = f"wordcloud_{nombre}_{N}"  
output_name = os.path.join(output_dir, output_name)



###  MODULO DE WORDCLOUD  ###
# verificar if colormap es una key de wc_params
# en la documentación de wordcloud
# si existe el parámetros color_func, se anular colormap
# entonces a la inversa
# si existe colormap, eliminamos color_func
if "colormap" in wc_params.keys() and wc_params["colormap"] != "":
    wc_params.pop("color_func")
else:
    color_tuple = wc_params["color_func"]
    color_func = lambda *args, **kwargs: color_tuple
    wc_params.pop("color_func")

# 1ra visualizacion: token
if token:
    with open(os.path.join(output_dir,'unique_batch_token.txt'), 'w', encoding="UTF-8") as f:
        f.write("\n".join(list(set(batch_token))))

    word_cloud = " ".join(batch_token)

    
    wordcloud = WordCloud(
        mask=mascara_wordcloud,
        collocations=False,
        **wc_params)
    if not "colormap" in wc_params.keys():
        wordcloud.color_func=color_func
    
    wordcloud.generate(word_cloud)
    
    wordcloud.to_file(f"{output_name}_token.png")


# 2da visualizacion: content
print(f"\nWordCloud Nº {N} de {nombre}\n")

plt.figure(figsize=(20,8))

word_cloud = ""
for row in batch_content:
    row += " "
    word_cloud+= row



# descargar en txt un listado de tokens únicos (no considera cantidad)
with open(os.path.join(output_dir,'unique_batch_content.txt'), 'w', encoding="UTF-8") as f:
    f.write("\n".join(list(set(word_cloud.split(" ")))))


# fecha: 23/10
###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)
###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)

## Se cambia el mode de RGBA a RGB y se cambia el background color
# se añaden las lineas de contorno y color del contorno

wordcloud = WordCloud(
    mask=mascara_wordcloud,
    collocations=False,
    contour_width=1.,
    contour_color=color_tuple,
    **wc_params)
###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)
###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)
# fecha: 23/10


if not "colormap" in wc_params.keys():
    wordcloud.color_func=color_func

wordcloud.generate(word_cloud)
wordcloud.to_file(f"{output_name}.png")
    
#plt.imshow(wordcloud);# BLOQUEA LA EJECUCION DEL INTERPRETE
    



# descargar txt con wc_params
wc_params["color_func"] = color_tuple
with open(os.path.join(output_dir, f"{output_name}.txt"), 'w', encoding="UTF-8") as f:
    f.write(str(wc_params))

print("programa finalizado exitosamente.")






## Consultar a ChatGPT
# array_wc = wordcloud.to_array()

# # pd.Series(array_wc.flatten()).value_counts()
# pd.Series(array_wc.flatten())
# pd.Series(array_wc.flatten()).value_counts()





