#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing proportion of self-harm incidents by women in prisons in England and Wales.
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

# Jinja2 template variables
TITLE = ""
SUBTITLE = "Women account for a disproportionate number of self-harm incidents"
SOURCE = "Ministry of Justice (2025). Safety in custody: quarterly update to December 2024"
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='self-harm-gender.html'
)


def process_data(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Filters data by year to retain every other year."""
    filt = df['year'] >= year
    return df[filt].iloc[::2].copy()


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for proportion of self-harm incidents by gender"""

    traces = [
        go.Bar(
            x=df["women_proportion"],
            y=df["year"],
            orientation="h",
            name="Women",
            text=df["women_proportion"],
            texttemplate="%{text}%",
            textposition="inside",
            customdata=df[['women_incidents']],
            hovertemplate=
                "<b>%{y}</b>: %{x}<br>" +
                "%{customdata[0]:,.0f} incidents",
        ),
        go.Bar(
            x=df["men_proportion"],
            y=df["year"],
            orientation="h",
            name="Men",
            text=df["men_proportion"],
            texttemplate="%{text}%",
            textposition="inside",
            customdata=df[['men_incidents']],
            hovertemplate=
                "<b>%{y}</b>: %{x}<br>" +
                "%{customdata[0]:,.0f} incidents",  # TODO #21 Add number of incidents to dataset and include in hovertemplate
        ),
    ]
    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway

    annotations = (
        prt_theme.add_annotation(text="Women", annotation_type="y-axis", font_color=colorway[0]) +
        prt_theme.add_annotation(text="Men", annotation_type="y-axis", xref="x", x=100, xanchor="right", font_color=colorway[1])
    )

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        automargin=True,
        dtick=2
        )
    fig.update_xaxes(
        zeroline=False,
        title_text="Proportion of all self-harm incidents",
        title_font_size=15,
        title_standoff=25,
        automargin=True,  # Allow necessary title spacing
        ticksuffix='%',
        )

    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="closest",
        margin_r=0,
        height=350,
        annotations=annotations,
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/self_harm_gender.csv")
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
