#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Children in prison in England and Wales
Subtitle: Child custody has fallen sharply — and so has offending
Sources:
    - Youth Justice Board (2024). Monthly youth custody report November 2024.
    - Youth Justice Board (2024). Youth Justice Statistics 2022-23. And previous editions.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Children in prison in England and Wales"
SUBTITLE = "Child custody has fallen sharply — and so has offending"
SOURCE = (
    "Youth Justice Board (2025). Monthly youth custody report September 2025.<br>"
    "Youth Justice Board (2025). Youth Justice Statistics 2023-24. And previous editions"
)
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='child_custody_offences.html'
)


def generate_traces(df: pd.DataFrame) -> go.Figure:
    """Generates Plotly subplot figure and traces for assaults and serious assault"""

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df["year"].tolist(),
            y=df["children"].tolist(),
            mode="lines+markers",
            name="Children in custody",
            hovertemplate="%{y} children<extra></extra>",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df["year"].tolist(),
            y=df["offences"].tolist(),
            mode="lines+markers",
            name="Proven offences",
            hovertemplate="%{y} proven offences<extra></extra>",
        ),
        secondary_y=True,
    )
    return fig


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly line chart of assault and serious assault rates in prison since 2012."""

    fig = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Configure axes
    fig.update_xaxes(dtick=2)

    fig.update_yaxes(
        title_text="Children in custody",
        range=[0, 4100],  # Explicitly set range
        dtick=500,  # Ensure ticks appear every 500
        title_font_color=colorway[0],
        tickfont_color=colorway[0],
        tickformat=",.0f",
        title_standoff=20,
        automargin=True,
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Proven offences",
        range=[0, 410000],  # Ensures proportional range
        dtick=50000,  # 100x the primary axis
        tickmode="linear",  # Ensures ticks appear at regular intervals
        tickformat=",.0f",
        title_standoff=20,
        title_font_color=colorway[1],
        tickfont_color=colorway[1],
        overlaying="y",
        automargin=True,
        secondary_y=True
    )

    # Configure layout
    fig.update_layout(
        hovermode="x unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        height=350
        )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/child_custody_offences.csv")
    df = utils.load_data(data_path)
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
