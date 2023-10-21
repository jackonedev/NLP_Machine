import re
import spacy
import pandas as pd


## PREVIAMENTE SE DEBE INSTALAR ESTE MODELO POR TERMINAL: 
## python -m spacy download es_core_news_sm


# Cargar el modelo de spaCy para el español
nlp = spacy.load('es_core_news_sm')



##  IMPLEMENTAR STOP WORDS
stopword_sample = {"nombre_muestra": pd.DataFrame()}## aca adentro tengo algo un dataframe
# corpus_sample = {}
# for label in list(stopword_sample.keys()):
#     corpus_sample[label] = []
#     ## agregar un if que si el batch tiene menos de 100 registros no se ejecute
#     if len(stopword_sample[label]) < 100:
#         continue

#     for contenido in stopword_sample[label]:
#         doc = nlp(contenido)
#         corpus_sample[label].append(" ".join([token.text for token in doc if not token.is_stop]))



def tokenize(text):
    tokens = [word for word in text.split(" ")]
    return tokens



def tokenizador(batch):
    "Tokenizador para la nube de palabras"
    stopword_batch = []
    for comentario in batch:
        # Verificar que el tweet tenga al menos 2 palabras
        comentario = comentario.strip()
        
        # extract everything that isn't a word
        comentario = re.sub(r"[^\w\s ñ]", "", comentario) ## verificar no perder las ñ
        
        comentario = comentario.lower()
        # remover tildes
        
        
        tokens = tokenize(comentario)
        if len(tokens) < 2:
            continue
        
        
        lista_palabras = comentario.split()
        
        # remove words with less than 4 characters
        lista_palabras = [palabra for palabra in lista_palabras if len(palabra) >= 4]
        
        ## Palabras a remover de forma manual
        lista_nombres = ["uñac", "sergio", "juan", "sanjuanino"]
        lista_stopwords = ["pais", "años", ]
        lista_palabras_raras = ["jaja", "jajaja", "jajajaja"]
        lista_palabras_comunes = ["provincia", "gobernador", "gobierno", "dios", "gobierno", "bendicione","bendiciones", "gente"]
        
        if not lista_palabras:
            continue
        
        # remove digits
        lista_palabras = [palabra for palabra in lista_palabras if not palabra.isdigit()]
        # remove names
        lista_palabras = [palabra for palabra in lista_palabras if palabra not in lista_nombres]
        # # remove stopwords
        lista_palabras = [palabra for palabra in lista_palabras if palabra not in lista_stopwords]
        # # remove rare words
        lista_palabras = [palabra for palabra in lista_palabras if palabra not in lista_palabras_raras]
        # # remove common words
        lista_palabras = [palabra for palabra in lista_palabras if palabra not in lista_palabras_comunes]
        stopword_batch.append(" ".join(lista_palabras))

    ### CHECKPOINT
    ### INFO: A PARTIR DE ACÁ PERDERIAMOS SINCRONICIDAD CON LOS IDS SI SE LLEGASE A CAMBIAR LA LONGITUD DEL BATCH
    print(f"longitud del batch: {len(stopword_batch)}")
    return stopword_batch



def procesamiento_parrafo(batch):
    "letra por letra"
    tokens = []
    ### WARNING: ESTE BUCLE REQUIERE OPTIMIZACIÓN
    ### Busqueda letra por letra - util si vamos a traducir en caso de detectar caracteres extraños
    # from tools.tokenizador import eliminar_caracteres_no_imprimibles, contiene_caracteres_alfabeticos
    cleaned_text = "" ### IMPLEMENTACION MINUCIOSA NO REALIZADA -letra por letras - estorba
    for word in tokens:
        for char in word:
            if char.isdigit():
                continue
            # if char in ["a","e","i","o","u"]: ## resolver "democraciaaaaaa"
            # existe alguna palabra que lleve silabas idénticas consecutivas? uu aa ee ii oo?
            #     continue
    return False



print("Tokenizador para nubes de palabras.\n")