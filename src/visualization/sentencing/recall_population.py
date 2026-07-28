#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the number of people in prison on recall in England & Wales
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from matplotlib import colors

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "The rise, and rise, and rise of the recall population"
SUBTITLE = r"Almost one in five of the sentenced prison population is now held in custody on recall"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: July to September 2024. And previous editions."

OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='recall_population.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Generates a line chart showing the prison population and projections.
    Args:
        df (pd.DataFrame): Dataframe containing the prison recall data.
    Returns:
        go.Figure: Plotly figure object.
    """

    fig = go.Figure()
    colorway = pio.templates[pio.templates.default].layout.colorway
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")

    fig.add_trace(
        go.Scatter(
            name="Recall population",
            x=df["date"],
            y=df["recall_pop"],
            mode="lines",
            hovertemplate="%{y} people<extra></extra>",
        ),
    )

    # Configure axes
    fig.update_yaxes(
        range=[0, 16050],
        automargin=True,
        fixedrange=True,
    )

    fig.update_xaxes(
        autorange="max",
        autorangeoptions_clipmax="2025-01-31",
        dtick="M24"
        )

    # Configure layout
    fig.update_layout(
        yaxis_tickformat=",.0f",
        hovermode="x",
        annotations=annotations,
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/recall_population.csv")
    df = utils.load_data(data_path, parse_dates=["date"], date_format="%b-%y")
    fig = create_chart(df)
    return fig


def main() -> None:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE,
    )


if __name__ == "__main__":
    main()


# df = pd.read_csv("data/processed/sentencing/recall_population.csv", parse_dates=["date"], date_format="%b-%Y", thousands=",")
