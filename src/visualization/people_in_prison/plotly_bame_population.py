#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the percentage change in the prison population in England and Wales, by ethnicity.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Ethnicity in prisons in England and Wales"
SUBTITLE = "The number of Asian and mixed ethnicity prisoners has risen sharply since 2004"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: April to June 2025."
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='bame_population.html'
)


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for each ethnic group in dataset."""
    traces = [
        go.Scatter(
            x=df_ethnicity["year"].tolist(),
            y=df_ethnicity["percent"].tolist(),
            mode="lines+markers",
            text=df_ethnicity['ethnicity'],
            hovertemplate="<b>%{text}</b><br>Change since 2004: %{y:,.0f}%<extra></extra>",
            name=str(ethnicity),
        )
        for ethnicity, df_ethnicity in df.groupby(df["ethnicity"])
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change of custodial sentences by length."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    # Generate annotations with optional y_offset_dict
    colorway = pio.templates[pio.templates.default].layout.colorway
    y_label = "People in prison (percentage change since 2004)"

    annotations = utils.generate_annotations(
        traces=traces,
        colorway=colorway,
        max_chars=19,
        y_label=y_label,
        x_pad=0.3)

    # Axis parameter adjustments
    fig.update_yaxes(
        automargin=True,
        range=[-21, 144],
    )

    fig.update_xaxes(
        range=[2003.8, 2025.8],
        tick0=2004,
        dtick=2,
        )

    # Layout parameter adjustments
    fig.update_layout(
        yaxis_ticksuffix='%',
        hovermode='x unified',
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        annotations=annotations,
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/bame_population.csv")
    df = utils.load_data(data_path)
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
