from bokeh.plotting import figure

import pandas as pd
import numpy as np

try:
    from tools.colors import colores
except:
    from colors import colores

def plot_ratios(data: pd.DataFrame, inner_radius:int, outer_radius:int, width:int=600, height:int=600, title:str ="") -> figure:
    """
    Se ingresa dataset tal cual sale de resample_dataset_s()
    Esta función tiene un umbral de 1.25 para filtrar los modelos que no tienen suficiente frecuencia
    """

    ## CREAMOS LA VARIABLE QUE VAMOS A VISUALIZAR:
    umbral = 1.24
    maxi = outer_radius - inner_radius

    data = data.T.sum(axis=1).to_frame()

    # CREACION DE COLUMNAS
    data.columns = ["count"]
    data= data.reset_index()
    ## TECNICAMENTE TODOS LOS MODELOS ESTAN NORMALIZADOS AL VALOR DE LA PREDICCION CON MÁS FRECUENCIA
    ## es decir, existe un solo máximo = outer_radio
    data["count_adjusted"] = (maxi * data["count"] / max(data["count"])) + inner_radius
    data.loc[:, "labels"] = data["index"].apply(lambda x: x.split("_")[-1].capitalize())
    data.loc[:, "colors"] = data["index"].map(colores)


    # APLICACION DE FILTRO
    data = data[data["count_adjusted"] > inner_radius *umbral]
    data= data.reset_index()



    ## CREAR VARIABLES RELACIONADAS A LOS COLORES

    big_angle = 2.0 * np.pi / (len(data))
    small_angle = big_angle / 7


    p = figure(width=width, height=height,
            title=title,# toolbar_location="above, below, left, right",
            x_axis_type=None, y_axis_type=None,
            x_range=(-420, 420), y_range=(-420, 420),
            min_border=0, outline_line_color="white",
            background_fill_color="lightgrey")




    ## VISUALIZACION

    angles = np.pi/2 - big_angle/2 - data.index.to_series()*big_angle
    xr = (inner_radius+outer_radius)/2 * np.cos(np.array(-big_angle/2 + angles))
    yr = (inner_radius+outer_radius)/2 * np.sin(np.array(-big_angle/2 + angles))



    p.annular_wedge(0, 0, inner_radius, outer_radius, -big_angle+angles, angles, color=data.colors, alpha=0.0015, line_width=5)
    p.annular_wedge(0, 0, inner_radius, data["count_adjusted"],
                    -big_angle+angles, angles, color=data.colors, alpha=1.0, line_width=2)
    p.text(x=xr, y=yr,
        text=data["labels"],
        text_font_size="8pt",
        text_align="center", text_baseline="middle")



    return p
