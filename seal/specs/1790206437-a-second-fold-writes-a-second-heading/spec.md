# Feature Specification: a second fold writes a second heading

<!-- seal/specs/1790206437-a-second-fold-writes-a-second-heading/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three sentences the 0.15.0 run found and could not fix, because each run's
one reopening was already spent. Each has a paste-ready block or a measured
instance in the round record that found it, and each is a patch to an
instrument the run uses on itself: no design, no new gate.

- **#540.** `.github/scripts/fold_ledger.py` builds `## X.Y.Z — <date>` in
  `section()` unconditionally and `append()` puts it below everything, so a
  second `--version X.Y.Z` — the ordinary shape when a release pull request
  goes red and a fragment lands after the preparation commit — writes a second
  heading for the same version into `seal/ledger.md`. #289 closed the same
  class in `gather_changelog.py` one file over. **The ticket says nobody has
  run the fold twice on this tree, and that is false: `seal/ledger.md` heads
  `0.9.3` twice today**, at lines 1673 and 1764 (the same date, adjacent
  sections), the second written by `4ac9bf35` the day after the 0.9.3
  preparation commit bee7ae99 — a fragment landing after the release
  pull request went red, exactly #289's shape.
- **#542.** Two sentences in `skills/code-review/scripts/round_record.py`
  describe the `Broad gate` cell's rule as it stood before round 2's `same_run`
  fix: the comment `new_broad_gate_file` writes into every `broad-gate.md`
  (*a run taken again is written in front, and the earlier one stays behind
  it*) and `kept_broad_gate`'s docstring (*the count of entries stop being the
  count of runs*). No test reads the written comment, so a third rewording
  reaches every `broad-gate.md` unpinned.
- **#366, the second half.** `round_record.py#depth_two` keys on a finding's
  `Location` and refuses every unit that finding's fix commit added in that
  file — so a finding whose coordinates sit at two depths (one inside a unit
  an earlier round's fixes created, the others not) has its depth-1 cases
  refused beside the depth-2 one. The three cases of the first half shipped in
  0.15.0 (`tests/test_a_release_is_sized_by_a_criterion.py:316`, `:326`,
  `:342`, read). What is left is the choice the ticket left open, and this
  frame decides it from the tree: the reviewing convention, not a finer
  check. Grounds under *Judgments the tree answered*, 6.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/release-checklist.md` §2 *Gather, fold, bump*: *A second gather for the same version appends into its section … the new entries join the existing section, the section keeps the first gather's date, and `tests/test_release_hygiene.py` refuses a file that heads a version twice* | The shape the fold mirrors, clause for clause: join, keep the first date, refuse a doubled heading. The paragraph gains one sentence saying the fold does the same |
| `docs/branch-and-release.md` §*The ledger fragments fold in the same commit*: *moves every fragment into `seal/ledger.md` under `## X.Y.Z — <date>` … `--check` reports a fragment left behind, and the hygiene workflow runs it beside the changelog check on every pull request into `main`* | The fold's contract and where `--check` runs. A doubled heading is a state `--check` can see and today does not refuse |
| `docs/one-root-by-lifetime.md` §*What happens at a release*, step 1: *This is a move, not a deletion: every row survives* | The 0.9.3 repair removes one heading line and no row; `evidence-check` reports the same totals before and after |
| `CLAUDE.md` §*a change writes fragments, never the shared file*: *Appended is the word, and a removal is not one* | The only edits this work makes to `seal/ledger.md` are a removal (the second `## 0.9.3` line), re-read notes on rows whose anchors it moves, and one correction note on a row whose claim it falsifies (A11). New rows go to this item's fragment |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `fold_ledger.py --check` is a hygiene arm at the release pull request; its new refusal carries the four answers: seen red against `9f846733:seal/ledger.md`, blocks more, prompt budget zero, a line-shaped read with no platform behind it |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides #366 between two designs that catch the same defect: a sentence the reviewer follows costs no gate change and no heuristic; a finer `depth_two` is design with a false-positive argument to make |
| `docs/review-chain-spec.md` §*The depth in `New units`*: *What no check can see is a depth declared wrong … The rule is a declaration, and the verifying round reading the `New units` surface is what looks at it* | The depth is per entry and declared, not derived. The convention sentence lands beside this paragraph: a finding whose coordinates sit at two depths is written as two findings |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed*: *Per entry rather than per round, because a single fix pass can answer a finding in code that predates the run and a finding inside an earlier unit in the same breath* | The rule already assumes one depth per finding; the convention makes the reviewer write findings that way |
| `templates/sdd-round.md:39`, the `Broad gate` row: *a run the newest entry already records — the same commit against the same base — replaces that entry rather than duplicating it, while a run at that commit against another base is kept behind the new entry* | The rule the two #542 sentences must state. The template is the pinned carrier (`tests/test_the_broad_gate_cell_keeps_every_run.py`), so it is the text the comment is brought to |
| `skills/agent-contract/SKILL.md` §14 (*a fix that changes what a person sees documents it and pins it, in the same commit*), §15 (*seen red*), §12 (*enumerate the class*) | The `broad-gate.md` comment is text a tool writes for a person to read, so it is pinned by a case over the written file. Every new case is shown red first. #540's class has two files and both are now closed; #542's class is the three carriers of one rule in one script |

## Scope

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #540 | The measured instance first: the second `## 0.9.3 — 2026-09-08` heading at `seal/ledger.md:1764` and the blank line after it are removed, joining `1788890000`'s section to the five above it under one heading; a real-tree case in `tests/test_release_hygiene.py` refuses a ledger that heads one version twice, red on arrival | Phase 1 |
| #540 | The fold joins a section the ledger already heads, keeps that section's first date, prints the heading it joins on `--dry-run`, and `--check` refuses a doubled version naming both lines; the module docstring and `docs/release-checklist.md` §2 say so | Phase 2 |
| #542 | The comment's last sentence and the docstring's count sentence take the round-3 report's two paste-ready blocks; a case in the seal module reads a written `broad-gate.md` for the new sentence; A9 is re-read and A11 corrected | Phase 3 |
| #366 | One sentence in the three places the reviewer copies from — a finding whose coordinates sit at two depths is written as two findings, one depth each — pinned by the report-standard module; `depth_two` is untouched; the ticket closes | Phase 4 |

### Out

| Left out | Why, and who answers |
|---|---|
| A finer `depth_two` that maps each added unit to what it asserts (#366's other option) | A gate change carrying a heuristic — what a test *asserts* is not in the AST, only which names it references — with `CONTRIBUTING.md`'s four answers and a false-positive argument nobody has made. The milestone's own rule for step D applies: design moves to 0.16.0. `questions.md` Q1 puts it in front of the owner without blocking this build |
| #547, the fold writing each release to its own file | Step D, built on top of this branch. Phase 2 adds two small helpers named as the gatherer's (`section_heading`, `insert`) and one reader (`doubled_versions`, NAME NOT IN TREE until phase 2 adds it), touches nothing in `fragments`, `demote`, `marker`, `is_marked` or `open_rows`, and leaves the `date = args.date or …` line byte-identical, so D rebases over three additions rather than a rewrite |
| A refusal of the second fold outright (*version already folded, exit 1*) | It leaves the red-release-pull-request shape with no path but a hand edit, which is how the second `0.9.3` heading got there. The gatherer's answer (#289) is join, and the fold takes the same one |
| Pinning `kept_broad_gate`'s docstring sentence by a test | It is a docstring, read by whoever opens the function; ledger row A9 anchors the unit and is re-read with a dated note in phase 3. Adding `round_record.py` to `GATE_CARRIERS` would pin the source rather than the written file round 2 and round 3 asked for, and would change A11's *eight documents* count for no reader's benefit |
| Rewording `DEPTH_EXIT` or any refusal line a person reads at the keyboard | `docs/review-chain-spec.md` §*Where a leftover goes* says rewording the pair is the repository owner's decision and a gate change; nothing here touches a refusal message |
| `gather_changelog.py`, `CHANGELOG.md` | #289 closed it; `CHANGELOG.md` heads no version twice (executed, 2026-09-24) |
| `docs/` beyond one sentence in `docs/release-checklist.md` §2 and one in `docs/review-chain-spec.md` §*The depth in `New units`* | A work item does not write policy; `settle` folds this spec at the release. The two sentences are edits to paragraphs that already state the rule each extends |
| A `--check` refusal of a doubled heading in `gather_changelog.py` for symmetry | The changelog's doubled heading is refused by `tests/test_release_hygiene.py` today and the release pull request runs that suite; adding a second reader there is mechanism nobody asked for. The fold gets the arm because #540 and #547 both name `--check` as where it belongs |

## The measured state, before the build

Read and executed 2026-09-24 by the framer at `9f846733` (the v0.15.0 tag, this
branch's base) in this worktree.

| Fact | How known |
|---|---|
| `seal/ledger.md` heads `0.9.3` at lines 1673 and 1764, both `— 2026-09-08`; the first holds five work items (`1788873600` … `1788873640`), the second one (`1788890000`); line 1763 is blank, 1765 is blank, 1766 is the marker | executed — `grep -n "^## "`, an `awk` over the two sections, a Python read of lines 1761–1768 |
| No other version heads the ledger twice; 30 version-shaped `## ` headings and 8 area headings, none of the areas version-shaped; the header quotes `## X.Y.Z — <date>` inside a `> ` blockquote line, which `^## ` does not match | executed — `grep "^## [0-9]" \| sort \| uniq -d` prints `## 0.9.3` alone |
| `CHANGELOG.md` heads no version twice | executed — the same pipeline, empty |
| The second `0.9.3` heading arrived in `4ac9bf35` (2026-09-09, *fix: the survivor step ran on a release range no fix pass wrote, and failed the release on it (#180)*), after the preparation commit bee7ae99 (*chore: release 0.9.3*) | executed — `git log -S'## 0.9.3 — ' -- seal/ledger.md` |
| Two more carriers describe a held run as always staying: `docs/review-handoff-protocol.md:171` (*a run taken again after a pre-existing failure or a late fix leaves both on the record*) and `skills/code-review/orchestration.md:528` (*in front of any run the cell already held, which stays behind it*). Under `same_run` a run at the same commit against the same base replaces the entry. Neither was re-read by `1790174138`'s round 3, whose proof lists the sealer, the spec and the template. `GATE_CARRIERS` pins both files on the phrase `earlier run`, which any rewording keeps | executed — `grep -rn "taken again\|stays behind\|earlier one stays\|count of runs\|count of entries" docs/ agents/ skills/ templates/ CONTRIBUTING.md` at `9f846733`: those two lines, the three in `round_record.py`, and four unrelated hits on other senses |
| `fold_ledger.py#section` builds the heading unconditionally, `#append` puts the block below everything, `#main` computes `date` from `--date` or today, and nothing searches the ledger for `## <version>`; the marker refusal (`folded`) is the only re-run guard | read — the whole script |
| `gather_changelog.py#section_heading`, `#existing_date`, `#insert` and `#main`'s `found`/`heading` lines are #289's fix; `tests/test_the_changelog_is_gathered_at_release.py#test_a_second_gather_for_the_same_version_appends_into_its_section` and `tests/test_release_hygiene.py#duplicated_version_headings` are its cases; ledger row P3 (§0.15.0, `1790173209`) records them | read |
| `tests/test_the_ledger_fragments_fold_at_release.py`'s `tree` fixture puts the version section last; `test_the_section_is_appended_below_the_existing_areas` asserts the last `## ` starts with the version; `test_folding_twice_finds_nothing_and_writes_nothing` re-runs with no new fragment and expects exit 1 | read |
| `round_record.py:4263-4290` (`new_broad_gate_file`) writes the comment; its last sentence is the one the ticket quotes. `:347-384` (`kept_broad_gate`) carries the count sentence at `:363-365`. `:387-402` (`same_run`) is the rule | read |
| The seal module's direct-home cases (`test_seal_writes_a_file_where_no_round_record_exists`, `test_the_direct_home_takes_the_same_shape_on_a_re_seal`) read the written file's cell through `fields(text)[ROW]` and count its table lines; none reads the comment | read; round 3's grep over `tests/` for the sentence hit one docstring |
| `tests/test_the_broad_gate_cell_keeps_every_run.py#GATE_CARRIERS` pins eight documents as gone/stands pairs; ledger row A11 (§0.15.0, `1790174138`) says the ninth carrier is the written comment and that no test pins it; A9's clause was corrected in the fragment before the fold to *distinct comparisons, commit and base* | read |
| `depth_two` (`round_record.py:3701`) builds `candidates` from every unit the range added in the Location's file and narrows them by `unit_adders` to the finding whose fix commit added each; one commit answering one finding with three coordinates resolves every unit to that finding | read |
| The report standard is one text in `agents/warden.md`, `skills/code-review/SKILL.md` and `docs/review-chain-spec.md`, pinned by `tests/test_the_report_standard_is_one_in_three_places.py` (`CARRIERS`, and `WARDEN` for sentences only the warden carries) | read |
| Python floor 3.12 (`round_record.py#FLOOR`); `zip(strict=True)` and `datetime.UTC` are in use already | read |

## User scenarios & acceptance *(mandatory)*

Every new case is seen red before it is committed (§15), and the hand-back
says how. Line numbers are as of `9f846733` and are for opening, never for
anchoring.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the repair | Given `seal/ledger.md` at `9f846733`. When line 1764 (`## 0.9.3 — 2026-09-08`) and the blank line 1765 are removed, then `1788890000`'s marker and `###` sit under the first `0.9.3` heading after `1788873640`'s rows, every table row is byte-identical, `evidence-check --strict .` reports the same totals before and after, and `fold_ledger.py --check` exits 0 with the same *work items marked* count | executed by the builder: the totals line before and after, `git diff --stat` showing two deleted lines and nothing else in the file |
| S2 · the real tree refuses a doubled version | `tests/test_release_hygiene.py#test_no_version_heads_two_sections_of_this_ledger`, beside the changelog case, reading `seal/ledger.md` through `duplicated_version_headings` (already proven against a doubled fixture by `test_a_version_heading_appears_once_in_a_changelog`). Then the message names the version and both lines and says *one release, one section* | red on arrival: run at `9f846733` before S1, `0.9.3 twice, at lines [1673, 1764]`; green after S1. The phase record carries both runs |
| S3 · a second fold joins the section | Given the fixture folded once (`0.4.0`, `2026-09-15`) and a new fragment `1788300000-late` written after. When `--version 0.4.0 --date 2026-09-16` runs, then exit 0; `^## ` headings are `Coordinates`, `An area from before the fragments`, `0.4.0 — 2026-09-15` and no other; the new marker and `### 1788300000-late` stand under it after `1788229400-later`'s section; the fragment is gone; `--check` then exits 0 naming three work items marked | red today: a second `0.4.0 — 2026-09-16` heading. The marker refusal (`test_a_fragment_whose_marker_is_already_in_the_ledger_is_refused`) still comes first and is unchanged |
| S4 · the joined section is one section, wherever it stands | Given S3's tree with an area heading appended after the version section (the shape the real ledger never has today but `insert` must not depend on). When the second fold runs, then the entries land before that next `## `, one blank line each side, no run of three newlines | mirrors the gather case's placement assertion; red today |
| S5 · the date is the first fold's | S3's heading keeps `2026-09-15` although `--date 2026-09-16` was passed; with no `--date`, today's date is not written either | asserted in S3; the `date = args.date or datetime…` line stays byte-identical (`plan.md` §Technical context says why) |
| S6 · the dry run says what the write will do | Given S3's tree. When `--dry-run --version 0.4.0` runs, then stdout shows `appending into the existing section:` and the existing heading `## 0.4.0 — 2026-09-15`, not a fresh one; nothing is written or removed | mirrors `test_a_dry_run_of_a_second_gather_shows_the_section_it_appends_into`; red today |
| S7 · the fold's message | S3's run prints `folded 1 fragments into seal/ledger.md under ## 0.4.0 — 2026-09-15 (appended into the existing section)` and names the fragment | asserted in S3 |
| S8 · `--check` refuses a doubled version | Given a folded fixture whose ledger carries a second `## 0.4.0 — …` heading planted by the case. When `--check` runs, then exit 1, the output names `0.4.0` and both line numbers and says one release, one section; the fragment and open-row reports are still printed when they apply. Given the fixture folded once, `--check` exits 0 and its count line is unchanged | red today: exit 0 over the planted file. Real-tree red: the new arm run with `--root` pointed at a scratch copy holding `git show 9f846733:seal/ledger.md` refuses `0.9.3` |
| S9 · the documents say it | `docs/release-checklist.md` §2's paragraph on the second gather gains one sentence: the fold does the same — joins the section, keeps the date, and `--check` refuses a ledger that heads a version twice. `fold_ledger.py`'s module docstring names the join under its `--version` line and the doubled-heading refusal under `--check` and in the exit-code paragraph | read by the reviewer; `test_the_release_sequence_names_the_fold_beside_the_gather` still passes (it reads `branch-and-release.md` and `CONTRIBUTING.md`, neither of which changes) |
| S10 · the written comment states the rule | Given a work item declaring `straight to the PR`. When `seal` writes `broad-gate.md`, then its comment, whitespace collapsed, carries *a run the newest entry already records — the same commit against the same base — replaces it* and does not carry *a run taken again is written in front*. The text is the round-3 report's block, verbatim | `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_written_broad_gate_file_says_a_same_run_re_seal_replaces_its_entry`, beside `test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list`; red against the unedited generator on the stands half, and on the gone half once the old sentence is restored |
| S11 · the docstring states the rule | `kept_broad_gate`'s sentence at `:363-365` reads the round-3 report's block: *the count of distinct comparisons — commit and base — which is what the run-level table reads off the cell* | read; ledger row A9 re-read with a dated note, `evidence-check --reverify` recomputing `kept_broad_gate`'s hash |
| S11b · the class, not the coordinate | The two carriers the measured-state table names — `docs/review-handoff-protocol.md`'s `Broad gate` row and `skills/code-review/orchestration.md`'s sealer paragraph — are read against `templates/sdd-round.md:39`'s clause; each that states a held run always stays is brought to the same-commit-same-base replace in one clause, and each that already reads true is left and said so in the phase record. `GATE_CARRIERS`' stands phrase for both files (`earlier run`) survives either way, so the pin is unchanged | read by the builder and the reviewer; `tests/test_the_broad_gate_cell_keeps_every_run.py` green; the phase-3 record names the judgment per carrier (§12) |
| S12 · A11 stops saying the comment is unpinned | The row's clause *a code comment no test pins* is corrected in place with a `Corrected <date>` note naming S10's case, the way A9 in the same section carries its own; the anchors are untouched and resolve | read; `evidence-check --strict .` exit 0; `questions.md` Q3 holds the alternative |
| S13 · the convention sentence | `agents/warden.md` (beside the paragraph on the previous record's `New units` surface), `skills/code-review/SKILL.md` §*Findings format* and `docs/review-chain-spec.md` §*The depth in `New units`* each carry, in the same words: *a finding whose coordinates sit at two depths — one inside a unit an earlier round's fixes created, another not — is written as two findings, so each verdict carries one depth and the fix of one does not refuse the units the other's fix adds* | `tests/test_the_report_standard_is_one_in_three_places.py#test_every_carrier_tells_the_reviewer_to_split_a_finding_that_sits_at_two_depths`, the phrase pinned in the three `CARRIERS` files that the reviewer copies from (not the template); red with the sentence deleted from any one carrier |
| S14 · nothing else moves | `depth_two`, `unit_adders`, `location_units`, `DEPTH_EXIT`, `same_run`, `kept_broad_gate`'s body, `seal`'s refusals, `gather_changelog.py`, `fold_ledger.py#fragments`/`#demote`/`#marker`/`#is_marked`/`#open_rows`: unchanged. `tests/test_docs_line_wrap.py` green over the edited documents | executed by the builder at each phase close: the module runs named in `plan.md`; `git diff --stat` at hand-back |
| S15 · the ledger stays true | Rows whose anchors this work moves are re-read and re-stamped with a dated note: the rows on `.github/scripts/fold_ledger.py`'s `section`, `main` and `append` (if touched) in §0.4.0; A9 on `skills/code-review/scripts/round_record.py`'s `kept_broad_gate` (the stamps are the ledger's, not this file's — `evidence-check`'s records arm reads a short path beside a hash as a file it cannot find); `tests/test_the_report_standard_is_one_in_three_places.py` anchors if a constant moves. `evidence-check --strict .` exit 0 at each phase close | executed |
| S16 · the branch's own sweep | `survivor-check --range origin/release/v0.15.1...HEAD` at hand-back exits 0, with a `survivors.md` row for any place it reports; `questions.md` Q4 names the one expected | executed at the verify phase |

## Data & interfaces

**`.github/scripts/fold_ledger.py`**

- `section_heading(ledger_text, version)` — the match for the `## <version>`
  line the file already has, or `None`; the gatherer's regex,
  `^## <version>\b(?: — (\S+))?.*$`, multiline.
- `insert(ledger_text, block, version)` — into the section `version` already
  heads, before the next `## `, dropping `block`'s heading and re-adding one
  blank line; otherwise `append`. Shape and blank-line handling as
  `gather_changelog.py#insert`, whose round-1 finding about a run of three
  newlines is already paid for there.
- `doubled_versions(text)` — `[(version, [line numbers])]` for every version
  a `^## (\d+\.\d+\.\d+)\b` line heads twice; the hygiene module's reader,
  spelled in the script because a script cannot import a test.
- `main` — `--check` prints the doubled versions with both lines and exits 1
  (with the fragment and open-row reports, when they apply); the fold reads
  `section_heading` once, keeps a found date, prints the heading it joins.
  **The line `date = args.date or datetime.datetime.now(datetime.UTC)…` stays
  byte-identical**: `1790173209`'s `survivors.md` quotes it as standing
  text, and the survivor sweep over this branch's range would otherwise
  report the gatherer's near-identical line as a survivor (Q4).
- The module docstring: one sentence under the `--version` line, one under
  `--check`, the exit-code paragraph gaining *a version headed twice*.

**`seal/ledger.md`** — line 1764 and 1765 removed (S1); A11's clause corrected
in place (S12); re-read notes and recomputed hashes on the rows S15 names.
Nothing appended.

**`skills/code-review/scripts/round_record.py`** — two string edits, the
round-3 report's blocks verbatim; nothing else.

**`agents/warden.md`, `skills/code-review/SKILL.md`, `docs/review-chain-spec.md`**
— one sentence each (S13). **`docs/release-checklist.md`** — one sentence (S9).

**Tests** — `tests/test_the_ledger_fragments_fold_at_release.py` (S3–S8),
`tests/test_release_hygiene.py` (S2), `tests/test_the_seal_is_taken_once_by_the_sealer.py`
(S10), `tests/test_the_report_standard_is_one_in_three_places.py` (S13).

**`seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`** — the new
rows: F1 the join and the kept date (S3–S7), F2 the `--check` refusal (S8),
F3 the real-tree case and the repair (S1, S2), B1 the written comment and its
case (S10), B2 the docstring (S11), D1 the convention sentence and its pin
(S13). Each names the case that saw it red.

**`seal/specs/1790206437-…/changelog.md`** — one entry per ticket, in the
fragment, never `CHANGELOG.md`.

**Unchanged on purpose**: `.github/workflows/hygiene.yml`, `gather_changelog.py`,
`chain_check.py`, `templates/`, `skills/code-review/orchestration.md`,
`agents/smith.md`, `agents/sealer.md`, `bin/`.

## Judgments the tree answered

Listed so nobody reopens them; each can be overturned by opening what is
cited.

1. **#540's premise is measured, not read.** The ticket says nobody has run
   the fold twice for one version on this tree. `seal/ledger.md` heads
   `0.9.3` twice, and `git log -S` names the commit and the day. The work
   starts with the repair and a real-tree case that is red before it.
2. **Join, do not refuse.** A second fold is the ordinary red-release shape
   (`docs/release-checklist.md` §2 says so of the gather), and a refusal
   would leave it a hand edit, which is what produced the instance in 1.
3. **`--check` gets the refusal, and the hygiene suite gets the real-tree
   case.** #540 and #547 both name `--check` as the home; #289's fix put the
   changelog's refusal in `tests/test_release_hygiene.py`, which runs on
   every pull request where `--check` runs only at the release. Both, at a
   cost of one reader each.
4. **The repair is two deleted lines.** The two `0.9.3` sections are
   adjacent and share a date, so removing the second heading and its blank
   line joins them; no row moves, so no parallel branch's re-stamp hunk is
   touched.
5. **The written comment is pinned by a case over the written file** (the
   ticket's first option), not left unpinned with a note at `GATE_CARRIERS`
   (its second). `agent-contract` §14 and `1790174138`'s own `plan.md`
   (*a red test rather than a stale sentence*) decide it; round 2 and round
   3 each asked for exactly that case.
6. **#366's second half is the reviewing convention.** The ticket left the
   choice open; the milestone lists the ticket under *the sentences* and
   says *no design and no new gate*; `CLAUDE.md`'s first goal prefers the
   design that adds no question and no heuristic; the finer check would map
   an added unit to *what it asserts*, which an AST cannot read and a gate
   would guess at. The convention costs one sentence in the three places the
   reviewer copies from and one pin. `depth_two` is untouched, and its
   refusal already names the finding whose fix added the unit, so a reviewer
   who did not split reads exactly which finding to split next round.
7. **The convention sentence has three carriers, not four.**
   `templates/sdd-round.md`'s comment describes the record's shape; the
   reviewer writes findings from `agents/warden.md` and
   `skills/code-review/SKILL.md`, and the spec is the policy both cite.
8. **A11 is corrected in place.** The row's anchors still resolve; only its
   last clause goes false, by a case this branch adds. A9 one row up already
   carries a `Corrected <date>` note in the same section and
   `correction_check.py` reads that marker. Q3 records the other shape.
9. **The date line is not edited.** The kept date is decided beside it, not
   in it, so the sweep has nothing removed to chase (Q4).
10. **#542 is a class of five carriers, not three.** The ticket names the
    comment and the docstring; the frame's grep adds the handoff protocol's
    `Broad gate` row and the orchestration skill's sealer paragraph, neither
    re-read by round 3 for `same_run`. Both are read in phase 3 and brought
    to the template's clause where they state the replaced rule (S11b).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is five
rows: one for a person that does not block (Q1, the finer `depth_two`), two
for the work (Q2, Q3) and two measurements (Q4, Q5).

Framed 2026-09-24 by framer, before the build.
