# Data dictionary

This document defines the research tables used by the released code. A **seed** is one stochastic realization of the synthetic procurement environment. The dyad labels describe the source bargaining dataset; they are not the identities of actors in a company.

## `data/glee_observed_negotiations_sample.csv`

| Column | Meaning |
|---|---|
| `type` | Source game group: `H` = human–LLM, `A` = LLM–LLM |
| `id` | GLEE source game identifier, used for provenance; not a participant identifier |
| `buyer` | Buyer's source-game reservation value |
| `seller` | Seller's source-game reservation cost |
| `price` | Last recorded agreed price, where available |
| `rounds` | Maximum observed negotiation round number |
| `deal` | Recorded acceptance event (0/1) before economic validity screening |
| `info` | Source game's complete-information setting (0/1) |
| `msg` | Source game's messaging-allowed setting (0/1) |

Computed fields: `feasible = buyer > seller`; `valid = deal == 1 and feasible and seller <= price <= buyer`; `seller_share = (price-seller)/(buyer-seller)` for valid deals only. Some recorded source agreements fail the economic validity screen.

## Primary `results/` tables

| File | Index / unit | Fields |
|---|---|---|
| `empirical_summary.csv` | source dyad | total, economically feasible and valid games; valid fraction; means of valid-deal rounds and seller share |
| `adaptive_trajectories.csv` | `(scenario, seed, t)` | `shock` flag, `demand`, `delivered`, `unserved`, `service`, `hhi`, `cost_per_demand`, component costs, `attempts`, `deals`, `n_ties`, `tie_retention`, `capacity_denials`, memory summaries and `seller_share` |
| `adaptive_replications.csv` | `(scenario, seed, phase)` | seed-level demand-weighted service and cost, time-averaged HHI, ties and retention, counts of attempts, deals and denials |
| `adaptive_summary.csv` | `(scenario, phase)` | across-seed means and empirical 2.5%/97.5% quantiles of the primary outcomes |
| `adaptive_paired.csv` | `(comparison, phase, metric)` | paired difference mean, empirical 2.5%/97.5% quantiles and number of seeds |
| `adaptive_sensitivity.csv` | `(variant, scenario)` | shock-window means for 12 seeds, plus all modified learning and shock parameters |
| `adaptive_snapshots_seed0.npz` | selected periods; seed 0 | trade-weight matrices; illustrative, not ensemble averages |

Phases: `pre` = 0–39, `shock` = 40–54, `post` = 55–99, `all` = 0–99.

## Emergent-network diagnostics

| File | Index / unit | Important fields |
|---|---|---|
| `emergent_link_trajectories.csv` | `(scenario, seed, t)` for t=30,…,99 | `supplier_tv`: supplier-flow-share total variation from 30–39 average; `active_edge_novelty`: share of current active edges absent from the reference set; `shock_new_volume_share`: volume on shock-activated reference-absent edges |
| `emergent_link_cohorts.csv` | `(scenario, seed, post_periods)` for k=1,…,30 | `n_shock_new`, `cumulative_reappearance`: proportion of shock-activated reference-absent edges seen again by the k-th recovery period |
| `emergent_link_phase_metrics.csv` | `(scenario, seed, phase)` | `flow_on_shock_new`, `supplier_tv`, `active_edge_novelty`, cohort count |
| `emergent_link_baseline_robustness.csv` | `(scenario, seed, baseline_window)` | reference windows 10, 20, 30 periods; cohort size, 15-period reappearance fraction, early-recovery delivered-volume share |

An edge counts as active when delivered quantity is positive. “Shock-activated” means traded during periods 40–54; “reference-absent” means unobserved during periods 30–39 (or in a specified alternative pre-shock window). These edges may have traded before that reference interval. A percentile interval over model replications is a simulation uncertainty summary, not an inferential estimate for human and LLM populations.
