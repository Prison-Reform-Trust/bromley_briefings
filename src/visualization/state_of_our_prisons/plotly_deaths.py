"""
A Plotly chart showing the proportion of deaths in prison in England & Wales by:
    - type
    - gender
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go

# Local modules
import src.utilities as utils

# Set template
utils.setup_plotly_template()

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Deaths in prisons in England and Wales"
SUBTITLE = "More than 400 people died in prison in the year to September 2025"
SOURCE = "Ministry of Justice (2025). Safety in custody: quarterly update to June 2025"
OUTPUT_PATH = utils.get_output_path(
    section='state_of_our_prisons',
    filename='deaths.html'
)


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a sunburst chart showing number and proportion of deaths in prison by type and gender."""

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        ids=df["ids"],
        labels=df['death_type'],
        parents=df["parent"],
        values=df["value"].tolist(),
        branchvalues="total",
        texttemplate="<b>%{label}</b><br>%{value}",
        hovertemplate="<b>%{label}</b><br>%{value} deaths<br>%{percentParent: .0%} of %{parent}<extra></extra>",
        marker_line_color="#F7F2F2",
        insidetextorientation="horizontal",
        ))

    fig.update_layout(
        margin=dict(t=0, b=20, l=0, r=0),
        uniformtext=dict(minsize=11, mode="hide"),
        height=500,
        )

    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    # utils.setup_plotly_template()
    data_path = os.path.join(CONFIG['data']['clnFilePath'], "state_of_our_prisons/deaths.csv")
    df = utils.load_data(data_path)
    fig = create_chart(df)
    return fig


def main() -> None:
    """Generates the chart, and saves it as an HTML file using a Jinja2 template."""
    fig = prepare_chart()
    utils.save_plotly_chart_as_html(
        fig=fig,
        output_path=OUTPUT_PATH,
        title=TITLE,
        subtitle=SUBTITLE,
        source=SOURCE,
    )


if __name__ == "__main__":
    main()
