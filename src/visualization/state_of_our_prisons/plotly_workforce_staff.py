#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Staff in prisons in England and Wales
Subtitle: Public sector prison officer numbers remain down on 2010
Source: Ministry of Justice (2023). HMPPS workforce quarterly: March 2023.
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters data by year to retain every other year."""
    df['type'] = df['type'].replace({"HMPPS employed prison officers": "HMPPS employed<br>prison officers"})
    df['percent'] = df['percent'] * 100
    return df

def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each group in dataset."""
    traces = [
        go.Scatter(
            x=df_group["year"].tolist(),
            y=df_group["percent"].tolist(),
            mode="lines+markers",
            text=df_group['type'],
            customdata=df_group['number'],
            hovertemplate="<b>Change since 2010:</b> %{y}<br><b>%{text}:</b> %{customdata:,.0f}<extra></extra>",
            name=str(group),
        )
        for group, df_group in df.groupby(df["type"])
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change in number of people in prison and band 3-5 officers since 2010."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    colorway = pio.templates[pio.templates.default].layout.colorway

    annotations = utils.generate_annotations(
        traces=traces,
        colorway=colorway,
        y_label="Percentage change since 2010",
        x_pad=0.3
        )

    # Set axes ranges
    fig.update_yaxes(range=[-31, 11])
    fig.update_xaxes(range=[2009.8, 2025.2])
    

    # Axis parameter adjustments
    fig.update_layout(
        margin_l=40,
        margin_r=75,
        yaxis_ticksuffix='%',
        annotations=annotations
    )

    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/workforce_staff.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="workforce_staff")
    return fig


if __name__ == "__main__":
    main()