#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Private prisons in England and Wales
Subtitle:
Source: 
    - Beard, J. (2023). The prison estate in England and Wales. House of Commons.
    - HM Prison and Probation Service. (2025).  Prisons and their resettlement providers.
"""

import os
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

def generate_traces(df: pd.DataFrame) -> list:
    """Generate traces for the chart."""
    colors = {
        "Sodexo": "#283897",
        "G4S": "#ef3e42",
        "Serco": "#46555f",
        "Mitie": "#5b1f69",
    }

    traces = [
        go.Scattermap(
            lat = group['latitude'],
            lon = group['longitude'],
            mode = 'markers',
            marker=go.scattermap.Marker(
                size=9,
                color= colors[provider],
            ),
            text = group['prison_name'],
            hovertemplate="%{text}",
            name=str(provider),
        )
        for provider, group in df.groupby('provider')
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        margin_l=0,
        margin_r=0,
        map_style="streets",
        showlegend=True,
        legend=dict(
            entrywidth=40,
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="top",
            y=0.95,
            xanchor="right",
            x=0.95,
        ),
        map=dict(
            bearing=0,
            center=dict(
                lat=53.0174642,
                lon=-2.5096761,
            ),
            pitch=10,
            zoom=5.3,
        ),
    )
    
    return fig

def generate_html(fig: go.Figure) -> None:
    """Saves the HTML content to a file."""
    output_path = os.path.join(config['viz']['outPath'], "state_of_our_prisons/private_prisons.html")
    fig_html = fig.write_html(output_path, full_html=True, include_plotlyjs="cdn", config = {'displayModeBar': False})
    return fig_html

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/private_prisons.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    generate_html(fig)
    return fig


if __name__ == "__main__":
    main()