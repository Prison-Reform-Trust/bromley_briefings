#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Children in prison in England and Wales
Subtitle: Child custody has fallen sharply — and so has offending
Sources: 
    - Youth Justice Board (2024). Monthly youth custody report November 2024.
    - Youth Justice Board (2024). Youuth Justice Statistics 2022-23. And previous editions.
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils

# Load configuration
config = utils.read_config()

def generate_traces(df:pd.DataFrame) -> go.Figure:
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
        hoverlabel_bgcolor="#F7F7F2",
        margin_t=0,
        )

    return fig
    

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "people_in_prison/child_custody_offences.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="child_custody_offences")
    return fig


if __name__ == "__main__":
    main()