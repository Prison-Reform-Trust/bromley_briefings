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
#Setting default Plotly template and assigning attributes to prt_template
pio.templates.default = "prt_template"
prt_template = prt_theme.pio.templates['prt_template']

# Read in datasets
df = pd.read_csv("data/processed/sentencing/sentence_lengths.csv")
# Filtering for every other year
df = df[::2]

# Create text arrays with labels only for the first and last observations
text_total = [""] * len(df)
text_indictable = [""] * len(df)
if len(df) > 1:
    text_total[0] = f"{df['total'].iloc[0]} months"
    text_total[-4] = f"{df['total'].iloc[-4]} months"
    text_total[-1] = f"{df['total'].iloc[-1]} months"
    text_indictable[0] = f"{df['indictable'].iloc[0]} months"
    text_indictable[-4] = f"{df['indictable'].iloc[-4]} months"
    text_indictable[-1] = f"{df['indictable'].iloc[-1]} months"

## Plotting
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["indictable"],
        y=df["year"],
        orientation="h",
        name="Indictable offences (more serious)",
        text=text_indictable,
        texttemplate="%{text}",
        textposition="inside",
        hovertemplate="<b>%{y}</b>: %{x} months",
        zorder=-1,  # Setting trace to be overlaid
        marker_color=prt_template.layout.colorway[1]
    ),
)
fig.add_trace(
    go.Bar(
        x=df["total"],
        y=df["year"],
        orientation="h",
        name="All offences",
        text=text_total,
        texttemplate="%{text}",
        textposition="inside",
        hovertemplate="<b>%{y}</b>: %{x} months",
        zorder=1,  # Setting trace to be on top
        marker_color=prt_template.layout.colorway[0]
    ),
)

fig.update_yaxes(autorange="reversed")
fig.update_xaxes(zeroline=False)

fig.update_layout(
    barmode="overlay",
    hovermode='closest',
    xaxis_ticks="inside",
    margin_pad=5,
    margin=dict(t=20, b=25, l=40, r=25),
)

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(
    annotations, "Average sentence length", annotation_type="y-axis"
)

# Adding annotations to layout
fig.update_layout(annotations=annotations)
# fig.show()
py.plot(fig, filename="sentence_lengths")