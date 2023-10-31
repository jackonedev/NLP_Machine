# CONFIGURACION DE COLORES

colors_sentiment = {
    "sentiment_i_negative": "#e7664cff",
	"sentiment_i_neutral": "#2261aa",
	"sentiment_i_positive": "#54b399ff"
 }

amarillo = "#FFFF00"
rosa = "#e926b0"
gris = "#7a9c7d"
verde = "#00FF00"
violeta = "#473b9e"
azul = "#0000ff"
rojo= "#FF0000"

colors_emotions_6 = {
    "emotions_6_max_label_anger": rojo,
    "emotions_6_max_label_fear": azul,
    "emotions_6_max_label_joy":amarillo,
    "emotions_6_max_label_love":verde,
    "emotions_6_max_label_sadness": azul,
    "emotions_6_max_label_surprise":amarillo
    }

azul_miedo_desagrado = "#473b9e"
rosa_aversion_duda = "#ea76e5"
rojo_tension_entusiasmo = "#901f31"
amarillo_satisfaccion_valor = "#d5d432"
verde_altivez_deseo = "#9cf581"
verde_amor_certeza = "#4bb710"
celeste_calma_aburrimiento = "#80c0ea"
celeste_apatia_tristeza = "#53b7d9"

colors_emotions_28 = {
    "emotions_26_max_label_neutral": celeste_calma_aburrimiento,
    "emotions_26_max_label_approval": amarillo_satisfaccion_valor,
    "emotions_26_max_label_realization": amarillo_satisfaccion_valor,
    "emotions_26_max_label_caring": verde_amor_certeza,
    "emotions_26_max_label_curiosity": rosa_aversion_duda,
    "emotions_26_max_label_confusion": rosa_aversion_duda,
    "emotions_26_max_label_disapproval": celeste_apatia_tristeza,
    "emotions_26_max_label_desire": verde_altivez_deseo,
    "emotions_26_max_label_annoyance": celeste_calma_aburrimiento,
    "emotions_26_max_label_gratitude": amarillo_satisfaccion_valor,
    "emotions_26_max_label_excitement": rojo_tension_entusiasmo,
    "emotions_26_max_label_pride": verde_altivez_deseo,
    "emotions_26_max_label_remorse": celeste_apatia_tristeza,
    "emotions_26_max_label_disappointment": celeste_apatia_tristeza,
    "emotions_26_max_label_relief": celeste_calma_aburrimiento,
    "emotions_26_max_label_admiration": verde_altivez_deseo,
    "emotions_26_max_label_anger": rojo_tension_entusiasmo,
    "emotions_26_max_label_amusement": amarillo_satisfaccion_valor,
    "emotions_26_max_label_embarrassment": azul_miedo_desagrado,
    "emotions_26_max_label_joy": verde_altivez_deseo,
    "emotions_26_max_label_surprise": rojo_tension_entusiasmo,
    "emotions_26_max_label_nervousness": rojo_tension_entusiasmo,
    "emotions_26_max_label_love": verde_amor_certeza,
    "emotions_26_max_label_sadness": celeste_apatia_tristeza,
    "emotions_26_max_label_grief": rosa_aversion_duda,
    "emotions_26_max_label_disgust": azul_miedo_desagrado,
    "emotions_26_max_label_optimism": verde_altivez_deseo,
    "emotions_26_max_label_fear": azul_miedo_desagrado}

colores = colors_sentiment | colors_emotions_6 | colors_emotions_28

if False:
    print("colores modelos M1, M2, M3:", colores)