#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the growth of remand population in England & Wales.
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
TITLE = "Remand on the rise"
SUBTITLE = "The number of people in prison on remand is now at its highest level in at least 50 years"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: January to March 2025. And previous editions"
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='remand_population.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing change in number of people in prison on remand."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="People in prison",
        annotation_type="y-axis")

    fig.add_trace(
        go.Scatter(
            name="Remand population",
            x=df["date"].tolist(),
            y=df["remand_pop"].tolist(),
            mode="lines",
            hovertemplate="%{y} people<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(
        range=[0, 20100],
        automargin=True,
        tickformat=",.0f",
        fixedrange=True
        )

    # Configure layout
    fig.update_layout(
        hovermode="x",
        annotations=annotations,
        )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/remand_population.csv")
    df = utils.load_data(
        data_path,
        parse_dates=["date"],
        date_format="%d-%b-%y"
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
