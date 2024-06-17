#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Read in datasets.
data = pd.read_csv("data/processed/sentence_explainers/Community.csv")

#Set style.
plt.style.use('src/visualization/prt_style.mplstyle')

###MAKING FIGURE###

#Set figure parameters. Remove figsize unless different to that on style sheet. 
fig, ax = plt.subplots(figsize=(9,0.7))

p1 = sns.barplot(x=data.licence, 
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
ax.text(50, 0.02,"Can be sanctioned for failing to comply", color='white', ha='center', va='center', size=10, zorder=5)

###PRINTING FIGURE###
plt.savefig("reports/figures/sentencing/explainers/community.svg", bbox_inches='tight', transparent=True)