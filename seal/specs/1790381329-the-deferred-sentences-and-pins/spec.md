# Feature Specification: the deferred sentences and pins (#610, #611, #612, #613, #615, #616)

<!-- seal/specs/1790381329-the-deferred-sentences-and-pins/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CHANGELOG.md` §0.15.x, the #590 entry: *exits 2, the code for an input nothing could be read from* | #610's code: a sibling missing beside a shipped script is exit 2 with one sentence naming the file and its purpose, never a traceback |
| `skills/agent-contract/SKILL.md` §12 | every item is fixed as a class: the finding names an instance, the fix is owed to every instance the same cause produces, and the handover says which were enumerated |
| `skills/agent-contract/SKILL.md` §14, §15 | a changed message, heading, help line or person-read sentence is pinned in the same commit, and each new case is seen red before it is planted |
| `CLAUDE.md` *a change writes fragments, never the shared file* | the changelog entry goes in `seal/specs/1790381329-the-deferred-sentences-and-pins/changelog.md`; new ledger rows in `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`; a row an edit drifts is re-read and re-stamped in the release file it lives in, with a dated note |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped* | a ledger file that conflicts with B's branch is resolved hunk by hunk, then `evidence-check` runs |
| `docs/release-checklist.md` step 0 | the release branch is merged in, never rebased onto, and only when a file actually conflicts |
| `docs/review-chain-spec.md` §the survivor sweep (the sentence #615 corrects) | the policy statement of the silent set is itself in scope; the docstrings follow it, not the reverse |

## Scope

Six items 0.15.4's capped rounds deferred (milestone 47, work item C). Each is
one exit code, one sentence class, or one pin.

### #610 — the two shipped scripts that still die with a traceback on a missing sibling

In: `skills/implement/scripts/seal.py` (loads `hooks/config.py` and
`hooks/optin.py` through `sys.path.insert` + `import`, at module top, so every
invocation reaches it) and `skills/verify/scripts/payload_meter.py#_session_cost`
(loads `session_cost.py` by path, reached only through `--calibrate`). Each
exits 2 with one sentence on stderr naming the missing path and what it is
for, and no traceback. Two rows join `tests/test_a_script_copied_alone_exits_2.py`'s
`CASES`, and that module's docstring and `CASES` comment stop saying *four
shipped scripts* and *by file path* (the `seal.py` shape is not by path).

The class was enumerated by construction for this frame, read 2026-09-26: every
`spec_from_file_location`, `sys.path.insert|append`, `import_module` and
`runpy` under `skills/`, plus every bare `import <sibling>` of a module in the
same `scripts/` directory (none exist). Of the shipped `skills/` loaders,
`survivor_check.py#reader`, `#evidence` and `#hook` and `broad_gate.py#load`
already raise their `Refused` (exit 2) with a sentence; `evidence_check.py`'s
two loaders fall back on purpose to a vendored copy or `<root>/seal`, which is
a design, not a traceback. So the class under `skills/` is exactly the issue's
two rows. `hooks/*.py` are out (the issue's own grounds: 2 blocks a tool call
there). `.github/scripts/*.py` are out: they ship with no plugin copy and
run only in this repository's CI, so *copied alone* never happens to them.

**Exit 2 for both, decided from the tree:**

- `payload_meter.py` already exits 2 for the one other "nothing ran" case it
  has, the interpreter floor (`payload_meter.py`, the module-level
  `_refusal` block). Its 1 is `CalibrationError` and "no agents": *this input
  could not be measured*. A missing `session_cost.py` is a broken plugin copy,
  which is the floor's kind, not the calibration's. #590's frame left the
  meter out on the 1-means-could-not-measure reading; that reading is why 2 is
  the right code, not a reason against it.
- `seal.py`'s docstring says `Exit codes: 0 done · 1 nothing was written ...
  There is no third one`. The fix adds a third, so that sentence is rewritten
  in the same commit (contract §14). No other document states seal's exit
  codes: `README.md`'s `seal mode --check` line says "exits non-zero", which
  stays true.

### #611 — settle's two kept-at-base headings

In: `skills/settle/SKILL.md` §1's sentence naming *kept until the closure
reaches <base>* also names *kept: the closure has not reached <base>*
(`settle.py#RULE_MOVED_HEADING`, chosen by `settle.py#base_heading`). The
round's paste-ready text matches lines 117-119 of the skill at the tree this
frame read, and is adopted as written. `test_the_documents_say_the_closure_has_to_reach_the_base`
gains the second wording beside the first, and
`test_the_report_does_not_promise_what_the_retirement_refuses` gains the
round's summary-line assertion (`BASE` is defined at the module level and
that case already asserts the heading formatted with it).

Neither README edition names a heading, and `docs/the-evidence-ledger.md` does
not either (grep of both wordings, 2026-09-26), so the skill is the only
document with the twin.
### #612 — where CI's unverified-check comparison actually lands

**The fact, read 2026-09-26.** `.github/workflows/hygiene.yml`'s checkout has
no `ref:`, so a `pull_request` job holds the merge ref, and
`git merge-base <base> HEAD` there answers the base's tip. The same file's
milestone-step comment says so, and `unverified_check.py#base_label`'s
docstring says so. On a branch checkout — a local run, the broad gate's run —
the same command answers the fork point. Both are true; the sentences below
say only the second and place it in CI. Their conclusions hold at both, which
is why the fix is prose: a file present at the base's tip and absent at the
merge ref was removed by this branch too, and a sibling squashed onto the base
is in the merge ref already.

**The statement every sentence is rewritten to carry:** what is read is
`git merge-base <ref> HEAD` — the fork point on a branch checkout, and the
base's tip in CI, whose checkout of a pull request is the head already merged
into the base — and either way a row or file that arrived on the base after
the branch was cut is not this branch's removal. Wording is the builder's; the
two places and the either-way conclusion are the contract.

In, enumerated by meaning for this frame (English: *fork point*, *forked
from*, *where this branch forked*, *after the fork*, *moving tip*, *merge
base* near *CI*/*pull request*; Korean: *갈라진 지점*, *갈라진 뒤*, *병합 기준*,
*merge base*), across `docs/`, `skills/`, `templates/`, `agents/`, `hooks/`,
`.github/`, both READMEs and `CONTRIBUTING.md`:

| File | Unit or place | What it says now |
|---|---|---|
| `.github/workflows/hygiene.yml` | the unverified step's comment | *fewer rows than where this branch forked from the base*; the #272 paragraph implies the merge base is what protects the CI run |
| `templates/hygiene.yml` | the unverified step's comment | the same two sentences, shorter |
| `skills/verify/scripts/unverified_check.py` | module docstring, *The base is the merge base* | *present at the fork point ... after the fork* |
| same | `merge_base`'s docstring | *The merge base is the fork point* |
| same | `folded_items`'s docstring (not in the issue's list) | *a directory present at the fork point and absent here* |
| same | `main`, the `--baseline` help | *where this branch forked from REF* twice |
| `skills/verify/SKILL.md` | §*`--baseline` names the branch you merge into* | *what it reads is where you forked from it* |
| `docs/one-root-by-lifetime.md` | the *Would break on removal* bullet | *the fork point, never the base branch's moving tip* — false in CI, not only incomplete |
| `docs/one-root-by-lifetime.ko.md` | the same bullet | *base 브랜치의 현재 끝이 아니라 갈라진 지점* — the same falsehood |
| `README.md` | the `unverified-check` cheat-sheet row | *the point where this branch forked from that ref ... at the fork point* |
| `README.ko.md` | the same row | *이 브랜치가 갈라진 지점 ... 갈라진 지점보다* |

Out, each read and found true: `settle.py`'s fork sentences and
`skills/settle/SKILL.md` (settle runs on a branch checkout, and #605 already
corrected that half); `docs/the-evidence-ledger.md` §retirement (already says
*until the base moves past the fork*); `.github/scripts/release_completeness_check.py`
and the hygiene milestone-step comment (state the merge ref correctly);
`correction_check.py#parse_range`, `survivor_check.py#parse_range`,
`chain_check.py`'s `fork` variable and its restored-record docstring (name a
merge base without placing it); the test docstrings in
`tests/test_unverified_rows_close.py` and
`tests/test_a_release_cannot_ship_an_untrue_milestone.py` (describe local
fixtures, which are branch checkouts). The #272 history sentences (*three of
0.9.2's four branches*) are history and stay; only a clause that places the
comparison in CI changes.

**The pin extends the case that already holds this class.**
`tests/test_unverified_rows_close.py#test_the_documents_state_the_merge_base_footing`
parametrizes eight of the files above and asserts each names the merge base.
It gains a second assertion per file: the base's tip is named, in one English
phrase and one Korean phrase the builder picks and uses in every file of that
language. `skills/verify/scripts/unverified_check.py` joins the parameter list,
because its `--baseline` help is a rendered line. The finding's own false
sentence is asserted absent where it stands today: *never the base branch's
moving tip* in `docs/one-root-by-lifetime.md` and *현재 끝이 아니라* in its
Korean edition. The case's own docstring (*after #272 it compares against the
fork point*) is the same false clause and is corrected with it.

### #613 — `fix_surface`'s docstring twin

In: `chain_check.py#fix_surface`'s docstring, the four lines from
`` `checked_by` prints a notice `` through *nothing refuses that today*,
replaced with the round's paste-ready text, which matches the tree this frame
read. The class was checked by meaning for twins of *refuses it on the LAST
record beside a checked `Pass`* (see plan.md phase 4 for the search the
builder repeats).

**The issue's count is wrong, and the builder uses the tree's.** The issue
says two `seal/releases/0.4.0.md` rows anchor on `fix_surface`. Seven rows do,
all at `@dd0a5d68`: `seal/releases/0.4.0.md` ×3, `seal/releases/0.8.0.md` ×3,
`seal/releases/0.15.0.md` ×1 (grep, 2026-09-26). Each is re-read against the
edit and re-stamped where it lives, with a dated note.
### #615 — the survivor sweep's silent set

In: the three statements, each still reading as the issue describes at the
tree this frame read (line numbers have moved):
`survivor_check.py`'s module docstring (the sentence from *same heading. A row
the id does not name*, around line 198), `removed_ledger_rows`' last docstring
paragraph (*What stays silent is a row corrected in place*), and
`docs/review-chain-spec.md`'s sentence after *every anchor it kept.* (now
line 932, not 926). Each is replaced with the round's paste-ready text, whose
bounds all match. Afterwards the three state one set: silent only when the id
does not name the row AND no live row cites every anchor of it that still
resolves.

The figure travels with the prose. The round counted 280 of 800 anchored
rows (35.0%) with no id `ROW_ID` reads, at its own tip; the tree now says
*about 37%* in all three places and *298 of about 800* in one. The builder
re-counts at the build tip (questions.md Q1) and writes the measured figure
into all three, not the round's.

The round's ⬜ 3 case,
`test_a_claim_split_into_two_rows_as_it_is_corrected_stays_measured`, is
planted in `tests/test_a_corrected_sentence_survives_elsewhere.py`. Its
helpers exist as the round wrote them: `ledger_row` stamps every row `R1 ·`,
so two rows at the tip against one at the left end is exactly what
`removed_ledger_rows`' `named[path][key] >= held[key]` passes and `==`
refuses.

Out: a case pinning S4 (a row whose id lost its sibling and whose every anchor
was renamed) as silent. It is a known false negative the docstring names as
*a design choice beyond this branch*; a case asserting exit 0 would lock the
gap in and turn red on the day someone closes it. The round's ⬜ 4 (28 rows
with id-like heads `ROW_ID` does not read) is documented behaviour and asks
for nothing.

### #616 — the broad gate's `%CD%` precedence and what `as_cmd_expands` claims

In: the round's case, appended to
`test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points` in
`tests/test_the_gate_hands_cmd_a_path_it_can_run.py`: a defined `CD` pointing
at a directory that does not exist leaves `%CD%/bin/test -q` as written. It
uses `%CD%` itself, the finding's own example, and swapping `value`'s two
branches in `as_cmd_expands` turns it red (the computed `CD` is the tree,
which has `bin/`).

The docstring half is a class, enumerated for this frame by meaning (*the way
`cmd /c`*, *as `cmd.exe` expands*, *expanded the same way*, *in no
environment*) across `skills/`, `docs/`, `templates/`, both READMEs:

| Place | What it says now | What it must say |
|---|---|---|
| `broad_gate.py#as_cmd_expands`, first line | `%NAME%` replaced *the way `cmd /c` replaces it* | qualified by the round's added sentence: a substring or substitution (`%NAME:~0,2%`, `%NAME:a=b%`) is not modelled and is left as written |
| same docstring | *`CD` and `__CD__` are in no environment* | false once one is defined, which is the case the new pin sets: a defined one wins, as in `cmd.exe` (`set /?`) — found by this frame, not in the issue |
| `broad_gate.py#handed_to_shell`, docstring and the comment above `command_names_backslashed` | *expanded the way `cmd.exe` expands it*; *expanded the same way* | point at `as_cmd_expands` for what is and is not modelled rather than claiming equality |
| `templates/config.md` §*Broad gate* | *A `%VAR%` in that part is expanded first, as `cmd.exe` expands it before it reads the name* | the same qualification, in the words a person typing a row reads. This sentence is pinned verbatim by `test_the_gate_hands_cmd_a_path_it_can_run.py`'s reader case (the needle list near line 383), so that needle changes in the same commit |

The case's own docstring (*which `cmd.exe` computes and no environment
holds*) is the same false clause and is corrected with it.

Out, recorded as unverified: where `cmd.exe` resumes scanning after an
undefined name. The round read it from memory and only a Windows run can
answer it (questions.md Q2). The docstring says it is not modelled; nothing
here claims it either way.

### Out of scope, and why

- **Every `hooks/*.py` loader** — the hook exit rules give 2 a meaning
  (blocks the tool call), so #590's class does not reach them (#610's own
  grounds).
- **`.github/scripts/*.py` loaders** — they run in this repository's CI only
  and never ship as a lone copy.
- **`evidence_check.py`'s two loaders** — they fall back by design, and the
  file is work item B's.
- **`docs/round-record-spec.md` line 96** (*What it may not do is stand beside
  a checked `Pass` on the run's last record*) and
  **`docs/review-handoff-protocol.md` line 274** — read as #613 twins and
  judged not to be. The first states the norm a record is held to, and line
  63 of the same file states when the check enforces it; the second states
  what the protocol leaves to the project. Neither describes the check's
  timing, which is what #613 corrects.
- **`docs/release-checklist.md` step 0** — listed by
  `test_the_documents_state_the_merge_base_footing`, read for #612, and true at
  both places: a sibling squashed into the release branch is not the other
  branch's removal on a branch checkout or at the merge ref.
- **The #272 history sentences** — past events, not claims about where CI
  compares.
- **Work items A and B** (milestone 47). The milestone says none of C's files
  is edited by them. Checked against both frames as committed on
  2026-09-26 (A: 693f1bf6, B: 6fc5532c), read for the files each names as an
  edit. A edits `hooks/worktree-guard.py`, `hooks/worktree_consent.py`,
  `hooks/routing.py`, `docs/worktree-guard-spec.md`,
  `skills/implement/orchestration.md`, `templates/claude-md-block.md` and
  their tests. B edits `evidence_check.py`, `skills/evidence-check/SKILL.md`
  and its tests; its frame names `broad_gate.py` only as a structural
  reader its notice is held against, and states that `README.md`,
  `README.ko.md`, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md` are
  not edited. No overlap with C's list. One surface can still meet, and the
  builder handles it as the work (questions.md Q3): the `seal/releases/*.md`
  files, where B's phase 3 and C's re-stamps may both touch rows.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · #610, `seal.py` alone | Given `seal.py` copied into a directory with no `hooks/` beside the plugin layout, when it is run with an invocation argparse accepts (`mode --check`; the load is at import, so any valid one reaches it, and argparse's own usage error is also exit 2, which an empty or wrong invocation would pass on), then it exits 2, prints no `Traceback`, and one stderr sentence names the missing path and what the file is for | a `CASES` row in `tests/test_a_script_copied_alone_exits_2.py`; red before the fix (exit 1, `ModuleNotFoundError`) |
| S2 · #610, `payload_meter.py` alone | Given `payload_meter.py` copied alone, when it is run with the smallest invocation that reaches `_session_cost` (`--calibrate <a file>`), then it exits 2 with a sentence naming `session_cost.py`'s path and purpose, and no traceback | a second `CASES` row; red before the fix |
| S3 · #610, the documented codes | Given `seal.py`'s module docstring, then its exit-code line names 2 and no longer says *There is no third one*; `payload_meter.py`'s docstring names the code for a missing sibling | read by the reviewer; the test module's docstring says six scripts and both loader shapes |
| S4 · #611, both headings in the skill | Given `skills/settle/SKILL.md` §1, then it names *kept until the closure reaches <base>* and *kept: the closure has not reached <base>* | `test_the_documents_say_the_closure_has_to_reach_the_base` asserts both; red with the second deleted |
| S5 · #611, the summary line | Given a directory kept at the base, when `settle` reports, then the summary line reads `1 kept because the closure has not reached <base>` | the round's assertion in `test_the_report_does_not_promise_what_the_retirement_refuses`; red with the old wording restored in `settle.py#main` |
| S6 · #612, every document places the comparison in both places | Given each file in the #612 table, then its sentence about `--baseline` says the merge base is the fork point on a branch checkout and the base's tip in CI, and none says CI compares at the fork point | the extended `test_the_documents_state_the_merge_base_footing`; red before the prose edits |
| S7 · #613, the docstring twin | Given `chain_check.py#fix_surface`'s docstring, then the `nobody` refusal on the last record reads *at a ready pull request*; and the seven `@dd0a5d68` rows are re-read and re-stamped | read by the reviewer; `evidence-check` reports none of the seven drifted after the re-stamp |
| S8 · #615, one silent set in three places | Given the module docstring, `removed_ledger_rows`' docstring and `docs/review-chain-spec.md`, then each states silence as both conditions failing, and the no-id figure is the one measured at the build tip | read by the reviewer against `removed_ledger_rows`' code (the `>=` key test and the `standing` citation test) |
| S9 · #615, the count guard's direction | Given a row corrected in place and split into two rows under its id, its anchor renamed, when the sweep runs, then it exits 1 and names `docs/x.md:3` | the round's case; red with `>=` changed to `==` |
| S10 · #616, a defined `CD` wins | Given `CD` set in the environment to a directory that does not exist, when `%CD%/bin/test -q` is handed to `cmd.exe`, then it is handed as written | the round's case; red with `value`'s two branches swapped |
| S11 · #616, the claim matches the model | Given `as_cmd_expands`, `handed_to_shell` and `templates/config.md` §*Broad gate*, then none claims equality with `cmd.exe` beyond the plain `%NAME%` form, and none says `CD` is in no environment | the reader case's needle list in `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` carries the new config sentence; red with the old sentence restored |

## Data & interfaces

- **Exit codes.** `seal` gains 2 (a sibling it loads is missing); it had 0
  and 1. `payload-meter`'s 2 gains a second cause beside the interpreter
  floor. No other command's codes change.
- **Output wording.** No command output changes. `settle`'s summary line is
  only pinned, not reworded.
- **Ledger.** New rows (the two exit-2 behaviours, the `%CD%` precedence, the
  count guard's direction, if the builder records them) go in
  `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`, which does not
  exist yet. Rows a docstring edit drifts stay in their release files and are
  re-stamped there: seven on `chain_check.py#fix_surface`; the rows on
  `survivor_check.py#removed_ledger_rows`, `unverified_check.py#merge_base`,
  `#main` and `#folded_items`, and any others `evidence-check` names after
  each phase.
- **Changelog.** One fragment,
  `seal/specs/1790381329-the-deferred-sentences-and-pins/changelog.md`.

## Open questions → questions.md

None blocks the build and none needs a person. `questions.md` holds two
measurements and two items the work settles, each with the default the build
proceeds on, and lists the judgments the issues left open that the tree
answered.

Framed 2026-09-26 by framer, before the build.
