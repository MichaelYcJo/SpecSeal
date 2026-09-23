# Feature Specification: settle leaves twelve directories with no way out

<!-- seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

#517, carrying #511 as its second repair step. After two folds `settle`
reports nothing left to fold and `seal/specs/` still holds twelve released
directories, because three kinds of work item have no way out. This work
gives each kind one, and makes the state a complete fold reaches — no
`seal/specs/` at all — a green state for the suite and for every CI reader.

**This branch ships the mechanism and retires nothing.** #517's own
*Sequencing* section fixes the order: ship it in a release, then run `settle`
on the released tree and confirm it reaches an empty `seal/specs/`. The
acceptance below is therefore split: what this branch proves on fixtures and
on a scratch clone of the real tree, and what the post-release fold measures.

## What the owner already decided, and what this frame follows

#517's first comment, *Design direction — decided by the owner, 2026-09-23*,
settles three of the four repair steps, and **it is followed here over the
issue body where the two differ**:

| # | The owner's decision | What the issue body said before it |
|---|---|---|
| D1 | **A fold is not a work item.** It opens no `routing.md`, `spec.md`, `plan.md` or rounds; the judgment is reviewed at the pull request; so no fold leaves a directory behind. Choosing *how* it runs outside the chain is part of this issue | repair step 3 offered two answers and asked the documents to say which |
| D2 | **No log of folds**, under `seal/` or anywhere else. What a fold leaves already has a home: the marker, the pull request, git history | — |
| D3 | **A released work item with no `spec.md` is retired by a rule, not by a record.** `--retire` removes it with no marker, and `settle` prints these under their own heading | repair step 1 asked for *an explicit, recorded acknowledgement* and called its shape the design question |

**Read, and a divergence from the spawn prompt:** the prompt summarised
repair step 1 as a recorded acknowledgement whose shape is open. D3 closes
that. Nothing here writes an acknowledgement, and *traceable to a recorded
acknowledgement* in #517's acceptance is read as *traceable to the rule*: a
removed directory either carries a live marker in `docs/`, or held no
`spec.md` at the commit the pull request forked from, and CI checks both
(A6–A8). D3 says *the acceptance above is unchanged*, which is the grounds
for reading the one clause that way rather than as a record to write.

The owner's second comment, *should a fold travel as a release at all?*, is
marked **to be examined, not decided**. It is `questions.md` Q1, and nothing
here depends on its answer (O1).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | every arm below is a refusal the command or a checker makes on its own; nothing new stops to ask a person (the prompt budget is zero, `plan.md` §*Operational impact*) |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* | the four standing rules this work rewrites two of: *a released work item that wrote no `spec.md` … is kept by name* is overturned by D3; *a retirement breaks every ledger row anchored inside the directory it removes, and nothing refuses the removal first* is overturned by #511's guard. *A population floor … is replaced, never lowered* and *a fold marker on a line of its own is exempt from the wrap limit* stand and bind this work |
| `skills/settle/SKILL.md` §1, §3, §4, §*What a fold branch owes* | the procedure this work extends; §3's three answers (retire, re-point, decline) are the only answers a floor gets; §*What a fold branch owes* carries the two sentences this work replaces — the `survivors.md` range-row and *Nothing in `seal/ledger.md` moves* |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* and §*Appended is the word, and a removal is not one* | what the guard tells a person per row (G3), and why a fold may take a row out of `seal/ledger.md` while never adding one |
| `docs/review-chain-spec.md` §*The declaration, and where the check went instead* | the chain checker's `retired:` arm, which D3 widens by one condition |
| `docs/release-checklist.md` §2b | where a fold runs today: a separate branch and pull request, by hand |
| `docs/one-root-by-lifetime.md` §*Decided when `settle` was built (2026-09-22)* and its Korean edition | a record of a moment; its row *the fold of the accumulated work items is its own work item* is overturned by D1, so both editions take a new dated section rather than an edit (`tests/test_settle_reads_before_it_removes.py#test_the_design_record_takes_the_later_decision_as_a_dated_section`, `#test_both_editions_took_the_same_decisions`) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | three CI readers change their verdict; each change arrives with a case seen red, a stated failure direction and a prompt budget (G6) |
| `CONTRIBUTING.md` §*House rules* — both READMEs move together | `README.md` and `README.ko.md` both describe what `settle` prints, in one table row each |
| `tests/test_first_setup_asks_once.py` | `seal/README.md` and `templates/seal-README.md` are held byte for byte, so both change together |
| `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `.claude-plugin/plugin.json` reads `0.13.2`; nothing this branch writes into a loaded file names that version or a later one |
| `tests/test_docs_line_wrap.py#COVERED` | every line written into a covered `docs/` file wraps at 88; a marker alone on its line is exempt |
| `skills/agent-contract/SKILL.md` §14, §15 | each changed sentence a person reads is pinned in the commit that changes it, and each new case is seen red before it is committed |

### G1 · the twelve, and the three that joined them — read on this branch at `10e37b0`

`seal/specs/` holds **14** directories. `origin/main` carries 12 of them;
`1790134781-…` (#515's repair) is on `origin/release/v0.14.0` only, and this
one is on this branch only. Checked per directory with `test -f spec.md`:

| Directory | `spec.md` | Released at `origin/main` | Holds it today | Its way out after this work |
|---|---|---|---|---|
| `1788177600` | no | yes | nothing to fold, so never named by `--retire` | the rule arm (D3) — **but its `overview.md` has two open `## Not verified` rows**, so it is kept until they close (G2) |
| `1788217118`, `1788220055`, `1788425222`, `1788824000`, `1788938400`, `1789024700`, `1789053786` | no | yes | the same | the rule arm; no `overview.md`, nothing open |
| `1788276387` | no | yes | the same | the rule arm; its one `## Not verified` row is closed (✅) |
| `1788395377` | no | yes | the same | the rule arm — **two open rows**, kept until they close |
| `1788184145` | **yes** | yes | the `seal/ledger.md` row anchored at its `rounds/round-3.md` | the row is REMOVED here (G4); its spec is folded by the next fold like any other |
| `1790119502` | **yes** | yes | it is the fold's own work item (#514) | folded by the next fold like any other; under D1 no later fold makes another |
| `1790134781` | no | not yet | unreleased | the rule arm once released — **three open rows** |
| `1790138190` (this one) | yes | not yet | unreleased | folded by the next fold like any other |

So after the release the next fold has three judgments to make (fold the
specs of `1788184145`, `1790119502` and this one), seven open rows to close
or re-home, and nothing else. That is the fold's work, not this branch's
(O3).

### G2 · the rule arm keeps a directory whose memo still has an open row

D3 says a released work item with no `spec.md` states no rule. **It is true
of the spec and false of the memo**: `1788177600`, `1788395377` and
`1790134781` each carry open `## Not verified` rows, and those rows are
claims with an answerer, not rules. #514's frame measured what happens to
such a row when its directory goes (`seal/specs/1790119502-…/spec.md` G4, row
L2): the only record that a production workflow was red sat in a retiring
`overview.md`. And `unverified_check.py --baseline` fails a pull request
whose `overview.md` rows *left the record without being closed* — so a rule
arm that removed these directories would be refused in CI unless the reader
were taught to drop open rows, which is the defect L2 measured.

**So the rule is: no `spec.md`, and no open `## Not verified` row, and no
open `evidence-todo.md` row.** A directory failing only the second condition
is kept and named with its rows; closing a row (✅ with what closed it) or
re-homing it (`seal/follow-up.md`, an issue) is what lets the next
`--retire` take it. The owner's own table (D1) already asks `settle` to list
these rows before `--retire`. This is one condition narrower than D3's
sentence, and it is recorded as a judgment in `questions.md`'s settled list
so it can be overturned.

The same predicate is the one the CI readers ask of the **merge-base**
(G5), which is what makes a branch that deletes a `spec.md` in one commit
and the directory in the next read as a deletion rather than a retirement.

### G3 · #511's guard names every row, and keeps every directory a row anchors into

Read: `skills/settle/scripts/settle.py#coordinates` attributes rows to work
items by their `<!-- specs/<id> -->` section and **skips every row above the
first marker**. Row 78 of `seal/ledger.md` — the one row anchored under
`seal/specs/` today — sits in *Who checked the last round's fixes*, above
every marker, so the existing reader would never see it. The guard reads
every live line of `seal/ledger.md` and of every `seal/ledger/*.md` with the
one liveness rule (`unverified_check.py#live_lines`) and the one coordinate
shape (`settle.py#COORDINATE_RE`), and asks only whether each anchor's path
lies under a directory in the set.

- **`settle`** names every such row whose anchor lies under any **released**
  work item's directory — the population a fold might retire — so the
  session sees them while it writes the prose, not after.
- **`settle --retire`** keeps every candidate directory a row anchors into,
  removes the rest, and exits 1, naming each row by its file, its line and
  its first cell. The existing evidence-todo guard already keeps per
  directory and exits 1; this is the same shape, and it is what
  `docs/the-evidence-ledger.md` already says a hit found before the removal
  gets: *the directory stays*.
- **Per row it says what `CLAUDE.md` requires**: REMOVED, when every anchor
  the row cites lies in the set; narrowed — the dead anchor dropped — when
  the row keeps a live one, with the sentence that the multi-anchor answer
  is the repository owner's (`seal/ledger.md` §1788354065's S12 row;
  `questions.md` Q2).

Nothing is re-pointed, and nothing is removed from the ledger by the
command: which row goes is a judgment about a claim, and the command reads.

### G4 · the one row the guard finds today is answered here

`seal/ledger.md` row *The last round's fixes are read by nobody, and the box
saying the review passed is ticked by the session that wrote them* has one
anchor, `seal/specs/1788184145-…/rounds/round-3.md`, and its Notes already
say `settle` *has to re-anchor or drop this row when it does*. Its claim is
**already prose**: `docs/review-chain-spec.md` §*Two records, and what each
of them says* carries the #33 measurement and names the same record. So:

- the row is **REMOVED** from `seal/ledger.md` — a removal from the shared
  file, which `CLAUDE.md` permits;
- one row in this work item's fragment re-founds the claim on a live anchor:
  the `docs/review-chain-spec.md` unit that states it;
- `docs/the-evidence-ledger.md`'s sentence that `1788184145` is *the one
  directory held this way today* and that the question *is carried by #517's
  design comment* is rewritten to say the row was answered.

The prose citations of that record's path — `docs/review-chain-spec.md`
§*Two records*, `tests/test_the_last_rounds_fixes_are_checked.py#test_the_same_record_only_prints_for_an_item_begun_before_it`,
and a Notes cell in `seal/ledger.md` §*Edits that reach the commit gate* —
stay until the fold that retires the directory, which is what the new
citations listing (S3) exists to hand it. **No row this branch writes may
anchor under `seal/specs/`**, including its own directory, or the next
fold's guard keeps this directory.

### G5 · one reader of what a retirement is, and every checker asks it

Three CI readers tell a retirement from a deletion today, and all three would
refuse the rule arm:

| Reader | What it does with a removed directory today | Read at |
|---|---|---|
| `unverified_check.py --baseline` | a removed `overview.md` is `folded` only when `folded_items` holds its id; otherwise *present at … and not here* — exit 1 | `unverified_check.py#main`, the `if args.baseline:` block after the scan |
| `chain_check.py --baseline` | a removed `routing.md` is `retired:` only when `folded_items` holds its id; otherwise *git does not carry this file at HEAD* — exit 1 | `chain_check.py#main`, the `retired = reader.folded_items(root)` arm |
| `survivor_check.py --range` | a removed file's sentences are *corrected wording*; the fold owed a `survivors.md` range-row to silence them — and under D1 a fold has no directory to hold one | `survivor_check.py#corrected`, `#whole_range` |

`unverified_check.py` is already the fold record's one reader (`settle.py`'s
own module docstring says so). **The rule arm's predicate is written there,
once, beside `folded_items`**, asked of a ref: the directory existed at the
ref, held no `spec.md` there, and its `overview.md` and `evidence-todo.md`
there held no open row. `settle` asks it of the working tree; the three CI
readers ask it of the merge-base they already compute. `survivor_check.py`
drops a retired directory's paths from the range on both sides, the way it
already drops `rounds/` — which also means **a fold owes no `survivors.md`
row any more**, marker arm included, and D1's fold has nothing it needs a
directory for.

### G6 · what each changed verdict does when it is wrong

`CONTRIBUTING.md` §*What a change to a gate must carry*, answered here so the
pull request can quote it:

| Change | Direction | Why that direction is the cheaper mistake |
|---|---|---|
| `settle --retire` keeps a directory a ledger row anchors into | blocks more | a wrong keep costs one re-run after the row is answered; a wrong removal is a BROKEN row CI fails, found after the directory is gone (#511 measured it twice) |
| the rule arm keeps a directory with an open memo row | blocks more | a wrong keep costs closing a row; a wrong removal loses a claim with an answerer, and nothing reads it again (L2) |
| three CI readers accept a removal with no marker when the merge-base held no `spec.md` and no open row | allows more | what they newly allow is exactly what `settle --retire` newly removes, asked of the same predicate at the same commit; a hand deletion of a spec-less directory with nothing open passes, and it loses a routing declaration and records of a moment, which D3 is the owner's statement costs nothing |
| `survivor_check.py` leaves a retired directory out of the range | allows more | a retired directory's sentences standing in `docs/` is the fold working; the removed spec is not a place that still instructs anybody, the same grounds the `rounds/` exclusion rests on |
| an absent `seal/specs/` under a present `seal/` root is a settled state for `settle` and `unverified_check.py` | allows more | refusing it turns every pull request after a complete fold red (G7); a mistyped path elsewhere is still exit 2 |

**Prompt budget: zero.** No arm asks anything; every one refuses or prints
on its own.

### G7 · an empty `seal/specs/` is not one state but two, and both must be green

Git keeps no empty directory. After the last retirement a fresh checkout has
**no `seal/specs/` at all**, while the working tree that ran `--retire` has
an empty one. Read, not run:

- `settle.py#main` returns 2, *has no seal/specs/ — nothing was read*, for
  the absent one.
- `unverified_check.py#main` returns 2 for a path absent at `HEAD` that held
  no overview at the merge-base — *a typo* — which is every pull request
  after a complete fold, the shipped `templates/hygiene.yml` included.
- `os.listdir` over `seal/specs/` raises for the absent one in
  `tests/test_chain_hooks_hardening.py` (two cases),
  `tests/test_handoff_outlives_the_merge.py`, `tests/test_release_hygiene.py`
  and `tests/test_a_finding_id_is_a_bare_integer.py`.

### G8 · the population floors, re-read from the readers

`grep -rln "seal/specs" tests/` names 45 modules; the ones below read the
real corpus and go red or raise once it is empty or absent. **Correction
carried from #514's frame:** its F1–F3 were declined as *green at any size*;
`tests/test_chain_check_at_the_pull_request.py#_the_walk_found_every_committed_record`
asserts `listed` is non-empty, so it is red at zero.

| # | Coordinate | What it asserts | Empty / absent |
|---|---|---|---|
| F1–F3 | `tests/test_chain_check_at_the_pull_request.py#_the_walk_found_every_committed_record`, its two walking sweeps, and `#test_this_repositorys_own_round_records_pass_the_per_record_checks` (`assert records`) | a record was listed | red |
| F4 | `tests/test_a_finding_id_is_a_bare_integer.py#_the_corpus_covers_every_work_item_that_has_rounds` | `assert with_rounds`; `os.listdir(specs)` | red / raises |
| F5, F11 | the same module, `assert paths`, `assert parsed` | something parsed | red |
| F6 | the same module, `assert teeth` — carried today by `1788395377`'s four records alone | a record the rule refuses exists | red |
| F12 | `tests/test_the_reopening_is_one.py#test_this_repositorys_own_records_are_not_refused_by_the_reopening_walk` | `assert records` | red |
| F13 | `tests/test_release_hygiene.py#test_this_repository_has_one_root_laid_out_by_lifetime`, `assert items` | a `routing.md` exists; `os.listdir` | red / raises |
| F14 | `tests/test_routing_is_recorded.py#test_every_declaration_in_this_repository_still_parses`, `assert found` | a declaration exists | red |
| F15 | `tests/test_the_pull_request_language_is_the_repositorys.py#test_the_existing_mirrors_are_consistent_with_the_rule` | a `pr.*.md` exists — all four live in directories the next fold retires | red |
| F17 | `tests/test_chain_hooks_hardening.py#test_spec_directories_carry_the_timestamp_prefix`, `#test_every_spec_directory_that_reached_the_ladder_has_an_overview`; `tests/test_handoff_outlives_the_merge.py#test_this_repository_keeps_no_record_at_the_old_location` | no offender | raise when absent |
| F9, F10 | `conftest.cutoff_item_is_traceable` for `REOPEN_FROM`, `FLOOR_FROM` | directory or marker | unaffected: neither cutoff is one of the fourteen, and the helper is `isdir`-guarded |

Named single-item readers (`1788501054`, `1788229400`) already take the
marker when the directory is gone, and name none of the fourteen.
`tests/test_unverified_rows_close.py`'s `>= 90` reads `seal/ledger.md` and
does not move.

## Scope

### In

| # | What |
|---|---|
| S1 | **#511's guard** (G3): `settle` names, and `settle --retire` refuses per directory, every live ledger row anchored inside the set; the per-row answer printed; exit 1 |
| S2 | **G4's answer**: the row REMOVED, one fragment row re-founding the claim, the `docs/the-evidence-ledger.md` sentence rewritten |
| S3 | **the rule arm** (D3, G2) in `settle`: its own heading in the report, `--retire` removes it without a marker, a directory with an open memo row kept and named. The report also lists, for every directory it would retire (either arm), the open `## Not verified` rows, the paths outside `seal/specs/` that cite into it, and the `tests/` files that read `seal/specs` (`skills/settle/SKILL.md` §3's grep) — the three things D1's table says the command should report by itself |
| S4 | **one predicate, four readers** (G5): the predicate beside `folded_items`; `unverified_check.py --baseline`, `chain_check.py --baseline` and `survivor_check.py --range` ask it; `settle` asks it of the tree |
| S5 | **an empty root is green** (G7): `settle` and `settle --retire` exit 0 with a sentence on an empty or absent `seal/specs/` under a present root; `unverified_check.py` does the same for the root's own `specs` path; every floor in G8 re-pointed by `skills/settle/SKILL.md` §3 so it is green with the corpus present, empty and absent, and none lowered |
| S6 | **the fold is not a work item** (D1): the documents say which of D1's two answers holds — see below — in `skills/settle/SKILL.md`, `docs/the-evidence-ledger.md`, `docs/release-checklist.md` §2b, and a dated section in both editions of `docs/one-root-by-lifetime`; §*What a fold branch owes* loses the range-row (G5) and *Nothing in `seal/ledger.md` moves* (Q3) |
| S7 | every document that says what `settle` prints or removes: `README.md` and `README.ko.md` (one row each), `seal/README.md` and `templates/seal-README.md` (one sentence, byte for byte), `docs/review-chain-spec.md` §*The declaration, and where the check went instead* |
| S8 | `overview.md`, `changelog.md`, `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md`, and a `survivors.md` only if this branch's own rewrites leave survivors the sweep reports (Q6) |

### Which of D1's two answers — decided from the tree

D1 asks the fold to run either **outside the chain** (`[no-review]`
commits, reviewed as a pull request) or through **a lightweight route that
reviews without a directory**. **The first.** Grounds:

- The review chain writes its records into a work item's `rounds/`, and
  `chain_check.py` reads them from nowhere else (`#round_records`). A route
  that reviews without a directory needs its records somewhere else, and
  every somewhere else is a log of folds, which D2 refuses.
- Outside the chain is already how the other by-hand release act runs: the
  release-preparation commit belongs to no work item and is waived per
  command (`docs/release-checklist.md` §4). A fold is the same shape one
  pull request later.
- It needs no new mechanism once G5 lands. `chain_check.py` on a pull request
  that declares nothing passes with a notice; the removed declarations read
  `retired:` by either arm; `unverified_check.py` reads the removed memos as
  folded or retired; the survivor sweep leaves the retired paths out.

So: a fold opens no work item, the routing question is not asked for it,
every fold commit carries `: '[no-review]';` in front, and its pull request
is where its prose is judged. The fold rewrites `seal/ledger.md` only by
removing a row the guard named or re-verifying a row its own prose drifted,
and appends nothing — it has no fragment id to append under.

### Out — and why, one line each

| # | Not done | Why |
|---|---|---|
| O1 | the fold's route — a pull request into the open release branch, or straight to `main` | the owner's second comment says *to be examined, not decided*; `questions.md` Q1 carries what reading established. G5 makes the fold pass on either route, so nothing here waits on it |
| O2 | retiring any directory on this branch | #517 §*Sequencing* — ship, then fold; the mechanism is proven on fixtures and on a scratch clone (A9) |
| O3 | folding `1788184145`, `1790119502` or this spec, and closing the seven open memo rows G1 names | the next fold's judgment; S3's listings are what hand it over |
| O4 | rewriting the prose citations of `1788184145-…/rounds/round-3.md` | they resolve until that directory goes, and the fold that removes it is handed them by S3's listing |
| O5 | a `plan.md`-only directory | none exists; D3 names `spec.md`, and the rule is written for what the owner named |
| O6 | a changelog fragment deleted before it was gathered | the marker arm has the same reach today, and `settle`'s released condition keeps the rule arm off it; no reader in the tree guards a deleted `changelog.md` for any branch |
| O7 | #518's lighter commit-gate tier and #519's ledger compression | named in the spawn as out; the couplings are written in `questions.md` |
| O8 | lowering any floor literal | `skills/settle/SKILL.md` §3 |
| O9 | `skills/implement/orchestration.md` | a fold session is running `settle`'s skill, which is where the rule *a fold is not a work item* reaches it |

## User scenarios & acceptance *(mandatory)*

### On this branch

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 a row anchored inside stops the retirement (#511's red direction) | Given a fixture tree with a released, marked work item and a ledger row anchored in its `rounds/` · When `settle --retire` runs · Then it exits 1, the directory is still there, every other candidate is removed, and the row is named with its file and its first cell and the word REMOVED | a `tmp_path` case, seen red against the unfixed `retire` |
| A2 a row above the first marker is seen | Given the anchored row sits above every `<!-- specs/ -->` marker, as row 78 does · Then A1 holds for it | the same case's second fixture |
| A3 a multi-anchor row is narrowed, not removed | Given a row with one anchor inside the set and one outside · Then the line says to drop the dead anchor and names the owner's question | a case pinning the sentence |
| A4 the rule arm | Given a released fixture directory with no `spec.md` and nothing open · When `settle` runs · Then it is listed under its own heading · When `--retire` runs · Then it is removed with no marker written anywhere | cases on the report text and on the tree |
| A5 an open memo row keeps a spec-less directory | Given the same directory with one open `## Not verified` row · Then `settle` names the row and `--retire` keeps it and exits 1 | a case |
| A6 `unverified_check.py --baseline` reads a rule retirement as one | Given a fixture history whose second commit removes a spec-less directory with a closed memo · Then exit 0 and it is named apart from folds; with the memo row open, exit 1 as today; with a `spec.md` at the base, exit 1 as today | cases, the first seen red first |
| A7 `chain_check.py --baseline` prints `retired:` for a rule retirement | the same fixture shape · Then a `retired:` notice naming the rule, and the refusal where the base held a `spec.md` | cases |
| A8 the survivor sweep leaves a retired directory out | Given a range that removes a marked directory and a spec-less one, with their sentences standing in `docs/` · Then `survivor_check.py` exits 0 with no `survivors.md`; a sentence the same range removes from `docs/` is still measured | cases |
| A9 the real tree, on a scratch clone | Given a clone of this branch · When `settle --retire` runs with `--released-at` naming the commit this repository's `origin/main` names, and is committed · Then it removes exactly the eight spec-less directories with nothing open, keeps `1788177600` and `1788395377` naming their rows, and leaves `1788184145`, `1790119502`, `1790134781` and this one · And `unverified_check.py --baseline`, `chain_check.py --baseline` and `survivor_check.py --range` against the clone's parent all exit 0 · And the clone is deleted | the probe's recorded output in the phase record; `agent-contract` §7 |
| A10 an empty root is green | Given a scratch clone with every directory under `seal/specs/` removed and committed · When `settle`, `settle --retire`, `unverified_check.py --baseline <parent> seal/specs/` and every module in G8 run · Then each exits 0 or passes, and the same modules pass on this branch's tree | the probe; the modules, run narrow |
| A11 no floor was lowered | Then `git diff origin/release/v0.14.0 -- tests/` removes no comparison against a literal and makes no literal smaller, and each re-pointed case is seen red with its defect planted | the diff, read; §15 |
| A12 the ledger holds | Then `bin/evidence-check --strict .` exits 0; `seal/ledger.md` differs only by the removed row and by re-read rows whose anchored unit this branch edited, each named in a phase record | the command; the diff |
| A13 the documents say one thing | Then the pinning modules for every edited sentence pass — `tests/test_settle_reads_before_it_removes.py`, `tests/test_first_setup_asks_once.py`, `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py` | the modules |

### After the release that carries this — the post-release fold

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A14 #517's acceptance | Given the released tree, the three specs folded and the seven memo rows closed or re-homed · When `settle` and then `settle --retire` run on a branch that is no work item · Then `seal/specs/` is empty, `bin/evidence-check --strict .` and the suite are green, and the pull request's CI is green with no `survivors.md` and no `routing.md` in it | the fold's pull request; its answerer is the repository owner, who runs it |
| A15 every removal is traceable | Then every removed directory is named by a live marker in `docs/` or read as a rule retirement by the three CI readers at the fold's merge-base | the three readers' output on that pull request |

## Data & interfaces

No schema. The command's surface keeps its three flags and its three exit
codes (0 produced or ran · 1 something refused · 2 unusable), and exit 0
widens to the settled root (G7). The report gains headings; their text is
the builder's and is pinned by the phase that writes it. The one new
function is the rule arm's predicate in `unverified_check.py`, taking a root
and a ref; its name is the builder's.

## Open questions → questions.md

Three rows a person answers, none blocking and each with a default; one a
measurement answers; two the work answers. The couplings to #518 and #519
are written there as well. Everything else the tree answered above.

Framed 2026-09-23 by framer, before the build.
