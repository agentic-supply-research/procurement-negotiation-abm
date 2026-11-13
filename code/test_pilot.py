from pilot import load_data,simulate
import numpy as np
import pandas as pd

def main():
 d=load_data();assert len(d)==64
 assert len(d[d.type=='H'])==33 and len(d[d.type=='A'])==31
 assert d[d.feasible&d.valid_deal].shape[0]==20
 x,_=simulate('Full AI-AI',123,d,T=64)
 y,_=simulate('Full AI-AI',123,d,T=64)
 pd.testing.assert_frame_equal(x,y,check_exact=True)
 assert (x.delivered<=x.demand+1e-8).all()
 assert np.allclose(x.delivered+x.unmet,x.demand)
 assert x.hhi.dropna().between(0,1).all()
 assert x.service.between(0,1).all()
 assert x.disrupted.sum()==15
 print('PASS: source counts, valid data, deterministic replay, flow accounting, HHI, shock duration')
if __name__=='__main__':main()
