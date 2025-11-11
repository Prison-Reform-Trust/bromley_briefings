#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart comparing the reoffending rates of different sentence types in England & Wales.
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
TITLE = "Community sentences are more effective in reducing reoffending"
SUBTITLE = (
    r"A Ministry of Justice study matched people by personal and offence characteristics to "
    r"compare the effectiveness of different sentence types"
)
SOURCE = "Ministry of Justice (2013). 2013 Compendium of re-offending statistics and analysis."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='plotly_reoffending_sentence_comparison.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Generates a line chart showing the prison population and projections.
    Args:
        df (pd.DataFrame): Dataframe containing the prison population data.
    Returns:
        go.Figure: Plotly figure object.
    """
    fig = go.Figure()
    annotations = prt_theme.add_annotation(
        annotations_list=None,
        text="Reconviction rate (within one year)",
        annotation_type="y-axis"
    )

    # Loop over each unique sentence
    unique_sentences = df['wrapped_sentence'].unique()
    for sentence in unique_sentences:
        # Filter dataframe for the current sentence
        sentence_data = df[df['wrapped_sentence'] == sentence]

        # Get the percentage value(s) for this sentence
        # Assuming we want the first occurrence's percentage, use `.iloc[0]`
        percent = sentence_data['percent'].iloc[0]

        # Add a trace for this sentence
        fig.add_trace(go.Bar(
            x=[percent],  # Use percentage on the x-axis
            y=[sentence],  # Sentence on the y-axis (wrapped using 'label' above)
            orientation='h',
            hovertemplate="%{y}: %{text}%<extra></extra>",
            text=[percent],
            texttemplate="%{x}%",
            textposition="outside",
            cliponaxis=False,
            name=str(sentence)
        ))

    fig.update_yaxes(
        type='category',
        autorange="reversed",
        automargin=True,
        )

    fig.update_xaxes(
        ticks="",
        showticklabels=False,
        zeroline=False,
        range=[0, 100],  # Must specify lower range as well as upper to avoid trace labels from being cut off
    )

    fig.update_layout(
        margin_pad=5,
        margin=dict(t=20, b=25, l=0, r=0),
        hovermode=False,
        dragmode=False,
        annotations=annotations
        )

    return fig


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepares data for the chart by wrapping sentence labels."""
    df['wrapped_sentence'] = df['sentence'].apply(prt_theme.wrap_labels, max_chars=20)
    return df


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/reoffending_sentence_comparison.csv")
    df = (
        utils.load_data(data_path)
        .pipe(prepare_data)
    )
    fig = create_chart(df)
    return fig


def main() -> go.Figure:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    utils.setup_plotly_template()
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE
    )
    return fig


if __name__ == "__main__":
    main()
