#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D

#Read in datasets.
data = pd.read_csv("data/processed/sentence_explainers/STS.csv")

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

p3 = sns.barplot(x=data.licence, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#499CC9",
            zorder=3)

#Axis labels. 
ax.set_xlabel(None)
ax.set_ylabel(None)

#Tick labels.
ax.set_yticklabels([])
ax.set_xticklabels([])

#Add text

#Release point
ax.text(45.7, 0.02,"100% of\n custodial term", color='white', ha='right', va='center', size=10, zorder=5)
ax.text(46.7, 1.05,"Automatic release", ha='center', va='center', size=7, zorder=4)
ax.text(73.35, 0.02,"Between 7 and 25 years", color='white', ha='center', va='center', size=10, zorder=5)
ax.text(50, -1.2,"Based on a custodial term of 14 years (the set period)\nand an extended licence period of 16 years", ha='center', va='center', size=10, zorder=5)

#Add line. The first coords are x and the second y, for line beginning/end. 

#Automatic release
ax.add_artist(Line2D((46.7, 46.7), (-0.8, 0.8), color='black', linewidth=1, linestyle='dotted', clip_on=False, zorder=8))

###PRINTING FIGURE###
plt.savefig("reports/figures/sentencing/explainers/STS.svg", bbox_inches='tight', transparent=True)