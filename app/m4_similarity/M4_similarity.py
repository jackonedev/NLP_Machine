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
def similarity_tweets(model:pipeline, topics:list, data:pd.DataFrame, target:str = "content", batching:bool = True) -> list:
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
    
    # vamos a trabajar con 8 batches
    # tamaño de la muestra:
    m = data.shape[0] // 8


    # convert to huggingface dataset for batching
    dataset = Dataset.from_pandas(data)

    # Classify tweets for each target
    res = []
    if batching:
        for result in model(data_stream(dataset, target=target), batch_size=m):
            res.append(result)
    else:
        for result in model(data_stream(dataset, target=target)):
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




































import pandas as pd
from transformers import pipeline
from datasets import Dataset
from tqdm import tqdm

# initialize classifier
classifier = pipeline("zero-shot-classification", model='MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', device = 1, batch_size = 16)

# define data streamer
def data_stream(samples):
    for i in range(samples.num_rows):
        yield samples['text'][i]

# classifier function with batching option
def classify_tweets(targets, labels, label_columns, classifier, data, batching=False):
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

    # Create label column names
    label_col_names = [target + '_lab' for target in targets]
    data = data.copy() # suppress setting with copy warning

    # convert to huggingface dataset for batching
    dataset = Dataset.from_pandas(data) if batching else None

    # Classify tweets for each target
    for i in tqdm(range(len(targets)), desc="Classifying tweets"):
        target = targets[i]
        # define template
        template = 'The author of this tweet {} ' + target +'.'

        if batching:
            samples = dataset.filter(lambda text: text[targets[i]] == 1)
            # Use classifier to get predictions for each sample
            res = []
            for result in classifier(data_stream(samples), labels, hypothesis_template = template, multi_label = False, batch_size = 32):
                res.append(result)
        else:
            # Use classifier to get predictions from list of text samples with the target
            res = classifier(list(data.loc[data[target] == 1, 'text']), labels, hypothesis_template=template, multi_label=False)

        # Add results to dataframe
        data.loc[data[target] == 1, label_col_names[i]] = [label['labels'][0] for label in res]

    # recode results to integers
    for column in tqdm(label_col_names, desc="Re-coding results"):
        data.loc[:,column] = data[column].replace(to_replace = {'supports':-1, 'opposes':1, 'does not express an opinion about': 0})
    
    # Fill NaN values with zero
    data[label_col_names] = data[label_col_names].fillna(0)
    # Create columns for liberal and conservative classifications
    data[label_columns + '_lib'] = [1 if label <= -1 else 0 for label in data[label_col_names].sum(axis = 1)]
    data[label_columns + '_con'] = [1 if label >= 1 else 0 for label in data[label_col_names].sum(axis = 1)]

    return data

# define targets to be classified and labels to use
targets = ['Stewart', 'Oliver', 'Maddow', 'Hayes', 'O\'Donnell', 'Klein', 'Krugman', 'Thunberg']
labels = ['supports', 'opposes', 'does not express an opinion about']

lib_df = classify_tweets(targets = targets, labels = labels, label_columns = 'libmed', classifier = classifier, data = lib_df, batching=False)





























































































##########################################################################################################################################
if __name__ == "__main__":
    
    import time

    MODEL = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    pipeline_iv = pipeline('text-classification', model=model, tokenizer=tokenizer, device=0, top_k=None)#batch_size=16

    df = menu()
    
    file_name = df.name




    user_input = input("presione N para abortar el proceso, cualquier otra tecla para continuar: ")
    if user_input.lower() == "n":
        print("Ejecución interrumpida de forma segura.")
        exit()
    
    # define targets to be classified and labels to use
    start_i = time.time()
    predictions_no_batching = similarity_tweets(pipeline_iv, df, target="content", batching=False)
    # end_i = time.time()
    # predictions = similarity_tweets(pipeline_iv, df, target="content")# dentro de un hilo aparte
    end_ii = time.time()
    
    # print(f"Tiempo de ejecución sin batching: {end_i - start_i}")
    # print(f"Tiempo de ejecución con batching: {end_ii - end_i}")
    print(f"Tiempo de ejecución: {end_ii - start_i}")
    
    
    ## MODULO DE GUARDADO DE DATOS
    #por las dudas
    # file_name = "".join(file_name.split(".")[0])
    try:
        print("guardando datos... en M2_OUTPUT_{}.pickle".format(file_name))
        with open(f"M2_OUTPUT_{file_name}.pickle", "wb") as file:
            pickle.dump(predictions, file)
    except:
        with open("M2_OUTPUT.pickle", "wb") as file:
            pickle.dump(predictions, file)
            print("datos guardados en M2_OUTPUT.pickle")
    
        
    print("Proceso finalizado.")