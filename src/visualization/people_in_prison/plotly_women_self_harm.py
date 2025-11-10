#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Rates of self-harm are at a record high.
Subtitle: Many women in prison have mental health needs and histories of abuse.
Source: Ministry of Justice (2024). Safety in custody: quarterly update to June 2024
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
    """Creates a line chart showing rate of self-harm by women in prison since 2012."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "Incidents per 1,000 women", annotation_type="y-axis")
    
    fig.add_trace(
        go.Scatter(
            name="Rate of self-harm",
            x=df["year"].tolist(),
            y=df["rate"].tolist(),
            mode="lines+markers",
            hovertemplate="%{y} incidents per 1,000 women<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(range=[0, 6020],automargin=True, tickformat= ",.0f")
    fig.update_xaxes(dtick=2)

    # Configure layout
    fig.update_layout(
        hovermode="x",
        annotations=annotations,
        )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "people_in_prison/women_self_harm.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="women_self_harm")
    return fig


if __name__ == "__main__":
    main()