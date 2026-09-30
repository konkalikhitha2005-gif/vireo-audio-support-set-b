# Vireo Audio — Support Tickets Set B

## Deliverable
A reproducible Streamlit dashboard for CSAT, median handle time, SLA breach rate, guarded Tier-1 training candidates, and local TF-IDF similar-ticket retrieval.

## Business target
Reduce Tier-1 first-response breaches from **9.09% to 6.00%**. At 650 tickets/week, 13 weeks, and ₹350 per breach: `650 × 13 × (9.09% − 6.00%) × ₹350 ≈ ₹91,360/quarter`. This is a scenario, not a causal guarantee.

## Decisions
- Join agents by `agent_id`, never name.
- Completed = resolved + closed; open/pending excluded.
- Blank CSAT = no response.
- Legacy resolution timestamps get +5:30 because legacy event log is UTC and helpdesk timestamps are IST.
- Tier-2 excluded from Tier-1 comparison per policy.
- Training candidates require ≥50 CSAT responses and use within-team percentiles: CSAT 60%, median handle 25%, breach 15%.
- Candidate output is coaching prioritization, not disciplinary scoring.

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python validate.py
python analysis.py
streamlit run app.py
```

## Limitations
Data ends 30 Jun 2026; CSAT response is ~45%; handle time is skewed; candidate scores are not causal; text similarity is retrieval, not an LLM judgment; budget allocation remains a management decision.
