# Archived simulation outputs

Files in this directory are archived results from the stated source sample and fixed implementation. They allow figure regeneration and independent inspection without rerunning 80 seeds. They are **synthetic** ABM outputs, not company data or measured real-world outcomes.

Core results:
- `empirical_summary.csv`: GLEE negotiation outcome summary by dyad.
- `adaptive_trajectories.csv`: per-period trajectories (4 regimes × 80 seeds × 100 periods).
- `adaptive_replications.csv`: seed-level averages by pre-shock, shock, post-shock and overall phases.
- `adaptive_summary.csv`: across-seed summaries with 2.5% and 97.5% empirical quantiles.
- `adaptive_paired.csv`: matched-seed difference summaries.
- `adaptive_sensitivity.csv`: eight mechanism/parameter variants for 12 matched seeds.
- `adaptive_snapshots_seed0.npz`: selected trading matrices for one illustrative seed.

Emergent-network results:
- `emergent_link_trajectories.csv`: supplier-share displacement, nonbaseline links and use of shock-only links over time.
- `emergent_link_cohorts.csv`: cumulative recovery-period reactivation of links activated during shock.
- `emergent_link_phase_metrics.csv`: phase-level link and supplier-flow metrics.
- `emergent_link_baseline_robustness.csv`: reactivation sensitivity to the pre-shock reference window.

Recomputations should be written to `scratch/` using the `--out-dir` option. See `docs/REPRODUCIBILITY.md` and `docs/DATA_DICTIONARY.md`.
