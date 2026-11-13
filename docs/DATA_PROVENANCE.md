# Data provenance and measurement construction

## Primary source

The empirical input was extracted from the publicly accessible GLEE negotiation recordings associated with *GLEE: A Unified Framework and Benchmark for Language-based Economic Environments* (2024), https://arxiv.org/abs/2410.05254. Original repository: https://github.com/eilamshapira/GLEE. The source repository includes human–LLM and LLM–LLM language-based economic games. Its recorded human participants should not be confused with a human–human procurement baseline.

The released table records **derived numerical observations** from 64 source games, not the full conversations. It contains no human participant names, email addresses, prompt messages, or transcript text. Individual source game IDs are retained for an audit trail. **The selection is non-random**: 33 human–LLM and 31 LLM–LLM observations from an initial hexadecimal game-ID shard. The selected configurations vary in valuations and information conditions and are not matched randomized experimental treatments.

## Source-to-extract mapping

The source directory convention is:

`Data/{human_vs_llm,llm_vs_llm}/negotiation/<ID-shard>/<source-game-id>/{config.json,game.csv}`

For every selected source game, the numeric extract retains the buyer reservation value, seller reservation cost, last submitted price in an accepted game, reported acceptance, maximum round index, information regime and messaging permission. The price is normalized by the source configuration’s price-order scale. Source case IDs allow reinspection against the upstream files. The script `code/extract_glee_local.py` offers a local extraction path; extracting the full upstream dataset is different from the selected sample used for the archived results.

## Screening and estimation

A bargaining opportunity is economically feasible when the buyer's reservation value exceeds the seller's reservation cost. A recorded acceptance is considered executable only if the accepted price belongs to that interval. This leaves **19 feasible human–LLM source games (13 valid agreements)** and **8 feasible LLM–LLM games (7 valid agreements)**. In the human–LLM group, some recorded acceptances do not satisfy the price bounds; these are excluded from the executable-contract kernel.

The ABM constructs an uncertainty-aware joint agreement probability using a Jeffreys-prior Beta posterior, then resamples valid-deal negotiation rounds and normalized seller-surplus shares. These are **dyad-level** measurements. The split of joint acceptance into separate buyer and supplier probabilities is an identification assumption. The rules for supplier search, learning, relationship retention, capacity shock and operating cost are synthetic and not estimated from GLEE.

## Third-party rights and publication boundary

The public availability of GLEE does not, by itself, establish redistribution permission. No explicit license covering the original Data directory was verified in this packaging step. The original transcripts and config files are therefore not included. The 64-row derived numeric extract is supplied for transparent research reproduction; before uploading the extract to a public repository, the repository owner should check the upstream terms and remove or replace the table if redistribution is not permitted. This repository's MIT license applies to original simulation and plotting code only, not to upstream data.

An alternative public-release strategy is to publish the extraction and analysis scripts, data schema, summary statistics and simulation outputs, while asking users with lawful source access to build the observation table locally. If the derived numeric extract is excluded, the primary experiment requires its regeneration before running.
