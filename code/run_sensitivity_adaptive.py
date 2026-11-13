"""Sensitivity of learned behavioral policy to unobserved update assumptions."""
from dataclasses import replace
from pathlib import Path
import sys
import pandas as pd
from adaptive_abm import Config, micro_data, simulate, aggregate, summary_metrics

ROOT=Path(__file__).resolve().parents[1]
DATA=micro_data()

def run(n=12, out_dir=ROOT/'results'):
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    rows=[]
    variants=[('reference',Config()),('no_learning',replace(Config(),alpha=0.)),
              ('slow_learning',replace(Config(),alpha=.08)),
              ('fast_learning',replace(Config(),alpha=.35)),
              ('no_rank_memory',replace(Config(),rank_gain=0.)),
              ('no_agreement_memory',replace(Config(),policy_gain=0.)),
              ('mild_shock',replace(Config(),shock_strength=.45)),
              ('severe_shock',replace(Config(),shock_strength=.8))]
    for label,cfg in variants:
        dfs=[]
        for seed in range(n):
            for scenario in ('H_fixed','H_adaptive','A_fixed','A_adaptive'):
                x,_=simulate(seed,scenario,DATA,cfg)
                dfs.append(x)
        agg=aggregate(pd.concat(dfs,ignore_index=True))
        summ=summary_metrics(agg)
        q=summ[summ.phase=='shock']
        for _,r in q.iterrows():
            rows.append({'variant':label,'scenario':r.scenario,'n':n,'shock_service_mean':r.service_mean,
                         'shock_cost_mean':r.cost_per_demand_mean,'shock_hhi_mean':r.hhi_mean,
                         'shock_retention_mean':r.tie_retention_mean,
                         'alpha':cfg.alpha,'policy_gain':cfg.policy_gain,
                         'rank_gain':cfg.rank_gain,'shock_strength':cfg.shock_strength})
        print(label,flush=True)
    r=pd.DataFrame(rows);r.to_csv(out_dir/'adaptive_sensitivity.csv',index=False)
    return r

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description='Feedback-policy sensitivity analysis')
    p.add_argument('--seeds', type=int, default=12)
    p.add_argument('--out-dir', type=Path, default=ROOT/'results')
    a=p.parse_args()
    run(a.seeds, a.out_dir)
