import pandas as pd
import pickle
import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
try:
    # ejecutado desde el main
    from . import data_feed
except ImportError:
    import data_feed
    
try:
    from ...tools import feed
    from ...tools.deteccion_hashtags import extraer_hashtags, eliminar_hashtags
    from ...tools.deteccion_usuarios import extraer_usuarios, eliminar_menciones
    from ...tools.extraer_indices_http import extraer_http, eliminar_https
    from ...tools.extraer_indices_rt import extraer_rt
except:
    from tools import feed
    from tools.deteccion_hashtags import extraer_hashtags, eliminar_hashtags
    from tools.deteccion_usuarios import extraer_usuarios, eliminar_menciones
    from tools.extraer_indices_http import extraer_http, eliminar_https
    from tools.extraer_indices_rt import extraer_rt


###  BIENVENIDO AL MODULO QUE PREPARA LOS SETS PARA MUCHOS OTROS MODULOS  ###



#####################
## DATA PREPROCESS ##
#####################
def main(df: pd.DataFrame) -> pd.DataFrame:

# 1. Tratamiento de la columna "content" (comentarios en redes)
    print("1. Limpieza del content\n")
    
    assert isinstance(df, pd.DataFrame), "El argumento df debe ser un dataframe de pandas"
    assert "content" in list(df.columns), "No existe la columna 'content' en el dataframe"
    
    content = df.content.to_list()
    print(f"Longitud del batch de contenidos: {len(content)}")


    # 1.1 Limpieza de cada parrafo de cada comentario del content
    for i, parrafo in enumerate(content):
        temporal = parrafo.splitlines()#TODO: GPT tokeniza las palabras así " palabra", dejando un espacio al comienzo
        auxiliar = []
        
        for t in temporal:
            # correjir "." y ",". Para simplificar la tokenización
            t = t.replace(".", " .")
            t = t.replace(",", " ,")
            if t != "":
                auxiliar.append(t)
                
        content[i] = " ".join(auxiliar)

    df["content"] = content
    
    return df
    

def preprocesamiento(df: pd.DataFrame, quitar=True, token_config=False) -> pd.DataFrame:
    """Especializado para Twitter
Se ocupa de eliminar los retwits, los links, los usuarios y los hashtags
Crear una columna con los usuarios mencionados
Crear una columna con los hashtags
    """
    # IDENTIFICAMOS LOS INDICES QUE COMIENZAN CON RT y EXTRAEMOS MUESRTA
    assert isinstance(df, pd.DataFrame), "El argumento df debe ser un dataframe de pandas"
    assert "content" in list(df.columns), "No existe la columna 'content' en el dataframe"
    
    if ["token"] in list(df.columns):
        #assert "token" in list(df.columns), "No existe la columna 'token' en el dataframe"
        df["token"] = df["token"].replace("-", None)
    
    if not token_config:
        df["content"] = df.content.apply(lambda x: x.lower()) #TODO: no está en la version original
    
    

    # check: df.loc[df.duplicated()] # vemos que hay registros duplicados que no son retwits

    # ELIMINAMOS LOS REGISTROS DUPLICADOS
    # esto es un doble check porque se supone que los retwits son los unicos duplicados
    if not token_config:
        df = df.drop(extraer_rt(df["content"]))
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)


    # IDENTIFICAMOS LOS INDICES QUE CONTIENEN HTTP Y EXTRAEMOS LA MUESTRA
    indices_http = extraer_http(df["content"])
    muestra_http = df.loc[indices_http]

    if quitar:
        df = eliminar_https(df, "content", indices_http)
        df = df.reset_index(drop=True)
    print(f"Tamaño de la muestra neta: {df.shape[0]}")

    # EXTRAER USUARIOS Y HASHES
    user_dict = extraer_usuarios(df["content"])
    hash_dict = extraer_hashtags(df["content"])

    # Eliminar menciones y hashtags
    if quitar:
        df["content"] = eliminar_menciones(df["content"], user_dict)
        df["content"] = eliminar_hashtags(df["content"], hash_dict)

    # AÑADIR UNA COLUMNA CON LOS USUARIOS DETECTADOS
    user_series = pd.Series(user_dict)
    df['usuarios_mencionados'] = df.index.map(user_series)

    hash_series = pd.Series(hash_dict)
    df['hashtags'] = df.index.map(hash_series)
    
    df["content"] = df.content.apply(lambda x: x.strip())
    

    return df
