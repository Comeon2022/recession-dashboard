"""Current Stress / Break Confirmation v1 derived states.

All thresholds here are provisional, descriptive, and excluded from scoring.
"""

from __future__ import annotations

from derived_metrics import derive_vix_metrics


STATE_RANK = {"calm": 0, "watch": 1, "stress": 2, "severe": 3}


def _state(value: str, **thresholds) -> str:
    selected = value
    for state, condition in thresholds.items():
        if condition and STATE_RANK[state] > STATE_RANK[selected]:
            selected = state
    return selected


def _signal(signal_id: str, name: str, state: str, value: float, display: str, explanation: str, **extra) -> dict:
    return {"id": signal_id, "name": name, "state": state, "value": value, "display_value": display, "explanation": explanation, **extra}


def build_current_stress(vix: list[dict], financial: list[dict], credit: list[dict], claims: list[dict], sahm: dict, unemployment: dict, curve: dict, vix_metrics: dict | None = None) -> dict:
    vix_metrics = vix_metrics or derive_vix_metrics(vix)
    vix_current, vix_average, vix_change = vix_metrics["current"], vix_metrics["average20"], vix_metrics["change20"]
    vix_state = _state("calm", severe=vix_current >= 35, stress=vix_current >= 25 or vix_change >= 8, watch=vix_current >= 20 or vix_current >= 1.15 * vix_average)

    fin_values = [item["value"] for item in financial[:12]]
    fin_current, fin_average = fin_values[0], sum(fin_values[:4]) / min(4, len(fin_values))
    fin_change = fin_current - fin_values[-1] if len(fin_values) > 1 else 0
    fin_state = _state("calm", severe=fin_current >= 1, stress=fin_current >= 0, watch=fin_current < 0 and fin_change >= 0.5)

    credit_values = [item["value"] for item in credit[:12]]
    credit_current, credit_average = credit_values[0], sum(credit_values[:4]) / min(4, len(credit_values))
    credit_change = credit_current - credit_values[-1] if len(credit_values) > 1 else 0
    credit_state = _state("calm", severe=credit_current >= 0.5, stress=credit_current >= 0, watch=credit_current < 0 and credit_change >= 0.10)

    claims_values = [item["value"] for item in claims]
    claims_average = sum(claims_values[:4]) / min(4, len(claims_values))
    prior_values = claims_values[13:17] if len(claims_values) >= 17 else claims_values[-4:]
    prior_average = sum(prior_values) / len(prior_values)
    claims_change_pct = (claims_average / prior_average - 1) * 100 if prior_average else 0
    claims_state = _state("calm", severe=claims_change_pct >= 20, stress=claims_change_pct >= 10, watch=claims_change_pct >= 5)

    sahm_value = sahm["value"]
    sahm_state = _state("calm", severe=sahm_value >= 0.75, stress=sahm_value >= 0.5, watch=sahm_value >= 0.3)

    rapid_bull = (curve.get("delta_2y_20d_bp") is not None and curve.get("spread_change_20d_bp") is not None and curve["delta_2y_20d_bp"] <= -25 and curve["spread_change_20d_bp"] >= 15)
    curve_state = "stress" if rapid_bull else "calm"

    signals = [
        _signal("volatility-release", "Volatility Release", vix_state, vix_current, f"{vix_current:.2f} | 20D avg {vix_average:.2f} | 20D change {vix_change:+.2f}", "VIX release relative to its level and 20-day baseline.", observation_date=vix_metrics["observation_date"], market_confirmation=True, average20=vix_average, change20=vix_change),
        _signal("financial-stress-confirmation", "Financial Stress", fin_state, fin_current, f"{fin_current:+.4f} | 4W avg {fin_average:+.4f} | 12W change {fin_change:+.4f}", "STLFSI4 crossing or rising toward broad financial stress.", observation_date=financial[0]["date"], market_confirmation=True),
        _signal("credit-conditions-confirmation", "Credit Conditions", credit_state, credit_current, f"{credit_current:+.4f} | 4W avg {credit_average:+.4f} | 12W change {credit_change:+.4f}", "NFCICREDIT stress state; not a high-yield spread.", observation_date=credit[0]["date"], market_confirmation=True),
        _signal("claims-acceleration", "Claims Acceleration", claims_state, claims_average, f"{claims_average:,.0f} | 13W change {claims_change_pct:+.1f}%", "Four-week claims average compared with its 13-weeks-ago average.", observation_date=claims[0]["date"], prior_average=prior_average, percent_change=claims_change_pct),
        _signal("sahm-confirmation", "Sahm Confirmation", sahm_state, sahm_value, f"Sahm {sahm_value:+.2f} | unemployment {unemployment['value']:.1f}%", "Economic confirmation signal; does not add new recession points.", observation_date=sahm["date"]),
        _signal("rapid-bull-steepening", "Rapid Bull Steepening", curve_state, 1 if rapid_bull else 0, f"2Y 20D {curve.get('delta_2y_20d_bp'):+.1f} bp | spread 20D {curve.get('spread_change_20d_bp'):+.1f} bp", "Potential slowdown / Fed-response confirmation when short rates fall rapidly and the curve widens.", observation_date=curve.get("observation_date"), rapid_bull_steepening=rapid_bull, market_confirmation=True),
    ]
    active = [item for item in signals if STATE_RANK[item["state"]] >= 2]
    market_active = any(item.get("market_confirmation") for item in active)
    count = len(active)
    if count >= 4:
        label = "Break Confirmation" if market_active else "Economic Deterioration"
    elif count >= 3:
        label = "Break Risk Rising"
    elif count == 2:
        label = "Early Stress"
    else:
        label = "Calm / No Break"
    return {"version": "v1", "state": label, "active_confirmations": count, "active_signal_ids": [item["id"] for item in active], "market_confirmation_active": market_active, "signals": signals, "thresholds_provisional": True, "summary": f"{count} of 6 stress confirmations active."}
