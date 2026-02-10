#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the growth in custodial sentences by length in England & Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "We choose to send people to prison for a long time — and it's growing"
SUBTITLE = "More than three times as many people were sentenced to 10 years or more in 2024 than in 2010"
SOURCE = "Ministry of Justice (2025) Criminal justice statistics quarterly: Update to December 2024."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='sentence_growth.html'
)


def generate_traces(df: pd.DataFrame) -> list:
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
    traces = generate_traces(df)[::-1]  # Reverse order for better visibility
    fig.add_traces(traces)

    # Generate annotations with optional y_offset_dict
    colorway = pio.templates[pio.templates.default].layout.colorway
    y_label = "People sentenced (percentage change since 2010)"
    y_offset_dict = {
        "Less than 6 months": -28,
        "6 months to less than 12 months": -20,
        "12 months to less than 4 years": 11,
        "4 years to 10 years": 10
    }

    annotations = utils.generate_annotations(
        traces=traces,
        colorway=colorway,
        max_chars=19,
        y_label=y_label,
        y_offset_dict=y_offset_dict,
        x_pad=0.3)

    # Set axes ranges
    fig.update_yaxes(range=[-110, 260])
    fig.update_xaxes(range=[2009.8, 2025.2])

    # Axis parameter adjustments
    fig.update_layout(
        margin=dict(l=50, r=80),
        yaxis_ticksuffix='%',
        hovermode='x unified',
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        annotations=annotations,
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/sentence_growth.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    return fig


def main() -> go.Figure:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE,
    )
    return fig


if __name__ == "__main__":
    main()
