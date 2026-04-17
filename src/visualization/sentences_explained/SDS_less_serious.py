#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the sentence breakdown SDS sentences for less serious offences.
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
SUBTITLE = "Standard determinate sentences for less serious offences"
SOURCE = ""
OUTPUT_PATH = utils.get_output_path(
    section='sentences_explained',
    filename='SDS_less_serious.html'
)

# Line and annotation constants
LINE_POSITIONS = [40]
ANNOTATION_CONFIGS = [
    {"text": "Start", "x": 0, "xanchor": "left"},
    {"text": "End", "x": 100, "xanchor": "right"},
    {"text": prt_theme.wrap_labels("Automatic release", max_chars=10), "x": LINE_POSITIONS[-1], "xanchor": "center"},
]


def generate_traces() -> list:
    """Generates Plotly traces"""
    colorway = ("#F9A237", "#A01D28", "#808080", "#499CC9", "#573D6B")

    traces = [
        go.Bar(
            x=[LINE_POSITIONS[-1]],
            y=[1],
            orientation="h",
            text=prt_theme.wrap_labels(f"{LINE_POSITIONS[-1]}% of custodial term", max_chars=15),
            textposition="inside",
            textfont_color="white",
            textfont_size=16,
            hovertemplate="Custodial period of sentence<extra></extra>",
            marker_color=colorway[1],
            width=7,
        ),
        go.Bar(
            x=[100 - LINE_POSITIONS[-1]],
            y=[1],
            orientation="h",
            hovertemplate="Part of custodial<br>period spent on<br>licence following<br>automatic release<extra></extra>",
            marker_color=colorway[3],
            width=7,
        ),
    ]

    return traces


def create_chart() -> go.Figure:
    """Creates a Plotly horizontal bar chart."""

    fig = go.Figure()
    traces = generate_traces()

    fig.add_traces(traces)

    fig.add_shape(
        type="line",
        x0=40, y0=0, x1=40, y1=1,
        xref="x", yref="paper",
        line=dict(
            color="white",
            width=2,
            dash="dot")
        )

    # Configure axes
    fig.update_xaxes(
        zeroline=False,
        ticks="",
        range=[0, 100],
        fixedrange=True
        )

    # Configure layout
    fig.update_layout(
        height=115,
        margin={'t': 0, 'b': 35, 'l': 0, 'r': 0, 'pad': 0, 'autoexpand': False},
        uniformtext_minsize=16,
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
