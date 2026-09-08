# every published reading carries three wrong rows — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_session_cost.py` | `totals["cache_write"], totals["cache_read"]` | The removed wording is three `totals[…] += count(…)` statements that became one loop over `FIELDS`. What still stands is a case asserting that the three columns are separate usage fields — it names the same dict keys because those keys still exist and are still what the report prints. Not a claim the range corrected: the case is more load-bearing after the change, since a field mix-up inside the loop is now one edit rather than three |
