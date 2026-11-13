# Publication figure guide and results provenance

The manuscript contains seven figures. Figures 1–3 are conceptual representations of the implemented research design and decision sequence. They are drawn with explicit coordinates and arrow paths in `code/plot_grayscale_framework.py`. Figures 4–7 display the archived micro-observations or recorded simulation outputs. Their source is `code/plot_publication_figures.py`, invoked in monochrome by `code/regenerate_grayscale_results.py`. All publication figures are available as 600 DPI PNGs and as vector PDF and SVG.

| Manuscript figure | File stem in `figures/` | Evidence or purpose |
|---|---|---|
| Figure 1 | `figure01_problem_network` | One shared buyer–supplier network and two possible relational authorities. Conceptual target; not an observed human-only / LLM-only comparison. |
| Figure 2 | `figure02_data_to_abm` | Observed GLEE counts → posterior and resampled contract terms → modeled bilateral acceptance and partner histories. |
| Figure 3 | `fig02_micro` | Valid-contract frequencies, 95% Wilson intervals, round counts and seller-surplus shares from 64 GLEE cases. |
| Figure 4 | `figure03_abm_schedule` | Feasibility, shortlist, bilateral acceptance, contract execution and feedback. |
| Figure 5 | `fig03_trajectories` | Archived `results/adaptive_trajectories.csv`; mean service and tie-retention over 100 periods. |
| Figure 6 | `fig06_sensitivity` | Archived `results/adaptive_sensitivity.csv`; 12 matched seeds for feedback-channel and learning-parameter diagnostics. |
| Figure 7 | `fig05_paired_effects` | Archived `results/adaptive_paired.csv`; mean and 2.5th–97.5th percentile of 80 paired seed-level differences. |

The network snapshot panels in `fig07_network_snapshots.*` are supplementary and represent one simulation seed at periods 39, 48 and 70. They are useful for illustrating possible changes in trading ties but must not be described as observed real-world networks or ensemble-average effects.

## Interpretation and audit checks

The human–LLM category contains 33 games (19 positive-surplus cases and 13 valid contracts). The LLM–LLM category contains 31 games (8 positive-surplus cases and 7 valid contracts). These figures are dyad-level outcomes and do not uniquely identify individual buyer or supplier acceptance decisions. Contract duration and seller surplus shares are resampled from the valid observations. All quantity allocation, learning and relationship feedback in the ABM are prescribed submodels.

The manuscript reports 80 paired replications for the main comparisons, and the control diagnostics use 12 matched seeds. The existing CSV files are the authoritative numerical sources. Plot regeneration does not run or fit new simulations. Across-seed quantiles are descriptive uncertainty ranges, not causal confidence intervals for replacing human managers with LLMs.

The code's 600 DPI setting controls raster export. The PDF and SVG outputs are vector graphics and remain sharp when scaled in the Springer layout. Figure labels use standard scientific typography and grayscale contrast; legends and captions remain outside the plotted data where appropriate. No AI-generated figures are part of the publication files.
