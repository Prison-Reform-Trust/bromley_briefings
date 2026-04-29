#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing proportion of prisons that received 'good' or 'reasonably good' rating from HMIP.
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
TITLE = "Standards are inconsistent — but purposeful activity remains poor"
SUBTITLE = "Percentage of prisons that received a rating of 'good' or 'reasonably good' by HM Inspectorate of Prisons, by criteria"
SOURCE = (
    "HM Chief Inspector of Prisons. Annual report 2024–25 and previous editions.<br>"
    "Note 2020 is not included due to low number of prisons inspected during Covid-19"
    )
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='prison_standards.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Set trace order, adjust year labels and make type categorical."""
    # Define the desired order
    desired_order = [
        "Safety",
        "Respect",
        "Purposeful activity",
        "Preparation for release",
        ]

    # Extract first four digits of year e.g. 2015 and convert to datetime
    df["year"] = pd.to_datetime(df["year"].astype(str).str.extract(r"^(\d{4})")[0]).dt.year
    df["type"] = (
        df["type"]
        .astype(pd.CategoricalDtype(categories=desired_order, ordered=True))
    )
    return df


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for each group in dataset."""
    # Set opacity values and target index for default highlighted trace
    highlighted_opacity = 1.0
    default_opacity = 0.3
    default_target = "Purposeful activity"

    traces = [
        go.Scatter(
            x=df_group["year"].tolist(),
            y=df_group["percent"].tolist(),
            mode="lines",
            opacity=highlighted_opacity if group == default_target else default_opacity,
            text=df_group['type'],
            hovertemplate="%{y}",
            name=str(group),
        )
        for group, df_group in df.groupby(df["type"], sort=False, observed=True)
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing proportion of prisons that received a type of 'good' or 'reasonably good'
    from HMIP since 2010."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    annotations = prt_theme.add_annotation(None, "Prisons rated 'good' or 'reasonably good'", annotation_type="y-axis")

    # Set axes ranges
    fig.update_yaxes(range=[0, 102])
    fig.update_xaxes(range=[2007.8, 2024.5], dtick=2)

    # Layout parameter adjustments
    fig.update_layout(
        margin_l=45,
        margin_b=35,
        yaxis_ticksuffix="%",
        hovermode="x unified",
        hoverlabel_bgcolor="rgba(247, 242, 242, 0.8)",
        annotations=annotations,
        showlegend=True,
        height=400,
        legend=dict(
            orientation="h",
            font_size=11,
            yanchor="top",
            y=1,
            xanchor="right",
            x=1,
        ),
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/prison_standards.csv")
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


# TODO: #22 Highlight trace on click


if __name__ == "__main__":
    main()
