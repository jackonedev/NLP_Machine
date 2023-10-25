
import tiktoken
import unicodedata
import re
from nltk.tokenize import word_tokenize
## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
sys.path.insert(0, project_root)


from tools.tokenizer import preprocesamiento, procesamiento
from tools.extraccion_muestras import nombres_propios

#######################################################################
"""
TOKENIZADOR POR TIKTOKEN

AHORRO DE TIEMPO DE PROCESAMIENTO:
    - eliminar tildes
    - pasar todo a minusculas no afecta a los nombre propios pero si a la palabra "Conclusion". Con clus ion vs conclus ion
    - eliminar las palabras escritas todas en mayúsculas

CASO EMOJIS



ETAPAS PREPROCESAMIENTO:
    -1- Eliminacion de caracteres no imprimibles
    -2- Tratemiento para los guiones medios "-"
    -3- Tratamiento de múltiples espacios en blanco
    -4- Extracción de muestras de nombres propios
    -5- Eliminación de tildes y pasar todo a minúsculas
    -6- Extraccion de Emojis
    

ETAPAS TOKENIZADOR:
    -6- Tokenizar
    -7- aplicar filtro miss-spelling
    
    
""";

# CONTENT
texto = "hola José Jose jose     Patricia -Bullrich PATRICIA-BULLRICH (patricia) bullrich !!!!!! Este es otro ejemplo de tokenizadorrrrr tokenizador basado!! en palabras. Conclusión. Conclusion. conclusion conclusión"


# PREPROCESSING
batch = [texto, "Hola Mundo!", "bastaaaaaaa", "massa vuelvo pais hijos 🙏 🙏"]
batch = preprocesamiento(batch)
# extracción de nombres propios
i_nombre_propios = nombres_propios(batch)
# eliminación de tildes y pasar todo a minúsculas
batch = procesamiento(batch)


# TIKTOKEN
encoding_base = tiktoken.get_encoding("cl100k_base")


texto_tokenizado = [encoding_base.encode(content) for content in batch]
texto_decodificado_bytes = [[encoding_base.decode_single_token_bytes(token) for token in content] for content in texto_tokenizado]
# texto_decodificado_str = [token.decode('UTF-8') for token in texto_decodificado_bytes]

texto_decodificado_bytes




# print("Texto tokenizado de forma numérica I:", texto_tokenizado)


# print("Texto decodificado I:", texto_decodificado)



# print("Texto decodificado II:", texto_decodificado)


# print(tuple(zip(texto_tokenizado, texto_decodificado)))
print("programa finalizado de forma exitosa")