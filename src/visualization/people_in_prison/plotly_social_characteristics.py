#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Social characteristics of adult prisoners
Subtitle: 
Sources:
    - Harker, L. et al. (2013). How safe are our children? NSPCC.
    - HM Inspectorate of Prisons (2024). Annual report 2023-24. HM Stationery Office.
    - Light, M., et al. (2013). Gender differences in substance misuse and mental health amongst prisoners. Ministry of Justice.
    - Ministry of Justice (2012). Accommodation, homelessness and reoffending of prisoners.
    - Ministry of Justice (2010.) Compendium of reoffending statistics.
    - Ministry of Justice (2012). Estimating the prevalence of disability amongst prisoners.
    - Ministry of Justice (2012). Prisoners' childhood and family backgrounds.
    - Ministry of Justice (2012). The pre-custody employment, training and education status of newly sentenced prisoners.
    - Table KS611EW, Office for National Statistics (2012). 2011 Census.
    - Table 1, Office for National Statistics (2013). Families and households, 2012.
    - Office for National Statistics (2013). Labour market statistics, September 2013.
    - Office for National Statistics (2013). Population estimates for UK, England and Wales, Scotland and Northern Ireland — Mid 2012.
    - Welsh Government (2013). Absenteeism by pupil characteristics 2011/12.
    - Wiles, N. et al. (2006). Self-reported psychotic symptoms in the general population. The British Journal of Psychiatry, 188: 519-52
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Load configuration
config = utils.read_config()


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the data to ensure it is in the correct format for plotting."""

    df["characteristic"] = pd.Categorical(df["characteristic"], ordered=True)

    df = df.melt(id_vars='characteristic', var_name="group").dropna().reset_index(drop=True)
    # Wrap and convert characteristic to categorical to maintain order
    df["wrapped_characteristic"] = df["characteristic"].apply(prt_theme.wrap_labels, max_chars=28)

    # Convert 'group' to categorical to maintain order
    df["group"] = pd.Categorical(df["group"], ordered=True)

    df["group"] = df["group"].cat.rename_categories({
        "prison_male": "Men in prison",
        "prison_female": "Women in prison",
        "prison_all": "Prison population (overall)",
        "general_pop": "General population",
    })

    return df


def generate_traces(df):
    """Generate chart traces"""

    colorway = pio.templates[pio.templates.default].layout.colorway
    colors = {
        "Men in prison": colorway[1],
        "Women in prison": colorway[0],
        "Prison population (overall)": colorway[4],
        "General population": colorway[3],
    }

    traces = [
        go.Scatter(
            x=df_group["value"].tolist(),
            y=df_group['wrapped_characteristic'].tolist(),
            orientation="h",
            mode="markers",
            name=str(group),
            text=df_group["group"].tolist(),
            texttemplate="%{text}%",
            textposition="top center",
            hovertemplate="%{x}",
            marker_color=colors.get(group, colorway[i % len(colorway)]),  # Use colorway for fallback
        )
        for i, (group, df_group) in enumerate(df.groupby("group", sort=False, observed=True))
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
        range=[0, 100],
    )

    # Configure layout
    fig.update_layout(
        height=1000,
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
    return os.path.join(config["data"]["clnFilePath"], "people_in_prison", filename)


def test_data():
    """Test function to load and process data."""
    df = utils.load_data(get_data_path("social_characteristics.csv"))
    df = process_data(df)
    return df


def main() -> go.Figure:
    """Loads data, processes it, generates the chart, and uploads it to Chart Studio."""

    utils.setup_plotly_credentials()
    df = utils.load_data(get_data_path("social_characteristics.csv")).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="social_characteristics")

    return fig


if __name__ == "__main__":
    main()
