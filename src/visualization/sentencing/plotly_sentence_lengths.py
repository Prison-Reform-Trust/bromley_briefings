#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title:
Subtitle: For more serious, indictable offences, the average prison sentence is now 62.4 months—almost two years longer than in 2011
Source: Ministry of Justice (2024) Criminal justice statistics quarterly: Update to December 2023.
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
    """Filters data to retain every other year."""
    return df.iloc[::2].copy()

def generate_labels(df:pd.DataFrame) -> list:
    """Generates labels for all offences and indictable offences"""
    text_total = [""] * len(df)
    text_indictable = [""] * len(df)
    
    if len(df) > 1:
        for idx in [0, -4, -1]:
            if idx < len(df):
                text_total[idx] = f"{df['total'].iloc[idx]} months"
                text_indictable[idx] = f"{df['indictable'].iloc[idx]} months"
    
    return text_total, text_indictable

def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for all offences and indictable offences"""
    text_total, text_indictable = generate_labels(df)
    colorway = pio.templates[pio.templates.default].layout.colorway
    
    traces = [
        go.Bar(
            x=df["indictable"].tolist(),
            y=df["year"].tolist(),
            orientation="h",
            name="Indictable offences (more serious)",
            text=text_indictable,
            texttemplate="%{text}",
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x} months",
            marker_color=colorway[1],
        ),
        go.Bar(
            x=df["total"].tolist(),
            y=df["year"].tolist(),
            orientation="h",
            name="All offences",
            text=text_total,
            texttemplate="%{text}",
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x} months",
            marker_color=colorway[0],
        ),
    ]
    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of average sentence lengths by year."""

    fig = go.Figure()
    traces = generate_traces(df)
    annotations = prt_theme.add_annotation(None, "Average sentence length", annotation_type="y-axis")

    fig.add_traces(traces)
    
    # Configure axes
    fig.update_yaxes(autorange="reversed", tick0=2011, dtick=2)
    fig.update_xaxes(zeroline=False)
    
    # Configure layout
    fig.update_layout(
        barmode="overlay",
        hovermode="closest",
        margin_l=40,
        annotations=annotations,
        # dragmode="pan", Currently deactivated. May see whether I can use in future to view earlier time period when panned
        
    )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/sentence_lengths.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="sentence_lengths")
    return fig

if __name__ == "__main__":
    main()