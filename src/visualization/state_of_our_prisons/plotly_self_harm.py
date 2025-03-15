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

prt_theme.set_axis_range(
    fig, 
    axis="x", 
    dataframe=df, 
    dataframe_column="rate", 
    min_value=0,
    )

fig.update_layout(
    xaxis_ticks="inside",
    xaxis_tickformat= ",.0f",
    margin_l=40,
    )

## Chart annotations
annotations = []

# Add title
# prt_theme.add_title(fig, "Rates of self-harm remain at historic highs")

# Add source annotation with default placement
# prt_theme.add_annotation(annotations, "Table 2.1, Ministry of Justice (2024). Safety in custody:<br>Quarterly update to December 2023.", annotation_type="source")

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "Self-harm incidents per 1,000 prisoners", annotation_type="y-axis")

# Adding annotations to layout
fig.update_layout(annotations=annotations)

py.plot(fig, filename="self_harm")