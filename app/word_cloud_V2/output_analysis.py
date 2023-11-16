## Librerias Nativas de Python y de Terceros
import sys, os, time, ast
from pathlib import Path
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from typing import List


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app_root = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
path_utils = os.path.join(project_root, "app", "word_cloud_utils")
sys.path.insert(0, project_root)


## Aplicaciones propias
from app.main.main import wordcloud
try:
    from app.word_cloud.main import limpieza_txt
    from app.word_cloud.schemas.config_mascara import WordCloudConfig
except:
    from main import limpieza_txt
    from schemas.config_mascara import WordCloudConfig

## Librerías propias
from tools.feed import procesar_file_csv, procesar_file_png


  
def load_resources():
    global remover_palabra, filtrado_palabras
    global content_wc, token_wc

    resources = wordcloud()
    remover_palabra = resources["wordcloud_remover_palabra"]
    filtrado_palabras = resources["wordcloud_filtrado_palabras"]
    
    content_wc = [
        "aclaro vote bullrich decime milei fascista",
        "vote bullrich pedo voto corrupto verbal milei",
        "bullrich señalada alutara asoc legt usuarios armas fuego desarmista peligro l militaron campaña milei piparo cambiemos gestion pesima anmac seguiran apoyando lla",
        "valores ucr",
        "patricia bullrich apoyara javier milei balotaje diferencia socios juntos cambio",
        "mano macri miley bullrich aseguro vos salvas cuidado libertad proponen libertad llenarse guita seria 2da fuga macri olvides pagando entraria represion",
        "bullrich respaldara milei balotaje definira encuentro anoche candidato libertario macri apoyo pro lña libertad avanza significara ruptura juntos cambio",
        "distinto ganar demostro mugre mendigando votantes bullrich aliandose macri destruyo pais dejo deuda enorme seguimos sufriendo fecha tomatela peluca",
        "patricia bullrich apoyara javier milei balotaje diferencia socios juntos cambio",
        "esperando conferencia patricia bullrich apoyara javier milei candidata presidencia viene reunirse integrantes juntos cambio dira minutos juegan viene juntos libertad",
        "radicales antipodas milei bullrich macri justamente luchar ideas politicas nacimos partido causa regimen derechas peligrosamente desinhibidas",
        "casamiento arreglado x macri milei bullrich sincero q tuvimos oposicion sentido radicalismo peronismo aberracion gualeguachu salga salga cartas mesa",
        "baby etchecopar enojado bullrich milei milei coptado cambiemos",
        "señor pida disculpas publicas señora patricia bullrich veremos dueño voto",
        "patricia bullrich luis petri punto anunciar apoyo javier milei estallar pacto juntos cambio radicales resisten sector elisa carrio sostienen apoyaran milei prescindencia libertad",
        "patricia bullrich apoyara javier milei balotaje diferencia socios juntos cambio",
        "patricia bullrich luis petri punto anunciar apoyo javier milei estallar pacto juntos cambio radicales resisten sector elisa carrio sostienen apoyaran milei prescindencia libertad",
        "deberia salir publicamente pedir disculpas dichos señora bullrich dando razones comprensibles armar henkidama",
        "javier milei necesita apoyo bullrich cornejo gente calienta opinion politicos radicalismo pro apoyan perjudicados seran radicalismo pro ceder exigencias apoyar balotaje",
        "patricia bullrich desmarca cargos juntos cambio apoyara javier milei balotaje"
    ]
    
    token_wc = [
        ['gano', 'bullrich', 'ignorante', 'rebaja', 'argentino', 'rebaja', 'elecciones', 'democraticas', 'vergüenza'],
        ['patricia', 'bullrich', 'luis', 'petri', 'hablando', 'representacion', 'apoyan', 'milei', 'patria', 'peligro', 'licito', 'excepto', 'defenderla'],
        ['impresionante', 'discurso', 'patriotico', 'patricia', 'bullrich', 'valiosa', 'presencia', 'luis', 'petri', 'representante', 'radicalismo', 'mendocino', 'neutralidad', 'sirve', 'riesgo', 'libertad', 'muerte'],
        ['habla', 'patricia', 'bullrich', 'patria', 'peligro', 'critica', 'cfk', 'milei', 'diferencias', 'obligacion', 'neutrales', 'ayer', 'reunio', 'libertario', 'perdonamos', 'mutuamente'],
        ['diluvio', 'lloriqueo', 'rojetes', 'argentinos'],
        ['impresionante', 'discurso', 'patriotico', 'patricia', 'bullrich', 'valiosa', 'presencia', 'luis', 'petri', 'representante', 'radicalismo', 'mendocino', 'neutralidad', 'sirve', 'riesgo', 'libertad', 'muerte'],
        ['patricia', 'gato', 'macri', 'acaban', 'estrellar', 'juntos', 'faltaba'],
        ['bullrich', 'adelante', 'elecciones', 'demuestran', 'irresponsabilidad', 'populismo', 'ganar', 'eleccion', 'politico', 'sucido', 'compartimos'],
        ['bullrich', 'termino', 'firmar', 'ruptura', 'jxc', 'declaracion', 'penosa', 'espero', 'radicalismo', 'deje', 'tirada', 'separe', 'vergüenza', 'postura'],
        ['bullrich', 'acaba', 'concepto', 'liberalismo', 'encuentro'],
        ['bullrrich', 'patria', 'peligro', 'milei', 'estaremos', 'peligro', 'decepcionaste', 'despues', 'denigrante', 'milei'],
        ['confio', 'patricia', 'bullrich', 'radicalismo', 'carrio', 'ricardito', 'alfonsin', 'abajo', 'trabajaron', 'kichnerismo', 'sigo', 'republica', 'corrupcion'],
        ['jajajajaja', 'saluden', 'milei', 'brazo', 'bullrich'],
        ['habra', 'ofrecido', 'miley', 'bullrich', 'diga', 'apoya', 'regalo', 'armado', 'seguramente', 'lla', 'pierde', 'diputados', 'tambien', 'pierde', 'coherencia', 'politica', 'tranza', 'casta'],
        ['bullrich', 'argentina', 'cfk', 'argentinos', 'unimos', 'terminar', 'preso'],
        ['campaña', 'milei', 'patricia', 'bullrich', 'correcto', '19', '11', 'juntos', 'sacar', 'peor', 'tuvo'],
        ['millon', 'socialismo', 'radicalismo', 'santafesino', 'fingir', 'demencia', 'elecciones', 'nacionales', 'unirse', 'bullrich', 'apoyaran', 'milei', 'basado', 'quita', 'autoritarismo', 'privatizacion', 'habitan'],
        ['millon', 'socialismo', 'radicalismo', 'santafesino', 'fingir', 'demencia', 'elecciones', 'nacionales', 'unirse', 'bullrich', 'apoyaran', 'milei', 'basado', 'quita', 'autoritarismo', 'privatizacion', 'habitan'],
        ['bullrich', 'resolvieron', 'apoyar', 'milei', 'elecciones', 'presidenciales', 'patria', 'peligro', 'permitido', 'defenderla', 'libertad', 'kichnerismo']
    ]



def main_df(dataframe:List[pd.DataFrame]) -> List[plt.figure]:
    from app.main.main import wordcloud
    
    load_resources()
    nombre = dataframe[0].name


# CREATING BATCHES
#######################################################################################
    ## Creating Mocking Data
    batch = [content_wc, token_wc]
    # Verifying data consistency
    assert type(batch) == list, "El archivo pickle no es un list."
    assert len(batch) > 0, "El archivo pickle está vacío."
        

    if len(batch) == 2:
        token = True
        batch_content, batch_token = batch

    elif len(batch) == 1:
        token = False
        batch_content = batch[0]

    else:
        print("DataError. Missmatch structure.")
        print("Finishing interpreter.")
        sys.exit(0)
#######################################################################################



    #  IMPORT CONFIGURATION FROM LOCAL FILE
    # Create wc_params dict from txt file
    with open(os.path.join(path_utils, "wordcloud_mask_config.txt"), "r", encoding="UTF-8") as file:
        wc_params = file.read()

    try:
        wc_params = ast.literal_eval(wc_params)
        wc_params["mascara"] = Path(os.path.join(path_utils, wc_params["mascara"]))

        ## PYDANTIC VALIDATION SCHEMA 
        validation_schema = WordCloudConfig(**wc_params)
        try:# (for V1)
            wc_parmams = validation_schema.dict()
        except:# (and V2)
            wc_parmams = validation_schema.model_dump()
        
        #TODO: El input inicial es una lista de DataFrame
        # por lo tanto, para aplicar cualquier configuración
        # por default, es necesario crear una objeto que 
        # contenga la configuraciones particulares para cada
        # DataFrame de la lista.
        
        # HARDCODED
        # Default configuration in function of pd.DataFrame(...).name attribute
        if nombre.split("-")[-1] in ["positive", "negative"]:
            if nombre.split("-")[-1] == "positive":
                wc_params["color_func"] = (84, 179, 153)
            elif nombre.split("-")[-1] == "negative":
                wc_params["color_func"] = (231, 102, 76)
        if False:
            print("Definir objeto que contenga las configuraciones definitivas \
                para cada DataFrame en función de su atributo 'name'")

    except Exception as e:
        print("Error en el formato del archivo de configuración.")
        print(e)
        print("Ejecución interrumpida de forma segura.")
        exit()# DRY

    ## Open .png file with mask shape
    ## Update wC_params dict
    #TODO: reeplace for contex manager
    try:
        print(f"Implementando configuración con Máscara: {wc_params['mascara']}")
        mascara_wordcloud = np.array(Image.open(wc_params["mascara"]))
        wc_params.pop("mascara")
    except FileNotFoundError as e:
        print("VARIABLE ANULADA: No se encontró el archivo de máscara.")


    

    ### LIMPIEZA ITERATIVA DEL BATCH  ###
    # usuario, ingresar si desea aplicar filtro de palabras
    # user_input = input("¿Aplicar filtro de palabras? [n/Y]: n\n")
    user_input = "y"
    if user_input.lower() == "y":#TODO: if df.name.split.sarasa :
        # sistema, leer archivos txt de configuracion y correr modulo de filtrado
        file = "eliminar_palabras_que_comiencen_con.txt"
        if os.path.isfile(os.path.join(path_utils, file)):
            eliminar_palabras = limpieza_txt(path_utils, file)
        else:
            if False:
                print("No se encontró el archivo 'eliminar_palabras_que_comiencen_con.txt' en el directorio de APP_utils")
            eliminar_palabras = []
        
        file = "eliminar_palabras_wordcloud.txt"
        if os.path.isfile(os.path.join(path_utils, file)):
            filtrar_palabras = limpieza_txt(path_utils, file)
        else:
            if False:
                print("No se encontró el archivo 'eliminar_palabras_wordcloud.txt' en el directorio de APP_utils")
            filtrar_palabras = []
            
        # sistema, aplicar filtros
        batch_content = remover_palabra(batch_content, eliminar_palabras)
        batch_content = filtrado_palabras(batch_content, filtrar_palabras)

        if False:
            print(f"\nEliminadas palabras: {eliminar_palabras}\nFiltradas palabras: {filtrar_palabras}\n")
    
    ####################################################################################

    ###  IDENTIFICACION DEL ULTIMO WORDCLOUD CREADO  ###
    # sistema, verificar la existencia de archivos de salida previos
    output_files = os.listdir(output_dir)
    output_files = [file for file in output_files if file.endswith(".png")]
    if len(output_files) == 0:
        N = 1
    else:
        N = [elemento.split("_")[-1] for elemento in output_files]
        N = [elemento.split(".")[0] for elemento in N]
        N = [int(elemento) for elemento in N if elemento.isdigit()]
        N = max(N) + 1

    output_name = f"wordcloud_{nombre}_{N}"  
    output_name = os.path.join(output_dir, output_name)



    ###  MODULO DE WORDCLOUD  ###
    if "colormap" in wc_params.keys() and wc_params["colormap"] != "":
        wc_params.pop("color_func")
    else:
        color_tuple = wc_params["color_func"]
        color_func = lambda *args, **kwargs: color_tuple
        wc_params.pop("color_func")

    # 1ra visualizacion: token
    if token:
        with open(os.path.join(output_dir,'unique_batch_token.txt'), 'w', encoding="UTF-8") as f:
            f.write("\n".join(list(set(batch_token))))

        word_cloud = " ".join(batch_token)

        
        wordcloud = WordCloud(
            mask=mascara_wordcloud,
            collocations=False,
            contour_width=1.0,
            **wc_params)
        if not "colormap" in wc_params.keys():
            wordcloud.color_func=color_func
            wordcloud.contour_color = color_tuple
        else:
            wordcloud.contour_color = (0, 0, 0)
        
        
        wordcloud.generate(word_cloud)
        wordcloud.to_file(f"{output_name}_token.png")


    # 2da visualizacion: content
    print(f"\nWordCloud Nº {N} de {nombre}\n")

    plt.figure(figsize=(20,8))

    word_cloud = ""
    for row in batch_content:
        row += " "
        word_cloud+= row



    # descargar en txt un listado de tokens únicos (no considera cantidad)
    with open(os.path.join(output_dir,'unique_batch_content.txt'), 'w', encoding="UTF-8") as f:
        f.write("\n".join(list(set(word_cloud.split(" ")))))


    # fecha: 23/10
    ###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)
    ###TODO: HARDCODED | contour_width: float (default=0) | contour_color: color value (default=”black”)

    ## Se cambia el mode de RGBA a RGB y se cambia el background color
    # se añaden las lineas de contorno y color del contorno

    wordcloud = WordCloud(
        mask=mascara_wordcloud,
        collocations=False,
        contour_width=1.0,
        **wc_params)
    
    ## si existe colormap. no existe contour
    if not "colormap" in wc_params.keys():
        wordcloud.color_func=color_func
        wordcloud.contour_color = color_tuple
    else:
        wordcloud.contour_color = (0, 0, 0)

    
    wordcloud.generate(word_cloud)
    wordcloud.to_file(f"{output_name}.png")
        

    # descargar txt con wc_params
    try:
        wc_params["color_func"] = color_tuple
    except:
        pass
        
    with open(os.path.join(output_dir, f"{output_name}.txt"), 'w', encoding="UTF-8") as f:
        f.write(str(wc_params))

    
    print("programa finalizado exitosamente.")
    print(f"Archivo guardado: {output_name}.png")
        







