#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title: Scotland and England & Wales have the highest imprisonment rates in western Europe.
Source: World Prison Brief, Institute for Crime & Justice Policy Research. 10 July 2024.
'''

# Importing libraries
import os

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import find_dotenv, load_dotenv

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

def create_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    annotations = prt_theme.add_annotation(None, "People in prison per 100,000 population", annotation_type="y-axis")
    
    fig.add_trace(
        go.Bar(
            x=df["rate"].tolist(),
            y=df["country"],
            orientation="h",
            hovertemplate="%{text} per 100,000 population<extra></extra>",
            text = df['rate'].tolist(),
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis = False,
        ),
    )
    fig.update_yaxes(
        type='category',
        autorange="reversed",
        automargin=True,
        domain=[0,0.95]
        )
    
    fig.update_layout(
    xaxis_ticks="inside",
    margin_pad = 5,
    margin = dict(t=20, b=25, l=0, r=25),
    annotations=annotations,
    dragmode=False
    )
    
    return fig

def main():
    df = utils.load_data(f"{config['data']['clnFilePath']}sentencing/imprisonment_rates.csv")
    fig = create_chart(df)
    py.plot(fig, filename="imprisonment_rates")
    return None

if __name__ == "__main__":
    main()