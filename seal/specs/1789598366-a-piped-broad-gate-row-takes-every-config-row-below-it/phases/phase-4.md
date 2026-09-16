# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | <pending> |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The documents and the records that promise the old behaviour.
`templates/config.md` §*What is refused, and what stays allowed* — the pipe row
now says how a pipe IS written; `skills/config/SKILL.md`; the changelog
fragment; the ledger fragment, where the falsified claim is removed and
rewritten. The cases asserting the old sentences change with them, in the same
commit, because a record naming a unit the tree lacks takes even the non-strict
`evidence-check` to exit 2.

## What this phase found

**Four documents carried the old promise, and `plan.md` named two.** The third
is `skills/implement/orchestration.md`'s bootstrap paragraph, which told a
session that a candidate carrying a `|` *cannot be written into the row* and to
offer the command without its pipe — advice that is now wrong in the one place
a candidate is actually derived, off a CI `run:` step. The fourth is
`skills/config/SKILL.md`, which `plan.md` does name but where the sentence that
was needed is not the one the plan implies: the skill points at the criterion
and both lists rather than copying them, so what it gained is **how to write
the cell at all**, which is not one of the three rules and cannot be read off
either list. It is the file that tells a person to edit the value in place, so
it is where they meet a value that needs a pipe.

**`plan.md`'s verification command for this phase names neither module that
pins the two document sentences.** It reads
`bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_settings_have_a_front_door.py -q`,
and the template's pipe case lives in
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` while the
bootstrap's lives in `tests/test_first_setup_asks_once.py`. Run as written, the
phase that rewrote both documents would have run neither case. All four
modules were run; this was reported at the close of phase 1, when the frame was
read, rather than discovered here.

**Two more cases were renamed, and one record needed marking.** A case whose
name says a pipe *cannot reach the row at all* and one that says a candidate
carrying a pipe is *refused* both state what stopped being true.
`seal/specs/1789445605-.../rounds/round-2-report.md` names both old names, and
that line is history — the round read what it read — so it carries
`NAME NOT IN TREE` with the new name beside it, which is what the records arm's
own rule prescribes. This work item's own `phase-1.md` and `overview.md` needed
the same marker for the same reason.

**Six ledger rows drifted and every one was re-read rather than swept.** Three
in `seal/ledger.md` (the template's shape, and the config skill's two) and
three in `seal/ledger/1789445605-...md` (the criterion's one owner, the
bootstrap question, the trailing `&`). None of their claims moved: what the
branch edited is one cell of one list, one paragraph of one step, and one new
bullet. Each row carries a note saying what was read and on what date, and
`--reverify` was run only after that reading — #424's rule, applied.

**The pipe cell gained a condition the old one did not have.** *And it takes
every row below it* is true only where a row above the piped one already
parsed; with the piped row first, `config_rows` steps past it and the rows
below survive. The cell now says so, and it names the worst outcome — `seal
mode` writing a second `Mode` row — which the old cell reached for through the
language rows instead. `questions.md` M2 is why: no production path reads
either language row through `config_rows`, so the ticket's example was a hazard
rather than a live loss.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `templates/config.md`'s *a pipe cannot reach this row at all* and *escaped or not* | the same cell, which now says the escape is `\|` and that a BARE pipe still parses as no row |
| `skills/implement/orchestration.md`'s *A candidate carrying a `\|` cannot be written into the row* | the same paragraph, which now says to offer it with the pipe escaped |
| `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py#test_the_allowed_list_says_a_pipe_cannot_reach_the_row_at_all` <!-- NAME NOT IN TREE: renamed by this phase; the new name is in the right-hand cell. --> and `tests/test_first_setup_asks_once.py#test_a_candidate_carrying_a_pipe_is_refused_where_candidates_are_derived` <!-- NAME NOT IN TREE: renamed by this phase; the new name is in the right-hand cell. --> — renamed, so both anchors are removed rather than drifted | `test_the_allowed_list_says_how_a_pipe_is_written` and `test_a_candidate_carrying_a_pipe_is_escaped_where_candidates_are_derived`, in the same files. No ledger row cited either; the round record that names both carries `NAME NOT IN TREE` |
