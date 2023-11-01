## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show


## Ubicación de los directorios - dirección
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
shared_resources = os.path.join(os.path.abspath(os.path.join(app_root, '..')), "shared_resources")
sys.path.insert(0, project_root)

# Librería Reputación Digital
from tools.feed import data_info
from tools.feature_treatment import create_sparse_feature, resample_dataset_s



########################
# PROGRAMA PRINCIPAL
########################


file_name = "panorama-economico.pickle"
with open(f"{project_root}/{file_name}", "rb") as f:
    df = pickle.load(f)


data_info(df)



filter_list = ["datetime", "content", "author", \
    "sentiment_i", "emotions_6_max_label", "emotions_26_max_label"]


"""
Objetivo:

            label_1  label_2  label_3  label_4  ... label_n
content_1
content_2
content_3
content_4
content_5
content_6
content_7
...
content_m


El datetime: me sirve para resamplear y repetir el mismo gráfico es distinto marco temporal
Previamente hay que ajustar el período que se desea visualizar.
Para temporalidades menores será una ventana de tiempo más pequeña, y 
para temporalidades mayores se utilizaría el set completo de datos.

mt: marco temporal

            label_1  label_2  label_3  label_4  ... label_n
sample_1
sample_2
sample_3
sample_4
...
sample_mt


/ mt_i < m para todo i

"""



df = df.filter(filter_list)
df = df.set_index("datetime").sort_index(ascending=False)


f1 = create_sparse_feature(df, "sentiment_i")
f2 = create_sparse_feature(df, "emotions_6_max_label")
f3 = create_sparse_feature(df, "emotions_26_max_label")

fs = pd.concat([f1, f2, f3], axis=1)


## ()SE HACE UN RESAMPLEO Y SE DEBERÍA TOMAR UN TIME_WINDOW CORRESPONDIENTE A LA TEMPORALIDAD
fs_h = resample_dataset_s(fs, "H")
fs_d = resample_dataset_s(fs, "D")





## CONFIGURACION DE LOS COLORES

colors_sentiment = {
    "sentiment_i_negative": "#e7664cff",
	"sentiment_i_neutral": "#2261aa",
	"sentiment_i_positive": "#54b399ff"
 }

verde = "#FFFF00"
amarillo = "#e926b0"
gris = "#7a9c7d"
rojo = "#00FF00"
azul = "#473b9e"

colors_emotions_6 = {
    "anger": rojo,
    "fear": azul,
    "joy":amarillo,
    "love":verde,
    "sadness": azul,
    "surprise":amarillo
    }

azul_miedo_desagrado = "#473b9e"
rosa_aversion_duda = "#ea76e5"
rojo_tension_entusiasmo = "#901f31"
amarillo_satisfaccion_valor = "#d5d432"
verde_altivez_deseo = "#9cf581"
verde_amor_certeza = "#4bb710"
celeste_calma_aburrimiento = "#80c0ea"
celeste_apatia_tristeza = "#53b7d9"

colors_emotions_28 = {
    "neutral": celeste_calma_aburrimiento, "approval": amarillo_satisfaccion_valor, "realization": amarillo_satisfaccion_valor,
    "caring": verde_amor_certeza, "curiosity": rosa_aversion_duda, "confusion": rosa_aversion_duda,
    "disapproval": celeste_apatia_tristeza, "desire": verde_altivez_deseo, "annoyance": celeste_calma_aburrimiento,
    "gratitude": amarillo_satisfaccion_valor, "excitement": rojo_tension_entusiasmo, "pride": verde_altivez_deseo,
    "remorse": celeste_apatia_tristeza, "disappointment": celeste_apatia_tristeza, "relief": celeste_calma_aburrimiento,
    "admiration": verde_altivez_deseo, "anger": rojo_tension_entusiasmo, "amusement": amarillo_satisfaccion_valor,
    "embarrassment": azul_miedo_desagrado, "joy": verde_altivez_deseo, "surprise": rojo_tension_entusiasmo,
    "nervousness": rojo_tension_entusiasmo, "love": verde_amor_certeza, "sadness": celeste_apatia_tristeza,
    "grief": rosa_aversion_duda, "disgust": azul_miedo_desagrado, "optimism": verde_altivez_deseo,
    "fear": azul_miedo_desagrado}

colores = colors_sentiment | colors_emotions_6 | colors_emotions_28
print(colores)

##  CREACION DE LA VARIABLE A VISUALIZAR PARTE 1

data = fs.T.sum(axis=1).to_frame()
data.columns = ["count"]


# df_promedios["colores"] = df_promedios.index.map(colores)
# data= data.reset_index()
# data

# df_promedios = df_promedios.to_frame().reset_index()