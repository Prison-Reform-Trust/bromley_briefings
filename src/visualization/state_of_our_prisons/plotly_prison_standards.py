#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Standards are slowly starting to recover — but purposeful activity remains poor
Subtitle: Percentage of prisons that received a type of 'good' or 'reasonably good' by HM Inspectorate of Prisons, by criteria
Source: HM Chief Inspector of Prisons. Annual report 2023–24 and previous editions.
Note 2020 is not included due to low number of prisons inspected during Covid-19
"""

import os

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Local modules
import src.utilities as utils
import src.visualization.prt_theme as prt_theme

# Load configuration
config = utils.read_config()

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Set trace order, adjust year labels and make type categorical."""
    # Define the desired order
    desired_order = [
        "Safety",
        "Respect",
        "Purposeful activity",
        "Preparation for release", 
        ]
    
    # Extract first four digits of year e.g. 2015 and convert to datetime
    df["year"] = pd.to_datetime(df["year"].astype(str).str.extract(r"^(\d{4})")[0]).dt.year
    df["type"] = (
        df["type"]
        .astype(pd.CategoricalDtype(categories=desired_order, ordered=True))
    )
    return df

def generate_traces(df:pd.DataFrame) -> list:
    """Generates Plotly traces for each group in dataset."""
    # Set opacity values and target index for default highlighted trace
    highlighted_opacity = 1.0
    default_opacity = 0.2
    default_target = "Purposeful activity"
    
    traces = [
        go.Scatter(
            x=df_group["year"].tolist(),
            y=df_group["percent"].tolist(),
            mode="lines",
            opacity=highlighted_opacity if group == default_target else default_opacity,
            text=df_group['type'],
            hovertemplate="<b>%{x}:</b> %{y}",
            name=str(group),
        )
        for group, df_group in df.groupby(df["type"], sort=False, observed=True)
    ]

    return traces

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Creates a line chart showing proportion of prisons that received a type of 'good' or 'reasonably good' from HMIP since 2010."""

    fig = go.Figure()
    traces = generate_traces(df)
    fig.add_traces(traces)

    annotations = prt_theme.add_annotation(None, "Prisons rated 'good' or 'reasonably good'", annotation_type="y-axis")

    # Set axes ranges
    fig.update_yaxes(range=[0, 102])
    fig.update_xaxes(range=[2007.8, 2024.2])

    # Layout parameter adjustments
    fig.update_layout(
        margin_l=45,
        yaxis_ticksuffix="%",
        hovermode="closest",
        hoverlabel_bgcolor="rgba(247, 242, 242, 0.8)",
        annotations=annotations,
        clickmode="event",
        showlegend=True,
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.9,
            xanchor="right",
            x=0.995,
        ),
    )

    return fig

def generate_html(fig: go.Figure) -> str:
    """Generates the HTML content for the chart with custom JavaScript."""
    fig_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn", config = {'displayModeBar': False})

    custom_js = """
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var gd = document.getElementsByClassName('plotly-graph-div')[0];
            if (!gd) return;

            // Set the initial state to have all traces at the default opacity
            var default_opacity = 0.2;
            var highlighted_opacity = 1.0;
            var reset_opacity = Array(gd.data.length).fill(default_opacity);

            gd.on('plotly_click', function(eventdata){
                // Reset all traces to default opacity
                Plotly.restyle(gd, {'opacity': reset_opacity});
                
                // Set clicked trace to highlighted opacity
                var update = {'opacity': Array(gd.data.length).fill(default_opacity)};
                update.opacity[eventdata.points[0].curveNumber] = highlighted_opacity;
                Plotly.restyle(gd, update);
            });
        });
    </script>
    """
    
    # Inject the JavaScript before closing the body tag
    return fig_html.replace("</body>", f"{custom_js}\n</body>")

def save_html(html_content: str) -> None:
    """Saves the HTML content to a file."""
    output_path = os.path.join(config['viz']['outPath'], "state_of_our_prisons/prison_standards.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def test_data() -> pd.DataFrame:
    """Loads data, generates the chart, and uploads it to Chart Studio."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/prison_standards.csv")
    df = utils.load_data(data_path).pipe(process_data)
    return df

def main() -> None:
    """Loads data, generates the chart, and saves it as an HTML file with hover effects."""
    utils.setup_plotly_template()
    data_path = os.path.join(config['data']['clnFilePath'], "state_of_our_prisons/prison_standards.csv")
    df = utils.load_data(data_path).pipe(process_data)
    fig = create_chart(df)
    py.plot(fig, filename="prison_standards")

    '''
    #TODO: #22 Highlight trace on click
    # Generate HTML content with JavaScript injection
    fig_html = generate_html(fig)
    save_html(fig_html)
    '''


if __name__ == "__main__":
    main()