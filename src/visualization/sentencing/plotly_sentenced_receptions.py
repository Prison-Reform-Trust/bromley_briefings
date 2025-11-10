#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the proportion of sentenced receptions in England & Wales by offence type and sentence length.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Local modules
import src.utilities as utils
from src.visualization import prt_theme

# Set template
utils.setup_plotly_template()

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = ""
SUBTITLE = ""
SOURCE = "Ministry of Justice (2024). Offender management statistics quarterly: April to June 2024."
OUTPUT_PATH = utils.get_output_path(
    section='sentencing',
    filename='sentenced_receptions.html'
)


def create_chart() -> go.Figure:
    """Generates a pie chart showing the proportion of sentenced receptions for
    different offence types and sentence lengths.
    Returns:
        go.Figure: Plotly figure object.
    """
    colors = ["rgb(160, 29, 40)", "rgba(84, 86, 91, 0.15)"]
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'domain'}, {'type': 'domain'}]],
        subplot_titles=[" ", " ", " "],
        shared_xaxes=True,
        shared_yaxes=False,
        vertical_spacing=0.001
    )

    # Create subplots: use 'domain' type for Pie subplot
    fig.add_trace(go.Pie(
        labels=["Non-violent offence", "Violent offence"],
        values=[55, 45],
        name="Offences",
        marker_colors=colors,
        direction='clockwise',  # Setting direction and sort attributes to match for each chart
        sort=False,
        title_text=prt_theme.wrap_labels("<br>The majority have committed a non-violent crime", 32),
        title_position="bottom center",
        title_font_weight='bold',
        title_font_size=17,
    ), 1, 1)

    fig.add_trace(go.Pie(
        labels=["Less than six months", "Six months or longer"],
        values=[37, 63],
        name="Sentence length",
        marker_colors=colors,
        direction='clockwise',
        sort=False,
        title_text=prt_theme.wrap_labels("<br>Almost two in five were sentenced to serve less than six months", 38),
        title_position="bottom center",
        title_font_weight='bold',
        title_font_size=17,
    ), 1, 2)

    # Update traces to create a donut chart and remove labels
    fig.update_traces(hole=0.7, hoverinfo="none", textinfo="none")

    # Add centred annotations with the first value of each pie chart
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text=f"{fig.data[0].values[0]}%", x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
                font_size=30, font_weight="bold", showarrow=False, xanchor="center"),
            dict(text=f"{fig.data[1].values[0]}%", x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
                font_size=30, font_weight="bold", showarrow=False, xanchor="center")
        ],
        margin=dict(t=20, b=25, l=0, r=25),
    )

    return fig


def main() -> None:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = create_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE,
    )

if __name__ == "__main__":
    main()
