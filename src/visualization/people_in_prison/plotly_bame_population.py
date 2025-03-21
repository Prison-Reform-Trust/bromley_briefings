#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Ethnicity in prisons in England and Wales
Subtitle: The number of Asian and mixed ethnicity prisoners has risen sharply since 2004
Source: Ministry of Justice (2024). Offender management statistics quarterly: April to June 2024
"""

import os
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils

# Load configuration
config = utils.read_config()

def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each ethnic group in dataset."""
    traces = [
        go.Scatter(
            x=df_ethnicity["year"].tolist(),
            y=df_ethnicity["percent"].tolist(),
            mode="lines+markers",
            text=df_ethnicity['ethnicity'],
            hovertemplate="<b>%{text}</b><br>Change since 2004: %{y:,.0f}%<extra></extra>",
            name=str(ethnicity),
        )
        for ethnicity, df_ethnicity in df.groupby(df["ethnicity"])
    ]
    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change of custodial sentences by length."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    # Generate annotations with optional y_offset_dict
    colorway = pio.templates[pio.templates.default].layout.colorway
    y_label = "People in prison (percentage change since 2004)"

    annotations = utils.generate_annotations(
        traces=traces, 
        colorway=colorway,
        max_chars=19,
        y_label=y_label, 
        x_pad=0.3)
    
    # Axis parameter adjustments
    fig.update_yaxes(
        automargin=True,
        range=[-21, 144],
    )

    fig.update_xaxes(
        range=[2003.8, 2025.2],
        tick0=2004,
        dtick=2,
        )
    
    # Layout parameter adjustments
    fig.update_layout(
        yaxis_ticksuffix='%',
        hovermode='x unified',
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        annotations=annotations,
    )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "people_in_prison/bame_population.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="bame_population")
    return fig

if __name__ == "__main__":
    main()