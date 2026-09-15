from inflation_expectations import _expectation_state

assert _expectation_state(6, -4) == "Expectations rising"  # raw sign conflict, but forward move is below 5 bp
assert _expectation_state(-6, 4) == "Expectations falling"
assert _expectation_state(6, -5) == "Mixed"
assert _expectation_state(-6, 5) == "Mixed"
assert _expectation_state(3, -8) == "Stable"  # primary remains authoritative below threshold
assert _expectation_state(None, -8) == "Unavailable"
print("inflation-expectations tests: PASS")
