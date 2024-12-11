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
df = pd.read_csv("data/processed/sentencing/sentence_lengths.csv")
#Filtering for every other year
df = df[::2]

## Plotting
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["total"],
        y=df["year"],
        orientation="h",
        # hovertemplate="%{text:,.0f} incidents<extra></extra>",
        text = df['total'],
        texttemplate="%{x} months",
        textposition="inside",
        zorder=1 #setting trace to be on top
    ),
)
fig.add_trace(
    go.Bar(
        x=df["indictable"],
        y=df["year"],
        orientation="h",
        # hovertemplate="%{text:,.0f} incidents<extra></extra>",
        text = df['indictable'],
        texttemplate="%{x} months",
        textposition="inside",
        zorder=0 #setting trace to be overlaid
    ),
)

fig.update_yaxes(autorange="reversed")

fig.update_layout(
    barmode='overlay',
    xaxis_ticks="inside",
    # xaxis_tickformat= ",.0f",
    margin_pad = 5,
    margin = dict(t=20, b=25, l=40, r=25),
    )

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "Average sentence length", annotation_type="y-axis")

# Adding annotations to layout
fig.update_layout(annotations=annotations)
fig.show()
# py.plot(fig, filename="sentence_lengths")