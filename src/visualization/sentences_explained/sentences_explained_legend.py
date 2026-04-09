#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the legend for the sentences explained section.
The chart is saved as an HTML file using a Jinja2 template for embedding
in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = ""
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='legend.html'
)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms data from wide to long"""
    df = df.T.reset_index()
    df.columns = df.iloc[0, :]
    df.drop(index=df.index[0], axis=0, inplace=True)
    return df


def generate_labels(df: pd.DataFrame) -> tuple[list, list]:
    """Generates labels for all offences and indictable offences"""
    text_total = [""] * len(df)
    text_indictable = [""] * len(df)

    if len(df) > 1:
        for idx in [0, -4, -1]:
            if idx < len(df):
                text_total[idx] = f"{df['total'].iloc[idx]} months"
                text_indictable[idx] = f"{df['indictable'].iloc[idx]} months"

    return text_total, text_indictable


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces"""
    # text_total, text_indictable = generate_labels(df)
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=df['value'],
            y=df['sentence'],
            orientation="h",
            text=df['text'].title(),
            textposition="inside",
            marker_color=colorway[i],
        )
        for i, sentence in enumerate(df)  # This needs updating to account for new transposition of data
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of average sentence lengths by year."""

    fig = go.Figure()
    traces = generate_traces(df)
    # annotations = prt_theme.add_annotation(
    #     annotations_list=None,
    #     text="Average sentence length",
    #     annotation_type="y-axis"
    # )

    fig.add_traces(traces)

    # Configure axes
    fig.update_xaxes(
        zeroline=False,
        ticks="",
        )

    # Configure layout
    fig.update_layout(
        height=100,
        barmode="stack",
        hovermode="closest",
        yaxis_showticklabels=False,
        xaxis_showticklabels=False,
        # annotations=annotations,
    )
    return fig


def load_data() -> pd.DataFrame:
    """Function to load dataset"""
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentences_explained/legend.csv")
    df = utils.load_data(data_path)
    return df


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    df = load_data()
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
        source=SOURCE
    )
    return fig


if __name__ == "__main__":
    main()
