#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing use of force rates amongst the prison population in England and Wales, by age group.
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
TITLE = "Use of force"
SUBTITLE = "The rate of force used against young adults in prison is much higher than for older adults"
SOURCE = "Bosworth et al. (2025). Use of force: an exploratory analysis of use of force in prisons 2018 2023. HM Prison & Probation Service."
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='young_adult_force.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing rate of self-harm by women in prison since 2012."""

    fig = go.Figure()
    annotations = (
        prt_theme
        .add_annotation(
            None,
            prt_theme.wrap_labels(
                "Incidents per 1,000 of the average male prison population to experience force",
                max_chars=40
            ),
            annotation_type="y-axis",
            align="left"
        )
    )

    fig.add_trace(
        go.Bar(
            name="Use of force rate",
            x=df["age_group"],
            y=df["rate"],
            text=df["rate"],
            texttemplate="%{text:,.0f}",
            textangle=0,
            hovertemplate="%{y} incidents per 1,000<extra></extra>",
        ),
    )
    # Configure axes
    fig.update_yaxes(
        range=[0, 1210],
        automargin=True,
        tickformat=",.0f"
    )

    fig.update_xaxes(
        type="category",
        automargin=True,
    )

    # Configure layout
    fig.update_layout(
        margin_t=40,
        hovermode="x",
        height=350,
        annotations=annotations,
        )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "people_in_prison/young_adult_force.csv")
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
