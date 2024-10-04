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
df = pd.read_csv("data/processed/sentencing/international_rates.csv")

## Plotting
# Get the unique values from the 'country' column
titles = df['country'].unique()

# Number of subplots
num_subplots = len(titles)

# Define the gap between subplots
gap = 0.05

# Calculate the width of each subplot
subplot_width = (1 - gap * (num_subplots - 1)) / num_subplots

# Create subplots
fig = make_subplots(
    rows=1, cols=num_subplots, 
    specs=[[{"secondary_y": True}] * num_subplots],
    )

annotations = []

for i in range(num_subplots):
    # Set spacing between subplots
    start_domain = i * (subplot_width + gap)
    end_domain = start_domain + subplot_width
    fig.update_layout(**{f'xaxis{i+1}_domain': [start_domain, end_domain]})

    # Calculate the position for the subplot titles
    title_x = (start_domain + end_domain) / 2
    annotations.append(
        dict(
            x=title_x,
            y=1.1,  # This places the title slightly above the plot
            xref="paper",
            yref="paper",
            text=titles[i],
            showarrow=False,
            font=dict(size=14),
            xanchor='center'
        )
    )

# Add the annotations to the layout
fig.update_layout(annotations=annotations)


# Adding traces
trace_list= []

for idx, country in enumerate(df["country"].unique()):
    df_country = df[df["country"] == country]

    fig.add_trace(go.Scatter(
        x=df_country["year"],
        y=df_country["value_prison"],
        mode="lines+markers",
        line_color=prt_template.layout.colorway[0],
        text=df_country['country'],
        name="Imprisonment rate",
        hovertemplate="<b>%{text}</b><br>%{x}: %{y} per 100,000"
        ), 
        row=1,
        col=idx+1,
        )
    
    fig.add_trace(go.Scatter(
        x=df_country["year"],
        y=df_country["value_crime"],
        mode="lines+markers",
        line_color=prt_template.layout.colorway[1],
        text=df_country['country'],
        name="Crime rate",
        hovertemplate="<b>%{text}</b><br>%{x}: %{y:,.0f} per 100,000",
        ),
        row=1,
        col=idx+1,
        secondary_y=True)

fig.add_traces(trace_list)

# Set y-axes titles
fig.update_layout(
    margin_pad = 5,
    margin = dict(t=30, b=50, l=70, r=70),
    autosize=False,
    height = 300,
    yaxis=dict(
        title_text="Imprisonment rate per 100,000",
        titlefont_color=prt_template.layout.colorway[0],
        ),
    
    yaxis6=dict(
        title_text="Crime rate per 100,000",
        titlefont_color=prt_template.layout.colorway[1],
        ),
)
# Set y-axis ranges
fig.update_yaxes(
    range=[0,210],
    dtick=50,
    tickfont_color=prt_template.layout.colorway[0],
    secondary_y=False)

fig.update_yaxes(
    range=[0,12600],
    dtick=3000,
    tickformat= ",.0f",
    tickfont_color=prt_template.layout.colorway[1],
    tickmode="sync",
    secondary_y=True)

# Removing ticklabels from inside ticks
for i in range(1,3):
    fig.update_yaxes(showticklabels=False, col=i, secondary_y=True)

for i in range(2,4):
    fig.update_yaxes(showticklabels=False, col=i, secondary_y=False)

# fig.show()
py.plot(fig, filename="international_rates")