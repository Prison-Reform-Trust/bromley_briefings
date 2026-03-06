#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing proportion of self-harm incidents by women in prisons in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = "Staff with less than three years service is high and those with 10 or more years is declining"
SOURCE = "Ministry of Justice (2025). HMPPS workforce quarterly: March 2025. And previous editions."
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='workforce_experience.html'
)


def generate_traces(df):
    """Generate bar chart traces dynamically based on dataframe columns."""
    # Define the desired order, ensuring only existing columns are included
    desired_order = ["short", "middle", "long"]
    colors = {
        "short": pio.templates[pio.templates.default].layout.colorway[0],
        "middle": "lightgrey",
        "long": pio.templates[pio.templates.default].layout.colorway[1],
    }

    name = {
        "short": "Less than three years",
        "middle": "Three years to less than 10 years",
        "long": "10 or more years",
    }

    # Filter only columns that exist in the DataFrame while maintaining order
    categories = [col for col in desired_order if col in df.columns]

    traces = [
        go.Bar(
            x=df["year"].tolist(),
            y=df[category].tolist(),
            name=name[category],
            text=df[category].tolist() if category != "middle" else "",
            texttemplate="%{text}%" if category != "middle" else None,  # Disable text labels for 'middle'
            textposition="auto",
            textangle=0,
            hovertemplate="%{y}%",
            marker_color=colors[category],
        )
        for category in categories
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)
    colorway = pio.templates[pio.templates.default].layout.colorway

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )
    fig.update_xaxes(
        ticks="",
        dtick=2,
        )

    # Configure layout
    fig.update_layout(
        barmode="stack",
        hovermode="x unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        margin_r=0,
        margin_t=0,
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="left",
            x=-0.007,
            traceorder="normal"
        ),
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/workforce_experience.csv")
    df = utils.load_data(data_path)
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
