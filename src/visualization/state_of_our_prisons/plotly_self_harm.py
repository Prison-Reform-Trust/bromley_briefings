#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing rates of self-harm in prisons in England and Wales.
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
TITLE = "Self-harm in prisons in England and Wales"
SUBTITLE = "Rates of self-harm continue to set new records"
SOURCE = "Ministry of Justice (2025). Safety in custody: quarterly update to December 2024"
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='self-harm.html'
)


def process_data(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Filters data by year to retain every other year."""
    filt = df['year'] >= year
    return df[filt].iloc[::2].copy()


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a horizontal bar chart showing rate and number of self-harm incidents in prison."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "Self-harm incidents per 1,000 prisoners", annotation_type="y-axis")

    fig.add_trace(
        go.Bar(
            x=df["rate"],
            y=df["year"],
            orientation="h",
            hovertemplate="%{text:,.0f} incidents<extra></extra>",
            text=df['incidents'],
            texttemplate="%{x:,.0f}",
            textposition="outside",
        ),
    )

    fig.update_yaxes(
        type='category',
        autorange="reversed",
        automargin=True,
    )

    fig.update_xaxes(
        ticks="inside",
        tickformat=",.0f",
        dtick=200,
        range=[0, 1000],
        fixedrange=True
    )

    fig.update_layout(
        margin_r=0,
        height=350,
        annotations=annotations,
        )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/self_harm.csv")
    df = utils.load_data(data_path).pipe(process_data, 2014)
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
