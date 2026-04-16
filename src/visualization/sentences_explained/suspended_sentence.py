#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the legend for the sentences explained section.
The chart is saved as an HTML file using a Jinja2 template for embedding
in a web page.
"""

import plotly.graph_objs as go

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = "Suspended sentence order"
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='suspended_sentence.html'
)


def generate_traces() -> list:
    """Generates Plotly traces"""
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=[100],
            y=[1],
            orientation="h",
            text=prt_theme.wrap_labels("Imprisonment can be triggered by breaches or further offending", max_chars=35),
            textposition="inside",
            insidetextanchor="middle",
            textfont_color="white",
            textfont_size=14,
            hovertemplate="Suspended sentence<extra></extra>",
            marker_color=colorway[0],
            width=7,
        )
    ]

    return traces


def create_chart() -> go.Figure:
    """Creates a Plotly horizontal bar chart."""

    fig = go.Figure()
    traces = generate_traces()

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


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    fig = create_chart()
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
