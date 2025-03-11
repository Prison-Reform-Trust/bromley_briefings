"""
This script provides useful funcs to all other scripts
"""
import os
import yaml
import pandas as pd
import plotly.graph_objs as go  # Offline plotting
import chart_studio.plotly as py  # Online plotting
import chart_studio.tools
import plotly.io as pio
import textwrap
from dotenv import find_dotenv, load_dotenv

import src.visualization.prt_theme as prt_theme

def read_config():
    # Read in config file
    config = {k: v for d in yaml.load(
        open('config.yaml'),
            Loader=yaml.SafeLoader) for k, v in d.items()}
    return config

def setup_plotly_credentials():
    """Loads environment variables and sets Plotly credentials."""
    load_dotenv(find_dotenv())
    chart_studio.tools.set_credentials_file(
        username=os.getenv("PLOTLY_USERNAME"),
        api_key=os.getenv("PLOTLY_API_KEY"),
    )
    pio.templates.default = "prt_template"

## Read data
def load_data(filepath:str) -> pd.DataFrame:
    """Loads processed data from CSV."""
    return pd.read_csv(filepath)

## Generate annotations dynamically
def generate_annotations(traces, colorway, y_label, y_label_placement=None, y_offset_dict=None, x_pad=None):
    """
    Generates trace labels and y-label annotation, allowing individual y-value adjustments.
    
    Parameters:
        traces (list): Plotly trace objects.
        colorway (list): Color scheme from Plotly template.
        y_label (str): Y-axis label text.
        y_label_placement (str, optional): Y-axis label placement.
        y_offset_dict (dict, optional): A dictionary mapping trace names (years) to y-offsets.
        x_pad (float or int, optional): Horizontal padding for trace labels.
    """
    if y_offset_dict is None:
        y_offset_dict = {}

    annotations = [
        dict(
            xref="x",
            yref="y",
            x=trace.x[-1] + x_pad if x_pad else trace.x[-1],
            y=trace.y[-1] + y_offset_dict.get(trace.name, 0),  # Apply y-offset if available
            text=trace.name,
            xanchor="left",
            align="left",
            showarrow=False,
            font_color=colorway[i],
            font_size=10,
        )
        for i, trace in enumerate(traces)
    ]

    # Add y-axis label
    annotations.append(
        dict(
            xref="x",
            yref="paper",
            x=y_label_placement if y_label_placement else traces[0].x[0],
            y=1.04,
            align="left",
            xanchor="left",
            showarrow=False,
            text=y_label,
            font_size=14,
        )
    )

    return annotations

## Main function to create chart
def create_chart(
    df, 
    xaxis_tickvals, 
    xaxis_ticktext, 
    traces, 
    title: str, 
    y_label: str,
    xaxis_range:tuple,
    yaxis_dtick=None,
    xaxis_range_vals=(1, 53),
    xaxis_nticks=None,
    yaxis_nticks=6,
    y_offset_dict=None,
) -> go.Figure:
    """Creates the Plotly chart with adjustable parameters."""

    fig = go.Figure(traces)

    # Wrap title for better formatting
    chart_title = textwrap.wrap(title, width=65)

    # Get colorway from template
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Generate annotations with optional y_offset_dict
    annotations = generate_annotations(traces, colorway, y_label, y_offset_dict)

    fig.update_layout(
        title="<br>".join(chart_title),
        yaxis_dtick=yaxis_dtick if yaxis_dtick else 2000,
        xaxis_tickvals=xaxis_tickvals,
        xaxis_ticktext=xaxis_ticktext,
        hovermode='x',
        annotations=annotations,
    )

    # Apply axis settings
    fig.update_yaxes(range=xaxis_range, nticks=yaxis_nticks)
    fig.update_xaxes(range=xaxis_range_vals, nticks=xaxis_nticks)

    return fig

## Save chart (offline and online)
def save_chart(fig, filename):
    """Saves the chart as an image and uploads it online."""
    config = read_config() # Read in config file
    fig.write_image(os.path.join(config['viz']['outPath'], f'{filename}.svg'))

    fig.layout.images = [
        dict(
            source="https://i.ibb.co/jhfYbyc/PRTlogo-RGB.png",
            xref="paper",
            yref="paper",
            x=-0.08,
            y=1.25,
            sizex=0.15,
            sizey=0.15,
            xanchor="left",
            yanchor="top",
        )
    ]

    layout_atr = prt_theme.pio.templates["prt_template"].layout
    fig.update_layout(
        width=layout_atr.width,
        height=layout_atr.height,
    )

    py.plot(fig, filename=filename)