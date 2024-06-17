#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import packages.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Read in datasets.
data = pd.read_csv("data/processed/sentence_explainers/Legend.csv")

#Set style.
plt.style.use('src/visualization/prt_style.mplstyle')

###MAKING FIGURE###

#Set figure parameters. Remove figsize unless different to that on style sheet. 
fig, ax = plt.subplots(figsize=(9,0.7))

p1 = sns.barplot(x=data.suspended, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#F9A237",
            zorder=7)

p2 = sns.barplot(x=data.custodial, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#A01D28",
            zorder=6)

p3 = sns.barplot(x=data.conditional, 
            y=data.sentence,
            data=data,
            orient='h',
            color="gray",
            zorder=5)

p4 = sns.barplot(x=data.licence, 
            y=data.sentence,
            data=data,
            orient='h',
            color="#499CC9",
            zorder=4)

p5= sns.barplot(x=data.supervision, 
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
ax.text(10, 0.02,"Suspended\nsentence", color='white', ha='center', va='center', size=10, zorder=7)
ax.text(30, 0.02,"Custodial period\nof sentence", color='white', ha='center', va='center', size=10, zorder=7)
ax.text(50, 0.02,"Period of sentence\non licence following\nconditional release", color='white', ha='center', va='center', size=8, zorder=7)
ax.text(70, 0.02,"Period of sentence\non licence following\nautomatic release", color='white', ha='center', va='center', size=8, zorder=7)
ax.text(90, 0.02,"Period of\npost-sentence\nsupervision", color='white', ha='center', va='center', size=8, zorder=7)
ax.text(50, -0.8,"Legend", ha='center', va='center', size=10, zorder=5)

###PRINTING FIGURE###
plt.savefig("reports/figures/sentencing/explainers/legend.svg", bbox_inches='tight', transparent=True)