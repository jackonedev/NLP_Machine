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

def create_plot(df, theme):
    fig, ax1 = plt.subplots()
    apply_theme(fig, ax1, theme)
    ax1.bar(df['months'], df['values'], color=df['colors'])
    ax1.set_xlabel('Months', color=theme.text_color)
    ax1.set_ylabel('Values', color=theme.text_color)
    ax1.set_title('Bar Plot with Point Connections', color=theme.text_color)
    for i in range(len(df)-1):
        plt.plot([df['months'][i], df['months'][i+1]], [df['values'][i], df['values'][i+1]], color=theme.text_color, marker='o')
    max_value = ceil(max(df['values']))
    ax1.set_yticks(range(0, max_value+1, int(max_value*0.1)))
    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax2 = ax1.twinx()
    ax2.set_ylabel('Values (Right)', color=theme.text_color)
    ax2.tick_params(axis='y', colors=theme.text_color)
    return fig
    
if __name__ == "__main__":
    # Usage
    df = create_dataframe()
    theme = create_theme(is_dark=False)
    fig = create_plot(df, theme)

    plt.show(fig)
