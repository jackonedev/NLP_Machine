import unicodedata, re
from typing import List


def tratamiento_i(content: str) -> str:
    """Etapas preprocesamiento:
    - Eliminación de caracteres no imprimibles
    - Reemplazo de caracteres por espacios en blanco
    - Reestructuración de texto para eliminar multiples espacios en blanco
    """
    cleaned_content = ''.join(
        ' ' if c in "&'()*+‘<=>[]^`{|}~ýª!?¿¡.,/⁉️‼:\"-;" else c
        for c in content
    )
    return re.sub("\s+", " ", cleaned_content)

def tokenizador_preprocesamiento(batch: List[str]) -> list:
    assert isinstance(batch, list), "El argumento batch debe ser una lista"
    assert isinstance(batch[0], str), "El argumento batch debe ser una lista de strings"
    
    batch = [tratamiento_i(content) for content in batch]
    return batch


def eliminacion_tildes(content: str) -> str:
    # cleaned_content = ''
    # for c in content:
        
    #     if c in 'áéíóúÁÉÍÓÚáéíóúÁÉÍÓÚó':
    #         cleaned_content += unicodedata.normalize('NFD', c)[0]
    #     elif c in ['ñ', "Ñ"]:
    #         cleaned_content += c
    #     else:
    #         cleaned_content += c
    # return cleaned_content
    return ''.join(
        unicodedata.normalize('NFD', c)[0]
        if c in 'áéíóúÁÉÍÓÚáéíóúÁÉÍÓÚó'
        else c
        for c in content
    )


def tokenizador_procesamiento(batch: list) -> list:
    assert isinstance(batch, list), "El argumento batch debe ser una lista"
    assert isinstance(batch[0], str), "El argumento batch debe ser una lista de strings"

    
    batch = [eliminacion_tildes(content) for content in batch]
    batch = [content.lower() for content in batch]
    
    return batch

            




# def correccion_de_palabras(content: str) -> str:
#     "Anulado: no responde como lo eperado"
#     from spellchecker import SpellChecker
#     corrector_palabras = SpellChecker(language='es')
#     correcciones = []
#     for token in content.split(' '):
#         # Verificar si la palabra está mal escrita
#         if corrector_palabras.correction(token) != token:
#             # Corregir la palabra
#             corrected_token = corrector_palabras.correction(token)
#             correcciones.append(corrected_token)
#         else:
#             correcciones.append(token)
#     return correcciones




if __name__ == "__main__":
    texto = "José Jose joseeee     Patricia! -Bullrich PATRICIA-BULLRICH (patricia) bullrich\
        !!!!!! Este es otro ejemplo de tokenizadorrrrr tokenizador basado!! en palabras.\
            Conclusión. Conclusion. conclusion conclusión"
            
    print("tratemiento_i")
    print(tratamiento_i(texto))
    # print("correccion palabras")
    # print(correccion_de_palabras(texto))
    print("preprocesamiento")
    batch = tokenizador_preprocesamiento([texto])
    print(batch)
    
    print("procesamiento")
    print(tokenizador_procesamiento(batch))
    