#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Plotly chart showing the social characteristics of adult prisoners in England and Wales.
The chart is saved as an HTML file using a Jinja2 template for embedding in a web page.
"""

import os

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
CONFIG = utils.read_config()

# Jinja2 template variables
TITLE = "Social characteristics of adult prisoners"
SUBTITLE = ""
SOURCE = (
    "<br>Harker, L. et al. (2013). How safe are our children? NSPCC.<br>"
    "HM Inspectorate of Prisons (2024). Annual report 2023-24. HM Stationery Office.<br>"
    "Light, M., et al. (2013). Gender differences in substance misuse and mental health amongst prisoners. Ministry of Justice.<br>"
    "Ministry of Justice (2012). Accommodation, homelessness and reoffending of prisoners.<br>"
    "Ministry of Justice (2010). Compendium of reoffending statistics.<br>"
    "Ministry of Justice (2012). Estimating the prevalence of disability amongst prisoners.<br>"
    "Ministry of Justice (2012). Prisoners' childhood and family backgrounds.<br>"
    "Ministry of Justice (2012). The pre-custody employment, training and education status of newly sentenced prisoners.<br>"
    "Table KS611EW, Office for National Statistics (2012). 2011 Census.<br>"
    "Table 1, Office for National Statistics (2013). Families and households, 2012.<br>"
    "Office for National Statistics (2013). Labour market statistics, September 2013.<br>"
    "Office for National Statistics (2013). Population estimates for UK, England and Wales, Scotland and Northern Ireland — Mid 2012.<br>"
    "Welsh Government (2013). Absenteeism by pupil characteristics 2011/12.<br>"
    "Wiles, N. et al. (2006). Self-reported psychotic symptoms in the general population. The British Journal of Psychiatry, 188: 519-52."
)
OUTPUT_PATH = utils.get_output_path(
    section='people_in_prison',
    filename='social_characteristics.html'
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Processes the data to ensure it is in the correct format for plotting."""

    df["characteristic"] = pd.Categorical(df["characteristic"], ordered=True)

    df = df.melt(id_vars='characteristic', var_name="group").dropna().reset_index(drop=True)
    # Wrap and convert characteristic to categorical to maintain order
    df["wrapped_characteristic"] = df["characteristic"].apply(prt_theme.wrap_labels, max_chars=28)

    # Convert 'group' to categorical to maintain order
    df["group"] = pd.Categorical(df["group"], ordered=True)

    df["group"] = df["group"].cat.rename_categories({
        "prison_male": "Men in prison",
        "prison_female": "Women in prison",
        "prison_all": "Prison population (overall)",
        "general_pop": "General population",
    })

    return df


def generate_traces(df):
    """Generate chart traces"""

    colorway = pio.templates[pio.templates.default].layout.colorway
    colors = {
        "Men in prison": colorway[1],
        "Women in prison": colorway[0],
        "Prison population (overall)": colorway[4],
        "General population": colorway[3],
    }

    traces = [
        go.Scatter(
            x=df_group["value"].tolist(),
            y=df_group['wrapped_characteristic'].tolist(),
            orientation="h",
            mode="markers",
            name=str(group),
            text=df_group["group"].tolist(),
            texttemplate="%{text}%",
            textposition="top center",
            hovertemplate="%{x}",
            marker_color=colors.get(group, colorway[i % len(colorway)]),  # Use colorway for fallback
        )
        for i, (group, df_group) in enumerate(df.groupby("group", sort=False, observed=True))
    ]

    return traces


def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a Plotly horizontal bar chart of proportion of all self-harm incidents by gender."""

    fig = go.Figure()
    traces = generate_traces(df)

    fig.add_traces(traces)

    # Configure axes
    fig.update_yaxes(
        autorange="reversed",
        type="category",
        automargin=True,
    )

    fig.update_xaxes(
        zeroline=False,
        showline=True,
        ticks="outside",
        ticksuffix='%',
        range=[0, 100],
        fixedrange=True
    )

    # Configure layout
    fig.update_layout(
        height=1000,
        margin_b=45,
        hovermode="y unified",
        hoverlabel_bgcolor='rgba(247, 242, 242, 0.8)',
        showlegend=True,
        legend=dict(
            orientation="h",
            traceorder="normal",
            itemclick="toggleothers",
            itemdoubleclick=False,
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1.05,
        ),
    )
    return fig


def prepare_chart() -> go.Figure:
    """Loads data and prepares the Plotly chart."""
    utils.setup_plotly_template()
    data_path = os.path.join(CONFIG["data"]["clnFilePath"], "people_in_prison/social_characteristics.csv")
    df = utils.load_data(data_path).pipe(process_data)
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
