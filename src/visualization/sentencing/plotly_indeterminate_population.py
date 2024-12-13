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
df = (
    pd.read_csv("data/processed/sentencing/indeterminate_population.csv", usecols=['year', 'indet_unreleased', 'indet_recalled'])
    .rename(columns={'indet_unreleased': 'Unreleased', 'indet_recalled': 'Recalled'})
    .melt(id_vars='year', value_vars=['Unreleased', 'Recalled'], var_name='custody_type')
)

## Plotting
fig = go.Figure()

trace_list= []

for i in df["custody_type"].unique():
    df_type = df[df["custody_type"] == i]

    trace = go.Bar(
        x=df_type["year"],
        y=df_type["value"],
        name=str(df_type['custody_type'].iloc[0]),
        # customdata=df_type['year'],
        hovertemplate="%{y:,.0f}"
        )
    
    trace_list.append(trace)

fig.add_traces(trace_list)


fig.update_layout(
    barmode="stack",
    hovermode='x',
    xaxis_dtick=2,
    yaxis_tickformat= ",.0f",
    yaxis_automargin=True, #To avoid clipping of y-axis labels
    margin_pad=5,
    margin=dict(t=20, b=25, l=0, r=25),
)

## Chart annotations
annotations = []

# Add y-axis label annotation with placement based on dataframe column
prt_theme.add_annotation(
    annotations, "People in prison", annotation_type="y-axis"
)

# Adding annotations to layout
fig.update_layout(annotations=annotations)
py.plot(fig, filename="indeterminate_population")