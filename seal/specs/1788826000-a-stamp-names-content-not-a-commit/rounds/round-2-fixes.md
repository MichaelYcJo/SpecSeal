# 1788826000-a-stamp-names-content-not-a-commit — round 2, the fix pass

Fix commits: `d069d54..HEAD` on `fix/239-a-stamp-names-content-not-a-commit`
— `677e10f`, `982b8d3` and the commit carrying this file. The round's target
was `2f0dd02`; its record is committed at `d069d54`.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 10 | fixed | `677e10f` — an `--only` selecting no rider is refused by path and the run exits 1. `982b8d3` closes the same cause three instances further out, in `main` |
| 11 | fixed | `677e10f` — `#` opens a comment everywhere except a `.md` file, where it opens a heading, and both callers of the reader are told the path so they cannot disagree about it. The module docstring now states the asymmetry the defect broke |
| 12 | answered | corrected at `982b8d3` — 33 marker lines with 13 extras at `2f0dd02` and 36 with 16 at `677e10f`, in all three records, each figure naming the commit it was taken at |
| 13 | answered | corrected at `982b8d3` — both records name both trailing forms, with the round each one was executed in |
| 14 | answered | corrected at `982b8d3` — `seal/ledger.md:1203` and `:1418` say who read what, on a fresh reading rather than on round 2's account of it |
| 15 | answered | corrected at `982b8d3` — the row is marked ✅ with the commit that answered it, and the ONE refusal that replaced it is a new row naming the orchestrator |

## The red seen before each fix

Contract §15, and two of the four were red for the wrong reason first.

| Case | What it did unpatched |
|---|---|
| `test_a_markdown_heading_naming_the_marker_is_not_a_rider` | `comment_blocks` returned `[(3, 3)]` for `## RIDER: what one is` and `riders_in` returned one rider with `new=False` — so `check()` gave `0 ok · 0 drifted · 1 broken`, exit 2, on a line nobody wrote as a rider. Executed directly against the unpatched module, because the case itself fails on the new signature first |
| `test_the_hasher_reads_a_markdown_heading_the_same_way_the_reader_does` | red with `region_lines` reverted to the argument-less call and everything else in place: `['## H', '', 'prose under it.', '', '', 'more prose.']` — the marker heading cut out of a region the reader does not read as a rider at all. Restored from a kept copy, `diff` byte-identical |
| `test_reverify_says_so_when_only_selects_no_rider` | `([], [])` — nothing written, nothing refused, and `main` printed `0 restamped · 0 refused` at exit 0 |
| `test_only_without_a_verb_is_refused_rather_than_ignored` | `main` returned 0 and printed `1 ok · 0 drifted · 0 broken`, having read the whole fixture tree with `--only` dropped |

## What the re-enumeration found

Findings 10 and 11 are one shape: the code being looser than what it says
about itself. Finding 11 accepts a form its own docstring excludes; finding 10
reports success for a path that does not exist. So every entry point this
branch added was put to the same two questions — what does it accept that its
docstring does not, and what does it report when its input is ABSENT rather
than wrong.

**Three more instances, fixed.** `--only` is documented as *one path, for
`--reverify`*, and `main` ignored it everywhere else. Executed on the working
tree before the guard: `--only hooks/worktree-guard.py` gave
`20 ok · 0 drifted · 0 broken` exit 0, `--only nope/nope.py` gave the same, and
`--migrate --only nope/nope.py` gave `0 migrated · 0 refused` exit 0. Each is a
person scoping a run and reading success for a run that ignored the scope.
Refused before anything is read, exit 2, with a sentence saying why.

**One instance, and it is the fix's own doing.** `region_lines` had `rel` in
scope and passed it to nothing. Finding 11's fix teaches the reader that `#` is
a heading in markdown, and without this the hasher would have kept the old
answer: no rider for the heading, and the heading's line still cut out of the
region hashed. The two callers now agree by construction.

**Two left, both a judgment.** `tree_files` skips a root that is not a
directory, so renaming one of the six leaves its riders read by nothing and the
run still exits 0 — and the module's own comment says this list has been the
defect twice. `all_riders` swallows `OSError` and `UnicodeDecodeError`, so a
file that cannot be decoded holds riders nothing reads. Refusing either is a
new rule about what CI rejects, which a fix pass may not add, and whether a
root may legitimately be missing is not this pass's call. Both are
`questions.md` C2, to the repository owner. Neither stands in the tree today:
all six roots exist and every file decodes.

## What this pass did not touch

`rounds/round-2.md` and `rounds/round-2-report.md`. The records arm of
`bin/evidence-check` refuses one name in the report — `round-2-report.md:216`
reads `evidence_check.py#unread_items` as a coordinate and no
`evidence_check.py` sits at the repository root — so the arm exits 2 and
`tests/test_a_record_states_what_the_tree_has.py` goes red with it. Executed at
`d069d54`, before this pass touched anything: the same one refusal, so it
arrived with the report. The remedy the checker names is `NAME NOT IN TREE` on
that line, or the full `skills/evidence-check/scripts/` path. It is the
orchestrator's, exactly as round 1's eight were — `2f0dd02` is the commit that
cleared those.

**It blocks the broad gate**, which is why it is here as well as in
`overview.md`.

## Verification

| What was run | Result |
|---|---|
| `bin/test tests/test_a_rider_reaches_its_file.py -q` | `29 passed` — 25 before this pass, 4 planted here |
| `rider_check.py` on the working tree, exit read without a pipe | `20 ok · 0 drifted · 0 broken`, exit 0 |
| `rider_check.py --reverify --only` — a mistyped path, an absolute path, the real path | refused and exit 1 for the first two, `0 restamped · 0 refused` exit 0 for the third, tree unchanged |
| `rider_check.py --only PATH`, `--only <absent path>`, `--migrate --only PATH` | all three exit 2 with the sentence, nothing read |
| A markdown heading naming the marker, through `check()` | `(0, 0, [])` — no verdict at all, where the unpatched reader gave `1 broken` |
| `bin/evidence-check`, ledger arm | `827 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `bin/evidence-check`, records arm | `3 work items read · 42 unread · 427 names read · 1 refused` — the refusal above, exit 2 |
| Marker lines over the six roots, per commit | `2f0dd02` 33 · `677e10f` 36, against 20 riders both times. The three added are the case file's own new fixtures, all string literals |
| Both `seal/ledger.md` rows' cited files, diffed across the whole branch | one line each: `Verified 2026-09-06 at 4581fe1` → `against test_the_refusal_above_can_actually_fail@8e0a246a`, and `Verified 2026-09-07 at 70c272c` → `against unread_items@9046e0b6`. Dates unchanged, claims untouched |
| `bin/test` over six neighbouring guard modules | `248 passed`, and `test_a_record_states_what_the_tree_has.py` red on the report line above |
| The full suite, the repository-wide lint, the typecheck | **not run** — contract §2, the orchestrator's. `ruff` is in neither `.venv` nor `PATH`, so lint has run nowhere in this work item |
