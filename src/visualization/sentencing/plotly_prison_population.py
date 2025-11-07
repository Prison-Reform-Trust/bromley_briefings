#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the prison population in England & Wales and future projections.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from matplotlib import colors

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "How many people do we imprison in England & Wales?"
SUBTITLE = (
    r"There are around 86,000 people in prison. The prison population has risen by 93% in the last 30 years—"
    r"and it is predicted to rise further still."
)
SOURCE = (
    "Ministry of Justice (2023). Offender management statistics: Prison population 2023.<br>"
    "Ministry of Justice (2024). Prison population projections: 2024 to 2029."
)
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='prison_population_inc_projections.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Generates a line chart showing the prison population and projections.
    Args:
        df (pd.DataFrame): Dataframe containing the prison population data.
    Returns:
        go.Figure: Plotly figure object.
    """

    fig = go.Figure()
    colorway = pio.templates[pio.templates.default].layout.colorway
    projection_shading = f'rgba{colors.to_rgba(colorway[0], alpha=0.2)}'
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")

    traces = [
        go.Scatter(
            name="Prison population",
            x=df["date"], y=df["population"].tolist(),
            mode="lines", hovertemplate="%{y} prisoners<extra></extra>",
        ),
        go.Scatter(
            name="Lower projection",
            x=df["date"], y=df["l_projection"].tolist(),
            marker_color="#444", line_width=0,
            mode="lines", fillcolor=projection_shading,
            hovertemplate="%{y} prisoners",
        ),
        go.Scatter(
            name="Central projection",
            x=df["date"], y=df["c_projection"].tolist(),
            marker_color=colorway[0], mode="lines",
            line_dash="dot", fillcolor=projection_shading, fill="tonexty",
            hovertemplate="%{y} prisoners",
        ),
        go.Scatter(
            name="High projection",
            x=df["date"], y=df["h_projection"].tolist(),
            marker_color="#444", line_width=0, mode="lines",
            fillcolor=projection_shading, fill="tonexty",
            hovertemplate="%{y} prisoners", cliponaxis=False,
        ),
    ]

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(range=[0, 120500], dtick=20000, automargin=True)
    fig.update_xaxes(range=["1989-01-01", "2031-01-01"])

    # Configure layout
    fig.update_layout(
        yaxis_tickformat=",.0f",
        hovermode="x",
        annotations=annotations,
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/prison_population_inc_projections.csv")
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
