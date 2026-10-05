# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 5c7cf3ca |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Measure before building, and put nothing in the tree but this record. M1:
git's truth table for every C1–C3 form of `spec.md` §*The class* under every
carrier, with real git in a scratch repository outside the worktree, and
`a3aa139a`'s `classify` verdict on each (A1). M2: whether resolve-then-peel
and the merge-base rule answer every form git moves on. M3 before-counts, both
readers, over the two corpus cuts (A12). Record that P1's default (a) was
taken by the orchestrator under the owner's `automation` routing.

## What this phase found

**P1 is not answered; its default is taken.** The orchestrator relayed at the
spawn that, under the owner's `automation` routing, the build guesses across
every remote (default (a)). `questions.md` P1 records that and stays open for
the owner, who can still answer (b) at the pull request.

**M1: the base is silent on exactly three shapes of the class, and they are
the ones the frame predicted.** Executed with git 2.54.0, by a deleted probe:
one scratch repository holding two branches with one merge base, two with two
(a criss-cross), an annotated tag, a merge commit, a reflog with a previous
branch, an upstream for `main`, and two bare remotes, `origin` and
`upstream`, holding a branch only `origin` has, one only `upstream` has and
one both have. Each form ran under each carrier in a fresh copy, through
`subprocess` with no shell, and a moved `HEAD` was read as a switch or a
detach. The base column is `a3aa139a`'s `classify` (its `hooks/` taken by
`git archive` into the scratchpad), with that repository as the tree.

The four `checkout` carriers are `checkout N`, `checkout N --`, `checkout
--detach N` and `checkout --detach N --`; the two `switch` carriers are
`switch N` and `switch --detach N`. Letters, carrier by carrier in that
order: S switches, D detaches, = stays where it is, R refused; for the base, S
is `switch` and - is `None`.

| Route and form | git | base | resolve-then-peel | merge-base rule |
|---|---|---|---|---|
| C1: a full and a short object name, a describe output, a branch, `refs/heads/<b>`, an annotated tag, `origin/main`, `upstream/<b>`, `<ref>@{<date>}`, `@{<date>}`, `<ref>@{<n>}`, `@{<n>}`, `<ref>@{upstream}`, `@{u}`, `<ref>@{push}`, `@{push}`, `<rev>^`, `<rev>^2`, `<rev>~`, `<rev>~1`, `<rev>^{commit}`, `<rev>^{}`, `<rev>^{tag}`, `<rev>^{/<text>}` | DDDDRD (a branch and `@{-1}`: SSDDSD) | SSSSSS | yes | — |
| C1: `@`, `HEAD` | ==DDRD | SSSSSS | yes | — |
| C1: `:/<text>` matching a commit, `:/!!<text>` matching a commit | DDDDRD | ----SS | **yes** | — |
| C1: `:/!-<text>` | DDDDRD | SSSSSS | yes | — |
| C1: `:/<text>` matching nothing, `<rev>^{tree}`, `<rev>:<path>` naming a blob and a tree, `:<path>`, `:0:<path>`, `<ref>@{<n>}` past the reflog | RRRRRR | ----SS | no | — |
| C2: `<a>...<b>`, `...<b>`, `<a>...`, each with one merge base | DDDDRD | ----SS | no | **yes** |
| C2: two merge bases (criss-cross), a side that names nothing | RRRRRR | ----SS | no | no |
| range: `<a>..<b>`, `<rev>^@`, `<rev>^!`, `<rev>^-1` | RRRRRR | ----SS | no | — |
| range: `^<rev>` | RRRRRR | SSSSSS | yes | — |
| C3: a branch only `origin` holds | SSRRSR | SSSSSS | — | — |
| C3: a branch only `upstream` holds | SSRRSR | ----SS | — | — |
| C3: a branch both remotes hold | RRRRRR | SSSSSS | — | — |
| C3: a name no remote holds | RRRRRR | ----SS | — | — |

So the silent shapes at the base are `:/<text>` and `:/!!<text>` (#790's own,
under every `checkout` carrier), every C2 form with one merge base, and a
branch guessed from a remote not named `origin` under `checkout N` and
`checkout N --`. Two differ from the frame's default in `questions.md` M1:

- `:/!-<text>` is not silent at the base. The `^{commit}` suffix is absorbed
  into the pattern there as well, but a negative search for a pattern that
  holds `^{commit}` matches the newest commit whatever the text, so the base
  answers yes by accident. It stays in the class and gets the resolved answer
  too.
- `^<rev>` is read as a ref at the base, although git refuses it. The OR keeps
  that answer, which is the louder direction and the base's.

Every range form is refused, and so is every form whose object is not a
commit; each keeps the base's verdict. Under `switch` every form reads as a
switch at the base already, as `spec.md` says, and git refuses most of them
without `--detach`.

The guess has refused shapes the build will ask about, and the base already
asks the `origin` half of them: `checkout --detach <name>` with or without a
trailing `--`, where git takes no guess, and a branch two remotes hold, where
git refuses as ambiguous. The base asks both for `origin`; the build asks
both for every remote. That is `spec.md` §*Out*'s case "a name git refuses but
the guard resolves", so §*Known limits* names it (phase 2).

**M2: yes, for both rules.** Resolve-then-peel answers yes on every C1 form
git moves on, `:/<text>` and `:/!!<text>` included, and no on every form git
refuses. The merge-base rule, split at the first `...` with an empty side read
as `HEAD`, answers yes on the three C2 forms git detaches on and no on the two
it refuses. `plan.md` J is built as written.

**M3 before: the class is absent from the recorded runs.** Executed by a
deleted probe over every `*.jsonl` under this repository's project directory
on the maintainer's machine: 619 transcripts (34 main), whose worktrees'
project directory holds none. Cut 1, Bash uses before
2026-10-03T11:06:22+09:00, is 25,913 uses and 25,741 distinct command and
directory pairs, the same counts work item 1791119071 read. Cut 2, every use
recorded up to the build day, is 36,423 uses and 36,199 pairs. Each pair was
replayed through `a3aa139a`'s `hooks/`:

| Reader | Cut 1 | Cut 2 |
|---|---|---|
| pairs holding a `checkout` segment the frozen walk yields | 347 (403 segments, 35 read as a switch) | 563 (647 segments, 37 read as a switch) |
| of those segments, a name holding `:/` or `...` | 0 | 0 |
| segments whose directory is gone from disk on the build day | 172 | 363 |
| pairs carrying `[worktree-ok]` anywhere, and read by `has_token` | 56, 35 read | 77, 56 read |
| pairs carrying `[shared-tree-ok]` anywhere, and read by `has_token` | 5, 1 read | 5, 1 read |

No recorded `checkout` names a message search or a merge-base shorthand, so
the syntax half of #790 moves no pair. The guess half is measured against each
pair's directory as it stands on the build day, which is the only tree there
is to read. Phase 4 replays the build over the same pairs.

The probes, their result files, the scratch repositories and the copy of
`a3aa139a`'s `hooks/` live under the session scratchpad and are deleted when
phase 4 has replayed the build.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probes lived outside it | none |
