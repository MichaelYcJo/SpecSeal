# Feature Specification: the fold ships, and the corpus is still on disk

<!-- seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

This work item applies `settle` to this repository for the first time: the
standing statements are written into `docs/`, every check carrying a
population floor over the record corpus is answered, and `settle --retire`
removes the directories the prose now covers. The mechanism is not being
built — it shipped — and nothing here invents procedure.

**Measured in this worktree at `6d410023`, by the framer, before the plan.**
`./bin/settle` reports **83 released and unfolded work items in 38 segments,
16 ungrouped, 0 skipped**. On disk: **100 directories** under `seal/specs/`
(99 released or in flight, plus this work item's own), **1,381 files**.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/settle/SKILL.md` §2 *Write one standing statement per segment* | one statement per segment, only what is still true, the newest work item wins, flat `docs/`, and every folded sentence carries `<!-- specs/<id> -->` on a line of its own |
| `skills/settle/SKILL.md` §3 *Answer every check that reads the corpus* | each floor gets **retire the case**, **re-point it at a fixture corpus**, or **decline** — and lowering a floor until the run passes is refused by name |
| `skills/settle/SKILL.md` §*What a fold branch owes* | a `survivors.md` range-row, and **nothing in `seal/ledger.md` moves** |
| `skills/settle/SKILL.md` §1 | an item with no ledger row, or with `tests/` anchors only, is **named rather than guessed at** — "yours to place, or to leave" |
| `docs/one-root-by-lifetime.md` §*What keeps `settle` light* | the step moves and does not verify; the prose half is a judgment the tool may not make |
| `docs/release-checklist.md` §2b | this is a separate branch and a separate pull request from the release-preparation commit, and it is run by hand |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | the changelog entry is `seal/specs/<id>/changelog.md`; any ledger row is `seal/ledger/<id>.md` |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* | governs the one permanent ledger row that anchors into a work item directory (G3 below) |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | folded prose uses `example.com` and `/Users/x/` |
| `tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `docs/` is inside the scanned set, so no folded sentence names the running version or any version at or above it |
| `tests/test_docs_line_wrap.py` | a file written wrapped goes into `COVERED` at birth; every new `docs/` file this work creates is wrapped at 88 columns and listed there |

### G1 · the fold record is the marker, and it is read at the top of `docs/`

`skills/verify/scripts/unverified_check.py#folded_items` reads **the top level
of `docs/` and no deeper**, and only lines `live_lines` calls live. Two
consequences the plan is built on: a segment anchored in
`docs/experiments/…` still lands in a top-level `docs/` file, and a marker
inside a fence or a commented-out draft records no fold.

### G2 · `settle --retire` removes exactly what a marker names

The retirement takes its candidates from the fold record, so the keep-list
below is enforced by **not writing those ids as markers**, never by editing
the script. Three other branches of this release are writing new work items
under `seal/specs/` while this one runs; nothing here reads "whatever is in
the tree".

### G3 · the one ledger row that anchors into a work item directory

`seal/ledger.md` line 78 anchors
`seal/specs/1788184145-the-gate-stops-the-session-editing-its-tests/rounds/round-3.md`,
and its own grounds say `settle` "has to re-anchor or drop this row when it
does". The repository rule refuses a re-point, and dropping the row deletes
verified evidence for a rule that still stands. **So that directory is kept**
— it is one of the 16 the tool leaves to a session anyway, and keeping eight
files is cheaper than losing the evidence. `seal/ledger.md` is therefore
byte-identical at the end of this branch.

## Scope

### In

| # | What |
|---|---|
| S1 | one standing statement per **segment**, 38 of them, each in the `docs/` file named by the plan, each carrying its work item's `<!-- specs/<id> -->` comment |
| S2 | the **16 ungrouped** items decided by the rule in *The rule for the ungrouped* below — 5 folded, 11 kept, each named |
| S3 | every check in this repository carrying a **population floor** over `seal/specs/`, enumerated by construction and each given one of the three sanctioned answers in writing |
| S4 | `settle --retire`, in a commit of its own, removing **exactly** the 88 directories the markers name |
| S5 | `seal/specs/1790076070-…/survivors.md` carrying the range-row the fold owes |
| S6 | `seal/specs/1790076070-…/changelog.md`; a `seal/ledger/1790076070-….md` fragment only for a claim this work establishes |
| S7 | the before/after measurement of the corpus, recorded in `overview.md` and the changelog fragment |

### Out — and why, one line each

| # | Not done | Why |
|---|---|---|
| O1 | #368's repair — neither the `git add -A` line in `docs/release-checklist.md` step 3 nor the `git ls-files` change | the issue offers two fix shapes and says both may be right; that choice is a gate change under `CONTRIBUTING.md` and belongs to whoever picks the shape. This branch **stages and commits the retirement before the broad gate runs**, so the defect cannot bite it, and reports what the gate said |
| O2 | #101's `seal export --check` nudge | it is a feature with four open questions of its own; this branch supplies only the measurement it waits on |
| O3 | re-pointing or removing any `seal/ledger.md` row | G3 — the one row at risk keeps its anchor because its directory is kept |
| O4 | `docs/one-root-by-lifetime.ko.md` and any other Korean mirror | no check pairs the `docs/` mirrors, and the only both-editions rule in the tree is the README pair's. A mirror sweep is its own work |
| O5 | unreleased work items, this work item's own directory, and anything an open `evidence-todo.md` row holds | `settle` reports 0 skipped today, and the released set is what the command resolves |
| O6 | judging whether a folded claim's code still behaves | `evidence-check`'s job; folding it in re-reads the whole ledger at every release |
| O7 | new `docs/` files below the top level, and `docs/experiments/` as a destination | G1 — a marker there is not a fold record |
| O8 | lowering any floor literal | `skills/settle/SKILL.md` §3 names that as the answer that turns a check into a comment |

## The rule for the ungrouped — decided here, not left open

Fifteen of the 16 are reported `no ledger row` and **two** are `tests only`
(`1788735085` and `1789540097`) — the framer counted the list rather than
taking the issue's *fifteen and one*, which is one off.

**The rule: an ungrouped item is folded where it wrote a `spec.md` stating a
rule that still governs. A directory holding no `spec.md` was below the SDD
ladder, states no rule, and is kept.** Six carry a `spec.md`; five of those
fold, and `1788184145` is kept for G3.

| Item | Decision | Grounds |
|---|---|---|
| `1788212517-the-last-rounds-fixes-are-reviewed-by-nobody` | fold → `docs/review-chain-spec.md` | it is where the verifying round comes from |
| `1788224363-a-subagent-rediscovers-what-the-session-established` | fold → `docs/review-handoff-protocol.md` | it is the handoff's own origin |
| `1788449488-measure-what-flow-finds` | fold → the measurement document | the segment its subject belongs to is `session_cost.py` |
| `1788735085-a-loaded-file-naming-a-real-version-is-a-timer` (`tests only`) | fold → `docs/release-checklist.md` | the checklist's own table already names the case this item wrote |
| `1789540097-three-checks-that-do-not-see-what-they-are-named-for` (`tests only`) | fold → the broad-gate document | its three checks are the gate's arms |
| `1788184145-the-gate-stops-the-session-editing-its-tests` | **keep** | G3 |
| `1788177600`, `1788217118`, `1788220055`, `1788276387`, `1788395377`, `1788425222`, `1788824000`, `1788938400`, `1789024700`, `1789053786` | **keep** | no `spec.md`: a release entry, a renumbering, a Windows CI repair, a PR-body record. Records of a moment, and a moment states no rule |

## The population floors — enumerated by construction

The class was enumerated with `grep -rn "seal/specs" tests/` (44 modules
name the path; 14 read the **real** corpus) and narrowed by reading each
reader. Every floor below is named with its coordinate and its post-fold
value, measured in this worktree.

| # | Coordinate | Floor | After the fold | Answer |
|---|---|---|---|---|
| F1 | `tests/test_chain_check_at_the_pull_request.py:2649` | `len(records) > 200` over `os.walk(seal/specs)` | **7** — red | re-point: derive the expected population from an independent listing of the tree (git at HEAD) and assert the walk equals it |
| F2 | `tests/test_chain_check_at_the_pull_request.py:2825` | the same floor in the fix-range sweep | **7** — red | as F1 |
| F3 | `tests/test_chain_check_at_the_pull_request.py:2852` | `assert carrying` — some record carries `\| Fix range \|` | **0** — red; every carrier is in the retire set | re-point the *carries the row* half at a record built in `tmp_path`; the real-corpus sweep keeps the *no record fails* half |
| F4 | `tests/test_a_finding_id_is_a_bare_integer.py:752` | `len(paths) > 100` | **7** — red | as F1 |
| F5 | `tests/test_a_finding_id_is_a_bare_integer.py:775` | `parsed > 100` | **≤ 7** — red | as F1, derived from the same listing |
| F6 | `tests/test_a_finding_id_is_a_bare_integer.py:776` | `assert teeth` — the rule refuses something in the corpus | unmeasured | measurement in phase 2; if no surviving record exercises it, re-point at a fixture record |
| F7 | `tests/test_the_set_a_work_item_always_has.py:342` | a live `seal/specs/*/evidence-todo.md` | **0 of 6** — red | re-point at a fixture tree holding both layouts |
| F8 | `tests/test_the_set_a_work_item_always_has.py:347` | a live `seal/specs/*/tests-todo.md` | **0 of 8** — red | as F7 |
| F9 | `tests/test_the_reopening_is_one.py:325` | the directory `REOPEN_FROM` (`1788597030`) names is in the tree | removed — red | re-point onto the fold record: the directory exists **or** `docs/` carries its marker, the same distinction `unverified_check.folded_items` already draws |
| F10 | `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:1250` | the directory `FLOOR_FROM` (`1788472135`) names is in the tree | removed — red | as F9 |
| F11 | `tests/test_a_finding_id_is_a_bare_integer.py:707` | `assert paths` — the corpus is not empty | **7** — green | decline: the floor is right and the population still exists |
| F12 | `tests/test_the_reopening_is_one.py:537` | `assert records` | **7** — green | decline |
| F13 | `tests/test_release_hygiene.py:1346` | a work item carries a `routing.md` | **12** — green | decline |
| F14 | `tests/test_routing_is_recorded.py:499` | declarations found | **12** — green | decline |
| F15 | `tests/test_the_pull_request_language_is_the_repositorys.py:229` | `assert mirrors` over `pr.*.md` | **4** — green | decline |
| F16 | `tests/test_unverified_rows_close.py:1897` | `len(occurrences) >= 90` over `<!-- specs/ -->` markers | unchanged | decline — its corpus is `seal/ledger.md`, which this branch does not touch. Named so nobody answers it by mistake |

**Readers with no floor, which shrink silently and must be re-measured rather
than trusted:** `tests/test_unverified_rows_close.py:341`,
`tests/test_chain_hooks_hardening.py:1344` and `:1367`,
`tests/test_handoff_outlives_the_merge.py:103`,
`tests/test_a_record_states_what_the_tree_has.py:999`,
`tests/test_release_hygiene.py:1165`, `tests/test_waiver_decided_at_start.py:792`,
`tests/test_a_corrected_sentence_survives_elsewhere.py` (the survivor corpus).

**A repair is green before the fold and after it.** A case that passes only
once the directories are gone is a lowering wearing a repair's clothes, and
the phase record says which of the two each change was shown to be.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 the prose exists | Given the 38 segments · When the prose phases close · Then `./bin/settle` lists no released, unfolded work item except the 11 kept ones | `./bin/settle`, read whole |
| A2 the removal is named | Given the keep-list in this spec · When `settle --retire` runs · Then the directories removed are exactly the 88 the markers name, and the 11 kept ones are still on disk | `git status --short` against the list; `ls seal/specs` |
| A3 every floor is answered | Given the table above · When phase 2 closes · Then each of F1–F16 carries a written answer and no floor literal was made smaller | the phase record; `git diff` of `tests/` |
| A4 the gate is green on the folded tree | Given the retirement committed · When the broad gate runs · Then every command exits 0, read directly and never through a pipe | `bin/test -q`, `uvx ruff check .`, `uvx ruff format --check .` — the sealer's run |
| A5 the removals read as folds | When `unverified_check.py --baseline origin/release/… seal/specs/` runs · Then every removed overview is reported **folded**, and none as a deletion | the command's own summary line |
| A6 the survivor sweep has its row | Given the fold removes shipped sections · When `survivor-check --range` runs with the exemption file · Then it is green | the hygiene step's command, run locally |
| A7 the ledger is untouched | Then `git diff --stat origin/release/… -- seal/ledger.md` is empty | the command |
| A8 nothing names the running version | Then the release-hygiene timer case is green over the new `docs/` prose | `tests/test_release_hygiene.py` |
| A9 the chain checker survives the removal | When `chain_check.py --baseline origin/main` runs after the retirement · Then its verdict is read and recorded, whatever it is | the command, exit code read directly |

## Data & interfaces

No schema, no endpoint. The interfaces this work touches are three file
shapes that already exist: the `<!-- specs/<id> -->` marker line, the
`survivors.md` range-row, and `plan.md`'s Status column.

## Open questions → questions.md

Four rows, one of them a person's. Everything the tree could answer is
answered above, in the two decided rules and the floor table.

Framed 2026-09-22 by framer, before the build.
