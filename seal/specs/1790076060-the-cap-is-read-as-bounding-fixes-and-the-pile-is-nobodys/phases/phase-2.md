# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c2527d96 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#492's carriers become links naming the owner phase 1 wrote:
`skills/code-review/orchestration.md`, `templates/sdd-round.md`,
`docs/review-handoff-protocol.md`, `agents/warden.md`, `agents/smith.md`,
`agents/sealer.md`, and the restating comment in
`skills/code-review/scripts/chain_check.py`. A new `RULES` row in
`tests/test_the_rules_have_one_owner.py` pins the rule and its links, with the
row's two assertions seen red before it is committed as a case.

## What this phase found

**The link had to say something different in each carrier, and that is what
made it a link rather than a copy.** The repository's link shape is one
sentence naming the owner's subsection, and seven carriers naming the same
subsection in the same words would have been the eight-carrier failure this
module exists to refuse, one level up. Each carrier says what the rule means
where it stands: the orchestrator decides, the template and the protocol
describe the record shape the decision produces, the warden keeps reporting at
the severity it finds, the sealer reads a `round-N` as a capped run that wrote
fixes rather than as a defect, and the smith learns that a capped run does not
end its fixes.

**`chain_check.py` is a link carrier, and the row's constant says why it can
be.** Its module docstring restated the capped exit without saying which bound
the exit belongs to. The new sentence names the owner and adds one fact about
the code that follows it — the walks read the records either shape produces
without knowing which bound ended the run. No constant, no arm, no message
moved, so nothing the checker computes changed.

**The eight mutations were killed one at a time, not as a set.** A probe
(`test_tmp_*`, run once, deleted) saved each file's bytes, removed one needle,
ran the module, and restored from its own copy. Every run exited 1 and named
the case it was meant to redden — `test_the_owner_states_the_rule[13 …]` for
the owner's sentence and `test_every_link_names_the_owner[13 …]` for each of
the seven links — and the module was 58 green before the first mutation and 58
green after the last restore. A second finding came out of the probe itself:
the needle is wrapped across lines in every carrier, so a raw `in` test
matched nothing and the mutation had to be whitespace-flexible, which is the
same join the module's own `flat()` does. A probe that had asserted nothing
would have reported a green mutation as a killed one.

**What was run, and what was not.** Sixteen modules — every module that pins
prose in a file this phase touched — ran at the phase boundary: 822 passed, 8
skipped, exit 0. The full suite is the sealer's and was not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — every carrier gained a sentence and lost none. The exit sentence each of them already carried is unchanged, because it is true of the bound it was written about | none |
