#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Factors which can affect reconviction rates
Subtitle:
Source: Brunton-Smith, I. & Hopkins, K. (2013) The factors associated with 
proven reoffending following release from prison: Findings from waves 1-3 of SPCR. 
Ministry of Justice.
"""

import os
from functools import reduce

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration and colorway
config = utils.read_config()
colorway = pio.templates[pio.templates.default].layout.colorway


def generate_traces(df):
    """Generate chart traces"""
    colors = {
        "negative": colorway[0],
        "positive": colorway[3],
        "remainder": "rgba(84, 86, 91, 0.15)"
        }

    traces = []
    for _, row in df.iterrows():
        value = row["value"]
        remainder = 100 - value
        labels = [row["outcome"], "Other"]
        values = [value, remainder]

        trace = go.Pie(
            labels=labels,
            values=values,
            marker_colors=[colors.get(label.lower(), colors['remainder']) for label in labels],
            name=str(row["factor"]).capitalize(),
            direction='clockwise',
            sort=False,
            hole=0.7,
            textinfo="none",
            hoverinfo="none",
            title_text=str(row['chart_title']),
            title_font_size=10,
            title_position="bottom center",
            automargin=True,
        )
        traces.append(trace)

    return traces


def generate_pie_labels(fig, annotations_list=None, y_offset=0.01):
    """Generates pie chart value labels for the figure."""
    annotations = [] if annotations_list is None else annotations_list

    for trace in fig.data:
        if isinstance(trace, go.Pie):
            # Center of the pie chart
            x = sum(trace.domain['x']) / 2
            y = sum(trace.domain['y']) / 2 + y_offset

            # First slice value
            value = trace.values[0]

            annotations.append(
                dict(
                    text=f"{value}%",
                    x=x,
                    y=y,
                    showarrow=False,
                    font=dict(size=13),
                    xanchor="center",
                    yanchor="middle",
                )
            )
    return annotations


def generate_chart_titles(fig, annotations_list=None):
    """Adds text annotations to the figure."""
    annotations = [] if annotations_list is None else annotations_list

    chart_titles = [
        "People are less likely to be reconvicted if they receive family visits whilst in prison",
        "People are more likely to be reconvicted if they use class A drugs on release",
        "People are less likely to be reconvicted if they live with their immediate family on release",
        "People are less likely to be reconvicted if they secure a job after their release"
    ]
    # Determine trace numbers of each chart pair
    chart_pairs = [(i, i+1) for i in range(0, len(fig.data), 2)]

    # Loop through each pair of charts and add chart title in the middle
    # of the two pie charts
    for i, (col1, col2) in enumerate(chart_pairs):
        annotations.append(
            dict(
                text=prt_theme.wrap_labels(chart_titles[i], max_chars=50),
                x=(fig.data[col1].domain['x'][0] + fig.data[col2].domain['x'][1]) / 2,
                y=fig.data[col1].domain['y'][1],
                showarrow=False,
                font_size=10,
                xanchor="center",
                yanchor="bottom",
                borderpad=4,
            )
        )
    return annotations


def get_label_positions(fig):
    """Gets the x and y positions to use in the placement of the standout labels."""
    # Retrieve first x domain value of the first pie chart
    first_x = fig.data[0].domain['x'][0]

    # Calculate a set of y-values centred around the y domain of each row of pie charts
    # and sort them in descending order to ensure correct order of placement
    y_values = sorted({sum(trace.domain['y']) / 2 for trace in fig.data}, reverse=True)
    return first_x, y_values


def generate_standout_labels(fig, annotations_list=None):
    """Generates standout labels for the pie charts."""
    annotations = [] if annotations_list is None else annotations_list

    standout_labels = [
        "69%",
        "1 in 3",
        "57%",
        "28%",
    ]

    first_x, y_values = get_label_positions(fig)
    # Add standout labels to the annotations
    for i, label in enumerate(standout_labels):
        annotations.append(
            dict(
                text=str(label),
                x=first_x / 2,
                y=y_values[i],
                showarrow=False,
                font_size=30,
                font_color=colorway[4],
                font_weight="bold",
                xanchor="center",
                yanchor="middle",
            )
        )

    return annotations


def generate_sub_standout_text(fig, annotations_list=None, y_offset=0.025):
    """Generates text to go below standout labels."""
    annotations = [] if annotations_list is None else annotations_list

    text = [
        "of prisoners said they had received visits from family whilst in prison",
        "said they had used class A drugs since leaving custody",
        "said they were living with their immediate family on release",
        "of prisoners had been in employment the year after custody"
    ]

    first_x, y_values = get_label_positions(fig)
    for i, text in enumerate(text):
        annotations.append(
            dict(
                text=str(prt_theme.wrap_labels(text, max_chars=35)),
                x=first_x / 2,
                y=y_values[i] - y_offset,
                showarrow=False,
                font_size=10,
                xanchor="center",
                yanchor="top",
            )
        )

    return annotations


def create_subplots() -> go.Figure:
    """Creates a figure with subplots for grouped pie charts."""
    specs = [
        [None, None, {"type": "domain"}, {"type": "domain"}]
        for _ in range(4)
    ]

    fig = make_subplots(
        rows=4, cols=4,
        row_heights=[0.25] * 4,
        vertical_spacing=0.13,
        specs=specs,
    )
    return fig


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a series of pie charts with reconviction outcomes."""
    traces = generate_traces(df)
    fig = create_subplots()

    # Determine rows and cols based on number of traces
    num_charts = len(traces)
    chart_pairs = [(r, c) for r in range(1, 5) for c in (3, 4)]
    rows, cols = zip(*chart_pairs[:num_charts])

    fig.add_traces(traces, rows=rows, cols=cols)

    # List of all annotation functions to add to figure
    annotation_funcs = [
        generate_pie_labels,
        generate_chart_titles,
        generate_standout_labels,
        generate_sub_standout_text,
    ]
    # Using reduce to apply function cumulatively to generate all annotations
    annotations = reduce(lambda acc, func: func(fig, acc), annotation_funcs, [])

    fig.update_layout(
        showlegend=False,
        annotations=annotations,
        margin=dict(t=30, b=4, l=0, r=25),
    )

    return fig


def get_data_path(filename: str) -> str:
    """Returns the full path for a given filename in the cleaned data directory."""
    return os.path.join(config["data"]["clnFilePath"], "rehabilitation_and_resettlement", filename)


def test_data():
    """Test function to load and process data."""
    df = utils.load_data(get_data_path("reconviction_factors.csv"))
    # df = process_data(df)
    return df


def main() -> go.Figure:
    """Loads data, processes it, generates the chart, and uploads it to Chart Studio."""

    utils.setup_plotly_credentials()
    df = utils.load_data(get_data_path("reconviction_factors.csv"))
    fig = create_chart(df)
    py.plot(fig, filename="reconviction_factors")

    return fig


if __name__ == "__main__":
    main()
