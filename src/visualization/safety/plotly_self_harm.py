#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing libraries
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import textwrap
from datetime import datetime

from src.visualization import prt_theme

#Setting default Plotly template
pio.templates.default = "prt_template"

#Read in datasets
df = pd.read_csv("data/processed/safety/self_harm.csv")
#Filtering for every other year
df = df[::2]

## Plotting
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["rate"],
        y=df["year"],
        orientation="h",
        hovertemplate="%{text:,.0f} incidents<extra></extra>",
        text = df['incidents'],
        texttemplate="%{x:,.0f}",
        textposition="outside",
    ),
)
fig.update_yaxes(
    type='category',
    autorange="reversed")

fig.update_layout(
    xaxis_ticks="inside",
    margin_pad = 5)

## Chart annotations
annotations = []

# Add title
prt_theme.add_title(fig, "Rates of self-harm remain at historic highs")

# Add source annotation with default placement
prt_theme.add_annotation(annotations, "Table 2.1, Ministry of Justice (2024). Safety in custody:\nQuarterly update to December 2023.", annotation_type="source")

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "Self-harm incidents per 1,000 prisoners", annotation_type="y-axis", y=1.05)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

fig.show()