"""Smoke/regression and accounting checks for learning ABM."""
from dataclasses import replace
import numpy as np
from adaptive_abm import Config, empirical_summary, micro_data,simulate,aggregate,kernels


def test():
    df=micro_data()
    a=empirical_summary(df)
    assert a.n_total.tolist()==[33,31]
    assert a.n_feasible.tolist()==[19,8]
    assert a.n_valid.tolist()==[13,7]
    assert len(kernels(df,10)['H']['share'])==13
    cfg=Config(periods=100,alpha=0.)
    x,_=simulate(7,'H_fixed',df,cfg)
    y,_=simulate(7,'H_adaptive',df,cfg)
    assert np.allclose(x.service,y.service)
    assert np.allclose(x.cost_per_demand,y.cost_per_demand)
    x2,_=simulate(7,'A_fixed',df,cfg)
    y2,_=simulate(7,'A_adaptive',df,cfg)
    assert np.allclose(x2.service,y2.service)
    assert np.allclose(x2.cost_per_demand,y2.cost_per_demand)
    assert (x.unserved>=-1e-8).all()
    assert np.allclose(x.delivered+x.unserved,x.demand)
    assert np.allclose(x.shock.values, np.r_[[0]*40,[1]*15,[0]*45])
    # Regression with fixed streams and seed: bitwise exact repeat
    z,_=simulate(7,'A_adaptive',df,Config())
    zz,_=simulate(7,'A_adaptive',df,Config())
    assert z.equals(zz)
    assert z.deals.le(z.attempts).all()
    assert z.service.between(0,1).all()
    assert z.hhi.between(0,1).all()
    print('All accounting, paired-control, data and reproducibility tests passed.')

if __name__=='__main__': test()
