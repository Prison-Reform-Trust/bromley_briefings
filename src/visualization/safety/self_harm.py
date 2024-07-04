#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

#Read in datasets.
data = pd.read_csv("data/processed/safety/self_harm.csv")
#Filtering for every other year
data = data[::2]

#Set style.
plt.style.use('src/visualization/prt_style.mplstyle')

###MAKING FIGURE###

#Set figure parameters. Remove figsize unless different to that on style sheet. 
fig, ax = plt.subplots(figsize=(3.9,3.0))
ax.grid(visible=False)
ax.invert_yaxis()

#Single category horizontal barplot
index = np.arange(len(data.year))
values = data.rate
incidents = data.incidents
labels = data.year

bars = ax.barh(index, values, height=0.8)
ax.set_yticks(index, labels=labels)

###ADDING LABELLING####

#Title.
#ax.set_title("Rates of self-harm\nremain at historic highs")

#Data source.
plt.figtext(0.03, -0.1, "Source: Table 2.1, Ministry of Justice (2024). Safety in custody:\nQuarterly update to December 2023.", ha="left", fontsize=7, bbox={"alpha":0, "pad":5})

#Axis labels. 
ax.set_xlabel("Self-harm incidents per 1,000 prisoners")
ax.set_ylabel(None)

#Tick labels. Give blank list to remove.
ax.set_xticklabels([])

#Additional text.
#Rates.
ax.bar_label(bars, padding=5)

#Incidents.
ax.bar_label(bars, labels=[f'{x:,.0f} incidents' for x in incidents],label_type='center', color='white')

###PRINTING FIGURE###
plt.savefig("reports/figures/safety/self_harm.svg", bbox_inches='tight', transparent=True)