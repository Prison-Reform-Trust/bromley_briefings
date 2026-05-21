#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pandas as pd
import plotly.colors as pcols
import plotly.graph_objs as go

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Prison performance in England and Wales"
SUBTITLE = "Almost half of prisons are rated “of concern” or “serious concern”"
SOURCE = (
    "Ministry of Justice (2025). Annual prison performance ratings 2024 25. And previous editions<br>"
    "Note that ratings were suspended in 2020-21 and reduced in 2021-22"
)
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='prison_performance.html'
)


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

    visible = {
        "outstanding": "legendonly",
        "good": "legendonly",
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
            visible=visible.get(rating, True),  # Sets whether trace is visible by default
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


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/prison_performance.csv")
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
