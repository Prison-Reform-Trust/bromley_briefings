#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: We imprison far more of our population than our nearest neighbours
Subtitle: Scotland and England & Wales have the highest imprisonment rates in Western Europe.
Source: World Prison Brief, Institute for Crime & Justice Policy Research. 10 March 2025.
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
    """Creates a horizontal bar chart of imprisonment rates by country."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison per 100,000 population", annotation_type="y-axis")

    fig.add_trace(
        go.Bar(
            x=df["rate"].tolist(), 
            y=df["country"].tolist(), 
            orientation="h",
            hovertemplate="%{text} per 100,000 population<extra></extra>",
            text=df["rate"].tolist(),
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis=False,
        )
    )

    # Configure axes
    fig.update_yaxes(type="category", autorange="reversed", automargin=True)

    # Configure layout
    fig.update_layout(
        annotations=annotations,
    )

    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/imprisonment_rates.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="imprisonment_rates")
    return fig


if __name__ == "__main__":
    main()