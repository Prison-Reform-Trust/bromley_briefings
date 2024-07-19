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
df = pd.read_csv("data/processed/sentencing/imprisonment_rates.csv")

## Plotting
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["rate"],
        y=df["country"],
        orientation="h",
        hovertemplate="%{text:,.0f} per 100,000 population<extra></extra>",
        text = df['rate'],
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis = False,
    ),
)
fig.update_yaxes(
    type='category',
    autorange="reversed",
    automargin=True,
    domain=[0,0.95]
    )

fig.update_layout(
    xaxis_ticks="inside",
    margin_pad = 5,
    margin_t = 20
    )

## Chart annotations
annotations = []

# Add title
# prt_theme.add_title(fig, "Scotland and England & Wales have the highest imprisonment rates in western Europe")

# Add source annotation with default placement
prt_theme.add_annotation(annotations, "World Prison Brief, Institute for Crime & Justice Policy Research. 10 July 2024.", annotation_type="source")

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "People in prison per 100,000 population", annotation_type="y-axis", xref="x", y=1.05)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

# fig.show()
py.plot(fig, filename="imprisonment_rates")