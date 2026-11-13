# Interpreting the saved results

The curated output files use 80 matched seeds for four policy configurations. The principal scientific question is how different negotiation-outcome kernels affect the **evolution of simulated buyer–supplier relations** under identical external procurement conditions.

## Observational calibration

| Source negotiation dyad | Total games | Feasible games | Valid agreements | Valid fraction | Rounds in valid deals (mean) | Seller surplus share (mean) |
|---|---:|---:|---:|---:|---:|---:|
| Human–LLM | 33 | 19 | 13 | 0.6842 | 1.4615 | 0.4378 |
| LLM–LLM | 31 | 8 | 7 | 0.8750 | 4.1429 | 0.5653 |

These are conditional descriptive statistics from a small, non-random dataset, not causal differences between human and LLM policies.

## Emergent link analysis

The reference is the set of trading links used at least once in periods 30–39. Shock-activated links absent in that window are tracked during the subsequent 30 periods. Cohort reactivation and delivered volume on those links capture two dimensions of network adjustment. The immediate 15-period recovery horizon is emphasized in the article, while 10/20/30-period pre-shock reference windows are assessed in `emergent_link_baseline_robustness.csv`.

The simulated network can retain changes after supplier capacity is restored, because repeated encounters alter partner familiarity and/or experience-dependent sourcing. These effects are features of the specified model and its synthetic environment; their magnitudes do not predict how a real LLM-operated industrial supply chain would behave. See `docs/EMERGENT_NETWORK_ANALYSIS.md` for equations and summary values.
