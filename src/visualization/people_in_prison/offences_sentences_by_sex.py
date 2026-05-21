#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the proportion of receptions by offence and sentence length, by sex.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Women tend to commit less serious offences — many serve prison sentences of less than 12 months"
SUBTITLE = "In 2024, women entered prison for committing these offences, to serve these sentences"
SOURCE = "Ministry of Justice (2025). Offender management statistics quarterly: October to December 2024"
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='offences_sentences_by_sex.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the data to ensure it is in the correct format for plotting."""

    if "offence" in df.columns:
        df["wrapped_offence"] = df["offence"].apply(prt_theme.wrap_labels, max_chars=18)

    if "sentence" in df.columns:
        df["sentence"] = df["sentence"].replace({
            "<6 months": "Less than 6 months",
            "6-12 months": "6 months to less than 12 months",
            "12 months-2 years": "12 months to less than 2 years",
            "2-4 years": "2 years to less than 4 years",
            "4 years+": "4 years and over",
            "indet": "Indeterminate"
        })

        df["sex"] = df["sex"].str.capitalize()
        df["wrapped_sentence"] = df["sentence"].apply(prt_theme.wrap_labels, max_chars=16)
        df = df[::-1]  # Reverse order for ascending sentence length in plot

    return df


def generate_traces(df: pd.DataFrame, show_legend: bool = True) -> list:
    """Generates Plotly traces for each offence in dataset."""

    colorway = pio.templates[pio.templates.default].layout.colorway
    colors = {"women": colorway[0], "men": colorway[1]}

    y_column = "wrapped_offence" if "offence" in df.columns else "wrapped_sentence"

    return [
        go.Bar(
            x=df_sex["percent"].tolist(),
            y=df_sex[y_column].tolist(),
            orientation="h",
            texttemplate="%{x}",
            textposition="auto",
            name=sex.capitalize(),
            marker=dict(color=colors[sex.lower()]),
            showlegend=show_legend,  # Show legend only for first subplot
        )
        for sex, df_sex in df.groupby("sex")
    ]


def create_chart(df_offences: pd.DataFrame, df_sentences: pd.DataFrame) -> go.Figure:
    """Creates a grouped bar chart for prison receptions by offence and sentence length."""

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.5, 0.5],
        vertical_spacing=0.05,
        shared_xaxes=True,
        specs=[[{"type": "bar"}], [{"type": "bar"}]],
        subplot_titles=("Offences", "Prison sentence lengths"),
    )

    offence_traces = generate_traces(df_offences, show_legend=True)
    sentence_traces = generate_traces(df_sentences, show_legend=False)

    fig.add_traces(offence_traces, rows=1, cols=1)
    fig.add_traces(sentence_traces, rows=2, cols=1)

    # Configure axes
    fig.update_xaxes(
        range=[0, 51],
        dtick=10,
        ticks="",
        showticklabels=False,
        automargin=True,
        ticksuffix="%",
        fixedrange=True
    )
    
    fig.update_yaxes(categoryorder="max ascending", automargin=True, fixedrange=True, row=1, col=1)
    fig.update_yaxes(automargin=True, fixedrange=True, row=2, col=1)

    # Configure layout
    fig.update_layout(
        barmode="group",
        hovermode="y unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        height=800,
        showlegend=True,
        legend=dict(
            orientation="v",
            traceorder="reversed",
            itemclick=False,
            itemdoubleclick=False,
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15,
        ),
    )

    return fig


def get_data_path(filename: str) -> str:
    """Returns the full path for a given filename in the cleaned data directory."""
    return os.path.join(CONFIG["data"]["clnFilePath"], "people_in_prison", filename)


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()

    df_offences = utils.load_data(get_data_path("offences_by_sex.csv")).pipe(process_data)
    df_sentences = utils.load_data(get_data_path("sentences_by_sex.csv")).pipe(process_data)

    fig = create_chart(df_offences, df_sentences)
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
