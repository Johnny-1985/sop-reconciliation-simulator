<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SunArc Solar — S&OP Reconciliation Simulator</title>
<style>
:root {
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
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 32px 20px 80px;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--sans);
  line-height: 1.5;
}
.wrap { max-width: 920px; margin: 0 auto; }

.masthead {
  border-bottom: 3px solid var(--ink);
  padding-bottom: 18px; margin-bottom: 24px;
}
.eyebrow {
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--ink-soft); margin-bottom: 6px;
}
h1 {
  font-family: var(--serif); font-size: 34px; font-weight: 700;
  margin: 0 0 6px; letter-spacing: -0.01em;
}
.subtitle { color: var(--ink-soft); font-size: 14.5px; }

.tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 18px; }
.tab {
  font-family: var(--mono); font-size: 12px; padding: 9px 14px;
  background: var(--paper); border: 1px solid var(--rule); border-bottom: none;
  border-radius: 6px 6px 0 0; cursor: pointer; color: var(--ink-soft);
  position: relative; top: 1px;
}
.tab.active {
  background: var(--ink); color: var(--paper); border-color: var(--ink);
  font-weight: 600;
}

.dossier {
  background: var(--paper); border: 1px solid var(--rule); border-radius: 0 6px 6px 6px;
  padding: 22px 24px; margin-bottom: 20px;
}
.dossier h2 { font-family: var(--serif); font-size: 21px; margin: 0 0 4px; }
.meta-row {
  font-family: var(--mono); font-size: 12px; color: var(--ink-soft);
  margin-bottom: 12px; display: flex; gap: 16px; flex-wrap: wrap;
}
.lifecycle-tag {
  display: inline-block; padding: 1px 7px; border-radius: 3px;
  background: var(--harm-bg); color: var(--harm); font-weight: 600;
}
.narrative { font-size: 14px; color: var(--ink); margin-bottom: 16px; }

table.data-table { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 12px; }
table.data-table th {
  text-align: right; padding: 6px 8px; border-bottom: 2px solid var(--ink);
  color: var(--ink-soft); font-weight: 600; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em;
}
table.data-table th:first-child, table.data-table td:first-child { text-align: left; }
table.data-table td { text-align: right; padding: 6px 8px; border-bottom: 1px solid var(--rule); }
.gap-pos { color: var(--surplus); font-weight: 600; }
.gap-neg { color: var(--deficit); font-weight: 600; }

.run-btn {
  display: block; width: 100%; margin-top: 20px; padding: 14px;
  background: var(--harm); color: var(--paper); border: none; border-radius: 6px;
  font-family: var(--sans); font-size: 14.5px; font-weight: 700; letter-spacing: 0.02em;
  cursor: pointer;
}
.run-btn:disabled { opacity: 0.5; cursor: default; }
.run-btn:hover:not(:disabled) { filter: brightness(1.08); }

.status {
  font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft);
  margin: 14px 0; min-height: 18px;
}
.status.active::before { content: "▸ "; color: var(--harm); }

.testimony { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }
@media (max-width: 700px) { .testimony { grid-template-columns: 1fr; } }
.card { border-radius: 6px; padding: 18px 20px; border: 1px solid; }
.card.sales { background: var(--sales-bg); border-color: var(--sales-line); }
.card.proc { background: var(--proc-bg); border-color: var(--proc-line); }
.card-label { font-family: var(--mono); font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700; margin-bottom: 6px; }
.card.sales .card-label { color: var(--sales); }
.card.proc .card-label { color: var(--proc); }
.position-summary { font-family: var(--serif); font-size: 15.5px; margin-bottom: 12px; }
.card ul { margin: 0 0 12px; padding-left: 18px; font-size: 13.5px; }
.card li { margin-bottom: 5px; }
.card .note { font-size: 12.5px; color: var(--ink-soft); border-top: 1px dashed var(--rule); padding-top: 10px; margin-top: 10px; }

.verdict {
  background: var(--harm-bg); border: 1px solid var(--harm-line); border-radius: 6px;
  padding: 22px 24px; margin: 20px 0;
}
.seal {
  display: inline-block; font-family: var(--mono); font-size: 11px; font-weight: 700;
  letter-spacing: 0.1em; color: var(--paper); background: var(--harm);
  padding: 4px 10px; border-radius: 3px; margin-bottom: 12px;
}
.exec-summary { font-family: var(--serif); font-size: 16px; margin-bottom: 14px; }
.verdict h4 { font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--harm); margin: 14px 0 6px; }
.verdict ul { margin: 0; padding-left: 18px; font-size: 13.5px; }
.risk-tag {
  display: inline-block; font-size: 12px; padding: 3px 9px; border-radius: 3px;
  background: #fff; border: 1px solid var(--deficit); color: var(--deficit); margin: 3px 6px 0 0;
}

.ledger { margin-top: 22px; }
.ledger-title { font-family: var(--mono); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-soft); margin-bottom: 8px; }
.ledger-row {
  background: var(--paper); border: 1px solid var(--rule); border-radius: 4px;
  margin-bottom: 6px; overflow: hidden;
}
.ledger-head {
  display: grid; grid-template-columns: 90px 1fr 1fr 1fr 20px; gap: 10px;
  padding: 10px 14px; cursor: pointer; align-items: center;
  font-family: var(--mono); font-size: 12.5px;
}
.ledger-head .lbl { font-size: 9.5px; text-transform: uppercase; color: var(--ink-soft); display: block; }
.ledger-head .arrow { text-align: right; color: var(--ink-soft); transition: transform 0.15s; }
.ledger-row.open .arrow { transform: rotate(90deg); }
.ledger-body {
  display: none; padding: 0 14px 14px 14px; font-size: 13px; color: var(--ink);
  border-top: 1px dashed var(--rule);
}
.ledger-row.open .ledger-body { display: block; padding-top: 10px; }

.footer-note { font-family: var(--mono); font-size: 11px; color: var(--ink-soft); margin-top: 40px; text-align: center; }
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
const SOP_DATA = {"meta": {"company_name": "SunArc Solar (fictional company)", "disclaimer": "모든 데이터는 포트폴리오 데모 목적의 가상 데이터이며, 특정 실존 기업의 데이터가 아닙니다.", "schema_version": "1.2", "target_inventory_months": 1.5, "unit_convention": {"module": "수량(quantity) 기준으로 입력하며, MWp = POWERCLASS(Wp) x 수량 / 10^6 으로 환산 (예: 590Wp x 30,500장 / 10^6 = 17.995 MWp)", "inverter": "units / 대수", "ess_battery": "units / 대수", "lead_time_baseline": "정상 기준 2~4개월 (약 8~16주). 공급 차질 시나리오는 이 밴드를 초과할 수 있음."}, "field_definitions": {"sales_forecast_request": "Sales팀이 요청하는 월별 물량 (제품별 단위는 scenario.unit 참조)", "current_supply_capacity": "해당 월 생산/조달 가능 물량 (동일 단위)", "lead_time_weeks": "발주 후 공급까지 소요되는 리드타임 (주 단위, 정상 기준 8~16주)", "moq": "최소발주단위", "unit_cost_eur": "단가 (EUR). 모듈은 MW당 단가, 인버터/ESS는 대당 단가.", "inventory_on_hand": "월초 기준 현재고 (동일 단위)", "target_inventory_level": "적정재고 수준 = sales_forecast_request(해당 월 수요 proxy) x target_inventory_months(1.5). Phase 1 단순화를 위해 해당 월 수요를 기준으로 산정 (향후 이동평균으로 고도화 가능)", "inventory_gap": "inventory_on_hand - target_inventory_level. 양수=재고 과잉(오버스톡), 음수=재고 부족(공급 시급성 높음)", "product_lifecycle_stage": "'established'(기존 제품, 과거 추세 기반 판단 가능) 또는 'new_launch'(신제품, 과거 데이터 없음)", "launch_month": "product_lifecycle_stage가 new_launch인 경우, 출시 월. established 제품은 null"}}, "scenarios": {"scenario_a_italy_surge": {"title": "Italy Inverter Demand Surge", "unit": "units (대수)", "product_lifecycle_stage": "established", "launch_month": null, "narrative_context": "이탈리아 C&I(상업/산업) 시장에서 3상 인버터 수요가 예상보다 빠르게 증가하고 있다. 경쟁사(가상명: VoltRax)가 유사 스펙 제품을 20% 낮은 가격에 공급하며 점유율을 확대 중이라는 시장 정보가 있다. Sales팀은 고객 이탈을 막기 위해 즉각적인 물량 확보를 요청하고 있으나, 현재 생산 공급망은 원자재 리드타임 문제로 여유가 크지 않다.", "product": "HYB-G3 Inverter 10kW 3P", "market": "Italy", "rows": [{"month": "2026-08", "sales_forecast_request": 850, "current_supply_capacity": 600, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 890, "inventory_on_hand": 120, "target_inventory_level": 1275, "inventory_gap": -1155}, {"month": "2026-09", "sales_forecast_request": 1100, "current_supply_capacity": 650, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 890, "inventory_on_hand": 0, "target_inventory_level": 1650, "inventory_gap": -1650}, {"month": "2026-10", "sales_forecast_request": 1400, "current_supply_capacity": 700, "lead_time_weeks": 12, "moq": 100, "unit_cost_eur": 905, "inventory_on_hand": 0, "target_inventory_level": 2100, "inventory_gap": -2100}, {"month": "2026-11", "sales_forecast_request": 1600, "current_supply_capacity": 750, "lead_time_weeks": 12, "moq": 100, "unit_cost_eur": 905, "inventory_on_hand": 0, "target_inventory_level": 2400, "inventory_gap": -2400}, {"month": "2026-12", "sales_forecast_request": 1750, "current_supply_capacity": 800, "lead_time_weeks": 14, "moq": 100, "unit_cost_eur": 920, "inventory_on_hand": 0, "target_inventory_level": 2625, "inventory_gap": -2625}]}, "scenario_b_poland_delay": {"title": "Poland Certification Delay", "unit": "units (대수)", "product_lifecycle_stage": "established", "launch_month": null, "narrative_context": "폴란드 정부의 계통연계 인증(가상 규제명: NC-RfG Type B) 갱신 절차가 예상보다 지연되며, 인증이 완료되지 않은 배터리 모델은 현지 판매가 불가능하다. Sales팀은 기존 계약된 물량을 차질 없이 공급해야 한다는 입장이고, Supply팀은 인증 완료 시점까지 공급 자체가 물리적으로 불가능하다는 입장이다 (정상 리드타임 대비 인증 지연으로 약 2개월 추가 지연).", "product": "ESS Battery Pack 5kWh", "market": "Poland", "rows": [{"month": "2026-08", "sales_forecast_request": 400, "current_supply_capacity": 400, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 1450, "inventory_on_hand": 300, "target_inventory_level": 600, "inventory_gap": -300}, {"month": "2026-09", "sales_forecast_request": 450, "current_supply_capacity": 150, "lead_time_weeks": 18, "moq": 50, "unit_cost_eur": 1450, "inventory_on_hand": 0, "target_inventory_level": 675, "inventory_gap": -675}, {"month": "2026-10", "sales_forecast_request": 500, "current_supply_capacity": 100, "lead_time_weeks": 20, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0, "target_inventory_level": 750, "inventory_gap": -750}, {"month": "2026-11", "sales_forecast_request": 500, "current_supply_capacity": 350, "lead_time_weeks": 14, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0, "target_inventory_level": 750, "inventory_gap": -750}, {"month": "2026-12", "sales_forecast_request": 550, "current_supply_capacity": 500, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0, "target_inventory_level": 825, "inventory_gap": -825}]}, "scenario_c_germany_oversupply": {"title": "Germany Residential Battery Oversupply", "unit": "units (대수)", "product_lifecycle_stage": "established", "launch_month": null, "narrative_context": "독일 주거용 배터리 시장의 정부 보조금(가상: KfW-Home Storage Incentive)이 예상보다 일찍 축소되며 실수요가 둔화됐다. Sales팀 예측치는 기존 계약 기준으로 유지되고 있으나 실제 판매 속도는 하락 중이며, 창고에는 이미 상당한 재고가 쌓여 있다. Supply팀은 추가 생산을 즉시 중단하고 가격 조정(프로모션)을 통한 재고 소진을 제안하고 있다.", "product": "Residential Battery 5kWh", "market": "Germany", "rows": [{"month": "2026-08", "sales_forecast_request": 900, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1200, "inventory_on_hand": 1800, "target_inventory_level": 1350, "inventory_gap": 450}, {"month": "2026-09", "sales_forecast_request": 850, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1200, "inventory_on_hand": 2400, "target_inventory_level": 1275, "inventory_gap": 1125}, {"month": "2026-10", "sales_forecast_request": 800, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1180, "inventory_on_hand": 3050, "target_inventory_level": 1200, "inventory_gap": 1850}, {"month": "2026-11", "sales_forecast_request": 750, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1180, "inventory_on_hand": 3700, "target_inventory_level": 1125, "inventory_gap": 2575}, {"month": "2026-12", "sales_forecast_request": 700, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1150, "inventory_on_hand": 4350, "target_inventory_level": 1050, "inventory_gap": 3300}]}, "scenario_d_france_module": {"title": "France Module Capacity Allocation", "unit": "modules (quantity); MWp derived via POWERCLASS(Wp) x quantity / 10^6", "powerclass_wp": 590, "product_lifecycle_stage": "established", "launch_month": null, "narrative_context": "프랑스 유틸리티 스케일 프로젝트향 모듈 수주가 늘며 Sales팀은 해당 고객사에 배정할 모듈 물량(MWp 기준) 확대를 요청하고 있다. 그러나 전체 생산 CAPA는 여러 국가 물량에 분산 배정되어야 하며, 특정 국가에 과도하게 배정할 경우 다른 시장向 공급에 차질이 생길 수 있다는 것이 Supply팀의 입장이다. 원자재(웨이퍼) 조달 리드타임도 고려 대상이다.", "product": "Q.TRON Module (가상 모델명, 590Wp)", "market": "France", "rows": [{"month": "2026-08", "sales_forecast_request": 30500, "current_supply_capacity": 23700, "lead_time_weeks": 10, "moq": 500, "unit_cost_eur": 56, "inventory_on_hand": 3400, "sales_forecast_mwp": 17.995, "current_supply_capacity_mwp": 13.983, "target_inventory_level": 45750, "inventory_gap": -42350}, {"month": "2026-09", "sales_forecast_request": 37300, "current_supply_capacity": 25400, "lead_time_weeks": 11, "moq": 500, "unit_cost_eur": 55, "inventory_on_hand": 0, "sales_forecast_mwp": 22.007, "current_supply_capacity_mwp": 14.986, "target_inventory_level": 55950, "inventory_gap": -55950}, {"month": "2026-10", "sales_forecast_request": 44100, "current_supply_capacity": 27100, "lead_time_weeks": 12, "moq": 500, "unit_cost_eur": 55, "inventory_on_hand": 0, "sales_forecast_mwp": 26.019, "current_supply_capacity_mwp": 15.989, "target_inventory_level": 66150, "inventory_gap": -66150}, {"month": "2026-11", "sales_forecast_request": 47500, "current_supply_capacity": 28800, "lead_time_weeks": 12, "moq": 500, "unit_cost_eur": 54, "inventory_on_hand": 0, "sales_forecast_mwp": 28.025, "current_supply_capacity_mwp": 16.992, "target_inventory_level": 71250, "inventory_gap": -71250}, {"month": "2026-12", "sales_forecast_request": 50800, "current_supply_capacity": 30500, "lead_time_weeks": 14, "moq": 500, "unit_cost_eur": 54, "inventory_on_hand": 0, "sales_forecast_mwp": 29.972, "current_supply_capacity_mwp": 17.995, "target_inventory_level": 76200, "inventory_gap": -76200}]}, "scenario_e_new_launch": {"title": "Germany New Compact ESS Launch", "unit": "units (대수)", "product_lifecycle_stage": "new_launch", "launch_month": "2026-10", "narrative_context": "신제품 Q.SAVE Compact 3kWh가 2026년 10월 독일 시장에 출시될 예정이다. 과거 판매 데이터가 존재하지 않아, Sales팀의 요청 물량은 유사 제품(기존 5kWh 모델)의 초기 3개월 판매 추이와 시장 규모 추정(market sizing)에 기반한 것이며 실제 트렌드 데이터가 아니다. 신규 생산 라인은 출시 초기 램프업 단계로, 정상 CAPA의 60~80% 수준에서 시작해 점진적으로 확대된다. 이 시나리오는 Agent가 '과거 추세 연장'이 아니라 '유사 제품 유추 + 시장 추정'이라는 다른 근거로 판단해야 함을 보여주기 위한 것이다.", "product": "Q.SAVE Compact 3kWh (NEW)", "market": "Germany", "rows": [{"month": "2026-10", "sales_forecast_request": 300, "current_supply_capacity": 180, "lead_time_weeks": 12, "moq": 50, "unit_cost_eur": 780, "inventory_on_hand": 0, "target_inventory_level": 450, "inventory_gap": -450}, {"month": "2026-11", "sales_forecast_request": 480, "current_supply_capacity": 260, "lead_time_weeks": 12, "moq": 50, "unit_cost_eur": 770, "inventory_on_hand": 0, "target_inventory_level": 720, "inventory_gap": -720}, {"month": "2026-12", "sales_forecast_request": 620, "current_supply_capacity": 380, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 760, "inventory_on_hand": 0, "target_inventory_level": 930, "inventory_gap": -930}]}}};
const SALES_PROMPT = "You are the Sales Demand Agent in an S&OP (Sales & Operations Planning) reconciliation simulation. Your role is to represent the commercial/market perspective.\n\nYour mandate:\n- Advocate for securing enough supply volume to capture market opportunity and protect against customer churn or competitive loss.\n- Base every argument on the specific numeric data provided (sales_forecast_request, market/competitive context in narrative_context). Do not invent numbers not present in the data.\n- Check product_lifecycle_stage. If it is \"established\", you may reason from the trend across months as if it reflects real historical momentum. If it is \"new_launch\" (see launch_month), there is NO real sales history - say so explicitly, and instead ground your argument in market-sizing logic and analogy to a comparable existing product (as described in narrative_context). Flag that your forecast confidence is lower than for an established product.\n- Be persuasive but professional. Acknowledge supply constraints exist, but argue why the business risk of under-supplying outweighs the operational difficulty.\n- Quantify the downside: estimate revenue-at-risk or churn risk in plain business terms based on the gap between sales_forecast_request and current_supply_capacity.\n\nRespond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:\n{\n  \"agent\": \"sales_demand\",\n  \"position_summary\": \"1-2 sentence summary of your stance\",\n  \"key_arguments\": [\"argument 1\", \"argument 2\", \"argument 3\"],\n  \"requested_volume_by_month\": {\"month\": number},\n  \"forecast_basis\": \"trend-based, or market-sizing/analog for new launches, with 1 sentence explaining which\",\n  \"business_risk_if_denied\": \"1-2 sentence risk statement\"\n}";
const PROCUREMENT_PROMPT = "You are the Supply/Procurement Agent in an S&OP reconciliation simulation. Your role is to represent operational feasibility and cost discipline.\n\nYour mandate:\n- You have just read the Sales Demand Agent's argument (provided below). Respond directly to their specific requested volumes.\n- Base every argument on the specific numeric data provided (current_supply_capacity, lead_time_weeks, moq, unit_cost_eur, inventory_on_hand). Do not invent numbers not present in the data.\n- Identify precisely which months the requested volume exceeds feasible capacity, and by how much.\n- Inventory position matters: the target inventory level is 1.5 months of demand (target_inventory_level in the data). If inventory_gap is positive (existing stock already exceeds 1.5 months of demand), argue for restraint even if Sales' request looks feasible. If inventory_gap is negative (stock is below the 1.5-month target), that strengthens the case for approving more supply.\n- Where possible, propose a constructive alternative (partial fulfillment, phased ramp-up, expedited lead time at cost premium) rather than a flat refusal. If genuinely infeasible for a given month, say so clearly.\n\nRespond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:\n{\n  \"agent\": \"supply_procurement\",\n  \"position_summary\": \"1-2 sentence summary of your stance\",\n  \"key_arguments\": [\"argument 1\", \"argument 2\", \"argument 3\"],\n  \"max_feasible_volume_by_month\": {\"month\": number},\n  \"inventory_position_note\": \"1 sentence noting surplus or deficit vs the 1.5-month target and how it affects your position\",\n  \"proposed_alternative\": \"1-2 sentence constructive proposal, if any\"\n}";
const HARMONIZER_PROMPT = "You are the Harmonizer in an S&OP reconciliation simulation, playing the role of an Integrated Planning Manager who sits between Sales and Supply/Procurement. You have read both agents' positions (provided below).\n\nYour mandate:\n- Do not simply average the two positions. Make a reasoned judgment call, the way an experienced planning manager would in a live monthly S&OP meeting.\n- Weigh business risk (from Sales) against operational/financial risk (from Procurement) explicitly.\n- Produce ONE final recommended volume per month.\n- CRITICAL - full traceability: an approver reviewing this must be able to see, for EVERY month, what each side argued and exactly why you landed on your final number. Reasoning can differ month to month.\n- Factor in inventory position explicitly: a surplus is a reason to lean toward the lower/Procurement number even if Sales' request is technically producible; a deficit strengthens the case for the higher/Sales number.\n- If product_lifecycle_stage is \"new_launch\", flag that Sales' forecast_basis is market-sizing/analog rather than trend data, treat as higher uncertainty, and consider a more conservative number with a faster review cycle.\n- Flag any risk that remains even after your decision.\n\nRespond with ONLY a valid JSON object, no markdown fences, no preamble, in this exact shape:\n{\n  \"agent\": \"harmonizer\",\n  \"decision_trace\": [\n    {\"month\": \"month\", \"sales_requested\": number, \"procurement_max_feasible\": number, \"final_decision\": number, \"reasoning\": \"1-2 sentence month-specific reason\"}\n  ],\n  \"key_rationale\": [\"overall reason 1\", \"overall reason 2\", \"overall reason 3\"],\n  \"risk_flags\": [\"remaining risk 1\", \"remaining risk 2\"],\n  \"executive_summary\": \"3-4 sentence summary suitable for an executive S&OP readout\"\n}";

const scenarioKeys = Object.keys(SOP_DATA.scenarios);
let currentKey = scenarioKeys[0];

function fmt(n) { return typeof n === "number" ? n.toLocaleString() : n; }

function renderTabs() {
  const tabs = document.getElementById("tabs");
  tabs.innerHTML = scenarioKeys.map((k, i) => {
    const label = "SCN-" + String.fromCharCode(65 + i);
    return `<div class="tab ${k === currentKey ? "active" : ""}" data-key="${k}">${label}</div>`;
  }).join("");
  tabs.querySelectorAll(".tab").forEach(el => {
    el.addEventListener("click", () => {
      currentKey = el.dataset.key;
      document.getElementById("results").innerHTML = "";
      document.getElementById("status").textContent = "";
      renderTabs();
      renderDossier();
    });
  });
}

function renderDossier() {
  const sc = SOP_DATA.scenarios[currentKey];
  const lifecycleTag = sc.product_lifecycle_stage === "new_launch"
    ? `<span class="lifecycle-tag">NEW LAUNCH · ${sc.launch_month}</span>`
    : `<span class="meta-row">established product</span>`;

  const isModule = "powerclass_wp" in sc;
  let headerCols = ["Month", "Sales Req", "Supply Cap", "Lead Time", "Inventory", "Target (1.5mo)", "Gap"];
  let rowsHtml = sc.rows.map(r => {
    const gapClass = r.inventory_gap >= 0 ? "gap-pos" : "gap-neg";
    const gapLabel = r.inventory_gap >= 0 ? "+" + fmt(r.inventory_gap) : fmt(r.inventory_gap);
    return `<tr>
      <td>${r.month}</td>
      <td>${fmt(r.sales_forecast_request)}</td>
      <td>${fmt(r.current_supply_capacity)}</td>
      <td>${r.lead_time_weeks}w</td>
      <td>${fmt(r.inventory_on_hand)}</td>
      <td>${fmt(r.target_inventory_level)}</td>
      <td class="${gapClass}">${gapLabel}</td>
    </tr>`;
  }).join("");

  document.getElementById("dossier").innerHTML = `
    <h2>${sc.title}</h2>
    <div class="meta-row">
      <span>PRODUCT: ${sc.product}</span>
      <span>MARKET: ${sc.market}</span>
      <span>UNIT: ${sc.unit}</span>
      ${lifecycleTag}
    </div>
    <div class="narrative">${sc.narrative_context}</div>
    <table class="data-table">
      <thead><tr>${headerCols.map(h => `<th>${h}</th>`).join("")}</tr></thead>
      <tbody>${rowsHtml}</tbody>
    </table>
  `;
}

async function callClaude(systemPrompt, userMessage) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }],
    }),
  });
  const data = await response.json();
  const block = (data.content || []).find(b => b.type === "text");
  const text = block ? block.text : "{}";
  const cleaned = text.replace(/```json|```/g, "").trim();
  try { return JSON.parse(cleaned); } catch (e) { return { error: "Could not parse response", raw: text }; }
}

function setStatus(msg) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = msg ? "status active" : "status";
}

function renderResults(sales, proc, harm) {
  const risksHtml = (harm.risk_flags || []).map(r => `<span class="risk-tag">${r}</span>`).join("");
  const traceHtml = (harm.decision_trace || []).map(t => `
    <div class="ledger-row">
      <div class="ledger-head" onclick="this.parentElement.classList.toggle('open')">
        <span>${t.month}</span>
        <span><span class="lbl">Sales req</span>${fmt(t.sales_requested)}</span>
        <span><span class="lbl">Procurement max</span>${fmt(t.procurement_max_feasible)}</span>
        <span><span class="lbl">Final decision</span>${fmt(t.final_decision)}</span>
        <span class="arrow">▸</span>
      </div>
      <div class="ledger-body">${t.reasoning}</div>
    </div>
  `).join("");

  document.getElementById("results").innerHTML = `
    <div class="testimony">
      <div class="card sales">
        <div class="card-label">Sales Demand Agent</div>
        <div class="position-summary">${sales.position_summary || ""}</div>
        <ul>${(sales.key_arguments || []).map(a => `<li>${a}</li>`).join("")}</ul>
        <div class="note"><strong>Forecast basis:</strong> ${sales.forecast_basis || "—"}<br>
        <strong>Risk if denied:</strong> ${sales.business_risk_if_denied || "—"}</div>
      </div>
      <div class="card proc">
        <div class="card-label">Supply / Procurement Agent</div>
        <div class="position-summary">${proc.position_summary || ""}</div>
        <ul>${(proc.key_arguments || []).map(a => `<li>${a}</li>`).join("")}</ul>
        <div class="note"><strong>Inventory position:</strong> ${proc.inventory_position_note || "—"}<br>
        <strong>Proposed alternative:</strong> ${proc.proposed_alternative || "—"}</div>
      </div>
    </div>

    <div class="verdict">
      <div class="seal">Harmonizer · Final Decision</div>
      <div class="exec-summary">${harm.executive_summary || ""}</div>
      <h4>Key Rationale</h4>
      <ul>${(harm.key_rationale || []).map(r => `<li>${r}</li>`).join("")}</ul>
      <h4>Remaining Risk Flags</h4>
      <div>${risksHtml || "—"}</div>
    </div>

    <div class="ledger">
      <div class="ledger-title">Decision Trace — click a month to see why</div>
      ${traceHtml}
    </div>
  `;
}

document.getElementById("runBtn").addEventListener("click", async () => {
  const btn = document.getElementById("runBtn");
  btn.disabled = true;
  document.getElementById("results").innerHTML = "";
  const sc = SOP_DATA.scenarios[currentKey];
  const scenarioContext = JSON.stringify(sc);

  try {
    setStatus("Sales Demand Agent is drafting its position...");
    const sales = await callClaude(SALES_PROMPT, "Scenario data:\n" + scenarioContext);

    setStatus("Supply/Procurement Agent is reviewing and responding...");
    const proc = await callClaude(PROCUREMENT_PROMPT,
      "Scenario data:\n" + scenarioContext + "\n\nSales Demand Agent's position:\n" + JSON.stringify(sales));

    setStatus("Harmonizer is deliberating a final decision...");
    const harm = await callClaude(HARMONIZER_PROMPT,
      "Scenario data:\n" + scenarioContext +
      "\n\nSales position:\n" + JSON.stringify(sales) +
      "\n\nProcurement position:\n" + JSON.stringify(proc));

    setStatus("");
    renderResults(sales, proc, harm);
  } catch (err) {
    setStatus("Error: " + err.message);
  }
  btn.disabled = false;
});

renderTabs();
renderDossier();
</script>
</body>
</html>
