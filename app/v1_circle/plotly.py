## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle
import pandas as pd

from sklearn.preprocessing import OneHotEncoder

# pd.options.plotting.backend = "plotly"

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


# pd.options.plotting.backend = "plotly"
file_name = "panorama-economico.pickle"
with open(f"{project_root}/{file_name}", "rb") as f:
    df = pickle.load(f)


data_info(df)



filter_list = ["datetime", "content", "author", \
    "sentiment_i", "emotions_6_max_label", "emotions_26_max_label"]


df = df.filter(filter_list)

df = df.set_index("datetime").sort_index(ascending=False)


f1 = create_sparse_feature(df, "sentiment_i")
f2 = create_sparse_feature(df, "emotions_6_max_label")
f3 = create_sparse_feature(df, "emotions_26_max_label")

fs = pd.concat([f1, f2, f3], axis=1)

fs_h = resample_dataset_s(fs, "H")
fs_d = resample_dataset_s(fs, "D")


fs_h.plot(kind="line", title="Sentimiento y Emociones - Panorama Económico - Resampleado por hora")



print("Programa finalizado de forma exitosa")
