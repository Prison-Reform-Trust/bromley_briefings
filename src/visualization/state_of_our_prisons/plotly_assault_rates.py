#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Assaults in prisons in England and Wales
Subtitle: Assaults and serious assaults declined during the pandemic—but are rising again
Source: Ministry of Justice (2024). Safety in custody: quarterly update to December 2023.
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

def generate_traces(df:pd.DataFrame) -> go.Figure:
    """Generates Plotly subplot figure and traces for assaults and serious assault"""
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["serious"],
            mode="lines+markers",
            name="serious assault rate",
            hovertemplate="%{y} serious assaults per 1,000 prisoners<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["assaults"],
            mode="lines+markers",
            name="assault rate",
            hovertemplate="%{y} assaults per 1,000 prisoners<extra></extra>",
        ),
        secondary_y=False,
    )
    return fig

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly line chart of assault and serious assault rates in prison since 2012."""
    
    fig = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway
    
    annotations = prt_theme.add_annotation(None, "Incidents per 1,000 prisoners", annotation_type="y-axis", y=1)
    prt_theme.add_annotation(annotations, "The definition of recorded<br>assaults changed in 2019", annotation_type="label", xref="x", yref="y", x=2019.5, y=475)

    # Configure axes
    fig.update_yaxes(
        title_text="Serious assaults",
        range=[0,51],
        titlefont_color=colorway[0],
        tickfont_color=colorway[0],
        automargin=True,
        overlaying="y",
        tickmode="sync",
        secondary_y=True)

    fig.update_yaxes(
        title_text="Assaults", 
        range=[0,510],
        title_standoff=20,
        titlefont_color=colorway[1],
        tickfont_color=colorway[1],
        automargin=True,
        secondary_y=False)
    
    # fig.update_xaxes(autorangeoptions_maxallowed=2024) Autorange works locally but doesn't on Chart Studio

    # Configure layout
    fig.update_layout(
        annotations=annotations)

    ## Adding dotted line for recording change
    fig.add_shape(
        type="line",
        x0=2019,
        y0=0,
        x1=2019,
        y1=500,
        line=dict(color=pio.templates[pio.templates.default].layout.xaxis.tickcolor, width=1, dash="dot"),
        layer="below",
    )
    return fig
    

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/assaults.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="assault_rates")
    return fig


if __name__ == "__main__":
    main()