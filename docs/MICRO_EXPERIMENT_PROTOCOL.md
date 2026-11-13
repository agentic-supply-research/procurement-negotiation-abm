# Proposed matched human/AI B2B micro-experiment (not yet run)

**Scientific target:** Differences in relational decisions, **not** differences in mathematical optimization algorithms.

## Case

A component supplier and a manufacturer have traded for six past quarters. The manufacturer needs 80–120 units next period; the supplier's available capacity and true production cost are private. A second buyer may bid for the same capacity. After two uneventful contract rounds, a machine outage reduces supply by 40%. Both parties may renegotiate price, quantity, deadlines and future priority. Maintain verifiable feasible contract constraints and a chance to continue the relationship over multiple periods.

## 2x2 actor design

- Human buyer / Human supplier
- Human buyer / LLM supplier
- LLM buyer / Human supplier
- LLM buyer / LLM supplier

Each negotiation should use the SAME underlying economic scenario and incentive conditions, randomly assigned among valid pools. Counterbalance role, game order and opponent model. For human observations use genuine consenting participants; real procurement professionals are preferable. Ethics approval is needed. An LLM 'playing a human' is not human data.

## Distinct behavioral choices

1. Share true available capacity or selectively withhold permitted information.
2. Offer / counteroffer the price, volume, payment term, and delay compensation.
3. Honor or seek to renegotiate an earlier promise when the shock occurs.
4. Provide temporary priority to a past cooperative customer versus a higher spot-market bid.
5. Continue or terminate a relationship after an adverse outcome.

Tool-mediated structured actions should be separated from natural-language persuasion, with typed JSON actions validated by the simulation. Both human and AI participants should have access to the SAME MILP-based feasible-price and capacity decision support when appropriate; optimization performance is controlled.

## Behavioral estimands

Pre-register per-dyad probability of economically feasible agreement, normalized surplus allocation, quantity delivered, price concession conditional on outside options, accuracy of stated capacity, contractual continuity, retaliation/reward after previous cooperation, renewal hazard and disruption recovery time. Record negotiation rounds and all permitted messages. Distinguish self-reported trust (only for humans) from revealed preference for renewal (both agent types).

## Micro validation before network ABM

Fit policies with respondent/agent-model clustered uncertainty. Hold out economic scenarios and counterpart types; assess calibration curves, likelihood and action-sequence realism; reproduce disruption interactions and check utility-bounded action validity. Condition on role, available surplus, message regime and specific model/prompt; avoid naïve cross-population comparisons.

## Agentic LLM requirements

Use independent agent sessions with isolated private state, strict budget and contract tools, and complete logs of prompts and tool calls. Run multiple model providers or weights, prompt paraphrases, temperature levels and random seeds. Record model versions, consent and cost. LLM failure, refusal, invalid JSON or contract violations are separate outcomes—not silently repaired into successful agreements.

**This protocol is a design specification. The present pilot contains no live LLM interactions and no newly recruited human participants.**
