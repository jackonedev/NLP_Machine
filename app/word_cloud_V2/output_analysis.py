## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle, ast
from pathlib import Path
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
path_utils = os.path.join(project_root, "app", "word_cloud_utils")
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


  
  
  
def main(file_path:str = None, verbose=False) -> None:
    from app.main.main import wordcloud
    
    ## VARIABLES GENERALES
    if verbose:
        print("WordCloud: Cargando configuración...")
    resoruces = wordcloud()
    remover_palabra = resoruces["wordcloud_remover_palabra"]
    filtrado_palabras = resoruces["wordcloud_filtrado_palabras"]



    ###  CARGAMOS EL BATCH  ###
    with open(file_path, "rb") as file:
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
    if verbose:
        print("Definición formato final de WordCloud.")



    user_input = "Y"

    if user_input.lower() == "y" or user_input == '':#bucle obligatorio

        with open(os.path.join(path_utils, "wordcloud_mask_config.txt"), "r", encoding="UTF-8") as file:
            wc_params = file.read()

        try:
            wc_params = ast.literal_eval(wc_params)
            wc_params["mascara"] = Path(os.path.join(path_utils, wc_params["mascara"]))

            ##Esquema de validación Pydantic
            validation_schema = WordCloudConfig(**wc_params)
            try:
                wc_parmams = validation_schema.dict()
            except:
                wc_parmams = validation_schema.model_dump()
                
            if nombre.split("-")[-1] in ["positive", "negative"]:
                if nombre.split("-")[-1] == "positive":
                    wc_params["color_func"] = (84, 179, 153)
                elif nombre.split("-")[-1] == "negative":
                    wc_params["color_func"] = (231, 102, 76)
                
 
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


    

    ### LIMPIEZA ITERATIVA DEL BATCH  ###
    # usuario, ingresar si desea aplicar filtro de palabras
    # user_input = input("¿Aplicar filtro de palabras? [n/Y]: n\n")
    user_input = "y"
    if user_input.lower() == "y":
        # sistema, leer archivos txt de configuracion y correr modulo de filtrado
        utils_files = os.listdir(path_utils)
        file = "eliminar_palabras_que_comiencen_con.txt"
        if os.path.isfile(os.path.join(path_utils, file)):
            eliminar_palabras = limpieza_txt(path_utils, file)
        else:
            if verbose:
                print("No se encontró el archivo 'eliminar_palabras_que_comiencen_con.txt' en el directorio de APP_utils")
            eliminar_palabras = []
        
        file = "eliminar_palabras_wordcloud.txt"
        if os.path.isfile(os.path.join(path_utils, file)):
            filtrar_palabras = limpieza_txt(path_utils, file)
        else:
            if verbose:
                print("No se encontró el archivo 'eliminar_palabras_wordcloud.txt' en el directorio de APP_utils")
            filtrar_palabras = []
            
        # sistema, aplicar filtros
        batch_content = remover_palabra(batch_content, eliminar_palabras)
        batch_content = filtrado_palabras(batch_content, filtrar_palabras)

        if verbose:
            print(f"\nEliminadas palabras: {eliminar_palabras}\nFiltradas palabras: {filtrar_palabras}\n")
    
    else:
        if verbose:
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
            contour_width=1.0,
            **wc_params)
        if not "colormap" in wc_params.keys():
            wordcloud.color_func=color_func
            wordcloud.contour_color = color_tuple
        else:
            wordcloud.contour_color = (0, 0, 0)
        
        
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
        contour_width=1.0,
        **wc_params)
    
    ## si existe colormap. no existe contour
    if not "colormap" in wc_params.keys():
        wordcloud.color_func=color_func
        wordcloud.contour_color = color_tuple
    else:
        wordcloud.contour_color = (0, 0, 0)

    
    wordcloud.generate(word_cloud)
    wordcloud.to_file(f"{output_name}.png")
        

    # descargar txt con wc_params
    try:
        wc_params["color_func"] = color_tuple
    except:
        pass
        
    with open(os.path.join(output_dir, f"{output_name}.txt"), 'w', encoding="UTF-8") as f:
        f.write(str(wc_params))

    
    print("programa finalizado exitosamente.")
    print(f"Archivo guardado: {output_name}.png")
        







