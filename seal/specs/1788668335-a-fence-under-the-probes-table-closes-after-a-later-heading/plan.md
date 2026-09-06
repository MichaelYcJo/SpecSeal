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
| The issue's `SECTIONS` membership test | goes stale when a section is added; the check then passes on the newest heading | to be judged against the next row |
| Refuse a fence whose collected lines cross the section's own boundary | needs `section_body`'s contract to be exact, which is the thing to read first | to be judged |
| No change, if the shape does not reproduce | the issue closes on executed evidence | to be judged |

The smith fills this in after the reproduction, and the verdict column is what
the round reviews.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reproduction at HEAD, the alternatives table settled on it, and the refusal or the answer that none is owed — with the two cases #169 names either way | `bin/test tests/test_the_record_is_generated.py -q`, the new cases seen red first, and the module's own mutation battery | |
| 2 | The closing set: ledger fragment, changelog fragment, `overview.md`, `docs/flow.md`'s #169 box | the modules that read them, `evidence-check`, and the orchestrator's broad gate after the rounds | |

Two phases rather than four: this item touches one function and its cases, and
a phase boundary that carries nothing is a record nobody reads.

## Operational impact

None. One generator function; no CLI, record format or field moves.
