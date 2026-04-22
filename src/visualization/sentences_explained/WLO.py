#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the sentence breakdown for Whole Life Order sentences.
The chart is saved as an HTML file using a Jinja2 template for embedding
in a web page.
"""

import plotly.graph_objs as go

# Local modules
import src.utilities as utils
from src.visualization.sentences_explained import chart_functions as cf

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = ""
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='WLO.html'
)

# Line and annotation constants
LINE_POSITIONS = [100]
ANNOTATION_CONFIGS = [
    {"text": "Start", "x": 0, "xanchor": "left", "y": 1, "yanchor": "bottom"},
    {"text": "End of life", "x": 100, "xanchor": "right", "y": 1, "yanchor": "bottom"},
]


def generate_traces() -> list:
    """Generates Plotly traces"""
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=[LINE_POSITIONS[0]],
            y=[1],
            orientation="h",
            hovertemplate="Custodial period of sentence<extra></extra>",
            marker_color=colorway[1],
            width=7,
        ),
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
        range=[0, 100],
        fixedrange=True
        )

    # Configure layout
    fig.update_layout(
        height=95,
        margin={'t': 15, 'b': 0, 'l': 0, 'r': 0, 'pad': 0, 'autoexpand': False},
        uniformtext_minsize=12,
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
    annotations = cf.prepare_annotations(ANNOTATION_CONFIGS)
    fig = cf.apply_layout_updates(fig, annotations=annotations)
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
