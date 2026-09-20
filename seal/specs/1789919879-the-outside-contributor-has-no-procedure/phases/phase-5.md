# 1789919879-the-outside-contributor-has-no-procedure — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 41e73f55 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The fragments this work item owes: `seal/specs/<id>/changelog.md` and
`seal/ledger/<id>.md`, verified by
`python3 .github/scripts/gather_changelog.py --check` and by
`python3 skills/evidence-check/scripts/evidence_check.py .` resolving the new
rows.

## What this phase found

### This branch drifted three rows of `seal/ledger.md`, and neither the plan nor the phase's own verification command was looking for it

`evidence_check.py .` reported two DRIFTED coordinates before a single new row
was written:

```
DRIFTED  .github/workflows/hygiene.yml#"- name: a change to what ships must move the version"  content changed at 58-98 — re-verify
DRIFTED  tests/test_docs_line_wrap.py#COVERED  content changed at 49-104 — re-verify
```

Three rows cite them, and both coordinates are units this branch edited —
phase 2's message and phase 3's `COVERED` entry. `CLAUDE.md` §*House rules*
gives two answers, and which applies is about the claim rather than the code:
re-verify where the claim still holds and has been re-read, remove the row and
write the new claim into this work item's fragment where the claim went with
the code.

**Established first that the branch caused them.** A pre-existing drift is a
different fact and would have been somebody else's. Each coordinate's hash was
recomputed at the base with the checker's own `resolve` and `content_hash`
over `git show origin/release/v0.12.1:<file>`:

| Coordinate | recorded | at base | now |
|---|---|---|---|
| `hygiene.yml#"- name: a change to what ships…"` | `2b250a60` | `2b250a60` | `a9eefea8` |
| `test_docs_line_wrap.py#COVERED` | `b9362cc3` | `b9362cc3` | `a46b388e` |

Clean at the base, drifted here. All three claims survive the edits — the
`bin/` claim is about the step's **pattern**, which phase 2 did not touch, and
the two `COVERED` claims are about eleven modules and two documented prose
maxima, neither of which an added list entry changes. So: re-verify, which is
the explicit *I have re-read these*.

**`--reverify` was the right command and the dangerous one, so the order
mattered.** It rewrites the hash of every **resolvable** row, and the tree held
two drifted coordinates at the moment of running. Had either been somebody
else's, the command would have silently re-stamped a claim nobody re-read.
Checking which rows drifted, and against what, came first; the run then
reported `3 rows re-verified` and `git diff --stat` showed `seal/ledger.md | 6
+++---`, three lines, exactly the three rows.

### The record checker refused a name in the frame's own `spec.md`

The same command's second arm, at exit 2:

```
NOT-IN-TREE  seal/specs/1789919879-…/spec.md:66  `read_body` — nothing outside
seal/specs and seal/ledger carries this name.
```

`spec.md`'s measurement table cites `read_body` as its grounds for <!-- NAME NOT IN TREE: this paragraph is the record of that retired coordinate. Round 1 🔴 1. -->
*an empty body is a body, and the only exit 2 is a step handed none*. No such
name exists in `.github/scripts/issue_claims_check.py`. **The claim holds and
only the coordinate was wrong**: `body_from` is the function that decides
whether a body was handed over, and its docstring says both halves — *An EMPTY
`PR_BODY` is a body … An ABSENT one is … the only thing here worth an exit
code.* Corrected in place, with an HTML comment recording what it was.

**The first correction attempt failed the same check**, because the comment
quoted the old name in backticks and the checker reads backticked names. The
comment now writes it bare and says why. After that: exit 0, `1368 ok · 0
drifted · 0 broken`, `0 refused`.

### `gather_changelog.py --check` exits 1 here, and that is the pass

It lists this work item's fragment as ungathered. On a feature branch every
fragment is legitimately ungathered — the hygiene step that runs this command
returns early unless the base is `main`, which is the same guard the exemption
list phase 1 wrote rests on. Reading exit 1 as a failure here would be reading
a release's check on a branch that is not one. Recorded so the next reader of
`plan.md`'s phase 5 row does not have to re-derive it.

### The closing memo, which `plan.md` did not list

`plan.md` names two fragments for this phase and no `overview.md`.
`skills/implement/SKILL.md` §4 opens one at the first divergence or unverified
item, and this work item has three of each, so it is written here rather than
left out because a table did not name it. `unverified-check --baseline
origin/release/v0.12.1` reads it: `3 open · 0 closed`, exit 0.

### Executed in this phase

| Command | Result |
|---|---|
| `python3 skills/evidence-check/scripts/evidence_check.py .` (before) | exit 1 lenient — 2 drifted, both caused by this branch |
| `bin/evidence-check --reverify .` | `3 rows re-verified`; `seal/ledger.md` 3 lines changed |
| `python3 skills/evidence-check/scripts/evidence_check.py .` (after) | **exit 0** — `1368 ok · 0 drifted · 0 broken · 0 external`, and the 4 coordinates of this work item's own fragment among them. **True when it was run, and false one commit later**: this table and the two paragraphs above it were themselves written with the retired name in backticks, which is the state round 1's 🔴 1 found at `c0b00d08`. The run was taken; the tree moved under it. The three lines now carry the marker |
| `python3 .github/scripts/gather_changelog.py --check` | exit 1, naming this work item's fragment — the correct state for a feature branch |
| `python3 skills/verify/scripts/unverified_check.py --baseline origin/release/v0.12.1` | exit 0 — `3 open · 0 closed` for this work item |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The three stale hashes in `seal/ledger.md` — `2b250a60` and two of `b9362cc3` | Replaced in place by `a9eefea8` and `a46b388e`. The rows are unchanged otherwise: each claim still holds and was re-read, which is what `--reverify` asserts. Nothing moved to this work item's fragment, because no claim went with the code |
| The frame's `read_body` coordinate in `spec.md` | Corrected to `body_from` in the same row, with an HTML comment holding what it was and why. `overview.md` §*Fed back into the spec* carries it as a correction a planner may overturn <!-- NAME NOT IN TREE: the removed item IS the retired coordinate. Round 1 🔴 1. --> |
