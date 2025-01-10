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
df = (
    pd.read_csv("data/processed/sentencing/ipp_post_tariff.csv", usecols=['Years over tariff', 'short_year', 'number'], dtype={'number': 'Int64'})
    .dropna()
    .rename(columns={'Years over tariff': 'years', 'short_year': 'short_years', 'number': 'value'})
)
# Calculating the median number of years post tariff
# Cumulative frequency
df["cumulative_sum"] = df["value"].cumsum()

# Total frequency
total = df["value"].sum()

# Find the median
median_year = int(df.loc[df["cumulative_sum"] >= total / 2, "short_years"].iloc[0])

# Set marker colors to highlight median year
marker_color = [prt_template.layout.colorway[0],] * len(df['short_years'])
marker_color[median_year] = prt_template.layout.colorway[1]

## Plotting
fig = go.Figure()

fig.add_traces(
    go.Bar(
        x=df["short_years"],
        y=df["value"],
        customdata=df['years'],
        hovertemplate="%{y} people<extra>%{customdata}</extra>",
        marker_color=marker_color,
    )
)

fig.update_layout(
    hovermode='x',
    margin_pad=5,
    margin=dict(t=20, b=25, l=0, r=25),
)

fig.update_yaxes(
    range=[0,145],
    tickformat= ",.0f",
    automargin=True, #To avoid clipping of y-axis labels
)

fig.update_xaxes(
    type='category',
    dtick=1,
    title_text="Additional years spent in prison post-tariff",
    titlefont_size= 15,
    title_standoff = 25,
    automargin=True, #To allow necessary title spacing
)

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(
    annotations, "People in prison", annotation_type="y-axis"
)

# Adding annotations to layout
fig.update_layout(annotations=annotations)
py.plot(fig, filename="ipp_post_tariff")