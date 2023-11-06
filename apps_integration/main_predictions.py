## Bienvenido al programa que integra la implementación de la serie de aplicaciones desarrolladas
import sys, os, pickle
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
shared_resources_root = os.path.abspath(os.path.join(project_root, "app", 'shared_resources'))
sys.path.insert(0, project_root)

from tools.feed import procesar_file_csv

from app.main import data_feed
from app.time_series import TimeSeries
from app.m1_sentiment import M1_sentiment
from app.m2_emotions import M2_emotions
from app.m3_emotions import M3_emotions



def obtener_dfts(file_name:str =None) -> pd.DataFrame:
    
    if file_name is None:
        file_name = input("Ingresar nombre de archivo: ")


    if not file_name:
        print("Sin input, se cierra programa de forma segura")
        sys.exit(0)
    
    nombre, archivo = procesar_file_csv(file_name)
    archivo_root = os.path.join(project_root, archivo)

    if not os.path.exists(archivo_root):
        print("El archivo no existe, se cierra programa de forma segura")
        sys.exit(0)


    ## ARCHIVO TIMESERIES
    dfts_path = TimeSeries.main(archivo)
    with open(dfts_path, "rb") as file:
        dfts = pickle.load(file)
        # print("archivo TS abierto exitosamente")

    dfts.name = nombre
    return dfts


def main_df(df:pd.DataFrame, verbose=False, backup=False) -> pd.DataFrame:
    
    nombre = df.name
    

    df_1 = M1_sentiment.main_df(df)
    print("Modelo 1 ejecutado exitosamente")
    ## Estos dos modelos de abajo podrían correr en pararlelo
    df_2 = M2_emotions.main_df(df, verbose=verbose)
    print("Modelo 2 ejecutado exitosamente")
    df_3 = M3_emotions.main_df(df, verbose=verbose)
    print("Modelo 3 ejecutado exitosamente")
    
    
    df = df.reset_index(drop=True)

    df_1 = df_1.filter(["sentiment_i", "score_sentiment_i"]).reset_index(drop=True)
    df_2 = df_2.reset_index(drop=True)
    df_3 = df_3.reset_index(drop=True)
    
    result = pd.concat([df, df_1, df_2, df_3], axis=1)

    ## Reemplazo de las etiquetas Neutral por la segunda opción más probable
    mask_neutral = (result["emotions_26_max_label"] == "neutral").values
    new_label = [row[0][1] for row in result.loc[mask_neutral,["emotions_26_labels"]].values]
    result.loc[mask_neutral, "emotions_26_max_label"] = new_label
    
    if backup:
        with open(os.path.join(shared_resources_root, f"{nombre}.pickle"), "wb") as file:
            pickle.dump(result, file)
        if verbose:
            print("Predicciones almacenadas exitosamente")

    return result


def main(file_name:str = None, verbose=False, backup=True) -> pd.DataFrame:
    
    dfts = obtener_dfts(file_name)
    nombre = dfts.name
    print("archivo TS abierto exitosamente")
    df_1 = M1_sentiment.main_df(dfts)
    print("Modelo 1 ejecutado exitosamente")
    ## Estos dos modelos de abajo podrían correr en pararlelo
    df_2 = M2_emotions.main_df(dfts, verbose=verbose)
    print("Modelo 2 ejecutado exitosamente")
    df_3 = M3_emotions.main_df(dfts, verbose=verbose)
    print("Modelo 3 ejecutado exitosamente")
    
    
    dfts = dfts.reset_index(drop=True)

    df_1 = df_1.filter(["sentiment_i", "score_sentiment_i"]).reset_index(drop=True)
    df_2 = df_2.reset_index(drop=True)
    df_3 = df_3.reset_index(drop=True)
    
    result = pd.concat([dfts, df_1, df_2, df_3], axis=1)

    ## Reemplazo de las etiquetas Neutral por la segunda opción más probable
    mask_neutral = (result["emotions_26_max_label"] == "neutral").values
    new_label = [row[0][1] for row in result.loc[mask_neutral,["emotions_26_labels"]].values]
    result.loc[mask_neutral, "emotions_26_max_label"] = new_label
    
    if backup:
        with open(os.path.join(shared_resources_root, f"{nombre}.pickle"), "wb") as file:
            pickle.dump(result, file)
        if verbose:
            print("Predicciones almacenadas exitosamente")

    return result
    