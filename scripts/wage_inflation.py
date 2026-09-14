"""Context-only wage/inflation transmission analysis using official FRED series."""
from __future__ import annotations

SERIES = {"eci":"CIU2020000000000I", "ulc_yoy":"PRS85006111", "ulc_qoq_ann":"PRS85006112", "ppi_final":"PPIFIS", "ppi_core":"WPSFD49116", "ppi_services":"PPIDSS", "ppi_transport":"PPIAWS", "ppi_services_ex_trade":"PPITWS"}

def _yoy(rows):
    if len(rows) < 2: return None
    latest = rows[0]; prior = next((x for x in rows[1:] if x["date"][:4] == str(int(latest["date"][:4])-1) and x["date"][5:7] == latest["date"][5:7]), None)
    return ((latest["value"] / prior["value"])-1)*100 if prior and prior["value"] else None

def _ahe_context(rows):
    ordered=sorted(rows,key=lambda x:x["date"]); yoy=[]
    for row in ordered:
        prior=next((x for x in ordered if x["date"][:4]==str(int(row["date"][:4])-1) and x["date"][5:7]==row["date"][5:7]),None)
        if prior and prior["value"]: yoy.append({"date":row["date"],"value":(row["value"]/prior["value"]-1)*100})
    current=ordered[-1] if ordered else {}; current_yoy=next((x["value"] for x in reversed(yoy) if x["date"]==current.get("date")),None)
    base=[x["value"] for x in yoy if "2017-01"<=x["date"]<="2019-12"]
    peak=max((x for x in yoy if x["date"]>="2022-01-01"),key=lambda x:x["value"],default={})
    def ann(n): return ((current["value"]/ordered[-1-n]["value"])**(12/n)-1)*100 if len(ordered)>n else None
    return {"level":current.get("value"),"date":current.get("date"),"mom":(current["value"]/ordered[-2]["value"]-1)*100 if len(ordered)>1 else None,"yoy":current_yoy,"three_month_annualized":ann(3),"six_month_annualized":ann(6),"three_month_average_yoy":sum(x["value"] for x in yoy[-3:])/3 if len(yoy)>=3 else None,"twelve_month_change_pp":yoy[-1]["value"]-yoy[-13]["value"] if len(yoy)>=13 else None,"prepandemic_baseline":{"average_yoy":sum(base)/len(base) if base else None,"observations":len(base),"min":min(base) if base else None,"max":max(base) if base else None},"post_pandemic_normalization_peak":peak}

def build_wage_inflation(fetch, ahe_rows, cpi):
    data={name:fetch(series) for name,series in SERIES.items()}; wage=_ahe_context(ahe_rows); cpi_yoy=cpi.get("yoy") if cpi else None
    def metric(name):
        rows=data[name]; return {"value":rows[0]["value"],"date":rows[0]["date"],"yoy":_yoy(rows),"mom":(rows[0]["value"]/rows[1]["value"]-1)*100 if len(rows)>1 and rows[1]["value"] else None} if rows else {}
    eci=metric("eci"); ulc_yoy=metric("ulc_yoy"); ulc_qoq=metric("ulc_qoq_ann")
    gap=wage["yoy"]-cpi_yoy if wage["yoy"] is not None and cpi_yoy is not None else None
    wage_leg="Unavailable"
    if wage["yoy"] is not None and eci.get("yoy") is not None:
        wage_leg="Balanced"
        if wage["yoy"]<3 and eci["yoy"]<3: wage_leg="Cooling"
        elif wage["yoy"]>4 or eci["yoy"]>4: wage_leg="Reaccelerating"
        elif abs(wage["yoy"]-eci["yoy"])>1: wage_leg="Mixed"
    ppi={key:metric(key) for key in ("ppi_final","ppi_core","ppi_services","ppi_transport","ppi_services_ex_trade")}; service=ppi["ppi_services"].get("mom"); transport=ppi["ppi_transport"].get("mom"); ex_trade=ppi["ppi_services_ex_trade"].get("mom")
    producer_leg="Unavailable" if any(value is None for value in (service, transport, ex_trade)) else ("Contained" if service<=0 else ("Selective" if transport>service and abs(ex_trade)<0.1 else "Broadening"))
    overall="Unavailable" if "Unavailable" in (wage_leg, producer_leg) else ("No broad confirmation" if wage_leg in ("Cooling","Balanced") and producer_leg in ("Contained","Selective") else ("Early pressure" if wage_leg=="Reaccelerating" or producer_leg=="Broadening" else "Mixed"))
    conclusion=f"Wage growth is {wage_leg.lower()}, while producer-price pressure is {producer_leg.lower()}; no broad wage-price spiral is confirmed." 
    return {"source":"FRED / BLS","source_status":"live","state":overall,"wage_leg":wage_leg,"producer_pass_through_leg":producer_leg,"overall_spiral_state":overall,"conclusion":conclusion if overall != "Unavailable" else "Wage-price transmission cannot be assessed until the required official series are available.","wage":{**wage,"wage_cpi_gap_pp":gap},"eci":eci,"unit_labor_costs":{"yoy":ulc_yoy,"qoq_annualized":ulc_qoq},"producer_prices":ppi,"methodology":"Context-only. Wage/CPI gap equals AHE YoY minus headline CPI YoY; it is not official real income. Project-defined descriptive thresholds: wage Cooling requires AHE and ECI YoY <3; Reaccelerating requires either >4; Mixed requires absolute difference >1; otherwise Balanced. Producer Contained requires Services MoM <=0; Selective requires Transportation > Services and absolute Services ex trade/transport <0.1; otherwise Broadening. Missing required fields produce Unavailable.","warnings":[]}
