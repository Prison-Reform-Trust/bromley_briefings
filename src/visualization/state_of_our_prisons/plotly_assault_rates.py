#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing assault and serious assault rates in prisons in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Assaults in prisons in England and Wales"
SUBTITLE = "Assaults and serious assaults declined during the pandemic—but are rising again"
SOURCE = "Ministry of Justice (2024). Safety in custody: quarterly update to December 2023."
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='assault_rates.html'
)


def generate_traces(df: pd.DataFrame) -> list[tuple[go.Scatter, bool]]:
    """Generates Plotly traces for assaults and serious assault with secondary_y info"""

    traces = [
        (go.Scatter(
            x=df["year"],
            y=df["serious"],
            mode="lines+markers",
            name="serious assault rate",
            hovertemplate="%{y} serious assaults per 1,000 prisoners<extra></extra>",
        ), True),  # secondary_y=True
        (go.Scatter(
            x=df["year"],
            y=df["assaults"],
            mode="lines+markers",
            name="assault rate",
            hovertemplate="%{y} assaults per 1,000 prisoners<extra></extra>",
        ), False),  # secondary_y=False
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly line chart of assault and serious assault rates in prison."""

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Add traces
    traces = generate_traces(df)
    for trace, secondary_y in traces:
        fig.add_trace(trace, secondary_y=secondary_y)

    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="Incidents per 1,000 prisoners",
        annotation_type="y-axis",
        y=1)

    prt_theme.add_annotation(
        annotations_list=annotations,
        text="The definition of recorded<br>assaults changed in 2019",
        annotation_type="label",
        xref="x", yref="y",
        x=2019.5, y=475)

    # Configure axes
    fig.update_yaxes(
        title_text="Serious assaults",
        range=[0, 51],
        title_font_color=colorway[0],
        tickfont_color=colorway[0],
        automargin=True,
        overlaying="y",
        tickmode="sync",
        secondary_y=True)

    fig.update_yaxes(
        title_text="Assaults",
        range=[0, 510],
        title_standoff=20,
        title_font_color=colorway[1],
        tickfont_color=colorway[1],
        automargin=True,
        secondary_y=False)

    # Configure layout
    fig.update_layout(
        annotations=annotations,
        height=350)

    # Adding dotted line for recording change
    fig.add_shape(
        type="line",
        x0=2019,
        y0=0,
        x1=2019,
        y1=500,
        line=dict(color=pio.templates[pio.templates.default].layout.xaxis.tickcolor, width=1, dash="dot"),
        layer="below",
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/assaults.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    return fig


def main() -> go.Figure:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE
    )
    return fig


if __name__ == "__main__":
    main()
