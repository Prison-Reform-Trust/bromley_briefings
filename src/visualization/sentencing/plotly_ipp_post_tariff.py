#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the number of people serving IPP sentences beyond their tariff in England & Wales.
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
TITLE = "Nearly 1,000 people serving the IPP sentence remain in prison who have never been released"
SUBTITLE = (
    r"On average, people serving the IPP sentence have spent 11 years in addition to their "
    r"original period of punishment — with many serving even longer"
)
SOURCE = (
    "Ministry of Justice (2024). Offender management statistics quarterly: April to June 2024.<br>"
    "House of Lords written question HL3985, 13 January 2025."
)
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='ipp_post_tariff.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process data by renaming columns, converting data types, and computing cumulative sum."""
    return (
        df.rename(
            columns={'Years over tariff': 'years', 'short_year': 'short_years', 'number': 'value'}
        )
        .astype({'value': 'Int64'})
        .assign(cumulative_sum=lambda x: x['value'].cumsum())  # Compute cumulative frequency
        .dropna()  # Drop NaN values after transformations
    )


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart showing additional years spent in prison post-tariff."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Calculate the median number of years post-tariff
    total = df["value"].sum()
    median_year_index = df.loc[df["cumulative_sum"] >= total / 2].index[0]  # Get the row index
    median_year = df.loc[median_year_index, "short_years"]  # Retrieve actual short_years value

    # Set marker colors to highlight the median year
    marker_color = [colorway[0]] * len(df)
    marker_color[median_year_index] = colorway[1]  # Highlight median bar

    fig.add_trace(
        go.Bar(
            x=df["short_years"].tolist(),
            y=df["value"].tolist(),
            customdata=df["years"].tolist(),
            hovertemplate="%{y} people<extra>%{customdata}</extra>",
            marker_color=marker_color,
        )
    )

    fig.update_yaxes(
        range=[0, 145],
        tickformat=",.0f",
        automargin=True,  # Avoid clipping y-axis labels
    )

    fig.update_xaxes(
        type="category",
        dtick=1,
        ticks="",
        title_text="Additional years spent in prison post-tariff",
        title_font_size=15,
        title_standoff=25,
        automargin=True,  # Allow necessary title spacing
    )

    fig.update_layout(
        hovermode="x",
        annotations=annotations,
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/ipp_post_tariff.csv")
    df = (
        utils.load_data(
            data_path,
            usecols=["Years over tariff", "short_year", "number"]
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
