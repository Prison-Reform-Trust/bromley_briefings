#Custom Plotly template for all charts in this project
##Created by Alex Hewson
##Last updated 19 July 2024

import plotly.io as pio
import plotly.graph_objs as go
import pandas as pd
import textwrap
from typing import Optional, Literal

#PRT standard template
pio.templates["prt_template"] = go.layout.Template(
    layout=go.Layout(
        title_font=dict(family="Helvetica Neue, Arial", size=20),
        title_y=0.94,
        title_yanchor="bottom",
        font_color="#54565B",
        font_family="Helvetica Neue, Arial",
        font_size=14,
        paper_bgcolor="rgba(1,1,1,0)",
        plot_bgcolor="rgba(1,1,1,0)",
        colorway=("#A01D28", "#499CC9", "#F9A237", "#6FBA3A", "#573D6B"),
        modebar_activecolor="#A01D28",
        showlegend=False,
        xaxis_showgrid=False,
        xaxis_tickcolor="#54565B",
        width=700,
        height=500,
    )
)
pio.templates["prt_template"].data.scatter = [
    go.Scatter(
        line_width=4,
        marker_size=10
        )
        ]

## Chart annotations
def add_annotation(
    annotations_list,
    text=None,
    x=None,
    y=None,
    xref="paper",
    yref="paper",
    xanchor="left",
    yanchor="top",
    align=None,
    showarrow=False,
    font_size=14,
    font_color=None,
    annotation_type=None,
    dataframe=None,
    dataframe_column=None,
    trace_list=None
):
    annotation_types = {"source", "y-axis", "trace_label", "label"}

    if annotation_type not in annotation_types:
        raise ValueError(f"You must supply a valid annotation_type from {annotation_types}")

    if annotation_type == "source":
        if text is None:
            raise ValueError("Text must be provided for source annotation.")
        text = f"Source: {text}"
        font_size = 12
        align = "left"
        x = 0 if x is None else x
        y = -0.1 if y is None else y

    elif annotation_type == "y-axis":
        if dataframe is not None and dataframe_column is not None:
            x = dataframe[dataframe_column].iloc[0]
            xref = "x"
        else:
            x = 0 if x is None else x
        y = 1 if y is None else y
        yanchor="bottom"

    elif annotation_type == "trace_label":
        if trace_list is not None:
            for j, trace in enumerate(trace_list):
                x = trace.x[-1]
                y = trace.y[-1]
                text = str(trace.name)
                font_color = pio.templates['prt_template'].layout.colorway[j]
                
                annotations_list.append(
                    dict(
                        xref="x",
                        yref="y",
                        xanchor=xanchor,
                        yanchor=yanchor,
                        x=x,
                        y=y,
                        align=align,
                        showarrow=showarrow,
                        text=text,
                        font_size=font_size,
                        font_color=font_color
                    )
                )
            return
        else:
            raise ValueError("You must supply a valid trace_list")
    
    elif annotation_type == "label":
        if text is None:
            raise ValueError("Text must be provided.")
        # font_size = 12
        align = "center"
        x = 0.5 if x is None else x
        y = 0.5 if y is None else y

    # Append the annotation for other types or source/y-axis annotations
    annotations_list.append(
        dict(
            xref=xref,
            yref=yref,
            xanchor=xanchor,
            yanchor=yanchor,
            x=x,
            y=y,
            align=align,
            showarrow=showarrow,
            text=text,
            font_size=font_size,
            font_color=font_color
        )
    )

def add_title(
        fig, 
        title, 
        width=80,
        bold=True):
    
    title = textwrap.wrap(f"{title}", width=width)
    font_size = "1.5rem"
    title.append("</span>")
    
    if bold:
        span_start = f"<span style='font-size:{font_size};font-weight:bold'>"
    else:
        span_start = f"<span style='font-size:{font_size}>"
    
    title = span_start + "<br>".join(title)

    fig.update_layout(
        title=title,
        title_automargin=True,
        title_yref='container',
        title_xanchor='left',
        title_x=0)
    
def set_axis_range(
    fig: go.Figure,
    axis: Literal["x", "y"],
    dataframe: Optional[pd.DataFrame] = None,
    dataframe_column: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> None:
    """
    Sets the axis range manually or based on a dataframe's column.

    Parameters
    ----------
    fig : go.Figure
        Target Plotly figure.

    axis : Literal["x", "y"]
        Axis to apply the range transformation ('x' or 'y').

    dataframe : pd.DataFrame, optional
        DataFrame for automatic calculation of min and/or max value if not provided.

    dataframe_column : str, optional
        Column in the DataFrame to calculate the axis range from.

    min_value : float, optional
        Minimum value for the axis range. Automatically calculated if not provided.

    max_value : float, optional
        Maximum value for the axis range. Automatically calculated if not provided.

    Raises
    ------
    ValueError
        If `min_value` or `max_value` is not provided and `dataframe` or `dataframe_column` is missing.
    """

    axis_update_funcs = {
        "x": fig.update_xaxes,
        "y": fig.update_yaxes
    }

    if min_value is None or max_value is None:
        if dataframe is None or dataframe_column is None:
            raise ValueError("Both dataframe and dataframe_column must be provided if min_value or max_value is None.")
        
        padding = (dataframe[dataframe_column].max() - dataframe[dataframe_column].min()) / len(dataframe[dataframe_column])
        min_value = dataframe[dataframe_column].min() - padding if min_value is None else min_value
        max_value = dataframe[dataframe_column].max() + padding if max_value is None else max_value

    if axis in axis_update_funcs:
        axis_update_funcs[axis](range=[min_value, max_value])