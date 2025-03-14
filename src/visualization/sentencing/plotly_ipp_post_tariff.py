#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Over 1,000 people serving the IPP sentence remain in prison who have never been released.
Subtitle: On average, people serving the IPP sentence have spent 10 years in addition to their 
original period of punishment — with many serving even longer.
Source:
- Ministry of Justice (2023). Offender management statistics quarterly: April to June 2023.
- House of Lords written question HL423, 4 December 2023.
"""

import os
import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()


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


def main() -> go.Figure:
    """Load data, generate the chart, and upload it to Chart Studio."""
    
    utils.setup_plotly_credentials()
    data_path = os.path.join(config["data"]["clnFilePath"], "sentencing/ipp_post_tariff.csv")

    df = (
        utils.load_data(data_path, usecols=["Years over tariff", "short_year", "number"])
        .pipe(process_data)
    )

    fig = create_chart(df)
    py.plot(fig, filename="ipp_post_tariff")
    return fig


if __name__ == "__main__":
    main()