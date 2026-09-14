import json
import tempfile
from pathlib import Path
import cpi_analyzer as c

def test_cache_rules():
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"cpi.json"; old= c.CPI_CACHE; c.CPI_CACHE=path
        valid={"source_status":"registered_api","validation":{"validation_status":"pass"},"headline":{"mom":.4,"yoy":3.3},"release_month":"2026-08","source_url":"x"}
        path.write_text(json.dumps(valid)); assert c._cached_cpi()["delivery_status"]=="cached_validated"
        path.write_text(json.dumps({**valid,"validation":{"validation_status":"fail"}})); assert c._cached_cpi() is None
        path.write_text(json.dumps({**valid,"source_status":"unavailable"})); assert c._cached_cpi() is None
        c.CPI_CACHE=old
if __name__=="__main__": test_cache_rules(); print("cpi cache tests: PASS")
