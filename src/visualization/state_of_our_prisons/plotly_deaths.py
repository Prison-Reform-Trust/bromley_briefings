#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Remand on the rise
Subtitle: The number of people in prison on remand is now at its highest level in at least 50 years
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
    """Creates a sunburst chart showing number and proportion of deaths in prison by type and gender."""

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        ids=df["ids"],
        labels=df['death_type'],
        parents=df["parent"],
        values=df["value"],
        branchvalues="total",
        texttemplate="<b>%{label}</b><br>%{value}",
        hovertemplate="<b>%{label}</b><br>%{value} deaths<br>%{percentParent: .0%} of %{parent}<extra></extra>",
        marker_line_color="#F7F2F2",
        insidetextorientation="horizontal",
        ))

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        )
    
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/deaths.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="deaths")
    return fig


if __name__ == "__main__":
    main()