# Implementation Plan: every markdown reader shares one fence rule (#584)

<!-- seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

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

Nine readers outside the ledger checker still decide by a rule of their own
whether a markdown line is quoted. Each is brought to the shared definition in
`skills/verify/scripts/unverified_check.py`: the delimiter pair
`fence_opener` / `fence_closes`, and the two walks already built on it,
`live_lines` for a marker and `closed_fence_lines` for a ledger row. The one
hook in the class, `hooks/config.py`, keeps its own copy, gains the comment
half, and has that half held to the shared functions by a parity test.
`spec.md` §*The class, enumerated* is the list, and it says which readers
stay apart and why.

## Technical context

- **The definition.** `unverified_check.py#fence_opener`, `#fence_closes`,
  `#fence_spans`, `#closed_fence_lines`, `#blank_fences`, `#comment_scan`
  and `#live_lines`. Nothing in this work edits any of them. Phase 7 edits
  `fence_opener`'s docstring alone.
- **How the release scripts load it.** `fold_ledger.py#load_reader` loads
  `unverified_check.py` by path at import, and a missing file is a traceback
  at the release, which that file's comment calls the loud direction.
  `gather_changelog.py` takes the same loader. `rider_check.py#load_checker`
  is the shape for a loader that says what is missing.
- **How the shipped scripts load a sibling.**
  `tests/test_a_script_copied_alone_exits_2.py`'s docstring: by path, and a
  missing file exits 2 with a sentence. `payload_meter.py#_session_cost` is
  the model.
- **The hook.** `hooks/config.py` is imported by `hooks/mode-gate.py`, a
  `PreToolUse` hook on every Bash call (`hooks/hooks.json`), and by
  `skills/implement/scripts/seal.py` and `skills/verify/scripts/broad_gate.py`
  and `skills/settle/scripts/fold_check.py`. Its three table walks read
  through `#unfenced`. `broad_gate.py#fenced_row_at` takes the complement of
  `#unfenced`, so a comment hidden INSIDE `#unfenced` would be reported by
  that refusal as a fence. That is the #429 wrong-cause shape, and phase 6
  exists to keep it from coming back.
- **Parallel work.** A (#585) adds an arm to `evidence_check.py`. This plan
  does not edit that file. D (#28) changes `hooks/dispatch.py`'s handling of
  a gate that fails to load. This plan adds no import to any hook, so the two
  do not meet.

**What breaks in six months.** A seventh markdown reader is written with its
own fence loop, because nothing enumerates readers mechanically. The guard
here is the one `fence_opener`'s docstring already is: a list a reviewer
checks a new reader against. The second is the config copy drifting from the
shared comment scan. The parity test is what catches that, so a shape that
matters and is missing from its table is the failure to watch for.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Chosen for the hook:** `hooks/config.py` keeps its own copy and adds the comment half, held to `comment_scan` + `blank_fences` by the parity test | The copy and the oracle agree on every shape in the test's table and disagree on one that is missing from it | Chosen. It is the arrangement the fence half already has, which `fence_opener`'s docstring and S6 of `1790260566` ratified, and it adds nothing to the hook path |
| The hook loads `unverified_check.py` by path | Every Bash call in every consumer session compiles and runs a 1,670-line module, and a broken skill module becomes a broken `PreToolUse` gate while D decides what that failure does | Rejected. `fence_opener`'s docstring gives the cost reason, and D gives the timing reason |
| Move the rule into a small module under `hooks/` and let `unverified_check.py` re-export it | The rule's home moves. The ledger rows anchored on `fence_opener`, `fence_closes`, `fence_spans`, `live_lines`, `_liveness`, `_partner_ahead` and `_paragraph_ends_at` become REMOVED, and every docstring citing `unverified_check.py#fence_opener` is rewritten | Rejected. The same guarantee costs a parity test, and this costs a dozen ledger rows and a rename across the corpus |
| Copy all of `live_lines` into the hook, so its comment half models code spans | A second copy of the rule that five review rounds of `1790039346` were spent on, on a hook path | Rejected. The oracle this plan picks has the same blind spot as the copy, so they agree, and that blind spot is already `readable`'s |
| Leave the config comment half out | A person comments out an old `\| Item \| Value \|` table, or the first row of the live one, with a multi-line comment, and the gate runs a command or reads a mode nobody declared. That is silent | Rejected. The milestone assigns `hooks/config.py` to this item. The direction is the module's own, and closed-comments-only means no file that reads today stops reading |
| **Chosen for the marker readers:** `live_lines` | A ledger file with a fence that never closes hides every marker below it (`spec.md` §*The direction of each change*) | Chosen. `docs/the-evidence-ledger.md` §*A marker counts only on a live line* says one function decides, and `survivor_check.py#gathered_fragments` already reads `CHANGELOG.md` through it |
| The marker readers skip closed fences only (the ledger-row rule) | Two readers of one `CHANGELOG.md` marker disagree about a marker in a comment or after an unclosed fence | Rejected. That is the policy clause's failure |
| **Chosen for `correction_check.py#rows`:** `closed_fence_lines` | none new. It reads exactly the rows `evidence_check.py#quoted_lines` leaves | Chosen. A row the checker watches is a row whose correction can be lost |
| `correction_check.py#rows` through `live_lines` | A row the checker reads, under an unclosed fence or in a comment, loses a correction and nothing reports it | Rejected. That is the silent direction for the one check that exists to see a lost correction |
| **Chosen for `rider_check.py`:** fence spans in `.md` files only, unclosed to the end | A rider written below a fence somebody forgot to close is not read. It loses an alarm | Chosen. `rider_check.py`'s docstring: "where a rule has to fall one way, it falls toward the silence" |
| `rider_check.py` through `live_lines` | A second rider inside an open comment stops being read, which `comment_blocks` reads on purpose (its "second marker before the closing `-->`" paragraph) | Rejected |
| `rider_check.py` reaches the rule through the checker it holds (`evidence_check.py#fence_rule`) | It couples to a function in the file A is editing in parallel | Rejected in favour of loading `unverified_check.py` by path, with `load_checker`'s missing-file shape |

## Phases

Vertical slices — each phase ends with something runnable and verified.

Every phase: the cases it names are seen red before the fix (contract §15),
the rows its edited units carry are re-read and re-stamped (`spec.md`
§*Data & interfaces*), and the reader moves into `fence_opener`'s docstring
list in the same commit. The narrow run is the phase's own test module.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `fold_ledger.py`: `demote` on `fence_opener` / `fence_closes` and its `# RIDER:` retired. `is_marked` (so `folded`), `doubled_markers` and the `--check` count read markers through `live_lines`. `version_headings`, `section_heading` and `insert`'s walk to the next `## ` skip fenced lines. `docs/branch-and-release.md` says a quoted marker is not a fold, where it describes `--check` | S1–S5, in `tests/test_the_ledger_fragments_fold_at_release.py` | c3afabf8 |
| 2 | `gather_changelog.py`: `ungathered` and the `--check` count read markers through `live_lines`, loaded as `fold_ledger.py` loads it. The module docstring says a marker counts only on a live line | S6, S7, in `tests/test_the_changelog_is_gathered_at_release.py` | a031f605 |
| 3 | `rider_check.py#comment_blocks`: in a `.md` file, a line inside a fence span opens no rider and changes no comment state. It loads `unverified_check.py` with `load_checker`'s missing-file shape. The docstring's paragraph on what opens a block says so | S8, S9, in `tests/test_a_rider_reaches_its_file.py`. The tree's own `rider_check.py` run is unchanged except for the rider phase 1 retired | 3c0787ff |
| 4 | `correction_check.py#rows` skips rows inside a fenced block that closes. It loads the reader by path and exits 2 with a sentence where it is missing. §*What it reads* in the module docstring says which rows | S10, S11, in `tests/test_a_merge_cannot_silently_drop_a_correction.py`. S18's row for this script | 3f422fa7 |
| 5 | `payload_meter.py#heading_starts` and `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings` on `fence_opener` / `fence_closes`. `payload_meter.py#FENCE` and the test's `FENCE` retire. The meter's missing reader exits 2 with a sentence | S12, S18's row for this script. Q2 answered before the fix | ee193db3 |
| 6 | `hooks/config.py`: the one table generator hides lines inside a closed HTML comment as well as fenced lines. An unclosed comment hides nothing. `broad_gate.py` names a `Broad gate` row that stands only inside a comment. `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row* gains the comment sentence, and the `Enforced by:` line names S17's case | S13–S17. `tests/test_the_mode_question_is_asked_once.py` and `tests/test_the_seal_is_taken_once_by_the_sealer.py` as the neighbouring modules | 6feed792 |
| 7 | `fence_opener`'s docstring: the paragraph naming "the readers #584 names" is rewritten as the readers that stay apart, each with its reason from `spec.md`. The ledger fragment carries this work's claims, and `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/changelog.md` its entry | `git grep` for `#584` in `unverified_check.py` and the files above returns only what this phase meant to leave | 56a47561 |
| 8 | **The readers with no fence state at all (#658).** Added 2026-09-29 by the orchestrating session at the owner's request, after round 1, to fix in this branch rather than file: the frame put them out as a different class, and the owner asked that the class be finished here. `hooks/routing.py#table_rows` (a routing row quoted inside a fence in `routing.md` reads as a declaration), the `--exempt` reader in `survivor_check.py` (a quoted exemption can excuse a survivor), and the own fence toggles in `tests/test_docs_line_wrap.py` and `tests/test_handoff_outlives_the_merge.py`. The hook keeps the copy-and-parity-test shape phase 6 chose for `hooks/config.py`, since a hook does not import from `skills/`. Work item D (#28) is editing other hooks in parallel and has been told to stay out of `routing.py`. | (1) For each reader, a fenced row that reads as live today, **seen red** at `08d4aec3`. (2) `bin/test` over each reader's modules and the parity test. (3) One mutant per changed unit, killed. | 7c47eec8 |
| 9 | **A fragment that leaves a fence or a comment open cannot hide the markers written below it (round 1, 🟡 1 and 🟡 2; `questions.md` Q5).** Added 2026-09-29 by the orchestrating session: round 1 found that `gather_changelog.py` and `fold_ledger.py` write a fragment verbatim, so an open fence or comment in one puts every later marker on a line their own `live_markers` cannot see. The gather's `--check` then asks for a second gather that doubles the entry, and the fold's case is silent. Closing it needs a rule a fix pass may not add. The builder chooses between refusing such a fragment before anything is written, and closing what it left open; the failure must be loud before a write, never a doubled entry after one. | (1) The two shapes round 1's report drafted, each **seen red** at `a06f23b2`. (2) `bin/test` over the gather, fold and live-marker modules. (3) One mutant per changed unit, killed. | 028eee43 |

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

**Order.** Phases 1 to 5 are independent of each other, and each can land on
its own. They run in ascending order of what a wrong answer costs: release
automation that a person watches, then a shipped check, then a meter. Phase 6
is last because it is the one change to a hook and the one new sentence a
person reads. Phase 7 closes the list after every reader has moved.

## Operational impact

- **No new dependency, flag or exit code.** One new refusal sentence in
  `broad-gate` (phase 6).
- **Two shipped scripts gain a load.** `correction_check.py` and
  `payload_meter.py` now load `unverified_check.py`. A copy of either taken
  without the plugin exits 2 with a sentence instead of reading.
- **Release automation.** `fold_ledger.py --check` and
  `gather_changelog.py --check` can change their answer only where a marker
  or a version heading stands inside a fence, a comment or a code span. The
  tree held none on 2026-09-29.
- **Consumers.** A `config.md` row inside a closed HTML comment stops being
  read, which can change the command `broad-gate` runs or bring back the
  mode question once. That is a behaviour change a consumer can see, and the
  changelog entry says so.
- **Platform.** Nothing here reads a process or a path. Line endings are the
  one platform-shaped input, and `fence_opener` already strips `\r\n`. The
  CRLF shape in the parity table covers the comment half.
