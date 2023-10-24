
import tiktoken
import unicodedata
import re
from nltk.tokenize import word_tokenize
## Librerias Nativas de Python y de Terceros
import sys, os, time, pickle

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
sys.path.insert(0, project_root)

from tools.feature_adjust import eliminar_caracteres_no_imprimibles
#######################################################################
"""
TOKENIZADOR POR TIKTOKEN

AHORRO DE TIEMPO DE PROCESAMIENTO:
    - eliminar tildes
    - pasar todo a minusculas no afecta a los nombre propios pero si a la palabra "Conclusion". Con clus ion vs conclus ion
    - eliminar las palabras escritas todas en mayúsculas
    
ETAPAS:
    - TOKENIZADOR I vs RegEx: word_tokenize
        - no contempla multiples espacios en blanco
    - NOMBRES PROPIOS: Extraer muestras de palabras con primera letra mayúscula
    - PROCESAMIENTO: Remover tildes y pasar todo a minúsculas
    - 
""";

# CONTENT
texto = "José Jose jose     Patricia -Bullrich PATRICIA-BULLRICH (patricia) bullrich !!!!!! Este es otro ejemplo de tokenizadorrrrr tokenizador basado!! en palabras. Conclusión. Conclusion. conclusion conclusión"


# PREPROCESSING
tokens = word_tokenize(texto)
texto_procesado = eliminar_caracteres_no_imprimibles
regex = re.sub("\s+", " ", texto)

print("Tokenizado de palabras I:", tokens)
print("Tokenizador de palabras II:", regex.split(" "))


# TIKTOKEN
encoding_base = tiktoken.get_encoding("cl100k_base")


texto_tokenizado = encoding_base.encode(texto)

print("Texto tokenizado de forma numérica I:", texto_tokenizado)

texto_decodificado = [encoding_base.decode_single_token_bytes(token) for token in texto_tokenizado]

print("Texto decodificado I:", texto_decodificado)


texto_decodificado = [token.decode('UTF-8') for token in texto_decodificado]

print("Texto decodificado II:", texto_decodificado)


print(tuple(zip(texto_tokenizado, texto_decodificado)))
