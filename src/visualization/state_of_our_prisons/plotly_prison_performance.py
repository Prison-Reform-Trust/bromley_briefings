#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Prison performance in England and Wales
Subtitle: Over a third of prisons are rated “of concern” or “serious concern by the prison service
Source: Source: Ministry of Justice. Annual prison performance ratings 2023-24 and previous editions.
        Note that ratings were suspended in 2020-21 and reduced in 2021-22
"""

import os
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import plotly.colors as pcols
from dotenv import find_dotenv, load_dotenv

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

import pandas as pd

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Melt dataframe from wide to long and enforce rating order"""
    
    # Define the desired order
    desired_order = [
        "serious_concern",
        "concern",
        "good",
        "outstanding", 
        ]
    
    # Melt the DataFrame to long format
    df = df.melt(
        id_vars=['year'],
        value_vars=desired_order,  # Ensure correct order when melting
        var_name='rating',
        value_name='number'
    )
    
    # Extract first four digits of year e.g. 2015
    df["year"] = df["year"].astype(str).str.extract(r"^(\d{4})")

    # Convert 'rating' to categorical to maintain order
    df["rating"] = pd.Categorical(df["rating"], categories=desired_order, ordered=True)

    return df

def generate_traces(df):
    """Generate bar chart traces"""

    colors = {
        "outstanding": pcols.qualitative.Prism[3],
        "good": pcols.qualitative.Prism[4],
        "concern": pcols.qualitative.Prism[5],
        "serious_concern": pcols.qualitative.Prism[7],
    }

    # Custom names for labels
    name_mapping = {
        "serious_concern": "Serious concern",
        "concern": "Of concern",
    }

    traces = [
        go.Bar(
            x=df_rating["year"].tolist(),
            y=df_rating['number'].tolist(),
            name=name_mapping.get(rating, rating.title()),  # Use mapping if available, otherwise use title case
            text=df_rating["number"].tolist(),
            texttemplate="%{text}%",
            textposition="inside",
            textangle=0,
            hovertemplate="%{y}%",
            marker_color=colors[rating],
        )
        for rating, df_rating in df.groupby("rating", sort=False, observed=True)
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly stacked bar chart of proportion of prisons by rating since 2015-16."""

    fig = go.Figure()
    traces = generate_traces(df)

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )
    fig.update_xaxes(
        ticks="",
        type="category",
        )

    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode=False,
        margin_r=0,
        margin_t=0,
        uniformtext_minsize=11, 
        uniformtext_mode='show',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=0.995
        ),
    )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/prison_performance.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="prison_performance")
    return fig


if __name__ == "__main__":
    main()