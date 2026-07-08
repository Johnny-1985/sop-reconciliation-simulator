import json

with open("/home/claude/synthetic_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

DATA_JS = json.dumps(DATA, ensure_ascii=False)

SALES_PROMPT = """You are the Sales Demand Agent in an S&OP (Sales & Operations Planning) reconciliation simulation. Your role is to represent the commercial/market perspective.

Your mandate:
- Advocate for securing enough supply volume to capture market opportunity and protect against customer churn or competitive loss.
- Base every argument on the specific numeric data provided (sales_forecast_request, market/competitive context in narrative_context). Do not invent numbers not present in the data.
- Check product_lifecycle_stage. If it is "established", you may reason from the trend across months as if it reflects real historical momentum. If it is "new_launch" (see launch_month), there is NO real sales history - say so explicitly, and instead ground your argument in market-sizing logic and analogy to a comparable existing product (as described in narrative_context). Flag that your forecast confidence is lower than for an established product.
- Be persuasive but professional. Acknowledge supply constraints exist, but argue why the business risk of under-supplying outweighs the operational difficulty.
- Quantify the downside: estimate revenue-at-risk or churn risk in plain business terms based on the gap between sales_forecast_request and current_supply_capacity.

Respond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:
{
  "agent": "sales_demand",
  "position_summary": "1-2 sentence summary of your stance",
  "key_arguments": ["argument 1", "argument 2", "argument 3"],
  "requested_volume_by_month": {"month": number},
  "forecast_basis": "trend-based, or market-sizing/analog for new launches, with 1 sentence explaining which",
  "business_risk_if_denied": "1-2 sentence risk statement"
}"""

PROCUREMENT_PROMPT = """You are the Supply/Procurement Agent in an S&OP reconciliation simulation. Your role is to represent operational feasibility and cost discipline.

Your mandate:
- You have just read the Sales Demand Agent's argument (provided below). Respond directly to their specific requested volumes.
- Base every argument on the specific numeric data provided (current_supply_capacity, lead_time_weeks, moq, unit_cost_eur, inventory_on_hand). Do not invent numbers not present in the data.
- Identify precisely which months the requested volume exceeds feasible capacity, and by how much.
- Inventory position matters: the target inventory level is 1.5 months of demand (target_inventory_level in the data). If inventory_gap is positive (existing stock already exceeds 1.5 months of demand), argue for restraint even if Sales' request looks feasible. If inventory_gap is negative (stock is below the 1.5-month target), that strengthens the case for approving more supply.
- Where possible, propose a constructive alternative (partial fulfillment, phased ramp-up, expedited lead time at cost premium) rather than a flat refusal. If genuinely infeasible for a given month, say so clearly.

Respond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:
{
  "agent": "supply_procurement",
  "position_summary": "1-2 sentence summary of your stance",
  "key_arguments": ["argument 1", "argument 2", "argument 3"],
  "max_feasible_volume_by_month": {"month": number},
  "inventory_position_note": "1 sentence noting surplus or deficit vs the 1.5-month target and how it affects your position",
  "proposed_alternative": "1-2 sentence constructive proposal, if any"
}"""

HARMONIZER_PROMPT = """You are the Harmonizer in an S&OP reconciliation simulation, playing the role of an Integrated Planning Manager who sits between Sales and Supply/Procurement. You have read both agents' positions (provided below).

Your mandate:
- Do not simply average the two positions. Make a reasoned judgment call, the way an experienced planning manager would in a live monthly S&OP meeting.
- Weigh business risk (from Sales) against operational/financial risk (from Procurement) explicitly.
- Produce ONE final recommended volume per month.
- CRITICAL - full traceability: an approver reviewing this must be able to see, for EVERY month, what each side argued and exactly why you landed on your final number. Reasoning can differ month to month.
- Factor in inventory position explicitly: a surplus is a reason to lean toward the lower/Procurement number even if Sales' request is technically producible; a deficit strengthens the case for the higher/Sales number.
- If product_lifecycle_stage is "new_launch", flag that Sales' forecast_basis is market-sizing/analog rather than trend data, treat as higher uncertainty, and consider a more conservative number with a faster review cycle.
- Flag any risk that remains even after your decision.

Respond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:
{
  "agent": "harmonizer",
  "decision_trace": [
    {"month": "month", "sales_requested": number, "procurement_max_feasible": number, "final_decision": number, "reasoning": "1-2 sentence month-specific reason"}
  ],
  "key_rationale": ["overall reason 1", "overall reason 2", "overall reason 3"],
  "risk_flags": ["remaining risk 1", "remaining risk 2"],
  "executive_summary": "3-4 sentence summary suitable for an executive S&OP readout"
}"""

SALES_PROMPT_JS = json.dumps(SALES_PROMPT)
PROCUREMENT_PROMPT_JS = json.dumps(PROCUREMENT_PROMPT)
HARMONIZER_PROMPT_JS = json.dumps(HARMONIZER_PROMPT)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SunArc Solar — S&OP Reconciliation Simulator</title>
<style>
:root {{
  --bg: #F3F4EF;
  --paper: #FBFBF9;
  --ink: #1B2027;
  --ink-soft: #565F6E;
  --rule: #D9DACF;
  --sales: #96591A;
  --sales-bg: #FBF0DE;
  --sales-line: #E3C89A;
  --proc: #2C5266;
  --proc-bg: #E8EFF1;
  --proc-line: #B9CDD5;
  --harm: #6B2737;
  --harm-bg: #F5EAEC;
  --harm-line: #D9B7BE;
  --surplus: #3D6B4A;
  --deficit: #A8341F;
  --mono: "SF Mono", "Cascadia Code", Consolas, "Courier New", monospace;
  --serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --sans: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 32px 20px 80px;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--sans);
  line-height: 1.5;
}}
.wrap {{ max-width: 920px; margin: 0 auto; }}

.masthead {{
  border-bottom: 3px solid var(--ink);
  padding-bottom: 18px; margin-bottom: 24px;
}}
.eyebrow {{
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--ink-soft); margin-bottom: 6px;
}}
h1 {{
  font-family: var(--serif); font-size: 34px; font-weight: 700;
  margin: 0 0 6px; letter-spacing: -0.01em;
}}
.subtitle {{ color: var(--ink-soft); font-size: 14.5px; }}

.tabs {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 18px; }}
.tab {{
  font-family: var(--mono); font-size: 12px; padding: 9px 14px;
  background: var(--paper); border: 1px solid var(--rule); border-bottom: none;
  border-radius: 6px 6px 0 0; cursor: pointer; color: var(--ink-soft);
  position: relative; top: 1px;
}}
.tab.active {{
  background: var(--ink); color: var(--paper); border-color: var(--ink);
  font-weight: 600;
}}

.dossier {{
  background: var(--paper); border: 1px solid var(--rule); border-radius: 0 6px 6px 6px;
  padding: 22px 24px; margin-bottom: 20px;
}}
.dossier h2 {{ font-family: var(--serif); font-size: 21px; margin: 0 0 4px; }}
.meta-row {{
  font-family: var(--mono); font-size: 12px; color: var(--ink-soft);
  margin-bottom: 12px; display: flex; gap: 16px; flex-wrap: wrap;
}}
.lifecycle-tag {{
  display: inline-block; padding: 1px 7px; border-radius: 3px;
  background: var(--harm-bg); color: var(--harm); font-weight: 600;
}}
.narrative {{ font-size: 14px; color: var(--ink); margin-bottom: 16px; }}

table.data-table {{ width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 12px; }}
table.data-table th {{
  text-align: right; padding: 6px 8px; border-bottom: 2px solid var(--ink);
  color: var(--ink-soft); font-weight: 600; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em;
}}
table.data-table th:first-child, table.data-table td:first-child {{ text-align: left; }}
table.data-table td {{ text-align: right; padding: 6px 8px; border-bottom: 1px solid var(--rule); }}
.gap-pos {{ color: var(--surplus); font-weight: 600; }}
.gap-neg {{ color: var(--deficit); font-weight: 600; }}

.run-btn {{
  display: block; width: 100%; margin-top: 20px; padding: 14px;
  background: var(--harm); color: var(--paper); border: none; border-radius: 6px;
  font-family: var(--sans); font-size: 14.5px; font-weight: 700; letter-spacing: 0.02em;
  cursor: pointer;
}}
.run-btn:disabled {{ opacity: 0.5; cursor: default; }}
.run-btn:hover:not(:disabled) {{ filter: brightness(1.08); }}

.status {{
  font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft);
  margin: 14px 0; min-height: 18px;
}}
.status.active::before {{ content: "▸ "; color: var(--harm); }}

.testimony {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }}
@media (max-width: 700px) {{ .testimony {{ grid-template-columns: 1fr; }} }}
.card {{ border-radius: 6px; padding: 18px 20px; border: 1px solid; }}
.card.sales {{ background: var(--sales-bg); border-color: var(--sales-line); }}
.card.proc {{ background: var(--proc-bg); border-color: var(--proc-line); }}
.card-label {{ font-family: var(--mono); font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700; margin-bottom: 6px; }}
.card.sales .card-label {{ color: var(--sales); }}
.card.proc .card-label {{ color: var(--proc); }}
.position-summary {{ font-family: var(--serif); font-size: 15.5px; margin-bottom: 12px; }}
.card ul {{ margin: 0 0 12px; padding-left: 18px; font-size: 13.5px; }}
.card li {{ margin-bottom: 5px; }}
.card .note {{ font-size: 12.5px; color: var(--ink-soft); border-top: 1px dashed var(--rule); padding-top: 10px; margin-top: 10px; }}

.verdict {{
  background: var(--harm-bg); border: 1px solid var(--harm-line); border-radius: 6px;
  padding: 22px 24px; margin: 20px 0;
}}
.seal {{
  display: inline-block; font-family: var(--mono); font-size: 11px; font-weight: 700;
  letter-spacing: 0.1em; color: var(--paper); background: var(--harm);
  padding: 4px 10px; border-radius: 3px; margin-bottom: 12px;
}}
.exec-summary {{ font-family: var(--serif); font-size: 16px; margin-bottom: 14px; }}
.verdict h4 {{ font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--harm); margin: 14px 0 6px; }}
.verdict ul {{ margin: 0; padding-left: 18px; font-size: 13.5px; }}
.risk-tag {{
  display: inline-block; font-size: 12px; padding: 3px 9px; border-radius: 3px;
  background: #fff; border: 1px solid var(--deficit); color: var(--deficit); margin: 3px 6px 0 0;
}}

.ledger {{ margin-top: 22px; }}
.ledger-title {{ font-family: var(--mono); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-soft); margin-bottom: 8px; }}
.ledger-row {{
  background: var(--paper); border: 1px solid var(--rule); border-radius: 4px;
  margin-bottom: 6px; overflow: hidden;
}}
.ledger-head {{
  display: grid; grid-template-columns: 90px 1fr 1fr 1fr 20px; gap: 10px;
  padding: 10px 14px; cursor: pointer; align-items: center;
  font-family: var(--mono); font-size: 12.5px;
}}
.ledger-head .lbl {{ font-size: 9.5px; text-transform: uppercase; color: var(--ink-soft); display: block; }}
.ledger-head .arrow {{ text-align: right; color: var(--ink-soft); transition: transform 0.15s; }}
.ledger-row.open .arrow {{ transform: rotate(90deg); }}
.ledger-body {{
  display: none; padding: 0 14px 14px 14px; font-size: 13px; color: var(--ink);
  border-top: 1px dashed var(--rule);
}}
.ledger-row.open .ledger-body {{ display: block; padding-top: 10px; }}

.footer-note {{ font-family: var(--mono); font-size: 11px; color: var(--ink-soft); margin-top: 40px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="masthead">
    <div class="eyebrow">SunArc Solar · Integrated Planning — Case File</div>
    <h1>S&amp;OP Reconciliation Simulator</h1>
    <div class="subtitle">Multi-agent simulation of a Sales–Supply demand/supply reconciliation, mediated by an Integrated Planning Manager persona (Harmonizer).</div>
  </div>

  <div class="tabs" id="tabs"></div>
  <div class="dossier" id="dossier"></div>
  <button class="run-btn" id="runBtn">Convene S&amp;OP Review</button>
  <div class="status" id="status"></div>

  <div id="results"></div>

  <div class="footer-note">All data is synthetic, for portfolio demonstration purposes only. Company and product names are fictional.</div>
</div>

<script>
const SOP_DATA = {DATA_JS};
const SALES_PROMPT = {SALES_PROMPT_JS};
const PROCUREMENT_PROMPT = {PROCUREMENT_PROMPT_JS};
const HARMONIZER_PROMPT = {HARMONIZER_PROMPT_JS};

const scenarioKeys = Object.keys(SOP_DATA.scenarios);
let currentKey = scenarioKeys[0];

function fmt(n) {{ return typeof n === "number" ? n.toLocaleString() : n; }}

function renderTabs() {{
  const tabs = document.getElementById("tabs");
  tabs.innerHTML = scenarioKeys.map((k, i) => {{
    const label = "SCN-" + String.fromCharCode(65 + i);
    return `<div class="tab ${{k === currentKey ? "active" : ""}}" data-key="${{k}}">${{label}}</div>`;
  }}).join("");
  tabs.querySelectorAll(".tab").forEach(el => {{
    el.addEventListener("click", () => {{
      currentKey = el.dataset.key;
      document.getElementById("results").innerHTML = "";
      document.getElementById("status").textContent = "";
      renderTabs();
      renderDossier();
    }});
  }});
}}

function renderDossier() {{
  const sc = SOP_DATA.scenarios[currentKey];
  const lifecycleTag = sc.product_lifecycle_stage === "new_launch"
    ? `<span class="lifecycle-tag">NEW LAUNCH · ${{sc.launch_month}}</span>`
    : `<span class="meta-row">established product</span>`;

  const isModule = "powerclass_wp" in sc;
  let headerCols = ["Month", "Sales Req", "Supply Cap", "Lead Time", "Inventory", "Target (1.5mo)", "Gap"];
  let rowsHtml = sc.rows.map(r => {{
    const gapClass = r.inventory_gap >= 0 ? "gap-pos" : "gap-neg";
    const gapLabel = r.inventory_gap >= 0 ? "+" + fmt(r.inventory_gap) : fmt(r.inventory_gap);
    return `<tr>
      <td>${{r.month}}</td>
      <td>${{fmt(r.sales_forecast_request)}}</td>
      <td>${{fmt(r.current_supply_capacity)}}</td>
      <td>${{r.lead_time_weeks}}w</td>
      <td>${{fmt(r.inventory_on_hand)}}</td>
      <td>${{fmt(r.target_inventory_level)}}</td>
      <td class="${{gapClass}}">${{gapLabel}}</td>
    </tr>`;
  }}).join("");

  document.getElementById("dossier").innerHTML = `
    <h2>${{sc.title}}</h2>
    <div class="meta-row">
      <span>PRODUCT: ${{sc.product}}</span>
      <span>MARKET: ${{sc.market}}</span>
      <span>UNIT: ${{sc.unit}}</span>
      ${{lifecycleTag}}
    </div>
    <div class="narrative">${{sc.narrative_context}}</div>
    <table class="data-table">
      <thead><tr>${{headerCols.map(h => `<th>${{h}}</th>`).join("")}}</tr></thead>
      <tbody>${{rowsHtml}}</tbody>
    </table>
  `;
}}

async function callClaude(systemPrompt, userMessage) {{
  const response = await fetch("https://api.anthropic.com/v1/messages", {{
    method: "POST",
    headers: {{ "Content-Type": "application/json" }},
    body: JSON.stringify({{
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{{ role: "user", content: userMessage }}],
    }}),
  }});
  const data = await response.json();
  const block = (data.content || []).find(b => b.type === "text");
  const text = block ? block.text : "{{}}";
  const cleaned = text.replace(/```json|```/g, "").trim();
  try {{ return JSON.parse(cleaned); }} catch (e) {{ return {{ error: "Could not parse response", raw: text }}; }}
}}

function setStatus(msg) {{
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = msg ? "status active" : "status";
}}

function renderResults(sales, proc, harm) {{
  const risksHtml = (harm.risk_flags || []).map(r => `<span class="risk-tag">${{r}}</span>`).join("");
  const traceHtml = (harm.decision_trace || []).map(t => `
    <div class="ledger-row">
      <div class="ledger-head" onclick="this.parentElement.classList.toggle('open')">
        <span>${{t.month}}</span>
        <span><span class="lbl">Sales req</span>${{fmt(t.sales_requested)}}</span>
        <span><span class="lbl">Procurement max</span>${{fmt(t.procurement_max_feasible)}}</span>
        <span><span class="lbl">Final decision</span>${{fmt(t.final_decision)}}</span>
        <span class="arrow">▸</span>
      </div>
      <div class="ledger-body">${{t.reasoning}}</div>
    </div>
  `).join("");

  document.getElementById("results").innerHTML = `
    <div class="testimony">
      <div class="card sales">
        <div class="card-label">Sales Demand Agent</div>
        <div class="position-summary">${{sales.position_summary || ""}}</div>
        <ul>${{(sales.key_arguments || []).map(a => `<li>${{a}}</li>`).join("")}}</ul>
        <div class="note"><strong>Forecast basis:</strong> ${{sales.forecast_basis || "—"}}<br>
        <strong>Risk if denied:</strong> ${{sales.business_risk_if_denied || "—"}}</div>
      </div>
      <div class="card proc">
        <div class="card-label">Supply / Procurement Agent</div>
        <div class="position-summary">${{proc.position_summary || ""}}</div>
        <ul>${{(proc.key_arguments || []).map(a => `<li>${{a}}</li>`).join("")}}</ul>
        <div class="note"><strong>Inventory position:</strong> ${{proc.inventory_position_note || "—"}}<br>
        <strong>Proposed alternative:</strong> ${{proc.proposed_alternative || "—"}}</div>
      </div>
    </div>

    <div class="verdict">
      <div class="seal">Harmonizer · Final Decision</div>
      <div class="exec-summary">${{harm.executive_summary || ""}}</div>
      <h4>Key Rationale</h4>
      <ul>${{(harm.key_rationale || []).map(r => `<li>${{r}}</li>`).join("")}}</ul>
      <h4>Remaining Risk Flags</h4>
      <div>${{risksHtml || "—"}}</div>
    </div>

    <div class="ledger">
      <div class="ledger-title">Decision Trace — click a month to see why</div>
      ${{traceHtml}}
    </div>
  `;
}}

document.getElementById("runBtn").addEventListener("click", async () => {{
  const btn = document.getElementById("runBtn");
  btn.disabled = true;
  document.getElementById("results").innerHTML = "";
  const sc = SOP_DATA.scenarios[currentKey];
  const scenarioContext = JSON.stringify(sc);

  try {{
    setStatus("Sales Demand Agent is drafting its position...");
    const sales = await callClaude(SALES_PROMPT, "Scenario data:\\n" + scenarioContext);

    setStatus("Supply/Procurement Agent is reviewing and responding...");
    const proc = await callClaude(PROCUREMENT_PROMPT,
      "Scenario data:\\n" + scenarioContext + "\\n\\nSales Demand Agent's position:\\n" + JSON.stringify(sales));

    setStatus("Harmonizer is deliberating a final decision...");
    const harm = await callClaude(HARMONIZER_PROMPT,
      "Scenario data:\\n" + scenarioContext +
      "\\n\\nSales position:\\n" + JSON.stringify(sales) +
      "\\n\\nProcurement position:\\n" + JSON.stringify(proc));

    setStatus("");
    renderResults(sales, proc, harm);
  }} catch (err) {{
    setStatus("Error: " + err.message);
  }}
  btn.disabled = false;
}});

renderTabs();
renderDossier();
</script>
</body>
</html>
"""

with open("/home/claude/sop_demo.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print("HTML artifact written, length:", len(HTML))
