"""Validate the shape, keys, and central values of the archived experiment data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'
EXPECT_SCENARIOS={'H_fixed','H_adaptive','A_fixed','A_adaptive'}

def require(ok,message):
    if not bool(ok): raise AssertionError(message)

def run():
    emp=pd.read_csv(RES/'empirical_summary.csv')
    require(len(emp)==2,'empirical summary must have 2 dyad rows')
    require(emp.n_total.sum()==64,'empirical count mismatch')
    require(emp.n_valid.tolist()==[13,7],'valid-agreement counts mismatch')

    trace=pd.read_csv(RES/'adaptive_trajectories.csv')
    require(len(trace)==32000,'expected 4×80×100 period-level rows')
    require(set(trace.scenario)==EXPECT_SCENARIOS,'scenario labels mismatch')
    require(set(trace.seed)==set(range(80)),'main seed range mismatch')
    require(set(trace.t)==set(range(100)),'main time range mismatch')
    require(not trace.duplicated(['scenario','seed','t']).any(),'duplicate trajectory key')
    require(np.allclose(trace.delivered+trace.unserved,trace.demand,atol=1e-8),'flow conservation failed')
    require((trace.delivered<=trace.demand+1e-8).all(),'delivered units exceed demand')
    require(trace.service.between(0,1).all(),'service outside [0,1]')
    require(trace.hhi.dropna().between(0,1).all(),'HHI outside [0,1]')
    require((trace.groupby(['scenario','seed']).shock.sum()==15).all(),'shock duration must be 15 periods per run')

    agg=pd.read_csv(RES/'adaptive_replications.csv')
    summ=pd.read_csv(RES/'adaptive_summary.csv')
    pairs=pd.read_csv(RES/'adaptive_paired.csv')
    require(len(agg)==1280,'replication metrics should contain 4×80×4 rows')
    require(len(summ)==16,'summary metrics should contain 4×4 rows')
    require(len(pairs)==80,'paired-effects table should contain 80 rows')
    require(not agg.duplicated(['scenario','seed','phase']).any(),'duplicate seed-phase key')
    for _, row in summ.iterrows():
        sample=agg[(agg.scenario==row.scenario)&(agg.phase==row.phase)]
        require(len(sample)==80,f'incomplete seed coverage for {row.scenario} {row.phase}')
        require(abs(sample.service.mean()-row.service_mean)<1e-11,'summary service mismatch')
        require(abs(sample.hhi.mean()-row.hhi_mean)<1e-11,'summary HHI mismatch')

    emer=pd.read_csv(RES/'emergent_link_trajectories.csv')
    cohort=pd.read_csv(RES/'emergent_link_cohorts.csv')
    met=pd.read_csv(RES/'emergent_link_phase_metrics.csv')
    robust=pd.read_csv(RES/'emergent_link_baseline_robustness.csv')
    require(len(emer)==11200,'emergent time trajectories require 2×80×70 rows')
    require(len(cohort)==4800,'emergent link cohorts require 2×80×30 rows')
    require(len(met)==480,'emergent phase metrics require 2×80×3 rows')
    require(len(robust)==480,'emergent baseline sensitivity requires 2×80×3 rows')
    v=cohort[cohort.post_periods==15].groupby('scenario').cumulative_reappearance.mean()
    require(abs(v.loc['H_adaptive']-0.5932)<1e-3,'H kernel emergence summary mismatch')
    require(abs(v.loc['A_adaptive']-0.4510)<1e-3,'A kernel emergence summary mismatch')
    print('PASS: empirical calibration, 80-seed runs, accounting, summaries and emergent-link results')
    print('Shock-activated link reactivation (15 recovery periods):',v.round(4).to_dict())

if __name__=='__main__':run()
