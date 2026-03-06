#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly map showing all private prisons in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Private prisons in England and Wales"
SUBTITLE = ""
SOURCE = (
    "Beard, J. (2023). The prison estate in England and Wales. House of Commons.<br>"
    "HM Prison and Probation Service. (2025). Prisons and their resettlement providers."
)
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='private_prisons.html'
)


def generate_traces(df: pd.DataFrame) -> list:
    """Generate traces for the chart."""
    colors = {
        "Sodexo": "#283897",
        "G4S": "#ef3e42",
        "Serco": "#46555f",
        "Mitie": "#5b1f69",
    }

    traces = [
        go.Scattermap(
            lat=group['latitude'],
            lon=group['longitude'],
            mode='markers',
            marker=go.scattermap.Marker(
                size=9,
                color=colors[provider],
            ),
            text=group['prison_name'],
            hovertemplate="%{text}",
            name=str(provider),
        )
        for provider, group in df.groupby('provider')
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly map of all private prisons in England and Wales."""
    fig = go.Figure()  # TODO: #45 Fix rendering of the Maplibre attribution below maps
    traces = generate_traces(df)
    fig.add_traces(traces)

    fig.update_layout(
        # autosize=True,
        height=500,
        hovermode='closest',
        margin_l=0,
        margin_r=0,
        map_style="streets",
        showlegend=True,
        legend=dict(
            entrywidth=40,
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="top",
            y=0.95,
            xanchor="right",
            x=0.95,
        ),
        map=dict(
            bearing=0,
            center=dict(
                lat=53.0174642,
                lon=-2.5096761,
            ),
            pitch=10,
            zoom=5.3,
        ),
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/private_prisons.csv")
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
