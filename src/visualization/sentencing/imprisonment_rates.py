#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing imprisonment rates by country.
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
TITLE = "We imprison far more of our population than our nearest neighbours"
SUBTITLE = "Scotland and England & Wales have the highest imprisonment rates in Western Europe"
SOURCE = "Institute for Crime & Justice Policy Research (2025). World Prison Brief."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='imprisonment_rates.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a horizontal bar chart of imprisonment rates by country."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="People in prison<br>(per 100,000 population)",
        annotation_type="y-axis",
        yanchor="top",
        y=1.1,
        align="left"
    )

    fig.add_trace(
        go.Bar(
            x=df["rate"].tolist(),
            y=df["country"].tolist(),
            orientation="h",
            hovertemplate="%{text} per 100,000 population<extra></extra>",
            text=df["rate"].tolist(),
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis=False,
        )
    )

    # Configure axes
    fig.update_yaxes(type="category", autorange="reversed", automargin=True)
    fig.update_xaxes(showticklabels=False, ticks="")

    # Configure layout
    fig.update_layout(
        margin=dict(b=0, t=35),
        annotations=annotations,
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/imprisonment_rates.csv")
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
