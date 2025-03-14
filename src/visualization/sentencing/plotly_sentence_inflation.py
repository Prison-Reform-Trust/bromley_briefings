#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: 
Subtitle: Almost all offences now receive a much longer prison sentence than they used to.
Source: Ministry of Justice (2024) Criminal justice statistics quarterly: Update to December 2023.
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

# Load configuration
config = utils.read_config()

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapping x-axis labels using textwrap.fill with apply"""
    df['wrapped_offence'] = df['offence'].apply(prt_theme.wrap_labels, max_chars=14)
    return df

## Generate traces for Plotly
def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each offence  in dataset."""
    
    traces = [
        go.Bar(
            x=df_year["wrapped_offence"].tolist(),
            y=df_year["length"].tolist(),
            text=df_year['length'],
            texttemplate='%{text}',
            name=str(year),
            customdata=df_year[['year','offence']], #Adding multiple columns to allow year and non-wrapped offences to be used in hovertemplate
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}: %{y} months<extra></extra>"
            )
            for year, df_year in df.groupby(df["year"])
    ]
    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a bar chart showing change in average custodial sentence length by offence."""

    fig = go.Figure()
    traces = generate_traces(df)
    annotations = prt_theme.add_annotation(None, "Average sentence length (months)", annotation_type="y-axis")
    
    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(range=[0, 121], dtick=20, automargin=True)
    fig.update_xaxes(tickfont_size=12)

    fig.update_layout(
        barmode="group",
        uniformtext_minsize=8,
        uniformtext_mode='show',
        margin=dict(b=60, l=35),
        annotations=annotations
    )

    return fig


def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "sentencing/sentence_inflation.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="sentence_inflation")
    return fig


if __name__ == "__main__":
    main()


"""
Possible development of arrows trace to show the percentage increase between the two years
arrow_trace = go.Scatter(
    x=trace_list[1].x,
    y=trace_list[1].y,
    mode="markers",
    hovertemplate="<extra></extra>",
    marker_symbol="arrow-up",
)

trace_list.append(arrow_trace)
"""