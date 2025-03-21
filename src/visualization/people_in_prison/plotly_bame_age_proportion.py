#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Ethnicity in prisons in England and Wales
Subtitle: Ethnic minority representation is even greater amongst younger prisoners
Sources:
    - House of Lords written question HL3924, 24 November 2021.
    - Ministry of Justice (2021) Youth Custody report September 2021 
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
    """Melt dataframe from wide to long and enforce order"""
    
    # Melt the DataFrame to long format
    df = (
        df
        .melt(
            id_vars=['age'],
            var_name='ethnicity',
            value_name='proportion'
        )
        .sort_values(by=["ethnicity"], ascending=True)
        )

    # Convert 'ethnicity' to categorical to maintain order
    df["ethnicity"] = pd.Categorical(df["ethnicity"], ordered=True)

    return df

def generate_traces(df):
    """Generate bar chart traces"""
        
    colorway = pio.templates[pio.templates.default].layout.colorway
    colors = {
        "Other": colorway[4],
    }

    traces = [
        go.Bar(
            x=df_ethnicity["proportion"].tolist(),
            y=df_ethnicity['age'].tolist(),
            orientation="h",
            name=str(ethnicity),
            text=df_ethnicity["proportion"].tolist(),
            texttemplate="%{text}%",
            textposition="inside",
            textangle=0,
            hovertemplate="%{x}",
            marker_color=colors.get(ethnicity, colorway[i % len(colorway)]),  # Use colorway for fallback
        )
        for i, (ethnicity, df_ethnicity) in enumerate(df.groupby("ethnicity", sort=False, observed=True))
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    annotations = prt_theme.add_annotation(text="Proportion of prison population", annotation_type="y-axis")

    fig.add_traces(traces)
    
    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        type="category",
        automargin=True,
        )
    fig.update_xaxes(
        zeroline=False,
        ticksuffix='%',
        )
    
    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="closest",
        margin_r=0,
        annotations=annotations,
        showlegend=True,
        legend=dict(
            orientation="h",
            traceorder="normal",
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=0.95,
        ),
    )
    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_credentials()
    data_path = os.path.join(config['data']['clnFilePath'], "people_in_prison/bame_age_proportion.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="bame_age_proportion")
    return fig

if __name__ == "__main__":
    main()