"""Redraw exact SST-2 values from Radford et al. (2018), Table 5, PDF p. 8.
Source: https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
No digitization, interpolation, or new experiment. Full model includes auxiliary LM.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17, 'text.color':'#17364a','axes.labelcolor':'#17364a','xtick.color':'#17364a','ytick.color':'#17364a','svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(6.4,4.4),layout='constrained',facecolor='#fbfaf6')
ax.set_facecolor('#fbfaf6')
bars=ax.bar(['No\npretraining','Full pretrained\nmodel'],[84.0,91.3],color=['#8b9da4','#0f7881'],width=.55)
ax.bar_label(bars,labels=['84.0','91.3'],padding=5,fontsize=23)
ax.set_ylim(0,103);ax.set_yticks([0,25,50,75,100]);ax.set_ylabel('SST-2 accuracy (%)');ax.set_title('Sentiment after task training',fontsize=19,pad=18)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.savefig(Path(__file__).resolve().parents[1]/'images/gpt-pretraining-ablation.svg')
