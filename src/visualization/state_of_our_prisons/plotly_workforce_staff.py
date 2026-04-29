#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the percentage change in prison officer numbers and prison population in England and Wales.
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
TITLE = "Staff in prisons in England and Wales"
SUBTITLE = "Public sector prison officer numbers remain down on 2010"
SOURCE = (
    "Ministry of Justice (2025). HMPPS workforce quarterly: March 2025. And previous editions.<br>"
    "Ministry of Justice (2025). Offender management statistics quarterly: January to March 2025"
)
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='workforce_staff.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Multiplies percent values."""
    df['percent'] = df['percent'] * 100
    return df


def generate_traces(df: pd.DataFrame) -> list:
    """Generates Plotly traces for each group in dataset."""
    traces = [
        go.Scatter(
            x=df_group["year"].tolist(),
            y=df_group["percent"].tolist(),
            mode="lines+markers",
            text=df_group['type'],
            customdata=df_group['number'],
            hovertemplate="<b>Change since 2010:</b> %{y}<br><b>%{text}:</b> %{customdata:,.0f}<extra></extra>",
            name=str(group),
        )
        for group, df_group in df.groupby(df["type"])
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing percentage change in number of people in prison and band 3-5 officers since 2010."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    colorway = pio.templates[pio.templates.default].layout.colorway

    annotations = utils.generate_annotations(
        traces=traces,
        colorway=colorway,
        max_chars=10,
        y_label="Percentage change since 2010",
        x_pad=0.3
        )

    # Set axes ranges
    fig.update_yaxes(range=[-31, 11])
    fig.update_xaxes(range=[2009.5, 2026.5])

    # Axis parameter adjustments
    fig.update_layout(
        margin_l=40,
        margin_r=75,
        yaxis_ticksuffix='%',
        hovermode="x unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        annotations=annotations
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/workforce_staff.csv")
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
