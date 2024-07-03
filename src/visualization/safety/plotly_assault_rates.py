#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing libraries
import os

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
from dotenv import find_dotenv, load_dotenv

from src.visualization import prt_theme

##Loading environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

##Adding plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), api_key=os.getenv("PLOTLY_API_KEY")
)
#Setting default Plotly template and assigning attributes to prt_template
pio.templates.default = "prt_template"
prt_template = prt_theme.pio.templates['prt_template']

#Read in datasets
df = pd.read_csv("data/processed/safety/assaults.csv")

## Plotting
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["serious"],
        mode="lines+markers",
        name="serious assault rate",
        hovertemplate="%{y} serious assaults per 1,000 prisoners<extra></extra>",
    ),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["assaults"],
        mode="lines+markers",
        name="assault rate",
        hovertemplate="%{y} assaults per 1,000 prisoners<extra></extra>",
    ),
    secondary_y=False,
)

# Set y-axes titles
fig.update_yaxes(
    title_text="Serious assaults",
    range=[0,51],
    titlefont_color=prt_template.layout.colorway[0],
    tickfont_color=prt_template.layout.colorway[0],
    overlaying="y",
    tickmode="sync",
    secondary_y=True)

fig.update_yaxes(
    title_text="Assaults", 
    range=[0,510],
    titlefont_color=prt_template.layout.colorway[1],
    tickfont_color=prt_template.layout.colorway[1],
    secondary_y=False)

# Axis parameter adjustments
fig.update_layout(
    xaxis_ticks="inside",
    margin_pad = 5)

## Adding dotted line for recording change
fig.add_shape(
    type="line",
    x0=2019,
    y0=0,
    x1=2019,
    y1=500,
    line=dict(color=prt_template.layout.xaxis.tickcolor, width=1, dash="dot"),
    layer="below",
)
## Chart annotations
annotations = []

# Add title
prt_theme.add_title(fig, "Assaults and serious assaults declined during the pandemic—but are rising again")

# Add source annotation with default placement
prt_theme.add_annotation(annotations, "Table 3.1, Ministry of Justice (2024). Safety in custody:\nQuarterly update to December 2023.", annotation_type="source")

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "Incidents per 1,000 prisoners", annotation_type="y-axis", y=1.05)

# Add note
prt_theme.add_annotation(annotations, "The definition of recorded<br>assaults changed in 2019", xref="x", yref="y", x=2019.5, y=475)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

# fig.show()
py.plot(fig, filename="assault_rates")