# S&OP Reconciliation Simulator

**A multi-agent AI simulation of a real Sales–Supply demand/supply reconciliation meeting — the kind of decision an Integrated Planning Manager runs every month, made explainable and auditable.**

> Not "AI that predicts a forecast." AI that simulates the *negotiation* behind the forecast — and shows its work.

---

## Why this exists

Most demand-planning tooling optimizes a number. It rarely explains *why* that number is the right trade-off between commercial ambition and operational reality — and it almost never shows an approver the specific reasoning, month by month, behind a final plan.

This project simulates that negotiation directly: a **Sales Demand Agent** and a **Supply/Procurement Agent** argue their positions using real planning data (forecast requests, supply capacity, lead times, MOQ, inventory), and a **Harmonizer** — playing the role of an Integrated Planning Manager — reconciles them into one final, explainable decision.

The design choices here (inventory-aware reasoning, new-product-launch handling, full decision traceability) come directly from real S&OP practice, not from a generic "AI agents" tutorial.

## What it does

1. Pick a scenario (a live planning conflict: demand surge, regulatory supply disruption, oversupply, capacity allocation across markets, or a new product launch with no sales history).
2. Run the review. Three sequential AI calls simulate the meeting:
   - **Sales Demand Agent** argues for volume, grounded in market data (or, for new launches, in market-sizing/analog reasoning rather than a trend that doesn't exist yet).
   - **Supply/Procurement Agent** responds with feasibility limits, lead times, and — critically — current inventory position against a 1.5-month target stock level.
   - **Harmonizer** does not average the two. It makes a judgment call, month by month, and states which factor tipped the decision each time.
3. Review the **Decision Trace** — an expandable, month-by-month ledger showing exactly what each side requested, what was decided, and why. This is the part built specifically so an approver never has to take the final number on faith.

## Architecture
