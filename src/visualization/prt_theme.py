#Custom Plotly template for all charts in this project
##Created by Alex Hewson
##Last updated 3 July 2024

import plotly.io as pio
import plotly.graph_objs as go
import textwrap

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
    annotation_type="custom",
    dataframe=None,
    dataframe_column=None,
    trace_list=None
):
    if annotation_type == "source":
        if text is None:
            raise ValueError("Text must be provided for source annotation.")
        text = f"Source: {text}"
        font_size = 12
        align = "left"
        x = 0 if x is None else x
        y = -0.1 if y is None else y
    elif annotation_type == "y-axis":
        # Set x to the first value of the specified dataframe column if provided
        if dataframe is not None and dataframe_column is not None:
            x = dataframe[dataframe_column].iloc[0]
            xref = "x"
        else:
            x = 0 if x is None else x
        y = 1.1 if y is None else y
    elif annotation_type == "trace_label":
        if trace_list is not None:
            for j in range(len(trace_list)):
                trace = trace_list[j]
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
            return  # Return early since we are appending multiple annotations
        else:
            raise ValueError("You must supply a valid trace_list")

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
        width=60,
        bold=True):
    
    if bold:
        title = textwrap.wrap(f'<b>{title}</b>', width=width)
    else:
        title = textwrap.wrap(f'{title}', width=width)
    fig.update_layout(
        title="<br>".join(title),
        title_automargin=True)