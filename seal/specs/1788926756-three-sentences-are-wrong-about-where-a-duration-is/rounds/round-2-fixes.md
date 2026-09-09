# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — round 2, fix pass

Round 2 opened five findings. Two are this pass's — the missing pin and the
misdiagnosed mechanism — one is a fourth instance of the class this work item
has been sweeping all along, and two belong to `round_record.py`'s generator
and are now #309.

**The depth-2 exit is withdrawn and the pin is planted.** Round 2's three
grounds were re-derived rather than taken from the report: `round-1.md:11`
reads `| New units | none |`, so `depth_two`'s parent set is empty and the
mechanised refusal cannot fire; `New units` is written from a top-level Python
AST comparison, so a Markdown paragraph can never be the parent it refuses
under; and `orchestration.md`'s first case — *a fix pass may add a unit* —
is the one this is. The case sits in
`tests/test_a_segment_feeds_the_flow_log.py`, the module that already reads
that section through `section_body()`, so no new mechanism came with it.

**The mechanism was `wanted`, and the repair the tree named moves the score by
a thousandth.** Round 2 measured all three states one change at a time and the
numbers are its own: 0.758 as shipped, 0.757 with every `survivors.md` dropped
from `corpus`, 1.829 with `corrected`'s added-n-gram subtraction disabled. So
an exemption quote does not weigh less, it leaves the search set — and #308
already carries that correction, with the repair moved to the diff side. The
three carriers of the old diagnosis are corrected and #308 is cited rather
than re-argued.

**One thing the paste-ready text did not have and one thing it could not.**
The `survivors.md` repair paragraph was pasted with its closing sentence
changed: it read *handed to the orchestrator as an issue, separate from #307*,
and the issue exists, so it names #308. And the proof line's figure is **97**
rather than the report's 96 — the pair was 96 at `b411e77` and this pass adds
the pinning case, so `tests/test_a_segment_feeds_the_flow_log.py` is 28 and the
line says which number moved and why.

**§12, by construction rather than by grep.** The class is *a sentence saying
what a span ends at, where a duration is, what causes an overlap, or how many
cases passed*, and it has now produced four instances inside this work item.
Two sweeps ran over every document the branch touched: every `N passed`,
`N cases`, `N assertions` claim in the work item (two, both now executed
figures), and every carrier of the survivor diagnosis outside the round
records. The second found a **fifth instance round 2 did not name** —
`phases/phase-3.md:57-58` says the two reports are *excused in `survivors.md`
with a quote as the anchor*, which is the promise the format makes and not
what happens. It is corrected in place with the measurement and the date.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 12 | fixed | `2caff29` — `test_the_section_names_batching_as_the_way_a_share_passes_one_hundred` in `tests/test_a_segment_feeds_the_flow_log.py`, which already loads that section. Seen red four ways, one assertion each, restoring `skills/verify/SKILL.md` from bytes the probe kept and comparing sha256 after every arm: the whole pre-fix file at `2479859` (assertion 1, exit 1), the measured sentence deleted (assertion 2, exit 1), *crossed a turn* reworded to *in another turn* (assertion 3, exit 1), and *something running in the background* pasted back beside the new cause (the negative assertion, exit 1). Green before and after all four. `overview.md`'s `## Not verified` row is closed ✅ with the case named, and the depth-2 grounds it carried are corrected there rather than deleted |
| 13 | answered | corrected at `2caff29` — three carriers, none of them code: `survivors.md`'s diagnosis and repair paragraphs, `overview.md`'s `## Not verified` row, and `phases/phase-3.md`'s *excused with a quote as the anchor* sentence, which round 2 did not name and is the same false claim one file over. All three now say the cause is `corrected`/`wanted` and the surface is the diff side, and all three cite #308. Executed here rather than re-argued: `survivor-check` over the CI range with every `seal/specs/*/survivors.md` handed to it and with **no** `--exempt` at all gives the identical output — 764 files, 80 removed sentences, *no removed wording is still standing*, exit 0 both times — so the flag changes nothing in either direction, which is #308's claim from the other side |
| 14 | answered | corrected at `2caff29` — `overview.md`'s `verified:` line said *105 passed*. Executed at `2caff29`: `tests/test_session_cost.py` 69, `tests/test_a_segment_feeds_the_flow_log.py` 28, the pair **97**, exit read directly as 0. The line now carries both numbers, says the 28 is 27 plus this pass's case, and records that the pair was 96 before it — round 2's figure, which was right when it was taken |
| 15 | deferred #309 | `round-1.md:12-13`'s truncated terminal rows. Left standing on the orchestrator's instruction: the truncation is `round_record.py new` reading one physical line of a field, the record was written by the generator rather than by hand, and correcting the two cells here would hide the generator defect behind a repaired record. #309 owns both halves |
| 16 | deferred #309 | `round_record.py new`'s silent truncation of a wrapped `Needs a fix` or `Loses a record or crashes` value. Pre-existing, outside this branch's fix range, and mechanism a fix pass may not add |

## What this pass did not run

The full suite, the repository-wide lint and the typecheck are the
orchestrator's, once, after this round settles — `skills/agent-contract/SKILL.md`
§2. `ruff` is not installed in this checkout. What ran here is the two modules
the change touches (97 passed, exit 0), `bin/evidence-check` (exit 0),
`bin/unverified-check` (exit 0, 204 open · 47 closed · 0 unreadable, one row
moved from open to closed and none deleted) and `bin/survivor-check` at both
ranges.
