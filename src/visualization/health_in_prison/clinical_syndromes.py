#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the estimated prevalence of clinical syndromes in the prison population in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Estimated prevalence of clinical syndromes in the prison population"
SUBTITLE = ""
SOURCE = (
    "Tyler, N. et al. (2019) An updated picture of the mental health needs of male and female\
    prisoners in the UK: prevalence, comorbidity, and gender differences,\
    Social Psychiatry and Psychiatric Epidemiology, 54, 1143-1152."
)
OUTPUT_PATH = utils.get_output_path(
    section='health_in_prison',
    filename='clinical_syndromes.html'
)


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
            x=df_gender["percent"],
            y=df_gender["wrapped_condition"],
            orientation="h",
            mode="markers",
            opacity=0.6,
            name=str(gender).capitalize(),
            text=df_gender["gender"],
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
        fixedrange=True
    )

    # Configure layout
    fig.update_layout(
        hovermode="y unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        showlegend=True,
        legend=dict(
            orientation="h",
            traceorder="reversed",
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="bottom",
            y=0.97,
            xanchor="right",
            x=1,
        ),
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG["data"]["clnFilePath"], "health_in_prison", "clinical_syndromes.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    return fig


def main() -> None:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE,
    )


if __name__ == "__main__":
    main()
