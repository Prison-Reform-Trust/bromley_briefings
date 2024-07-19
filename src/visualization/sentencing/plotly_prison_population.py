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
from matplotlib import colors

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
PROJECTION_SHADING = f'rgba{colors.to_rgba(prt_template.layout.colorway[0], alpha=0.2)}'

#Read in datasets
df = pd.read_csv("data/processed/sentencing/prison_population_inc_projections.csv")

## Plotting
# Create figure with secondary y-axis
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        name="Prison population",
        x=df["date"],
        y=df["population"],
        mode="lines",
        hovertemplate="%{y} prisoners<extra></extra>",
    ),
)

fig.add_trace(
    go.Scatter(
        name='Lower projection',
        x=df['date'],
        y=df['l_projection'],
        marker_color="#444",
        line_width=0,
        mode='lines',
        fillcolor=PROJECTION_SHADING,
        hovertemplate="%{y} prisoners",
        ),
)

fig.add_trace(
    go.Scatter(
        name='Central projection',
        x=df['date'],
        y=df['c_projection'],
        marker_color=prt_template.layout.colorway[0],
        mode='lines',
        line_dash="dot",
        fillcolor=PROJECTION_SHADING,
        fill='tonexty',
        hovertemplate="%{y} prisoners",
        ),
)

fig.add_trace(
    go.Scatter(
        name='High projection',
        x=df['date'],
        y=df['h_projection'],
        marker_color="#444",
        line_width=0,
        mode='lines',
        fillcolor=PROJECTION_SHADING,
        fill='tonexty',
        hovertemplate="%{y} prisoners",
        ),
)

# Set y-axes range
fig.update_yaxes(
    range=[0, 120500],
    dtick=20000,
    automargin=True,
    domain=[0,0.95]
    )

# Set x-axes range
fig.update_xaxes(range=['1989-1-1', '2029-01-01'],
                dtick="M60")

# Axis parameter adjustments
fig.update_layout(
    xaxis_ticks="inside",
    yaxis_tickformat= ",.0f",
    hovermode="x",
    margin_pad = 5,
    margin_t = 20)

## Chart annotations
annotations = []

# Add title
prt_theme.add_title(fig, "The prison population has risen by 93% in the last 30 years—and it is predicted to rise further still")

# Add source annotation with default placement
prt_theme.add_annotation(annotations, ("Ministry of Justice (2023). Offender management statistics: Prison population 2023.<br>"
                                        "Ministry of Justice (2024). Population and capacity briefing for 5 July 2024.<br>"
                                        "Ministry of Justice (2024). Prison population projections: 2023 to 2028."), 
                                        annotation_type="source")

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(annotations, "People in prison", annotation_type="y-axis", y=1.05)

# Adding annotations to layout
fig.update_layout(annotations=annotations)

py.plot(fig, filename="prison_population_inc_projections")