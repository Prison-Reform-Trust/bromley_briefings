#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing rates of self-harm in prisons in England and Wales.
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
TITLE = "Rates of self-harm are at a record high"
SUBTITLE = "Many women in prison have mental health needs and histories of abuse"
SOURCE = "Ministry of Justice (2025). Safety in custody: quarterly update to December 2024"
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='women_self_harm.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing rate of self-harm by women in prison since 2012."""

    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "Incidents per 1,000 women", annotation_type="y-axis")

    fig.add_trace(
        go.Scatter(
            name="Rate of self-harm",
            x=df["year"].tolist(),
            y=df["rate"].tolist(),
            mode="lines+markers",
            hovertemplate="%{y} incidents per 1,000 women<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(
        range=[0, 7024],
        automargin=True,
        tickformat=",.0f"
    )

    fig.update_xaxes(dtick=2)

    # Configure layout
    fig.update_layout(
        hovermode="x",
        height=350,
        annotations=annotations,
        )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/women_self_harm.csv")
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
