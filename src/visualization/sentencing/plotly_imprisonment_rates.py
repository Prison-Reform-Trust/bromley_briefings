#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: We imprison far more of our population than our nearest neighbours
Subtitle: Scotland and England & Wales have the highest imprisonment rates in Western Europe.
Source: World Prison Brief, Institute for Crime & Justice Policy Research. 10 March 2025.
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

# Load environment variables and configuration
load_dotenv(find_dotenv())
config = utils.read_config()

# Set Plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), 
    api_key=os.getenv("PLOTLY_API_KEY")
)

# Set default Plotly template
pio.templates.default = "prt_template"


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a horizontal bar chart of imprisonment rates by country."""
    
    df["rate"] = df["rate"].tolist()  # Ensure proper serialization for Chart Studio

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison per 100,000 population", annotation_type="y-axis")

    fig.add_trace(
        go.Bar(
            x=df["rate"], 
            y=df["country"], 
            orientation="h",
            hovertemplate="%{text} per 100,000 population<extra></extra>",
            text=df["rate"],
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis=False,
        )
    )

    # Configure axes
    fig.update_yaxes(type="category", autorange="reversed", automargin=True, domain=[0, 0.95])

    # Configure layout
    fig.update_layout(
        xaxis_ticks="inside",
        margin=dict(t=20, b=25, l=0, r=25, pad=5),
        annotations=annotations,
        dragmode=False,
    )

    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    data_path = f"{config['data']['clnFilePath']}sentencing/imprisonment_rates.csv"
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="imprisonment_rates")
    return fig


if __name__ == "__main__":
    main()