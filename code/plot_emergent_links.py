"""Publication figures for network emergence from independently replayed ABM edge logs.

Uses results from analyze_emergent_links.py. Schematics are not generated with
image models. Every plotted value is computed from 80 saved matched seed runs.
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'; OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
DARK='#111111'; MID='#747474'; LIGHT='#DADADA'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.7,'axes.titlesize':9.3,
 'axes.labelsize':8.7,'xtick.labelsize':8.1,'ytick.labelsize':8.1,'axes.linewidth':.7,
 'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
 'savefig.facecolor':'white'})


def stylize(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(direction='out',length=2.5,width=.6)
    ax.grid(axis='y',color='#E5E5E5',lw=.50)
    ax.set_axisbelow(True)


def bootstrap(xs, seed=43, n=700):
    """Pointwise mean + 95% bootstrap interval over independent simulation seeds."""
    xs=np.asarray(xs,dtype=float)
    rng=np.random.default_rng(seed)
    idx=rng.integers(0,xs.shape[0],size=(n,xs.shape[0]))
    draw=xs[idx].mean(axis=1)
    return xs.mean(axis=0),np.quantile(draw,.025,axis=0),np.quantile(draw,.975,axis=0)


def moving(x,k=5):
    return pd.DataFrame(x.T).rolling(k,center=True,min_periods=1).mean().to_numpy().T


def save(fig,name):
    for ext in ('pdf','svg','png'):
        fig.savefig(OUT/f'{name}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.035)
    plt.close(fig)


def flow_rewiring():
    d=pd.read_csv(RES/'emergent_link_trajectories.csv')
    figs,axs=plt.subplots(1,2,figsize=(4.79,2.35))
    figs.subplots_adjust(left=.106,right=.992,bottom=.21,top=.77,wspace=.31)
    specs=[('supplier_tv','(a) Supplier flow reallocation','Supplier-share distance'),
           ('active_edge_novelty','(b) Links outside baseline','Share of active links')]
    for ax,(col,ttl,ylab) in zip(axs,specs):
        stylize(ax);ax.set_title(ttl,pad=7)
        for scenario,color,style in [('H_adaptive',DARK,'-'),('A_adaptive',MID,'--')]:
            pivot=d[d.scenario==scenario].pivot(index='seed',columns='t',values=col).sort_index().sort_index(axis=1)
            t=pivot.columns.values
            vals=moving(pivot.to_numpy(float),5)
            center,lo,hi=bootstrap(vals,seed=51 if scenario.startswith('H') else 57)
            ax.fill_between(t,lo,hi,color=color,alpha=.11,lw=0,zorder=2)
            ax.plot(t,center,color=color,linestyle=style,lw=1.5,zorder=3)
        ax.axvspan(40,54.5,color=LIGHT,alpha=.38,zorder=0)
        ax.axvline(40,color='#999999',ls=':',lw=.7)
        ax.axvline(54.5,color='#999999',ls=':',lw=.7)
        ax.set_xlim(30,99);ax.set_xticks([30,40,55,70,85,99]);ax.set_xlabel('Simulation period')
        ax.set_ylabel(ylab,labelpad=4)
        if col=='supplier_tv':ax.set_ylim(.035,.30);ax.set_yticks([.05,.10,.15,.20,.25,.30])
        else:ax.set_ylim(0,.23);ax.set_yticks([0,.05,.10,.15,.20])
    handles=[Line2D([0],[0],color=DARK,lw=1.6,ls='-',label='Human–LLM kernel'),
             Line2D([0],[0],color=MID,lw=1.6,ls='--',label='LLM–LLM kernel')]
    figs.legend(handles=handles,loc='upper center',bbox_to_anchor=(.54,.975),ncol=2,
                fontsize=8.5,frameon=False,handlelength=2.8,columnspacing=1.2)
    save(figs,'fig08_emergent_rewiring')


def shock_link_persistence():
    data=pd.read_csv(RES/'emergent_link_cohorts.csv')
    ph=pd.read_csv(RES/'emergent_link_phase_metrics.csv')
    fig,(a,b)=plt.subplots(1,2,figsize=(4.79,2.37))
    fig.subplots_adjust(left=.103,right=.985,bottom=.24,top=.77,wspace=.33)
    for ax in (a,b):stylize(ax)
    a.set_title('(a) Reuse of shock-only links',pad=7)
    for scenario,color,style in [('H_adaptive',DARK,'-'),('A_adaptive',MID,'--')]:
        p=data[data.scenario==scenario].pivot(index='seed',columns='post_periods',values='cumulative_reappearance').sort_index().sort_index(axis=1)
        t=p.columns.values; c,lo,hi=bootstrap(p.to_numpy(float),seed=100 if scenario.startswith('H') else 101)
        a.fill_between(t,lo,hi,color=color,alpha=.12,lw=0)
        a.plot(t,c,color=color,ls=style,lw=1.5)
    a.set_xlabel('Periods after capacity restoration');a.set_ylabel('Share reactivated')
    a.set_xlim(1,30);a.set_ylim(0,.80);a.set_xticks([1,5,10,15,20,25,30]);a.set_yticks([0,.2,.4,.6,.8])
    b.set_title('(b) Flow on shock-only links',pad=7)
    phases=['early_recovery','late_recovery'];names=['55–69','70–99']
    xs=[.79,1.17,2.35,2.73]
    scenario_order=['H_adaptive','A_adaptive']
    arrays=[];boxes=[]
    for idx,phase in enumerate(phases):
        for k,sc in enumerate(scenario_order):
            x=ph[(ph.phase==phase)&(ph.scenario==sc)].flow_on_shock_new.to_numpy()*100
            arrays.append(x)
            boxes.append((idx,k))
    bp=b.boxplot(arrays,positions=xs,widths=.27,patch_artist=True,showfliers=False,
                 medianprops={'color':'black','linewidth':1.0},
                 whiskerprops={'color':'#555555','linewidth':.8},
                 capprops={'color':'#555555','linewidth':.8},
                 boxprops={'linewidth':.9,'edgecolor':'#333333'})
    for patch,(idx,k) in zip(bp['boxes'],boxes):
        patch.set_facecolor('#D3D3D3' if k==0 else '#FFFFFF')
        if k==1:patch.set_hatch('///')
    b.set_xticks([.98,2.54]);b.set_xticklabels(names);b.set_xlim(.5,3.05)
    b.set_xlabel('Recovery periods');b.set_ylabel('Delivered volume (%)')
    b.set_ylim(0,26);b.set_yticks([0,5,10,15,20,25])
    for x,vals in zip(xs,arrays):
        b.plot(x,np.mean(vals),marker='o',ms=2.9,mec='black',mew=.5,mfc='black',zorder=5)
    handles=[Line2D([0],[0],color=DARK,lw=1.6,label='Human–LLM kernel'),
             Line2D([0],[0],color=MID,lw=1.6,ls='--',label='LLM–LLM kernel')]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.54,.973),ncol=2,
               fontsize=8.5,frameon=False,handlelength=2.8,columnspacing=1.2)
    save(fig,'fig09_shock_link_reuse')

if __name__=='__main__':
    flow_rewiring()
    shock_link_persistence()
    print('Exported emergent figures (PDF, SVG, 600-DPI PNG).')
