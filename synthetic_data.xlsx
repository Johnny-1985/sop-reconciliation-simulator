import json

# 단위 규칙 (실제 태양광 업계 관행 반영):
#   - 모듈(Module): MW 단위
#   - 인버터(Inverter) / ESS(배터리): 대수(unit count) 단위
#   - 리드타임: 정상 기준 2~4개월(약 8~16주). 공급 차질 시나리오는 이 밴드를 초과할 수 있음.

scenarios = {
    "scenario_a_italy_surge": {
        "title": "Italy Inverter Demand Surge",
        "unit": "units (대수)",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "이탈리아 C&I(상업/산업) 시장에서 3상 인버터 수요가 예상보다 빠르게 증가하고 있다. "
            "경쟁사(가상명: VoltRax)가 유사 스펙 제품을 20% 낮은 가격에 공급하며 점유율을 확대 중이라는 "
            "시장 정보가 있다. Sales팀은 고객 이탈을 막기 위해 즉각적인 물량 확보를 요청하고 있으나, "
            "현재 생산 공급망은 원자재 리드타임 문제로 여유가 크지 않다."
        ),
        "product": "HYB-G3 Inverter 10kW 3P",
        "market": "Italy",
        "rows": [
            {"month": "2026-08", "sales_forecast_request": 850, "current_supply_capacity": 600, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 890, "inventory_on_hand": 120},
            {"month": "2026-09", "sales_forecast_request": 1100, "current_supply_capacity": 650, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 890, "inventory_on_hand": 0},
            {"month": "2026-10", "sales_forecast_request": 1400, "current_supply_capacity": 700, "lead_time_weeks": 12, "moq": 100, "unit_cost_eur": 905, "inventory_on_hand": 0},
            {"month": "2026-11", "sales_forecast_request": 1600, "current_supply_capacity": 750, "lead_time_weeks": 12, "moq": 100, "unit_cost_eur": 905, "inventory_on_hand": 0},
            {"month": "2026-12", "sales_forecast_request": 1750, "current_supply_capacity": 800, "lead_time_weeks": 14, "moq": 100, "unit_cost_eur": 920, "inventory_on_hand": 0},
        ],
    },
    "scenario_b_poland_delay": {
        "title": "Poland Certification Delay",
        "unit": "units (대수)",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "폴란드 정부의 계통연계 인증(가상 규제명: NC-RfG Type B) 갱신 절차가 예상보다 지연되며, "
            "인증이 완료되지 않은 배터리 모델은 현지 판매가 불가능하다. Sales팀은 기존 계약된 물량을 "
            "차질 없이 공급해야 한다는 입장이고, Supply팀은 인증 완료 시점까지 "
            "공급 자체가 물리적으로 불가능하다는 입장이다 (정상 리드타임 대비 인증 지연으로 약 2개월 추가 지연)."
        ),
        "product": "ESS Battery Pack 5kWh",
        "market": "Poland",
        "rows": [
            {"month": "2026-08", "sales_forecast_request": 400, "current_supply_capacity": 400, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 1450, "inventory_on_hand": 300},
            {"month": "2026-09", "sales_forecast_request": 450, "current_supply_capacity": 150, "lead_time_weeks": 18, "moq": 50, "unit_cost_eur": 1450, "inventory_on_hand": 0},
            {"month": "2026-10", "sales_forecast_request": 500, "current_supply_capacity": 100, "lead_time_weeks": 20, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0},
            {"month": "2026-11", "sales_forecast_request": 500, "current_supply_capacity": 350, "lead_time_weeks": 14, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0},
            {"month": "2026-12", "sales_forecast_request": 550, "current_supply_capacity": 500, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 1470, "inventory_on_hand": 0},
        ],
    },
    "scenario_c_germany_oversupply": {
        "title": "Germany Residential Battery Oversupply",
        "unit": "units (대수)",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "독일 주거용 배터리 시장의 정부 보조금(가상: KfW-Home Storage Incentive)이 예상보다 "
            "일찍 축소되며 실수요가 둔화됐다. Sales팀 예측치는 기존 계약 기준으로 유지되고 있으나 "
            "실제 판매 속도는 하락 중이며, 창고에는 이미 상당한 재고가 쌓여 있다. Supply팀은 추가 "
            "생산을 즉시 중단하고 가격 조정(프로모션)을 통한 재고 소진을 제안하고 있다."
        ),
        "product": "Residential Battery 5kWh",
        "market": "Germany",
        "rows": [
            {"month": "2026-08", "sales_forecast_request": 900, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1200, "inventory_on_hand": 1800},
            {"month": "2026-09", "sales_forecast_request": 850, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1200, "inventory_on_hand": 2400},
            {"month": "2026-10", "sales_forecast_request": 800, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1180, "inventory_on_hand": 3050},
            {"month": "2026-11", "sales_forecast_request": 750, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1180, "inventory_on_hand": 3700},
            {"month": "2026-12", "sales_forecast_request": 700, "current_supply_capacity": 900, "lead_time_weeks": 10, "moq": 100, "unit_cost_eur": 1150, "inventory_on_hand": 4350},
        ],
    },
    "scenario_d_france_module": {
        "title": "France Module Capacity Allocation",
        "unit": "modules (quantity); MWp derived via POWERCLASS(Wp) x quantity / 10^6",
        "powerclass_wp": 590,
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "프랑스 유틸리티 스케일 프로젝트향 모듈 수주가 늘며 Sales팀은 해당 고객사에 배정할 "
            "모듈 물량(MWp 기준) 확대를 요청하고 있다. 그러나 전체 생산 CAPA는 여러 국가 물량에 "
            "분산 배정되어야 하며, 특정 국가에 과도하게 배정할 경우 다른 시장向 공급에 차질이 "
            "생길 수 있다는 것이 Supply팀의 입장이다. 원자재(웨이퍼) 조달 리드타임도 고려 대상이다."
        ),
        "product": "Q.TRON Module (가상 모델명, 590Wp)",
        "market": "France",
        "rows": [
            {"month": "2026-08", "sales_forecast_request": 30500, "current_supply_capacity": 23700, "lead_time_weeks": 10, "moq": 500, "unit_cost_eur": 56, "inventory_on_hand": 3400},
            {"month": "2026-09", "sales_forecast_request": 37300, "current_supply_capacity": 25400, "lead_time_weeks": 11, "moq": 500, "unit_cost_eur": 55, "inventory_on_hand": 0},
            {"month": "2026-10", "sales_forecast_request": 44100, "current_supply_capacity": 27100, "lead_time_weeks": 12, "moq": 500, "unit_cost_eur": 55, "inventory_on_hand": 0},
            {"month": "2026-11", "sales_forecast_request": 47500, "current_supply_capacity": 28800, "lead_time_weeks": 12, "moq": 500, "unit_cost_eur": 54, "inventory_on_hand": 0},
            {"month": "2026-12", "sales_forecast_request": 50800, "current_supply_capacity": 30500, "lead_time_weeks": 14, "moq": 500, "unit_cost_eur": 54, "inventory_on_hand": 0},
        ],
    },
    "scenario_e_new_launch": {
        "title": "Germany New Compact ESS Launch",
        "unit": "units (대수)",
        "product_lifecycle_stage": "new_launch",
        "launch_month": "2026-10",
        "narrative_context": (
            "신제품 Q.SAVE Compact 3kWh가 2026년 10월 독일 시장에 출시될 예정이다. 과거 판매 데이터가 "
            "존재하지 않아, Sales팀의 요청 물량은 유사 제품(기존 5kWh 모델)의 초기 3개월 판매 추이와 "
            "시장 규모 추정(market sizing)에 기반한 것이며 실제 트렌드 데이터가 아니다. 신규 생산 라인은 "
            "출시 초기 램프업 단계로, 정상 CAPA의 60~80% 수준에서 시작해 점진적으로 확대된다. "
            "이 시나리오는 Agent가 '과거 추세 연장'이 아니라 '유사 제품 유추 + 시장 추정'이라는 "
            "다른 근거로 판단해야 함을 보여주기 위한 것이다."
        ),
        "product": "Q.SAVE Compact 3kWh (NEW)",
        "market": "Germany",
        "rows": [
            {"month": "2026-10", "sales_forecast_request": 300, "current_supply_capacity": 180, "lead_time_weeks": 12, "moq": 50, "unit_cost_eur": 780, "inventory_on_hand": 0},
            {"month": "2026-11", "sales_forecast_request": 480, "current_supply_capacity": 260, "lead_time_weeks": 12, "moq": 50, "unit_cost_eur": 770, "inventory_on_hand": 0},
            {"month": "2026-12", "sales_forecast_request": 620, "current_supply_capacity": 380, "lead_time_weeks": 10, "moq": 50, "unit_cost_eur": 760, "inventory_on_hand": 0},
        ],
    },
}

# Derive MWp for the module scenario (POWERCLASS_Wp * quantity / 10^6). Computed here in Python;
# the Excel version recreates this as a live formula rather than a hardcoded value.
_mod = scenarios["scenario_d_france_module"]
for row in _mod["rows"]:
    row["sales_forecast_mwp"] = round(_mod["powerclass_wp"] * row["sales_forecast_request"] / 1_000_000, 3)
    row["current_supply_capacity_mwp"] = round(_mod["powerclass_wp"] * row["current_supply_capacity"] / 1_000_000, 3)

# Target inventory level (1.5 months of demand, using current-month sales_forecast_request as the
# demand proxy for Phase 1 simplicity) and resulting surplus/deficit gap, applied to every scenario.
TARGET_INVENTORY_MONTHS = 1.5
for sc in scenarios.values():
    for row in sc["rows"]:
        target = round(TARGET_INVENTORY_MONTHS * row["sales_forecast_request"])
        row["target_inventory_level"] = target
        row["inventory_gap"] = row["inventory_on_hand"] - target

meta = {
    "company_name": "SunArc Solar (fictional company)",
    "disclaimer": "모든 데이터는 포트폴리오 데모 목적의 가상 데이터이며, 특정 실존 기업의 데이터가 아닙니다.",
    "schema_version": "1.2",
    "target_inventory_months": 1.5,
    "unit_convention": {
        "module": "수량(quantity) 기준으로 입력하며, MWp = POWERCLASS(Wp) x 수량 / 10^6 으로 환산 (예: 590Wp x 30,500장 / 10^6 = 17.995 MWp)",
        "inverter": "units / 대수",
        "ess_battery": "units / 대수",
        "lead_time_baseline": "정상 기준 2~4개월 (약 8~16주). 공급 차질 시나리오는 이 밴드를 초과할 수 있음.",
    },
    "field_definitions": {
        "sales_forecast_request": "Sales팀이 요청하는 월별 물량 (제품별 단위는 scenario.unit 참조)",
        "current_supply_capacity": "해당 월 생산/조달 가능 물량 (동일 단위)",
        "lead_time_weeks": "발주 후 공급까지 소요되는 리드타임 (주 단위, 정상 기준 8~16주)",
        "moq": "최소발주단위",
        "unit_cost_eur": "단가 (EUR). 모듈은 MW당 단가, 인버터/ESS는 대당 단가.",
        "inventory_on_hand": "월초 기준 현재고 (동일 단위)",
        "target_inventory_level": "적정재고 수준 = sales_forecast_request(해당 월 수요 proxy) x target_inventory_months(1.5). Phase 1 단순화를 위해 해당 월 수요를 기준으로 산정 (향후 이동평균으로 고도화 가능)",
        "inventory_gap": "inventory_on_hand - target_inventory_level. 양수=재고 과잉(오버스톡), 음수=재고 부족(공급 시급성 높음)",
        "product_lifecycle_stage": "'established'(기존 제품, 과거 추세 기반 판단 가능) 또는 'new_launch'(신제품, 과거 데이터 없음)",
        "launch_month": "product_lifecycle_stage가 new_launch인 경우, 출시 월. established 제품은 null",
    },
}

output = {"meta": meta, "scenarios": scenarios}

with open("/home/claude/synthetic_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("JSON written.")
