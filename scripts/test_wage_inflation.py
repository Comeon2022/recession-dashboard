from wage_inflation import build_wage_inflation

def rows(value, prior=None):
    return [{"date":"2026-08-01","value":value},{"date":"2026-07-01","value":prior if prior is not None else value}]

def fake_fetch(series):
    if series in ("CIU2020000000000I",): return [{"date":"2026-04-01","value":179.304},{"date":"2025-04-01","value":173.849}]
    if series == "PPIDSS": return rows(100, 99)
    if series == "PPIAWS": return rows(102, 100)
    if series == "PPITWS": return rows(100, 100)
    return rows(101, 100)

def test_missing_data_is_unavailable():
    result=build_wage_inflation(lambda _: [], rows(101,100), {"yoy":3.3})
    assert result["wage_leg"] == "Unavailable" and result["producer_pass_through_leg"] == "Unavailable" and result["overall_spiral_state"] == "Unavailable"

def test_current_state_rules():
    ahe=[{"date":f"{year}-08-01","value":100+(year-2020)*3} for year in range(2020,2027)]
    result=build_wage_inflation(fake_fetch,ahe,{"yoy":3.353})
    assert result["wage_leg"] == "Balanced" and result["producer_pass_through_leg"] == "Selective" and result["overall_spiral_state"] == "No broad confirmation"

if __name__ == "__main__":
    test_missing_data_is_unavailable(); test_current_state_rules(); print("wage-inflation tests: PASS")
