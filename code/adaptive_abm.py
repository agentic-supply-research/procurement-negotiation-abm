"""Paired ABM: GLEE-outcome priors and explicitly assumed experience-based policies.

All operational states are stylised. 'H' calibrates human--LLM dyads (NOT
human--human); 'A' calibrates LLM--LLM dyads. Learning concerns abstract
contract agents' relational scores, NOT fine-tuning or on-line LLM execution.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.special import expit, logit

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data' / 'glee_observed_negotiations_sample.csv'
OUT = BASE / 'results'

@dataclass(frozen=True)
class Config:
    buyers: int = 24
    suppliers: int = 12
    periods: int = 100
    shock_start: int = 40
    shock_end: int = 55  # exclusive
    shock_strength: float = .65  # reduction of first 4 suppliers
    alpha: float = .18        # update rate (illustrative)
    policy_gain: float = 1.1  # log-odds sensitivity to beliefs
    rank_gain: float = .75    # impact on supplier ranking
    relationship_bonus: float = .6
    unmet_penalty: float = 13.
    negotiation_cost_per_round: float = .08
    max_candidates: int = 5

SCENARIOS = ('H_fixed','H_adaptive','A_fixed','A_adaptive')


def micro_data(path=DATA):
    d = pd.read_csv(path)
    if d.id.duplicated().any():
        raise ValueError('duplicated source ID')
    d['feasible'] = d.buyer > d.seller + 1e-9
    d['valid'] = (d.deal == 1) & d.feasible & d.price.ge(d.seller-1e-9) & d.price.le(d.buyer+1e-9)
    d['share'] = np.where(d.valid, (d.price-d.seller)/(d.buyer-d.seller).replace(0,np.nan),np.nan)
    return d


def empirical_summary(d):
    x=[]
    for typ,lab in [('H','Human--LLM'),('A','LLM--LLM')]:
        f = d[(d.type==typ)&d.feasible]
        v = f[f.valid]
        x.append({'dyad':lab,'n_total':int((d.type==typ).sum()),'n_feasible':len(f),
                  'n_valid':len(v),'valid_rate':len(v)/len(f),
                  'mean_rounds':v.rounds.mean(),'mean_seller_share':v.share.mean()})
    return pd.DataFrame(x)


def kernels(d, seed):
    rng = np.random.default_rng(seed + 987654321)
    out = {}
    for typ in ('H','A'):
        f=d[(d.type==typ)&d.feasible]
        v=f[f.valid]
        n_yes=len(v); n_no=len(f)-n_yes
        p=float(rng.beta(n_yes+.5,n_no+.5))
        out[typ]={'p':np.clip(p,1e-6,1-1e-6),'share':v.share.to_numpy(float),'rounds':v.rounds.to_numpy(int)}
    return out


def setup(seed: int, cfg:Config):
    """Exogenous panel identical across regimes sharing seed."""
    rng=np.random.default_rng(seed)
    B,S,T=cfg.buyers,cfg.suppliers,cfg.periods
    cap=rng.uniform(12,19,S)
    cost=rng.uniform(6.8,9.2,S)
    val=rng.uniform(11,13.5,B)
    demand=rng.poisson(5.3,(T,B)).astype(float)
    init_rel=np.zeros((B,S),float)
    for b in range(B):
        j=rng.choice(S,3,replace=False)
        init_rel[b,j]=rng.uniform(.35,.70,3)
    # Scenario-invariant idiosyncratic draws by time/buyer/supplier.
    streams=np.random.default_rng(seed+111111)
    u_b=streams.random((T,B,S)); u_s=streams.random((T,B,S))
    u_z=streams.random((T,B,S)); u_round=streams.random((T,B,S))
    cap_noise=np.random.default_rng(seed+222222).normal(0,.8,(T,S))
    order=[np.random.default_rng(seed+333333+t).permutation(B) for t in range(T)]
    return cap,cost,val,demand,init_rel,u_b,u_s,u_z,u_round,cap_noise,order


def simulate(seed:int,scenario:str,data:pd.DataFrame,cfg:Config=Config(),trace_edges=False, edge_records=None):
    if scenario not in SCENARIOS:
        raise ValueError(scenario)
    typ=scenario[0]
    learning=scenario.endswith('adaptive') and cfg.alpha>0
    ker=kernels(data,seed)[typ]
    # Joint feasible-deal probability is only identified at dyad level. The
    # equal square-root allocation to both roles is an IDENTIFICATION ASSUMPTION.
    base_p=np.sqrt(ker['p'])
    base_logit=logit(base_p)
    (base_cap,base_cost,values,demands,rel,u_b,u_s,u_z,u_round,cap_noise,order)=setup(seed,cfg)
    B,S,T=cfg.buyers,cfg.suppliers,cfg.periods
    q_b=np.zeros((B,S),float)  # buyer's partner-specific satisfaction memory
    q_s=np.zeros((S,B),float)  # supplier's buyer-specific satisfaction memory
    recent_active=np.zeros((B,S),bool)
    total_edges=np.zeros((B,S),float)
    rows=[]; saved=[]
    for t in range(T):
        shock = cfg.shock_start <= t < cfg.shock_end
        caps=base_cap.copy()
        if shock: caps[:min(4,S)]*=(1-cfg.shock_strength)
        caps=np.maximum(0,caps+cap_noise[t])
        available=caps.copy()
        served=np.zeros(B); supplied=np.zeros(S)
        trading=np.zeros((B,S),float)
        rounds_total=0; attempts=0; deals=0; price_spend=0.; capacity_denials=0
        accepted_margins=[]
        for b in order[t]:
            remaining=demands[t,b]
            if remaining<=0: continue
            score=base_cost+1.15*(1-rel[b]) - cfg.relationship_bonus*rel[b] + .06*np.arange(S)/S
            if learning: score-=cfg.rank_gain*q_b[b]
            # Same mathematical ranking function in every scenario; only
            # empirical dyad prior and endogenous memory differ.
            candidates=np.argsort(score)[:cfg.max_candidates]
            for s in candidates:
                if remaining<=1e-9: break
                if values[b]<=base_cost[s]: continue
                if available[s]<=1e-9:
                    capacity_denials += 1
                    if learning: q_b[b,s]=(1-cfg.alpha)*q_b[b,s]+cfg.alpha*(-.9)
                    continue
                attempts+=1
                p_b=expit(base_logit + (cfg.policy_gain*q_b[b,s] if learning else 0.))
                p_s=expit(base_logit + (cfg.policy_gain*q_s[s,b] if learning else 0.))
                buyer_agrees=u_b[t,b,s]<p_b
                supplier_agrees=u_s[t,b,s]<p_s
                success=bool(buyer_agrees and supplier_agrees)
                if success:
                    qty=min(remaining,available[s]); available[s]-=qty; remaining-=qty
                    served[b]+=qty;supplied[s]+=qty;trading[b,s]+=qty;total_edges[b,s]+=qty
                    z=float(ker['share'][min(int(u_z[t,b,s]*len(ker['share'])),len(ker['share'])-1)])
                    rd=int(ker['rounds'][min(int(u_round[t,b,s]*len(ker['rounds'])),len(ker['rounds'])-1)])
                    price=base_cost[s]+z*(values[b]-base_cost[s])
                    assert base_cost[s]-1e-8<=price<=values[b]+1e-8
                    price_spend+=qty*price;rounds_total+=rd;deals+=1
                    accepted_margins.append(z)
                    rel[b,s]=min(1.,rel[b,s]+.055)
                    # Distinct payoffs reflect buyer/supplier surplus shares.
                    if learning:
                        outcome_b=1.-.60*z
                        outcome_s=.40+.60*z
                else:
                    rel[b,s]*=.96
                    if learning: outcome_b=outcome_s=-.65
                if learning:
                    q_b[b,s]=(1-cfg.alpha)*q_b[b,s]+cfg.alpha*outcome_b
                    q_s[s,b]=(1-cfg.alpha)*q_s[s,b]+cfg.alpha*outcome_s
            rel[b]*=.997
        assert np.all(available>=-1e-8)
        assert np.all(served<=demands[t]+1e-8)
        assert np.all(supplied<=caps+1e-8)
        assert np.isclose(served.sum(),supplied.sum(),atol=1e-6)
        miss=demands[t].sum()-served.sum();demand_sum=demands[t].sum()
        shares=supplied/supplied.sum() if supplied.sum()>0 else np.zeros(S)
        active=trading>1e-9
        prev_edges=int(recent_active.sum())
        persistent=int((active & recent_active).sum())
        tie_retention=(persistent/prev_edges) if prev_edges else np.nan
        recent_active=active
        if edge_records is not None:
            # Optional observational trace; does not alter agent actions or RNG streams.
            edge_records.append((active.copy(), supplied.copy(), trading.copy()))
        neg_fee=rounds_total*cfg.negotiation_cost_per_round
        rows.append({'seed':seed,'scenario':scenario,'t':t,'shock':int(shock),
                     'demand':demand_sum,'delivered':float(served.sum()),'unserved':miss,
                     'service':served.sum()/max(demand_sum,1),
                     'hhi':float((shares**2).sum()) if served.sum()>0 else np.nan,
                     'cost_per_demand':(price_spend+neg_fee+cfg.unmet_penalty*miss)/max(demand_sum,1),
                     'purchase_cost':price_spend,'negotiation_cost':neg_fee,
                     'attempts':attempts,'deals':deals,
                     'n_ties':int(active.sum()),'tie_retention':tie_retention,
                     'capacity_denials':capacity_denials,'q_b_mean':q_b.mean(),'q_s_mean':q_s.mean(),
                     'seller_share':float(np.mean(accepted_margins)) if accepted_margins else np.nan})
        if trace_edges and t in (0,39,48,54,70,99):
            saved.append({'t':t,'trade_weights':trading.copy(),'cumulative_weights':total_edges.copy(),
                          'buyer_memory':q_b.copy(),'supplier_memory':q_s.copy()})
    return pd.DataFrame(rows),saved


def aggregate(trace):
    parts=[]
    for (scenario,seed),g in trace.groupby(['scenario','seed'],sort=False):
        for phase,gp in [('all',g),('pre',g[g.t<40]),('shock',g[(g.t>=40)&(g.t<55)]),('post',g[g.t>=55])]:
            d=gp.demand.sum()
            parts.append({'scenario':scenario,'seed':seed,'phase':phase,
                          'service':gp.delivered.sum()/d,
                          'cost_per_demand':float((gp.cost_per_demand*gp.demand).sum()/d),
                          'hhi':float(gp.hhi.mean()),
                          'n_ties':float(gp.n_ties.mean()),
                          'tie_retention':float(gp.tie_retention.mean()),
                          'attempts':int(gp.attempts.sum()),'deals':int(gp.deals.sum()),
                          'denials':int(gp.capacity_denials.sum())})
    return pd.DataFrame(parts)


def summary_metrics(agg):
    out=[]
    for (scenario,phase),g in agg.groupby(['scenario','phase'],sort=False):
        row={'scenario':scenario,'phase':phase,'reps':len(g)}
        for col in ('service','cost_per_demand','hhi','n_ties','tie_retention'):
            x=g[col].dropna().to_numpy()
            row[col+'_mean']=float(x.mean())
            row[col+'_q025']=float(np.quantile(x,.025))
            row[col+'_q975']=float(np.quantile(x,.975))
        out.append(row)
    return pd.DataFrame(out)


def paired_differences(agg):
    pairs=[('A_fixed','H_fixed'),('A_adaptive','H_adaptive'),('A_adaptive','A_fixed'),('H_adaptive','H_fixed')]
    out=[]
    for x,y in pairs:
        for phase in ('pre','shock','post','all'):
            a=agg[(agg.scenario==x)&(agg.phase==phase)].set_index('seed')
            b=agg[(agg.scenario==y)&(agg.phase==phase)].set_index('seed')
            for col in ('service','cost_per_demand','hhi','tie_retention','n_ties'):
                z=(a[col]-b[col]).dropna()
                out.append({'comparison':f'{x} - {y}','phase':phase,'metric':col,'mean':z.mean(),
                            'q025':z.quantile(.025),'q975':z.quantile(.975),'n':len(z)})
    return pd.DataFrame(out)


def main(reps=80,cfg:Config=Config(),out_dir=OUT,save=True):
    d=micro_data()
    traces=[];snapshots={}
    for seed in range(reps):
        for scenario in SCENARIOS:
            trace,snaps=simulate(seed,scenario,d,cfg,trace_edges=(seed==0))
            traces.append(trace)
            if seed==0: snapshots[scenario]=snaps
    trace=pd.concat(traces,ignore_index=True)
    agg=aggregate(trace)
    sm=summary_metrics(agg);pdiff=paired_differences(agg)
    if save:
        out_dir.mkdir(parents=True,exist_ok=True)
        empirical_summary(d).to_csv(out_dir/'empirical_summary.csv',index=False)
        trace.to_csv(out_dir/'adaptive_trajectories.csv',index=False)
        agg.to_csv(out_dir/'adaptive_replications.csv',index=False)
        sm.to_csv(out_dir/'adaptive_summary.csv',index=False)
        pdiff.to_csv(out_dir/'adaptive_paired.csv',index=False)
        np.savez_compressed(out_dir/'adaptive_snapshots_seed0.npz',**{
            f'{scenario}_trade_t{e["t"]}':e['trade_weights'] for scenario,ls in snapshots.items() for e in ls})
    return trace,agg,sm,pdiff

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--reps',type=int,default=80)
    ap.add_argument('--alpha',type=float,default=.18)
    ap.add_argument('--shock-strength',type=float,default=.65)
    ap.add_argument('--out-dir',type=Path,default=OUT,help='Output directory (default: results/)')
    ns=ap.parse_args()
    _,_,sm,paired=main(ns.reps,replace(Config(),alpha=ns.alpha,shock_strength=ns.shock_strength),out_dir=ns.out_dir)
    print('SHOCK SUMMARY:')
    print(sm[sm.phase=='shock'][['scenario','service_mean','cost_per_demand_mean','hhi_mean','tie_retention_mean']].to_string(index=False))
    print('\nPAIRED SHOCK:')
    print(paired[(paired.phase=='shock')&(paired.metric.isin(['service','cost_per_demand']))].to_string(index=False))
