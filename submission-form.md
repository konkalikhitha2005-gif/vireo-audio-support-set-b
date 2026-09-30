# Submission form — Vireo Audio Set B

## What did you build, and what business outcome does it move?
A reproducible Streamlit dashboard for CSAT, median handle time, SLA breaches, and 10 guarded Tier-1 training candidates, plus local similar-ticket retrieval. Target: **9.09% → 6.00% Tier-1 first-response breaches**, worth about **₹91,360 per 13-week quarter** at 650 tickets/week and ₹350/breach.

## What does one run cost, and what would a month cost?
**₹0 in paid model/API calls.** Runtime uses pandas, Streamlit and local scikit-learn TF-IDF. Monthly model-call cost = **₹0 × ~2,817 tickets/month = ₹0**. (650×52/12 ≈ 2,817.)

## How do you know it works?
**500 completed tickets** were cross-checked (250 legacy + 250 current) with an independent timestamp/SLA calculation. **0 handle-time mismatches, 0 SLA mismatches, 0% observed cross-check error rate.** Full-data invariants also pass. Main failure mode: the tool cannot prove causal agent effects because queue/case difficulty is only partially observed.

## Did you change, narrow, or push back on the client's ask?
Yes. “Bottom ten” became **10 Tier-1 training candidates** because policy excludes Tier-2 from Tier-1 volume comparison and the email warns hardware triage receives angrier customers by design. Minimum 50 CSAT responses and within-team comparisons reduce small-sample and queue-mix bias.

## What is wrong with what you are handing us?
Data ends 30 Jun 2026; CSAT response is ~45%; candidate score is not causal; handle time is skewed; no automatic ₹4 lakh budget allocation; text similarity is retrieval rather than an LLM diagnosis.

## What did you deliberately leave out?
Lot-code analysis, detailed replacement root-cause modeling and automatic training-budget allocation. They were not needed for the immediate CSAT/handle-time decision and would add complexity/unsupported assumptions.

## Anything extra?
A local TF-IDF similar-ticket helper, with no external API calls.

## What did you use AI for?
ChatGPT helped with analysis structure, implementation review and documentation. The shipped runtime makes no paid AI/API calls. The local similarity model is scikit-learn TF-IDF. I discarded per-ticket paid LLM calls and unsupported causal labeling.

**Screen recording:** [PASTE PUBLIC GOOGLE DRIVE VIDEO LINK]

## Public Google Drive Link
[PASTE PUBLIC GOOGLE DRIVE FOLDER LINK]

## Monday handoff — three things
1. `pip install -r requirements.txt`, then `python validate.py`, then `streamlit run app.py`.
2. Never compare Tier-2 with Tier-1 on volume metrics.
3. 9.09%→6.00% is a savings scenario worth ~₹91,360/quarter, not a guaranteed training effect.

## Honest hours
**5.0**

## Github Repo Link
[PASTE PUBLIC GITHUB REPO URL]
