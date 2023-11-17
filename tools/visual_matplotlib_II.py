import random
import pandas as pd
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Theme:
    def __init__(self, background_color, text_color, grid_color, plot_color):
        self.background_color = background_color
        self.text_color = text_color
        self.grid_color = grid_color
        self.plot_color = plot_color


def create_theme(is_dark):
    if is_dark:
        return Theme('black', 'white', 'gray', '#1f77b4')
    else:
        return Theme('white', 'black', 'gray', '#1f77b4')

def create_dataframe():
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august']
    values = [random.random() *1e6 for _ in range(8)]
    pastel_colors = []
    for color in ['#FF0000', '#FF4500', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#8A2BE2']:
        rgb = mcolors.to_rgb(color)
        pastel_rgb = tuple((c + 1) / 2 for c in rgb)
        pastel_color = mcolors.to_hex(pastel_rgb)
        pastel_colors.append(pastel_color)
    return pd.DataFrame({
        "months":months,
        "values":values,
        "colors":pastel_colors
    })

def apply_theme(fig, ax, theme):
    fig.patch.set_facecolor(theme.background_color)
    ax.set_facecolor(theme.background_color)
    ax.spines['bottom'].set_color(theme.grid_color)
    ax.spines['left'].set_color(theme.grid_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', colors=theme.text_color)
    ax.tick_params(axis='y', colors=theme.text_color)
    ax.yaxis.label.set_color(theme.text_color)
    ax.xaxis.label.set_color(theme.text_color)
    ax.title.set_color(theme.text_color)

def create_average_line_plot(df, theme):
    "This one use different colors for each line"
    global fig, ax1
    fig, ax1 = plt.subplots(figsize=(18, 5))
    apply_theme(fig, ax1, theme)
    ax1.set_xlabel('Months', color=theme.text_color)
    ax1.set_ylabel('Values', color=theme.text_color)
    ax1.set_title('Line Plot with Vertical Lines', color=theme.text_color)
    
    # Line plot
    umbral_y = 0.2
    plt.plot(df, marker='o')
    min_value = df.min().min()
    max_value = ceil(df.max().max())
    step_size = int((max_value - min_value) * umbral_y) if max_value >= 10 else 1
    ax1.set_yticks(range(int(min_value), max_value+1, step_size))
    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax2 = ax1.twinx()
    ax2.set_ylabel('Values (Right)', color=theme.text_color)
    ax2.tick_params(axis='y', colors=theme.text_color)
    

    plt.legend(df.columns)
    
    return fig
    
    
if __name__ == "__main__":
    theme = create_theme(is_dark=False)


    fig = create_average_line_plot(
        df.drop(df.columns[0], axis=1)*1e6,
        theme
        )

    # random time serie module

    plt.show(fig)