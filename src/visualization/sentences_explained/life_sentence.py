#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the sentence breakdown for life sentences.
The chart is saved as an HTML file using a Jinja2 template for embedding
in a web page.
"""

import plotly.graph_objs as go

# Local modules
import src.utilities as utils
from src.visualization import prt_theme
from src.visualization.sentences_explained import chart_functions as cf

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = "Based on a custodial tariff of 21 years (the average tariff imposed in 2021) and an assumption of living for 30 years after release"
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='life_sentence.html'
)

# Line and annotation constants
LINE_POSITIONS = [41.2]
ANNOTATION_CONFIGS = [
    {"text": "Start", "x": 0, "xanchor": "left", "y": 1, "yanchor": "bottom"},
    {"text": "End of life", "x": 100, "xanchor": "right", "y": 1, "yanchor": "bottom"},
    {"text": prt_theme.wrap_labels("Discretionary release", max_chars=13), "x": LINE_POSITIONS[0], "xanchor": "center"},
]


def generate_traces() -> list:
    """Generates Plotly traces"""
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=[LINE_POSITIONS[0]],
            y=[1],
            orientation="h",
            text=prt_theme.wrap_labels("Term set by judge", max_chars=9),
            textposition="inside",
            textfont_color="white",
            textfont_size=16,
            hovertemplate="Custodial period of sentence<extra></extra>",
            marker_color=colorway[1],
            width=7,
        ),
        go.Bar(
            x=[100 - LINE_POSITIONS[0]],
            y=[1],
            orientation="h",
            hovertemplate="Part of custodial<br>period spent on<br>licence following<br>discretionary release<extra></extra>",
            marker_color=colorway[2],
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
        height=130,  # Added extra height to accommodate annotations and added margin
        margin={'t': 15, 'b': 35, 'l': 0, 'r': 0, 'pad': 0, 'autoexpand': False},
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
    shapes = cf.prepare_line_shapes(LINE_POSITIONS)
    annotations = cf.prepare_annotations(ANNOTATION_CONFIGS)
    fig = cf.apply_layout_updates(fig, shapes=shapes, annotations=annotations)
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
