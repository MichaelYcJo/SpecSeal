# Implementation Plan: a joined project's `specs/` is read and never taken

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-01 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Five slices, each runnable and verified on its own, in the order the ticket's
boxes are met. Phases 1 and 2 close the write side: the hook moves only a
`specs/<id>/` that carries the plugin's marks, and the bootstrap sends a bare
`specs/` to the question. Phase 3 adds the `Reference specs` row with one
resolver and gives it its first reader, the survivor sweep. Phase 4 pins the
remaining checks against a planted team `specs/` and prunes
`unverified-check`'s walk. Phase 5 tells the readers. The changelog fragment
and the ledger fragment ride each phase's closing commit; `evidence-check
--reverify` re-stamps the rows each phase drifts, in that same commit.

## Technical context

Existing code this builds on, read at `cd24f516` on `release/v0.17.0`:

- `hooks/root-migrate.py#ITEM_RE` (line 96), `#old_items` (232–248),
  `#moves` (251–272), `#repoint_path` (387–398), `#main` (460–578; the
  symlinked-`specs/` refusal at 508–524, the printed tail at 568–578).
  `old_items` keeps a name when `ITEM_RE.match(n)` and the path is a
  directory — the name alone. `repoint_path` re-points any `specs/<id>/`
  anchor whose head matches `ITEM_RE`, moved or not.
- `hooks/dispatch.py:88` — `"session-start": ("version-check.py",
  "root-migrate.py", "ledger-migrate.py")`; nothing else names the hook.
- `skills/implement/orchestration.md:72–81` — the paragraph *First, look
  for the 0.3.x layout*, which reads "`.specseal/` or a top-level `specs/`".
  `tests/test_first_setup_asks_once.py#test_an_unmoved_old_layout_is_not_asked_but_told`
  (332–338) pins `0.3.x layout` before `**shared**` and the word `moves it`.
- `README.md:364–397` and `README.ko.md:357–` — §*Coming up from 0.3.x*,
  the by-hand block included; `tests/test_the_root_migrates_itself.py#by_hand_block`
  reads the block out of the section, and `#test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set`
  runs it.
- `tests/test_no_document_names_the_old_roots.py` — `OLD_ROOT =
  r"\.specseal/|(?<![\w/.])specs/<"`: any shipped `.md`/`.yml`/`.sh` line
  spelling `specs/<…>` outside `seal/specs/<…>` needs a `KEEP` entry with a
  reason, and every `KEEP` entry must still occur somewhere. Spelling the
  marks as *a `specs/` entry named `<unix-seconds>-<slug>`* avoids the
  pattern; spelling `specs/<id>/` needs the entry.
- `hooks/config.py#config_rows` (306–359), `#unfenced`, `#config_path`;
  `skills/settle/scripts/fold_check.py:114–161, 451–506` is the precedent
  for a shipped script loading `hooks/config.py` and `hooks/optin.py` by
  path and reading optional rows under `home_at`.
- `skills/code-review/scripts/survivor_check.py#tracked` (436),
  `#records_a_past_state` (849–880), `#WORK_ITEM_DIR` (947),
  `#retired_directories` (973–998), `#corpus` (1175–1188), `#corrected`
  (1194–), `#hook` (1653) and `#OPTIN` (1650) — the by-path loader and the
  resolver it already uses for local mode.
- `skills/verify/scripts/unverified_check.py#SKIP_DIRS` (143),
  `#overviews` (872–887), `#main` (1451–; `path` defaults to `["."]`),
  `#settled_root` (1380–1402).
- `skills/settle/scripts/settle.py#SPECS` (172), `#work_items` (238),
  `#tracked_text` (822), `#citations` (844), `#retire` (972–1130).
- `skills/evidence-check/scripts/correction_check.py#LEDGER/#FRAGMENTS/#RELEASES`
  (236–238), `#ledger_listing` (618). `evidence_check.py#unshipped`
  (2510–), `#tree_names` (3036–), `#scan_candidates` (879–).
  `skills/code-review/scripts/chain_check.py:1255` — `ls-tree HEAD --
  seal/specs/`.
- `templates/config.md` — the row table at 31–36 and one `##` section per
  row; `templates/seal-README.md:51` / `seal/README.md:51`.
- `agents/framer.md:130–163`, `agents/smith.md:32–36`, `agents/warden.md`
  §Role, `skills/settle/SKILL.md:143–224` (§2), `skills/implement/SKILL.md:84–152`.
- `docs/one-root-by-lifetime.md:642–700` and the Korean edition's matching
  sections (`docs/one-root-by-lifetime.ko.md:618–`); `tests/test_both_editions_carry_the_same_folds.py`
  compares heading outlines, so a section added to one edition fails until
  the other has it.
- Ledger rows that drift: `seal/releases/0.4.0.md:238–299` (`root-migrate.py#main`,
  `#moves`, `#old_items`, `#ITEM_RE`, `#repoint_path`, `#repoint`;
  the two README section rows at 265 and 280), `seal/releases/0.5.0.md:29, 57`
  (`#has_root`, `#main`), `seal/releases/0.10.0.md:8–14` and
  `seal/releases/0.12.0.md:30, 32, 109` (the Bootstrap heading),
  `seal/releases/0.15.0.md:71–73` (survivor's `records_a_past_state`),
  `seal/releases/0.9.3.md:90` (`records_a_past_round`).

**Constraints.** Every record and fixture uses neutral names
(`tests/test_no_real_identifiers.py`). `tests/test_docs_line_wrap.py` holds
the agent and skill documents it scans to its width. The contract's §9: edits
through the `Edit` tool, never a heredoc, and no shell line carrying `git
commit` inside a patch. §15: every new case is shown red first and the
hand-back says how. §17: commits name the worktree with `git -C`.

**The failure scenario of the chosen approach — what breaks in six months.**
A check added later walks the tree without asking the resolver, and the class
reopens one script at a time. The mitigation is in phase 4: the planted
fixture case enumerates every shipped check by name, so a new check is either
added to the list or is the one that nobody pinned — which the next reviewer
of a `bin/` addition can see. The second failure is the default: a repository
whose own tests live in a directory named `specs/` (a BDD convention) gets
them out of the survivor pool silently. The row is the way out, and
`templates/config.md` says so in the row's section; the cost is stated
rather than hidden, the way the fold rows' is.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| One resolver in `hooks/config.py`, loaded by path (chosen) | A script that forgets to load it walks the whole tree; mitigated by phase 4's enumerating case | chosen — `fold_check.py` and `broad_gate.py` already read optional rows this way, and `optin.py`'s docstring is the argument against copies |
| A `specs`-name test written into each script | Four copies, four drifts; the shape `optin.py` was written to end | rejected |
| The resolver in `hooks/optin.py` | That module's docstring says no config key lives there and everything in it fails toward *not opted in*; a row reader there reads as the opt-in clause being softened (`hooks/config.py` docstring, *Not in `optin.py`, deliberately*) | rejected |
| Marks = `routing.md` or `rounds/` (chosen) | A 0.3.x item with neither is left behind; measured none at `v0.3.0` (13 of 13 carry `routing.md`). Left behind is also the safe direction, and the README's by-hand block is the way | chosen |
| Marks = any of `spec.md`, `plan.md`, `overview.md`, `questions.md` | A team's specification uses those names; the hook would take it | rejected |
| Proof = `.specseal/` present, items then moved by name | A team directory with an id-shaped name in a 0.3.x repository is still taken | rejected — the proof is per directory |
| The bootstrap asks the person whether `specs/` is theirs | A question a document answers (`CLAUDE.md` §*The goal*); and a subagent cannot ask it | rejected |
| `survivor-check`: reference roots out of the pool only | A team file the range edited still becomes a source, which is #365's shape one class over; `records_a_past_state` is applied on both sides for that reason | rejected — both sides |
| `survivor-check`: report reference-root hits under their own label | Still a hit over a document the plugin never wrote, and a new output shape for every reader of the report | rejected |
| `unverified-check`: refuse a path inside a reference root | A person naming a file has asked for it; refusing is the wrong direction for a CLI someone is watching | rejected — prune the walk, honour an explicit file |
| Default for an absent row: none (opt in) | The repository that needs it most, the joined one, has no `config.md` yet; the ticket's default reads less as a record, which is the safe direction | rejected — the ticket's default |
| Build `seal adopt` | The three outcomes `spec.md` §*What is refused* names: an existing path, an existing path, or a move the root's own rules undo | refused in the spec; a follow-on ticket can overturn |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
`Verified by` cell names the test files the phase pins and what is seen red
first; the hand-back of each phase says how the red was shown.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **`root-migrate` moves nothing without the marks, and names what it left** (box 2). `hooks/root-migrate.py`: `MARKS`, `old_items` keeps an id-shaped directory only with `routing.md` or `rounds/` directly under it; `repoint_path` follows the moved set; the symlink refusal in `main` reads the same; the tail line names an unmarked id-shaped directory with the reason; docstring step 5 and the boundaries say so. Re-read and re-stamp the `hooks/root-migrate.py#…` rows in `seal/releases/0.4.0.md` and `0.5.0.md` with a dated note; the claims hold. Changelog and ledger fragments opened | `tests/test_the_root_migrates_itself.py`: B1 (red against old `old_items`), B2 (red against old `repoint_path`), B3 (a pin, red in a probe with `rounds` out of `MARKS`), the printed reason pinned; every existing case green, the fixture already carries `routing.md`. Narrow run: that file. `evidence-check` on the drifted rows | |
| 2 | **A bare `specs/` reaches the shared/local question; the 0.3.x path needs the marks** (box 1). The Bootstrap paragraph in `skills/implement/orchestration.md`; both READMEs' *Coming up from 0.3.x* say a marked directory moves and the rest stays (the by-hand block untouched); `docs/one-root-by-lifetime.md` and `.ko.md` gain one dated section, *Decided when a joined project's `specs/` was read and never taken (2026-10-0N)*, in the 2026-09-23 shape, with one row for the content test and one for the reference roots; `KEEP` entries in `tests/test_no_document_names_the_old_roots.py` only if the wording spells `specs/<`. Re-read the Bootstrap-heading rows (`0.10.0.md`, `0.12.0.md`) and the README rows (`0.4.0.md:265, 280`) | `tests/test_first_setup_asks_once.py`: A1 (new, red with the sentence deleted), `test_an_unmoved_old_layout_is_not_asked_but_told` green; `tests/test_no_document_names_the_old_roots.py`, `tests/test_both_editions_carry_the_same_folds.py`, `tests/test_the_root_migrates_itself.py#test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set`, `tests/test_docs_line_wrap.py` green. Narrow run: those files | |
| 3 | **The `Reference specs` row, one resolver, and the survivor sweep as its first reader** (box 4, the measured check). `templates/config.md`: the row in the table and a `## Reference specs` section (grammar, `none`, the default, what it governs, the BDD-`specs/` cost); `hooks/config.py#reference_roots`, `#under_reference_root`; `survivor_check.py`: reference roots out of `corpus` and `corrected` through one predicate, `WORK_ITEM_DIR` narrowed to `seal/specs/`; the standing statement in `docs/review-chain-spec.md` §*The survivor sweep* gains *outside the reference roots* and its `Enforced by:` line the new case. The hand-back carries the pool size on this repository before and after | `tests/test_a_reference_root_is_read_and_never_taken.py` (new): C1's five cases, red before the resolver exists; `tests/test_a_corrected_sentence_survives_elsewhere.py`: D1's two cases, red against the old walk; the `records_a_past_state` docstring case and `#test_the_docstring_names_both_sides_of_the_round_record_exclusion` green; `tests/test_a_folded_statement_names_what_enforces_it.py` green over the edited statement. Narrow run: those files. Re-read `0.15.0.md:71–73`, `0.9.3.md:90` | |
| 4 | **Every remaining check is pinned to the root, and a planted team `specs/` shows each leaves it alone** (box 4, the rest). `unverified_check.py#overviews` prunes reference roots from a directory walk and still reads an explicitly named file; one fixture — `specs/1788000001-team-thing/` with `spec.md`, `overview.md` (malformed section) and `design.md` beside a retirable `seal/specs/<id>/` — handed to `settle --retire`, `evidence-check` (both arms), `correction-check`, `chain_check.py` and `unverified-check`, each asserted to leave it on disk, unread as a record, and its own verdict unchanged. The case enumerates the shipped checks by name so a later one is either listed or visibly not | `tests/test_unverified_rows_close.py`: D2 (red against old `overviews`); `tests/test_settle_reads_before_it_removes.py`: D3's retire case; `tests/test_a_reference_root_is_read_and_never_taken.py`: D3's pins, each shown red in a probe by widening the constant it rests on. Narrow run: those files | |
| 5 | **The readers say when they read a reference root and that they cite it** (box 3). `agents/framer.md` §*What you read*: one bullet; `agents/smith.md` §Phases step 1: one sentence; `agents/warden.md` §Role, stage 1: one sentence (a `spec.md` citation into a reference root is opened like any other coordinate); `skills/settle/SKILL.md` §2: one paragraph (may draw on the reference roots for the area's history; the settled statement cites what it read); `skills/implement/SKILL.md` §*Document layout*: one sentence after the roots table; `templates/seal-README.md:51` and `seal/README.md:51` reworded to *nothing writes*. Each names the row and the absent-row default by pointing at `templates/config.md` §*Reference specs*, not by restating the grammar | `tests/test_a_reference_root_is_read_and_never_taken.py`: C2, one case per document (red with the sentence absent); `tests/test_docs_line_wrap.py`, `tests/test_no_document_names_the_old_roots.py` (`KEEP` for the README line if its key phrase moves), `tests/test_every_agent_reads_the_contract.py` green. Narrow run: those files | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **A new optional `seal/config.md` row, `Reference specs`.** Absent means
  the default; no repository has to add it. A repository whose own tests sit
  under a directory named `specs/` loses them from the survivor pool under
  the default and gets them back with `Reference specs | none` or a row
  naming its real reference roots.
- **The session-start hook changes what it moves.** A repository on the
  0.3.x layout is moved as before (every 0.3.x work item carries
  `routing.md`). An id-shaped `specs/<x>/` with no mark is now left and
  named where it used to be taken; the README's by-hand block remains the
  way to move one by hand.
- **The bootstrap asks the shared/local question in a repository with a
  bare `specs/`** where it used to decide shared silently.
- No migration, no new dependency, no change to any check's exit codes or
  to `hygiene.yml`. `survivor-check`'s examined count drops by the size of
  the reference roots; the sealer's run prints it.
