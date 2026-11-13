"""Independent regression checks using the released data and simulation code."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from adaptive_abm import Config, SCENARIOS, aggregate, empirical_summary, micro_data, simulate


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=micro_data()

    def test_empirical_screen(self):
        s=empirical_summary(self.source).set_index('dyad')
        self.assertEqual(len(self.source),64)
        self.assertEqual((int(s.loc['Human--LLM','n_total']),int(s.loc['LLM--LLM','n_total'])),(33,31))
        self.assertEqual((int(s.loc['Human--LLM','n_feasible']),int(s.loc['LLM--LLM','n_feasible'])),(19,8))
        self.assertEqual((int(s.loc['Human--LLM','n_valid']),int(s.loc['LLM--LLM','n_valid'])),(13,7))
        self.assertTrue(self.source[self.source.valid].share.between(0,1).all())

    def test_replay_and_trading_observer(self):
        events=[]
        base,_=simulate(5,'A_adaptive',self.source)
        logged,_=simulate(5,'A_adaptive',self.source,edge_records=events)
        pd.testing.assert_frame_equal(base,logged,check_exact=True)
        self.assertEqual(len(events),100)
        for active,supplied,trades in events:
            self.assertEqual(active.shape,(24,12))
            np.testing.assert_allclose(trades.sum(axis=0),supplied,atol=1e-8)

    def test_regression_seed_against_saved_output(self):
        got,_=simulate(7,'H_adaptive',self.source)
        saved=pd.read_csv(ROOT/'results'/'adaptive_trajectories.csv')
        ref=saved[(saved.seed==7)&(saved.scenario=='H_adaptive')].sort_values('t').reset_index(drop=True)
        self.assertEqual(len(ref),100)
        for col in ('demand','delivered','unserved','service','hhi','cost_per_demand','n_ties','deals','attempts','tie_retention'):
            np.testing.assert_allclose(got[col],ref[col],rtol=1e-11,atol=1e-11,equal_nan=True,err_msg=col)

    def test_accounting_and_symmetric_control(self):
        cfg=Config(alpha=0)
        for ty in ('H','A'):
            fixed,_=simulate(8,f'{ty}_fixed',self.source,cfg)
            feedback_off,_=simulate(8,f'{ty}_adaptive',self.source,cfg)
            np.testing.assert_array_equal(fixed.delivered,feedback_off.delivered)
            np.testing.assert_allclose(fixed.delivered+fixed.unserved,fixed.demand,atol=1e-8)
            self.assertTrue(fixed.service.between(0,1).all())
            self.assertTrue(fixed.hhi.between(0,1).all())
            self.assertEqual(int(fixed.shock.sum()),15)


if __name__=='__main__': unittest.main()
