# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d735248 |
| Ran by | specseal:smith on claude-opus-5[1m] |

<!-- The spawn prompt carried no `Ran by` value. The model id above is the one
the harness stated at spawn, not one this segment decided about itself, and
the orchestrator is named in `overview.md` as the party who can confirm it.
The same value stands in phases 2 to 5 for the same reason. -->

## What this phase was asked

Split `skills/code-review/SKILL.md` on the seam the file already declares:
the five sections it prefixes `Orchestrator:` leave a warden spawn's startup
payload. Not #255 §4's seam. Where the five sections go was left to `plan.md`
on one constraint — the orchestrator must reach them without knowing a path
it has to be told — with a further instruction to read how other skills in
this repository carry material that is not their preload before inventing a
third shape.

## What this phase found

**The five sections are one contiguous block, lines 236–653.** Nothing said
they would be. It is the strongest available evidence that the seam is the
author's rather than this change's: every heading in the run carries the
prefix and no heading outside it does, so the split is a single cut with no
interleaving to judge.

**No skill in this repository carries non-preload Markdown.** `find skills
-type f | grep -v 'SKILL.md$'` returns seven files and all seven are under a
`scripts/` directory. So "a reference file under the skill's directory" is a
shape this tree uses for scripts and not for prose, and the mechanism — the
skill names the path, only `SKILL.md` is the payload — is what carries over.

**A skill of its own was rejected on a cost the plan records in full.** Four
cases in `tests/test_chain_hooks_hardening.py` glob `skills/*/SKILL.md` and
two of them read a count both READMEs must spell, so a new directory moves
four pinned numbers in two languages. Worse at runtime: a new skill either
fires on its own description mid-round, or becomes a slash command a person
must type for a procedure no person types.

**The section table had to be re-measured.** The ticket's 24,553 characters
and 55% were taken on `release/v0.9.2` at `a495e4f`; at this branch's base the
five sections are 24,948 of 46,986, which is 53.1%. Both readings are correct
about their own commit and only one of them is about this diff.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The five `Orchestrator:` sections, 418 lines, from `skills/code-review/SKILL.md` | `skills/code-review/orchestration.md`, verbatim — the removed lines are byte-identical to the block the new file holds, checked against `git diff -U0` |
| Nothing else | none |
