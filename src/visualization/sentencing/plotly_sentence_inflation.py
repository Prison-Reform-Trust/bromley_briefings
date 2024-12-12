# Importing libraries
import os

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv

from src.visualization import prt_theme

## Loading environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

## Adding Plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), api_key=os.getenv("PLOTLY_API_KEY")
)
#Setting default Plotly template
pio.templates.default = "prt_template"

# Read in datasets
df = pd.read_csv("data/processed/sentencing/sentence_inflation.csv")

# Wrapping x-axis labels using textwrap.fill with apply
df['wrapped_offence'] = df['offence'].apply(prt_theme.wrap_labels, max_chars=14)

## Plotting
fig = go.Figure()

trace_list= []

for i in df["year"].unique():
    df_year = df[df["year"] == i]

    trace = go.Bar(
        x=df_year["wrapped_offence"],
        y=df_year["length"],
        text=df_year['length'],
        name=str(df_year['year'].iloc[0]),
        customdata=df_year['year'],
        hovertemplate="<b>%{customdata}</b><br>%{x}: %{y} months<extra></extra>"
        )
    
    trace_list.append(trace)
"""
Possible development of arrows trace to show the percentage increase between the two years
arrow_trace = go.Scatter(
    x=trace_list[1].x,
    y=trace_list[1].y,
    mode="markers",
    hovertemplate="<extra></extra>",
    marker_symbol="arrow-up",
)

trace_list.append(arrow_trace)
"""

fig.add_traces(trace_list)

fig.update_layout(
    barmode="group",
    hovermode='closest',
    xaxis_ticks="inside",
    xaxis_tickangle=0,
    uniformtext_minsize=8, 
    uniformtext_mode='hide',
    margin_pad=5,
    margin=dict(t=20, b=60, l=40, r=25),
)

fig.update_xaxes(tickfont_size=12)

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(
    annotations, "Average sentence length (months)", annotation_type="y-axis"
)

# Adding annotations to layout
fig.update_layout(annotations=annotations)
py.plot(fig, filename="sentence_inflation")