## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

## Ubicación de los directorios - dirección
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
shared_resources = os.path.join(os.path.abspath(os.path.join(app_root, '..')), "shared_resources")

sys.path.insert(0, project_root)

# Librería Reputación Digital
from tools.feed import data_info
from tools.feature_treatment import create_sparse_feature, resample_dataset_c



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

fs_min = resample_dataset_c(fs, "15T")
fs_h = resample_dataset_c(fs, "H")
fs_d = resample_dataset_c(fs, "D")


fs_min.T




print("Programa finalizado de forma exitosa")