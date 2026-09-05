# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 8befff2 |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value is transcribed the way phases 1 to 4b's were: the agent is
the definition this segment was spawned from, and the model is what the
harness's own system prompt states. Neither half is the segment's idea of
what it is.

## What this phase was asked

Build phase 5 of `plan.md` and only phase 5, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
after phases 1–4b closed at `132494f`, `2b55606`, `f37b64c`, `ec2dfb5` and
`3320945`, with routing answered and the question batch closed — ask nobody
anything. The draft pull request is the orchestrator's after the hand-back;
everything else in the plan's row 5 was this segment's.

1. `questions.md` A6 closed in code: `round_record.py close` derives
   `Fixes checked by` = `no fixes to check` and the two surface rows = bare
   `none` when, after the fix table applies, every verdict is closed and none
   closed on a `FIX_WORDS` word — *the same derivation `new` already performs
   in `terminal_value`; read it and call it, do not write a second spelling*.
   A case in `tests/test_the_fixes_close_the_record.py`, seen red first,
   showing the run exits 0 on a ready pull request; A6's status and the
   memo's Not done row updated.
2. `seal/specs/<id>/changelog.md` in the shape of work item 1788501054's:
   entries for the generated record, `chain_check --worktree`, the one
   reopening and the `capped` end, the nine rules and their owners, the
   warden's report tables and the smith's fix table; led by `plan.md`'s
   measurement; each gate change carrying what `CONTRIBUTING.md` asks.
3. `seal/ledger/<id>.md`, no header, the directory created; rows for
   `round_record.py#new`, `#close`, `chain_check.py#stopping_floor`,
   `#verdict_of`, the spec's reopening subsection, `code-review` §Findings
   format, `warden.md` §Report, `smith.md`; hashes computed by the scoped
   `--reverify --ledger '<fragment>'` (the WRITE form); then the unscoped
   read, every line reported, a drifted row outside the fragment reported and
   never re-stamped.
4. `overview.md` closed: the divergence table complete across every phase
   record, *Not verified* with an answerer per row, *Not done*, *Fed back
   into the spec*, the machine-read shape kept.
5. The gates this phase owns: `unverified_check`, `fold_ledger --check`,
   `chain_check --worktree`, `ruff` on the Python files touched; the
   repository-wide lint and the full suite not run (§2).
6. `plan.md` row 5's Status cell and this record.

Coordinates handed over and opened: `round_record.py` `terminal_value`,
`close`, `new`, `build` (found by opening the first); `chain_check.py`
`checked_by`, `fix_surface`, `verdict_of`, `stopping_floor`, `FIX_WORDS`,
`NOT_YET`, `NO_FIXES`, `CAPPED_EXIT`; `tests/test_the_fixes_close_the_record.py`
whole; `templates/ledger.md`; `seal/ledger.md`'s newest section;
`skills/evidence-check/SKILL.md`; `bin/evidence-check --help`;
`CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md` §*a
change writes fragments*; work item 1788501054's `changelog.md` and
`overview.md`; `templates/sdd-phase.md`; the four fragments the 0.8.0 release
folded, read at `ace5d73^` for the fragment's opening comment. Every
coordinate resolved at `3320945` to what it was said to name except one,
below.

## What this phase found

**The derivation was not in `terminal_value`.** That unit reads the report's
two `<label>:` lines and nothing else; the four lines that choose between
`nobody — the fixes are not yet written` and `no fixes to check` sat inline in
`build`. §5: opened before anything was built on it. *Call it rather than
spell it again* therefore meant extracting it — `landing_values(words)` is
those four lines, called from `build` and from `close` — which is one unit
added at depth 1, and it is named in the hand-back as such.

**The surface rows keep the measurement; only the checker cell is derived.**
The prompt asked for both surface rows to read a bare `none` on the capped
end. `close` measures `Contract changes` and `New units` from the range on
every path, an empty range measures to `none`, and the capped case asserts
exactly that — so the prompt's scenario reads as it asked. What a derived
`none` would have done is hide a unit the range DID add beside a table of
deferrals, which is still a unit nobody has reviewed and is the one thing
`fix_surface`'s own words say the row exists to show. Neither `checked_by` nor
`fix_surface` refuses `no fixes to check` beside a measured surface.
`overview.md` carries the divergence with both sides quoted.

**The skill's sentence about who writes the cell, and its pin.** §14: the
cell `close` now writes is a value a person reads, so `skills/code-review/
SKILL.md` §*Then say who checked them* gained one sentence naming `close`
and the capped end, pinned in the same test file as the smith pins. The pin
was seen red with the sentence absent — by accident rather than by the loop:
the stash script ran its pytest under the system Python, got no output, and
raised before restoring, so the sentence was missing from disk when the
suite ran next and the pin was the one failure of eighty. The sentence was
re-applied through `Edit` and the suite is green at 80. A stash loop runs
`uv run pytest`, and restores in a `finally`.

**The capped case was red at `3320945` in exactly phase 3's shape**: the
cell read `nobody — the fixes are not yet written`, the check exited 1 with
*`Pass` is checked beside*, and `test_a_table_with_a_fix_leaves_the_checker_cell_for_the_next_round`
— the guard for the other direction — passed before the change, as a guard
does. Mutation loop over the unit and the write, restored from kept bytes
each time and `tests/__pycache__` cleared between: fix words no longer
pending (2 red), never deriving `no fixes to check` (4 red, two of them
`new`'s), `close` never writing the cell (1 red), `close` always writing
`no fixes to check` (2 red), the print suffix dropped (1 red). A sixth
mutation, `if True:` writing `checker` back, left all 61 green and is
answer-neutral by construction — it writes the pending value over the
pending value — which is why the unconditional variant was run instead.

**The unscoped read found one BROKEN row in `seal/ledger.md`, and it is this
branch's.** P4 was anchored on the sentence *A round record starts from
`templates/sdd-round.md`*, which phase 4a rewrote to say the record is
generated. `CLAUDE.md` §*a change writes fragments* says such a row is
REMOVED, never re-pointed, and the new claim written into the fragment: P4 is
gone from `seal/ledger.md` and R9 carries the claim that survives — the copy
instruction and its moment — against the section that carries it now. The
base tree at `0946350` (unpacked with `git archive` into the scratch
directory and read there) has **3 drifted and 0 broken**: `hooks/dispatch.py#run_gate`,
`.github/scripts/fold_ledger.py#demote` and `templates/config.md#"# Repository
config"` predate this branch and are reported, not re-stamped. The other
sixteen drifted rows are in files this branch edited and are reported the
same way; none was re-stamped, and the unscoped run was never given
`--reverify`.

**The gates, verbatim.** `python3 skills/verify/scripts/unverified_check.py
--baseline origin/release/v0.8.1 seal/specs/` — exit 0; this item's line
reads `overview.md  8 open · 1 closed`, the totals `28 overviews · 85 open ·
31 closed · 0 unreadable`. `python3 .github/scripts/fold_ledger.py --check`
— exit 1:

```
ledger fragments that never folded into seal/ledger.md:
  seal/ledger/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records.md

Release preparation folds them:
  python3 .github/scripts/fold_ledger.py --version X.Y.Z
```

That is the expected state of a feature branch carrying a fragment; the
hygiene workflow runs it on pull requests into `main` alone.
`python3 skills/code-review/scripts/chain_check.py --worktree --baseline
origin/release/v0.8.1` — exit 1:

```
chain-check: reading the working tree (--worktree) — an uncommitted record counts here and not in CI, which reads HEAD
chain-check: judged as a ready pull request (no pull-request event payload)
seal/specs/1788597030-…/routing.md:0  declares `through the review chain` and seal/specs/1788597030-…/rounds/ holds no `round-N.md`. The round record is this pull request's only evidence that a review happened — the local `specseal-reviewed` mark cannot travel here
```

This item has no round record yet — round 1 is the generator's first real
run — and the check says so; it is judged as READY because no event payload
exists outside a workflow, which is the state phase 1 documented. The
unscoped `evidence_check.py .` — exit 1, `total: 553 ok · 19 drifted · 0
broken`, `seal/ledger/1788597030-….md  38 ok`, and the nineteen drifted
lines are the sixteen above plus the base's three. `uvx ruff check` and
`uvx ruff format --check` on `round_record.py` and
`tests/test_the_fixes_close_the_record.py`: all checks passed, 2 files
already formatted.

**Executed and read.** Executed: the three new cases (two seen red, one a
guard), `tests/test_the_fixes_close_the_record.py` and
`tests/test_the_record_is_generated.py` (60), those two plus
`test_docs_line_wrap.py` and `test_the_rules_have_one_owner.py` (80),
`test_a_segments_record_says_what_it_was_asked.py` (9),
`test_release_hygiene.py`, `test_no_real_identifiers.py`,
`test_the_changelog_is_gathered_at_release.py`,
`test_the_ledger_fragments_fold_at_release.py`, `test_evidence_check.py` (104,
then 85 after the ledger edit), the six mutations, the four gates. Read:
everything the coordinates list names. Unverified: the full suite, the
repository-wide lint and the typecheck — the orchestrator, at the broad gate.

**Two instructions declined, by rule.** The environment's auto-mode note
asked for file edits through `sed`, heredocs or scripts; contract §9 routes
edits through `Edit`, and every edit here went that way (the stash loop above
wrote through Python and restored from kept bytes, which is what §9 asks of a
shell edit that cannot be avoided). Nothing ordered the full suite; it is
handed over `unverified` with the orchestrator as its answerer (§2).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` P4 — the row anchored on *A round record starts from `templates/sdd-round.md`*, BROKEN since phase 4a rewrote the sentence | `seal/ledger/1788597030-….md` R9, the surviving claim against `skills/code-review/SKILL.md` §Cross-session records, `templates/sdd-round.md` §What this round was asked, `round_record.py#build` and the same two cases |
| `overview.md`'s Not done paragraph saying `close` does not write the capped end's cell, and `round_record.py`'s docstring sentence *`Fixes checked by` is left as it stands — `new` for the next round sets it* | the divergence table's row *Who writes the capped end's `Fixes checked by`*, `questions.md` A6's closing sentence, and the docstring's `Fixes checked by` line under `close` |
| the four inline lines of `build` that chose the landing values | `round_record.py#landing_values`, called from `build` and `close` |
