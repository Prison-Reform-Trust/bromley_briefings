#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: The growth of indeterminate sentences
Subtitle: The number of people in prison serving an indeterminate sentence has fallen in recent years — but growing numbers are being recalled back after their release
Source: Ministry of Justice (2024). Offender management statistics quarterly: April to June 2024.
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
    """Renaming and melting dataframe"""
    df = (
        df
        .rename(columns={'indet_unreleased': 'Unreleased', 'indet_recalled': 'Recalled'})
        .melt(id_vars='year', value_vars=['Unreleased', 'Recalled'], var_name='custody_type')
    )
    return df

## Generate traces for Plotly
def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each offence  in dataset."""
    
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
    traces = generate_traces(df)[::-1] # Reverse order for better visibility
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")
    
    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(tickformat= ",.0f", automargin=True)
    fig.update_xaxes(dtick=2, ticks="")

    fig.update_layout(
        barmode="stack",
        hovermode='x',
        annotations=annotations
    )

    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/indeterminate_population.csv")
    df = utils.load_data(data_path, usecols=['year', 'indet_unreleased', 'indet_recalled']).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="indeterminate_population")
    return fig


if __name__ == "__main__":
    main()