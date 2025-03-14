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
#Setting default Plotly template
pio.templates.default = "prt_template"

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Setting default Plotly template
pio.templates.default = "prt_template"

# Data
colors = ["rgb(160, 29, 40)", "rgba(84, 86, 91, 0.15)"]

# Plotting
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=[" ", " ", " "],
    shared_xaxes=True,
    shared_yaxes=False,
    vertical_spacing=0.001
)

# Create subplots: use 'domain' type for Pie subplot
fig.add_trace(go.Pie(
    labels=["Non-violent offence", "Violent offence"],
    values=[55, 45],
    name="Offences",
    marker_colors=colors,
    direction ='clockwise', # Setting direction and sort attributes to match for each chart
    sort=False,
    title_text=prt_theme.wrap_labels("<br>The majority have committed a non-violent crime", 32), # Wrapping the title
    title_position="bottom center",
    title_font_weight='bold',
    title_font_size=17,
), 1, 1)

fig.add_trace(go.Pie(
    labels=["Less than six months", "Six months or longer"],
    values=[37, 63],
    name="Sentence length",
    marker_colors=colors,
    direction ='clockwise',
    sort=False,
    title_text=prt_theme.wrap_labels("<br>Almost two in five were sentenced to serve less than six months", 38), # Wrapping the title
    title_position="bottom center",
    title_font_weight='bold',
    title_font_size=17,
), 1, 2)

# Update traces to create a donut chart and remove labels
fig.update_traces(hole=0.7, hoverinfo="none", textinfo="none")

# Add centred annotations with the first value of each pie chart
fig.update_layout(
    showlegend=False,
    annotations=[
        dict(text=f"{fig.data[0].values[0]}%", x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
             font_size=30, font_weight="bold", showarrow=False, xanchor="center"),
        dict(text=f"{fig.data[1].values[0]}%", x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
             font_size=30, font_weight="bold", showarrow=False, xanchor="center")
    ],
    margin = dict(t=20, b=25, l=0, r=25),
)

# fig.show()
py.plot(fig, filename="sentenced_receptions")