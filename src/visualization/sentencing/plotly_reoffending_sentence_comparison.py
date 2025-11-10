#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing libraries
import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Setting default Plotly template
pio.templates.default = "prt_template"

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Community sentences are more effective in reducing reoffending"
SUBTITLE = (
    r"A Ministry of Justice study matched people by personal and offence characteristics to compare the "
    r"effectiveness of different sentence types"
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

    # Loop over each unique sentence
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
        range=[0, 80], # Must specify lower range as well as upper to avoid trace labels from being cut off
    )

    fig.update_layout(
        margin_pad=5,
        margin=dict(t=20, b=25, l=0, r=0),
        hovermode=False,
        dragmode=False
        )

    ## Chart annotations
    annotations = []

    # Add y-axis label annotation with placement based on dataframe column
    prt_theme.add_annotation(annotations, "Reconviction rate (within one year)", annotation_type="y-axis")

    # Adding annotations to layout
    fig.update_layout(annotations=annotations)
    
    return fig

#Read in datasets
df = pd.read_csv("data/processed/sentencing/reoffending_sentence_comparison.csv")

# Wrapping y-axis labels using textwrap.fill with apply
df['wrapped_sentence'] = df['sentence'].apply(prt_theme.wrap_labels, max_chars=20)

# Get unique wrapped sentences for plotting
unique_sentences = df['wrapped_sentence'].unique()


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "sentencing/prison_population_inc_projections.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    return fig