## Bienvenido al programa que integra la implementación de la serie de aplicaciones desarrolladas
import sys, os, pickle

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
shared_resources_root = os.path.abspath(os.path.join(project_root, "app", 'shared_resources'))
sys.path.insert(0, project_root)

from tools.feed import procesar_file_csv

from app.main import data_feed
from app.tokenizadores import tokenizador_i
from app.time_series import TimeSeries
from app.word_cloud import WordCloud, output_analysis


## 1. Data preparation: Tokenizacion y TimeSeries (convención)
##      - obtener df directo del csv
##      - implementar tokenizacion en dftk
##      - implementar timeseries en dfts


user_input = 'octubre-untitled.csv'
# user_input = input("Ingresar nombre de archivo: ")
if not user_input:
    print("Sin input, se cierra programa de forma segura")
    sys.exit(0)
    
nombre, archivo = procesar_file_csv(user_input)
archivo_root = os.path.join(project_root, archivo)

if not os.path.exists(archivo_root):
    print("El archivo no existe, se cierra programa de forma segura")
    sys.exit(0)


## ARCHIVO ELASTIC SEARCH
df = data_feed.main(archivo_root)
df.name = nombre
print("archivo original abierto exitosamente")

## ARCHIVO TIMESERIES
##TODO: procesamiento light sin perdida de registros
# dfts_path = TimeSeries.main(archivo)
# with open(dfts_path, "rb") as file:
#     dfts = pickle.load(file)
# dfts.name = nombre
# print("archivo TS abierto exitosamente")

## ARCHIVO TOKENIZADO
dftk = tokenizador_i.main(archivo)
dftk.name = nombre
print("archivo TK abierto exitosamente")

print(df.shape)
# print(dfts.shape)
print(dftk.shape)




## 2. WordClouds - content + tokens
## TODO: decidir
## TODO: que el tokenizador descargue archivos en shared_resources
# o que wordcloud pueda recibir dataframes...
dfwc = dftk[['content']]
dfwc.loc[:, "token"] = dftk.loc[:, 'tokens_i']
dfwc.name = nombre

#TODO: 

nombre_wc = WordCloud.main_df(dfwc)
output_analysis.main(nombre_wc)


## APP 2
## 3. Clasificación por transformers -
## También se lo aplicamos a dftk

## 4. Plotly: graficos de torta -> de lineas (Series temporales) -> de barras
## 
## 5. (Pendiente) Bokeh: graficos radiales en coordenadas polares


## APP 3
## 6. (Pendiente) Word2Vec: Embeddings
## 
## 7. (Pendiente) K Means: Clustering
## 
## 8. (Pendiente) LDA: Topic Modeling
## 
## 9. (Pendiente) NER: Named Entity Recognition
## 
## 10. (Pendiente) WordNet: NetworkX
## 



