from pilot import load_data,simulate,ROOT
import pandas as pd
D=load_data();out=[]
for sh in (.35,.65,.80):
 for bonus in (0.,.6,1.25):
  for seed in range(3):
   for regime in ('Human-LLM mixed','Full AI-AI'):
    x,_=simulate(regime,seed+2000,D,shock_strength=sh,relation_bonus=bonus)
    w=x[x.disrupted==1]
    out.append({'shock':sh,'relationship_bonus':bonus,'seed':seed,'regime':regime,'service':w.delivered.sum()/w.demand.sum(),'hhi':w.hhi.mean()})
pd.DataFrame(out).to_csv(ROOT/'results'/'sensitivity.csv',index=False)
print('Sensitivity rows',len(out))
