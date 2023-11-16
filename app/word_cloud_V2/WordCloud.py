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

def load_resources():
    global remover_palabra, procesamiento_texto
    global feed, data_process, preparation

    resources = wordcloud()
    remover_palabra = resources["wordcloud_remover_palabra"]
    procesamiento_texto = resources["wordcloud_procesamiento_texto"]
    feed = resources["main_feed"]
    data_process = resources["main_data_process"]
    preparation = resources["main_preparation"]

#OK
def word_filters_load(path:str, verbose:bool=False) -> list:  
    """
    Carga los filtros desde los recursos locales del sistema
    que se encuentran en el diretorio "word_cloud_config/"
    Devuelve una lista con dos elementos: [filter_1, filter_2]
    
    Filtro 1: palabras que comienzan con
    Filtro 2: palabras a filtrar
    """
    filename = "_epqcc.txt"#eliminar palabras que comienzan con
    if os.path.isfile(os.path.join(path, filename)):
        eliminar_por_comienzo = limpieza_txt(path, filename)
    else:
        print("No se encontró el archivo '_epqcc.txt' en el directorio APP_utils")
        eliminar_por_comienzo = []
    
    filename = "_epw.txt"# eliminar palabras wordcloud
    if os.path.isfile(os.path.join(path, filename)):
        eliminar_palabra = limpieza_txt(path, filename)
    else:
        print("No se encontró el archivo '_epw.txt' en el directorio APP_utils")
        eliminar_palabra = []
    
    if verbose:
        print(f"\nEliminar palabras: {eliminar_por_comienzo}\nFiltrar palabras: {eliminar_palabra}\n")

    return [eliminar_por_comienzo, eliminar_palabra]


#OK  
def word_filtering(df:pd.DataFrame, filter_1:list, filter_2:list) -> pd.DataFrame:
    """
    Función que nos permite aplicar filtros de palabra de forma manual, por medio de archivos .txt en el directorio /word_cloud_config/
    """
    assert "content_cleaned" in df.columns, "df debe tener una columna content_cleaned"
    
    ###  PROCESAMIENTO BATCH CONTENT  ###
    name = df.name
    df = df.copy()
    df.name = name
    batch_content = df.content_cleaned.to_list()
    ## primero limpiamos conservando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo, conservar_simbolos=True) for parrafo in batch_content]
    ## eliminamos palabras que comienzan con
    batch_content = remover_palabra(batch_content, filter_1)
    ## volvemos a limpiar quitando simbolos
    batch_content = [eliminar_caracteres_no_imprimibles(parrafo) for parrafo in batch_content]
    ## filtramos palabras configuradas
    batch_content = procesamiento_texto(batch_content, filter_2)
    
    
    df["content_cleaned"] = batch_content
    return df

#OK
def token_aggregation(df):
    name = df.name
    df = df.copy()
    df.name = name
    
    #OK: Actualiza la columna que recibe
    if "token" in df.columns:
        """
        Actualmente identifica la existencia de la columna y la procesa una por una 
        para reemplazar los "-" por None <- de esto no estoy seguro que esté pasando acá
        y también hace limpieza de ["TODOS LOS TOKENS JUNTOS"] -> ["TODOS","LOS","TOKENS","JUNTOS"]
        y también filtra el símbolo de hashtag
        """
        batch_ = df.token.to_list()
        
        if isinstance(batch_[0], list):
            batch_token = df.token.to_list()
        elif isinstance(batch_[0], str):
            # token elastic: [["token1, token2, token3"], ["token4, token5, token6"], "-", ...]
            # return: [["token1", "token2", "token3""],[...],[None], ...]
            
            batch_token = [row.replace(",", "").replace("#", "").split(" ") for row in batch_ if row != "-"]
        else:
            print("WordCloud: Error en la interpretacion de los tokens")
            sys.exit(0)

        batch_token = [item for sublist in batch_token for item in sublist]
        # assertion si batch_token no es una lista de string
        try:
            assert isinstance(batch_token, list), "batch_token no es una lista"
            assert isinstance(batch_token[0], str), "batch_token no es una lista de strings"
        except AssertionError as error:
            print(error)
            print("Continúa la ejeciución")
            
        df["token"] = batch_token
        
    # Setea (default): la columna en la que se van a ejecutar los WC
    if "tokens_i" in df.columns:
        # No se implementan filtros sobre los tokens
        df["token_wc"] = df.tokens_i
    
    # Utiliza el auxiliar
    else:
        df["token_wc"] = df.token
    
    return df


def stop_words_multithread(batch_content, filtros_bool, max_workers):
    pass  

#TODO: devuelve una lista de DataFrames
def stop_words_execution(df:pd.DataFrame, filtros_bool:list=None, max_workers:int=4) -> list:
    """
    Esta funcion recibe 3 parámetros: df: pd.DataFrame, filtros:list = None, max_workers:int = 4
    Devuelve una lista de DataFrames: List[pd.DataFrame]
    
    
    Filtros puede ser una lista vacía o None, en ese caso el return es una lista con 1 DataFrame.
    En cuanto se aplican filtros, la longitud del return cambia.
    Solo acepta filtros booleanos.
    Si la lista tiene 1 elemento, ese elemento es un filtro booleano, y si tiene 2 elementos, cada elemento es un filtro booleano, sucesivamente...
    
    Los DataFrame resultantes tienen agregada una columna llamada "content_cleaned"
    Dicha columna es la que ingresa en el objeto Wordcloud de la librería wordcloud
    
    """
    assert "content_cleaned" in df.columns, "df debe tener una columna content_cleaned"
    assert "token_wc" in df.columns, "df debe tener una columna token_wc"
    
    name = df.name
    df = df.copy()
    df.name = name
    
    if filtros_bool is None:
        filtros_bool = []
        
    if not len(filtros_bool) > 0:
        batch_content = aplicar_stopwords(df.content_cleaned.to_list())
    else:#TODO
        print("no está implementado")
        1/0
        batch_content = stop_words_multithread(batch_content, filtros_bool, max_workers)
        # multithread va a ser necesario ordenar los outputs
    
    df["content_wc"] = batch_content
    return df



##############################################################################
##############################################################################
##############                PROGRAMA PRINCIPAL                ##############
##############################################################################
##############################################################################

def main_df(df:pd.DataFrame, filtros=None, max_workers=4) -> pd.DataFrame:# La próxima actualización es List[pd.DataFrame]
    """
    PROCESOS:
    
    - Se cargan los recursos enviados desde main/main.py
    - 1er procesamiento: eliminar duplicados del content
    - Se ejecuta preprocesamiento
    def token_aggregations()
    - 2do: procesamiento de los tokens existentes -> token_wc
    - 3ro: filtrado de palabras -> content_cleaned
    - 4to: implementar stop_words -> content_wc
    """
    load_resources()

    name = df.name
    df = df.copy()
    df.name = name


    df = df.drop_duplicates(subset=["content"], keep="first")
    df.name = name

    # verificar que df tenga name
    df = token_aggregation(df)
        

    # Recibe una lista de str,y el path donde se encuentran ambos archivos txt (nombres hardcodeados)
    path_utils = os.path.join(project_root, "word_cloud_config")
    df = word_filtering(df, *word_filters_load(path_utils))
    

    df = stop_words_execution(df)#, filtros, max_workers)

    # Esto no va a correr ni en remil pedo
    # file_path = finale(df, path_utils)#warning: se va a sobrecargar de archivos la carpeta de cofiguracion

    
    # hacer algo con result
    # print(file_path)
    print("Programa ejecutado exitosamente")
    # return #Datasets con los stop_words aplicados
    return df# Debería devolver una lista con dataframes. Sea de longitud 1 para procesamiento lineal o multiples elementos para optimizacion por multihilos en la seccion de stop_words.


def new_finale(df): #TENER SIEMPRE PRESENTE QUE SE VA A ACTUALIZAR A List[pd.DataFrame]
    """
    Esta funcion ejecuta la libreria wordcloud
    
    devuelve la o las figure, y agregaciones implicitas en el dataset
    
    para que eso ocurra, se debe incorporar la logica de output_analytics.py
    
    Algo muy importante a tener en cuenta es que debe recibir el diccionario de params
    en vez de buscar el txt correspondiente.
    Se debe ser cuidadoso con los valores por default que se van a establecer
    Recudir al esquema de validacion en /schemas/...
    
    Agregacion pendiente: el array vectorial con el que fue conformado el wordcloud
    # array_wc = wordcloud.to_array()
    # pd.Series(array_wc.flatten())
    # # pd.Series(array_wc.flatten()).value_counts()
    
    """
    dataset = [df]
    

# PROVISORIO
def finale(df, path):
    """
    Mete el batch de content y el batch de token dentro de una lista
    y guarda la lista dentro de un fichero pickle
    devuelve el path de dicho fichero pickle.
    """

    ### OUTPUT PARA OUTPUT_ANALYTICS.PY ###
    output = [df.content_wc.to_list(), df.token_wc.to_list()]

    file_path = os.path.join(path, "wordcloud_batch.pickle")

    with open(file_path, "wb") as file:
        pickle.dump(output, file)
    
    return file_path
