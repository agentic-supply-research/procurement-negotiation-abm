"""Derived network emergence diagnostics, 80 matched seeds, H/A feedback-on.

Existing ABM behavior is unmodified. Logs all realized trading edges to calculate
shock-driven supplier-share displacement and persistence of shock-originated edges.
No results are interpreted as observations of real firm networks.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from adaptive_abm import micro_data, simulate, Config

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)


def run(nseeds=80, out_dir=OUT):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data=micro_data(); cfg=Config(); rows=[]; cohort=[]; metrics=[]; robustness=[]
    for seed in range(nseeds):
        for sc in ('H_adaptive','A_adaptive'):
            rec=[]
            traj,_=simulate(seed,sc,data,cfg,edge_records=rec)
            assert len(rec)==cfg.periods
            edge=np.array([r[0] for r in rec],dtype=bool)
            supplied=np.array([r[1] for r in rec],float)
            weights=np.array([r[2] for r in rec],float)
            shares=supplied/np.maximum(supplied.sum(1)[:,None],1e-12)
            baseline_share=shares[30:40].mean(0)
            baseline_edges=edge[30:40].any(0)
            shock_edges=edge[40:55].any(0)
            shock_new=shock_edges & ~baseline_edges
            n_new=int(shock_new.sum())
            for w in (10,20,30):
                ref=edge[40-w:40].any(0)
                newcomers=shock_edges & ~ref
                n_cohort=int(newcomers.sum())
                returns=int((edge[55:70].any(0) & newcomers).sum())
                post_trade=weights[55:70]
                robustness.append(dict(seed=seed,scenario=sc,baseline_window=w,
                                       newcomer_count=n_cohort,
                                       reappearance_15=returns/n_cohort if n_cohort else np.nan,
                                       early_post_volume_share=post_trade[:,newcomers].sum()/max(post_trade.sum(),1e-12)))
            for t in range(30,100):
                active=edge[t]
                tv=.5*np.abs(shares[t]-baseline_share).sum()
                novelty=float((active & ~baseline_edges).sum()/max(1,active.sum()))
                share_vol=float(weights[t][shock_new].sum()/max(1e-12,weights[t].sum()))
                rows.append(dict(seed=seed,scenario=sc,t=t,phase='pre' if t<40 else 'shock' if t<55 else 'post',
                                 supplier_tv=tv,active_edge_novelty=novelty,
                                 shock_new_volume_share=share_vol,n_shock_new=n_new))
            # Post-shock cumulative fraction of new shock-created edges seen again.
            for k in range(1,31):
                has_return=(edge[55:55+k].any(0) & shock_new).sum() if n_new else 0
                cohort.append(dict(seed=seed,scenario=sc,post_periods=k,n_shock_new=n_new,
                                   cumulative_reappearance=has_return/n_new if n_new else np.nan))
            for phase,inds in [('shock',slice(40,55)),('early_recovery',slice(55,70)),('late_recovery',slice(70,100))]:
                act=edge[inds]; wei=weights[inds]
                # Per-run coherent shares; no double count within time.
                flow_on_shock_new=float(wei[:,shock_new].sum()/max(wei.sum(),1e-12))
                metrics.append(dict(seed=seed,scenario=sc,phase=phase,shock_new_count=n_new,
                                    flow_on_shock_new=flow_on_shock_new,
                                    supplier_tv=float(np.mean([.5*np.abs(s-baseline_share).sum() for s in shares[inds]])),
                                    active_edge_novelty=float(np.mean([(a & ~baseline_edges).sum()/max(1,a.sum()) for a in act]))))
    pd.DataFrame(rows).to_csv(out_dir/'emergent_link_trajectories.csv',index=False)
    pd.DataFrame(cohort).to_csv(out_dir/'emergent_link_cohorts.csv',index=False)
    pd.DataFrame(metrics).to_csv(out_dir/'emergent_link_phase_metrics.csv',index=False)
    pd.DataFrame(robustness).to_csv(out_dir/'emergent_link_baseline_robustness.csv',index=False)
    print('\nEmergent metrics by phase and scenario:')
    a=pd.DataFrame(metrics)
    print(a.groupby(['scenario','phase'])[['shock_new_count','flow_on_shock_new','supplier_tv','active_edge_novelty']].mean().round(4).to_string())
    print('\nShock-created edges returning by 15 periods:')
    b=pd.DataFrame(cohort)
    print(b[b.post_periods==15].groupby('scenario').cumulative_reappearance.agg(['mean','std','count']).round(4).to_string())
    print('\nPre-shock reference window sensitivity:')
    print(pd.DataFrame(robustness).groupby(['baseline_window','scenario'])[['newcomer_count','reappearance_15','early_post_volume_share']].mean().round(4).to_string())

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Recompute realized trading-network metrics')
    parser.add_argument('--seeds', type=int, default=80)
    parser.add_argument('--out-dir', type=Path, default=OUT)
    args=parser.parse_args()
    run(nseeds=args.seeds, out_dir=args.out_dir)
