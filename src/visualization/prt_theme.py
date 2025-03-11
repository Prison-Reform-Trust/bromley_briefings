#Custom Plotly template for all charts in this project
##Created by Alex Hewson
##Last updated 11 March 2025

import plotly.io as pio
import plotly.graph_objs as go
import pandas as pd
import textwrap
from typing import Optional, Literal, Union, List

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
        xaxis_ticks='inside',
        xaxis_tickcolor="#54565B",
        width=700,
        height=500,
        margin=dict(t=20, b=25, l=0, r=25, pad=5),
        dragmode=False,
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
    annotations_list=None,  # Default to None, so we can initialize if needed
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
    trace_list=None,
    trace_list_idx: Union[None, int, List[int]] = None,
    x_pad=0
):
    """
    Add an annotation to a Plotly chart.

    Parameters:
    ----------
    annotations_list : list, optional
        A list to which the annotation dictionary will be appended. If not provided, a new list is created.
    
    text : str, optional
        The text to display in the annotation. Required for "source" and "label" annotation types.
    
    x : float or list of floats, optional
        The x-coordinate(s) for the annotation(s). If not specified, defaults are used based on `annotation_type`.
    
    y : float or list of floats, optional
        The y-coordinate(s) for the annotation(s). If not specified, defaults are used based on `annotation_type`.
    
    xref : str, default="paper"
        The reference for the x-coordinate. Can be "paper" (relative to the plot area) or "x" (data coordinates).
    
    yref : str, default="paper"
        The reference for the y-coordinate. Can be "paper" (relative to the plot area) or "y" (data coordinates).
    
    xanchor : str, default="left"
        The horizontal alignment of the annotation. Options include "left", "center", and "right".
    
    yanchor : str, default="top"
        The vertical alignment of the annotation. Options include "top", "middle", and "bottom".
    
    align : str, optional
        The alignment of the text within the annotation box. Options include "left", "center", and "right".
    
    showarrow : bool, default=False
        Whether to display an arrow pointing to the annotation's coordinates.
    
    font_size : int, default=14
        The font size of the annotation text.
    
    font_color : str, optional
        The color of the annotation text. If not specified, a default color is used.
    
    annotation_type : str, required
        The type of annotation. Must be one of:
        - "source": Adds a source label to the chart.
        - "y-axis": Adds a label near the y-axis.
        - "trace_label": Adds annotations to specific traces.
        - "label": Adds a generic label annotation.
    
    dataframe : pandas.DataFrame, optional
        A DataFrame to extract values for certain annotations (e.g., "y-axis").
    
    dataframe_column : str, optional
        The column in `dataframe` to use for the annotation's x-coordinate (used with "y-axis" type).
    
    trace_list : list, optional
        A list of Plotly traces to annotate (used with "trace_label" type).
    
    trace_list_idx : int or list of ints, optional
        The indices of traces in `trace_list` to annotate. If not provided, all traces are annotated.
    
    x_pad : float, default=0
        An optional padding to apply to the x-coordinate of the annotation(s). Useful for adjusting placement.
    
    Raises:
    -------
    ValueError
        If `annotation_type` is not one of the predefined types.
        If required arguments (e.g., `text`, `trace_list`) are missing for certain annotation types.

    """
    # Ensure annotations_list is initialized
    if annotations_list is None:
        annotations_list = []

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
        yanchor = "bottom"

    elif annotation_type == "trace_label":
        if trace_list is not None:
            if trace_list_idx is None:
                trace_list_idx = list(range(len(trace_list)))
            elif isinstance(trace_list_idx, int):
                trace_list_idx = [trace_list_idx]

            x_map = {trace_list_idx[i]: x[i] for i in range(len(trace_list_idx))} if isinstance(x, list) else {}
            y_map = {trace_list_idx[i]: y[i] for i in range(len(trace_list_idx))} if isinstance(y, list) else {}

            for j, trace in enumerate(trace_list):
                x_override = x_map.get(j, trace.x[-1]) + x_pad
                y_override = y_map.get(j, trace.y[-1])

                annotations_list.append(
                    dict(
                        xref="x",
                        yref="y",
                        xanchor=xanchor,
                        yanchor=yanchor,
                        x=x_override,
                        y=y_override,
                        align=align,
                        showarrow=showarrow,
                        text=str(trace.name),
                        font_size=font_size,
                        font_color=pio.templates['prt_template'].layout.colorway[j]
                    )
                )
        else:
            raise ValueError("You must supply a valid trace_list")

    elif annotation_type == "label":
        if text is None:
            raise ValueError("Text must be provided.")
        align = "center"
        x = 0.5 if x is None else x
        y = 0.5 if y is None else y

    if x is not None:
        x += x_pad

    if annotation_type != "trace_label":
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

    return annotations_list


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

def wrap_labels(text, max_chars=20):
    """
    Wraps text with specified max characters per line and replaces newlines with <br>.

    Args:
        text (str): The text to wrap.
        max_chars (int): The maximum number of characters per line.

    Returns:
        str: Text with wrapped lines and <br> instead of newline characters.
    """
    # Wrap the text with textwrap and replace newlines with <br>
    return textwrap.fill(text, width=max_chars).replace('\n', '<br>')

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