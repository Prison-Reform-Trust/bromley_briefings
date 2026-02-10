#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title:
Subtitle: Women account for a disproportionate number of self-harm incidents
Source: Ministry of Justice (2024). Safety in custody: quarterly update to September 2024
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

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Replace values for men to actual proportion"""
    df["men"] = 100 - df["women"]
    return df

def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for proportion of self-harm incidents by gender"""
    
    traces = [
        go.Bar(
            x=df["women"].tolist(),
            y=df["year"].tolist(),
            orientation="h",
            name="Women",
            text=df["women"].tolist(),
            texttemplate="%{text}%",
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x}",
        ),
        go.Bar(
            x=df["men"].tolist(),
            y=df["year"].tolist(),
            orientation="h",
            name="Men",
            text=df["men"].tolist(),
            texttemplate="%{text}%",
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x}", #TODO #21 Add number of incidents to dataset and include in hovertemplate
        ),
    ]
    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway

    annotations = (
    prt_theme.add_annotation(text="Women", annotation_type="y-axis", font_color=colorway[0]) +
    prt_theme.add_annotation(text="Men", annotation_type="y-axis", xref="x", x=100, xanchor="right", font_color=colorway[1])
    )

    fig.add_traces(traces)
    
    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        tick0=2013,
        automargin=True,
        dtick=2
        )
    fig.update_xaxes(
        zeroline=False,
        title_text="Proportion of all self-harm incidents",
        title_font_size=15,
        title_standoff=25,
        automargin=True,  # Allow necessary title spacing
        ticksuffix='%',
        )
    
    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="closest",
        margin_r=0,
        annotations=annotations,
    )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/self_harm_gender.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="self_harm_gender")
    return fig


if __name__ == "__main__":
    main()