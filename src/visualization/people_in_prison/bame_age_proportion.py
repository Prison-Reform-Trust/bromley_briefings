#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the proportion of the prison population in England and Wales, by age group and ethnicity.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Ethnicity in prisons in England and Wales"
SUBTITLE = "Ethnic minority representation is even greater amongst younger prisoners"
SOURCE = "Ministry of Justice (2025). Chapter 6: Offender management tables. Ethnicity and the criminal justice system 2024."
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='bame_age_proportion.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Melt dataframe from wide to long and sort by proportion"""

    # Melt the DataFrame to long format
    df = (
        df
        .melt(
            id_vars=['age'],
            var_name='ethnicity',
            value_name='proportion'
        )
        .sort_values(by=["proportion"], ascending=False)
        )

    return df


def generate_traces(df):
    """Generate bar chart traces"""

    colorway = pio.templates[pio.templates.default].layout.colorway
    colors = {
        "Asian": colorway[0],
        "Black": colorway[1],
        "Mixed": colorway[2],
        "Other": colorway[4],
    }

    traces = [
        go.Bar(
            x=df_ethnicity["proportion"],
            y=df_ethnicity['age'],
            orientation="h",
            name=str(ethnicity),
            text=df_ethnicity["proportion"],
            texttemplate="%{text}%",
            textposition="inside",
            textangle=0,
            hovertemplate="%{x}",
            marker_color=colors.get(ethnicity, colorway[i % len(colorway)]),  # Use colorway for fallback
        )
        for i, (ethnicity, df_ethnicity) in enumerate(df.groupby("ethnicity", sort=False, observed=True))
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    annotations = prt_theme.add_annotation(text="Proportion of prison population", annotation_type="y-axis")

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        type="category",
        automargin=True,
        )
    fig.update_xaxes(
        zeroline=False,
        ticksuffix='%',
        automargin=True,
        fixedrange=True
        )

    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="closest",
        margin_r=0,
        annotations=annotations,
        uniformtext=dict(minsize=11, mode="hide"),
        xaxis_showgrid=True,
        showlegend=True,
        legend=dict(
            orientation="h",
            traceorder="normal",
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="bottom",
            y=1.1,
            xanchor="right",
            x=0.95,
        ),
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/bame_age_proportion.csv")
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
