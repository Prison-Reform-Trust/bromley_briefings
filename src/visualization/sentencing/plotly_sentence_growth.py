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
from plotly.subplots import make_subplots

# Import prt_theme module
from src.visualization import prt_theme

# Loading environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Adding plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), api_key=os.getenv("PLOTLY_API_KEY")
)

# Setting default Plotly template and assigning attributes to prt_template
pio.templates.default = "prt_template"
prt_template = prt_theme.pio.templates['prt_template']

# Read in datasets
df = pd.read_csv("data/processed/sentencing/sentence_growth.csv")

## Plotting
fig = go.Figure()
trace_list= []

for i in df["sentence"].unique():
    df_type = df[df["sentence"] == i]

    trace = go.Scatter(
        x=df_type["year"],
        y=df_type["percent"],
        mode="lines+markers",
        text=df_type['sentence'],
        name=str(df_type['sentence'].iloc[0]),
        customdata=df_type['percent'],
        hovertemplate="<b>%{text}</b><br>Change since 2010: %{y:,.0f}%<extra></extra>"
        )
    
    trace_list.append(trace)

fig.add_traces(trace_list)

# Set y-axes range
fig.update_yaxes(range=[-110, 210])

# Axis parameter adjustments
fig.update_layout(
    xaxis_ticks="inside",
    margin_pad=5,
    margin = dict(t=20, b=25, l=50, r=25),
    yaxis_ticksuffix='%',
    hovermode='x unified',
    hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)'
)

## Chart annotations
annotations = []

# Add y-axis label annotation
prt_theme.add_annotation(annotations, "People sentenced (percentage change since 2010)", annotation_type="y-axis")

# Add trace label annotation
prt_theme.add_annotation(annotations, annotation_type="trace_label", trace_list=trace_list, trace_list_idx=[1, 3], y=[30, -5], x_pad=0.3)

# Adding annotations to layout
fig.update_layout(annotations=annotations)
# fig.show()
py.plot(fig, filename="sentence_growth")