#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the growth of life sentences in England & Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Life behind bars"
SUBTITLE = "The number of people in prison serving a life sentence has almost trebled in the last 30 years"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: January to March 2025."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='lifer_population.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing change in number of people in prison serving a life sentence."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="People in prison",
        annotation_type="y-axis"
    )

    fig.add_trace(
        go.Scatter(
            name="Lifer population",
            x=df["year"].tolist(),
            y=df["number"].tolist(),
            mode="lines",
            hovertemplate="%{y} people<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(
        range=[0, 10050],
        automargin=True,
        tickformat=",.0f",
        fixedrange=True
    )
    
    fig.update_xaxes(dtick=5)

    # Configure layout
    fig.update_layout(
        margin_b=35,
        hovermode="x",
        annotations=annotations,
        )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/lifer_population.csv")
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
        source=SOURCE
    )
    return fig


if __name__ == "__main__":
    main()
