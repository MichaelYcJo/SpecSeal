# Feature Specification: survivors.md silences what it quotes

<!-- seal/specs/1790174139-survivors-md-silences-what-it-quotes/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

The survivor sweep (`survivor-check`, `skills/code-review/scripts/survivor_check.py`)
reports every place at a range's tip that still carries wording the range
removed. Its escape is a row in the work item's own
`seal/specs/<id>/survivors.md`: the standing text quoted, the grounds beside
it, and the survivor still printed under `exempt` so a reader at the pull
request sees what was excused and why. On three pull requests of the 0.14.0
release the file did the opposite of that. Committing it made the survivors
it quoted disappear from the report, with `--exempt` and without it, and not
one `exempt` line was printed. The check went green because the survivors
were no longer found, not because they were excused.

This work makes the exemption file, and the other records under a work item
directory that quote wording in order to record it, invisible to the search
on both of its sides. A survivor is then found, and the row is read, judged
against its quote, and printed with its grounds — which is the only thing a
row was ever supposed to do.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else*: *A survivor that is a deliberate carrier is exempted by a content-anchored row in the work item's own `seal/specs/<id>/survivors.md`, so the exemption stops holding the moment that text changes* | An exemption is a row that is READ against the standing text. Anything that removes the survivor before the row is consulted breaks the anchor: a row that cannot be consulted cannot rot loudly, so its quote stops meaning anything |
| Same section, the folded statement of `1789211172`: *A round record is outside the sweep's corpus on both sides. A record is the write-up of a finding rather than a carrier of the claim* | The exclusion shape this work extends. It is a predicate on the path's own shape, and it holds on the pool and on the range's path list alike — #365 is what one-sided exclusion cost |
| `survivor_check.py` module docstring §*The escape, which is not turning it off*: *An exempted survivor is still printed, under `exempt`, with its grounds — a row that silences something invisibly is a row nobody audits. There is no value meaning* check nothing | The property the three pull requests lost. The fix is judged by whether the `exempt` line prints, never by the exit code alone |
| `survivor_check.py` module docstring §*What is excluded, by construction rather than by list* | Exclusions are by the path's shape, never by a list of files, and the docstring names each one and which side it holds on. `tests/test_a_corrected_sentence_survives_elsewhere.py#test_the_docstring_names_both_sides_of_the_round_record_exclusion` pins the sentence |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every phase carries a test seen red, a stated failure direction, a prompt budget and platform honesty. All three phases make the gate find MORE or refuse MORE; the prompt budget is zero; the platform question is a path shape read from `git` output, which uses `/` |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The reader of the `exempt` lines at the pull request is the whole review of an exemption. Nothing here asks a person anything at run time |
| `skills/agent-contract/SKILL.md` §12 (*A defect belongs to a class — enumerate the class*) and §15 (*A new case is not planted until it has been seen red*) | The class is *a file under a work item directory that records or judges a past state and instructs nobody*: round records and reviewer reports (already excluded), the exemption file (#507, #308), phase records (#460). Each case is shown red against the unedited module first |
| `skills/implement/SKILL.md` §*The SDD file set*, the `phases/phase-N.md` row: *what this phase was asked, what building it found, what it removed from the tree* | What a phase record IS, which is what puts it in the class above and answers #460 from the tree |

## Scope

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #507 | The **range** half. `corrected()` reads every path the range touched, including a committed `survivors.md`, and returns the n-grams the range wrote; `wanted()` subtracts them. An exemption row's quote is the survivor's own wording, so the survivor leaves the search set before `--exempt` is consulted. #371 described this half, was closed on 2026-09-13 as completed with no pull request and no change to the module, and #507 is its re-filing; #532 was closed as a duplicate | Phase 1 |
| #308 | The **corpus** half. `corpus()` reads every tracked file at the tip except round records, so a committed `survivors.md` is one more carrier of exactly the phrases that produced the score, `df` rises, the weight falls, and a survivor near the floor drops under it. The title of #308 reads as the range half; the ticket's own comments and `seal/follow-up.md`'s row say it is the corpus half. Both halves land here, so the title needs no re-pointing | Phase 1 |
| #460 | A phase record (`seal/specs/<id>/phases/phase-N.md`) is the same kind of file as a round record — a record of what a phase was asked, found and removed — and is not excluded. Left in the pool it is reported as a survivor and dilutes the real ones; left in the range it subtracts what it quotes, which is #507's shape one directory over | Phase 2 |
| #304 | `OWNER_DIR`'s tail is `[^/]+$`, so a `survivors.md` one directory deeper than the layout has no owner, and an ownerless declaration keeps the unbounded reach the owner check exists to refuse. CI cannot reach it (`hygiene.yml` globs one level); a hand run can | Phase 3 |

The `seal/follow-up.md` row opening *Writing a `survivors.md` row silences its survivor a SECOND way, and that way does not rot* is the range half waiting on this work. This work is that prerequisite: the row is deleted when phase 1 closes, and what it asked a person — *whether that exclusion is right* — is answered below under *Judgments the tree answered*.

### Out

| Left out | Why, and who answers |
|---|---|
| #366, *the release-sizing sweep's reach is unpinned* | A different subject. Its module is `tests/test_a_release_is_sized_by_a_criterion.py`, not the survivor sweep; its open question is `skills/code-review/scripts/round_record.py#depth_two`'s handling of a finding whose `Location` spans two depths, and `round_record.py` is work item A's file (the review record). Two drafted cases in a retired work item's round-2 report pin `STATES_A_SIZE` and `SCANNED`; they are a test-only change that rides whichever branch takes the depth question. `questions.md` Q1 puts the home in front of the owner; the default is A, and this build does not wait on the answer |
| A live file the range writes that quotes the old wording — `overview.md`, `changelog.md`, a ledger fragment — subtracting the survivor it quotes | The same arithmetic as #507, but those files are live statements (#460 §*Not this*), and *a phrase the fix kept is not a phrase the fix corrected* is the rule that makes the score mean *removed*. Excluding them would exclude the three places #423's pass found one false fact standing. Phase 1 measures whether any survivor of the three pull requests still vanishes this way (`questions.md` Q3); if one does, the count goes to `overview.md` §*Not done* with the repository owner named |
| `OWNER_DIR` accepting the pre-0.4.0 top-level `specs/` root the way `WORK_ITEM_DIR` does | Harm needs every exemption file in a tree handed to one run, and only this repository's `hygiene.yml` does that, over `seal/specs/*` alone. A hand run passes the one file whose range it is. Named here so the next reader of `OWNER_DIR` does not take the omission for an oversight; the repository owner decides whether it is ever worth a line |
| The shape #423's pass found in a phase record — a correction inside an HTML comment while the false claim rendered in bold — which the sweep caught only because phase records were in the pool | Phase 2 gives that catch up, on purpose, and says so. Nothing else checks the shape. Phase 2 writes a `seal/follow-up.md` row naming the repository owner as the answerer for whether a marker-shape checker is worth building; `questions.md` Q5 |
| Widening the `seal/specs/*/survivors.md` glob in `.github/workflows/hygiene.yml` | #304 §*Not this*: it would hand CI the deeper files and make the hole reachable where it is not |
| `docs/` | A work item does not write policy; `settle` folds this spec at the release |
| `skills/code-review/orchestration.md`, `agents/smith.md`, the templates | Each says *correct each report, or answer it in `survivors.md` with a quote and the grounds*, and that sentence becomes true again rather than different |

## The measured state, before the build

Executed 2026-09-23 by the framer at `cdc8d182` in this worktree, over the
squash commits of the three 0.14.0 pull requests the milestone names. The
range `<squash>^..<squash>` is exactly the range each pull request was checked
over, and the exemption file is the one that pull request committed and that
still stands in the tree.

| Pull request | Range | Path rows in its `survivors.md` | With `--exempt <its file>` | Without `--exempt` |
|---|---|---|---|---|
| #525, `1790138190-settle-leaves-twelve-directories-with-no-way-out` | `f8f1c9d..edd022a`, 162 sentences removed | 29 | exit 0, **7** `exempt` lines | exit 1, 7 standing |
| #528, `1790154759-the-review-arm-asks-where-no-reviewer-compares` | `c626382..24ea206`, 5 sentences removed | 4 | exit 0, **0** `exempt` lines | exit 0, 0 standing |
| #527, `1790154761-folded-statements-pile-into-one-spec` | `edd022a..c626382`, 8 sentences removed | 3 | exit 0, **0** `exempt` lines | exit 0, 0 standing |

Read, not re-executed: #525's own round-1 report measured 15 places before
its `survivors.md` existed and 7 after, with 15 again once the file was
removed in a probe; #528's round-2 report measured its four rows printing
under `exempt` against a tip without the file and none of them at the real
tip; #527's round-3 report measured its three survivors returning once the
quotes were replaced by text matching nothing. So on the three pull requests
29 + 4 + 3 = 36 rows were written and 7 were consulted. The 29 that were not
were silenced by the file that holds them.

## User scenarios & acceptance *(mandatory)*

Every case below is a case in `tests/test_a_corrected_sentence_survives_elsewhere.py`
unless it says otherwise, built the way that module's `build()` fixtures are
built, and each is seen red against the unedited module before it is
committed (§15), with the hand-back saying how.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the range half (#507) | Given a claim stated in two files and a range that corrects one of them AND adds `seal/specs/<id>/survivors.md` quoting the other. When the check runs without `--exempt`, then the survivor is reported, exit 1, and the removed-sentence count is unchanged (`against 1 sentence(s)`). When it runs with `--exempt <that file>`, then the survivor prints under `exempt` with the row's grounds and the run says `every survivor is excused by a row above (1)`, exit 0 | Red today: exit 0 and `no removed wording is still standing` in both runs. The case mirrors `test_a_round_record_the_range_added_does_not_subtract_the_survivor_it_quotes` |
| S2 · the corpus half (#308) | Given the same two files and a `survivors.md` committed BEFORE the range (so it is in the pool and not in the range) quoting the surviving sentence. When the check runs, then the survivor's score is the score it has with the file absent, and the phrase the report names is the strongest shared phrase, not a weaker one. The assertion is on which phrase is reported and on the score, both, because #308's second comment measured two scores under the floor that were both the weaker phrase | Red today: with `N = 3` and a four-file corpus, one extra carrier halves the weight of every phrase the row quotes |
| S3 · the file is invisible to the search | Given any of S1's or S2's trees. When the check runs without `--exempt` at a tip with the file and at the same tip with the file deleted in a further commit, then the two reports name the same candidates with the same scores | The property the three pull requests lost, stated as one invariant. Also run over the three real ranges in S5 |
| S4 · the file is never a source | Given a range that edits only `seal/specs/<id>/survivors.md`. When the check runs, then `against 0 sentence(s)` and exit 0 | Mirrors `test_a_round_record_the_range_edited_does_not_become_a_source`. Red today: a reflowed row reads as a corrected sentence somebody has to chase |
| S5 · the three pull requests | For each row of the table above, after phase 1 and again after phase 2: with `--exempt <its file>` exit 0 and every line under `exempt` names a row of that file; without `--exempt` exit 1 and the count of standing places equals the count of `exempt` lines; that count is at least the number measured today (7 / 0 / 0) and is written into the phase record beside today's number; a probe commit deleting the file at the tip changes neither count | Executed by the builder with the numbers read into `phases/phase-1.md` and `phases/phase-2.md`. The probe is one Python script driving `git` (§8) in a scratch clone, run once, deleted |
| S6 · a phase record is a record (#460) | Given the trees of S1 and S4 with `seal/specs/<id>/phases/phase-3.md` in place of `survivors.md`. Then a phase record the range added does not subtract the survivor it quotes; one the range edited is not a source; and one standing in the pool at the tip carrying the removed wording is not reported | Three cases, red today in the directions S1 and S4 name and, for the pool half, a phase record reported as a survivor |
| S7 · a deeper exemption file has an owner (#304) | Given a `survivors.md` at `seal/specs/<id>/deeper/survivors.md` holding a `\| Range \| Grounds \|` row whose range resolves to this run's range, and a range that touches nothing under `seal/specs/<id>/`. When the check runs with that file as `--exempt`, then the run prints `not yours` naming `seal/specs/<id>` and every survivor is still reported. Given the same file at the layout position, then nothing changes from today | Red today: the deeper file matches no owner, the declaration keeps the old reach, and the run is excused with no line printed. Mirrors `test_a_declaration_does_not_reach_a_work_item_that_did_not_write_it` |
| S8 · the class is enumerated from the source | Every regular expression in the module that reads a path segment is listed in the phase-3 record with what a deeper path does to it. `OWNER_DIR` is the one whose tail stops a segment short; `WORK_ITEM_DIR` is anchored at the start and reads a prefix, so a deeper path matches it | Read by the builder, written into `phases/phase-3.md` |
| S9 · the docstring names each exclusion and both sides | The §*What is excluded* section keeps `**A record of a past round.**` as its first exclusion (the pinning case requires it), and adds the exemption file and the phase record, each saying it holds on the pool and on the range, on both sides of the path list. The pinning case is extended to the two new paragraphs the same way it pins the first | `test_the_docstring_names_both_sides_of_the_round_record_exclusion` extended, seen red with each new paragraph deleted |
| S10 · every path list is still classified | `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` passes with the predicate the build chooses in `corrected` and `corpus`, and `whole_range`'s list stays unfiltered with its `foreign` grounds | Executed. The test's `PREDICATE` constant follows the name; nothing else in it changes |
| S11 · the round-record cases still pass unchanged | Every case in the module that was green at `cdc8d182` is green after each phase, unedited except where S9 and S10 say | `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py` at each phase boundary; the count read directly |
| S12 · the branch's own sweep | `survivor-check --range origin/release/v0.15.0...HEAD --exempt seal/specs/1790174139-survivors-md-silences-what-it-quotes/survivors.md` exits 0 at the hand-back, and each `exempt` line, if any, names a row of this item's file. The rewritten docstring sentences have folded copies in `docs/review-chain-spec.md`, which is where a survivor will stand | Executed in the verify phase, which is also the first real run of the fix on a range that writes an exemption file |

## Data & interfaces

**`skills/code-review/scripts/survivor_check.py`**

- One predicate for the class, applied where `records_a_past_round` is
  applied today: `corrected`'s `paths` and `corpus`'s pool. It is true for a
  round record (`records_a_past_round` unchanged, so ledger row S6's anchor on
  it holds), for a `survivors.md` sitting directly under a `specs/<id>/`
  directory, and for anything under a `specs/<id>/phases/` directory. Matched
  on the path's own shape, at either `seal/` root, the way the existing
  predicate is. The name is the builder's (`questions.md` Q4); what is pinned
  is the class and the two call sites.
- `whole_range`'s changed-file list stays unfiltered. A `survivors.md` under
  `seal/specs/<id>/` is evidence that the range touches its own work item,
  and filtering it there turns a legitimate declaration into `foreign`
  (`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`'s
  `NAMED_EXCEPTION`, and #371's own paragraph on `whole_range`).
- `OWNER_DIR`: the tail `/[^/]+$` becomes `/.+$`, so the owner is the
  `seal/specs/<id>` prefix wherever the file sits beneath it. The ownership
  test in `whole_range` is unchanged and now reaches the deeper file.
- The docstring's §*What is excluded* gains one paragraph per new member of
  the class, each naming both sides; §*The escape* is unchanged because it
  was true of the design and becomes true of the code.

**`tests/test_a_corrected_sentence_survives_elsewhere.py`**: the cases S1–S4,
S6, S7 and the extensions S9 and S10. `PREDICATE` follows the predicate's
name.

**`seal/ledger.md`** — rows whose anchors this change moves, every claim
still true, so each is re-read and re-stamped with
`evidence-check --reverify .`, never re-pointed or removed:
`corpus@cfdd6a91` (S6 of `1788873640`), `corrected@6652b30d` (S1 of
`1789211172` and G5 of `1790138190`), the docstring section
`"## What is excluded, by construction rather than by list"@57f0406a` (S3 of
`1789211172`), `OWNER_DIR@09c29ef5` (G5 of `1788912166`), and the two test
functions S9 and S10 extend. Work items A and C also re-stamp rows in this
file; a conflict there is resolved hunk by hunk, both sides read
(`CLAUDE.md` §*a change writes fragments*).

**`seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md`**: the
new rows — one per member of the class stating the side it holds on and the
case that saw it red, one for `OWNER_DIR`, one for the S5 table.

**`seal/follow-up.md`**: the row opening *Writing a `survivors.md` row
silences its survivor a SECOND way* is deleted at phase 1 (discharged); a row
for the phase-record loss is added at phase 2, the repository owner named.

**`seal/specs/1790174139-survivors-md-silences-what-it-quotes/changelog.md`**:
one entry per phase, in the fragment, never `CHANGELOG.md`.

**Unchanged on purpose**: `.github/workflows/hygiene.yml`, `docs/`,
`skills/code-review/orchestration.md`, `agents/smith.md`, `templates/`,
`bin/survivor-check`.

## Judgments the tree answered

Listed so nobody reopens them; each can be overturned by opening what is
cited.

1. **Both halves land, in one phase.** #308's third comment and #371's
   comment measure that landing either alone leaves the row silenced by the
   other path. The three pull requests' numbers above are the same fact.
2. **The exclusion is right, on both sides.** `seal/follow-up.md`'s row asked
   a person whether excluding the exemption file is right, and argued that
   *a branch may legitimately edit prose in the same commit as its exemption
   file*. Exclusion is per path, so prose edited in the same commit in any
   other file is measured exactly as before; the only prose in `survivors.md`
   is a grounds cell, which is a judgment about the range and instructs
   nobody. The one-sided exclusion was measured at three tips by #365 and is
   the shape refused.
3. **A phase record is excluded whole, not sentence by sentence.** #460
   offered the narrower answer — only the quoted original inside a
   correction marker. That needs a marker syntax the repository does not
   have and a parser for it, which is mechanism nobody asked for; and the
   dilution half of the defect (the file as a further carrier) is not about
   quotes at all. What is given up is named under *Out* and goes to
   `seal/follow-up.md`.
4. **A phase record being edited while its work item is live does not keep
   it in the sweep.** A round record is too: `round_record.py close` writes
   into it, and its `Deferred` and `Fixes checked by` cells are filled after
   the fact. The exclusion is about what the file is, never about when it
   was last written.
5. **A deeper exemption file is owned, not refused.** #304 asked whether an
   ownerless declaration should be refused or reported. Reading the owner off
   the `seal/specs/<id>` prefix at any depth gives the file its owner and the
   ownership test then applies — refused and printed as `not yours` when the
   range touches nothing of that work item, applied when it does. A file
   outside any work item directory keeps the hand-run reach the module
   documents. No new printed state is needed.
6. **#366 is not this item's subject** (see *Out*); the default home is A.
7. **#371 needs nothing in the tree.** It is closed as completed with no
   change behind it; #507 carries the same defect and is what this work
   closes. The pull request body says so.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is five
rows: one for a person that does not block (Q1, #366's home), three
measurements and one for the work (Q2–Q4), and one for a person that does
not block and records what phase 2 gives up (Q5).

Framed 2026-09-23 by framer, before the build.
