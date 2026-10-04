# Feature Specification: a work item's directory is sorted by how long each part matters (#729)

<!-- seal/specs/1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters/spec.md
     Issue #729, F3 of `docs/the-record-layout.md`, cut out of #715 by its
     frame (D8). Record language: English (`seal/config.md` has no `Record
     language` row). Every coordinate below was opened by the framer at
     e141980a (this branch's base) unless it says otherwise, and every number
     was measured there by the framer on 2026-10-04. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-record-layout.md` §*What is decided and not built yet*, F3 | The principle: what outlives the merge stays, or folds into `docs/` and the ledger; what a review run needs only while it runs leaves the tree, or becomes one file per run. This frame decides which, after reading the readers |
| `docs/the-record-layout.md` §*seal/specs/<work-item-id>/* | The file table this work sorts by lifetime. It ends *How these files are laid out by lifetime is decided in principle and not built (F3)*, which this work replaces |
| `docs/the-record-layout.md` §*The size a reader takes whole* | A file a reader takes whole stays at or under 1,000 lines and 64 KB. It is the measure that rejects *one file per run* (D2) |
| `docs/review-handoff-protocol.md` §*Why the directory is not deleted* and the paragraph above *Files* (*Outliving the merge is not outliving the release*) | A record must outlive the merge, so nothing here removes one before it. What happens after the release "is the implementation's business, and this one's answer is `skills/settle/SKILL.md`". So the protocol permits an earlier removal after the release without a protocol change; its explanatory sentences that name only the fold still have to follow (D6) |
| `docs/one-root-by-lifetime.md` §*Where the line between the SDD set and the process record runs* and §*Retention: measured, and answered by `settle`* | The two classes already have names: the **SDD set** (spec, plan, questions, overview, changelog) and the **process record** (routing, rounds, todos, pr.ko), "read by nothing after the merge". Separating them inside a work item was "out of scope by the owner's decision" for 0.4.0, "a larger change than this one". F3 is that larger change, ratified in principle by #715 |
| `skills/settle/SKILL.md` §*When it runs*, §*A fold is not a work item*, §*4. Retire what the policy absorbed* | `settle` is the one command that removes a work item's records. It refuses local mode. Its mechanical arm (`--retire`) runs only after a person's fold or under the no-`spec.md` rule. A fold branch is not a work item and commits under `[no-review]` |
| `docs/release-checklist.md` §*2b. Settle what the release leaves behind* | `settle` runs by hand, on its own branch and pull request, and "the honest answer on a busy release is to skip this step". This is why the process record waits: it waits on a judgment it does not need (D3) |
| `skills/code-review/scripts/survivor_check.py#records_a_past_state` | The survivor sweep already names the class this work removes: everything under `rounds/`, everything under `phases/`, and `survivors.md` directly under the work item. It is excluded from both sides of every range, so a range that deletes those files reports nothing from them |
| `skills/code-review/scripts/chain_check.py#changed_routing` and `#main` | A work item is judged at a pull request only when that pull request adds or edits its `routing.md`, or the item is the branch's own. Removing an item's `rounds/` while its `routing.md` stays unchanged does not put it under judgment. Removing `routing.md` from a directory that still holds `spec.md` is refused unless the item is folded or retired by the rule (D4) |
| `.github/scripts/release_seal.py#chain_counts` | The release seal reads the rounds of every work item the release's pull requests carry, through `routing.item_dir` and `routing.rounds`, when the release is published. A release's own records must be in the tree at its tag (D3) |
| `seal/config.md` `Ledger frozen from` and `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | The precedent for leaving released records unchanged. Its grounds are citations by content anchor and parallel re-stamps. Neither applies to a round record, so the precedent does not carry over (D5) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The readers of the removed paths, the sentences that say how long records stay, and the tests that read the real corpus are each a class, enumerated below by construction. The new command's output is text a person acts on, so it is documented and pinned in the same commit, and every new case is seen red first |

## The readers, enumerated

How this was built: `grep` over `hooks/*.py`, `.github/scripts/*.py`, `.github/workflows/*.yml` and `skills/*/scripts/*.py` for every path segment of the files in question (`rounds`, `round-`, `phases`, `phase-`, `survivors.md`, `-report.md`, `tests-todo`, `evidence-todo`, `broad-gate.md`, `handoff.md`, `pr.`), then opening each hit to see which work item it reads. Comments and docstrings were dropped by reading, not by pattern.

| Reader | What it opens | Which work items | After the release that ships an item |
|---|---|---|---|
| `skills/code-review/scripts/round_record.py` (`new`, `close`, `seal`) | `<item>/rounds/round-N.md`, `round-N-report.md` | the one it is run on, during its run | nothing |
| `skills/code-review/scripts/chain_check.py#main` | `rounds/round-*.md` git carries, `broad-gate.md` | only items whose `routing.md` the pull request adds or edits, plus the branch's own | nothing: a released item's `routing.md` is no longer in any later diff. The release pull request into `main` does carry every item of that release, so the records must stand until the release merges |
| `.github/scripts/release_seal.py#chain_counts` | `rounds/round-*.md` | every work item the release's pull requests carry | read once, when the release is published |
| `skills/code-review/scripts/survivor_check.py` with `.github/workflows/hygiene.yml` (step *wording this branch removed is not still standing elsewhere*) | every `seal/specs/*/survivors.md` in the tree, as `--exempt` | every item still in the tree | read on every later pull request into a release branch. Its range rows bind only to their own work item's range; its quote rows are unscoped. The module's own docstrings say a `survivors.md` "lives until the release that ships it" (lines 271, 1904), which the tree contradicts: 35 shipped ones stand today |
| `skills/verify/scripts/broad_gate.py#round_count`, `skills/verify/scripts/seal_stamp.py` | `<item>/rounds/` | the item being sealed | nothing |
| `hooks/review-history-guard.py`, `hooks/routing.py` (`rounds`, `stray_rounds`) | `<item>/rounds/` | the item the checked-out branch declares | nothing |
| `hooks/root-migrate.py` (`MARKS`) | `specs/<name>/routing.md` or `specs/<name>/rounds/` | pre-`seal/` directories being migrated | nothing; `routing.md` alone still marks an item |
| `skills/verify/scripts/unverified_check.py` | `overview.md` `## Not verified`, `evidence-todo.md` | every item, against the base | reads `overview.md`, which stays; an `evidence-todo.md` with an open row is never removed (D4) |
| `skills/settle/scripts/settle.py` | `evidence-todo.md`, ledger anchors into the directory, citations into it | released items | the command this work extends |
| `skills/evidence-check/scripts/evidence_check.py` | ledger anchors | anchored paths | **no ledger row anchors inside any work item's directory**: 0 anchors in `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` (measured) |
| `.github/scripts/gather_changelog.py` | `changelog.md` | items the release gathers | `changelog.md` is not in the class this work removes (D4) |
| Agents and people: `agents/framer.md` §*What you read* ("Their round records included") | released items' round records | every item still in the tree | the one reader after the merge, and it reads by convenience: the decisions that outlive a run are in `spec.md`, `plan.md`, `overview.md` and `docs/`, and the records stay in git history at the release tag |

Tests that read the real corpus rather than a scratch repository: `tests/conftest.py#committed_round_records_on_disk` and its users (`test_a_finding_id_is_a_bare_integer.py`, `test_chain_check_at_the_pull_request.py`, `test_the_reopening_is_one.py`), `test_chain_hooks_hardening.py` (directory names and overviews), `test_handoff_outlives_the_merge.py` (no flat records), `test_release_hygiene.py` and `test_the_pull_request_language_is_the_repositorys.py` (`pr.*.md`), `test_a_record_precedes_the_fixes_it_commissions.py` (one named item's copies). Each already reads "absent after a complete fold (#517)" as valid at any size. Whether any of them pins a removed file of a named released item is the build's to settle by running them after a drop in a scratch copy (Q4).

## Measured at e141980a

- 56 directories under `seal/specs/`: 55 released (each directory is in a tag, v0.18.0 the latest) and this one. 841 files, 8,960,856 bytes. Files per directory: median 16, max 22, min 2.
- By kind: `rounds/` 286 files in 53 directories, 4,870,896 bytes (145 `round-N.md`, median 11.6 KB, max 31.7 KB; 141 `round-N-report.md`, median 21.8 KB, max 48.5 KB). `phases/` 200 files in 51, 981,125 bytes (median 4.6 KB). `survivors.md` 35, 108,707 bytes, holding 323 quote rows and 2 range rows. `handoff.md` 2, `pr.ko.md` 1, `broad-gate.md` 1. No `tests-todo.md` or `evidence-todo.md` stands in the tree. The SDD set and routing: `routing.md` 56, `overview.md` 54, `changelog.md` 53, `spec.md` 52, `plan.md` 51, `questions.md` 50.
- The process record (`rounds/`, `phases/`, `survivors.md`, `handoff.md`, `pr.*.md`, `broad-gate.md`) is 525 of 841 files (62%) and 5,978,646 of 8,960,856 bytes (67%). Removed from the 55 released directories, a directory holds at most six files.
- One file per run: the whole `rounds/` of one work item has a median of 94,523 bytes and a max of 185,719. 41 of 53 would be over the 64 KB a reader takes whole.
- The last retirement is `c52e8350` (2026-09-24, #582), which left `seal/specs/` empty. No directory has been retired since (`git log --diff-filter=D -- 'seal/specs/*/routing.md'`), so all 55 released directories standing now accumulated after it, across the seven releases 0.15.4 to 0.18.0.

## Decisions

**D1. The paths inside a work item's directory do not change.** `rounds/round-N.md`, `rounds/round-N-report.md`, `phases/phase-N.md` and the top-level files keep their names and depths. Ten readers and 57 test files name these paths (measured by `grep -l` over `tests/*.py`), and the earlier move of the records one level down (`docs/review-handoff-protocol.md` §*Why the records moved a second time*) already sorted the growing half into subdirectories. A regrouping (for example a `run/` directory holding `rounds/`, `phases/` and `survivors.md`) would buy a reader nothing a listing does not already show, and it would cost a no-fallback migration across every reader. What changes is **when** the process record leaves, not where it sits.

**D2. *One file per run* is rejected.** It is the second half of D8's either-or. A run's round records are already split one file per round on purpose, `Fixes checked by` names a `round-N`, and 41 of 53 runs would exceed the 64 KB a reader takes whole. Phases total far less (max 61 KB per item) but carry nothing a reader needs after the release, so there is nothing to keep in one file.

**D3. The process record leaves the tree after the release that ships its work item, by a mechanical arm of `settle` that does not wait for the fold.** The command is `settle --retire-process`. It runs in `docs/release-checklist.md` §*2b*, as that step's first act, and it runs even on a release that skips the fold, because it writes no prose and judges nothing. Grounds: no reader needs the process record after its release (the readers table); the fold is a judgment that has lagged seven releases while the process record waited on it; and the removal is mechanical, so it does not inherit the fold's reason for being skipped. The earliest safe point is after the release is merged to `main` and published, because `chain_check` judges every item of a release at its pull request into `main` and `release_seal.py` reads their rounds at publish. `settle`'s own *released* test (the directory is present at `--released-at`, default `origin/main`) is exactly that point, so no new predicate is introduced: at release N's step 2b, the items of releases up to N−1 are the ones taken.

**D4. What leaves, by construction, and what stays.**

- **Leaves:** `rounds/` (whole), `phases/` (whole), `survivors.md`, `broad-gate.md`, `handoff.md`, `pr.*.md`, `tests-todo.md` and `evidence-todo.md`. The first three are `survivor_check.py#records_a_past_state`, the survivor sweep's own definition of a record of a past state. The rest are written for a pull request that has merged.
- **Stays until the fold:** `routing.md`, `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`.
  - `routing.md` stays because it is the item's identity to the readers: `chain_check#main` refuses a removed `routing.md` whose directory still holds `spec.md` unless the item is folded or retired by the rule, `release_seal.py` maps a pull request to its item through it, and `hooks/root-migrate.py` marks an item by it. Removing it early would need a third retirement predicate in `chain_check`, and one file per directory does not pay for that.
  - `overview.md` stays because `unverified_check.py --baseline` counts its `## Not verified` rows, and a removed row is refused.
  - `changelog.md` stays because #728 (F2) owns the changelog's homes in this release and is framing in parallel; whether a gathered fragment leaves is its decision.
- **The list is an allow-list of what leaves, and anything else stays and is named.** Removal is the destructive direction, so a file nobody anticipated (one released directory once held an `ab-comparison.md`) is kept and printed, never taken. This is the direction `chain_check.py#REGULAR` takes for the same reason.
- **Guards, the ones `--retire` already has, applied per item:** an item whose `evidence-todo.md` or `tests-todo.md` holds an open row (by `unverified_check.py#todo_open_rows`) is kept whole and named, with its count. An item that a ledger row anchors into, inside a file this arm would remove, is kept and the row named (`settle.py#anchored_rows`); measured, no such row exists today. Paths outside `seal/specs/` that cite into a removed file are **listed and never refused**, as `--retire` lists them. Four `docs/` lines cite a specific round or phase record (`docs/worktree-guard-spec.md` near line 656, `docs/the-commit-gate-inside-git.md` near 28, `docs/round-record-spec.md` near 507, `docs/review-chain-spec.md` near 635). Two of them already name directories a fold retired (1788735085, 1788184145), so a citation that resolves only in history is a state the tree already accepts; the other two name 1790815613, which the first run would take.
- **Local mode is refused**, as all of `settle` already is: nothing under a local root is committed, so nothing removed from it can be recovered.

**D5. Released work items are not exempt. The first run takes all 55, and this work item does not perform it.** The ledger freeze is not a precedent here. Released ledger files are frozen because rows are cited by content anchor and because two branches re-stamping one released row conflict. A round record has neither: no anchor names one (measured 0), and nothing edits a released one. `settle --retire` already removes these same files, from every released item, without a cutoff. So the arm reads every released item. The first run happens at 0.18.1's step 2b (or later) as its own `[no-review]` pull request, the way a fold does, and not inside this work item's diff. Grounds: a 525-file deletion inside a reviewed pull request costs the review chain a reading it does not need, and it entangles the command's review with its first use. The person running step 2b sees the dry run before anything is removed.

**D6. Every sentence that says how long a work item's records stay is brought into line, and `docs/the-record-layout.md` marks F3 built.** The carriers, found by `grep` for the phrases that state a lifetime (`records themselves stay`, `closed at merge and kept`, `round records included`, `lives until the release`, `is not deleted`, `dropped with the directory`, `waits until a later settle`):

- `docs/the-record-layout.md`: the line *How these files are laid out by lifetime is decided in principle and not built (F3)* becomes a short statement of the two lifetimes, and the F3 paragraph says it is built by #729. The `seal/specs/<work-item-id>/` table's rows are not edited, so #728's edit to the `changelog.md` row does not conflict.
- `docs/release-checklist.md` §*2b*: `settle --retire-process` is its first act, and it is the part that is not skipped.
- `docs/review-handoff-protocol.md`: the paragraph *Outliving the merge is not outliving the release* (around line 66) and §*Why the directory is not deleted*, which name only the fold as the second deadline.
- `docs/one-root-by-lifetime.md` and its `.ko.md` edition: one appended `## Decided when …` section, in that document's own convention for later decisions, pointing at `docs/the-record-layout.md`. The body is a dated design record and is not rewritten.
- `skills/settle/SKILL.md`: the new arm, its own section, its output and its guards; the opening count and the usage block.
- `skills/implement/SKILL.md`: the tree's `round-N.md … closed at merge and kept` line and §6's *The records themselves stay*.
- `agents/framer.md` §*What you read*: the earlier work items' round records are read where they still stand, and in git history at the release tag where they do not.
- `skills/code-review/scripts/survivor_check.py` docstrings at lines 271 and 1904 (*a `survivors.md` lives until the release that ships it*): become true with this arm, and are adjusted to name it.
- `seal/README.md`, where it describes what `settle` removes.

Where a carrier is a test-pinned sentence, the pin follows the sentence. `docs/review-chain-spec.md` stands at 992 lines against the 1,000-line ceiling and is not a carrier; nothing is added to it.

## Scope

**In.** `settle --retire-process` and its report section in `settle`'s dry run (D3, D4); the cases that show the readers accept a drop (S5–S7); the carriers of D6; this work item's changelog fragment and ledger fragment.

**Out, and why:**

| Left out | Why |
|---|---|
| Moving or renaming any path inside a work item (D1) | Measured: the cost is a migration across ten readers and the test suite; the gain is nothing a listing does not already show |
| One file per run (D2) | 41 of 53 runs would be over the size a reader takes whole |
| Running the drop on the 55 released directories (D5) | Its own `[no-review]` pull request at step 2b, after this command is reviewed |
| Removing `routing.md` early (D4) | Needs a third retirement predicate in `chain_check`; one file per directory |
| What happens to a gathered `changelog.md` | #728 (F2) owns the changelog's homes and is framing in parallel |
| Folding the 52 released `spec.md` files into `docs/` | That is `settle`'s judgment act, unchanged here |
| Rewriting the four `docs/` lines that cite a specific round or phase record | Two already cite retired directories; the arm lists every such citation, as `--retire` already does for a whole directory, and the person running the first drop decides |
| Making `settle` run automatically, from a hook or a release script | `skills/settle/SKILL.md` §*When it runs*: it is invoked, never triggered, and the release-preparation commit is gather, fold and bump only |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | **Given** a scratch repository whose `origin/main` holds item A with `rounds/`, `phases/`, `survivors.md`, `pr.ko.md` and the SDD set, **when** `settle --retire-process` runs, **then** exactly the D4 leave-list is removed from A, the SDD set and `routing.md` stand, each removed path is printed, and it exits 0 | a case in a scratch repository |
| S2 | **Given** item B present on the branch but not at `--released-at`, **when** the arm runs, **then** nothing of B is touched and B is not named as a candidate | case |
| S3 | **Given** item C whose `evidence-todo.md` (or `tests-todo.md`) holds one open row, **when** the arm runs, **then** C is kept whole, printed under a *kept* heading with its open-row count, and the run exits 1; a todo file whose rows are all closed is removed | case |
| S4 | **Given** a released item holding a file outside both lists (for example `notes.md`), **when** the arm runs, **then** that file stays and is printed as *not a process record*, and the run's exit status is not changed by it | case |
| S5 | **Given** the tree after S1, committed on a branch cut from the base, **when** `chain_check.py` runs against that base, **then** item A is not judged and the run passes | case, seen red by a variant that also removes A's `routing.md` (which must fail) |
| S6 | **Given** the same range, **when** `survivor_check.py --range base...HEAD` runs, **then** nothing from the removed `rounds/`, `phases/` or `survivors.md` is reported as a survivor | case |
| S7 | **Given** the same range, **when** `unverified_check.py --baseline <base>` runs, **then** it passes, because no `overview.md` row was removed | case |
| S8 | **Given** a local-mode root, **when** `settle --retire-process` runs, **then** it refuses as `settle` already does, and removes nothing | case (the existing refusal, named for the new flag) |
| S9 | **Given** a ledger row anchored inside a released item's `rounds/` file, **when** the arm runs, **then** that item is kept and the row is named with its file and line | case |
| S10 | **Given** `settle` with no flag, **when** it runs over a tree with released items holding a process record, **then** the report has a section naming how many items and files `--retire-process` would remove | case pinning the heading |
| S11 | **Given** the shipped documents, **when** a reader looks for how long each file of a work item stays, **then** `docs/the-record-layout.md` answers it, F3 reads built, and no carrier in D6 still says the process record waits for the fold | `grep` for D6's phrases, and the pins that follow them |

## Data & interfaces

- `skills/settle/scripts/settle.py`: a new flag, `--retire-process`, exclusive with `--retire`. It reuses `released`, `open_items`/`unverified_check.todo_open_rows`, `anchored_rows` and `citations`; it does not re-derive any of them. Every file it opens names `encoding="utf-8"` (#741 adds a check over all file I/O).
- Output lines a person acts on: `removed <path>`, a *kept* heading per guard, a *not a process record* heading, and a closing count line in the shape `--retire`'s closing line already has. These strings are pinned (§14).
- Exit status: 0 when nothing was held, including the case with nothing left to remove (that is the done state after a previous run, unlike `--retire`'s nothing-folded case, which is work still to do); 1 when an item was kept by a guard; 2 for the refusals `settle` already has (local mode, an unresolvable `--released-at`, a missing interpreter floor).
- No ledger coordinate changes form; no template changes.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-04 by framer, before the build.
