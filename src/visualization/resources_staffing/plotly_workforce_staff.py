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
df = pd.read_csv("data/processed/resources_staffing/workforce_staff.csv")
df['type'] = df['type'].replace({"HMPPS employed prison officers": "HMPPS employed<br>prison officers"})

## Plotting
fig = go.Figure()
trace_list = []

for i in df["type"].unique():
    df_type = df[df["type"] == i]

    trace = go.Scatter(
        x=df_type["year"],
        y=df_type["percent"],
        mode="lines+markers",
        text=df_type['type'],
        name=str(df_type['type'].iloc[0]),
        customdata=df_type['number'],
        hovertemplate="<b>Change since 2010:</b> %{y}<br><b>%{text}:</b> %{customdata:,.0f}<extra></extra>"
    )
    
    trace_list.append(trace)

fig.add_traces(trace_list)

# Set y-axes range
fig.update_yaxes(range=[-31, 11])

# Axis parameter adjustments
fig.update_layout(
    xaxis_ticks="inside",
    margin_pad=5,
    margin = dict(t=20, b=25, l=40, r=25),
    yaxis_ticksuffix='%'
)

## Chart annotations
annotations = []

# Add title
# prt_theme.add_title(fig, "Public sector prison officer numbers remain down on 2010")

# Add source annotation
# prt_theme.add_annotation(annotations, "Table 4, Ministry of Justice (2023). HMPPS workforce quarterly: March 2023.", annotation_type="source")

# Add y-axis label annotation
prt_theme.add_annotation(annotations, "Percentage change since 2010", annotation_type="y-axis")

# Add trace label annotation
prt_theme.add_annotation(annotations, annotation_type="trace_label", trace_list=trace_list)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

# fig.show()
py.plot(fig, filename="workforce_staff")