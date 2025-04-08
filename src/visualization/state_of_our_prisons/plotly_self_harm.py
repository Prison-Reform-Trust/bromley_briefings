#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Self-harm in prisons in England and Wales
Subtitle: Rates of self-harm remain at historic highs
Source: Ministry of Justice (2024). Safety in custody: quarterly update to September 2024
"""

import os
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

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
            text = df['incidents'],
            texttemplate="%{x:,.0f}",
            textposition="outside",
        ),
    )
    
    fig.update_yaxes(
        type='category',
        autorange="reversed"
    )
    
    fig.update_xaxes(
        ticks="inside",
        tickformat= ",.0f",
    )

    prt_theme.set_axis_range(
        fig, 
        axis="x", 
        dataframe=df, 
        dataframe_column="rate", 
        min_value=0,
    )

    fig.update_layout(
        margin_l=45,
        margin_r=0,
        annotations=annotations
        )

    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/self_harm.csv")
    df = utils.load_data(data_path).pipe(process_data, 2013)
    fig = create_chart(df)
    py.plot(fig, filename="self_harm")
    return fig


if __name__ == "__main__":
    main()