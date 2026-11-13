"""Reproducible Matplotlib figures for Relational Decisions in Agentic Supply Networks.

All conceptual layouts and connectors are specified in Python; no generative-image
assets are used. Charts read the recorded GLEE extracts and simulation CSVs.
Save lossless 600 dpi PNGs + vector PDF/SVG for typesetting.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D
from statsmodels.stats.proportion import proportion_confint
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'figures'; RES=ROOT/'results'; DATA=ROOT/'data'; OUT.mkdir(exist_ok=True)
# Restrained academic colors: ink, slate, stone, and muted pine. No gradients or decorative shadows.
INK='#141414'; SLATE='#111111'; PINE='#858585'; RUST='#777777'; MID='#666666'; GRID='#dddddd'; PALE='#f4f4f4'; PALE_B='#f4f4f4'; PALE_G='#eeeeee'; PALE_R='#eeeeee'; WHITE='#FFFFFF'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':11,'axes.labelsize':10,'xtick.labelsize':9.5,'ytick.labelsize':9.5,
 'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'lines.solid_capstyle':'round',
 'savefig.facecolor':'white','axes.edgecolor':MID})

def figax(w=6.65,h=3.05):
 fig=plt.figure(figsize=(w,h),dpi=180,facecolor='white');ax=fig.add_axes([.018,.02,.964,.96]);ax.set(xlim=(0,100),ylim=(0,100));ax.axis('off');return fig,ax

def text(ax,x,y,word,fs=10,weight='normal',color=INK,ha='center',va='center',**k):
 return ax.text(x,y,word,fontsize=fs,fontweight=weight,color=color,ha=ha,va=va,linespacing=1.22,**k)

def card(ax,x,y,w,h,fill=WHITE,stroke=GRID,lw=.9,r=.9):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.0,rounding_size={r}',fc=fill,ec=stroke,lw=lw,joinstyle='miter');ax.add_patch(p);return p

def arrow(ax,start,end,color=SLATE,lw=1.15,scale=10):
 a=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=scale,lw=lw,color=color,shrinkA=0,shrinkB=0,joinstyle='miter',capstyle='butt',zorder=10);ax.add_patch(a)

def ortho(ax,points,color=SLATE,lw=1.05,scale=9):
 # deterministic straight orthogonal connector; the last segment receives the arrowhead
 for p,q in zip(points[:-2],points[1:-1]):ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=lw,zorder=8,solid_capstyle='butt')
 arrow(ax,points[-2],points[-1],color,lw,scale)

def save(fig,key):
 for ext in ['pdf','svg','png']:
  fig.savefig(OUT/f'{key}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.035)
 plt.close(fig)

def div(ax,x1,x2,y,color=GRID):ax.plot([x1,x2],[y,y],color=color,lw=.85)

# F1: controlled conceptual comparison; identical exogenous structure, human/agent decision authority.
def problem():
 fig,ax=figax(6.65,2.90)
 card(ax,2,88,96,10,PALE,GRID,.8)
 text(ax,50,93,'SHARED STRUCTURED DECISIONS   Demand   ·   capacity   ·   sourcing rules',10,weight='semibold')
 edges=[(0,0),(0,1),(1,0),(1,2),(2,1),(2,2),(3,0),(3,2)]
 for base,name,color,bg in [(2.5,'HUMAN DECISION AUTHORITY',SLATE,PALE_B),(51,'LLM AGENT DECISION AUTHORITY',PINE,PALE_G)]:
  card(ax,base,22,46.5,61,WHITE,GRID,.85,1)
  text(ax,base+23.25,77,name,10.4,'bold',color)
  div(ax,base+2,base+44.5,72)
  bx=base+10.3; sx=base+35.4
  by=[61,52,43,34];sy=[61,47.5,34]
  for i,j in edges:
   ax.plot([bx+2.1,sx-2.2],[by[i],sy[j]],c='#A8B4B7',lw=1.05,zorder=1)
  for yi in by:
   ax.add_patch(Circle((bx,yi),2.22,fc=bg,ec=color,lw=1.1,zorder=3))
  for k,yi in enumerate(sy):
   ax.add_patch(Rectangle((sx-2.25,yi-2.25),4.5,4.5,fc=PALE_R if k==1 else bg,ec=RUST if k==1 else color,lw=1.15,zorder=3))
  text(ax,bx,67.2,'Buyers',9,color=color);text(ax,sx,67.2,'Suppliers',9,color=color)
  text(ax,base+23.25,27.0,'Trading links evolve with negotiation',8.6,color=MID)
 # legend below panels, no overlap with network
 ax.add_patch(Circle((6,12.7),1.65,fc=PALE_B,ec=SLATE,lw=1)); text(ax,11,12.7,'Buyer',9,ha='left')
 ax.add_patch(Rectangle((29,11.05),3.3,3.3,fc=PALE_G,ec=PINE,lw=1));text(ax,35,12.7,'Supplier',9,ha='left')
 ax.add_patch(Rectangle((56,11.05),3.3,3.3,fc=PALE_R,ec=RUST,lw=1));text(ax,62,12.7,'Disrupted capacity',9,ha='left')
 text(ax,50,4.3,'RELATIONAL DECISIONS   Negotiation   ·   acceptance   ·   partner memory',9.2,'semibold')
 save(fig,'figure01_problem_network')

# F2: data, inference, assumptions and ABM outputs in a single audit-friendly framework.
def pipeline():
 fig,ax=figax(6.65,2.82)
 headers=[('01','OBSERVE',4,22),('02','SCREEN',29,22),('03','ESTIMATE',54,22),('04','SIMULATE',79,17)]
 bodies=[('64 games','33 human–LLM\n31 LLM–LLM'),('Feasible bargains','13/19 and 7/8\nvalid deals'),('Contract kernel','agreement chance\nrounds • price share'),('Repeated trade','24 buyers\n12 suppliers')]
 for (num,hd,x,w),(sub,desc) in zip(headers,bodies):
  bg=PALE_B if num in ('01','02') else PALE_G if num=='03' else PALE
  cl=SLATE if num in ('01','02') else PINE
  card(ax,x,43,w,42,bg,GRID,lw=.9)
  text(ax,x+2.6,78,num,9,'bold',cl,ha='left');text(ax,x+w/2,70.5,hd,10.2,'bold',cl)
  div(ax,x+2.5,x+w-2.5,64.3)
  text(ax,x+w/2,56.2,sub,9.1,'semibold')
  text(ax,x+w/2,47.5,desc,8.8)
 for a,b in [(26.25,28.7),(51.25,53.7),(76.25,78.6)]:arrow(ax,(a,64.2),(b,64.2),SLATE,1.05,9)
 card(ax,4,20,44,14,WHITE,SLATE,.8)
 text(ax,26,29.2,'DATA-INFORMED',9.5,'bold',SLATE)
 text(ax,26,24.0,'Observed outcomes + uncertainty',8.5)
 card(ax,52,20,44,14,WHITE,RUST,.8)
 text(ax,74,29.2,'MODEL-SPECIFIED',9.5,'bold',RUST)
 text(ax,74,24.0,'Bilateral rules + memory + shock',8.5)
 # Provenance bands below annotate the upper pipeline; they are not outputs.
 card(ax,19,3.5,62,10.5,PALE,GRID,.8)
 text(ax,50,8.8,'OUTCOMES    Service   ·   cost   ·   HHI   ·   tie retention',9.1,'semibold')
 # Results are generated by the simulated repeated procurement process above.
 save(fig,'figure02_data_to_abm')

# F3: complete deterministic ABM schedule, with no crossing connectors or ambiguous arrowheads.
def schedule():
 fig,ax=figax(6.65,3.65)
 specs=[(79,'Realize demand and capacity',PALE_B,SLATE),
        (63,'Rank five candidate suppliers',PALE_B,SLATE),
        (47,'Check price and capacity',PALE_B,SLATE),
        (31,'Two-sided agreement decision',PALE_G,PINE),
        (15,'Contract, deliver, update memory',PALE_G,PINE)]
 for y,cap,bg,stroke in specs:
  card(ax,29,y,42,12,bg,GRID,.9)
  text(ax,50,y+6,cap,10.5,'semibold',stroke)
 for ys,ye in [(79+0.1,75),(63+0.1,59),(47+0.1,43),(31+0.1,27)]:
  arrow(ax,(50,ys),(50,ye),SLATE,1.1,10)
 # explicit two failure branches feed a *single* fallback lane on the right
 card(ax,77,37,21,23,PALE_R,GRID,.9)
 text(ax,87.5,53,'IF UNAVAILABLE',8.8,'bold',RUST)
 text(ax,87.5,46.8,'or no agreement',8.6,color=RUST)
 text(ax,87.5,40.7,'try next candidate',8.4,color=RUST)
 arrow(ax,(71,53),(76.6,53),RUST,1.1,9)
 ortho(ax,[(71,37),(74.5,37),(74.5,42),(76.6,42)],RUST,1.1,9)
 ortho(ax,[(87.5,60.2),(87.5,69),(71.3,69)],RUST,1.1,9)
 text(ax,73.7,57,'No',8.1,color=RUST)
 text(ax,72.6,33,'No',8.1,color=RUST)
 text(ax,46.0,24.8,'Yes',8.2,color=PINE,ha='right')
 card(ax,29,1,42,9,PALE,GRID,.8)
 text(ax,50,5.5,'Record service, cost and network state',9.2,'semibold')
 arrow(ax,(50,15),(50,10.1),PINE,1.1,9)
 # semantic layer labels at left; no connector crossing
 card(ax,2,50,21,37,WHITE,GRID,.9)
 text(ax,12.5,77,'STRUCTURED',9,'bold',SLATE)
 text(ax,12.5,68,'shared sourcing\nand feasibility',9.0)
 text(ax,12.5,56,'same in both\nregimes',8.4,color=MID)
 card(ax,2,13,21,31,WHITE,GRID,.9)
 text(ax,12.5,35,'RELATIONAL',9,'bold',PINE)
 text(ax,12.5,26.2,'negotiation\npartner history',8.9)
 text(ax,12.5,17.1,'policy varies',8.5,color=MID)
 save(fig,'figure03_abm_schedule')

# F4 concise stateful buyer/supplier view. Retains only information modeled in code.
def agents():
 fig,ax=figax(6.65,2.52)
 for x,title,cl,bg in [(3,'BUYER i',SLATE,PALE_B),(52,'SUPPLIER j',PINE,PALE_G)]:
  card(ax,x,29,45,62,WHITE,GRID,.9)
  text(ax,x+22.5,82,title,10.5,'bold',cl); div(ax,x+3,x+42,76)
  card(ax,x+3,61,39,10,bg,GRID,.8)
  text(ax,x+22.5,66,'Current demand / ranking' if x==3 else 'Capacity / reservation cost',9)
  card(ax,x+3,45,39,10,bg,GRID,.8)
  text(ax,x+22.5,50,'Partner-specific experience',9)
  card(ax,x+3,29,39,10,bg,GRID,.8)
  text(ax,x+22.5,34,'Acceptance propensity',9)
  arrow(ax,(x+22.5,60.8),(x+22.5,55.3),cl,.95,9);arrow(ax,(x+22.5,44.7),(x+22.5,39.3),cl,.95,9)
 text(ax,50,20,'Agreement needs both parties',9.5,'semibold')
 card(ax,17,3,66,10.5,PALE,GRID,.8)
 text(ax,50,8.2,'Outcomes update partner experience',9.1)
 ortho(ax,[(25.5,28.7),(25.5,24),(45,24)],SLATE,1.0,8)
 ortho(ax,[(74.5,28.7),(74.5,24),(55,24)],PINE,1.0,8)
 arrow(ax,(50,18.3),(50,13.6),SLATE,1.0,8)
 save(fig,'figure04_stateful_agents')

D=pd.read_csv(DATA/'glee_observed_negotiations_sample.csv')
D['valid']=(D.buyer>D.seller)&(D.deal==1)&(D.price>=D.seller)&(D.price<=D.buyer)
D['seller_share']=np.where(D.valid,(D.price-D.seller)/(D.buyer-D.seller),np.nan)
# empirical plot: three honest observed measures; no inference of independent human/AI policies.
def micro():
 fig,axs=plt.subplots(1,3,figsize=(6.65,2.63),dpi=180,gridspec_kw={'width_ratios':[1.05,1.0,1.02]})
 fig.subplots_adjust(left=.065,right=.98,bottom=.24,top=.79,wspace=.44)
 keys=['H','A']; colors=[SLATE,PINE]; labs=['Human–LLM','LLM–LLM']
 valid_counts=[]
 for k in keys:
  x=D[(D.type==k)&(D.buyer>D.seller)];valid_counts.append((int(x.valid.sum()),len(x)))
 ax=axs[0];xs=np.arange(2)
 for i,(s,n) in enumerate(valid_counts):
  p=s/n;lo,hi=proportion_confint(s,n,alpha=.05,method='wilson')
  ax.errorbar(i,p,yerr=[[p-lo],[hi-p]],color=colors[i],fmt='o',markersize=6,capsize=4,lw=1.4,zorder=3)
  ax.text(i,p+.12,f'{s}/{n}',ha='center',fontsize=9,color=INK)
 ax.set_ylim(.25,1.12);ax.set_yticks([.4,.6,.8,1.]);ax.set_ylabel('Valid agreement share');ax.set_xticks(xs,labs,rotation=0,fontsize=8.2);ax.grid(axis='y',color=GRID,lw=.7);ax.set_title('A   Valid agreements',loc='left',fontweight='bold',fontsize=9.5)
 rng=np.random.default_rng(17)
 for idx,field,head,ylim,yticks in [(1,'rounds','B   Deal rounds',(0,11),[0,2,4,6,8,10]),(2,'seller_share','C   Seller surplus share',(-.08,1.09),[0,.25,.5,.75,1])]:
  ax=axs[idx]
  for i,k in enumerate(keys):
   v=D.loc[(D.type==k)&D.valid,field].dropna().values
   jitter=rng.uniform(-.14,.14,size=len(v))
   ax.scatter(np.full_like(v,i,dtype=float)+jitter,v,s=17,color=colors[i],alpha=.52,linewidth=0,zorder=2)
   ax.plot([i-.20,i+.20],[v.mean(),v.mean()],color=INK,lw=2.2,zorder=3)
  ax.set_xticks(xs,labs,fontsize=8.2);ax.set_xlim(-.4,1.4);ax.set_ylim(*ylim);ax.set_yticks(yticks);ax.grid(axis='y',color=GRID,lw=.65)
  ax.set_title(head,loc='left',fontweight='bold',fontsize=9.5);ax.set_ylabel('Rounds' if idx==1 else 'Normalized surplus share')
 save(fig,'fig02_micro')

TR=pd.read_csv(RES/'adaptive_trajectories.csv')
# transparent trajectories: means across 80 replications, five-period smoothing only for displayed line.
def trajectories():
 d=TR[TR.scenario.isin(['H_adaptive','A_adaptive'])].groupby(['scenario','t'],as_index=False)[['service','tie_retention']].mean()
 fig,axs=plt.subplots(2,1,figsize=(6.65,3.45),dpi=180,sharex=True)
 fig.subplots_adjust(left=.104,right=.978,bottom=.14,top=.83,hspace=.31)
 mapping=[('H_adaptive','Human–LLM kernel',SLATE),('A_adaptive','LLM–LLM kernel',PINE)]
 for k,(field,ylabel,ylim) in enumerate([('service','Service rate',(0.65,.96)),('tie_retention','Tie retention',(.24,.57))]):
  ax=axs[k];ax.axvspan(40,54,color=GRID,alpha=.55,zorder=0)
  for sc,lab,color in mapping:
   s=d[d.scenario==sc].sort_values('t')
   # retain exact t values, smooth only presentation, not data underlying model summary
   rolling=s[field].rolling(5,center=True,min_periods=1).mean()
   ax.plot(s.t,rolling,color=color,lw=1.65,label=lab)
  ax.set_ylim(*ylim);ax.set_xlim(0,99);ax.set_ylabel(ylabel);ax.grid(axis='y',color=GRID,lw=.7)
  ax.spines['left'].set_color(GRID);ax.spines['bottom'].set_color(GRID)
 axs[-1].set_xlabel('Simulation period');axs[-1].set_xticks([0,20,39,54,70,99])
 fig.legend([Line2D([0],[0],color=SLATE,lw=2),Line2D([0],[0],color=PINE,lw=2),Rectangle((0,0),1,1,fc=GRID,ec='none',alpha=.55)],
            ['Human–LLM kernel','LLM–LLM kernel','Capacity shock, t = 40–54'],loc='upper center',bbox_to_anchor=(.52,.99),ncol=3,frameon=False,fontsize=9.1)
 save(fig,'fig03_trajectories')

PA=pd.read_csv(RES/'adaptive_paired.csv')
# per-seed distributions not confidence intervals around population effect
def paired():
 sub=PA[(PA.phase=='shock')&(PA.comparison=='A_adaptive - H_adaptive')].set_index('metric')
 labels=[('service','Service level',0.20),('cost_per_demand','Illustrative cost / demand',1.),('hhi','Supplier HHI',.04),('tie_retention','Tie retention',.30)]
 fig,axs=plt.subplots(2,2,figsize=(6.65,3.50),dpi=180);fig.subplots_adjust(left=.13,right=.965,bottom=.16,top=.84,wspace=.48,hspace=.93)
 for i,(field,name,limit) in enumerate(labels):
  ax=axs.flat[i];z=sub.loc[field];x=float(z['mean']);l=float(z['q025']);r=float(z['q975']);
  ax.axvline(0,color=MID,lw=.85,ls='--')
  ax.plot([l,r],[0,0],color=SLATE,lw=2.3);ax.plot([l,l],[-.15,.15],color=SLATE,lw=1.3);ax.plot([r,r],[-.15,.15],color=SLATE,lw=1.3)
  ax.scatter([x],[0],s=40,c=PINE,zorder=5,edgecolor=WHITE,linewidth=.5)
  ax.set_xlim(-limit,limit if field!='cost_per_demand' else limit)
  ax.set_ylim(-.5,.5);ax.set_yticks([]);ax.set_title(chr(65+i)+'   '+name,fontsize=10.3,loc='left',fontweight='bold')
  # Common panel interpretation is given once below all axes.
  ax.spines['left'].set_visible(False);ax.grid(axis='x',color=GRID,lw=.6)
 fig.text(.5,.965,'Dot: mean   ·   Bar: 2.5–97.5% of 80 paired differences',ha='center',va='top',fontsize=9.5,color=MID)
 fig.text(.5,.055,'LLM–LLM kernel minus human–LLM kernel',ha='center',fontsize=9.6,color=INK)
 save(fig,'fig05_paired_effects')

SENS=pd.read_csv(RES/'adaptive_sensitivity.csv')
# additional result artifact: main-file integration optional under page budget.
def sensitivity():
 s=SENS[SENS.scenario=='A_adaptive'].set_index('variant')
 names=[('no_learning','No partner-feedback'),('no_rank_memory','No memory in ranking'),('no_agreement_memory','No memory in acceptance'),('reference','Reference feedback'),('slow_learning','Lower learning rate'),('fast_learning','Higher learning rate')]
 y=np.arange(len(names))[::-1]
 fig,ax=plt.subplots(figsize=(6.65,2.85),dpi=180);fig.subplots_adjust(left=.32,right=.955,bottom=.16,top=.93)
 for ix,(key,lab) in enumerate(names):
  value=float(s.loc[key,'shock_service_mean']);color=PINE if key=='reference' else SLATE
  ax.hlines(y[ix],.72,value,color=color,lw=2.2)
  ax.scatter([value],[y[ix]],s=45,color=color,zorder=3)
  ax.text(value+.003,y[ix],f'{value:.3f}',va='center',ha='left',fontsize=9.6,color=INK)
 ax.set_yticks(y,[x[1] for x in names]);ax.set_xlim(.72,.86);ax.grid(axis='x',color=GRID,lw=.6);ax.set_xlabel('Mean shock-period service (12-seed diagnostic)')
 ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
 save(fig,'fig06_sensitivity')

if __name__=='__main__':
 for f in [problem,pipeline,schedule,agents,micro,trajectories,paired,sensitivity]:
  f();print(f.__name__,'done')
