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

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Legend"
SUBTITLE = "Stages of a custodial sentence"
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='legend.html'
)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms data from wide to long format by transposing,
    setting the first row as column headers, and resetting the index."""
    return (
        df.T.reset_index()  # Convert index to a column (preserves sentence values)
        .pipe(lambda x: x.set_axis(x.iloc[0], axis=1))  # Set columns to the first row
        .iloc[1:]  # Drop the first row (now used as headers)
        .reset_index(drop=True)  # Reset the row index
    )


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces"""
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=[df['value'][i]],
            y=[1],
            orientation="h",
            text=prt_theme.wrap_labels(df['text'][i].capitalize(), max_chars=17),
            textposition="inside",
            insidetextanchor="middle",
            textfont_color="white",
            textfont_size=14,
            customdata=[prt_theme.wrap_labels(df['text'][i].capitalize(), max_chars=25)],  # Using %{text} in hovertemplate didn't render correctly, this is a workaround
            hovertemplate="%{customdata}<extra></extra>",
            marker_color=colorway[i],
            width=7,
        )
        for i, sentence in enumerate(df['sentence'])
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart."""

    fig = go.Figure()
    traces = generate_traces(df)

    fig.add_traces(traces)

    # Configure axes
    fig.update_xaxes(
        zeroline=False,
        ticks="",
        )

    # Configure layout
    fig.update_layout(
        height=100,
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        uniformtext_minsize=9,
        uniformtext_mode='show',
        barmode="stack",
        hovermode="closest",
        hoverlabel_font_color="white",
        yaxis_showticklabels=False,
        xaxis_showticklabels=False,
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
    df = load_data().pipe(prepare_data)
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
