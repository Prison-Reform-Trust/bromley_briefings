#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing libraries
import os

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv

from src.visualization import prt_theme

##Loading environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

##Adding plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), api_key=os.getenv("PLOTLY_API_KEY")
)
#Setting default Plotly template
pio.templates.default = "prt_template"

#Read in datasets
df = pd.read_csv("data/processed/sentencing/reoffending_sentence_comparison.csv")

# Wrapping y-axis labels using textwrap.fill with apply
df['wrapped_sentence'] = df['sentence'].apply(prt_theme.wrap_labels, max_chars=20)

# Get unique wrapped sentences for plotting
unique_sentences = df['wrapped_sentence'].unique()

# Initialize a plotly figure
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
        name=str(sentence)
    ))

fig.update_yaxes(
    type='category',
    autorange="reversed",
    automargin=True,
    domain=[0,1],
    )

fig.update_xaxes(
    ticks="",
    showticklabels=False,
    zeroline=False,
    range=[None, 90]
)

fig.update_layout(
    margin_pad = 5,
    margin = dict(t=20, b=25, l=0, r=0),
    hovermode=False
    )

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "Reconviction rate", annotation_type="y-axis")

# Adding annotations to layout
fig.update_layout(annotations=annotations)

# fig.show()
py.plot(fig, filename="reoffending_sentence_comparison")