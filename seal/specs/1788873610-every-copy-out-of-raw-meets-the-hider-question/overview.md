# 1788873610-every-copy-out-of-raw-meets-the-hider-question — overview

<!-- seal/specs/1788873610-every-copy-out-of-raw-meets-the-hider-question/overview.md -->

📋 implement applied
· spec:     `spec.md`, `plan.md` §Alternatives, `questions.md`, `routing.md`,
            `phases/phase-1.md`, `phases/phase-2.md`;
            `skills/agent-contract/SKILL.md` §§1, 2, 4, 5, 7, 9, 12, 13, 14,
            15; `skills/implement/SKILL.md` §§1–5;
            `skills/writing-style/SKILL.md`; `CLAUDE.md` §*The goal a design
            is chosen against*, §*a change writes fragments*, §*commit
            early*; `docs/review-chain-spec.md` §*The reopening*;
            `seal/config.md` (`Record language` absent → English);
            `seal/follow-up.md` §*Anything tied to a coordinate*;
            `seal/specs/1788668335-…/rounds/round-3.md` and its
            `overview.md`; `templates/sdd-spec.md`, `sdd-plan.md`,
            `sdd-questions.md`, `sdd-phase.md`, `sdd-overview.md`
· evidence: `seal/ledger/1788873610-every-copy-out-of-raw-meets-the-hider-question.md`
            F6 and F7, twelve coordinates; and nine rows of `seal/ledger.md`
            re-read one at a time and re-stamped — R1, R2 and R9 of
            `1788597030-…`, F1 to F5 of `1788668335-…` (F2's claim struck and
            corrected), R3 and R4 of `1788749195-…`, R3 of `1788761915-…`
· verified: **executed** — `tests/test_the_record_is_generated.py` (100
            passed), `tests/test_the_fixes_close_the_record.py` (43 passed),
            the ten modules that touch `round_record.py` plus
            `tests/test_a_rider_reaches_its_file.py` (295 passed, 1 skipped),
            six mutations each restored from kept bytes, `ruff check` and
            `ruff format --check` on the four files this branch touched,
            `bin/evidence-check` unscoped (944 ok · 0 drifted · 0 broken,
            exit 0), `rider_check.py` (24 ok · 0 drifted · 0 broken),
            `gather_changelog.py --check`. **read** — the ticket's three
            facts, opened at `8114937` by probe before anything was built;
            `inherited_rows`, `table_of`, `fenced_after`, `terminal_value`,
            `fix_table`, `close`, `reach_back`, `units_named_earlier`,
            `floor_and_fixes`, and `reader.strip_comments` / `blank_fences`.
            **unverified** — the full suite, the repository-wide lint and the
            typecheck, which are the orchestrator's (contract §2)

## Why this work exists

`round_record.py` guarded four texts against a hider that never closes and
never read back the record it wrote, so a comment a copied cell took half of
left a record whose three lower sections were blank to every reader at exit
0 — and the guard's own completeness argument was a grid whose rows were the
copies somebody could see, one short.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether `inherited_rows`' copy loses a section silently | Issue #182, finding 10: *"a verdict row carrying an unterminated `&lt;!--` reaches a later record, whose `## Deferred` is then present in the bytes and resolves to zero occurrences through the shared reader, silently — and the loss re-enters every later record of the chain"* | the measurement | `inherited_rows` copies the `Location` cell alone. An opener there swallows the row's remaining pipes — the raw reading treats a `\|` inside a comment as text — so the row comes in under its header width and the run is **refused**, at `a verdict row has 3 cells`. An opener in a `Grounds` cell is never copied, and round 2's record came out clean with every section resolving. Executed at `8114937`, both paths the ticket names. The premise stands and the consequence does not, and `overview.md` of `1788668335-…` carries the same correction at its own coordinate |
| Where the guard goes | `spec.md` §Scope for this work item was written after the measurement, so it already says the destination. The ticket says *"every copy taken out of `raw` meets the hider question"*, which reads as a question per copy — and the grid's fourth row is what that spelling produces | the destination | Three things. A whole-text question on an input read for named sections refuses a file this repository already has (`1788826000-…/rounds/round-1-fixes.md`, a code-span marker on a table row). Narrowed to the section it is `swallowed` parameterised over its three constants, a refactor of the function five ledger rows name, for a copy the reader's arithmetic already refuses. And the destination answers for a fifth copy nobody has written yet, where a row answers for one. `CLAUDE.md`'s first goal decides between the two: the destination catches the same defects and asks nobody anything |
| What is reachable and worse than either | nothing in the ticket or in `1788668335-…`'s records names it | the measurement, recorded | A report whose `Grounds` cell opens a comment and closes it on the line below is accepted, `new` **exits 0**, round 1's record is written, and `## Executed probes`, `## Inherited coordinates` and `## Deferred` each resolve to 0 occurrences while standing in the bytes. `chain_check` reads only `## Verdicts` among sections, so nothing downstream says a word either. That is the straddle the branch had recorded as open, measured one input earlier than round 2's fix pass measured it |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck — contract §2 keeps them out of a build phase. The suite was **read**, not executed: the orchestrator ran it on the base `c0a65d5` on macOS at 2026-09-08 and reported `2808 passed, 2 skipped in 439.63s` | the orchestrator, immediately after this hand-back |
| whether the released `## 0.8.2 — 2026-09-06` section of `CHANGELOG.md` should be edited as well. Its `1788668335-…` entry is byte-identical to the fragment beside it and carries *"What is left is one cell, named rather than assumed"*, which is false. `questions.md` Q1 states the two options; the correction is written into this work item's own fragment either way | the repository owner |
| the READ-LESS half of this class, which is deliberately left open and is not the same as unverified — its three members were each measured. It is here as well as in §Not done because a reader of this table is the party who schedules it | the repository owner, in an issue the orchestrator opens (contract §6 forbids this session posting one) |

## Not done

**The read-less half of the class is left open, with its three members
measured and its home at the coordinate.** A hider in a text the generator
reads for named sections can make it read LESS than the text holds:

- an earlier record's verdict row blanked, so `inherited_rows` does not
  inherit its coordinate;
- a `New units` row blanked, so `units_named_earlier` does not see an entry
  and `depth_two`'s depth-2 refusal is not made;
- a `## Fixes` row blanked, so `close` reports the smith as never having
  written a row they did write.

None of the three puts a hider into a record — `write_record` is what would
catch that, and it does. All three are LOUD today, and each refusal talks
about cell arithmetic or a missing row rather than about a comment, which is
§14's defect one step short of a loss. What closing it takes is a question
scoped to the section each text is read for, because a whole-text question
there refuses a file this repository already has: the `` `&lt;!--` `` inside a
code span at
`seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1-fixes.md`
blanks that file's tail and hides nothing `fix_table` reads. Scoped, it is
`swallowed` parameterised over `REQUIRED_HEADINGS`, `REPORT_TABLES` and
`TERMINAL_LINES` — a design call rather than a fix, and one that touches the
function five rows of `seal/ledger.md` name. It is recorded as a rider at
`round_record.py#inherited_rows`, with the measurement and the instruction
that a reader takes the whole class or none of it. Not in
`seal/follow-up.md`: that file's own header sends a coordinate-tied item to
the coordinate, and this repository has a tracker.

**The straddle's other spelling is not chased.** `reader.strip_comments`
does not know a code span from prose, so `` `&lt;!--` `` in a Grounds cell is a
hider to it. In a RECORD that now refuses, which is correct — a record whose
tail is blank to `chain_check` is broken however the marker got there — and
it is bounded rather than argued: all 163 records committed under
`seal/specs/*/rounds/round-*.md` were read through both passes at `8114937`
and none has an open hider. Teaching the reader about code spans is out of
scope by `spec.md` §Out: it is the shared reader, and every comparison in
this plugin agrees only because both sides run the same passes.

**`reach_back` has no behavioural case, only the AST one.** It writes
`cell(chain.CHECKED_BY, "round-N")`, a value that cannot carry a hider, so
there is no shape to construct. The mutation that bypasses `write_record`
there turns exactly one case red, and that case is the property.

## Fed back into the spec

None. The rule and its completeness argument live in
`seal/ledger/1788873610-…` F6 and F7 and in `write_record`'s own docstring,
and no clause of `spec.md` was rewritten — the three rows above are where the
ticket was found wrong, which is what that section is for.
