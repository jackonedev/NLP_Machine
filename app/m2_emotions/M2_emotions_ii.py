import sys, os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
sys.path.insert(0, project_root)

# modelo 6 emociones: daveni/twitter-xlm-roberta-emotion-es
# emociones: sadness, anger, surprise, joy, disgust, fear + others

#
# ======================================================================================================================
# from transformers import pipeline
# classifier = pipeline("text-classification",model='daveni/twitter-xlm-roberta-emotion-es', top_k=None)
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# https://github.com/huggingface/transformers/issues/22387
# Es buenísimo:
# MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli

import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from datasets import Dataset
from tqdm import tqdm
import numpy, pickle


#warning# Rompiendo el diseño de la arquitectura
try:
    from app.main.shared_resources_feed import menu
except:
    from main.shared_resources_feed import menu



# define data streamer
def data_stream(samples: Dataset, target:str = 'content'):
    for i in range(samples.num_rows):
        yield samples[target][i]




# classifier function with batching option
def classify_tweets(model:pipeline, data:pd.DataFrame, target:str = "content") -> list:
    """
    Classify tweets based on given targets and labels using a HuggingFace pipeline.

    Args:
    - targets: list of targets in the data frame that will be classified
    - labels: list of labels that will be passed to the template
    - label_columns: name of the label columns
    - classifier: HuggingFace pipeline object
    - data: pandas DataFrame that contains the tweets to classify
    - batching: whether to use batching or not

    Returns:
    - pandas DataFrame with modified columns

    """

    # # Create label column names # HARDCODED
    # label_col_names = ["sadness", "anger", "surprise", "joy", "disgust", "fear", "others"]

    try:
        if isinstance(data, list):
            data = pd.DataFrame(data).T
            data.columns = [target]
    except AttributeError:
        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"
        


    # convert to huggingface dataset for batching
    dataset = Dataset.from_pandas(data)

    # Classify tweets for each target
    res = []
    for result in model(data_stream(dataset, target=target)):#), batch_size = 32):
        res.append(result)

    # # recode results to integers
    # for column in tqdm(label_col_names, desc="Re-coding results"):
    #     data.loc[:,column] = data[column].replace(to_replace = {'supports':-1, 'opposes':1, 'does not express an opinion about': 0})
    # # Fill NaN values with zero
    # data[label_col_names] = data[label_col_names].fillna(0)
    # # Create columns for liberal and conservative classifications
    # data[label_columns + '_lib'] = [1 if label <= -1 else 0 for label in data[label_col_names].sum(axis = 1)]
    # data[label_columns + '_con'] = [1 if label >= 1 else 0 for label in data[label_col_names].sum(axis = 1)]
    

    return res



if __name__ == "__main__":

    MODEL = "02shanky/finetuned-twitter-xlm-roberta-base-emotion"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    pipeline_i = pipeline('text-classification', model=model, tokenizer=tokenizer, device=0, top_k=None)#batch_size=16

    df = menu()

    user_input = input("presione N para abortar el proceso, cualquier otra tecla para continuar: ")
    if user_input.lower() == "n":
        print("Ejecución interrumpida de forma segura.")
        exit()
    
    # define targets to be classified and labels to use
    predictions = classify_tweets(pipeline_i, df, target="content")
    
    with open("M2_OUTPUT.pickle", "wb") as file:
        pickle.dump(predictions, file)
        
    print("Proceso finalizado.")