# ODD model description: Delegating Procurement Negotiations to LLM Agents

**Model:** Negotiation-informed procurement network, implementation v2.0  
**Date:** 13 November 2026  
**Reference implementation:** `code/adaptive_abm.py`  
**Simulation files:** `results/adaptive_*.csv`  
**Reporting convention:** Grimm et al. (2020), *Journal of Artificial Societies and Social Simulation*, 23(2), 7, https://doi.org/10.18564/jasss.4259

This document describes the implemented model at a level intended to make its decisions, inputs and interpretation reproducible. The model links recorded bargaining outcomes to repeated procurement in a capacity-constrained buyer–supplier network. The available observations describe human–LLM and LLM–LLM bargaining pairs. They inform the joint outcome of a negotiation, while the model specifies how individual buyers and suppliers use those outcomes and learn from subsequent trade. The distinction is important when interpreting the results or extending the framework to autonomous LLM executions.

## 1. Purpose and patterns

### Purpose

The model explores how negotiation behavior can affect an evolving supply network even when the operational rules used to rank suppliers and allocate feasible quantities remain the same. Procurement involves a sequence of decisions. A buyer identifies an eligible partner; the buyer and supplier respond to an opportunity; a contract is formed or declined; and the outcome becomes part of their history. As these encounters accumulate, buyers may approach different suppliers and the network may become more or less concentrated. The model follows these consequences across repeated periods and during a temporary loss of supplier capacity.

This is a controlled computational study of decision mechanisms. Its physical network, costs, capacities and experience updates are synthetic. Two distributions of negotiation outcomes are informed by published GLEE recordings: interactions between a human and an LLM, and interactions between two LLMs. A comparison between fully human and fully autonomous supply networks is the larger research question motivating this work; it requires role-specific observations that are unavailable in the current sample.

### Patterns examined

The empirical patterns are the fraction of economically executable agreements, the number of rounds in completed negotiations, and the division of bargaining surplus between buyer and seller. At the network level we measure the fraction of demand served, cost per unit of demand under an illustrative accounting rule, the concentration of supplier deliveries, the number and persistence of trading links, and the response to a common capacity disruption. The simulated patterns are consequences of the implemented rules and stochastic inputs.

## 2. Entities, state variables and scales

The network contains 24 buyers and 12 suppliers. Each simulated period represents one procurement cycle. A contract, when formed, is fulfilled in the same cycle. No geographical distance, inventory carryover or production lead time is represented.

| Entity | State and decisions | Scale |
|---|---|---|
| Buyer `i` | Demand `d_i(t)`, reservation value `v_i`, familiarity with suppliers `w_ij`, and an assessment `qB[i,j]` of each supplier. Ranks up to five suppliers and makes a bilateral acceptance decision. | 24 agents |
| Supplier `j` | Reservation cost `c_j`, realized capacity `C_j(t)`, remaining capacity after prior contracts, and an assessment `qS[j,i]` of each buyer. Responds independently to a proposed contract. | 12 agents |
| Trading relation `(i,j)` | Contracted quantity during the current period, cumulative quantity, familiarity score, and current/previous-period activity. | Up to 288 dyads |
| Bargaining-outcome kernel `g` | Joint feasible-agreement probability and empirical distributions of completed-deal rounds and seller surplus share. | Human–LLM (`H`) or LLM–LLM (`A`) |
| Environment | Demand, supplier capacity variation, buyer processing order and a prescribed disruption. | 100 periods |

All scenarios use buyers and suppliers as decision-making agents. The model's policy label indicates which source of bargaining outcomes is used; it does not label an implemented buyer as a live LLM or as an experimentally observed human. This matters because the source identifies agreements at the dyad level, not independent decisions made by both roles.

## 3. Process overview and scheduling

Each period begins with a new demand vector and updated supplier capacities. A common random order determines the sequence in which buyers act. A buyer ranks the available supplier candidates using the specified sourcing score. It considers the five lowest-scoring suppliers in order, stopping once its demand is met or its shortlist is exhausted.

A contact first passes the valuation and capacity checks. An unavailable supplier cannot deliver; in the adaptive settings, the buyer also records the capacity denial in its partner assessment. For an eligible contact, buyer and supplier independently accept or decline according to the model's role-specific policy. Agreement leads to a feasible delivery, a price obtained from the bargaining kernel and an update of each party's partner history. A failed negotiation changes the corresponding relationship states and sends the buyer to the next candidate.

At the end of the buyer's actions, familiarity is slightly reduced through a common decay factor. After every buyer has acted, the model records material flows, costs, supplier shares and trading links. The process repeats for 100 periods. During periods `t=40,...,54` the first four suppliers experience a 65% reduction in base capacity before period-specific capacity noise is applied.

Processing is sequential: buyers compete for finite capacity, so an earlier contract may prevent a later buyer from dealing with the same supplier. All scenarios with a shared simulation seed receive the same exogenous demand, capacity disturbances and buyer ordering.

## 4. Design concepts

### Basic principles and emergence

The supply-network representation draws on complex adaptive systems: aggregate network structure emerges from individual decisions under shared resource constraints (Choi et al., 2001; Bonabeau, 2002). Each contract is locally feasible, yet the collection of successful contracts can concentrate trade in some suppliers and leave other demand unmet. The evolving network is an output of decentralized exchange.

### Objectives and bounded search

A buyer seeks to satisfy its demand through a shortlist of relatively attractive suppliers. Its score combines a supplier's unit cost, relationship familiarity, a small deterministic tie-breaker and, in adaptive scenarios, experience with that supplier. This is a limited-search decision procedure in the sense of Simon's bounded rationality; the model does not calculate an optimal system-wide assignment. A supplier considers feasible incoming opportunities and makes an acceptance decision using its own partner assessment. Contract quantities still obey physical demand and capacity limits.

### Adaptation and memory

The model contains two related forms of relationship state. Familiarity `w` changes after successful and unsuccessful contacts and operates in every scenario. The optional partner assessments `qB` and `qS` are updated by recency-weighted feedback from an encounter. These assessments affect both buyer ranking and the two parties' acceptance propensities. The recency-weighted form is motivated by experience-based choice and adaptive learning (Camerer and Ho, 1999; March, 1991). The numerical feedback coefficients are experimental assumptions chosen for transparent mechanism tests.

A stateful policy provides a useful representation of how remembered interactions might alter a future action. In this implementation the policy is a probabilistic decision rule. No LLM is called during a simulated procurement period, and no language-model weights are updated. A future direct-LLM implementation would require explicit persistent memory and a controlled prompt/tool environment.

### Sensing, interaction and uncertainty

Buyers know their demand, valuation, the ranking inputs assigned to them and what happened during their own supplier contacts. Suppliers know their capacity, cost and their history with a contacting buyer. They do not receive a globally shared table of every firm's partner assessments. Negotiation is represented by bilateral acceptance draws and, when successful, sampled contract terms. Supplier capacity couples otherwise separate buyer decisions.

Uncertainty enters through stochastic demand, heterogeneous costs and capacities, capacity noise, buyer action order, bargaining probabilities, and sampling of contract price share and duration. The simulation makes these components traceable to either a source record, a probability model or an explicit input assumption.

### Observation and collectives

The set of active buyer–supplier ties is the principal collective object. The model records period-level service, HHI, tie persistence, total active ties, negotiation attempts, deals, capacity denials, and buyer and supplier experience averages. There is no centralized coalition or joint bargaining organization.

## 5. Initialization

For each random seed, suppliers receive independent unit costs drawn from `Uniform(6.8, 9.2)` and base capacities from `Uniform(12, 19)`. Buyers receive reservation values from `Uniform(11, 13.5)`. Buyer demands are drawn independently for each period from `Poisson(5.3)`. Supplier capacity varies each period by independent normal noise with standard deviation `0.8`, then is constrained to be nonnegative.

Each buyer begins with familiarity links to three randomly selected suppliers; their initial weights are drawn from `Uniform(0.35, 0.70)`. Other familiarity entries begin at zero. Both buyer and supplier partner-assessment matrices begin at zero. The initial trade network has no accumulated deliveries. The same seed initializes the same operational environment in each scenario.

The negotiation kernel is drawn once per replication for each observed dyad class. The associated source records provide the set of completed-deal round counts and seller surplus shares from which the model subsequently samples.

## 6. Input data

### The bargaining observations

`data/glee_observed_negotiations_sample.csv` contains 64 selected negotiation logs from the GLEE public benchmark (Shapira et al., 2024). Its `type` field indicates human–LLM (`H`) or LLM–LLM (`A`) dyads. The recorded fields include participant reservation values, agreement status, final price and negotiation rounds. The source selection is a convenience sample and the two sets of games are not experimentally matched.

The extraction step classifies an opportunity as economically feasible when buyer valuation exceeds seller reservation cost. A completed deal is valid for simulated contracting when the recorded price lies between those two values. Table 1 reports the source quantities used for the behavioral kernel.

| Quantity | Human–LLM | LLM–LLM |
|---|---:|---:|
| Negotiation games | 33 | 31 |
| Positive-surplus opportunities | 19 | 8 |
| Economically valid completed deals | 13 | 7 |
| Observed valid-agreement proportion | 0.684 | 0.875 |
| Mean rounds, completed valid deals | 1.462 | 4.143 |
| Mean seller surplus share, valid deals | 0.438 | 0.565 |

For dyad class `g`, let `a_g` denote valid deals and `n_g` positive-surplus opportunities. At the beginning of each replication we draw a joint agreement probability from the Jeffreys-prior posterior:

`p_g ~ Beta(a_g + 0.5, n_g - a_g + 0.5)`.

A successful simulated contract receives a seller surplus share `z` and a round count independently sampled with replacement from their respective valid-deal observations in the appropriate class. Thus the observed marginal distributions are preserved but a possible dependence between duration and surplus share is not modeled. The valid agreement price is then `P_ij = c_j + z(v_i - c_j)` with `0 <= z <= 1`.

### Synthetic system inputs

The population sizes, demand distributions, capacity shock, relationship-update rates, shortage penalty and sourcing weights come from `code/adaptive_abm.py`, chiefly its `Config` dataclass. They represent an experimental environment. The bargaining records alone do not identify supplier loyalty, contract fulfillment, individual role probabilities, capacity disclosure or learning rates.

## 7. Submodels

### 7.1 Supplier search

Buyer `i` ranks suppliers using

`R_ij(t) = c_j + 1.15(1 - w_ij(t)) - 0.60 w_ij(t) + 0.06 j/S - gamma qB[i,j](t)`.

The five lowest-scoring suppliers form the buyer's ordered shortlist. `w_ij` is familiarity and `qB` is the buyer's experience assessment. `gamma=0.75` when additional experience feedback is active, and zero otherwise. Identical functional forms and coefficients are used across the two bargaining-data classes; their evolving states can differ after contracts are realized.

### 7.2 Two-sided acceptance

Each positive-surplus contact with available capacity reaches a buyer and a supplier decision. The observed source record describes only whether the dyad reaches agreement. To generate two decisions whose independent baseline success probability equals `p_g`, the model assigns each side the baseline propensity `sqrt(p_g)`. It then uses a logistic response to the relevant partner assessment:

`piB_ij(t) = sigmoid(logit(sqrt(p_g)) + 1.10 qB[i,j](t))`

`piS_ji(t) = sigmoid(logit(sqrt(p_g)) + 1.10 qS[j,i](t))`.

A deal requires both Bernoulli decisions to accept. The square-root factorization is an identification assumption: many different buyer and supplier propensities could yield the same observed joint agreement rate. Learning separate role policies requires observations of role-specific offers, responses and refusals. In the fixed-feedback diagnostic, the additional experience terms remain at zero, although common familiarity continues to evolve.

### 7.3 Outcome-based updates

After a successful deal, the buyer receives feedback `uB = 1 - 0.60 z` and the supplier `uS = 0.40 + 0.60 z`. Failed bilateral acceptance assigns `-0.65` to both sides. An exhausted supplier assigns `-0.90` to the buyer alone, as no bargaining decision takes place at that contact. These scores express the modeled value of outcomes; they are not observations of psychological trust.

When feedback is enabled, each partner assessment is updated as

`q_next = (1 - alpha) q_previous + alpha u`, with `alpha=0.18`.

This recency-weighted update can change future acceptance and partner ranking. The feedback strengths (`1.10` in acceptance and `0.75` in ranking) are specified for mechanism tests. The `fixed` and `adaptive` condition names in the code distinguish feedback components; they do not imply that a deployed LLM necessarily has or lacks persistent experience.

### 7.4 Familiarity and network change

Successful trade increases buyer familiarity with the contracted supplier by `0.055`, capped at one. An unsuccessful negotiation multiplies the relevant familiarity score by `0.96`. After the buyer has completed its contacts for a period, its familiarity scores are multiplied by `0.997`. Each executed quantity adds to the cumulative volume of the associated network edge. Thus the trading network changes as a product of acceptance and capacity competition.

### 7.5 Contract execution

With remaining buyer demand `d_remaining` and supplier capacity `C_remaining`, an accepted contract transfers

`x_ij = min(d_remaining, C_remaining)`.

Both budgets are reduced by this amount. A purchase is executed only when buyer reservation value exceeds supplier cost; the sampled normalized surplus share ensures the resulting price stays inside the feasible interval. All accepted quantities arrive within the current period. The model has no lead time, inventory carryover or renegotiation after a missed delivery.

### 7.6 Output indicators

- **Service:** total delivered quantity divided by realized demand.
- **Supplier HHI:** sum of squared supplier shares in total delivered volume for the period; undefined if delivery is zero.
- **Trading ties:** number of buyer–supplier pairs with positive delivered quantity during the period.
- **Tie retention:** fraction of the previous period's active trading pairs that are also active this period; undefined when there are no previous ties.
- **Illustrative cost:** sum of purchase spending, `0.08` per round for executed contracts, and `13` per unit of unmet demand, divided by total demand.

The monetary weights are illustrative. Service and cost are aggregated over periods using demand weights; supplier HHI and tie retention are time-averaged within a replication.

**Emergent network diagnostics.** The analysis also retains the binary buyer–supplier trading matrix and supplier-level delivery totals in each period. For every simulation seed and behavioral kernel, the reference network comprises links used at least once in periods 30–39. The reference supplier-share vector is the mean of the ten period-level share vectors. The total-variation distance between the supplier shares in period `t` and this reference is `0.5 × sum_j abs(share_j(t) − mean_share_j(30:39))`. The nonbaseline-link share is the proportion of active links in period `t` that do not belong to the reference network. Both quantities describe a change in the distribution of realized exchange, not a change in the exogenous supplier population.

To examine the lasting role of links activated during disruption, we define a cohort of buyer–supplier pairs that trade at least once in periods 40–54 but are absent throughout periods 30–39. For recovery horizon `k`, cumulative reactivation is the fraction of this cohort that trades at least once in periods `55` through `54+k`. We also record the fraction of delivered volume conducted on these links in early recovery (55–69) and later recovery (70–99). These links are new relative to the selected reference window; they are not necessarily the first transactions between those firms in the entire simulation. A longer 20- or 30-period reference produces the same direction of the reactivation contrast. None of these measurements requires an additional behavioral rule or affects the model's decisions.

### 7.7 Experimental conditions and verification

The main experiment uses 80 matched seeds for the four internal scenario codes `H_fixed`, `H_adaptive`, `A_fixed` and `A_adaptive`. The primary comparison holds the partner-history mechanism fixed and changes the source bargaining kernel from `H` to `A`. Feedback-off runs serve as mechanism diagnostics. A separate 12-seed sensitivity set changes feedback channels and learning parameters. Each run lasts 100 periods, with a 15-period capacity disruption beginning at period 40. Individual run differences are paired by seed before aggregation.

The tests in `code/test_adaptive_abm.py` check reproducibility, feasible transfers, material-flow conservation, price bounds and scenario consistency. The optional `edge_records` output in `simulate()` creates a record of realized links without consuming random numbers or changing a decision. Network diagnostics are calculated from 80 matched human–LLM-derived and LLM–LLM-derived simulations with feedback active. The plotting code uses only these saved diagnostics. The plotted 2.5th and 97.5th percentiles summarize the distribution of matched simulation differences; they are not sampling-based causal confidence intervals for differences between human and AI decision makers.

## Reproduction and interpretation

From the project root, install the packages in `requirements.txt` and run:

```bash
python code/test_adaptive_abm.py
python code/adaptive_abm.py --reps 80
python code/plot_grayscale_framework.py
python code/regenerate_grayscale_results.py
python code/analyze_emergent_links.py
python code/plot_emergent_links.py
```

If output files already exist, preserve them before re-running the simulation. The simulation commands may take time, depending on the environment. The source CSV and calibration procedure are described in `docs/DATA_PROVENANCE.md` and `code/extract_glee_local.py`.

The most consequential extension is to estimate both sides' relational policies from repeated, matched procurement negotiations in human–human, human–AI, AI–human and AI–AI assignments. Future records should contain offers, counteroffers, disclosed capacity, fulfilled commitments, rejected proposals, concessions and partner renewal decisions. Such observations would allow role-specific policies to be validated outside the data used to estimate them, then placed within an operationally calibrated network. The intended live-agent integration is documented separately in `docs/LIVE_AGENT_EXTENSION.md`; it is an interface proposal and has not generated the reported experiments.

## Selected methodological references

- Bonabeau, E. (2002). Agent-based modeling: Methods and techniques for simulating human systems. *Proceedings of the National Academy of Sciences*, 99(suppl. 3), 7280–7287. https://doi.org/10.1073/pnas.082080899
- Camerer, C., & Ho, T.-H. (1999). Experience-weighted attraction learning in normal form games. *Econometrica*, 67(4), 827–874. https://doi.org/10.1111/1468-0262.00054
- Choi, T. Y., Dooley, K. J., & Rungtusanatham, M. (2001). Supply networks and complex adaptive systems: Control versus emergence. *Journal of Operations Management*, 19(3), 351–366. https://doi.org/10.1016/S0272-6963(00)00068-1
- Grimm, V., et al. (2020). The ODD protocol for describing agent-based and other simulation models: A second update to improve clarity, replication, and structural realism. *JASSS*, 23(2), 7. https://doi.org/10.18564/jasss.4259
- March, J. G. (1991). Exploration and exploitation in organizational learning. *Organization Science*, 2(1), 71–87. https://doi.org/10.1287/orsc.2.1.71
- Poppo, L., & Zenger, T. (2002). Do formal contracts and relational governance function as substitutes or complements? *Strategic Management Journal*, 23(8), 707–725. https://doi.org/10.1002/smj.249
- Shapira, E., et al. (2024). GLEE: A unified framework and benchmark for language-based economic environments. arXiv:2410.05254. https://arxiv.org/abs/2410.05254
