import json

# Unit conventions (reflecting real solar-industry practice):
#   - Module: entered as a quantity (count), converted to MWp
#   - Inverter / ESS (battery): unit count
#   - Lead time: normal baseline is 2-4 months (~8-16 weeks). Supply-disruption
#     scenarios may exceed this band.

scenarios = {
    "scenario_a_italy_surge": {
        "title": "Italy Inverter Demand Surge",
        "unit": "units",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "Demand for three-phase inverters in the Italian C&I (commercial & "
            "industrial) segment is growing faster than expected. Market intelligence "
            "suggests a competitor (fictional name: VoltRax) is gaining share by "
            "offering a comparable spec at a 20% lower price. Sales is requesting an "
            "immediate volume increase to prevent customer churn, but current "
            "production capacity has little slack due to raw-material lead-time "
            "constraints."
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
        "unit": "units",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "The renewal of Poland's grid-connection certification (fictional "
            "regulation name: NC-RfG Type B) is taking longer than expected, and "
            "battery models without completed certification cannot legally be sold "
            "in the country. Sales insists that already-contracted volumes must "
            "still be delivered on schedule, while Procurement maintains that supply "
            "is physically impossible until certification is complete — adding "
            "roughly two months of delay on top of the normal lead time."
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
        "unit": "units",
        "product_lifecycle_stage": "established",
        "launch_month": None,
        "narrative_context": (
            "Germany's residential battery subsidy (fictional program: KfW-Home "
            "Storage Incentive) was scaled back earlier than expected, slowing real "
            "demand. Sales' forecast still reflects the originally contracted "
            "volumes, but actual sell-through has slowed and the warehouse already "
            "holds a significant surplus. Procurement is proposing an immediate "
            "halt to further production and a price action (promotion) to clear "
            "the excess stock."
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
            "Module orders for utility-scale projects in France are increasing, and "
            "Sales is requesting a larger MWp allocation for this customer. However, "
            "total production capacity must be split across multiple countries, and "
            "Procurement's position is that over-allocating to one market risks "
            "disrupting supply to others. Wafer procurement lead time is also a "
            "factor."
        ),
        "product": "Q.TRON Module (fictional model, 590Wp)",
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
        "unit": "units",
        "product_lifecycle_stage": "new_launch",
        "launch_month": "2026-10",
        "narrative_context": (
            "The new Q.SAVE Compact 3kWh model is scheduled to launch in Germany in "
            "October 2026. No historical sales data exists — Sales' requested "
            "volume is based on the early sell-through pattern of a comparable "
            "existing product (the 5kWh model) and a market-sizing estimate, not on "
            "actual trend data. The new production line is in its initial ramp-up "
            "phase, starting at 60-80% of normal capacity and expanding gradually. "
            "This scenario is designed to show that the agents must reason "
            "differently here — from analog-product inference and market "
            "estimation, rather than extrapolating a historical trend."
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
ANNUAL_HOLDING_COST_RATE = 0.18  # 18% p.a. (cost of capital + warehousing + obsolescence risk; typical for electronics/ESS)
DEAD_STOCK_TRIGGER_MONTHS = 2  # How many consecutive surplus months trigger the Finance Agent

for sc in scenarios.values():
    consecutive = 0
    trigger_month = None
    for row in sc["rows"]:
        target = round(TARGET_INVENTORY_MONTHS * row["sales_forecast_request"])
        row["target_inventory_level"] = target
        row["inventory_gap"] = row["inventory_on_hand"] - target
        if row["inventory_gap"] > 0:
            consecutive += 1
        else:
            consecutive = 0
        row["consecutive_surplus_months"] = consecutive
        if consecutive >= DEAD_STOCK_TRIGGER_MONTHS and trigger_month is None:
            trigger_month = row["month"]
    sc["dead_stock_trigger_month"] = trigger_month

meta = {
    "company_name": "SunArc Solar (fictional company)",
    "disclaimer": "All data in this file is synthetic, created for portfolio demonstration purposes only, and does not represent any real company.",
    "schema_version": "1.3",
    "target_inventory_months": 1.5,
    "annual_holding_cost_rate": 0.18,
    "dead_stock_trigger_months": 2,
    "unit_convention": {
        "module": "Entered as a quantity (count); MWp = POWERCLASS(Wp) x quantity / 10^6 (e.g., 590Wp x 30,500 units / 10^6 = 17.995 MWp)",
        "inverter": "units",
        "ess_battery": "units",
        "lead_time_baseline": "Normal baseline is 2-4 months (~8-16 weeks). Supply-disruption scenarios may exceed this band.",
    },
    "field_definitions": {
        "sales_forecast_request": "Monthly volume requested by Sales (unit depends on scenario.unit)",
        "current_supply_capacity": "Production/procurement capacity available that month (same unit)",
        "lead_time_weeks": "Lead time from order to supply, in weeks (normal baseline 8-16 weeks)",
        "moq": "Minimum order quantity",
        "unit_cost_eur": "Unit cost (EUR) — per module for the module scenario, per unit for inverters/ESS",
        "inventory_on_hand": "Inventory on hand at the start of the month (same unit)",
        "target_inventory_level": "Target inventory = sales_forecast_request (demand proxy for that month) x target_inventory_months (1.5). Simplified for Phase 1; could be refined with a moving average later.",
        "inventory_gap": "inventory_on_hand - target_inventory_level. Positive = surplus (overstock), negative = deficit (higher supply urgency)",
        "consecutive_surplus_months": "How many consecutive months inventory_gap has been positive (resets to 0 on a negative month)",
        "product_lifecycle_stage": "'established' (existing product, trend-based reasoning possible) or 'new_launch' (no historical data)",
        "launch_month": "Launch month if product_lifecycle_stage is new_launch; null for established products",
    },
}

output = {"meta": meta, "scenarios": scenarios}

with open("/home/claude/synthetic_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("JSON written.")
