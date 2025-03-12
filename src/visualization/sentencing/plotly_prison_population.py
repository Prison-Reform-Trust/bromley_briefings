#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: How many people do we imprison in England & Wales?
Subtitle: There are around 86,000 people in prison. The prison population has risen by 93% in the last 30 years—and it is predicted to rise further still.
Source: 
- Ministry of Justice (2023). Offender management statistics: Prison population 2023.
- Ministry of Justice (2024). Prison population projections: 2024 to 2029.
"""

import os
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv
from matplotlib import colors

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly chart for prison population trends with projections."""
    
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
    fig.update_yaxes(range=[0, 120500], dtick=20000, automargin=True, domain=[0, 0.95])
    fig.update_xaxes(range=["1989-01-01", "2031-01-01"])

    # Configure layout
    fig.update_layout(
        yaxis_tickformat=",.0f",
        hovermode="x",
        annotations=annotations,
    )

    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/prison_population_inc_projections.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="prison_population_inc_projections")
    return fig


if __name__ == "__main__":
    main()