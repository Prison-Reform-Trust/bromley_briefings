#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Growing inexperience
Subtitle: Staff with less than three years service is high and those with 10 or more years is declining
Source: Ministry of Justice (2024). HMPPS workforce quarterly: March 2024. And previous editions.
"""

import os

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

def generate_traces(df):
    """Generate bar chart traces dynamically based on dataframe columns."""
    # Define the desired order, ensuring only existing columns are included
    desired_order = ["short", "middle", "long"]
    colors = {
        "short": pio.templates[pio.templates.default].layout.colorway[0],
        "middle": "lightgrey",
        "long": pio.templates[pio.templates.default].layout.colorway[1],
    }

    name = {
        "short": "Less than three years",
        "middle": "Three years to less than 10 years",
        "long": "10 or more years",
    }

    # Filter only columns that exist in the DataFrame while maintaining order
    categories = [col for col in desired_order if col in df.columns]

    traces = [
        go.Bar(
            x=df["year"].tolist(),
            y=df[category].tolist(),
            name=name[category],
            text=df[category].tolist() if category != "middle" else "",
            texttemplate="%{text}%" if category != "middle" else None,  # Disable text labels for 'middle'
            textposition="auto",
            textangle=0,
            hovertemplate="%{y}%",
            marker_color=colors[category],
        )
        for category in categories
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )
    fig.update_xaxes(
        ticks="",
        dtick=2,
        )

    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="x unified",
        margin_r=0,
        margin_t=0,
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        hoverlabel_bgcolor="#F7F7F2",
    )
    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/workforce_experience.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="workforce_experience")
    return fig


if __name__ == "__main__":
    main()