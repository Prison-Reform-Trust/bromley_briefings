#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: If we imprison more people won't crime fall?
Subtitle: International comparisons show there is no consistent link between the two
Source: Data source not specified.
"""

import os
import pandas as pd
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
from dotenv import find_dotenv, load_dotenv

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load environment variables and configuration
load_dotenv(find_dotenv())
config = utils.read_config()

# Set Plotly credentials
chart_studio.tools.set_credentials_file(
    username=os.getenv("PLOTLY_USERNAME"), 
    api_key=os.getenv("PLOTLY_API_KEY")
)

# Set default Plotly template
pio.templates.default = "prt_template"

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a multi-country subplot chart comparing imprisonment and crime rates."""
    
    # Get colorway from the current Plotly template
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Get unique country names
    countries = df["country"].unique()
    num_subplots = len(countries)

    # Define subplot spacing
    gap = 0.05
    subplot_width = (1 - gap * (num_subplots - 1)) / num_subplots

    # Create subplots
    fig = make_subplots(
        rows=1, 
        cols=num_subplots, 
        specs=[[{"secondary_y": True}] * num_subplots],
    )

    # Add subplot titles as annotations
    annotations = []
    for i, country in enumerate(countries):
        start_domain = i * (subplot_width + gap)
        end_domain = start_domain + subplot_width
        title_x = (start_domain + end_domain) / 2

        # Update subplot domains
        fig.update_layout(**{f"xaxis{i+1}_domain": [start_domain, end_domain]})

        # Add title annotation
        annotations.append(
            dict(
                x=title_x,
                y=1.1,
                xref="paper",
                yref="paper",
                text=f"<b>{country}</b>",
                showarrow=False,
                font_size=14,
                xanchor="center"
            )
        )

    # Add traces for each country
    for idx, country in enumerate(countries):
        df_country = df[df["country"] == country]

        fig.add_trace(
            go.Scatter(
                x=df_country["year"],
                y=df_country["value_prison"],
                mode="lines+markers",
                line_color=colorway[0],
                text=df_country["country"],
                name="Imprisonment rate",
                hovertemplate="<b>%{text}</b><br>%{x}: %{y} per 100,000",
            ), 
            row=1, col=idx+1
        )

        fig.add_trace(
            go.Scatter(
                x=df_country["year"],
                y=df_country["value_crime"],
                mode="lines+markers",
                line_color=colorway[1],
                text=df_country["country"],
                name="Crime rate",
                hovertemplate="<b>%{text}</b><br>%{x}: %{y:,.0f} per 100,000",
            ), 
            row=1, col=idx+1, secondary_y=True
        )

    # Configure layout
    fig.update_layout(
        margin=dict(t=20, b=25, l=55, r=70, pad=5),
        annotations=annotations,
        xaxis_ticks="inside",
        dragmode=False,
    )

    # Sync y-axes ranges for primary and secondary y-axes across all subplots
    primary_y_range = [0, 210]
    secondary_y_range = [0, 12600]

    # Update y-axes for all subplots
    for i in range(1, num_subplots + 1):
        # Primary y-axis: Only show the title on the first subplot
        fig.update_yaxes(
            title_text="Imprisonment rate per 100,000" if i == 1 else '',
            titlefont_color=colorway[0],
            showgrid=True,
            gridcolor="#CACFDB",
            range=primary_y_range,  # Set range for primary y-axis
            dtick=50,
            tickfont_color=colorway[0],
            secondary_y=False,
            showticklabels=True,  # Ensure tick labels are shown
            row=1, col=i
        )

        # Secondary y-axis: Only show the title on the last subplot
        fig.update_yaxes(
            title_text="Crime rate per 100,000" if i == num_subplots else '',
            titlefont_color=colorway[1],
            showgrid=False,
            range=secondary_y_range,  # Set range for secondary y-axis
            dtick=3000,
            tickformat=",.0f",
            tickfont_color=colorway[1],
            tickmode="sync",
            secondary_y=True,
            showticklabels=True,  # Ensure tick labels are shown
            row=1, col=i
        )

    # Remove unnecessary tick labels from specific subplots
    for i in range(1, num_subplots + 1):
        # Remove primary y-axis tick labels from subplots where they are unnecessary
        if i != 1:  # Keep tick labels only on the first subplot for primary y-axis
            fig.update_yaxes(showticklabels=False, row=1, col=i, secondary_y=False)
        
        # Remove secondary y-axis tick labels from subplots where they are unnecessary
        if i != num_subplots:  # Keep tick labels only on the last subplot for secondary y-axis
            fig.update_yaxes(showticklabels=False, row=1, col=i, secondary_y=True)

    return fig

def main() -> go.Figure:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    data_path = f"{config['data']['clnFilePath']}sentencing/international_rates.csv"
    df = utils.load_data(data_path)
    fig = create_chart(df)
    py.plot(fig, filename="international_rates")
    return fig

if __name__ == "__main__":
    main()