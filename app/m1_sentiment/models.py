import torch
from transformers import AutoModelForTokenClassification, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer, AutoModel
from transformers import AutoConfig, AutoModelForSequenceClassification
from transformers import XLMRobertaForCausalLM
from transformers import pipeline


# REEMPLAZAR LAS HEAD PERSONALIZADAS POR Transformers.AutoModel.from_pretrained()

#### copiado y pegado
classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)
prediction = classifier(data[-1],)
#### 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

try:
    num_gpus = torch.cuda.device_count()
    for ix in range(0, num_gpus):
        # select the latest recognized gpu
        device_id = 'cuda:{}'.format(ix)
        device = torch.device(device_id)
        print("GPU disponible, otorgada mediante el id: {}".format(device_id))

except:
    print("Esto debería imprimirse si no existen GPUs disponibles")

# MODELO 1: Analisis de sentimiento
twitter_sa_multilingual = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
pipeline_i = pipeline("sentiment-analysis",
                      model=twitter_sa_multilingual, tokenizer=twitter_sa_multilingual, device=device)


def model_pipeline_i(batch, **kwargs):
    "Modelo de clasificación de Sentimientos"
    prediction = pipeline_i(batch, **kwargs)
    return prediction


# MODELO 4: emotions
twitter_emotion_multilingual = "daveni/twitter-xlm-roberta-emotion-es"
pipeline_iv = pipeline("sentiment-analysis",
                       model=twitter_emotion_multilingual,
                       tokenizer=twitter_emotion_multilingual,
                       framework="pt", device=device)


def model_pipeline_iv(batch: list, **kwargs):
    "Modelo de clasificación de emociones"
    return pipeline_iv(batch, **kwargs)


# PENDIENTE
# # MODELO 2: NER 1 (light) ADJ Y SUST
# ner_model_i = "QCRI/bert-base-multilingual-cased-pos-english"
# tokenizer_ner_model_light = AutoTokenizer.from_pretrained(ner_model_i)
# model_ner_model_light = AutoModelForTokenClassification.from_pretrained(ner_model_i)

# # ADDITIONAL FEATURE: NLTK PREVIO A LA TRADUCCION
# # MODELO 2-1: TRADUCTOR
# model_traductor = "Helsinki-NLP/opus-mt-es-en"
# tokenizer_ner_model_big = AutoTokenizer.from_pretrained(ner_model_big)
# model_ner_model_big = AutoModelForSeq2SeqLM.from_pretrained(ner_model_big)


# PENDIENTE: #TODO: renombrar variables, asegurarse que el modelo tenga el HEAD correcto
# MODELO 3: NER 2 PERSONAS Y LUGARES
# ner_model_ii = "Davlan/distilbert-base-multilingual-cased-ner-hrl"
# tokenizer_ner_model_big = AutoTokenizer.from_pretrained(ner_model_big)
# model_ner_model_big = AutoModelForSeq2SeqLM.from_pretrained(ner_model_big)
if __name__ == "__main__":

    batch = ['atinadas declaraciones del gobernador uñac muy seductor el compa lo noto candidato repuesto ',
             'tarde habilitaron las urnas en l escuela mariano necochea a las 9 primero se dedicaron a desayunar pusieron como escusas q haban urnas mentiraaaaa desfilaban los termos de caf y tortitas',
             ' el chanta de uñac, no me gusta el fallo de la corte habra que acatar y promover un cambio en la constitucin provincialarrobandose el hecho de ser abogadobuscan que el feudo sea eternomejor que devuelva el titulo sr!gobiernocorruptocriminalymentiroso',
             'un abrazo y mucha fuerza para fdanivareseci fnicomendezpoi y todos los compañeros del fit san juanito que estn peleando contra los punteros que roban las boletas y la eleccin fraudulenta de sergio uñac httpstcojqg6rz8pfe',
             'uñac dice que aunque sea gobernador eso no cuenta para contar como vicegobernador, claro, entonces él va de vice, el gobernador renuncia y sigue, es ridculo el planteo',
             'los de todonoticias no se horrorizan de que sergiounac est rompiendo la veda, hablando mal de la corte, juntoscambioar y la poderjudicialpy ? q loco todo! porque si hubiera sido alguien de la oposicin estaran rasgndose las vestiduras pero ya sabemos quien los sponsorea',
             'urgente hay que ver si me sacan del campeonato sergio uñac hizo una analoga entre el deporte, y su candidatura a gobernador por su tercer mandato y la suspensin de la corte suprema por ahora estoy suspendido, hay que ver si me sacan del campeonato, dijo el actual mandatario sanjuanino lo tendran que sacar?',
             'sergiounac una provincia tan linda con polticos tan corruptos andate uñac',
             'la constitucin me habilita un perodo ms, palabra del gobernador sergio uñaceleccionensanjuan',
             'que chanta que es uñac no pens que fuese tan mamarracho escuchen lo que dice es massa con tonada sanjuanina',
             'muy atinadas declaraciones del gobernador uñaces muy seductor el compalo noto centrado y candidato ',
             'uñaccreo que la justicia se va a expedirest eliminada la inabilidadtom el camino de acatar el fallova a haber una cmara conformada y no un gobernadorfue una medida extemporneasanjuan',
             'queridas madres, en empastados el veloz queremos celebrar el inmenso amor y la dedicacin que brindan a sus hijos d7diadelamadre2023 diadelasmadres felizdiadelasmadres felizdiadelamadre lamejormama teamo elveloz universidad ucv ulima unfv up uni unac utp httpstcowlgvvqziwc',
             'sanjuan  lleg el gobernador sergio uñac sergiounacl la provincia solo elige las bancas de la legislatura provincial, las intendencias y sus concejos deliberantes3 gonzalofprado httpstcox4deco2hqr',
             'eleccionesahora en sanjuan uñac, gobernador, declara antes de votar mucha expectativa, hemos cumplido el fallo de cortesomos respetuosos hombres de derechoyo creo en la justiciaeleccin a gobernador suspendidase vota intendentes, concejales, diputados',
             'sergiounac c5n por favor el señor est diciendo que hay veda y que no puede hablar, basta de culpar a mauriciomacri basta de hablar de la justicia, hay que trabajar por y para el pueblo',
             'el gobernador uñac, cuando le preguntaron si est proscritpo estoy suspendido por un par de fechas, pero creo en la justicia',
             'uñac estuviste llorando toda la semana nunca en tu vida saliste tanto en la tele y siempre llorando      ',
             'tiene pinta de chanta uñac poco serio lanacion todonoticias',
             'un papelón las declaraciones de uñac novaresio tendra que dar explicaciones']  # shape(150k, 1)

    with torch.no_grad():
        results = model_pipeline_i(batch)
        # results = model_pipeline_iv(batch)
        print(results)
