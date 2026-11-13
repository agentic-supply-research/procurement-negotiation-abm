# Experimental design and parameter specification

## Modelled procurement environment

A single-tier network contains 24 buying agents and 12 capacity-constrained supplying agents. The model advances through 100 discrete procurement periods. Buyer demand is drawn each period, and supplier costs and buyer values are drawn once per replication. During periods 40–54 inclusive, four suppliers experience a 65% reduction in their base capacity before additive random capacity noise.

All scenarios use identical supplier-ranking functional forms and quantity-feasibility checks. Buyers and suppliers make separate stochastic acceptance decisions; successful proposals result in immediate within-period deliveries. The environment is a stylized model, with no industrial data used to calibrate demand, production, transport, or inventory dynamics.

## Scenario labels

| Source dyad | Fixed additional experience feedback | Experience-based feedback active |
|---|---|---|
| Human–LLM negotiated outcomes | `H_fixed` | `H_adaptive` |
| LLM–LLM negotiated outcomes | `A_fixed` | `A_adaptive` |

These are **simulated policies calibrated on dyad outcomes**, not experiments with a human-operated supply chain or live LLM-based agents. Both fixed and adaptive scenarios retain a common evolving familiarity score. The role-specific partner assessments are active only for adaptive settings. The main behavioral comparison holds feedback mode constant and changes the source dyad kernel.

## Numerical inputs

| Quantity | Symbol / implementation | Value | Provenance |
|---|---|---|---|
| Buyers | `Config.buyers` | 24 | Synthetic |
| Suppliers | `Config.suppliers` | 12 | Synthetic |
| Periods | `Config.periods` | 100 | Synthetic |
| Main paired seeds | `--reps` | 80 (0–79) | Experiment design |
| Sensitivity paired seeds | `--seeds` | 12 (0–11) | Experiment design |
| Supplier base capacity | `cap` | Uniform(12,19) | Synthetic |
| Supplier unit reservation cost | `cost` | Uniform(6.8,9.2) | Synthetic |
| Buyer value | `val` | Uniform(11,13.5) | Synthetic |
| Buyer period demand | `demand` | Poisson(5.3) | Synthetic |
| Supplier capacity noise | `cap_noise` | Normal(0,0.8) | Synthetic |
| Initially familiar suppliers per buyer | `init_rel` | 3 | Synthetic |
| Initial familiarity | `init_rel` | Uniform(0.35,0.70) | Synthetic |
| Shock-affected suppliers | `caps[:4]` | first 4 by index | Synthetic |
| Shock period | `[40,55)` | 40–54 inclusive | Synthetic |
| Capacity reduction | `Config.shock_strength` | 0.65 | Synthetic |
| Buyer shortlist | `Config.max_candidates` | 5 | Synthetic |
| Familiarity ranking coefficients | `1.15`, `relationship_bonus` | 1.15, 0.60 | Model assumption |
| Relationship increase on success | `rel` update | +0.055 | Model assumption |
| Relationship reduction on failure | `rel` update | ×0.96 | Model assumption |
| Familiarity decay per buyer period | `rel` update | ×0.997 | Model assumption |
| Memory recency weight | `Config.alpha` | 0.18 | Model assumption |
| Acceptance log-odds sensitivity | `Config.policy_gain` | 1.10 | Model assumption |
| Ranking sensitivity to memory | `Config.rank_gain` | 0.75 | Model assumption |
| Failed-negotiation feedback | `q_b`, `q_s` | −0.65 | Model assumption |
| Capacity-denial feedback to buyer | `q_b` | −0.90 | Model assumption |
| Unserved-demand penalty | `Config.unmet_penalty` | 13 per unit | Illustrative accounting |
| Negotiation cost | `Config.negotiation_cost_per_round` | 0.08 per completed-deal round | Illustrative accounting |
| Joint agreement prior | `kernels()` | Beta(n_valid+0.5, n_feasible−n_valid+0.5) | Estimated from observed games |
| Conditional rounds & seller share | `kernels()` | Sampled with replacement from valid deals | Observed extract |
| Buyer/supplier probability decomposition | `simulate()` | sqrt(p) for each role | Identification assumption |

Additional feedback payoff functions, sorting tie-breakers, and random number stream definitions are given in the [ODD protocol](ODD_protocol.md). They are implemented explicitly in `code/adaptive_abm.py`.

## Outcomes and controls

Measured outcomes are service level, demand-normalized illustrative cost, supplier delivery HHI, active trading ties, one-period link retention, agreement attempts and successes, capacity denials, trading-link novelty, supplier-share reallocation, and recovery-period reuse of shock-activated links.

The paired design uses the same exogenous seed for all four scenarios; joint agreement parameter draws share a seed but follow the separate GLEE kernels. Differences are sample- and model-dependent. They do not estimate a causal effect of replacing human procurement personnel with autonomous LLM systems.
