#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module of shared functions for the sentences explained charts"""

from typing import Dict, List, Optional

import plotly.graph_objs as go

from src.visualization import prt_theme


def prepare_line_shapes(line_positions: List) -> List[Dict]:
    """
    Prepares vertical line shapes to be added to the figure.

    Parameters:
        line_positions (list): List of x positions for the vertical lines.

    Returns:
        list: List of prepared line shape dicts.
    """
    return [
        {
            "type": "line",
            "x0": pos, "y0": 0, "x1": pos, "y1": 1,
            "xref": "x", "yref": "paper",
            "line": {
                "color": "rgba(255, 255, 255, 0.6)" if pos != line_positions[-1] else "white",
                "width": 2,
                "dash": "dot"
            }
        }
        for pos in line_positions
    ]


def prepare_annotations(annotation_configs: List[Dict]) -> list:
    """
    Prepares annotations to be added to the figure.

    Parameters:
        annotation_configs (list of dict): Each dict should contain keys:
            - "text" (str): The annotation text.
            - "x" (float or int): The x position for the annotation.
            - "xanchor" (str): The x anchor for the annotation.
            - "font_size" (int, optional): Font size for the annotation (default is 12).

    Returns:
        list: List of prepared annotation dicts.
    """
    annotations = []
    for config in annotation_configs:
        prt_theme.add_annotation(
            annotations_list=annotations,
            text=config["text"],
            annotation_type="label",
            x=config["x"],
            xref="x",
            y=0,
            xanchor=config["xanchor"],
            font_size=config.get("font_size", 12)  # Default font size
        )

    return annotations


def apply_layout_updates(
        fig: go.Figure,
        shapes: Optional[list] = None,
        annotations: Optional[list] = None
        ) -> go.Figure:
    """Applies all layout updates to the figure."""
    update_dict = {}
    if shapes:
        update_dict["shapes"] = shapes
    if annotations:
        update_dict["annotations"] = annotations
    if update_dict:
        fig.update_layout(**update_dict)
    return fig
