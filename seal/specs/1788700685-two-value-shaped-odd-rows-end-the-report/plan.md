# Implementation Plan: one odd row does not end the report, on the axis the rule is about

## Summary

`parse_time` states the file's rule — *one odd row must not end the report* —
and `count` applies it to the value axis. Two operands taken out of a
transcript still end the report: a zero span, which four divisions in `report`
consume, and a naive `datetime`, which four subtractions in `analyse` cannot
mix with an aware one. Round 3 of #170 found both and measured them absent from
299 real transcripts, which is why this is a claim repair rather than a
firefight.

## Technical context

- `skills/verify/scripts/session_cost.py#report` — `data['command_s'] / data['span_s']`, and three more divisions by the same denominator, including the `idle > data['span_s'] * 0.1` guard which is itself safe at zero but sits inside the same block.
- `skills/verify/scripts/session_cost.py#analyse` — `(calls[-1]["end"] - calls[0]["start"])`, the per-call sum, the turn gap and the family sum: four subtractions, one class.
- `skills/verify/scripts/session_cost.py#parse_time` — the one place a stamp becomes a `datetime`, which is what makes normalisation there a closure rather than a patch.
- `seal/ledger.md` — #170's row stating the guarantee over the class. It is not falsified; it is under-specified, and the repair is the axis named in it.

**What breaks in 6 months.** A fifth arithmetic site is added and takes a
value straight out of a transcript. `parse_time` and `count` are the two
funnels this file already has; a repair that guards the four call sites instead
of the funnel leaves the next site to find on its own.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Guard each of the four divisions and each of the four subtractions | Eight guards and no funnel; the ninth site is written without one, which is exactly how these two arrived | **No** |
| Drop a naive stamp at `parse_time` the way an unparseable one is dropped | A transcript whose stamps are ALL naive loses every row and reports nothing, where today it reports numbers that are internally consistent | **No** |
| Normalise a naive stamp at `parse_time` — attach UTC, the assumption the file already makes when it rewrites `Z` — and make the span's denominator safe once, where the report's percentages are computed | A transcript from a harness writing local naive stamps is read as UTC, so a span is right and an absolute time is not. Nothing here prints an absolute time | **Yes** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `parse_time` normalises a naive stamp, with the assumption stated in its docstring; the report survives a zero span without inventing a percentage. Cases for both, over synthetic transcripts, each seen red first, each asserting the report and `--json` | The new cases plus the existing `session_cost` module; `uvx ruff` | b0e4859 |
| 2 | #170's ledger row names the axis its enumeration ran on, and this work item's fragment carries the row for the second axis | `./bin/evidence-check .` unscoped; the records | |

## Operational impact

None. A transcript this harness produces takes neither path, so no reading
already taken changes.
