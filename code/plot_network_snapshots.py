"""Six matched illustrative buyer-supplier trade matrices (seed 0); supplemental only.
No claim of representativeness: each panel is a single saved simulation state.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'results';OUT=ROOT/'figures'
z=np.load(RES/'adaptive_snapshots_seed0.npz')
scenarios=[('H_adaptive','Human–LLM kernel'),('A_adaptive','LLM–LLM kernel')];steps=[39,48,70]
cm=LinearSegmentedColormap.from_list('trades',['#FFFFFF','#DBDBDB','#969696','#242424'])
mx=max(float(np.max(z[f'{sc}_trade_t{t}'])) for sc,_ in scenarios for t in steps)
fig,axs=plt.subplots(2,3,figsize=(6.65,3.52),dpi=180,sharex=True,sharey=True)
fig.subplots_adjust(left=.14,right=.88,bottom=.10,top=.86,wspace=.06,hspace=.22)
for i,(sc,label) in enumerate(scenarios):
 for j,t in enumerate(steps):
  a=axs[i,j];mat=z[f'{sc}_trade_t{t}'];im=a.imshow(mat,aspect='auto',origin='lower',cmap=cm,vmin=0,vmax=mx,interpolation='nearest')
  a.set_title(f'{"Pre-shock" if t==39 else "Shock" if t==48 else "Recovery"} (t={t})',fontsize=9.5)
  a.set_xticks([0,3,7,11]);a.set_yticks([0,5,11,17,23]);a.tick_params(labelsize=8,length=2)
 axs[i,0].set_ylabel(label+'\nBuyer index',fontsize=9)
for a in axs[-1,:]:a.set_xlabel('Supplier index',fontsize=9)
cbar=fig.colorbar(im,ax=axs.ravel().tolist(),fraction=.023,pad=.023);cbar.ax.tick_params(labelsize=8);cbar.set_label('Delivered units',fontsize=9)
fig.text(.5,.965,'One matched seed: illustrative trade matrices, not estimated real networks',ha='center',va='top',fontsize=9.5,color='#222222')
for ext in ('pdf','svg','png'):fig.savefig(OUT/f'fig07_network_snapshots.{ext}',dpi=600,bbox_inches='tight',pad_inches=.05)
plt.close(fig)
