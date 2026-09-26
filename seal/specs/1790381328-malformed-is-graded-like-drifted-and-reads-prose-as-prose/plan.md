# Implementation Plan: MALFORMED is graded like DRIFTED, and rule (a) reads prose as prose

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

Two changes to one checker, `skills/evidence-check/scripts/evidence_check.py`,
landing on one branch. Rule (a) first: #614's three edges and the both-marks
observation, so prose stops being refused and one coordinate shape stops being
missed. Then the grading: `MALFORMED` returns exit 1 on a lenient run and 2
under `--strict`, which is the owner's answer to #606's Q1. Every document,
workflow comment and test that states the old grading moves with it, and the
ledger rows that quoted it are corrected in place.

## Technical context

Read at 47e32d57 (the branch's base, `release/v0.15.5` = `main`):

- `evidence_check.py#PATH_HASH_RE`, `#URL_RE`, `#refused_coordinate`: rule
  (a). `refused_coordinate(s)` is called once per code span and once per word
  outside a span, on what is left of a `Code grounds` cell after every
  well-formed and old-format coordinate is blanked (`#malformed_rows`). A span
  may hold whitespace; a word never does. That difference is why the
  both-marks test only misfires on spans, and why the glued-marks rule can
  only change a span's verdict.
- `evidence_check.py#exit_code`: the `MALFORMED` branch sits directly after
  `OLD-FORMAT` and before `BROKEN`, returning 2. Its comment names Q1 of work
  item 1790297087 as the owner's to move. Moving it without reordering would
  return 1 for a tree holding a `BROKEN` row beside a `MALFORMED` one, so it
  goes below the `BROKEN`/`refused` branch (or joins the drift branch).
- `evidence_check.py#LENIENT_NOTICE` and `#main`'s `if code == 1:`. The
  notice prints on exit 1 alone and is held verbatim by
  `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#NOTICE`,
  and structurally against `broad_gate.py`'s ledger call
  (`checks[LEDGER] = run(LEDGER, [py, EVIDENCE, "--strict", root], …)`), the
  `bin/evidence-check` wrapper and `seal_stamp.py`.
- `.github/workflows/test.yml`'s `ledger` job runs the checker with no flag,
  fails on `-ge 2`, and prints a fixed `::warning::` on 1. It reads the exit
  code and never the text.
- `templates/evidence-check.yml` passes `--strict`, so a repository that
  vendored the template still refuses a `MALFORMED` row at exit 2 after this
  work. That is why part 2 still matters to consumers after part 1.
- `hooks/evidence-advisor.py#failing_rows` imports the checker and never sees
  an exit code. Unchanged.

**What breaks in six months.** The glued-marks rule is a regex over a span,
and the next shape it misreads will be a quoted locator whose escaping the
regex models differently from `unescape`. The guard case (a quoted locator
holding `# c`) and the bare-quote case are what catch that; a new shape goes
into the same parametrised cases. On the grading side, a future reader may
read exit 1 as *drift, re-read it* and run `--reverify` over a `MALFORMED`
row. `--reverify` names it and writes nothing, so the failure is a wasted
command, never a false stamp.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Grading: keep `MALFORMED` exit 2 under both readings** (0.15.4's default (a)) | the owner answered (b) on 2026-09-26 | rejected by the owner |
| **Grading: fold `MALFORMED` into the drift branch's condition** instead of a branch of its own | nothing breaks; the reason for a branch of its own was that the owner might move it, and the owner has now moved it | either is acceptable. The builder keeps a separate branch only if it reads clearer; the ordering below `BROKEN` is what is required |
| **Notice: two sentences chosen by cause** (one for drift, one for `MALFORMED`) | a second constant and a predicate that restates the grading beside `exit_code`, which the notice's own comment refuses ("A predicate that restates the rule is a predicate that can drift from it"); a tree with both causes needs a third sentence | rejected |
| **Notice: one sentence naming both verdict words** | none measured; the sentence gets longer, and it still fits one line | **chosen** |
| **Notice: unchanged** ("where drift is exit 2") | true but incomplete: on a malformed-only run it explains the strict refusal by a cause the run does not have | rejected |
| **CI warning: unchanged** | a malformed-only run prints *reports drift — re-verify the rows above* over a row whose remedy is to fix the coordinate, which sends the reader to `--reverify` | rejected |
| **CI job: fail on `MALFORMED` by reading stdout** | makes this repository's CI stricter than the owner's answer, and parses text in a step that deliberately reads only the exit code | rejected — contradicts the answer |
| **Rule (a) items 1–3: #614's paste-ready fix as written** | the trades in `spec.md` §*What each part gives up*; round 3 executed it (11 parameters red at its target, green with the fix; 207 passed over the four reader modules) | **chosen** |
| **Item 3 with an upper bound too** (`{6,12}`, `ANCHOR_RE`'s range) | a 40-character SHA pasted after a path goes silent | rejected |
| **Item 4: defer** | ships a release that says rule (a) reads prose as prose while a shape round 3 measured still is refused; same class, same unit (§12) | rejected |
| **Item 4: an `@` anywhere after the first `#`** | fixes `` `@lru_cache  # memoized` `` and leaves `` `x = 1  # see @jane` `` refused — the second shape round 3's report named for the same rule | rejected — half the class |
| **Item 4: both marks inside one whitespace-separated token** | misses a malformed quoted locator holding a space, `#"a b"@0`, which has no path for the per-word rule to catch | rejected |
| **Item 4: glued marks — an `@` following a `#` with no whitespace between them outside a quoted string** | a path-less coordinate with an unquoted space between the marks (`#handler @abcdef12`) goes silent | **chosen**; the loss is stated in `spec.md` |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Rule (a) reads prose as prose.** `PATH_HASH_RE` `{6,}`; `ISSUE_TAIL_RE` in place of `tail.isdigit()`; the dotless file name's openers `_`, `"`, `<`; `GLUED_MARKS_RE` in place of `"#" in s and "@" in s`; both docstrings state the rule and its trades. #614's two functions (11 parameters) plus one for the decorated lines (S11) and one guard parameter (the quoted locator holding `# c`, S12), after `test_a_directive_or_a_string_holding_a_hash_is_prose` | `bin/test tests/test_a_row_points_by_content.py -q`; each new case shown red with the phase's checker edit reverted (§15), the guard shown green on both sides; then `bin/test tests/test_evidence_check.py tests/test_dispatch.py tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q`, the three other modules that read this arm | |
| 2 | **`MALFORMED` is graded like `DRIFTED`.** `exit_code`'s branch and order; `LENIENT_NOTICE` verbatim from `spec.md` §*Scope* item 2; the module docstring's exit line, `malformed_rows`' docstring, `--strict`'s help. The six test pins of `spec.md` item 8 (one renamed), S3's new `BROKEN`-beside-`MALFORMED` assertion, and the two new pins (item 9). `SKILL.md` (option row, reader table with a `MALFORMED is` column, verdict rows), `skills/evidence-ci/SKILL.md` step 4, `templates/evidence-check.yml`'s step comment, `test.yml`'s `ledger` comment and warning. The `questions.md` Q1 Status cell of work item 1790297087 | `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py tests/test_a_row_points_by_content.py -q`; S1 and S3 shown red against 47e32d57's `exit_code`, the two new pins shown red with the old text restored; then the enumeration in `spec.md` §*Data & interfaces* re-run over the edited tree, listing no function that still asserts 2 for a lenient `MALFORMED` | |
| 3 | **The records.** The four ledger rows of `spec.md` §*Data & interfaces*, plus any other row `evidence-check .` names: false claims corrected in place with a `Corrected 2026-09-…` note, then re-read, `evidence-check --reverify` narrowed to the files holding them, and a dated `Re-read` note. New rows in `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`. `changelog.md` in this directory. `survivor-check --range origin/release/v0.15.5...HEAD`, with any exemption in this directory's `survivors.md` (expected: `SKILL.md`'s `OLD-FORMAT` row keeps "(exit 2, `--strict` or not)", which `MALFORMED`'s row drops, correctly). `overview.md` | `python3 skills/evidence-check/scripts/evidence_check.py --strict .` reads `0 drifted · 0 broken · … · 0 malformed`, exit 0; `survivor-check` exits 0 with every survivor exempt | |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** A tick is refused, and so is `done`.
What a phase discovers and the next phase needs goes in
`seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

**Why this order.** The milestone ranks prose refusal first ("the direction
that reaches other people's builds"), and a consumer on the vendored template
keeps exit 2 after phase 2, so phase 1 is the part they feel. The two phases
touch different units (`refused_coordinate`/`PATH_HASH_RE` against
`exit_code`/`LENIENT_NOTICE`) and different cases, so neither re-edits the
other's work. Phase 3 is last because both earlier phases drift the same
ledger rows, and re-reading each row once is the `implement` skill's *draft as
you go, write in one pass*.

The broad gate (full suite, repository-wide lint and format) is not in any
phase. It is the sealer's, once, after the review rounds settle.

## Operational impact

- **A consumer running the checker without `--strict`** — the
  `evidence-ci` lenient recipe `|| [ $? -eq 1 ]`, or a bare invocation —
  stops failing on a malformed coordinate after this update. The run still
  names it with its remedy and prints the notice. This is the owner's
  accepted trade and the changelog fragment says it in its first sentence.
- **A consumer on the vendored template** (`--strict`) keeps exit 2 on a
  genuinely malformed row, and stops getting it on the prose shapes phase 1
  fixes.
- **This repository's CI**: the `ledger` job warns on a malformed row
  instead of failing; `broad-gate` still refuses it at the seal.
- No new dependency, no environment variable, no migration.
