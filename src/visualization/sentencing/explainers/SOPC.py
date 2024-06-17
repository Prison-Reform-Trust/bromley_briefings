#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D

#Read in datasets.
data = pd.read_csv("data/processed/sentence_explainers/SOPC.csv")

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
            zorder=5)

p2 = sns.barplot(x=data.conditional, 
            y=data.sentence,
            data=data,
            orient='h',
            color="gray",
            zorder=4)

p3 = sns.barplot(x=data.supervision, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#573D6B",
            zorder=3)

#Axis labels. 
ax.set_xlabel(None)
ax.set_ylabel(None)

#Tick labels.
ax.set_yticklabels([])
ax.set_xticklabels([])

#Add text

#Release point
ax.text(59.5, 0.02,"66% of\n custodial term", color='white', ha='right', va='center', size=10, zorder=5)
ax.text(60.5, 1.05,"Conditional release", ha='center', va='center', size=7, zorder=4)
ax.text(90.8, 1.05,"100% of\ncustodial term", ha='center', va='center', size=7, zorder=4)
ax.text(95.45, 0.02,"1 year", color='white', ha='center', va='center', size=10, zorder=5)
ax.text(50, -1.2,"Based on a custodial term of 10 years (the average term of a SOPC in 2023)", ha='center', va='center', size=10, zorder=5)

#Add line. The first coords are x and the second y, for line beginning/end. 

#Automatic release
ax.add_artist(Line2D((60.5, 60.5), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

#100% of term
ax.add_artist(Line2D((90.8, 90.8), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

###PRINTING FIGURE###
plt.savefig("reports/figures/sentencing/explainers/SOPC.svg", bbox_inches='tight', transparent=True)