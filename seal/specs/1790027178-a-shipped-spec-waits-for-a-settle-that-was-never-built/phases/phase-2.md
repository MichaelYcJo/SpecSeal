# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `b3ddd2b7` |
| Ran by | `specseal:smith` on Opus 5 (1M context) — the agent definition names no `model`, and the spawning session passed no override, so the segment inherited the session's model |

## What this phase was asked

**`settle` reads.** `skills/settle/scripts/settle.py` plus `bin/settle` and
`bin/settle.cmd`: enumerate released, unfolded work items; group them by
ledger anchor rolled up to a segment; name the ungrouped; skip and name an
item with an open `evidence-todo.md` row; record what was folded so a second
run folds nothing twice and an interrupted one resumes. Writes nothing to
`docs/`, removes nothing. Carries the interpreter-floor guard.

Verified by A3, A4, A5 and A7 — cases over a fixture root, and the report over
this repository's own tree. The phase also decides Q2 (what a `tests/` anchor
rolls up to) and Q4 (where the fold record lives), and records the rule each
one actually used.

## What this phase found

**Q4 is decided on its default, and the default turned out to be the only
answer that also makes the run resumable.** The fold record is the
`<!-- specs/<id> -->` provenance comment the folded prose carries in its
`docs/` document. What was not obvious from the row: because the record is
DERIVED from the destination, it splits the work into two halves that can be
in different states — folded but not retired, folded and retired — and that is
exactly what A4's *an interrupted run resumes* needs. A record kept in a file
of its own would have had to be written twice, once per half, and a run
interrupted between the two writes would have left the file disagreeing with
the tree. The command reads it through
`skills/verify/scripts/unverified_check.py#folded_items`, which phase 1 wrote:
one reader, loaded the way `chain_check.py` already loads that module.

**Q2 is decided on its default, and the rule is a majority over the work
item's code anchors.** A work item's segment is the file the most of its
non-`tests/` coordinates anchor in, ties broken by path order so the same
input always gives the same grouping. Test anchors are dropped in favour of
code anchors — a case pinning `round_record.py` is evidence about
`round_record.py` — and a work item whose anchors are ALL under `tests/` is
named as `tests only` rather than filed under a guess, because the link from a
case to the code it pins is nowhere a machine reads.

Measured on this repository, which is what the rule was decided against: **two
work items are `tests only`** — `1788735085-a-loaded-file-naming-a-real-version-is-a-timer`
and `1789540097-three-checks-that-do-not-see-what-they-are-named-for`. So the
48% of coordinates that sit under `tests/` cost two named items out of 97, not
a segment called `tests` holding half the corpus. The majority rule is what
buys that: nearly every work item that writes a case also writes a row about
the code the case pins.

**A second arm was needed and the spec implies it rather than naming it.** A3
says *with no write flag*, so a write flag exists; nothing in the spec says
what it does, and it cannot write prose (G1). It is `--retire`: it removes the
directories whose fold `docs/` records, and refuses one the evidence-todo
guard is holding even when the marker is there. That keeps the judgment with
the session and the mechanical half with the command, and it is what makes
`plan.md` §*What breaks in six months* true — the worst outcome available is a
thin policy document, which a reader can see, rather than a directory removed
with nothing absorbing it.

**`released` refuses rather than degrading, and local mode is why the message
says so.** A `--released-at` ref that does not resolve would make every work
item read as unreleased and the whole report read as *nothing to fold*, which
is the quiet zero every checker here is written against. In local mode the
root is never committed, so no ref holds the directories at all and there is
nothing the command can call released; the refusal names that case rather than
leaving a reader to find it.

**`load()` arrives repaired rather than copied broken.** The rider on
`skills/code-review/scripts/round_record.py#load` says a missing sibling
reaches `exec_module` and dies in a traceback, because
`spec_from_file_location` hands back a spec for any path ending in `.py`. This
copy checks the file exists first and refuses with a sentence. The rider's own
coordinate is untouched — that is its file's work item, not this one's.

**What phase 3 inherits.** The skill has to carry the two halves this command
deliberately does not do: which sentences go up (a judgment) and where they
land. It also has to carry the population-floor rule (A11), which `spec.md`
§*The ticket's headline claim is false* establishes as general and which
`docs/one-root-by-lifetime.md` §*The dependency rule* gets wrong by naming two
readers where there are at least sixteen.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing — the phase only adds | none |
