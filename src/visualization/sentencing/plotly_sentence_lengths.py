#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing average sentence lengths for all offences and indictable offences
in England & Wales. The chart is saved as an HTML file using a Jinja2 template for embedding
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
SUBTITLE = "For more serious, indictable offences, the average prison sentence is now 69.9 months—more than two and a half years longer than in 2010"
SOURCE = "Ministry of Justice (2025) Criminal justice statistics quarterly: Update to December 2024."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='sentence_lengths.html'
)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters data to retain every other year."""
    return df.iloc[::2].copy()


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
            hovertemplate="%{x} months",
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
            hovertemplate="%{x} months",
            marker_color=colorway[0],
        ),
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of average sentence lengths by year."""

    fig = go.Figure()
    traces = generate_traces(df)
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="Average sentence length",
        annotation_type="y-axis"
    )

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(zeroline=False)

    # Configure layout
    fig.update_layout(
        barmode="overlay",
        hovermode="y unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        margin_l=40,
        annotations=annotations,
        # dragmode="pan", Currently deactivated. May see whether I can use in future to view earlier time period when panned
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/sentence_lengths.csv")
    df = (
        utils.load_data(data_path)
        .pipe(prepare_data)
    )
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
