#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Life behind bars
Subtitle: The number of people in prison serving a life sentence has almost trebled in the last 30 years
Source: Ministry of Justice (2024). Offender management statistics quarterly: January to March 2024. And previous editions
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

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing change in number of people in prison serving a life sentence."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")
    
    fig.add_trace(
        go.Scatter(
            name="Lifer population",
            x=df["year"].tolist(),
            y=df["number"].tolist(),
            mode="lines+markers",
            hovertemplate="%{y} people<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(range=[0, 10050],automargin=True, tickformat= ",.0f")
    fig.update_xaxes(dtick=5)

    # Configure layout
    fig.update_layout(
        hovermode="x",
        annotations=annotations,
        )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/lifer_population.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="lifer_population")
    return fig


if __name__ == "__main__":
    main()