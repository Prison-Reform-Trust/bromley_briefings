#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the relative reoffending rates of people leaving prison in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os
from functools import reduce

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration and colorway
CONFIG = utils.read_config()
COLORWAY = None
SMALLER_FONT_SIZE = 12

# Jinja2 template variables
TITLE = "Factors which can affect reconviction rates"
SUBTITLE = ""
SOURCE = (
    "Brunton-Smith, I. & Hopkins, K. (2013) The factors associated with \
    proven reoffending following release from prison: Findings from waves 1-3 of SPCR. \
    Ministry of Justice."
)
OUTPUT_PATH = utils.get_output_path(
    section='rehabilitation_and_resettlement',
    filename='reconviction_factors.html'
)


def generate_traces(df):
    """Generate chart traces"""
    colors = {
        "negative": COLORWAY[0],
        "positive": COLORWAY[3],
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
            title_position="bottom center",
            title_font_size=SMALLER_FONT_SIZE,
            # automargin=True,
        )
        traces.append(trace)

    return traces


def generate_pie_labels(fig, annotations_list=None, y_offset=0.015):
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
                    font_size=SMALLER_FONT_SIZE,
                    showarrow=False,
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
                text=prt_theme.wrap_labels(chart_titles[i], max_chars=35),
                x=(fig.data[col1].domain['x'][0] + fig.data[col2].domain['x'][1]) / 2,
                y=fig.data[col1].domain['y'][1],
                font_size=SMALLER_FONT_SIZE,
                showarrow=False,
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
    y_values = sorted({trace.domain['y'][1] for trace in fig.data}, reverse=True)
    return first_x, y_values


def generate_standout_labels(fig, annotations_list=None, y_offset=0.035):
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
                y=y_values[i] - y_offset,
                showarrow=False,
                font_size=40,
                font_color=COLORWAY[4],
                font_weight="bold",
                xanchor="center",
                yanchor="middle",
            )
        )

    return annotations


def generate_sub_standout_text(fig, annotations_list=None, y_offset=0.075):
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
                text=str(prt_theme.wrap_labels(text, max_chars=25)),
                x=first_x / 2,
                y=y_values[i] - y_offset,
                font_size=SMALLER_FONT_SIZE,
                showarrow=False,
                xanchor="center",
                yanchor="top",
            )
        )

    return annotations


def create_subplots() -> go.Figure:
    """Creates a figure with subplots for grouped pie charts."""
    specs = [
        [None, {"type": "domain"}, {"type": "domain"}]
        for _ in range(4)
    ]

    fig = make_subplots(
        rows=4, cols=3,
        row_heights=[0.25] * 4,
        vertical_spacing=0.13,
        column_widths=[0.5, 0.25, 0.25],
        specs=specs,
    )
    return fig


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a series of pie charts with reconviction outcomes."""
    traces = generate_traces(df)
    fig = create_subplots()

    # Determine rows and cols based on number of traces
    num_charts = len(traces)
    chart_pairs = [(r, c) for r in range(1, 5) for c in (2, 3)]
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
        title_font_size=SMALLER_FONT_SIZE,
        margin=dict(t=60, b=20, l=0, r=0),
        height=600,
    )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()

    # set COLORWAY after template is active
    global COLORWAY
    COLORWAY = pio.templates[pio.templates.default].layout.colorway

    data_path = os.path.join(
        CONFIG["data"]["clnFilePath"],
        "rehabilitation_and_resettlement",
        "reconviction_factors.csv",
    )
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
