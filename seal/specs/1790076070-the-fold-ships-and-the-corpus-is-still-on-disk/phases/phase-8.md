# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 8

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | 534769c0 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

**new** `docs/the-gates-a-session-meets.md` and `docs/worktree-guard-spec.md`
— the four hooks a session meets, and the worktree guard's two. Seven items:
`commit-review-gate.py`, `hooks/cmdline.py`, `implementer-notice.py` (2),
`review-history-guard.py`, `worktree-guard.py` (2).

## What this phase found

### The new document is not written, and the plan is what refuses it

`plan.md` states the one thing a phase may not change without going back to
it: **no new document for an area one already covers.** Reading the
destination before writing it shows `docs/review-chain-spec.md` already
carries a section per gate, each with its own decision table:

| Section | Line |
|---|---|
| `## commit-review-gate (PreToolUse, Bash)` | 300 |
| `### Which repository, and what happens when it cannot be read` | 336 |
| `#### A cd the gate cannot read` | 478 |
| `## review-history-guard (PostToolUse, Bash)` | 1738 |
| `## implementer-mark · implementer-notice` | 1757 |

A new document about the same four hooks would be a second home for a
subject that has one. The rule this repository already holds — a thing more
than one party can have is named with whose — is about the same failure: two
places stating one thing, and no rule saying which is right when they
disagree.

So the four items fold into the sections that hold their rules:

| Item | Marked on |
|---|---|
| `1788305134` | chain spec §*Which repository, and what happens when it cannot be read* |
| `1788310269` | chain spec §*implementer-mark · implementer-notice* |
| `1788844300` | chain spec §*review-history-guard* |
| `1788354065` | `one-root-by-lifetime.md` §*What first setup asks* |

**`1788354065` moved documents as well as phases.** Its segment is
`hooks/commit-review-gate.py`, and its scope is local mode's CREATE side and
the first-setup question — which is `one-root-by-lifetime.md`'s subject, and
where phase 6 put the rest of that story. A gate document would have held
one half of a question whose other half is three sections away.

### `1789081272` moves to phase 10

Its segment is `hooks/implementer-notice.py` and its subject is
`agents/framer.md`: the writer of a contract is not its executor. That
belongs in `docs/the-agent-set.md`, which phase 10 creates. Folding it into
a gate section would file the agent split under the hook that happens to
mark it.

### What this costs, stated rather than left to be found

**Q1's five new policy documents become four.** The owner is being asked
whether five new top-level `docs/` files is the shape the repository wants,
and this phase removes one of the five without being asked. That is the
safer direction on that question — a policy surface that grows by four
rather than five — and it is reversible: the four markers sit on named
sections, so cutting a gates document later is a move, not a rewrite.

What is given up: a reader who wants *every gate a session meets, in one
place* still has to read the chain spec, where the gates sit beside the
review chain they enforce. That was already true before this phase.

### The worktree guard's two had their sentences waiting

`1788817291` onto §*Creation consent — the first creation is the question,
not every one*, which is the rule it wrote; `1788846800` onto §*Activity:
what makes a session ACTIVE*, whose heuristics table is what it corrected.

### What was dropped rather than folded

**`1788305134`'s re-application note.** That work item re-applied a reviewed
change whose branch lost its history, and half its scope is *what the tree
already carries, verified here*. A verification of a past merge is not a
rule.

**`1788846800`'s Out clause** — the verdict ladders it deliberately did not
touch. A boundary between two tickets.

**`1788844300`'s two arms as coordinates.** The `shlex` arm and the two
index guards are the commit. What governs is what its own changelog says
about the class: a `PostToolUse` hook must not raise into the session's Bash
call, and an arm no case watches is an arm that can be deleted without
anything going red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-gates-a-session-meets.md`, which `plan.md`'s destination map names and this phase does not create | the four items' rules land in `docs/review-chain-spec.md` and `docs/one-root-by-lifetime.md`, named above. The decision itself lands in `overview.md`, under the note about Q1's count |
