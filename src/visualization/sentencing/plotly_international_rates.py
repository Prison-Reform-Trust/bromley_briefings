#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart comparing imprisonment rates and crime rates across multiple countries.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "If we imprison more people won't crime fall?"
SUBTITLE = "There is no link between the prison population and levels of crime according to the National Audit Office. International comparisons show there is no consistent link between the two"
SOURCE = (
    "<a href = https://www.prisonstudies.org/world-prison-brief-data>Institute for Crime and Justice Policy Research (2023). World Prison Brief. Birkbeck, University of London.</a><br>"
    "<a href = https://ec.europa.eu/eurostat/databrowser/view/crim_hist/default/table>Eurostat (2015). Crimes recorded by the police (1950-2000).</a><br>"
    "Clarke, S. (2013). Trends in crime and criminal justice, 2010. Eurostat.<br>"
    "Home Office (2023). Police recorded crime and outcomes open data tables: Outcomes open data ending March 2021.<br>"
    "Office for National Statistics (2022). UK population estimates, 1838 to 2020.<br>"
    "Statistics Finland (2023). 13ex -- Offences recorded and their solving by offence category according to the municipality of offence and year of reporting, 1980-2022.<br>"
    "<a href = https://www.stat.fi/tup/suoluk/suoluk_vaesto_en.html>Statistics Finland (2023). Population and society.</a><br>"
    "<a href = https://www150.statcan.gc.ca/n1/pub/11-630-x/11-630-x2015001-eng.htm#def1>Statistics Canada (2018). Canada's crime rate: Two decades of decline.</a><br>"
    "Statistics Canada (2023). Incident-based crime statistics, by detailed violations, Canada, provinces, territories, Census Metropolitan areas and Canadian Forces Military Police."
)
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='international_rates.html'
)


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
        height=300,
        margin=dict(t=30, b=25, l=55, r=70, pad=5),
        annotations=annotations,
    )

    # Sync y-axes ranges for primary and secondary y-axes across all subplots
    primary_y_range = [0, 210]
    secondary_y_range = [0, 12600]

    # Update y-axes for all subplots
    for i in range(1, num_subplots + 1):
        # Primary y-axis: Only show the title on the first subplot
        fig.update_yaxes(
            title_text="Imprisonment rate per 100,000" if i == 1 else '',
            title_font_color=colorway[0],
            title_font_size=14,
            title_standoff=20,
            showgrid=True,
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
            title_font_color=colorway[1],
            title_font_size=14,
            title_standoff=20,
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


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = f"{CONFIG['data']['clnFilePath']}sentencing/international_rates.csv"
    df = utils.load_data(data_path)
    fig = create_chart(df)
    return fig


def main() -> go.Figure:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    utils.setup_plotly_template()
    fig = prepare_chart()

    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE
    )
    return fig


if __name__ == "__main__":
    main()
