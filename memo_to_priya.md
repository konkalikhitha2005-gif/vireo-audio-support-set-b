# Memo — Vireo Audio Support Performance

**To:** Priya Raman, Head of Customer Experience  
**Data:** Jan 2025–Jun 2026

I built a reproducible dashboard for completed tickets with agent CSAT, median handle time and first-response SLA breach rate. It flags 10 Tier-1 coaching candidates using a transparent within-team comparison. Tier-2 is excluded because the policy says Tier-2 is measured in resolution days and is not to be compared with Tier-1 on volume.

**Business target:** reduce Tier-1 first-response breaches from **9.09% to 6.00%**. The policy charges **₹350 per breach**. At 650 tickets/week, this is approximately **₹91,360 per 13-week quarter** in avoided SLA credits. This is a savings scenario, not a claim that training alone causes the savings.

There are 11,183 completed tickets and 4,947 CSAT responses. Tier-1 average CSAT is about **3.42/5**; **18.23%** of responding Tier-1 tickets score 1–2; Tier-1 first-response breach rate is **9.09%**.

The dashboard does not treat low CSAT as proof an agent caused it. The email thread notes that hardware triage gets angrier customers by design. Candidate selection therefore uses a minimum of 50 CSAT responses and within-team comparisons.

Legacy resolution timestamps were reconstructed from UTC while helpdesk timestamps are IST, so legacy resolution times are normalized by +5:30. Blank CSAT is excluded. Agent joins use `agent_id`.

Use the 10 candidates as a coaching queue, not an automatic disciplinary list. Measure the same metrics for four weeks after coaching and release training spend in stages rather than assuming the full ₹4 lakh will pay back.

**Limitations:** the data ends June 2026, so it cannot establish an actual Q3 outcome; CSAT has sampling noise; handle time is skewed; the candidate score is not causal.
