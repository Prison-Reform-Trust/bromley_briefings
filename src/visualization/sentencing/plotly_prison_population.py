#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title: How many people do we imprison in England & Wales?
Subtitle: There are around 86,000 people in prison. The prison population has risen by 93% in the last 30 years—and it is predicted to rise further still
Source: Ministry of Justice (2024). Prison population projections: 2024 to 2029.
'''

# Importing libraries
import os

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv
from matplotlib import colors

# Local scripts
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

## Load environment variables and config
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
config = utils.read_config()

##Adding plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), api_key=os.getenv("PLOTLY_API_KEY")
)
#Setting default Plotly template
pio.templates.default = "prt_template"

# Get colorway from template
COLORWAY = pio.templates[pio.templates.default].layout.colorway
PROJECTION_SHADING = f'rgba{colors.to_rgba(COLORWAY[0], alpha=0.2)}'

def create_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison", annotation_type="y-axis")

    fig.add_trace(
        go.Scatter(
            name="Prison population",
            x=df["date"],
            y=df["population"].tolist(),
            mode="lines",
            hovertemplate="%{y} prisoners<extra></extra>",
        ),
    )

    fig.add_trace(
        go.Scatter(
            name='Lower projection',
            x=df['date'],
            y=df['l_projection'].tolist(),
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
            y=df['c_projection'].tolist(),
            marker_color=COLORWAY[0],
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
            y=df['h_projection'].tolist(),
            marker_color="#444",
            line_width=0,
            mode='lines',
            fillcolor=PROJECTION_SHADING,
            fill='tonexty',
            hovertemplate="%{y} prisoners",
            cliponaxis = False,
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
    fig.update_xaxes(
        range=['1989-1-1', '2031-01-01'],
        )

    # Axis parameter adjustments
    fig.update_layout(
        xaxis_ticks="inside",
        yaxis_tickformat= ",.0f",
        hovermode="x",
        margin_pad = 5,
        margin = dict(t=20, b=25, l=0, r=25),
        annotations=annotations,

        )

def main():
    DATA = "sentencing/prison_population_inc_projections.csv"
    df = utils.load_data(f"{config['data']['clnFilePath']}{DATA}")
    fig = create_chart(df)
    py.plot(fig, filename="prison_population_inc_projections")
    return df

if __name__ == "__main__":
    main()