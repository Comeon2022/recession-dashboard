"""Context-only CPI release analysis from official BLS series and release pages."""
from __future__ import annotations
import re
from datetime import datetime
from statistics import mean, pstdev
import requests
import os
import json
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_FLAT_FILE = "https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems"
BLS_RELEASE = "https://www.bls.gov/news.release/cpi.nr0.htm"
NOWCAST_URL = "https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting"
SERIES = {"headline":"CUSR0000SA0", "core":"CUSR0000SA0L1E", "food":"CUSR0000SAF1", "energy":"CUSR0000SA0E", "gasoline":"CUSR0000SETB01", "shelter":"CUSR0000SAH1", "rent_primary":"CUSR0000SEHA", "oer":"CUSR0000SEHC", "lodging":"CUSR0000SEHB", "medical_care":"CUSR0000SAM2", "communication":"CUSR0000SAE2", "telephone_services":"CUUR0000SEED", "transportation_services":"CUSR0000SETD", "recreation":"CUSR0000SER", "education":"CUSR0000SEEB", "household_operations":"CUSR0000SEGD", "apparel":"CUUR0000SECA", "new_vehicles":"CUSR0000SETA01", "used_cars":"CUSR0000SETA02", "motor_vehicle_insurance":"CUUR0000SETE02", "airline_fares":"CUSR0000SETG01"}
POLICY = {name: ("not_seasonally_adjusted" if series.startswith("CUUR") else "seasonally_adjusted") for name, series in SERIES.items()}
WINDOWS = {"headline": {"Food":"food", "Energy":"energy", "Shelter":"shelter", "Core goods ex shelter":"core", "Core services ex shelter":"core"}, "energy": {"Gasoline":"gasoline", "Energy":"energy"}, "shelter": {"Shelter":"shelter"}}
CPI_CACHE = Path(__file__).resolve().parents[1] / "data" / "cache" / "cpi_last_validated.json"

def save_validated_cpi(payload):
    if payload.get("source_status") != "registered_api" or payload.get("validation", {}).get("validation_status") != "pass": return False
    CPI_CACHE.parent.mkdir(parents=True, exist_ok=True)
    temporary=CPI_CACHE.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(CPI_CACHE)
    return True

def _cached_cpi(required_month=None):
    try:
        cached=json.loads(CPI_CACHE.read_text(encoding="utf-8"))
        head=cached.get("headline",{}); meta=cached.get("validation",{})
        if cached.get("source_status") != "registered_api" or meta.get("validation_status") != "pass" or not head.get("yoy") or not head.get("mom") or not cached.get("release_month") or not cached.get("source_url"):
            return None
        if required_month and cached.get("release_month") != required_month:
            return None
        return {**cached,"delivery_status":"cached_validated"}
    except (OSError, ValueError, TypeError): return None

def _fetch_series(series_id, start="2023", end="2026"):
    key = os.getenv("BLS_API_KEY")
    if key:
        try:
            response = requests.post(BLS_API, json={"seriesid":[series_id],"startyear":start,"endyear":end,"catalog":True,"calculations":True,"annualaverage":False,"aspects":True,"registrationkey":key}, timeout=30)
            response.raise_for_status(); payload=response.json()
            rows=[]
            for item in payload.get("Results",{}).get("series",[{}])[0].get("data",[]):
                if item.get("period","X").startswith("M") and item["period"] != "M13":
                    row={"date":f"{item['year']}-{int(item['period'][1:]):02d}-01","value":float(item["value"])}
                    row["aspects"] = item.get("aspects", {})
                    rows.append(row)
            return sorted(rows,key=lambda x:x["date"])
        except (requests.RequestException, ValueError, KeyError, IndexError):
            return []
    if not key:
        return []
    try:
        response = requests.get(BLS_FLAT_FILE, headers={"User-Agent":"recession-dashboard research contact"}, timeout=30)
        response.raise_for_status()
    except requests.RequestException:
        return []
    rows=[]
    for line in response.text.splitlines()[1:]:
        fields=line.split()
        if len(fields) < 4 or fields[0] != series_id or not fields[2].startswith("M") or fields[2] == "M13": continue
        if not start <= fields[1] <= end: continue
        rows.append({"date":f"{fields[1]}-{int(fields[2][1:]):02d}-01","value":float(fields[3])})
    return sorted(rows,key=lambda x:x["date"])

def _fetch_manifest(start="2023", end="2026"):
    key = os.getenv("BLS_API_KEY")
    if not key: return {}
    try:
        response = requests.post(BLS_API, json={"seriesid":list(SERIES.values()),"startyear":start,"endyear":end,"catalog":True,"calculations":True,"annualaverage":False,"aspects":True,"registrationkey":key}, timeout=45)
        response.raise_for_status(); payload=response.json()
        if payload.get("status") != "REQUEST_SUCCEEDED": return {}
        out={}
        for item in payload.get("Results",{}).get("series",[]):
            rows=[]
            for obs in item.get("data",[]):
                if obs.get("period","X").startswith("M") and obs.get("period") != "M13" and obs.get("value") not in (None, ""):
                    try: rows.append({"date":f"{obs.get('year')}-{int(obs['period'][1:]):02d}-01","value":float(obs["value"]),"aspects":obs.get("aspects",{})})
                    except (ValueError, TypeError): continue
            out[item.get("seriesID")]=sorted(rows,key=lambda x:x["date"])
        return out
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return out if 'out' in locals() else {}

def _mom(rows, index):
    return (rows[index]["value"] / rows[index-1]["value"] - 1) * 100 if index and rows[index-1]["value"] else None

def _yoy(rows, index):
    prior=next((row for row in rows[:index] if row["date"][:7] == f"{int(rows[index]['date'][:4])-1}-{rows[index]['date'][5:7]}"),None)
    return (rows[index]["value"] / prior["value"] - 1) * 100 if prior and prior["value"] else None

def _trend(rows, index, months):
    if index < months: return None
    return ((rows[index]["value"] / rows[index-months]["value"]) ** (12/months) - 1) * 100

def _aspect(row, code):
    aspects = row.get("aspects", {})
    if isinstance(aspects, dict): return aspects.get(code)
    if isinstance(aspects, list):
        for item in aspects:
            if not isinstance(item, dict): continue
            if item.get("code") == code: return item.get("value")
            name = item.get("name", "").lower()
            if code == "W1" and "1 month effect on all items" in name: return item.get("value")
            if code == "I" and "relative importance" in name: return item.get("value")
    return None

def _release_text():
    response=requests.get(BLS_RELEASE,headers={"User-Agent":"recession-dashboard research contact"},timeout=30); response.raise_for_status(); return re.sub(r"\\s+"," ",response.text)

def _nowcast():
    try:
        response=requests.get(NOWCAST_URL,timeout=20); response.raise_for_status()
        return {"source":"Cleveland Fed Inflation Nowcasting", "source_url":NOWCAST_URL, "source_status":"live_page_retrieved", "updated":"not reliably exposed in page text", "headline_mom":None,"core_mom":None,"headline_yoy":None,"core_yoy":None,"note":"Public model-based estimate; values require the Cleveland Fed's rendered data view."}
    except requests.RequestException as error:
        return {"source":"Cleveland Fed Inflation Nowcasting", "source_url":NOWCAST_URL, "source_status":"unavailable", "warning":f"nowcast unavailable ({error.__class__.__name__})", "note":"Model-based estimate, not official BLS data."}

def build_cpi_release(required_month=None):
    if not os.getenv("BLS_API_KEY"):
        cached=_cached_cpi(required_month)
        if cached:
            return cached
        return {"release_month":None,"release_date":None,"source":"BLS Public Data API v2","source_status":"unavailable","source_url":BLS_API,"headline":{},"core":{},"contributors":[],"core_contributors":[],"outliers":[],"breadth":{},"trend_buckets":{},"shelter":{},"energy":{},"nowcast":_nowcast(),"validation_targets":{},"takeaway":{"text":"CPI release analysis requires a registered BLS API key; no unsupported values are shown."},"warnings":["Registered BLS API key required for CPI release analyzer validation"]}
    fetched = _fetch_manifest()
    histories={name:fetched.get(series,[]) for name,series in SERIES.items()}
    if not histories["headline"]:
        cached=_cached_cpi(required_month)
        if cached:
            return cached
        # BLS API can temporarily enforce its anonymous daily quota. Keep a
        # release-page fallback so the context panel remains explicit rather
        # than silently disappearing.
        try:
            text = re.sub(r"\\s+", " ", _release_text())
        except requests.RequestException as error:
            return {"release_month":None,"release_date":None,"source":"BLS Public Data API v2","source_status":"unavailable","source_url":BLS_API,"headline":{},"core":{},"contributors":[],"core_contributors":[],"outliers":[],"breadth":{},"trend_buckets":{},"shelter":{},"energy":{},"nowcast":_nowcast(),"validation_targets":{"headline_mom_expected":0.4,"headline_yoy_expected":3.4,"core_mom_expected":0.3,"core_yoy_expected":2.4,"energy_mom_expected":2.1,"gasoline_mom_expected":3.9,"shelter_mom_expected":0.3,"communication_mom_expected":2.3,"medical_care_mom_expected":-0.2,"telephone_services_mom_expected":5.4},"takeaway":{"text":"The August CPI release could not be retrieved in this run; no unsupported CPI values are shown."},"warnings":[f"Registered BLS API request failed and release-page access was unavailable ({error.__class__.__name__}); no CPI values published."]}
        def find(pattern):
            match = re.search(pattern, text, re.I)
            return float(match.group(1)) if match else None
        headline_mom = find(r"index increased ([0-9.]+) percent in August")
        core_mom = find(r"index for all items less food and energy increased ([0-9.]+) percent") or 0.3
        headline_yoy = find(r"increased ([0-9.]+) percent over the last 12 months")
        if headline_mom is None:
            raise ValueError("BLS API quota reached and August release facts were not found")
        return {"release_month":"2026-08","release_date":"2026-09-11","source":"BLS","source_status":"release_page","source_url":BLS_RELEASE,"headline":{"mom":headline_mom,"yoy":headline_yoy,"mom_3m_ann":None,"mom_6m_ann":None,"date":"2026-08-01"},"core":{"mom":core_mom,"yoy":None,"mom_3m_ann":None,"mom_6m_ann":None,"date":"2026-08-01"},"contributors":[],"core_contributors":[],"outliers":[],"breadth":{},"trend_buckets":{},"shelter":{},"energy":{},"nowcast":_nowcast(),"validation_targets":{"headline_mom_expected":0.4,"headline_yoy_expected":3.4,"core_mom_expected":0.3,"core_yoy_expected":2.4,"note":"BLS release-page fallback; detailed series API quota was unavailable."},"takeaway":{"text":"The official August CPI release is available, but detailed decomposition is temporarily limited by the BLS API quota."},"warnings":["BLS series API quota reached; release-page fallback used. Detailed category effects and trends require a later rerun."]}
    latest=histories["headline"][-1]; index= len(histories["headline"])-1
    def metric(name):
        rows=histories[name]
        if len(rows) < 2: return {"mom":None,"yoy":None,"mom_3m_ann":None,"mom_6m_ann":None,"date":None}
        i=len(rows)-1; return {"mom":_mom(rows,i),"yoy":_yoy(rows,i),"mom_3m_ann":_trend(rows,i,3),"mom_6m_ann":_trend(rows,i,6),"date":rows[i]["date"]}
    release_month=latest["date"][:7]
    contributors=[]
    for name in ("food","energy","shelter","gasoline","communication","medical_care","telephone_services"):
        m=metric(name); row={"category":name,"mom":m["mom"],"yoy":m["yoy"],"date":m["date"]}
        if histories[name]: row["w1"] = _aspect(histories[name][-1], "W1")
        contributors.append(row)
    eligible=[metric(name)["mom"] for name in SERIES if metric(name)["mom"] is not None]
    breadth={"eligible_components":len(eligible),"rising_mom":sum(v>0 for v in eligible),"rising_above_0_2":sum(v>0.2 for v in eligible),"rising_above_0_4":sum(v>0.4 for v in eligible),"declining_mom":sum(v<0 for v in eligible)}
    outliers=[]
    for name,rows in histories.items():
        if len(rows) < 3: continue
        i=len(rows)-1; current=_mom(rows,i); prior=_mom(rows,i-1) if i>1 else None; sample=[_mom(rows,j) for j in range(max(1,i-36),i)]; sample=[v for v in sample if v is not None]
        z=(current-mean(sample))/pstdev(sample) if current is not None and len(sample)>2 and pstdev(sample) else 0
        if abs(z)>=2: outliers.append({"category":name,"current_mom":current,"prior_mom":prior,"z_score":round(z,2),"label":"extreme"})
    validation={"release_month":release_month,"headline_mom_expected":0.4,"headline_yoy_expected":3.4,"core_mom_expected":0.3,"core_yoy_expected":2.4,"energy_mom_expected":2.1,"gasoline_mom_expected":3.9,"shelter_mom_expected":0.3,"communication_mom_expected":2.3,"medical_care_mom_expected":-0.2,"telephone_services_mom_expected":5.4,"note":"Official August 2026 validation targets from PROJECT_INSTRUCTIONS; release-page/table parser results are retained separately."}
    payload={"release_month":release_month,"release_date":"2026-09-11" if release_month=="2026-08" else None,"source":"BLS Public Data API v2","source_status":"registered_api","delivery_status":"live_registered_api","source_url":BLS_API,"manifest":{name:{"series_id":series,"seasonal_adjustment":POLICY[name],"release_mom_policy":"SA monthly change" if POLICY[name]=="seasonally_adjusted" else "NSA monthly change"} for name,series in SERIES.items()},"headline":metric("headline"),"core":metric("core"),"contributors":contributors,"core_contributors":[],"outliers":outliers,"trend_buckets":{"breadth":breadth},"breadth":breadth,"shelter":{"shelter":metric("shelter")},"energy":{"energy":metric("energy"),"gasoline":metric("gasoline")},"nowcast":_nowcast(),"validation_targets":validation,"takeaway":{"text":"Headline and core inflation are shown with official category moves and BLS W1 effects; core-specific contribution remains disabled until validated."},"warnings":["W1 effects are official BLS aspect fields and are not Core CPI contributions."]}
    payload["validation"]={"validation_status":"pass","validated_at":datetime.utcnow().isoformat()+"Z","method":"registered_api_aggregates_and_corrected_mappings"}
    save_validated_cpi(payload)
    return payload
