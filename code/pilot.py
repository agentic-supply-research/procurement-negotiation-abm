"""Genuine GLEE logged micro-observations -> illustrative network agent-based model.
This is a FEASIBILITY pilot, not a causal human-vs-autonomous-AI comparison.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'glee_observed_negotiations_sample.csv'
OUT=ROOT/'results'


def load_data(path=DATA):
    df=pd.read_csv(path)
    assert df.id.is_unique
    df['feasible']=df.buyer>df.seller+1e-7
    df['valid_deal']=(df.deal==1)&df.feasible&df.price.ge(df.seller-1e-8)&df.price.le(df.buyer+1e-8)
    df['share']=np.where(df.valid_deal,(df.price-df.seller)/(df.buyer-df.seller).replace(0,np.nan),np.nan)
    df['source_path']=df.apply(lambda x: 'https://github.com/eilamshapira/GLEE/blob/master/Data/' + ('human_vs_llm' if x.type=='H' else 'llm_vs_llm') + '/negotiation/' + '/'.join(list(x.id[:3])) + '/'+x.id+'/game.csv',axis=1)
    return df


def empirical_summary(df):
    out=[]
    for regime,name in [('H','Human-LLM'),('A','LLM-LLM')]:
        d=df[df.type==regime];f=d[d.feasible];v=f[f.valid_deal]
        out.append(dict(regime=name,n_all=len(d),n_feasible=len(f),n_deals=int(f.deal.sum()),n_valid=int(v.valid_deal.sum()),valid_rate=float(v.shape[0]/max(len(f),1)),mean_rounds_valid=float(v.rounds.mean()),mean_seller_share=float(v.share.mean()),n_infeasible_deals=int(((~d.feasible)&(d.deal==1)).sum()),n_irrational_deals=int(((d.deal==1)&(~d.valid_deal)).sum())))
    res=pd.DataFrame(out)
    tab=[[int(res.iloc[0].n_valid),int(res.iloc[0].n_feasible-res.iloc[0].n_valid)],[int(res.iloc[1].n_valid),int(res.iloc[1].n_feasible-res.iloc[1].n_valid)]]
    odds,p=fisher_exact(tab)
    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT/'micro_summary.csv',index=False)
    pd.DataFrame([{'fisher_p_unadjusted':p,'odds_ratio':odds,'warning':'Non-random unmatched and small: p-value does NOT identify decision-maker effect.'}]).to_csv(OUT/'micro_exploratory_test.csv',index=False)
    return res


def posterior_config(df, rng):
    cfg={}
    for typ in ('H','A'):
        obs=df[(df.type==typ)&df.feasible]
        yes=obs.valid_deal.sum();no=len(obs)-yes
        valid=obs[obs.valid_deal]
        cfg[typ]={'p':float(rng.beta(yes+0.5,no+0.5)),
                  'rounds':valid.rounds.to_numpy(dtype=int),
                  'shares':valid.share.to_numpy(dtype=float)}
    return cfg


def simulate(regime: str,seed: int,df:pd.DataFrame,shock_strength=.65,relation_bonus=.6,T=100):
    """Two-tier, multi-buyer and multi-supplier synthetic ABM.

    Economic scenario draws identical for matched seed; negotiation outcomes vary
    by estimated dyad regimes (H-L and L-L). Not a validated industrial case.
    """
    rng=np.random.default_rng(seed)
    posterior_rng=np.random.default_rng(seed+987654321)
    cfg=posterior_config(df,posterior_rng)
    n_b,n_s=24,12
    base_cap=rng.uniform(12,19,size=n_s)
    base_cost=rng.uniform(6.8,9.2,size=n_s)
    valuation=rng.uniform(11.0,13.5,size=n_b)
    # Reserve identical streams across regimes for paired policy comparisons.
    base_dem=rng.poisson(5.3,size=(T,n_b)).astype(float)
    rel=np.zeros((n_b,n_s),float)
    for b in range(n_b):
        rel[b,rng.choice(n_s,3,replace=False)]=rng.uniform(.35,.70,size=3)
    tie_history=np.zeros((n_b,n_s),float)
    records=[]
    episode=None
    for t in range(T):
        # Shock to four suppliers, independent of negotiation regime.
        disrupt=40<=t<=54
        caps=base_cap.copy()
        if disrupt:
            caps[:4]*=(1-shock_strength)
        # Optional mild day-to-day capacity noise, common by seed and timestep.
        cap_rng=np.random.default_rng(seed*10007+t*61+14)
        caps=np.maximum(0,caps+cap_rng.normal(0,.8,n_s))
        demand=base_dem[t].copy()
        capacities=caps.copy()
        buying=np.zeros(n_s)
        received=np.zeros(n_b)
        allocated=np.zeros((n_b,n_s))
        value=0.;fees=0.;neg_rounds=[];offers=0;agreements=0
        buyers=np.random.default_rng(seed*999+7*t).permutation(n_b)
        for b in buyers:
            unmet=float(demand[b])
            if regime=='Full AI-AI':
                buyer_mode='A'
            elif regime=='Human-LLM mixed':
                buyer_mode='H'
            else:
                buyer_mode='A' if b<int(n_b*min(1.,t/max(T-1,1))) else 'H'
            # Fixed evaluation metric across regimes: price plus relational value.
            # Each buyer may contact up to 5 suppliers (same search scope).
            scores=(base_cost+1.15*(1-rel[b])+0.06*np.arange(n_s)/n_s-relation_bonus*rel[b])
            candidates=np.argsort(scores)[:5]
            for s in candidates:
                if unmet<=1e-9: break
                available=capacities[s]
                if available<1e-8: continue
                if valuation[b]<=base_cost[s]: continue
                offers+=1
                if rng.random() > cfg[buyer_mode]['p']:
                    rel[b,s]*=.96
                    continue
                amount=min(unmet,available)
                # Real micro-data only inform feasible agreements and time; no
                # invented LLM utterances are generated in the ABM.
                share=float(rng.choice(cfg[buyer_mode]['shares']))
                rounds=int(rng.choice(cfg[buyer_mode]['rounds']))
                price=base_cost[s]+share*(valuation[b]-base_cost[s])
                assert base_cost[s]-1e-7<=price<=valuation[b]+1e-7
                capacities[s]-=amount;buying[s]+=amount;received[b]+=amount
                allocated[b,s]+=amount;unmet-=amount
                value+=amount*price
                fees+=.08*rounds # illustrative friction cost per negotiation, *not* observed money
                neg_rounds.append(rounds);agreements+=1
                rel[b,s]=min(1.,rel[b,s]+.055)
                tie_history[b,s]+=amount
            # Unsuccessful relationships decay slightly.
            rel[b]*=.997
        assert np.all(capacities>=-1e-7) and np.all(received<=demand+1e-7)
        assert np.isclose(received.sum(),buying.sum(),atol=1e-6)
        missed=float((demand-received).sum());tot_dem=demand.sum()
        marketshare=buying/buying.sum() if buying.sum()>1e-8 else np.zeros(n_s)
        hhi=float((marketshare**2).sum()) if buying.sum()>1e-8 else np.nan
        weighted_ties=allocated>1e-6
        active_ties=int(weighted_ties.sum())
        rec={'regime':regime,'seed':seed,'t':t,'disrupted':int(disrupt),'demand':tot_dem,'delivered':float(received.sum()),'unmet':missed,
             'service':float(received.sum()/max(tot_dem,1)),'hhi':hhi,'contracted_qty':float(buying.sum()),
             'purchase_cost':value,'negotiation_friction':fees,'accounting_total':value+fees+missed*13.,
             'active_ties':active_ties,'mean_rounds':float(np.mean(neg_rounds)) if neg_rounds else 0,
             'attempts':offers,'agreements':agreements,'ai_buyer_share': 1. if regime=='Full AI-AI' else (0 if regime=='Human-LLM mixed' else min(1.,t/max(T-1,1))) }
        records.append(rec)
        if t==60: episode={'regime':regime,'seed':seed,'ties':(tie_history>0).astype(int),'volume':tie_history.copy()}
    return pd.DataFrame(records),episode


def main(reps=80):
    df=load_data(); micro=empirical_summary(df)
    regimes=['Human-LLM mixed','Gradual delegation','Full AI-AI']
    runs=[];episodes=[]
    for seed in range(reps):
        for regime in regimes:
            out,ep=simulate(regime,seed,df)
            runs.append(out)
            if seed==0: episodes.append(ep)
    df_runs=pd.concat(runs,ignore_index=True)
    df_runs.to_csv(OUT/'sim_trajectories.csv',index=False)
    # Entire period and shock period, per paired seed.
    out=[]
    for (rg,seed),sub in df_runs.groupby(['regime','seed']):
        for phase,frame in [('all',sub),('shock',sub[sub.disrupted==1]),('post',sub[sub.t>=55])]:
            out.append({'regime':rg,'seed':seed,'phase':phase,'service':frame.delivered.sum()/frame.demand.sum(),
            'hhi':float(frame.hhi.mean()),'active_ties':float(frame.active_ties.mean()),
            'friction_per_demand':frame.negotiation_friction.sum()/frame.demand.sum(),
            'system_cost_per_demand':frame.accounting_total.sum()/frame.demand.sum(),
            'nominal_procurement_per_delivered':frame.purchase_cost.sum()/max(frame.delivered.sum(),1),
            'undelivered_units':frame.unmet.sum()})
    reps_df=pd.DataFrame(out);reps_df.to_csv(OUT/'sim_replications.csv',index=False)
    def aggregate(g):
        x={}
        for col in ['service','hhi','active_ties','friction_per_demand','system_cost_per_demand','undelivered_units']:
            z=g[col].to_numpy()
            x[col+'_mean']=float(z.mean());x[col+'_ci_lo']=float(np.quantile(z,.025));x[col+'_ci_hi']=float(np.quantile(z,.975))
        return pd.Series(x)
    summary=reps_df.groupby(['regime','phase']).apply(aggregate,include_groups=False).reset_index()
    summary.to_csv(OUT/'sim_summary.csv',index=False)
    # True pairs: shared seeds and exogenous inputs. Difference CIs are simulation
    # variation and posterior propagated; no sampling-to-industries inference.
    paired=[]
    for phase in ['all','shock','post']:
        a=reps_df[(reps_df.regime=='Full AI-AI')&(reps_df.phase==phase)].set_index('seed')
        b=reps_df[(reps_df.regime=='Human-LLM mixed')&(reps_df.phase==phase)].set_index('seed')
        for k in ['service','hhi','system_cost_per_demand','active_ties']:
            delta=(a[k]-b[k]).to_numpy()
            paired.append({'phase':phase,'metric':k,'full_AI_minus_mixed_mean':delta.mean(),'q025':np.quantile(delta,.025),'q975':np.quantile(delta,.975)})
    pd.DataFrame(paired).to_csv(OUT/'paired_differences.csv',index=False)
    np.savez(OUT/'network_snapshots_seed0.npz',**{e['regime'].replace(' ','_')+'_vol':e['volume'] for e in episodes})
    # Run code/run_sensitivity.py separately for the small stress experiment.
    print('Observed micro data:');print(micro.to_string(index=False))
    print('\nSimulation summary (shock):');print(summary[summary.phase=='shock'][['regime','service_mean','hhi_mean','system_cost_per_demand_mean']].to_string(index=False))
    print('\nPaired differences (shock):');print(pd.DataFrame(paired).query("phase=='shock'").to_string(index=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reps',type=int,default=80)
    main(parser.parse_args().reps)
