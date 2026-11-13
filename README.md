# Negotiation-informed procurement networks

**Reproducible agent-based simulation, observational bargaining calibration, and emergent network diagnostics**

This repository accompanies a research study of how negotiation-related decisions can shape a supply network over repeated procurement cycles. Buyer and supplier agents face the same capacity constraints and structured procurement rules across experimental conditions. Their stochastic bargaining outcomes are calibrated from a selected set of published economic-game records, while partner-specific experience modifies future contacts and acceptance decisions through explicit model rules. The simulations examine service, costs, supplier concentration, the persistence of trading links, and reorganization after a capacity disruption.

**Scope of the evidence.** The underlying 64 GLEE negotiations comprise **33 human–LLM** and **31 LLM–LLM** games, not human–human and LLM–LLM matched experiments. The source observations identify joint outcomes, not separately estimated buyer and supplier policies. The simulated agents are stochastic decision policies informed by those outcomes. **No live LLM was run during these experiments, and no real firm-level network was observed.** The role-specific agreement mechanism and relational updates are transparent modeling assumptions.

## Repository contents

| Directory | What it contains |
|:--|:--|
| `code/` | Core ABM, negotiation-data preparation, perturbation analysis, emergent-link diagnostics, figure generation, and an optional live-agent interface stub |
| `data/` | A 64-game table of derived outcome measurements from publicly accessible GLEE game files; no transcript text or participant names |
| `results/` | Archived seed-level, period-level, paired-effect, sensitivity, and emergent-network outputs, including a single-seed network snapshot |
| `figures/` | Publication diagrams and model-based results in vector PDF/SVG and 600-DPI PNG |
| [`ODD_2020_Protocol.pdf`](ODD_2020_Protocol.pdf) | Readable, paginated PDF of the complete ODD 2020 model description |
| [`docs/ODD_protocol.md`](docs/ODD_protocol.md) | Editable Markdown version of the ODD description |
| `docs/` | Data provenance, data dictionary, experiment design, interpretation and reproducibility instructions |
| `tests/` | Independent repository checks and regression tests |
| `tools/` | Output verification and manifest checks |

## Quick start

Use Python 3.11 or newer. From the extracted repository root:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python tools/verify_outputs.py
```

The commands above validate source counts, invariants, archived outputs, and deterministic replays without replacing the included results.

## Reproduce the experiments

The full experiment consists of **80 matched simulation seeds**, **100 periods**, **24 buyers**, **12 suppliers**, and a capacity reduction over periods **40–54**. Regimes `H` and `A` refer to the **source negotiation dyads**, while `fixed` and `adaptive` indicate the activation of additional partner-specific experience feedback.

```bash
# Generates a separate main-experiment copy, preserving archived outputs
python code/adaptive_abm.py --reps 80 --out-dir scratch/main

# Network-emergence cohort and reallocation statistics
python code/analyze_emergent_links.py --seeds 80 --out-dir scratch/emergence

# Policy-mechanism sensitivity, 12 matched seeds as reported
python code/run_sensitivity_adaptive.py --seeds 12 --out-dir scratch/sensitivity

# Figures use the archived data in results/ and write to figures/
python code/plot_grayscale_framework.py
python code/regenerate_grayscale_results.py
python code/plot_emergent_links.py
python code/plot_network_snapshots.py
```

See [reproduction instructions](docs/REPRODUCIBILITY.md) for expected files, verification, and a source-data re-extraction example.

## What the observational data support

The model uses the fraction of **economically valid agreements**, observed numbers of negotiation rounds conditional on validity, and the seller's share of available surplus. Its starting bilateral success probability is the empirically calibrated dyad-level quantity; the decomposition into separate buyer and supplier decisions is a symmetric **identification assumption**, not a role-specific empirical estimate. Operational dynamics, partner-history updates and shock parameters are synthetic. The framework separates these evidence classes in the ODD document and the [assumption ledger](docs/THEORY_TO_MODEL_TRACEABILITY.md).

## Network emergence diagnostics

Two analyses use full-period bilateral trading records: the distance of current supplier-volume shares from the pre-disruption reference distribution and the return of shock-activated links during recovery. A link described as *new* is new **relative to a preceding reference window**, not necessarily a first-ever trading relationship. Statistical intervals describe variation across simulated seeds and should not be interpreted as confidence intervals for causal human/LLM differences.

## Data, use and citation

The GLEE dataset was introduced in *GLEE: A Unified Framework and Benchmark for Language-based Economic Environments* (2024), https://arxiv.org/abs/2410.05254. Upstream repository: https://github.com/eilamshapira/GLEE. The original game transcripts are not redistributed here. The 64-row measurement extract records numeric fields and source game IDs; the provenance and usage boundary are documented in [data provenance](docs/DATA_PROVENANCE.md). No original GLEE license was confirmed during packaging, so the original dataset remains governed by its upstream terms; this repository's code license does not grant rights over upstream material.

This repository contains no personal contributor name, institutional email, GitHub handle, personal computer path, or manuscript author block. It is prepared for assignment to a public GitHub repository. A permanent link and citation can be added to the manuscript after publication of the repository and release tag.
