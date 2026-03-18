#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the total annual amount raised for the Victims Levy by the prison population in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()
COLORWAY = None

# Jinja2 template variables
TITLE = "Working for victims"
SUBTITLE = "People in prison have raised £25m through the Prisoners' Earnings Act levy—particularly in the last three years"
SOURCE = "HM Prison and Probation Service Annual Digest, April 2024 to March 2025."
OUTPUT_PATH = utils.get_output_path(
    section='rehabilitation_and_resettlement',
    filename='victims_levy.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the data to ensure it is in the correct format for plotting."""
    df['running_total'] = df['value'].cumsum()
    df['bottom'] = df['value'].cumsum().shift(fill_value=0)
    return df


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a bar chart showing the annual and cumulative total raised for the Victims Levy."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(text="Money raised", annotation_type="y-axis")

    fig.add_trace(
        go.Bar(
            name="Cumulative",
            x=df["year"],
            y=df["bottom"],
            marker_color="rgba(84, 86, 91, 0.3)",
            hovertemplate="Total from previous years: %{y}<extra></extra>",
        ),
    )
    fig.add_trace(
        go.Bar(
            name="Annual",
            x=df["year"],
            y=df["value"],
            texttemplate="%{y}",
            textangle=0,
            textposition="outside",
            marker_color=COLORWAY[0],
            hovertemplate="%{y} during %{x}<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(
        range=[0, 27],
        automargin=True,
        tickprefix="£",
        ticksuffix="m"
    )

    fig.update_xaxes(
        type="category",
        automargin=True,
        dtick=2
    )

    # Configure layout
    fig.update_layout(
        barmode='stack',
        hovermode="x",
        height=350,
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        annotations=annotations,
        )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    
    # set COLORWAY after template is active
    global COLORWAY
    COLORWAY = pio.templates[pio.templates.default].layout.colorway

    data_path = os.path.join(CONFIG['data']['clnFilePath'], "rehabilitation_and_resettlement/victims_levy.csv")
    df = utils.load_data(data_path).pipe(process_data)
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
