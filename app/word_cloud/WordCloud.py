## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
sys.path.insert(0, project_root)

## Aplicaciones propias
from app.main.main import wordcloud
try:
    from app.word_cloud.main import main as Main
    from app.word_cloud.main import limpieza_txt
except:
    from main import main as Main
    from main import limpieza_txt

## Libreria propia
from tools.feature_adjust import eliminar_caracteres_no_imprimibles, aplicar_stopwords
from tools.feed import procesar_file_csv, crear_directorio_salida_numerado



  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###
###  ###  ###  ###  ###  ###  PROGRAMA PRINCIPAL  ###  ###  ###  ###  ###  ###
  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###
  
  
def main_df(df:pd.DataFrame, verbose:bool=False) -> str:
    import time
    start = time.time()    
    
    if verbose:
        print("Ejecutando wordcloud/WordCloud.py\n")
        print("Cargando configuración...")
    
    ## CARGA DE RECURSOS DESDE APP MAIN MAIN
    ## VARIABLES GENERALES
    path_utils = os.path.join(project_root, "app", "word_cloud_utils")
    resources = wordcloud()
    remover_palabra = resources["wordcloud_remover_palabra"]
    procesamiento_texto = resources["wordcloud_procesamiento_texto"]




    #TODO: DOCUMENTACION: Cómo es que se limpian los wordclouds? utilizar estos archivos
    #TODO: DRY
    file = "_epqcc.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        eliminar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo '_epqcc.txt' en el directorio APP_utils")
        eliminar_palabras = []
    
    file = "_epw.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        filtrar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo '_epw.txt' en el directorio APP_utils")
        filtrar_palabras = []
    
    if verbose:
        print(f"\nEliminar palabras: {eliminar_palabras}\nFiltrar palabras: {filtrar_palabras}\n")
    
    

    #TODO: file_name recognition
    
    ## EJECUCION DEL MODULO WORDCLOUD MAIN
    if df is None:
        df, path_output = Main()
    else:
        ## GESTION DE DIRECTORIOS
        nombre = df.name
        path_output = os.path.join(project_root , "output")
        path_output = os.path.join(path_output, nombre)
        path_output = crear_directorio_salida_numerado(path_output, verbose=False)
        if verbose:
            print("Directorio de salida:")
            print(path_output)


    ### PROCESAMIENTO DATA  ###
    df = df.drop_duplicates(subset=["content"], keep="first")

    if "token" in df.columns:
        # user: definí si querés visualizar el content o el content y el token: default True
        token = True
        batch_ = df.token.to_list()
        
        if isinstance(batch_[0], list):
            # token_tokenizador: [["token1", "token2"], ["token3", "token4"], [...]]
            # batch_ = [",".join(row) for row in batch_]
            batch_token = df.token.to_list()
            batch_token = [item for sublist in batch_token for item in sublist]
        #DRY
        elif isinstance(batch_[0], str):
            # token elastic: ["token1, token2, token3", "token4, token5, token6"]
            batch_token = [row.replace(",", "").replace("#", "").split(" ") for row in batch_ if row != "-"]
            batch_token = [item for sublist in batch_token for item in sublist]
        else:
            print("WordCloud: Error en la interpretacion de los tokens")
            sys.exit(0)
            
        # output: ["token1", "token2", "token3", "token4", "token5", "token6"]
        
        # assertion si batch_token no es una lista de string
        assert isinstance(batch_token, list)
        assert isinstance(batch_token[0], str)
        
        #TODO: crear esquema de validación para una lista de string de una sola palabra

    else:
        token = False
    
    batch_content = df.content.to_list()
    
    string_batch = "\n".join(batch_content)# SALIDA PREPROCESADA
    with open(os.path.join(path_output, "wordcloud_raw_content.txt"), "w", encoding="UTF-8") as file:
        file.write(string_batch)

    
    ###  PROCESAMIENTO BATCH CONTENT  ###
    if verbose:
        print("Modulo de procesamiento duro - aguarde un momento...")
    ## primero limpiamos conservando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo, conservar_simbolos=True) for parrafo in batch_content]
    ## eliminamos palabras que comienzan con
    batch_content = remover_palabra(batch_content, eliminar_palabras)
    ## volvemos a limpiar quitando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo) for parrafo in batch_content]
    ## filtramos palabras configuradas
    batch_content = procesamiento_texto(batch_content, filtrar_palabras)
    ## aplicamos stopwords
    if verbose:
        print("Iniciando filtrado de stop_words...")
    batch_content = aplicar_stopwords(batch_content)
    
    
    ### OUTPUT PARA HUMANOS  ##
    string_batch = "\n".join(batch_content)# SALIDA PROCESADA
    with open(os.path.join(path_output, "wordcloud_batch_i.txt"), "w", encoding="UTF-8") as file:
        file.write(string_batch)
    
    if token:
        string_batch = "\n".join(batch_token)
        with open(os.path.join(path_output, "wordcloud_batch_token.txt"), "w", encoding="UTF-8") as file:
            file.write(string_batch)


    ### OUTPUT PARA OUTPUT_ANALYTICS.PY ###
    output = [batch_content]
    if token:
        output.append(batch_token)

    with open(os.path.join(path_output, "wordcloud_batch.pickle"), "wb") as file:
        pickle.dump(output, file)


    ## FINALIZACION DE LA EJECUCION
    end = time.time()
    if verbose:
        print("Tiempo de ejecución:", round(end-start, 2), "[seg]") # data-benchmark: 14.6 segundos
    
    return nombre


























if __name__ == "__main__":
    ##  ORIGINAL  ##

    import time
    start = time.time()    
    
    print("Ejecutando wordcloud/WordCloud.py\n")
    
    ## CARGA DE RECURSOS DESDE APP MAIN MAIN
    ## VARIABLES GENERALES
    print("Cargando configuración...")
    path_utils = os.path.join(project_root, "app", "word_cloud_utils")
    resources = wordcloud()
    remover_palabra = resources["wordcloud_remover_palabra"]
    procesamiento_texto = resources["wordcloud_procesamiento_texto"]




    #TODO: DOCUMENTACION: Cómo es que se limpian los wordclouds? utilizar estos archivos
    #TODO: DRY
    file = "_epqcc.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        eliminar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo '_epqcc.txt' en el directorio APP_utils")
        eliminar_palabras = []
    
    file = "_epw.txt"
    if os.path.isfile(os.path.join(path_utils, file)):
        filtrar_palabras = limpieza_txt(path_utils, file)
    else:
        print("No se encontró el archivo '_epw.txt' en el directorio APP_utils")
        filtrar_palabras = []
        
    print(f"\nEliminar palabras: {eliminar_palabras}\nFiltrar palabras: {filtrar_palabras}\n")
    
    

    
    
    ## EJECUCION DEL MODULO WORDCLOUD MAIN
    df, path_output = main()
    print("Saliendo de wordcloud/main.py\n")
    
    ### PROCESAMIENTO DATA  ###
    df = df.drop_duplicates(subset=["content"], keep="first")
    
    if "token" in df.columns:
        # user: definí si querés visualizar el content o el content y el token: default True
        token = True
        batch_ = df.token.to_list()
        batch_token = [row.replace(",", "").replace("#", "").split(" ") for row in batch_ if row != "-"]
        batch_token = [item for sublist in batch_token for item in sublist]
        #TODO: crear assertion si batch_token no es una lista de string
        #TODO: crear esquema de validación para una lista de string
        

    else:
        token = False
    
    batch_content = df.content.to_list()
    
    string_batch = "\n".join(batch_content)# SALIDA PREPROCESADA
    with open(os.path.join(path_output, "wordcloud_raw_content.txt"), "w", encoding="UTF-8") as file:
        file.write(string_batch)
    
    
    
    
    
    ###  OPTIMIZAR  ###
    ###  OPTIMIZAR  ###
    ###  OPTIMIZAR  ###
    print("Modulo de procesamiento duro - aguarde un momento...")
    ## primero limpiamos conservando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo, conservar_simbolos=True) for parrafo in batch_content]
    ## eliminamos palabras que comienzan con
    batch_content = remover_palabra(batch_content, eliminar_palabras)
    ## volvemos a limpiar quitando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo) for parrafo in batch_content]
    ## filtramos palabras configuradas
    batch_content = procesamiento_texto(batch_content, filtrar_palabras)
    
    """   TODO:
    - Hasta acá conservamos los simbolos: - ; (+ emojis)  
    - Eliminamos todos las palabras 100% conformada por números: 19hs 40% se conserva - 2018 se elimina
    - Tenemos renglones vacíos
    - Hay palabras que estan pegadas al guíon medio ej: -tambien pepito-menganito volver-
        
    """
    ## aplicamos stopwords
    print("Iniciando filtrado de stop_words...")
    batch_content = aplicar_stopwords(batch_content)
    ###  OPTIMIZAR  ###
    ###  OPTIMIZAR  ###
    ###  OPTIMIZAR  ###
    
    
    
    
    
    
    
    
    ### OUTPUT PARA HUMANOS  ##
    string_batch = "\n".join(batch_content)# SALIDA PROCESADA
    with open(os.path.join(path_output, "wordcloud_batch_i.txt"), "w", encoding="UTF-8") as file:
        file.write(string_batch)
    
    if token:
        string_batch = "\n".join(batch_token)
        with open(os.path.join(path_output, "wordcloud_batch_token.txt"), "w", encoding="UTF-8") as file:
            file.write(string_batch)


    ### OUTPUT PARA OUTPUT_ANALYTICS.PY ###
    output = [batch_content]
    if token:
        output.append(batch_token)

    with open(os.path.join(path_output, "wordcloud_batch.pickle"), "wb") as file:
        pickle.dump(output, file)


    ## FINALIZACION DE LA EJECUCION
    end = time.time()
    print("Tiempo de ejecución:", round(end-start, 2), "[seg]") # data-benchmark: 14.6 segundos
    
