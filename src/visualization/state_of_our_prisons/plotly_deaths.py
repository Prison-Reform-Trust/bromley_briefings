#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Deaths in prisons in England and Wales
Subtitle: Nearly 350 people died in prison during 2024
Source: Ministry of Justice (2024). Safety in custody: quarterly update to September 2024
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
        values=df["value"].tolist(),
        branchvalues="total",
        texttemplate="<b>%{label}</b><br>%{value}",
        hovertemplate="<b>%{label}</b><br>%{value} deaths<br>%{percentParent: .0%} of %{parent}<extra></extra>",
        marker_line_color="#F7F2F2",
        insidetextorientation="horizontal",
        ))

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        uniformtext=dict(minsize=12, mode="hide"),
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