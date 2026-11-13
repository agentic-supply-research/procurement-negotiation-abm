# Reproducing the computational study

This guide separates data validation, recreation of the stochastic experiments, and figure generation. The project has no secret keys, hosted services, account credentials, or proprietary runtime dependencies. The optional live-agent adapter is an unconnected interface; the numerical results depend only on local Python libraries and the supplied derived observations.

## Environment

Tested for this release using Python 3.13.5 with numpy 2.3.5, pandas 2.2.3, scipy 1.17.0, matplotlib 3.10.8, and statsmodels 0.14.6. The `requirements.txt` specifies supported version ranges; environments with other versions can show minor floating-point or rendering differences. Run commands from the repository root.

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Step 1: validate the released datasets without rerunning the study

```bash
python -m unittest discover -s tests -v
python tools/verify_outputs.py
python tools/verify_manifest.py
```

The tests verify the 64 source cases, 13/19 and 7/8 economically valid agreements, deterministic decisions under fixed seeds, buyer and supplier capacity accounting, the 15-period disruption, saved-output dimensions, and observational edge logging. The output verifier also recomputes selected study statistics from the saved data. The SHA-256 manifest reports integrity of the archived data and results.

## Step 2: regenerate full main simulation

```bash
python code/adaptive_abm.py --reps 80 --out-dir scratch/main
```

This produces `adaptive_trajectories.csv`, `adaptive_replications.csv`, `adaptive_summary.csv`, `adaptive_paired.csv`, `adaptive_snapshots_seed0.npz`, and `empirical_summary.csv` in `scratch/main/`. Seed indexes are 0–79 and each seed uses four scenarios. The generated outputs can be compared numerically against `results/` with `python tools/compare_results.py --generated scratch/main`.

## Step 3: reproduce emergent network diagnostics

```bash
python code/analyze_emergent_links.py --seeds 80 --out-dir scratch/emergence
python tools/compare_results.py --generated scratch/emergence
```

This replays the same random streams and records trading-edge matrices observationally. The diagnostic does not change agent decisions. It reproduces four `emergent_link_*.csv` files, including the 10/20/30-period baseline-window check.

## Step 4: reproduce mechanism sensitivity

```bash
python code/run_sensitivity_adaptive.py --seeds 12 --out-dir scratch/sensitivity
python tools/compare_results.py --generated scratch/sensitivity
```

This evaluates eight variants, each for all four scenarios and 12 seeds. Sensitivity to learning-rate assumptions and the distinction between partner selection and agreement-memory effects is reported in the output table.

## Step 5: rebuild publication figures

```bash
python code/plot_grayscale_framework.py
python code/regenerate_grayscale_results.py
python code/plot_network_snapshots.py
python code/plot_emergent_links.py
```

All figures are exported as vector PDF/SVG and 600-DPI PNG. Their content is based on the source extract, saved outputs or explicit conceptual model rules; no image-generating AI is required.

## Optional: recover the source observations from the public GLEE repository

GLEE source: https://github.com/eilamshapira/GLEE. Obtain the original dataset yourself and follow its access and reuse conditions.

```bash
python code/extract_glee_local.py --glee-dir PATH_TO_GLEE --out scratch/glee_full_extract.csv
```

This script extracts **all discoverable source negotiation games** into a separate file, and so will not necessarily reproduce the provided **convenience sample of 64 cases**. To reproduce the exact sample, use the source IDs listed in the provided 64-row table together with the original game files. The present model defaults to the included 64-case extract.

## Methodological cautions

The GLEE dyads provide joint bargaining outcomes only. Two-sided acceptance probabilities are divided symmetrically for simulation purposes. Feedback scores and supplier relationship updates are explicit experimental assumptions, as are all physical capacities and costs. The provided output quantiles describe uncertainty under these computational assumptions; they should not be interpreted as evidence that fully autonomous LLM procurement systems perform better than real human-managed supply chains. See `docs/ODD_protocol.md` for the complete process model.
