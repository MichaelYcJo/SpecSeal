# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 81888e22 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The criterion the row has never had. The three rules into `templates/config.md`
§*Broad gate*, which becomes their one owner; `skills/config/SKILL.md` and
`skills/implement/orchestration.md` point at it and restate nothing. Rule 3
exists in two places today and is folded into the one home rather than copied
a third time. Red first by deleting each rule, and by leaving rule 3's second
copy in place.

## What this phase found

**Rule 3's two copies were the template's closing paragraph and the config
skill's bullet**, and the fold is a real fold rather than a deletion: the
paragraph's whole content — the reactive base comparison, the scratch
worktree, `new` or `failing on base too`, and why the runner comes first — is
now rule 3's *Why* cell, and the standalone paragraph is gone. The template
carries the string `The suite runner comes first` exactly once, which a case
asserts.

**`tests/test_the_rules_have_one_owner.py` took the rule in its own shape,
with no new mechanism.** Its `RULES` table is `rule → (owner, the sentence the
owner states, {link carrier: how it names the owner})`, and the criterion fits
it as a twelfth entry. That is the whole of what this phase needed from that
module: no new checker, no new walk. The rule's owner sentence had to be
prose the module's own `flat()` can find, which a table cell is.

**`skills/implement/orchestration.md`'s link is phase 4's, not this one's.**
A8 wants both carriers pointing at the owner, and the orchestration file has
no reason to mention the row until the bootstrap asks for it. The `RULES`
entry lists only `skills/config/SKILL.md` here and gains `ORCH_IMPL` in phase
4 — recorded because a reader comparing A8 against this commit will find half
of it.

**Eight mutations, all red**: each of the three rules deleted, rule 1's reason
deleted, the link to the owner dropped from the config skill (against both the
new module and the one-owner module), and rule 3's second copy put back in
place, which fails the fold case.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `templates/config.md` §*Broad gate*'s closing paragraph on the base comparison | rule 3's *Why* cell in the same section's criterion table, which carries every sentence of it |
| `skills/config/SKILL.md`'s *put the suite runner first, because the base comparison re-runs what stands before the first `&&`* | the same rule 3 cell. The bullet now names the owning section instead |
