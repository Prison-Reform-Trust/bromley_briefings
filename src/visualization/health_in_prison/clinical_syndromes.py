#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Estimated prevalence of clinical syndromes in the prison population
Subtitle:
Source: Tyler, N. et al. (2019) An updated picture of the mental health needs of male and female
prisoners in the UK: prevalence, comorbidity, and gender differences,
Social Psychiatry and Psychiatric Epidemiology, 54, 1143-1152.
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
config = utils.read_config()


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the data to ensure it is in the correct format for plotting."""

    df["gender"] = pd.Categorical(df["gender"], ordered=True)

    df["condition"] = df["condition"].replace({
        "mood": "Mood disorder",
        "eating": "Eating disorder",
        "psychotic": "Psychotic disorder",
        "ptsd": "PTSD",
        "alcohol": "Problematic alcohol use",
        "suicidal": "Risk of suicidal behaviours",
        "drug": "Drug dependence",
        "anxiety": "Anxiety",
    })

    # Wrap condition labels
    df["wrapped_condition"] = df["condition"].apply(prt_theme.wrap_labels, max_chars=17)

    return df


def generate_traces(df):
    """Generate chart traces"""
    traces = [
        go.Scatter(
            x=df_gender["percent"].tolist(),
            y=df_gender['wrapped_condition'].tolist(),
            orientation="h",
            mode="markers",
            opacity=0.6,
            name=str(gender).capitalize(),
            text=df_gender["gender"].tolist(),
            texttemplate="%{text}%",
            textposition="top center",
            hovertemplate="%{x}",
        )
        for gender, df_gender in df.groupby("gender", sort=False, observed=True)
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        type="category",
        automargin=True,
    )

    fig.update_xaxes(
        zeroline=False,
        showline=True,
        ticks="outside",
        automargin=True,
        ticksuffix='%',
        dtick=20,
        range=[0, 100],
    )

    # Configure layout
    fig.update_layout(
        scattermode="group",
        hovermode="y unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            traceorder="normal",
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="bottom",
            y=0.97,
            xanchor="right",
            x=1,
        ),
    )
    return fig


def get_data_path(filename: str) -> str:
    """Returns the full path for a given filename in the cleaned data directory."""
    return os.path.join(config["data"]["clnFilePath"], "health_in_prison", filename)


def test_data():
    """Test function to load and process data."""
    df = utils.load_data(get_data_path("clinical_syndromes.csv"))
    df = process_data(df)
    return df


def main() -> go.Figure:
    """Loads data, processes it, generates the chart, and uploads it to Chart Studio."""

    utils.setup_plotly_template()
    df = utils.load_data(get_data_path("clinical_syndromes.csv")).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="clinical_syndromes")

    return fig


if __name__ == "__main__":
    main()
