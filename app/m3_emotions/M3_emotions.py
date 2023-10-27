import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch
from datasets import Dataset




# define data streamer
def data_stream(samples: Dataset, target:str = 'content'):
    for i in range(samples.num_rows):
        yield samples[target][i]
        


# classifier function with batching option
def classify_tweets(model:pipeline, data:pd.DataFrame, target:str = "content") -> list:
    try:
        if isinstance(data, list):
            data = pd.DataFrame(data).T
            data.columns = [target]
    except AttributeError:
        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"
    
    # convert to huggingface dataset for batching
    dataset = Dataset.from_pandas(data)

    res = list()
    for result in model(data_stream(dataset, target=target)):
        res.append(result)

    return res


def emotions_features(predictions:list) -> pd.DataFrame:
# Crear una lista para almacenar los datos de cada columna
  label_columns = []
  score_columns = []
  max_label_column = []

  # Recorrer la lista de predicciones
  for prediction in predictions:
      labels = []
      scores = []
      max_score = 0
      max_label = ''

      # Recorrer cada predicción dentro de la lista
      for pred in prediction:
          label = pred['label']
          score = pred['score']

          labels.append(label)
          scores.append(score)

          # Actualizar la etiqueta con el mayor puntaje
          if score > max_score:
              max_score = score
              max_label = label

      label_columns.append(labels)
      score_columns.append(scores)
      max_label_column.append(max_label)

  # Crear el DataFrame con las columnas correspondientes
  df = pd.DataFrame(
    {'emotions_26_labels': label_columns,
     'emotions_26_scores': score_columns,
     'emotions_26_max_label': max_label_column}
    )

  return df