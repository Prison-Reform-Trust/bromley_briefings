#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the percentage change in the prison population in England and Wales, by age group.
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
TITLE = "Age in prisons in England and Wales"
SUBTITLE = "Over 50s account for almost one in five people in prison"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: January to March 2025."
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='age_groups.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df.replace({'age_group': {"60 and over": "60+"}}, inplace=True)
    df["age_group"] = pd.Categorical(df["age_group"], ordered=True)
    return df


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for each age group in dataset."""
    traces = [
        go.Scatter(
            x=df_age_group["year"],
            y=df_age_group["percent"],
            mode="lines+markers",
            text=df_age_group['age_group'],
            hovertemplate="<b>%{text}</b><br>Change since 2002: %{y:,.0f}%<extra></extra>",
            name=str(age_group),
        )
        for age_group, df_age_group in df.groupby(df["age_group"], observed=True)
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change of custodial sentences by length."""

    fig = go.Figure()
    traces = generate_traces(df)[::-1]  # Reverse order for better visibility
    fig.add_traces(traces)

    # Generate annotations with optional y_offset_dict
    colorway = pio.templates[pio.templates.default].layout.colorway
    y_label = "People in prison (percentage change since 2002)"

    annotations = utils.generate_annotations(
        traces=traces,
        colorway=colorway,
        max_chars=7,
        y_label=y_label,
        x_pad=0.3)

    # Axis parameter adjustments
    fig.update_yaxes(
        automargin=True,
        range=[-105, 410],
        dtick=100,
    )

    fig.update_xaxes(
        range=[2001.8, 2025.8],
        tick0=2002,
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
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/age_groups.csv")
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
