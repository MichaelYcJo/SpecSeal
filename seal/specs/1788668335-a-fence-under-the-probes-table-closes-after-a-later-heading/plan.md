# Implementation Plan: a fence that closes after a later heading is refused

<!-- seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/plan.md -->

## Summary

The smallest item of 0.8.2, and the only one whose fix arrived written out. So
the work is not the edit — it is establishing that the edit is still owed, and
then enumerating the class properly rather than taking the issue's word that
the late-closed shape is *the one member left open*.

## Technical context

- **[read]** `round_record.py#fenced_after` collects fence lines from `raw` at
  the indices `section_body` gives for the heading, tracking an opener marker
  and clearing it on a matching closer. `marker is not None` at the end raises
  `Refused` — *a fenced block under `<heading>` is never closed*.
- **[read]** `VERDICTS`, `PROBES` and `DEFERRED` are module constants, so the
  issue's `SECTIONS` tuple has its members already named.
- **[read]** `terminal_value` already refuses a fence closed at the end of the
  file, by counting `Needs a fix:` lines — which the issue names as the reason
  that shape is not the one at large.
- **The open question is what `section_body` returns.** If it stops at the next
  `##`, `## Deferred` is outside the range and the reported shape is already
  refused as unclosed. Open it before anything else.

**What breaks in six months.** A refusal keyed to a list of section constants
goes stale the day a section is added — the record grows a heading, the list
does not, and a fence swallowing the new one is accepted. Whatever is built,
prefer a rule about *what a fence may not cross* over a list of things it may
not swallow.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| The issue's `SECTIONS` membership test, inside `fenced_after` | **measured to miss two members already, not one in six months.** A fence taking `## Executed probes` means `build` never calls `fenced_after`, so the guard is not merely stale — it is never reached; and a fence taking a prose heading is accepted by the membership test on the day it is written | **rejected** |
| Refuse a fence whose span crosses a line the generator reads the report by, over the whole report | needs `section_body`'s contract to be exact — which the reproduction settled: `readable` blanks a fence, so a swallowed heading is not a boundary at all. The remaining risk is a false positive on a fence that merely quotes a heading, which the *still stands outside* clause answers | **taken** |
| No change, the shape does not reproduce | — | **rejected: it reproduces.** Executed at `c4d7077`, exit 0, the Deferred table inside the fence and the record reading `nothing to drain` |

**Why the winner won, in one line each.** Row 1 was measured against the class
rather than against the reported shape, and the class has seven members where
the issue named one. Row 2 keys on the span, so it covers the members the row
list does not enumerate, and it derives the read lines from `REPORT_TABLES`
and `TERMINAL_LINES` — the module's own statement of what it reads, which had
no reader before this — so no second list exists to go stale. Row 3 is closed
by execution, not by argument.

`phases/phase-1.md` carries the seven-member table, the measured exit of each,
and how the enumeration is known to be complete.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reproduction at HEAD, the alternatives table settled on it, and the refusal or the answer that none is owed — with the two cases #169 names either way | `bin/test tests/test_the_record_is_generated.py -q`, the new cases seen red first, and the module's own mutation battery | `2b6e8f1` |
| 2 | The closing set: ledger fragment, changelog fragment, `overview.md`, `docs/flow.md`'s #169 box | the modules that read them, `evidence-check`, and the orchestrator's broad gate after the rounds | `5083595` |

Two phases rather than four: this item touches one function and its cases, and
a phase boundary that carries nothing is a record nobody reads.

## Operational impact

None. One generator function; no CLI, record format or field moves.
