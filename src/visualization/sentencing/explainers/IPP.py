#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D

#Read in datasets.
data = pd.read_csv("data/processed/sentence_explainers/IPP.csv")

#Set style.
plt.style.use('src/visualization/prt_style.mplstyle')

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
ax.text(4.55, 0.02,"Term set\nby judge", color='white', ha='center', va='center', size=9, zorder=5)
ax.text(9.1, 1.05,"Conditional release", ha='center', va='center', size=7, zorder=4)
ax.text(50, -1.2,"Based on a custodial tariff of 4 years (the average tariff of the remaining unreleased people serving IPP in prison)\nand an assumption of living for 40 years after release", ha='center', va='center', size=10, zorder=5)
ax.text(31.8, 1.05,"Licence review", ha='center', va='center', size=7, zorder=4)
ax.text(100, 1.05,"End of life", ha='center', va='center', size=7, zorder=4)

#Add line. The first coords are x and the second y, for line beginning/end. 

#Release
ax.add_artist(Line2D((9.1, 9.1), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

#Licence review
ax.add_artist(Line2D((31.8, 31.8), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

#End of life
ax.add_artist(Line2D((100, 100), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

###PRINTING FIGURE###
plt.savefig("reports/figures/sentencing/explainers/IPP.svg", bbox_inches='tight', transparent=True)