# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `0111020a`, with `5c40359` for the two README copies the survivor sweep named |
| Ran by | `specseal:smith` on Opus 5 (1M context) — the agent definition names no `model`, and the spawning session passed no override, so the segment inherited the session's model |

## What this phase was asked

**The documents stop describing a `settle` that does not exist.**
`seal/README.md` and `templates/seal-README.md`; a dated section in
`docs/one-root-by-lifetime.md` **and** `docs/one-root-by-lifetime.ko.md`;
`docs/review-handoff-protocol.md` §*Layout* and §*Why the directory is not
deleted*, distinguishing the pre-merge deadline from the post-release fold;
`skills/implement/SKILL.md`'s layout table (G6).

Verified by A9 — one case per corrected sentence (§14), the wrap test, and the
survivor sweep read rather than assumed.

## What this phase found

**The handoff protocol was not wrong, it was silent about a second
deadline.** §*Why the directory is not deleted* argues against draft 0.1's
deletion, which happened **before the merge**, while later rounds could still
inherit from the records. `settle` removes the directory **after the release**,
when there is no next round to inherit anything and the deferral deadline has
been in force for the whole of the work item's life. Both sections now say
which deadline they are about, so a reader meeting *it outlives the merge*
does not read it as *it is never removed*. Nothing in the protocol's own
requirements changed: the protocol is about the first deadline.

**The design record takes the later decision rather than a rewrite.**
`tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD` classifies
`docs/one-root-by-lifetime.md` as a record of a moment, and both editions
already have the shape for a later decision — a dated table. Six rows were
added to each: what `settle` turned out to be, where the fold record lives,
what groups, what a removal actually breaks, who may write in `docs/`, and
whether the mechanism's own release folds this repository. The 2026-09-02 text
is untouched, including the two sentences that predicted what this work item
would correct.

**§*The dependency rule* is corrected in the dated section and not in place,
and the correction is the load-bearing one.** It named two readers; the real
list is those two, the survivor sweep, and every check carrying a population
floor over `seal/specs/`. Left as it stood, a later fold branch would start
from a list of two and rediscover the rest as a red suite.

**A case comparing the two editions is cell-for-cell rather than
sentence-for-sentence.** The rows are prose in two languages, so nothing can
compare their text; what a drift would look like is one edition taking a
decision the other did not, which is a row count. `CONTRIBUTING.md` requires
the two to move together and the hygiene workflow only warns, so the case is
what actually holds them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/implement/SKILL.md`'s *never created here* claim about `docs/` | the same table cell, which now names `settle` as the one writer; `docs/one-root-by-lifetime.md`'s dated section records that the correction happened |
| `seal/README.md`'s and `templates/seal-README.md`'s *a later `settle`* — the step described in the future tense | the same paragraph, which names the command, the skill and the two halves |
