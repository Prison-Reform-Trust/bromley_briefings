#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import matplotlib.ticker as mtick

#Set working directory.
os.chdir("/Users/Sophie/OneDrive - Prison Reform Trust/Policy and Communications/Factfile/Winter 2024/Python Scripts")

#Read in datasets.
data = pd.read_csv("Data/Sentence explainers/Life.csv")

#Set style.
plt.style.use('prt_style.mplstyle')

###MAKING FIGURE###

#Set figure parameters. Remove figsize unless different to that on style sheet. 
fig, ax = plt.subplots(figsize=(9,0.7))

p1 = sns.barplot(x=data.custodial, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#A01D28",
            zorder=4)

p2 = sns.barplot(x=data.conditional, 
            y=data.sentence,
            data=data,
            orient='h',
            color="gray",
            zorder=3)

#Axis labels. 
ax.set_xlabel(None)
ax.set_ylabel(None)

#Tick labels.
ax.set_yticklabels([])
ax.set_xticklabels([])

#Add text

#Release point
ax.text(20.6, 0.02,"Term set\nby judge", color='white', ha='center', va='center', size=9, zorder=5)
ax.text(41.2, 1.05,"Conditional release", ha='center', va='center', size=7, zorder=4)
ax.text(50, -1.2,"Based on a custodial tariff of 21 years (the average tariff imposed in 2021\nand an assumption of living for 30 years after release", ha='center', va='center', size=10, zorder=5)
ax.text(100, 1.05,"End of life", ha='center', va='center', size=7, zorder=4)

#Add line. The first coords are x and the second y, for line beginning/end. 

#Release
ax.add_artist(Line2D((41.2, 41.2), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

#End of life
ax.add_artist(Line2D((100, 100), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

###PRINTING FIGURE###
plt.savefig("/Users/Sophie/OneDrive - Prison Reform Trust/Policy and Communications/Factfile/Winter 2024/InDesign Documents/Charts/Sentence explainers/Life.pdf", dpi=600, bbox_inches='tight', transparent=True)