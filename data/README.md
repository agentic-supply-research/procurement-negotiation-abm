# Derived negotiation measurements

`glee_observed_negotiations_sample.csv` is a **non-random convenience extract** of 64 GLEE negotiation-game outcomes (33 human–LLM, 31 LLM–LLM). It contains source game IDs and numerical descriptors, but no transcript contents or participant names. The fields `buyer` and `seller` are reservation values in the source games; they are not observations of industrial procurement prices. The `price` field stores the last accepted price under the dataset-processing rules; its numerical value does not imply economic validity.

The selection is confined to a source ID shard and is not representative of all possible human/LLM bargaining situations. The simulation conditions on the economically feasible subset (`buyer > seller`) and uses only valid agreements (`seller <= price <= buyer`). Source paths and extraction instructions: [provenance](../docs/DATA_PROVENANCE.md). Field definitions: [data dictionary](../docs/DATA_DICTIONARY.md).

Data rights: observations are **derived from a third-party public research dataset**. This repository's MIT code license does not extend to source recordings or override upstream conditions. Verify upstream data reuse conditions before making the derived table publicly available.
