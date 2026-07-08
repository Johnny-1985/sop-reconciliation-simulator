# S&OP Reconciliation Simulator

**Status: 🚧 Actively developed — Phase 2 in progress.** See [Roadmap](#roadmap) for what's shipped vs. planned.

**A multi-agent AI simulation of a real Sales–Supply demand/supply reconciliation meeting — the kind of decision an Integrated Planning Manager runs every month, made explainable and auditable.**

> Not "AI that predicts a forecast." AI that simulates the *negotiation* behind the forecast — and shows its work.

![Demo](docs/assets/demo.gif)

---

## Why this exists

Most demand-planning tooling optimizes a number. It rarely explains *why* that number is the right trade-off between commercial ambition and operational reality — and it almost never shows an approver the specific reasoning, month by month, behind a final plan.

This project simulates that negotiation directly: a **Sales Demand Agent** and a **Supply/Procurement Agent** argue their positions using real planning data (forecast requests, supply capacity, lead times, MOQ, inventory), and a **Harmonizer** — playing the role of an Integrated Planning Manager — reconciles them into one final, explainable decision.

The design choices here (inventory-aware reasoning, new-product-launch handling, full decision traceability) come directly from real S&OP practice, not from a generic "AI agents" tutorial.

## What it does

1. Pick a scenario (a live planning conflict: demand surge, regulatory supply disruption, oversupply, capacity allocation across markets, or a new product launch with no sales history).
2. Run the review. The system simulates the meeting with a variable number of AI calls depending on the situation:
   - **Sales Demand Agent** argues for volume, grounded in market data (or, for new launches, in market-sizing/analog reasoning rather than a trend that doesn't exist yet).
   - **Supply/Procurement Agent** responds with feasibility limits, lead times, and — critically — current inventory position against a 1.5-month target stock level.
   - **Finance Agent** joins *only* if inventory surplus has persisted 2+ consecutive months — a dead-stock risk that Sales and Procurement aren't positioned to resolve. It weighs holding cost against markdown vs. write-off.
   - **Harmonizer** does not average the positions. It makes a judgment call, month by month, and states which factor tipped the decision each time — including whether it accepted or overrode Finance's pricing recommendation.
3. Review the **Decision Trace** — an expandable, month-by-month ledger showing exactly what each side requested, what was decided, and why. This is the part built specifically so an approver never has to take the final number on faith.

## Architecture

```
┌─────────────────────┐
│  Scenario Data       │  Synthetic solar-industry data: modules (MWp), inverters,
│  (synthetic_data.json)│  ESS batteries — forecast, capacity, lead time, MOQ, inventory
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│ Sales Demand Agent   │  Argues for volume; distinguishes trend-based vs.
│                      │  market-sizing reasoning for new product launches
└──────────┬───────────┘
           │ (sees Sales' output)
           ▼
┌─────────────────────┐
│ Supply/Procurement   │  Argues feasibility; weighs inventory surplus/deficit
│ Agent                │  against a 1.5-month target stock level
└──────────┬───────────┘
           │
           ▼
   ┌─── dead_stock_trigger_month set? ───┐
   │ NO → skip to Harmonizer             │ YES ↓
   │                                      │
   │                          ┌─────────────────────┐
   │                          │ Finance Agent        │  Holding cost vs. markdown
   │                          │ (conditional)        │  vs. write-off, with numbers
   │                          └──────────┬───────────┘
   └──────────────────────────────────────┘
                              │ (sees all prior outputs)
                              ▼
                   ┌─────────────────────┐
                   │ Harmonizer           │  Integrated Planning Manager persona.
                   │                      │  Final volume + (if applicable) pricing
                   │                      │  decision, both with a reasoning trace
                   └──────────┬───────────┘
                              │
                              ▼
           Executive Summary + Decision Trace (expandable, auditable)
```

Three API calls per review, or four when the Finance Agent is triggered. No infinite loops, no hidden state — every output is a structured JSON object so the UI can render it directly.

## Key differentiators

- **Explainable by design, not by afterthought.** The Harmonizer's `decision_trace` ties every final number to a specific, month-level reason drawn from the two agents' actual arguments — not one generic paragraph for the whole plan.
- **Inventory-aware, not just capacity-aware.** Procurement's position factors in whether current stock is already above or below a 1.5-month target, which changes the argument even when raw production capacity would technically allow more supply.
- **The agent roster adapts to the situation.** The Finance Agent is not always in the room — it's only convened when the data shows a genuine dead-stock risk (inventory surplus persisting 2+ consecutive months), the same way a real planning manager wouldn't put a write-off decision on every meeting's agenda. This conditional orchestration, not a fixed pipeline, is deliberate.
- **New product launches are handled differently, on purpose.** When a scenario has no sales history, the Sales Agent is required to say so and switch to market-sizing/analog reasoning — and the Harmonizer treats that as higher uncertainty, not as equivalent confidence to an established product.
- **Built on real planning judgment.** The scenario structure, unit conventions (MWp for modules via POWERCLASS × quantity, unit counts for inverters/ESS), and lead-time assumptions reflect actual solar-industry S&OP practice, not a generic supply-chain template.

## Tech stack

- Single-file HTML/JS demo (`sop_demo.html`), rendered as a Claude Artifact
- Anthropic Messages API (`claude-sonnet-4-6`), called directly from the browser — three sequential calls per review, each agent's output feeding the next
- Synthetic data generated with Python (`build_data.py`) and mirrored into a formatted Excel workbook (`synthetic_data.xlsx`) with live formulas (no hardcoded derived values)

## Data & scenarios

All data is synthetic — a fictional company ("SunArc Solar") and fictional product names. Five scenarios cover distinct S&OP conflict types:

| Scenario | Product | Conflict type |
|---|---|---|
| A — Italy Inverter Demand Surge | 3-phase hybrid inverter | Demand outpacing supply, competitive pressure |
| B — Poland Certification Delay | ESS battery pack | Regulatory supply disruption |
| C — Germany Battery Oversupply | Residential battery | Demand slowdown, existing inventory surplus |
| D — France Module Capacity Allocation | PV module (MWp) | Cross-market capacity trade-offs |
| E — Germany New Compact ESS Launch | New ESS model | No sales history — market-sizing reasoning required |

## Running the demo

This demo calls the Anthropic API directly from the browser. It runs live inside a Claude Artifact (claude.ai) without any setup.

**Important:** if you download `sop_demo.html` and open it outside claude.ai, the API calls will not authenticate — there is no backend proxy in this repository yet. Bringing this online as a standalone public demo would require a small serverless proxy (e.g., a Vercel/Cloudflare function holding the API key). See Roadmap.

## Roadmap

| Phase | Scope |
|---|---|
| **Phase 1** | 2 agents (Sales, Procurement) + Harmonizer, 5 pre-built scenarios, full decision-trace explainability, inventory-aware logic, new-launch handling |
| **Phase 2 (in progress)** | ✅ Finance Agent (margin/write-off perspective) + dead-stock/liquidation logic, conditionally triggered when inventory surplus persists 2+ consecutive months · Next: result history, standalone hosted demo with backend proxy |
| **Phase 3** | Reviewer Agent for automated quality checks, adjustable What-if parameters (forecast %, lead time, promotion on/off) |

## About this project

This simulates a decision I make in a real job, not a toy problem. I lead EU cluster demand planning at a multinational solar manufacturer, sitting between regional sales teams and supply/procurement as the point of reconciliation — this project is a deliberately simplified, auditable version of that role.

---

*All data, company names, and product names in this repository are fictional and created for demonstration purposes only.*
