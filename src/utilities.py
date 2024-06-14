#!/usr/bin/env python
"""
This script provides useful functions to all other scripts
"""
import yaml
import os
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path # type: ignore


def read_config():
    # Read in config file
    config = {k: v for d in yaml.load(
        open('config.yml'),
            Loader=yaml.SafeLoader) for k, v in d.items()}
    return config