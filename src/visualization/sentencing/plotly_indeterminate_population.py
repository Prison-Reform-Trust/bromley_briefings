#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the growth of indeterminate sentences in England & Wales.
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
TITLE = "The growth of indeterminate sentences"
SUBTITLE = (
    r"The number of people in prison serving an indeterminate sentence has fallen in recent years — "
    r"but growing numbers are being recalled back after their release"
)
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: January to March 2025."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='indeterminate_population.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Renaming and melting dataframe"""
    df = (
        df
        .rename(columns={'indet_unreleased': 'Unreleased', 'indet_recalled': 'Recalled'})
        .melt(id_vars='year', value_vars=['Unreleased', 'Recalled'], var_name='custody_type')
    )
    return df


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for each offence in dataset."""

    traces = [
        go.Bar(
            x=df_type["year"].tolist(),
            y=df_type["value"].tolist(),
            name=str(type),
            hovertemplate="%{y:,.0f}"
            )
        for type, df_type in df.groupby(df["custody_type"])
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a bar chart showing change in average custodial sentence length by offence."""

    fig = go.Figure()
    traces = generate_traces(df)[::-1]  # Reverse order for better visibility
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="People in prison",
        annotation_type="y-axis"
        )

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(tickformat=",.0f", automargin=True)
    fig.update_xaxes(dtick=2, ticks="")

    fig.update_layout(
        barmode="stack",
        hovermode='x',
        annotations=annotations
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/indeterminate_population.csv")
    df = (
        utils.load_data(
            data_path,
            usecols=['year', 'indet_unreleased', 'indet_recalled']
        )
        .pipe(process_data)
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
