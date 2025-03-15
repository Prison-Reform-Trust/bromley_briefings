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
df = pd.read_csv("data/processed/safety/deaths.csv", dtype={'parent': 'str'})

## Plotting

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=df["ids"],
    labels=df['death_type'],
    parents=df["parent"],
    values=df["value"],
    branchvalues="total",
    texttemplate="<b>%{label}</b><br>%{value}",
    hovertemplate="<b>%{label}</b><br>%{value} deaths<br>%{percentParent: .0%} of %{parent}<extra></extra>",
    marker_line_color="#F7F2F2",
    insidetextorientation="horizontal",
    ))

fig.update_layout(
    margin = dict(t=20, b=20),
    uniformtext_minsize=10, 
    uniformtext_mode='hide',
    )

## Chart annotations
annotations = []

# Add title
# prt_theme.add_title(fig, "Nearly 300 people died in prison in the year to March 2024", width=65)

# Add source annotation
# prt_theme.add_annotation(annotations, "Table 2, Ministry of Justice (2024). Safety in custody:<br>Quarterly update to December 2023.", annotation_type="source", y=-0.03)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

# fig.show()
py.plot(fig, filename="deaths")