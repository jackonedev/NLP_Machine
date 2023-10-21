from app.main.creacion_features import eliminar_caracteres_no_imprimibles
import tiktoken

### 0. Cargar muestra y modelos ###
encoding_base = tiktoken.get_encoding("cl100k_base")
muestra = [
        "@fargosi todo de tu gobierno , viejo meado y defensor de un abusador y degenerado como Melconian!",
        "Larreta es mejor que Milei",
        "Si el audio es verdadero y todo lo que dice es cierto, yo no puedo entender a la gente que sigue votando a JXC, yo entiendo que quieran votar a un gobernador y/o intendente de JXC, pero Bullrich uy su equipo son un desastre, Milei Presidente ",
        "Espert, Macri, Bullrich sub mejores que Milei",
        "Frente a toda esta angustia quiero darte tranquilidad. "
    ]

###  1. Quitar tildes, conservar simbolos  ###
for i in range(len(muestra)):
    muestra[i] = eliminar_caracteres_no_imprimibles(muestra[i], conservar_simbolos=True)

###  2. Tokenizar  ###
muestra_tokenizada_i = []
for parrafo in muestra:# sigue siendo una sola iteracion
    muestra_tokenizada_i.append(encoding_base.encode(parrafo))


###  3. Expresar en bytes  ###
muestra_bytes_i = []
for parrafo in muestra_tokenizada_i:
    muestra_bytes_i.append([encoding_base.decode_single_token_bytes(token) for token in parrafo])    

###  4. Decodificacion y Preprocesamiento  ###
tokens_i = [] # hace referencia a tokens_independientes
tokens_c = [] # hace referencia a tokens_compuestos

for ix in range(len(muestra_bytes_i)):
    cache = []
    last_token = ""
    for i, token in enumerate(muestra_bytes_i[ix]):
        
        # DECODIFICACION
        try:
            token = token.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"Error de decodificación: {e}")
            continue                
        
        # TRATAMIENTO PRIMERA PALABRA
        if i == 0:# REVISAR
            tokens_i.append(token)
            last_token = token
            continue
        
        ##  MODULO DE PALABRAS COMPUESTAS POR VARIOS TOKENS  ##
        if not token.startswith(" ") and last_token.startswith(" "):
            cache.append(last_token)#primer token compuesto
        elif not token.startswith(" ") and not last_token.startswith(" "):
            cache.append(last_token)# caso entre medio
        elif token.startswith(" ") and not last_token.startswith(" ") and i != 1:#TODO: buscar un caso que la primera palabra sea compuesta "Bienvenidos" "Gracias" "Estimados"
            cache.append(last_token)# caso ultimo token
            tokens_c.append("".join(cache).strip())
            cache = []
            last_token = token
            continue

        ##  MODULO DE PALABRAS COMPUESTAS POR UN UNICO TOKEN  ##
        if token.startswith(" ") and last_token.startswith(" "):
            if len(last_token.strip()) < 3:#
                last_token = token
                continue
            tokens_i.append(last_token.strip())

        last_token = token

    if cache:
        tokens_c.append("".join(cache).strip())
        cache = []


        
TOKENS = tokens_i + tokens_c
with open("outputs/tokens/tokens.txt", "w") as f:
    f.write("\n".join(TOKENS))