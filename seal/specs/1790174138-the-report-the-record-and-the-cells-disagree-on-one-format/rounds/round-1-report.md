# Round 1 report — the report, the record and the cells disagree on one format

Target SHA `e3cc83c90d104c742f06d07d3878c282044e30e0`, measured against
`0b8dc4b2` (work item 0's sealed tip, the base until #537 squashes). Reviewed
in a `git clone --no-local` of the worktree at the target SHA; nothing was
written in the worktree except this file.

Every claim below is labelled. **executed** means I ran the command and read
its output in the clone; **read** means I opened the coordinate and it says
what is stated; **unverified** names who answers.

## Summary

Stage 1: every phase builds what its scenarios say, all five divergences
`overview.md` records were the right call, and the five points inherited from
work item 0 still hold of the landed code. Stage 2: `section_end` is one
definition in `chain_check.py` that both scripts read, all three readers take
it, the six-entry report reaches the record whole, the `Broad gate` readers
take the newest entry on both homes, a first seal is byte-identical, the four
carriers of the carried-closure row are one text, the skeleton runs through
`new` at exit 0, the survivor sweep in CI's form excuses its one report, and
the `#436` arm's grandfathering excuses exactly what the record-order arm would
over the committed corpus.

Three things need a fix, none of which loses a record or crashes:

- **🟡 1** — `close --broad-gate` is the second writer of the `Broad gate`
  cell and still replaces a run the cell already holds. #174's class is every
  writer of the cell, and the branch moved one of two, while three documents
  now say `close --broad-gate` writes "the same cell" in the sentence that
  describes the keep rule.
- **🟡 2** — a ninth carrier of the one-run wording stands in
  `agents/warden.md` itself, and no test pins any of the eight carriers the
  branch rewrote, so the "red test rather than a stale sentence" that
  `plan.md` §*What breaks in six months* promises does not exist.
- **🟡 3** — now that a `###` no longer ends a section, a second table's
  header row under one is copied into the record as a verdict row and nothing
  refuses it (probe, executed: `| # | Finding | Location | Verdict | Grounds |`
  lands in `## Verdicts` at exit 0). The same shape reaches the checker's
  `verdict_table` on a hand-edited record.

## The implementer's account, checked

The hand-back's claims and what I found:

- *Per-phase narrow runs, every new case red first or red under a named
  mutation.* The phase files quote the red runs; I did not reproduce the
  reversions. The cases themselves are green: **executed**, 579 passed across
  the eight modules the diff touches (command in §Executed probes).
- *38 mutations all killed.* **Read.** Each tabled mutation names a branch
  that exists in the landed code (`floor_and_fixes`'s inner `break` at
  `round_record.py:2012`, `<=` in `chain_check.py#section_end`, the `not
  chain.says_gate_not_yet(held)` guard at `round_record.py:4443`, the
  `elif NOT_IN_TREE not in line` arm at `evidence_check.py:2087`). Not
  re-executed; the case counts they cite match the modules I ran.
- *584-sequence differential 16 → 0, probe deleted.* **Unverified** as a
  count — the probe is gone. What I executed is the case that is the
  differential in miniature (A9,
  `test_a_stopped_count_walk_that_reached_two_is_not_a_reopening_left`), which
  asserts `bound_line` and `stopping_floor` over the same three records.
- *Q3 walk, 0 ending inside a comment.* **Read** the phase's account. My own
  smaller walk (executed): no committed record carries a `###` inside its
  `## Verdicts` section, which is the hand edit the third reader was fixed for.
- *Q7, `✅` admitted as a no-id row.* **Read** against `finding_number` at
  `round_record.py:2738-2751`: no digit, not in `OWED_MARKERS`, `idless` on —
  admitted. Consistent with the phase's execution.
- *Sweep over `0b8dc4b2...HEAD`, one survivor excused.* **Executed** in CI's
  form (`--exempt` per `survivors.md`): exit 0, one exempt, "every survivor is
  excused by a row above". Without `--exempt` the same run exits 1 naming
  `tests/test_a_phase_hands_the_next_one_a_record.py:108`, so the excusal is
  the row and not the code; the row's quote matches the standing text.
- *Zero committed records hold the pending pair at or after `RANGE_FROM`; the
  cutoff excuses exactly what `ORDER_FROM` would.* **Executed** over the 25
  committed round records at the target SHA: none between `ORDER_FROM` and
  `RANGE_FROM` carries a `Fix range` row at all (so either cutoff reaches the
  absent-row branch for them), and none at or after `RANGE_FROM` holds the
  pending value beside a `round-N`. The two cutoffs are identical over the
  corpus, not by construction; `overview.md` §Not done says the former and
  that is the honest sentence.

## Findings

### 🟡 1 · `close --broad-gate` still overwrites a run the cell holds

`skills/code-review/scripts/round_record.py:3883` builds the cell from the
flag alone — `gate = cell(BROAD_GATE, args.broad_gate) if args.broad_gate else None`
— and `:4067` writes it over whatever the row held. `seal` at `:4441-4444` now
reads the held run first and keeps it behind the new entry; `close` does not.
Two writers of one cell with two behaviours, and §12 of the contract says the
class is the writers, not the one the ticket named.

It is reachable without a hand edit. `seal`'s own docstring at `:4223-4226`
records the path that worked before `seal` existed — a fix table with a header
and no rows plus `--broad-gate` — and nothing refuses it now; and `close`
ticks `Pass` only when no verdict row is open (`:45`, `:78`), so a partial fix
table followed by a second `close --broad-gate` is the same overwrite one
call later. Either way the first run's record is erased, which is the sentence
#174 was filed on.

Why it matters beyond the code: `templates/sdd-round.md:39` says, inside the
sentence describing the keep rule, that "`close --broad-gate` writes the same
cell where fixes and the gate land in one pass"; `skills/code-review/orchestration.md:535`
says "`close --broad-gate` still writes the same cell". A reader takes *the
same cell* to mean the same rule. The fix is to give both writers one keep,
so the documents become true rather than rewritten. Paste-ready below; the
helper's name in prose is `kept_broad_gate` NAME NOT IN TREE.

### 🟡 2 · A ninth carrier of the one-run wording, and no pin on the eight

`agents/warden.md:320-322`: "Whether the one full-suite run has happened —
`not yet`, or the SHA it ran at and the base it was compared against — is
invisible in the code". That is the sentence shape `docs/review-handoff-protocol.md:171`
carried and the branch rewrote ("`not yet`, or one entry per run, newest
first"). `spec.md` §Data & interfaces listed seven carriers by reading,
phase 4 found an eighth by executing the list, and this one is found by
`grep -rn "the SHA it ran at" agents docs skills templates` (executed: one hit
outside the rewritten files, this line). The reviewer is the one agent that
carries the cell's state into a report row, so the sentence that tells it
what the state looks like is the one that should not read as one run.

The second half is the missing pin. `plan.md:74-77` (§*What breaks in six
months*) says a document that still reads *the SHA the run happened at* is
"a red test rather than an eighth stale sentence" because of "A16's pin and
the list in `spec.md`". A16 pins the carried-closure row and the five
markers; nothing pins the `Broad gate` carriers — `grep -rn "newest first\|earlier run" tests/`
(executed) hits only a docstring in the seal module. So the next edit that
takes one carrier back to one run is caught by nothing, which is what
happened to this ninth one. Paste-ready below: the sentence, and a pin case
whose name in prose is `test_every_carrier_says_the_cell_holds_one_entry_per_run` NAME NOT IN TREE.

### 🟡 3 · A repeated header row under a `###` is copied into the record as a row

Probe, executed (§Executed probes): a report whose `## Verdicts` holds the
table, then `### earlier rounds, re-checked`, then a second table with its own
header row, produces a record whose verdict section reads

```
| 🔴 1 | the parser drops a row | `f.py:1` | open | executed |
| # | Finding | Location | Verdict | Grounds |
| 🟢 | round 1's blocking finding is closed — x | `f.py:1` | confirmed | read |
```

at exit 0, and the `chain_check --worktree` that `new` runs afterwards says
nothing about it. `table_body` at `round_record.py:1086-1090` drops separator
rows after the first header and nothing else; `finding_number` then admits
the `#` cell reading `#` as a row that commissions nothing (no digit, not
empty, no owed marker). Before this branch the whole second table was lost
silently, which was worse; now it arrives with a row that says nothing, which
the standard calls the one shape it refuses.

The checker's `verdict_table` at `chain_check.py:1569-1583` has the same
reading over a hand-edited record: rows after the header are read, separators
skipped, a repeated header taken as a row whose verdict is `Verdict` — neither
open nor closed. Same class as the third reader the branch fixed, and the
same direction (permissive). Paste-ready below for both.

### ⬜ 4 · "a section ends at the next `##`" understates the rule

`agents/warden.md:466`. The rule the code implements is *a heading of the
section's own level or shallower ends it* (`chain_check.py#section_end`), so
a `#` ends a `##` section too. The behaviour is right; the sentence names one
of the two enders. Paste-ready below.

### ⬜ 5 · A running walk that already reached two prints the pre-refusal sentence

`round_record.py:2093-2102`. With records floor `no`, quiet, quiet and
`new --round 4`, the walk is running with `counted == 2` and the line prints
"the 2 records after it neither reopened the run nor closed on a fix, so the
gate's count … reaches 3 here" — while `stopping_floor` already returns an
error at that floor record with count 2, before this record exists. Same
verdict (the run ends), and the gate's error follows one command later, so
nothing un-says itself the way #218's case did; but the branch's stated rule
for a walk that reached two is *report the gate's own refusal*, and this is
the sibling case (§12). `if not running or counted > 1:` on the stopped
branch prints the right sentence for both. Read, not executed.

### ⬜ 6 · An aggregate stated without its source

`docs/review-chain-spec.md:982-984` and `skills/code-review/SKILL.md:332-334`:
"Measured over the 71 work items with two or more records: 3 had a last
record reading as closed-with-a-fix". The tree at the target SHA holds 25
round records across the live work items (executed count), so the number
cannot be re-measured here; it is #437's measurement, filed before the
settled work items were removed. Contract §5: an aggregate is not a
coordinate. Name the source and the tree it was taken at, so a reader can
tell a stale number from a wrong one.

### ⬜ 7 · The module named for three places pins four

`tests/test_the_report_standard_is_one_in_three_places.py` — `CARRIERS` holds
four files (the warden, the skill, the specification, the template). The
module docstring and name say three. A name, not a defect.

### ⬜ 8 · A same-commit re-seal appends a duplicate entry

`round_record.py:4441-4444`: `seal` run twice with the same `--broad-gate`
value writes `<sha> against <base>; earlier run: <sha> against <base>`. The
cell's own definition — one entry per run — makes that honest if the suite
really ran twice, and `plan.md` §Technical context noted that none of the six
refusals is *the cell already holds this run*. Recorded as a question rather
than a defect: whether a re-seal at the commit the cell already names should
be refused, or kept as written. Read.

## Regression tests to plant

| Test | Destination |
|---|---|
| a `close --broad-gate` over a cell already holding a run keeps that run behind the new entry, for both a header-only fix table and a partial one | `tests/test_the_fixes_close_the_record.py`, beside the `--broad-gate` cases |
| every carrier of the `Broad gate` cell's shape says one entry per run (the pin 🟡 2's paste-ready gives) | `tests/test_the_report_standard_is_one_in_three_places.py` |
| a second header row under a `###` inside `## Verdicts` reaches the record as no row | `tests/test_the_record_is_generated.py`, beside `test_paste_ready_fixes_under_subheadings_are_carried_in_order` |
| a repeated header row inside a record's `## Verdicts` is not a verdict row to the checker | `tests/test_chain_check_at_the_pull_request.py`, beside `test_a_blocking_finding_below_a_subheading_is_still_in_the_table` |

## Facts for the evidence ledger

- A5's clause says `seal` is the writer for both homes; it should also say
  `close --broad-gate` is a second writer and, once 🟡 1 lands, that both
  keep the held run through one helper — with the helper as a code ground.
- A1's clause can add: a repeated header row inside a section is dropped by
  `table_body` and by `verdict_table` (after 🟡 3), so a `###` inside a table
  section carries rows and never a second header.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `close --broad-gate` is the second writer of the `Broad gate` cell and still replaces a run the cell already holds; three documents say it writes "the same cell" | `skills/code-review/scripts/round_record.py:3883`, `:4067`, `templates/sdd-round.md:39`, `skills/code-review/orchestration.md:535` | open | read — `gate = cell(BROAD_GATE, args.broad_gate)` is built from the flag alone and written over the row; `seal` keeps the held run at `:4441-4444`; reachable through the header-only fix table `seal`'s docstring names and through a partial table, since `Pass` ticks only when no row is open |
| 🟡 2 | a ninth carrier of the one-run wording stands in the reviewer's own file, and no test pins any of the eight the branch rewrote | `agents/warden.md:320-322`; `plan.md:74-77` | open | executed — `grep -rn "the SHA it ran at"` over `agents docs skills templates` hits this line alone outside the rewritten files; `grep -rn "newest first\|earlier run" tests/` hits one docstring; read — the plan says a pin makes the class red and A16 pins something else |
| 🟡 3 | a second table's header row under a `###` inside `## Verdicts` is copied into the record as a verdict row at exit 0, and the checker reads the same shape on a record | `skills/code-review/scripts/round_record.py:1086-1090`, `skills/code-review/scripts/chain_check.py:1569-1583` | open | executed — the probe in §Executed probes; read — `table_body` drops separators only and `finding_number` admits `#` as a no-id cell; `verdict_table` skips separators only |
| ⬜ 4 | "a section ends at the next `##`" names one of the two enders | `agents/warden.md:466` | open | read — `section_end` ends at own level or shallower, so a `#` ends it too |
| ⬜ 5 | a running walk that already reached two prints "reaches N+1 here" where the gate already refuses at the floor record with N — #218's sibling | `skills/code-review/scripts/round_record.py:2093-2102` | open | read — `fires` at `:2013` admits a running walk of two; the stopped branch at `:2081` is the sentence for it and the running branch falls past it; verdict unchanged |
| ⬜ 6 | "Measured over the 71 work items …" states an aggregate without source or tree state; 25 records exist at the target SHA | `docs/review-chain-spec.md:982-984`, `skills/code-review/SKILL.md:332-334` | open | read — the number is #437's; executed — 25 committed round records at `e3cc83c9` |
| ⬜ 7 | the module named for three places pins four carriers | `tests/test_the_report_standard_is_one_in_three_places.py` | open | read — `CARRIERS` has four entries |
| ⬜ 8 | a re-seal at the commit the cell already names appends a duplicate entry; none of `seal`'s refusals is *already holds this run* | `skills/code-review/scripts/round_record.py:4441-4444` | open | read — the keep is keyed on a held SHA, not on a different one; a question for the owner, not a defect by the cell's definition |
| 🟢 | phase 1 (#218): a stopped walk that reached two fires with `running` false, `bound_line` prints the gate's refusal, the inner `break` is load-bearing, the exits table matches (A9, A10, A11, A17) | `round_record.py:2003-2016`, `:2081-2092`; `docs/review-chain-spec.md:1517-1518` | verified | executed — the generator module (A9, A10 green; `grep -n FLOOR_YES` returns six lines, none a reopening read); read — the `one reopening remains` row's condition is `fires` negated |
| 🟢 | phase 2 (#505, #382): one definition of a section's end in `chain_check.py`, delegated to by the generator, read by `section_body`, `swallowed`'s row loop and `verdict_table`; six `###` entries reach the record; `Target SHA` holds the resolved commit (A1–A5) | `chain_check.py:1180-1223`, `:1529-1533`; `round_record.py:1006-1032`, `:1035-1048`, `:1219-1224`, `:2119-2125`, `:2215` | verified | executed — the generator, target and close modules; read — `heading_level` keeps `startswith("#")` and adds depth; `commit_of` is the resolver `resolves` wraps |
| 🟢 | phase 3 (#436, #217): `fix_range`'s pending arm is keyed on `Fixes checked by`, normalised as `fix_surface` normalises, behind `RANGE_FROM`; `claim_lines` holds an unclosed comment's lines symmetrically with `held` (A6–A8) | `chain_check.py:1862-1894` against `:2641-2648`; `evidence_check.py:2065-2103` | verified | executed — the pull-request module's cases and the records-arm module; executed — corpus count of 25 records, no pending pair at or after `RANGE_FROM`, no `Fix range` row between the two cutoffs |
| 🟢 | phase 4 (#174): `seal` keeps a held run behind the new entry on both homes, a first seal is byte-identical, `broad_gate` and `direct_seal` read `named[0]` (A12–A14) | `round_record.py:4313-4319`, `:4441-4444`; `chain_check.py:3684`, `:3723`, `:4012-4021` | verified | executed — the seal module's three new cases inside 579; read — `direct_seal` delegates to `broad_gate` with its own floor; the `not chain.says_gate_not_yet(held)` guard is what keeps a first seal one entry |
| 🟢 | phase 5 (#503, #437, the opener rule): the skeleton carries the three shapes of a `#` cell and runs through `new`; the carried-closure row is one text in four carriers; the five markers, `&lt;!--` and the `###` permission are pinned (A15, A16) | `agents/warden.md:423-441`, `:443-453`, `:464-471`; `tests/test_the_report_standard_is_one_in_three_places.py` | verified | executed — the pin module and the skeleton case inside 579; read — the standard and the generator agree on every shape I wrote in this report, and the report's own `###` entries under `## Paste-ready fixes` are the A1 shape |
| 🟢 | phase 6 (#366's three cases): each pins a widening of the sweep against the reader itself | `tests/test_a_release_is_sized_by_a_criterion.py:100-142` | verified | executed — the module inside 579; the reversions are the phase record's account, read |
| 🟢 | the five divergences `overview.md` records — A9's home, the frame's dropped stamps, the sixth phase, the eighth carrier, the third reader — were each the right call | `overview.md:26-32` | verified | read — each names its grounds and the code agrees; the third reader is the one this round's 🟡 2 and 🟡 3 are siblings of, which says the class was named right and enumerated by sweep rather than by construction |
| 🟢 | work item 0's five inherited points hold: the terminal values with reasons, one reopening reader with no `== FLOOR_YES`, two `Review` answers, `broad-gate.md` through `broad_gate`, the gone/stands pairs untouched | `round_record.py:1397`, `:1973-1975`; `templates/sdd-round.md` diff; `chain_check.py:4012-4021` | verified | executed — the A11 grep and the floor-and-depth module (211 passed with five document-pinning modules); read — the branch's diff touches neither the declaration table nor the four-combination table |
| 🟢 | the four `survivors.md` rows excuse what they quote on grounds that hold, and the sweep in CI's form exits 0 | `seal/specs/1790174138-…/survivors.md:17-20` | verified | executed — `survivor_check.py --range 0b8dc4b2...HEAD --exempt …` exit 0, one exempt; read — the phase-record helper already reads to the first `## `, the ledger row is a past reading, the two paragraph walks share loop tokens and nothing of the rule |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict`, taken once after the rounds settle | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; the hand-back labelled it `unverified` and the orchestrator re-ran thirteen modules — the sealer answers it once this round's fixes land |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_record_is_generated.py tests/test_chain_check_at_the_pull_request.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_a_record_states_what_the_tree_has.py tests/test_new_says_when_head_is_not_the_target.py tests/test_the_report_standard_is_one_in_three_places.py tests/test_a_release_is_sized_by_a_criterion.py tests/test_the_fixes_close_the_record.py -q` in the clone at `e3cc83c9` | 579 passed, exit 0 |
| `bin/test tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_the_reviewers_report_reaches_the_record.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py -q` | 211 passed, exit 0 |
| `python3 skills/code-review/scripts/survivor_check.py --range 0b8dc4b2...HEAD` with `--exempt` for every `seal/specs/*/survivors.md` (CI's form) | exit 0 — 418 files, 151 removed sentences, one place exempt (`tests/test_a_phase_hands_the_next_one_a_record.py:108`); the same command without `--exempt` exits 1 naming that place |
| corpus count over `seal/specs/*/rounds/round-*.md` (records, not reports): id between `ORDER_FROM` and `RANGE_FROM` with a `Fix range` row; id at or after `RANGE_FROM` with the pending value beside a `round-N`; any `###` inside `## Verdicts` | 25 records; 0, 0 and 0 |
| `grep -n FLOOR_YES skills/code-review/scripts/round_record.py` (A11) | six lines — `terminal_value` and `written_late_cell`'s own refusals and one comment; no `== FLOOR_YES` |
| `grep -rn "the SHA it ran at" agents docs skills templates` | one hit outside the rewritten carriers: `agents/warden.md:321` |
| `grep -rn "newest first\|earlier run\|EARLIER_RUN" tests/` | the seal module's docstring and one unrelated line; no pin over the carriers |
| coverage probe `test_tmp_probe_second_table` (one file, run once, deleted — NAME NOT IN TREE): a report with the verdict table, then `### earlier rounds, re-checked`, then a second table with its header row, through `generate()` | exit 0, record written; the record's `## Verdicts` carries `\| # \| Finding \| Location \| Verdict \| Grounds \|` as a row between the two findings; `chain-check` after the write reports only the ordinary `nobody` notice |
| this report itself through `round_record.py new --round 1 --target e3cc83c9… --baseline 0b8dc4b2` in the clone (the record it wrote there was removed; the worktree's record is the orchestrator's to write) | exit 0 — `Pass` unticked over the three 🟡s, both terminal lines copied as values, 17 verdict rows and all nine fenced blocks under the `###` entries carried; the standard at the target SHA and the generator at the target SHA agreed on every shape written here |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` | not yet |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #366's second half — what `depth_two` should do when one finding's `Location` spans units of two depths | already deferred in `overview.md` §Not done, on #366 | the repository owner |
| #159 — a record cell corrected in place leaves no trace; the sketch for it | already deferred in `plan.md` §Alternatives and `questions.md` Q1, relayed to #159 | the repository owner, who relays it to the framer of the release after |

## Paste-ready fixes

### 🟡 1 — skills/code-review/scripts/round_record.py

One keep for both writers. Define beside `EARLIER_RUN` (the constant's own
constraints apply), then call it from `close` and from `seal`:

```python
def kept_broad_gate(reader, rows, value):
    """`value` in front of the run `rows`' `Broad gate` cell already holds,
    or `value` alone where it holds none (#174).

    ONE ENTRY PER RUN, NEWEST FIRST, for every writer of the cell: `seal` and
    `close --broad-gate` used to disagree, the first keeping a held run and
    the second replacing it, and the template describes them as writing the
    same cell. `not yet` holds no run and is replaced, so a first seal is
    byte-identical to what it always was; the new entry goes in front so that
    `chain_check.broad_gate`, which takes the first SHA-shaped word as the
    run, reads what it read before.
    """
    held = reader.visible(chain.field(rows, BROAD_GATE) or "").strip()
    if held and chain.SHA_RE.search(held) and not chain.says_gate_not_yet(held):
        return f"{value}{EARLIER_RUN}{held}"
    return value
```

In `close`, where `gate` is built (`:3883`), `rows` is the record's parsed
table rows that the surface reads already use:

```python
    gate = cell(BROAD_GATE, kept_broad_gate(reader, rows, args.broad_gate)) if args.broad_gate else None
```

In `seal` (`:4441-4444`), replace the four lines with:

```python
    value = kept_broad_gate(reader, rows, args.broad_gate)
```

And one case beside the `--broad-gate` cases of
`tests/test_the_fixes_close_the_record.py`, seen red by reverting the `close`
line above: a record sealed once, then `close` with a header-only fix table
and `--broad-gate '<sha2> against base'`, asserting the cell reads
`<sha2> against base; earlier run: <sha1> against base`.

### 🟡 2 — agents/warden.md and tests/test_the_report_standard_is_one_in_three_places.py

The sentence at `agents/warden.md:320-322`:

```markdown
  Whether
  the one full-suite run has happened — `not yet`, or one entry per run,
  newest first, each the SHA it ran at and the base it was compared against,
  an earlier run kept behind the newest as `earlier run` — is invisible in the
  code, and the next
  session either repeats a sealed run or ships assuming someone else made it.
```

The pin, in `tests/test_the_report_standard_is_one_in_three_places.py`, one
phrase per carrier because the carriers do not share one:

```python
# Every document that describes the `Broad gate` cell's shape, with the phrase
# that says it holds one entry per run (#174). A carrier that drifts back to
# one run is the stale sentence `plan.md` §What breaks in six months names.
GATE_CARRIERS = (
    (("agents", "sealer.md"), "earlier run"),
    (("agents", "warden.md"), "earlier run"),
    (("docs", "review-chain-spec.md"), "earlier run"),
    (("docs", "review-handoff-protocol.md"), "earlier run"),
    (("skills", "code-review", "SKILL.md"), "one entry per full-suite run"),
    (("skills", "code-review", "orchestration.md"), "earlier run"),
    (("skills", "verify", "SKILL.md"), "earlier run"),
    (("templates", "sdd-round.md"), "earlier run"),
)


def test_every_carrier_says_the_cell_holds_one_entry_per_run():
    """#174's shape is stated in eight documents and pinned in none of them
    until now; the ninth carrier (`agents/warden.md` §Role) was found by grep
    one round after the eight were rewritten."""
    for parts, phrase in GATE_CARRIERS:
        text = flat(*parts)
        assert phrase in text, (
            f"{'/'.join(parts)} no longer says the Broad gate cell holds "
            f"one entry per run ({phrase!r} missing)"
        )
        assert "the SHA it ran at and the base it was compared against — is" not in text, (
            f"{'/'.join(parts)} describes the cell as one run"
        )
```

### 🟡 3 — skills/code-review/scripts/round_record.py and skills/code-review/scripts/chain_check.py

`table_body`, the return at `round_record.py:1086-1090`: a row that repeats
the header is a second table's header under a `###`, not a row.

```python
    return [
        (i, cells)
        for i, cells in rows[1:]
        if not reader.is_separator([reader.visible(c) for c in cells])
        and tuple(reader.visible(c) for c in cells) != header
    ]
```

`verdict_table`, the loop at `chain_check.py:1570-1583`: the same test, on the
casefolded header the function already built.

```python
    for line_no, cells in rows[1:]:
        seen = [reader.visible(c) for c in cells]
        if reader.is_separator(seen):
            continue
        if [c.casefold() for c in seen] == header:
            # A second table's header under a `###` inside the section
            # (#505): a row that names the columns is not a verdict row, and
            # read as one it carries a `#` cell reading `#` that nothing
            # refuses.
            continue
```

Two cases, each seen red by reverting its own line: the probe above as a case
in `tests/test_the_record_is_generated.py` asserting the record's verdict
section carries no `| # |` row beyond the header; and a hand-inserted second
header inside a record's `## Verdicts` in
`tests/test_chain_check_at_the_pull_request.py` asserting `verdict_table`
returns two rows, not three.

### ⬜ 4 — agents/warden.md

```markdown
nothing else, and a section ends at the next heading of its own level or
shallower — a `##` or a `#` — never at a `###` (#505). **Write `&lt;!--`
```

### ⬜ 5 — skills/code-review/scripts/round_record.py

At `:2081`, so a running walk that already reached two reports the gate's
own refusal too:

```python
        if not running or counted > 1:
```

Needs a fix: yes — 🟡 1 (`close --broad-gate` replaces a held run), 🟡 2 (the ninth carrier and the missing pin), 🟡 3 (a repeated header row copied as a verdict row)
Loses a record or crashes: no — nothing found writes outside `seal/specs/` or raises; 🟡 1 erases one entry inside a cell the generator itself rewrites, which is a record kept short rather than a record lost

## Proof

· the eight touched modules pass — `bin/test <eight modules> -q` → `579 passed` (exit 0)  [executed]
· the six document-pinning and floor modules pass — `bin/test <six modules> -q` → `211 passed` (exit 0)  [executed]
· the survivor sweep in CI's form — `survivor_check.py --range 0b8dc4b2...HEAD --exempt …` → `every survivor is excused by a row above (1)` (exit 0)  [executed]
· a repeated header row under a `###` is copied as a verdict row — `test_tmp_probe_second_table`, deleted (NAME NOT IN TREE) → record written, `| # | Finding | Location | Verdict | Grounds |` inside `## Verdicts` (exit 0)  [executed]
· `close --broad-gate` replaces a held run — `skills/code-review/scripts/round_record.py:3883`, `:4067`  [read]
· the ninth carrier — `agents/warden.md:320-322`; no pin — `grep -rn "newest first\|earlier run" tests/`  [executed]
· the 38 mutations and the 584-sequence differential — unverified as re-executions; the phase files are the account, the cases they cite are inside the 579  [unverified — no answerer needed; the smith's executions stand as read]
· broad gate: not yet — due when the last round record's `Pass` is checked; the sealer takes it  [unverified — the sealer]
· cost: 2 test runs, 2 sweep runs, 1 probe run, about 8 minutes of command time
· red proven: the probe's assertion is the printout, not a pass; the eight-module run is green and proves nothing red
· files opened: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `phases/phase-1.md` … `phase-6.md`, `changelog.md`, `survivors.md`, `routing.md`, `seal/ledger/1790174138-….md`, `seal/ledger/1790173106-….md` (diff), `seal/ledger.md` (diff), work item 0's `plan.md` §Alternatives, `agents/warden.md`, `agents/sealer.md`, `docs/review-chain-spec.md` (diff), `docs/review-handoff-protocol.md` (diff), `skills/code-review/SKILL.md` (diff), `skills/code-review/orchestration.md` (diff), `skills/evidence-check/SKILL.md` (diff), `skills/verify/SKILL.md` (diff), `templates/sdd-round.md`, `skills/code-review/scripts/chain_check.py`, `skills/code-review/scripts/round_record.py`, `skills/evidence-check/scripts/evidence_check.py`, `skills/verify/scripts/unverified_check.py`, `skills/verify/scripts/deferral_check.py`, `skills/code-review/scripts/survivor_check.py`, `.github/workflows/hygiene.yml`, `bin/test`, and the nine test modules the diff touches
