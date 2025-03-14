#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: We choose to send people to prison for a long time — and it’s growing
Subtitle: Almost three times as many people were sentenced to 10 years or more in 2023 than in 2010
Source: Ministry of Justice (2024) Criminal justice statistics quarterly: Update to December 2023.
"""

import os
import chart_studio
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

## Generate traces for Plotly
def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each sentence length in dataset."""
    traces = [
        go.Scatter(
            x=df_sentence["year"].tolist(),
            y=df_sentence["percent"].tolist(),
            mode="lines+markers",
            text=df_sentence['sentence'],
            hovertemplate="<b>%{text}</b><br>Change since 2010: %{y:,.0f}%<extra></extra>",
            name=str(sentence),
        )
        for sentence, df_sentence in df.groupby(df["sentence"])
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change of custodial sentences by length."""

    fig = go.Figure()
    traces = generate_traces(df)[::-1] # Reverse order for better visibility
    fig.add_traces(traces)
    
    # Generate annotations with optional y_offset_dict
    colorway = pio.templates[pio.templates.default].layout.colorway
    y_label = "People sentenced (percentage change since 2010)"
    y_offset_dict = {
        "Less than 6 months": -20,
        "6 months to less than 12 months": 8, 
        "12 months to less than 4 years": -20,
        "4 years to 10 years": 8
    }
    
    annotations = utils.generate_annotations(
        traces=traces, 
        colorway=colorway,
        max_chars=19,
        y_label=y_label, 
        y_offset_dict=y_offset_dict, 
        x_pad=0.3)

    # Set axes ranges
    fig.update_yaxes(range=[-110, 210])
    fig.update_xaxes(range=[2009.8, 2024.2])

    # Axis parameter adjustments
    fig.update_layout(
        margin=dict(l=50, r=80),
        yaxis_ticksuffix='%',
        hovermode='x unified',
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        annotations=annotations,
    )
    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = f"{config['data']['clnFilePath']}sentencing/sentence_growth.csv"
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="sentence_growth")
    return fig

if __name__ == "__main__":
    main()