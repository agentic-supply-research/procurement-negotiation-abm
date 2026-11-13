# Theoretical foundations and model traceability

This note accompanies *Relational Decisions in Agentic Supply Networks: A Negotiation-Informed Agent-Based Study* (13 November 2026). It explains what is derived from theory, what is measured, and what is a chosen simulation representation.

## 1. Problem and contribution

The research question is how transferring authority for relational procurement decisions to LLM agents might change long-run trading relationships and a capacity-constrained supply network, even if everyone uses the same resource-allocation and candidate-ranking rule.

The implemented proof-of-mechanism includes both buyers and suppliers as independent contract-decision entities. Observed negotiation data distinguish **human–LLM** and **LLM–LLM** games, not human-managed and AI-managed industrial networks. A future matched experiment is necessary to identify the latter counterfactual.

## 2. Two decision layers

| Layer | What is decided | Decision representation | Relation to data |
| --- | --- | --- | --- |
| Structured operational | Demand, available supplier capacity, reservation values, feasible quantities | Greedy shortlist, capacity and accounting constraints | Completely synthetic operational setting |
| Relational/bargaining | Buyer acceptance; supplier acceptance; agreement terms; whether contact continues | Two Bernoulli decisions with conditional price and round draws | **Joint** agreement rate, price share and rounds drawn from GLEE; role split assumed |
| Experience and relationship | What to expect from this partner on the next encounter | Recency-weighted buyer/supplier scores and evolving familiarity | Designed feedback mechanism; not learned from GLEE |
| Network consequences | Which ties are active, how much demand is served, concentration, cost | Emergent ABM output | Simulated, not observed |

## 3. Source evidence versus decisions

**Source records**: 33 human–LLM games (19 surplus-feasible, 13 valid deals); 31 LLM–LLM games (eight surplus-feasible, seven valid deals). Valid agreements imply seller reservation cost <= agreed price <= buyer value. The conditional agreement fractions are 0.684 and 0.875; mean rounds are 1.46 and 4.14; mean normalized seller surplus shares are 0.438 and 0.565.

**Estimated probability**: A Jeffreys-prior beta-binomial posterior uses `Beta(a + 0.5, n - a + 0.5)` for each game class (Jeffreys 1946). Price shares and rounds are sampled separately from observed valid games. This is an uncertainty model, not role-level inference.

**Bilateral factorization**: `sqrt(p)` is the equal buyer/supplier baseline acceptance probability chosen so that *independent* Bernoulli outcomes have product `p`. This is not identified from GLEE; other factorizations are equally compatible with the joint data.

## 4. Theoretical-to-mathematical mapping

| Paper mechanism | Theoretical rationale and citation | What the study actually implements |
| --- | --- | --- |
| Repeated partner links produce a network | Complex-adaptive systems view of supply networks: Choi et al. (2001), DOI [10.1016/S0272-6963(00)00068-1](https://doi.org/10.1016/S0272-6963(00)00068-1) | Feasible contracts generate period-specific and cumulative buyer–supplier edges |
| Limited search and feasible sourcing | Bounded rationality: Simon (1955), DOI [10.2307/1884852](https://doi.org/10.2307/1884852) | Buyer ranks at most five suppliers by a specified score; coefficient values are assumed |
| Partner familiarity matters | Relational governance complementing formal contracts: Poppo and Zenger (2002), DOI [10.1002/smj.249](https://doi.org/10.1002/smj.249) | Familiarity weight `w` enters sourcing score and updates after success/failure |
| Experience modifies future propensity to agree | Experience-weighted choice: Camerer and Ho (1999), DOI [10.1111/1468-0262.00054](https://doi.org/10.1111/1468-0262.00054) | Logistic acceptance model with a recency-weighted memory score. **Not the estimated EWA model of Camerer and Ho** |
| Exploiting known partners can reduce future diversity | Exploration/exploitation: March (1991), DOI [10.1287/orsc.2.1.71](https://doi.org/10.1287/orsc.2.1.71) | Supplier ranking gives preference to past experience; no separate formal exploration policy |
| Uncertain agreement prevalence | Jeffreys (1946), DOI [10.1098/rspa.1946.0056](https://doi.org/10.1098/rspa.1946.0056) | Posterior `Beta(a+0.5,n-a+0.5)` sampled per replication |
| Disruption propagates through dependencies | Supply-chain resilience and disruption analysis: Ivanov (2020), DOI [10.1016/j.tre.2020.101922](https://doi.org/10.1016/j.tre.2020.101922) | Controlled 65% capacity reduction at four suppliers over periods 40–54 |

The citations justify **modeling mechanisms**, not the chosen numerical values. The partner reward parameters, the familiarity changes, and the allocation of joint agreement probabilities across roles are explicitly assumed. Those would need estimation in repeated human/LLM procurement experiments.

## 5. Situation-specific mechanism

1. **Ordinary feasible procurement:** The buyer evaluates a common sourcing score; each side independently accepts with baseline `sqrt(p)` modified by its partner score; a successful negotiation transfers capacity-limited quantity at an economically valid price.
2. **Failed agreement:** There is no transfer. Familiarity weakens, and the two partner scores receive a negative experience signal if feedback is enabled. The buyer proceeds to another eligible supplier.
3. **Insufficient capacity:** The buyer cannot obtain a feasible contract from that supplier, and (in feedback-on scenarios) records an availability denial; supplier memory is not updated by a non-negotiation.
4. **Successful contract:** Volume is transferred; price depends on the observed seller surplus-share distribution. Both parties update their memories and the familiarity link strengthens.
5. **Capacity shock:** A fixed group of suppliers loses 65% of base capacity over 15 periods. Competing buyers adjust their links through the same rules; the aggregate outcome is measured, not imposed.
6. **Next period:** Exogenous demand and capacity noise are realized. Partner history is carried forward and can redirect supplier ranking and the probability of mutual acceptance.

## 6. Scientific interpretation

An LLM can use persistent memory, external tools, or fine-tuning, but does not automatically update its parameters after every negotiation. Here adaptation occurs through **explicit numerical state**. The model can later substitute actual logged human decisions and live LLM calls for the policy module, provided action validity, tool permissions, reproducibility and independent behavioral validation are controlled.

## 7. Reproducibility linkages

- Bayesian kernel: `code/adaptive_abm.py::kernels()`.
- Common exogenous setup: `code/adaptive_abm.py::setup()`.
- Firm decisions, memory, contracts: `code/adaptive_abm.py::simulate()`.
- Micro-level extracted data: `data/glee_observed_negotiations_sample.csv`.
- Figure generation: `code/draw_revised_figures.py`.
- Full model details: `docs/ODD_protocol.md`.
- Results: `results/adaptive_summary.csv`, `results/adaptive_paired.csv`, and `results/adaptive_sensitivity.csv`.

The original GLEE benchmark is https://arxiv.org/abs/2410.05254 .
