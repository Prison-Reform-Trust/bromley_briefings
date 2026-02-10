"""
This script provides useful functions to all other scripts
"""
import os
import textwrap
from typing import Optional

import chart_studio.plotly as py  # Online plotting
import pandas as pd
import plotly.graph_objs as go  # Offline plotting
import plotly.io as pio
import yaml
from jinja2 import Template

from src.visualization import prt_theme


def read_config():
    """Read in config file"""
    config = {k: v for d in yaml.load(
        open('config.yaml', encoding='utf-8'),
        Loader=yaml.SafeLoader) for k, v in d.items()}
    return config

# Load config once at module level
CONFIG = read_config()


def setup_plotly_template():
    """Sets Plotly template to PRT theme."""
    pio.templates.default = "prt_template"


# Read data
def load_data(
        filepath: str,
        usecols=None,
        parse_dates=None,
        date_format=None,
        ) -> pd.DataFrame:
    """Loads processed data from CSV with optional column selection and date
        parsing."""
    return pd.read_csv(
        filepath,
        usecols=usecols,
        parse_dates=parse_dates,
        date_format=date_format)


# Generate annotations dynamically
def generate_annotations(
        traces,
        colorway,
        max_chars=None,
        y_label=None,
        y_label_placement=None,
        y_offset_dict=None,
        x_pad=None):
    """
    Generates trace labels and y-label annotation, allowing individual y-value
        adjustments.

    Parameters:
        traces (list): Plotly trace objects.
        colorway (list): Color scheme from Plotly template.
        max_chars (int, optional): Set maximum number of characters for trace
            labels before text is wrapped.
        y_label (str, optional): Y-axis label text.
        y_label_placement (str, optional): Y-axis label placement.
        y_offset_dict (dict, optional): A dictionary mapping trace names
            (years) to y-offsets.
        x_pad (float or int, optional): Horizontal padding for trace labels.
    """
    if y_offset_dict is None:
        y_offset_dict = {}

    annotations = [
        dict(
            xref="x",
            yref="y",
            x=trace.x[-1] + x_pad if x_pad else trace.x[-1],
            # Apply y-offset if available
            y=trace.y[-1] + y_offset_dict.get(trace.name, 0),
            text=(
                prt_theme.wrap_labels(trace.name, max_chars)
                if max_chars else trace.name
            ),
            xanchor="left",
            align="left",
            showarrow=False,
            font_color=colorway[i],
            font_size=12,
        )
        for i, trace in enumerate(traces)
    ]

    # Add y-axis label
    annotations.append(
        dict(
            xref="x",
            yref="paper",
            x=y_label_placement if y_label_placement else traces[0].x[0],
            y=1.04,
            align="left",
            xanchor="left",
            showarrow=False,
            text=y_label if y_label else "",
            font_size=14,
        )
    )

    return annotations


# Main function to create chart
def create_chart(
    xaxis_tickvals,
    xaxis_ticktext,
    traces,
    title: str,
    y_label: str,
    xaxis_range: tuple,
    yaxis_dtick=None,
    xaxis_range_vals=(1, 53),
    xaxis_nticks=None,
    yaxis_nticks=6,
    y_offset_dict=None,
) -> go.Figure:
    """Creates the Plotly chart with adjustable parameters."""

    fig = go.Figure(traces)

    # Wrap title for better formatting
    chart_title = textwrap.wrap(title, width=65)

    # Get colorway from template
    colorway = pio.templates[pio.templates.default].layout.colorway

    # Generate annotations with optional y_offset_dict
    annotations = generate_annotations(
        traces,
        colorway,
        y_label,
        y_offset_dict
        )

    fig.update_layout(
        title="<br>".join(chart_title),
        yaxis_dtick=yaxis_dtick if yaxis_dtick else 2000,
        xaxis_tickvals=xaxis_tickvals,
        xaxis_ticktext=xaxis_ticktext,
        hovermode='x',
        annotations=annotations,
    )

    # Apply axis settings
    fig.update_yaxes(range=xaxis_range, nticks=yaxis_nticks)
    fig.update_xaxes(range=xaxis_range_vals, nticks=xaxis_nticks)

    return fig


def get_output_path(section: str, filename: str) -> str:
    """Generate output path from config values."""
    return os.path.join(
        CONFIG['viz']['outPath'],
        CONFIG['report_section'][section],
        filename
    )


# Save chart (offline and online)
def save_chart(fig, filename):
    """Saves the chart as an image and uploads it online."""
    fig.write_image(os.path.join(CONFIG['viz']['outPath'], f'{filename}.svg'))

    fig.layout.images = [
        dict(
            source="https://i.ibb.co/jhfYbyc/PRTlogo-RGB.png",
            xref="paper",
            yref="paper",
            x=-0.08,
            y=1.25,
            sizex=0.15,
            sizey=0.15,
            xanchor="left",
            yanchor="top",
        )
    ]

    layout_atr = prt_theme.pio.templates["prt_template"].layout
    fig.update_layout(
        width=layout_atr.width,
        height=layout_atr.height,
    )

    py.plot(fig, filename=filename)  # NOTE: This will need to be removed following migration away from chart studio


def save_plotly_chart_as_html(
    fig: go.Figure,
    output_path: str,
    title: str,
    subtitle: str,
    source: str,
    template_path: Optional[str] = None,
    config: Optional[dict] = None,
    embed_styles: bool = False,
    styles_path: Optional[str] = None
) -> None:
    """Saves a Plotly figure as an HTML file using a Jinja2 template.

    Args:
        fig (go.Figure): Plotly figure object.
        output_path (str): Path where the HTML file will be saved.
        title (str): Chart title.
        subtitle (str): Chart subtitle.
        source (str): Data source attribution.
        template_path (str, optional): Path to Jinja2 template. Uses default if None.
        config (dict, optional): Plotly config. Uses default if None.
        embed_styles (bool): Whether to embed CSS styles directly in HTML. Default False.
        styles_path (str, optional): Path to CSS file. Uses default if None.
    """
    if config is None:
        config = CONFIG

    if template_path is None:
        template_path = "reports/figures/prt_web_template.html"

    if styles_path is None:
        styles_path = "reports/figures/styles.css"

    # Load CSS styles if embedding is requested
    embedded_styles = ""
    if embed_styles and os.path.exists(styles_path):
        with open(styles_path, "r", encoding="utf-8") as css_file:
            embedded_styles = css_file.read()

    plotly_jinja_data = {
        "title": title,
        "subtitle": subtitle,
        "fig": fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            config=config['plotly']['config']
        ),
        "source": source,
        "embedded_styles": embedded_styles,
        "embed_styles": embed_styles
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as output_file:
        with open(template_path, "r", encoding="utf-8") as template_file:
            j2_template = Template(template_file.read())
            output_file.write(j2_template.render(plotly_jinja_data))
