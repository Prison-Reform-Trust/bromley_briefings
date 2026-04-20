#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module of shared functions for the sentences explained charts"""

from typing import Any, Dict, List, Optional

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


def prepare_annotations(annotation_configs: List[Dict[str, Any]]) -> list:
    """
    Prepares annotations to be added to the figure.

    Parameters:
        annotation_configs (list of dict):
            Each dict is passed as keyword arguments to
            `prt_theme.add_annotation()`. Supported keys are the same as
            `add_annotation`, except `annotations_list` is handled internally.
            Example keys include:
                - text
                - x
                - y
                - xref
                - yref
                - xanchor
                - yanchor
                - align
                - showarrow
                - font_size
                - font_color
                - annotation_type
                - dataframe
                - dataframe_column
                - trace_list
                - trace_list_idx
                - x_pad

            Defaults applied by this wrapper when keys are missing:
                - annotation_type="label"
                - xref="x"
                - y=0

    Returns:
        list: List of prepared annotation dicts.
    """
    annotations = []
    for config in annotation_configs:
        params = config.copy()
        params.setdefault("annotation_type", "label")
        params.setdefault("xref", "x")
        params.setdefault("y", 0)
        params.setdefault("font_size", 12)
        prt_theme.add_annotation(annotations_list=annotations, **params)
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
