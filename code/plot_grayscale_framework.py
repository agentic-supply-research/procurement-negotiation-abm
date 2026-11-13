"""Print-first scientific diagrams. Coordinate-based, monochrome, 600 dpi.

A: one physical buyer-supplier system and two alternatives for relational
   decision authority (target interventions, NOT two observed networks).
B: auditable evidence-to-policy translation with explicit assumptions.
C: operational/relational decision sequence with condition branches.

All figures use matplotlib native vector geometry; no generative imagery.
"""
from pathlib import Path
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D

OUT=Path(__file__).resolve().parents[1]/'figures'
OUT.mkdir(exist_ok=True)
BLACK='#141414'; CHAR='#343434'; MID='#636363'; LIGHT='#a7a7a7'; GRID='#d1d1d1'; PALE='#f3f3f3'; WHITE='#ffffff'
mpl.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'text.color':BLACK,
   'axes.edgecolor':CHAR,'pdf.fonttype':42,'ps.fonttype':42,
   'savefig.facecolor':'white','savefig.pad_inches':0.03})

def newfig(name,h):
    fig,ax=plt.subplots(figsize=(6.72,h))
    fig.patch.set_facecolor(WHITE);ax.set_xlim(0,100);ax.set_ylim(0,100);ax.set_aspect('auto');ax.axis('off')
    fig.subplots_adjust(left=.015,right=.985,bottom=.015,top=.985)
    return fig,ax

def txt(ax,x,y,s,fs=8.6,weight='normal',ha='left',va='center',color=BLACK,**kwargs):
    return ax.text(x,y,s,fontsize=fs,fontweight=weight,ha=ha,va=va,color=color,linespacing=1.25,**kwargs)

def rect(ax,x,y,w,h,fill=WHITE,edge=CHAR,lw=.75):
    p=Rectangle((x,y),w,h,linewidth=lw,edgecolor=edge,facecolor=fill,joinstyle='miter',zorder=1)
    ax.add_patch(p);return p

def line(ax,x1,y1,x2,y2, lw=.75,color=CHAR,style='-'):
    ax.add_line(Line2D([x1,x2],[y1,y2],color=color,linewidth=lw,linestyle=style,solid_capstyle='butt',zorder=3))

def arrow(ax,a,b,lw=.85,color=BLACK,ms=8,style='-|>'):
    p=FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=ms,color=color,linewidth=lw,
            shrinkA=0,shrinkB=0,connectionstyle='arc3,rad=0',zorder=4)
    ax.add_patch(p)

def route(ax,xy,stroke=BLACK,lw=.85,finish=True,ms=7.5):
    for a,b in zip(xy[:-2],xy[1:-1]): line(ax,*a,*b,lw,stroke)
    if finish: arrow(ax,xy[-2],xy[-1],lw,stroke,ms)
    else: line(ax,*xy[-2],*xy[-1],lw,stroke)

def dot(ax,x,y,r=0.95,fill=WHITE,lw=.9):
    ax.add_patch(Circle((x,y),r,fc=fill,ec=BLACK,lw=lw,zorder=6))

def panel_title(ax,x,y,label,rule_to=None):
    txt(ax,x,y,label,fs=8.5,weight='bold')
    if rule_to: line(ax,x,y-4,rule_to,y-4,.55,GRID)

def export(fig,name):
    for ext in ('pdf','svg','png'):
        fig.savefig(OUT/(name+'.'+ext),dpi=600 if ext=='png' else 200,
                bbox_inches='tight',pad_inches=.035,metadata=({'Creator':'Matplotlib; code/plot_grayscale_framework.py'} if ext=='pdf' else None))
    plt.close(fig)

# FIGURE 1: one physical supply network; decision authority is the counterfactual.
def figure1():
    fig,ax=newfig('figure01_problem_network',3.58)
    panel_title(ax,2.0,96,'A   COMMON SUPPLY ENVIRONMENT',98)
    rect(ax,2,51,45,37,WHITE,GRID,.7)
    txt(ax,4,84,'Buyers',8.2,'bold');txt(ax,30.5,84,'Suppliers',8.2,'bold')
    bxs=[(10,74),(10,65.5),(10,57)];sxs=[(34,76),(34,65.5),(34,55)]
    edges=[(0,0),(0,1),(1,0),(1,2),(2,1),(2,2)]
    for i,j in edges:line(ax,bxs[i][0]+1.15,bxs[i][1],sxs[j][0]-1.15,sxs[j][1],.73,CHAR)
    for i,(x,y) in enumerate(bxs):
        dot(ax,x,y,1.25,WHITE);txt(ax,x-3.8,y,f'B{i+1}',7.0,ha='right')
    for j,(x,y) in enumerate(sxs):
        rect(ax,x-1.3,y-1.3,2.6,2.6,WHITE,BLACK,.95)
        txt(ax,x+2.7,y,f'S{j+1}',7.0)
    # Shock is common to both authority arrangements
    # The network is schematic; interpretation belongs in the manuscript caption.
    rect(ax,52,51,46,37,PALE,GRID,.7)
    panel_title(ax,55,84,'Structured decisions (shared)')
    for i,s in enumerate(['Demand and reservation values','Supplier ranking / candidate shortlist','Price and capacity feasibility','Contract quantity and material flow']):
        txt(ax,55,77-i*6.3,f'{i+1:02d}',7.5,'bold',color=CHAR)
        txt(ax,61,77-i*6.3,s,8.0)
    arrow(ax,(47.4,69),(51.6,69),.9,BLACK,8.5)

    panel_title(ax,2,45,'B   DECISION AUTHORITY',98)
    # Single environment with alternatives at the policy layer, not duplicate networks
    rect(ax,2,19,46,22,WHITE,BLACK,.8)
    rect(ax,52,19,46,22,WHITE,BLACK,.8)
    txt(ax,5,36,'Human decision maker',9.0,'bold')
    txt(ax,5,29.1,'Contextual judgment and relational trust',7.95)
    txt(ax,5,23.3,'Concessions, renewal and partner commitment',7.8)
    txt(ax,55,36,'LLM-based procurement agent',9.0,'bold')
    txt(ax,55,29.1,'Model-based dialogue, context and tools',7.95)
    txt(ax,55,23.3,'Memory retrieval, proposals and partner choices',7.75)
    # route of interventions: no implied already-estimated separate policies
    route(ax,[(75,50.8),(75,49.0),(42,49.0),(42,41.3)],CHAR,.80,True)
    arrow(ax,(75,49.0),(75,41.3),.8,CHAR,7.5)
    rect(ax,18,3,64,11.2,PALE,GRID,.7)
    txt(ax,50,9.9,'Contracts  →  partner histories  →  changing supply ties',8.0,'bold',ha='center')
    txt(ax,50,5.6,'Service   ·   concentration   ·   continuity   ·   disruption response',7.2,ha='center',color=MID)
    arrow(ax,(25,18.7),(25,14.7),.8,CHAR,7)
    arrow(ax,(75,18.7),(75,14.7),.8,CHAR,7)
    export(fig,'figure01_problem_network')

# FIGURE 2: measured vs assumed quantities separated visibly.
def figure2():
    fig,ax=newfig('figure02_data_to_abm',3.35)
    panel_title(ax,2,96,'EVIDENCE  →  BEHAVIORAL POLICY  →  REPEATED PROCUREMENT',98)
    # three columns
    rect(ax,2,31,28,56,WHITE,GRID,.8)
    rect(ax,36,31,28,56,WHITE,GRID,.8)
    rect(ax,70,31,28,56,WHITE,GRID,.8)
    txt(ax,5,82,'1   SOURCE RECORDS',8.75,'bold')
    line(ax,5,78,27,78,.6,GRID)
    txt(ax,5,71,'Human–LLM: 33 games',8.0)
    txt(ax,5,65,'LLM–LLM: 31 games',8.0)
    txt(ax,5,55,'Economic feasibility',8.2,'bold')
    txt(ax,5,49,'13 / 19 valid deals',8.2)
    txt(ax,5,43,'7 / 8 valid deals',8.2)
    txt(ax,5,35,'Observed dyad outcomes',7.45,color=MID)
    txt(ax,39,82,'2   UNCERTAIN KERNEL',8.75,'bold')
    line(ax,39,78,61,78,.6,GRID)
    txt(ax,39,70,'Agreement probability',8.0,'bold')
    txt(ax,39,63,'Beta posterior, by dyad',7.85)
    txt(ax,39,53,'Deal duration',8.0,'bold')
    txt(ax,39,46,'Observed rounds, resampled',7.7)
    txt(ax,39,36,'Seller share, resampled',7.7)
    txt(ax,73,82,'3   ABM DECISIONS',8.75,'bold')
    line(ax,73,78,95,78,.6,GRID)
    txt(ax,73,70,'Buyer and supplier',8.1,'bold')
    txt(ax,73,63,'Joint contract acceptance',7.8)
    txt(ax,73,53,'Partner-specific history',8.0,'bold')
    txt(ax,73,46,'Future supplier contacts',7.75)
    txt(ax,73,36,'Capacity-constrained trade',7.6)
    arrow(ax,(30.3,59.8),(35.4,59.8),1,BLACK,9)
    arrow(ax,(64.3,59.8),(69.4,59.8),1,BLACK,9)
    # basis row
    panel_title(ax,2,25,'IDENTIFICATION AND MODEL SCOPE')
    rect(ax,2,3,96,17.5,PALE,GRID,.7)
    txt(ax,4.5,15.0,'Measured',8.15,'bold')
    txt(ax,4.5,8.3,'Agreement, rounds, price share',7.7)
    line(ax,34,5,34,18,.7,GRID)
    txt(ax,37,15,'Assumed',8.15,'bold')
    txt(ax,37,8.2,'Role split, memory, feedback',7.7)
    line(ax,68,5,68,18,.7,GRID)
    txt(ax,71,15,'Generated',8.15,'bold')
    txt(ax,71,8.2,'Contracts, ties, service, costs',7.7)
    export(fig,'figure02_data_to_abm')

# FIGURE 3: decision logic with explicit yes/no branches and one return loop.
def figure3():
    fig,ax=newfig('figure03_abm_schedule',3.28)
    panel_title(ax,2,95,'ONE PROCUREMENT PERIOD: BUYER–SUPPLIER DECISIONS',98)
    # structured (upper) and relational (lower) separated by a horizontal rule
    txt(ax,2,84,'Structured',8.3,'bold')
    rect(ax,19,77.5,23,13,PALE,CHAR,.8)
    txt(ax,30.5,85.6,'Demand and',8.15,ha='center')
    txt(ax,30.5,80.8,'supplier capacity',8.15,ha='center')
    rect(ax,53,77.5,26,13,PALE,CHAR,.8)
    txt(ax,66,85.6,'Rank up to five',8.15,ha='center')
    txt(ax,66,80.8,'candidate suppliers',8.15,ha='center')
    arrow(ax,(42.5,84),(52.7,84),.95,BLACK,8.8)
    # stage change down to contact check
    route(ax,[(66,77.1),(66,72.8),(22,72.8),(22,65.5)],BLACK,.9,True)
    line(ax,2,68.8,98,68.8,.6,GRID)
    txt(ax,2,64.4,'Relational',8.3,'bold')
    # Conditions and states in single horizontal pathway, two no arrows downward
    rect(ax,15,47,20,16,WHITE,CHAR,.8)
    txt(ax,25,57.5,'Feasible price',8.05,ha='center')
    txt(ax,25,51.7,'and capacity?',8.05,ha='center')
    rect(ax,43,47,24,16,WHITE,CHAR,.8)
    txt(ax,55,57.5,'Buyer and supplier',8.0,ha='center')
    txt(ax,55,51.7,'both accept?',8.0,ha='center')
    rect(ax,76,47,22,16,PALE,BLACK,.85)
    txt(ax,87,57.5,'Execute contract',8.0,'bold',ha='center')
    txt(ax,87,51.7,'and deliver',8.0,ha='center')
    arrow(ax,(35.25,55),(42.7,55),.9,BLACK,8.5)
    txt(ax,39,59,'yes',7.2,ha='center',color=MID)
    arrow(ax,(67.25,55),(75.7,55),.9,BLACK,8.5)
    txt(ax,71,59,'yes',7.2,ha='center',color=MID)
    # failures go to same fallback, but down arrows end before box borders
    rect(ax,24,18.5,45,15,WHITE,CHAR,.8)
    txt(ax,46.5,28,'Update outcome; try next candidate',8.0,ha='center')
    txt(ax,46.5,22.7,'(if unserved demand and options remain)',7.45,ha='center',color=MID)
    arrow(ax,(25,46.6),(25,34),.85,BLACK,7.5)
    txt(ax,27,40.8,'no',7.2,color=MID)
    arrow(ax,(55,46.6),(55,34),.85,BLACK,7.5)
    txt(ax,57,40.8,'no',7.2,color=MID)
    # return to next candidate via left margin (no crossings)
    route(ax,[(24,26),(12,26),(12,55),(14.7,55)],MID,.85,True)
    # Success path
    rect(ax,77,19,21,14,PALE,CHAR,.8)
    txt(ax,87.5,27,'Update both',8.0,ha='center')
    txt(ax,87.5,22.2,'partner states',8.0,ha='center')
    arrow(ax,(87,46.7),(87,33.4),.85,BLACK,7.5)
    # bottom observation strip
    line(ax,2,14,98,14,.6,GRID)
    txt(ax,2,7.6,'At period end',8.15,'bold')
    txt(ax,24,7.6,'Unfilled demand   •   unit cost   •   active ties   •   supplier HHI   •   tie retention',7.7)
    export(fig,'figure03_abm_schedule')

if __name__=='__main__':
    figure1();figure2();figure3()
    print('Exported grayscale print-first Figs 1–3 to',OUT)
