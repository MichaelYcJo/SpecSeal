# 1789956662-the-gate-and-ci-ask-about-different-ranges — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b0b09908 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The resolver, as a function in `broad_gate.py`: `(given spelling, resolved
ref, resolved commit)`, with the three-step rule and the fallback. Nothing in
`gate()` uses it yet. New cases for A8, A9, A12 and both halves of the rule,
each seen red against the function's absence, plus a fixture builder that can
give a repository a remote and move it.

## What this phase found

**The cases live in a new module, and that is what makes A3 checkable by
reading.** `spec.md` A3 asks that
`tests/test_the_seal_is_taken_once_by_the_sealer.py` stay green with nothing
edited inside it. A new case added there would satisfy the words and destroy
the evidence: a reader could no longer tell an untouched module from one that
was adjusted until it passed. The new module is
`tests/test_the_gate_asks_the_range_ci_will_ask.py`, and A3 is then
`git diff --name-only` over the branch not naming the old one.

**The fixture builds its remote by cloning a non-bare repository, not by
pushing into a bare one.** A clone gives the local `base` an upstream for
free, which is the rule's first step; moving the remote is then a commit in
the upstream followed by `git fetch` in the clone, and a fetch — never a
pull — is what leaves the two refs naming different commits in one checkout.
That is the state 2026-09-16 was found in, reproduced in about ten lines.

**A base that resolves nowhere comes back from the resolver with no commit
rather than as an exception.** A10 asks that the refusal still quote the
spelling the caller typed, and a resolver that raised would either have to
carry `gate()`'s message or lose the given spelling. So `Base.commit` is
`None` there and `gate()` keeps its own refusal, which is also what lets
phase 2 read `args.base` exactly once.

**`moved` is true for a base that names no local commit at all**, not only
for one that is behind. A clone that never made a local branch for its base
is an ordinary checkout — and on the reading where `moved` meant *behind*,
that case would resolve silently, which is the defect this work item is
about. `given_commit` being `None` differs from the resolved commit, so the
property falls out of the comparison rather than needing a branch. What it
costs is that phase 3's printed line has two fillings rather than one.

**The upstream step and the `origin/` step agree in every ordinary
checkout**, so deleting the upstream step alone turns exactly one case red —
the second-remote case written for it. That is the whole of what the order
buys, and it is why `plan.md` §*Alternatives considered* argues it from the
fork case rather than from the common one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds a unit and a module and takes nothing out of the tree | none |
