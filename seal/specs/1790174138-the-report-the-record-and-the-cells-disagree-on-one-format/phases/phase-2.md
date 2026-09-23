# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e31acbb7 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

What the generator reads out of a report — #505 and #382. `section_body`
ends at a heading of the same level or shallower; `swallowed`'s section-end
scan takes the same rule or this record says why not (A3, Q6). `build`
writes the resolved commit into `Target SHA`. Cases A1, A2, A4, A5; the
existing `HEAD~1` case's docstring rewritten to say the cell is now pinned.
New ledger rows for `section_body` and `fenced_after` in the fragment.

## What this phase found

**The frame holds for this phase.** `section_body`, `table_body`,
`fenced_after`, the section-end scan inside `swallowed` and `build`'s
`cell(chain.TARGET, args.target)` were each where `plan.md` §*Technical
context* put them, and the refusal for an unresolvable `--target` already
stood two lines above the cell it then wrote the flag into.

**Q6 answer: the same rule.** The section-end scan inside `swallowed` reads
`section_end` now, the one definition `section_body` reads. The reason it
must, rather than may: a table a reviewer labels with a `###` and quotes only
inside a fence was, under the old scan, outside the span the row loop read —
so the loss the guard exists to name was not named, and the record arrived
with the template's empty table at exit 0. That is the case
`test_a_table_hidden_under_a_subheading_is_still_a_swallowed_table`, red at
`47f6f97a` and green now, and the mutation that keeps `swallowed`'s own
any-`#` scan is red on that case alone — which is what says the case pins
the row loop rather than `section_body`. A3's class is therefore two
readers, both moved.

**What a heading is did not change; what its depth means did.** The
reader's own `headings` is `startswith("#")`, and `heading_level` keeps
that: a `#120` at column 0 is a heading to both, because only a fence tells a
Markdown heading from a Python comment and `readable` has already blanked
the fences (`swallowed`'s docstring owns that argument). So the one shape
that changes is the deeper heading. A reviewer's `##` inside a section is
still an end, and `####` under `###` under the section is carried, because
the rule is *same level or shallower ends it* and not *one level deeper is
allowed* — `plan.md` §*What breaks in six months* named that and it holds.

**Seen red at `47f6f97a`** (executed), the four cases:

```
FAILED tests/test_the_record_is_generated.py::test_paste_ready_fixes_under_subheadings_are_carried_in_order
E         'no paste-ready fix in the report' is contained here:
FAILED tests/test_the_record_is_generated.py::test_a_section_still_ends_at_a_heading_of_its_own_level
E       assert '```python\ndef helper(a):\n    return a  # the replacement\n```' in '\n\n| What was run | Result |\n|---|---|\n| `pytest tests/test_x.py -q` | 3 passed |\n\n'
FAILED tests/test_the_record_is_generated.py::test_a_table_hidden_under_a_subheading_is_still_a_swallowed_table
E       assert 0 == 2
FAILED tests/test_new_says_when_head_is_not_the_target.py::test_a_target_given_as_a_revision_is_named_by_its_sha
E         | Target SHA | HEAD~1 |
```

The third of those was first written with `report(probes=…)`, which puts the
real table header outside any fence, so the section had standing rows and
nothing to refuse; the fixture now splices the whole section in by hand and
was seen red against HEAD's generator restored from git before the phase
2 bytes went back (from a kept copy, never `git checkout` over uncommitted
work).

**Then green** (executed): `bin/test tests/test_the_record_is_generated.py -q`
126 passed; `bin/test tests/test_new_says_when_head_is_not_the_target.py
tests/test_the_fixes_close_the_record.py -q` 110 passed. A5: the refusal
cases naming *does not resolve* —
`test_the_target_is_the_flag_and_it_has_to_resolve` in the generator module
and `tests/test_the_fixes_close_the_record.py`'s — are inside those counts.

**Five mutations, restored from kept bytes** (executed): M1 the old any-`#`
rule — 3 red (A1, A2, A3); M2 `<` for `<=` — 11 red, every `##` stopping
ending a section; M3 `swallowed` keeping its own scan — A3 red alone; M4 the
cell taking `args.target` — A4 red; M5 every line read as depth 1 — 3 red.

**Ledger:** A1 and A2 written into the fragment. Ten `seal/ledger.md` rows
anchor `build` or `swallowed` (R1, R9, F1–F5, R3, R4 and the id-refusal row)
and each carries a dated re-read note; hashes recomputed with
`evidence-check --reverify`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence in `test_a_target_given_as_a_revision_is_named_by_its_sha`'s docstring that the cell was deliberately not pinned, and #345's `overview.md` §Not done as its grounds | the same docstring, which now says the cell is pinned and why; #382 is the ticket |
| `section_body`'s own end-of-section loop and `swallowed`'s `next(... startswith("#") ...)` scan — two definitions of a section | `section_end`, the one definition |
