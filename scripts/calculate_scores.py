"""Deterministic, rule-based scores for the ten Phase 2 sample indicators."""


def score_payrolls(value: float) -> int:
    # Provisional: weak job growth is a warning; outright contraction is recessionary.
    if value >= 200_000:
        return 0
    if value >= 0:
        return 1
    return 2


def score_sahm(value: float) -> int:
    if value < 0.25:
        return 0
    if value < 0.50:
        return 1
    return 2


def score_initial_claims(value: float) -> int:
    if value < 220_000:
        return 0
    if value < 250_000:
        return 1
    return 2


def score_jolts_hires(value: float) -> int:
    # Provisional threshold because the sample combines a rate-style display with a single value.
    if value >= 3.5:
        return 0
    if value >= 2.5:
        return 1
    return 2


def score_jolts_quits(value: float) -> int:
    # Provisional: lower quits indicate less worker confidence.
    if value >= 2.1:
        return 0
    if value >= 1.5:
        return 1
    return 2


def score_wage_growth(value: float) -> int:
    # Provisional: moderate wage growth is healthy; very low growth signals weakness.
    if value >= 4.0:
        return 0
    if value >= 2.0:
        return 1
    return 2


def score_ism_employment(value: float) -> int:
    # Provisional: 50 separates expansion from contraction.
    if value >= 50:
        return 0
    if value >= 45:
        return 1
    return 2


def score_ism_activity(value: float) -> int:
    # Provisional: activity above 50 indicates expansion.
    if value >= 50:
        return 0
    if value >= 45:
        return 1
    return 2


def score_yield_curve(value: float) -> int:
    # Provisional: an inverted curve is warning/recessionary; positive spread is healthy.
    if value >= 100:
        return 0
    if value >= 0:
        return 1
    return 2


def score_lei(value: float) -> int:
    # Provisional: a small positive reading is still treated as a warning until momentum is stronger.
    if value >= 0.5:
        return 0
    if value >= 0:
        return 1
    if value >= -0.5:
        return 1
    return 2


def score_housing_starts(value: float) -> int:
    # Provisional annualized-unit thresholds; weaker construction adds housing risk.
    if value >= 1.5:
        return 0
    if value >= 1.2:
        return 1
    return 2


def score_building_permits(value: float) -> int:
    # Provisional annualized-unit thresholds for forward-looking permits.
    if value >= 1.5:
        return 0
    if value >= 1.2:
        return 1
    return 2


def score_new_home_sales(value: float) -> int:
    # Provisional annualized-sales thresholds.
    if value >= 0.8:
        return 0
    if value >= 0.6:
        return 1
    return 2


def score_mortgage_delinquency(value: float) -> int:
    # Provisional credit-stress thresholds; this is the only mortgage indicator scored initially.
    if value < 3.0:
        return 0
    if value < 5.0:
        return 1
    return 2


SCORERS = {
    "payrolls": score_payrolls,
    "sahm-rule": score_sahm,
    "initial-claims": score_initial_claims,
    "jolts-hires": score_jolts_hires,
    "jolts-quits": score_jolts_quits,
    "wage-growth": score_wage_growth,
    "ism-employment": score_ism_employment,
    "ism-activity": score_ism_activity,
    "yield-curve": score_yield_curve,
    "lei": score_lei,
    "housing-starts": score_housing_starts,
    "building-permits": score_building_permits,
    "new-home-sales": score_new_home_sales,
    "mortgage-delinquency": score_mortgage_delinquency,
}


def get_regime(total_score: int) -> str:
    if total_score <= 5:
        return "Healthy"
    if total_score <= 10:
        return "Slowdown"
    if total_score <= 14:
        return "Elevated Risk"
    return "Recessionary"


def get_regime_from_risk_score(risk_score: int) -> str:
    if risk_score <= 25:
        return "Healthy"
    if risk_score <= 50:
        return "Slowdown"
    if risk_score <= 70:
        return "Elevated Risk"
    return "Recessionary"
