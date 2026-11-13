# Network reallocation and tie reactivation

This note documents the two additional result figures reported in the 12-page manuscript. Both measure emergent network properties produced by the existing, capacity-constrained procurement model. No LLM calls or new bargaining observations were made.

## Source and replication

Run `python code/analyze_emergent_links.py` from the repository root. For each of the 80 seeds, the script replays both active-feedback negotiation policies (`H_adaptive` and `A_adaptive`) with the same random streams as the recorded main experiment. The optional trading-edge observer records a binary 24 × 12 matrix and supplier deliveries in each of 100 periods. Replaying the system makes these measures available for all seeds, whereas the old supplementary trade matrices were saved for seed 0 only. `python code/plot_emergent_links.py` produces vector PDFs and SVGs and 600 DPI PNGs.

## Operational definitions

For each seed and regime, define the reference set `E_pre` as all buyer–supplier edges with a positive transfer at least once in periods 30–39. Define the supplier reference shares `q0` as the average of daily shares over the same window. Figure 4 in the updated article shows `TV_t = 0.5*sum(abs(q_t-q0))` and the fraction of period-`t` active edges absent from `E_pre`. Lines are five-period rolling means across 80 seeds; shaded regions show 95% pointwise bootstrap intervals of the mean over seeds. The shaded disruption runs from period 40 through 54.

Define the shock-activated, baseline-absent set `E_new = (union of edges traded during periods 40–54) \ E_pre`. Figure 6 in the updated article shows the mean fraction of `E_new` that is used at least once in the next `k=1,...,30` recovery periods, and the post-shock fraction of delivered volume traded on `E_new`. An `E_new` edge can have appeared in earlier periods before the immediate reference window. Therefore the phrase “new ties” in this analysis always means new *relative to the reference window*, not first-ever partnerships. The box plot shows seed-level distributions; it is not a real-world sampling confidence interval.

## Reproducible descriptive findings

The mean number of shock-activated, baseline-absent links per run was 22.86 for the human–LLM-derived policy and 21.06 for the LLM–LLM-derived policy. Of these, 59.32% and 45.10%, respectively, reappeared at least once during the first 15 recovery periods. In these periods the corresponding links carried 8.87% and 5.61% of delivered volume. Switching the baseline to the last 20 or 30 periods before the shock reduces cohort sizes but does not reverse the reactivation-rate ordering (see `results/emergent_link_baseline_robustness.csv`).

The mean supplier-share total-variation distance relative to the reference was approximately 0.200 and 0.196 during the disruption, declining to 0.114 and 0.102 in early recovery. Persistence away from the baseline identifies trading-network path dependence within the model, without demonstrating memory retention by deployed LLM systems. The original empirical source identifies joint bargaining outcomes; these link dynamics also depend on assumed sourcing and partner-history rules.
