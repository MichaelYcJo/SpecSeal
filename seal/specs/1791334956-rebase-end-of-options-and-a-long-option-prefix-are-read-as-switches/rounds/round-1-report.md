# Round 1 report — 1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches

| Field | Value |
|---|---|
| Target SHA | 71e4b3a3496bb9d3505692fc569852aa0d43c172 |
| Range under review | `origin/release/v0.20.0...HEAD`, base `3d78c220` (7 commits) |
| Pull request | #855 (draft) |
| Round kind | first round of the work item |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

The fix closes the class it was framed for. Every way git 2.50.1 ends a
rebase's options, and every prefix of `--root` it accepts, now stops in an
ACTIVE tree wherever git switches HEAD (executed). The three findings of
round 3 of work item 1791270162 that framed this item are closed. The new
cases go red at the base, and the ledger re-stamps change hashes and nothing
else.

What remains sits beside the class, not inside it, in cause order:

1. **bash can still hand git words the guard never reads (🟡 1, deferred).**
   Brace expansion is a shell spelling, not a git one. `git rebase
   {main,feature/x}` and `git rebase --ro{,} feature/x` each switch HEAD
   under bash and are silent in an ACTIVE tree, at the build and at the base
   alike. The same gap reaches `stash` and `worktree` (read), so it belongs
   to the whole guard and not to this work item.
2. **Two sentences of this branch claim more than the code reads.** The
   docstring of `_rebase_names_a_branch` and ledger row R1 say `--root` is
   read "off the words bash hands git". The code reads the words once their
   redirections are off, which item 1 shows is narrower (⬜ 2).
3. **The changelog fragment promises that every other option passes (⬜ 3).**
   A one-word rebase with an option that takes a value stops: `git rebase -X
   theirs main` is denied in an ACTIVE tree (executed). That cost is #826's
   by design, and the sentence hides it from the person reading the release
   note.

Nothing here needs a fix before the run ends. Items 2 and 3 are wording
corrections.

## Does the fix close the class?

Yes, for git's own parsing. `git rebase -h` on git 2.50.1 lists one long
option that changes how many words name a branch, `--root`, as the smith
found (read). Every other option either takes no value or has its value
counted as a word, and the guard drops only a word that starts with `-`.

So the guard can count fewer words than git only where git reads a `-` word
as a revision. That happens after the first `--` or `--end-of-options` that
is not an option's value, and for a lone `-`. The guard ends at the first of
those words even where git takes it as a value (`git rebase -x -- …`). That
can only make the guard count more words than git, and a word after the end
that git reads as `--root` is then counted as a word instead of lowering the
threshold, which comes to the same answer.

Executed in a deleted probe: each command ran under bash against git 2.50.1
in a copy of the `repo` fixture with a second commit on `feature/x` and a
branch `-x`, and through the build's and the base's `main()` in an ACTIVE
tree.

| Command | git | HEAD after | Build | Base |
|---|---|---|---|---|
| `git rebase --end-of-options main feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase --root --end-of-options feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase --ro --end-of-options feature/x` | 0 | `feature/x` | deny | silent |
| `git rebase --no-root --root feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase --root --no-root feature/x` | 0 | `main` | deny | deny |
| `git rebase --no-ro feature/x` | 0 | `main` | silent | silent |
| `git rebase --onto main --ro feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase -x true --ro feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase -x -- --ro feature/x` | 1 | detached, mid-rebase | deny | deny |
| `git rebase -x --end-of-options --ro feature/x` | 1 | detached, mid-rebase | deny | silent |
| `git rebase --exec=true --ro feature/x` | 0 | `feature/x` | deny | silent |
| `git rebase -iq main feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase -i -r main feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase main feature/x -i` | 0 | `feature/x` | deny | deny |
| `git rebase --keep-base main feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase --onto=main main feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase --ro 2>/dev/null feature/x` | 0 | `feature/x` | deny | silent |
| `git rebase --end-of-options>/dev/null main -x` | 0 | `-x` | deny | silent |
| `git rebase "--ro" feature/x` | 0 | `feature/x` | deny | silent |
| `git rebase --r\oot feature/x` | 0 | `feature/x` | deny | deny |
| `git rebase -- -x` | 0 | `main` | silent | silent |
| `git rebase --end-of-options -x` | 0 | `main` | silent | silent |
| `git rebase --root=x feature/x` | 129 | `main` | silent | silent |
| `git rebase -- --root main` | 128 | `main` | deny | deny |
| `git rebase -X theirs main` | 0 | `main` | deny | deny |
| `git rebase -s ort main` | 0 | `main` | deny | deny |
| `git rebase -ix true main` | 0 | `main` | deny | deny |
| `git rebase {main,feature/x}` | 0 | `feature/x` | **silent** | silent |
| `git rebase --ro{,} feature/x` | 0 | `feature/x` | **silent** | silent |

Every row where HEAD moved denies at the build, except the two brace rows,
which are 🟡 1. Two exec rows exit 1 with HEAD detached mid-rebase. Why the
exec step failed was not investigated; git had already left `main` by then,
which is the only thing the row measures. A short-option cluster changes nothing, since no
short option of `rebase` stands for `--root` and a cluster's value is either
glued on or counted.

The other direction holds too. Every row this branch moved from silent to
deny is one where git moved HEAD. The deny rows with HEAD unmoved (`-X
theirs`, `-s ort`, `-ix true`, `--root --no-root`) deny at the base as well.
They are #826's documented cost of reading without an option table.

## Is the git-binding case portable?

On the gits that have run it, yes. The case makes a branch `-x` with `git
update-ref refs/heads/-x HEAD`, passes every word to git as a list with no
shell, and reads HEAD from `.git/HEAD`. A ref file named `-x` needs nothing a
Windows or a case-insensitive file system refuses, and `update-ref` checks no
leading dash, which only `check-ref-format --branch` does.

Executed in this round: the case passes here under git 2.50.1. Read from CI
at 71e4b3a3: it passed under git 2.55.0 on Ubuntu and macOS and under git
2.55.0.windows.5 on Windows (the CI section below).

## Are the re-stamps of 1791270162's fragment faithful?

Yes. A word diff of the fragment between `3d78c220` and the head changes
anchor hashes and nothing else: ten rows, no claim, evidence, date or note
cell (executed). `bin/evidence-check --strict --ledger` on that fragment
passed at the base with the old hashes (127 ok) and passes at the head with
the new ones (127 ok), so each old hash was the base's content and each new
one is the head's (executed).

Each claim still holds at the new content (read). F3's threshold is now
short of the two new spellings but not false, and R1 carries them. K6's
Known limits bullet gained two examples of the same fallback. F8's "one tree
reads as this tree" is now what §A says outright. Re-stamping a fragment's
row in place is the documented mechanism (`docs/the-evidence-ledger.md`
§*A citation that does not hold is named*).

The released rows citing the guard's Known limits at older hashes (in
`seal/releases/0.17.0.md`, `0.18.0.md`, `0.18.2.md` and `0.18.3.md`) and the
broad-gate fragment each pass `evidence-check --strict --ledger` at the head
(executed), and CI's `ledger` leg passed.

## Round 3's findings of 1791270162, answered

| Round 3 | What this branch does | Answer |
|---|---|---|
| finding 1, `--ro` and `--end-of-options` listed | the end set gains `--end-of-options`; `--root` is read by prefix from `--ro`, off the plain words | Closed. Executed in the table above, and the new rebase and git-binding rows are red at `3d78c220` |
| note 2, one-tree reason | §A says a one-tree reason calls its tree "this tree"; a behaviour case pins it | Closed. Read, and the policy pin is red at the base (executed) |
| note 3, two spellings reach the fallback | §Known limits names both; two `UNPLACED` rows pin the silence | Closed. Read, and the policy pin is red at the base (executed) |
| note 4, round 2's red glyph | not this branch's; it lifted when round 3's record landed | `release` passed at 71e4b3a3 |

The divergence from round 3's paste-ready fix holds. The smith reads the
prefix from `--ro`, not `--r`, and git 2.50.1 refuses `--r` as ambiguous
(exit 129), so the build reads what git reads.

## 🟡 1 — Brace expansion hands git words the guard never reads

**Where.** `hooks/worktree-guard.py:2250`, `_rebase_names_a_branch`, and
every reader in the guard that takes a word as bash hands it.

**What is wrong.** bash expands `{main,feature/x}` into two words and
`--ro{,}` into `--ro --ro` before git runs. The guard reads each as one word
that is neither an option prefix nor two revisions, so the rebase stays
listed.

**Why it matters.** Both commands switch HEAD under git 2.50.1 and are
silent in an ACTIVE tree (executed, table above), which is what the Premise
exists to stop. The weight is low. Nobody writes these spellings by habit,
and the base was silent on both, so this is not a regression.

The gap is not rebase's alone. `git stash {branch,} y` reaches bash as `git
stash branch y`, and the guard's `stash` test compares the first word with
`branch`, so it would stay listed (read, not executed). The same holds for
`worktree {add,} …`. A fix belongs in the guard's word reading, not in this
function, so it is out of this work item's frame (`spec.md` In 1: ways git
stops reading options or reads a short spelling of one).

**Fix, for the issue it goes to.** Read a word carrying an unquoted brace
expansion as an unrecognised shape, as the guard already does for a word
the frozen reading cannot read.

## ⬜ 2 — "Off the words bash hands git" says more than the code reads

`hooks/worktree-guard.py:2246`, in the docstring of
`_rebase_names_a_branch`, and the same phrase in ledger row R1. The code
reads the words through `_plain_words`, whose own docstring says what that
is: the words once their redirections are off. The phrase is right for
`--root>/dev/null` and wrong for `--ro{,}` (🟡 1). The behaviour is
unchanged by rewording. Say the narrower thing.

## ⬜ 3 — The changelog says every other option passes

`seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/changelog.md:12`.
"A rebase of the branch HEAD is on still passes, and so do `--rebase-merges`
and every other option." An option that takes a value is counted as a word,
so `git rebase -X theirs main`, `git rebase -s ort main` and `git rebase -x
'make test' main` stop where a switch would matter (executed for the first
two and for `-ix true main`). The cost is #826's documented choice, so the
behaviour is right and the release note is not. This is the run's paperwork,
a correction.

## Regression tests to plant

| Finding | Destination | What it asserts |
|---|---|---|
| 🟡 1 | the issue it is deferred to; `tests/test_worktree_guard.py`, `test_a_rebase_naming_a_branch_is_unrecognised` and the `SWITCHING` tuple, once the guard reads brace expansion | `git rebase {main,feature/x}` and `git rebase --ro{,} feature/x` stop. Red at 71e4b3a3 (executed: silent in an ACTIVE tree) |

## Facts for the evidence ledger

- git 2.50.1 takes `--root` from `--ro` anywhere before the first `--` or
  `--end-of-options` that is not an option's value; `git rebase -x
  --end-of-options --ro feature/x` and `git rebase --exec=true --ro
  feature/x` switch to `feature/x` (executed in this round).
- bash hands git `git rebase main feature/x` for `git rebase
  {main,feature/x}`, and git switches to `feature/x` (executed).
- CI ran git 2.55.0 on Ubuntu and macOS and git 2.55.0.windows.5 on
  Windows at 71e4b3a3, and the git-binding case, with its branch `-x` made
  by `update-ref`, passed on each (read from the job logs).

## CI at 71e4b3a3

Every workflow of #855 passed at 71e4b3a3, read until the last leg ended:
`lint`, `ledger`, both `arm-check-grammar` legs, `release`, and `pytest` on
Ubuntu, macOS and all four Windows shards. None is red, pending or missing.

The git-binding case ran on three gits besides this round's 2.50.1. Ubuntu
and macOS ran git 2.55.0 and the Windows shards git 2.55.0.windows.5 (read
from the job logs). The case sat on Windows shard 4 (job 112583961187) at
16.46 s, against a 90 s ceiling. Round 3 measured it at 7.41 s on a Windows
shard before the three new forms. Three more repository copies do not
account for that much, so runner variance probably does, but no run here
separates the two (not measured).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | brace expansion hands git words the guard reads as one: `git rebase {main,feature/x}` and `git rebase --ro{,} feature/x` switch HEAD and are silent in an ACTIVE tree | `hooks/worktree-guard.py:2250` | deferred a new issue | executed under git 2.50.1 and bash; silent at the base too, so not a regression; the same gap reaches `stash` and `worktree` (read), so the fix is the guard's word reading and outside this item's frame |
| ⬜ 2 | the docstring and R1 say `--root` is read off the words bash hands git, and the code reads them only once redirections are off | `hooks/worktree-guard.py:2246` | open | read; the phrase is false for a brace-expanded word (finding 1); wording only |
| ⬜ 3 | the changelog fragment says every other option passes, and a one-word rebase with an option taking a value stops | `seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/changelog.md:12` | open | executed: `-X theirs main`, `-s ort main` and `-ix true main` deny in an ACTIVE tree, as at the base; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 3's finding 1 of work item 1791270162 is closed — `--end-of-options` and every prefix of `--root` git accepts are read | `hooks/worktree-guard.py:2257` | confirmed | executed: 29 spellings under git 2.50.1, every switch denies but the two brace rows; the new rebase rows and the git-binding case red at `3d78c220`, green here |
| 🟢 | round 3's note 2 of work item 1791270162 is closed — §A says a one-tree reason calls its tree "this tree" | `docs/worktree-guard-spec.md:102` | confirmed | read; the policy pin red at `3d78c220` (executed) |
| 🟢 | round 3's note 3 of work item 1791270162 is closed — §Known limits names `cd w 2>&1` and a cut git in an `if` body | `docs/worktree-guard-spec.md:807` | confirmed | read; the policy pin red at `3d78c220` (executed) |
| 🟢 | the in-place re-stamps of 1791270162's fragment change hashes only, and each claim holds at the new content | `seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md` | confirmed | executed: word diff shows hashes only; `evidence-check --strict --ledger` 127 ok at the base and at the head; read: each claim against the changed text |
| 🟢 | the git-binding case's new forms run on the CI gits | `tests/test_worktree_guard.py:2008` | confirmed | read from CI at 71e4b3a3: passed on Ubuntu and macOS (git 2.55.0) and on Windows (git 2.55.0.windows.5, shard 4, 16.46 s against a 90 s ceiling); passes here under git 2.50.1 (executed) |
| 🟢 | every workflow of #855 at 71e4b3a3 passed | `gh pr checks 855` | confirmed | read: `lint`, `ledger`, both `arm-check-grammar` legs, `release`, Ubuntu, macOS and Windows shards 1 to 4 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_docs_line_wrap.py -q --durations=5` in this round's clone at 71e4b3a3 | 288 passed in 7.32 s; `test_no_listed_form_moves_head_under_git` 3.04 s |
| the head's two guard test modules copied into a clone at `3d78c220`, then `bin/test … -k "rebase or listed_form or one_tree_reason or guard_policy_says or cannot_place"` | 8 failed, 36 passed: the five new switching rebase rows, the git-binding case naming exactly `rebase --end-of-options {start} -x` and `rebase --ro feature/x`, and both policy pins. The new listed rows, the one-tree case and the two `UNPLACED` rows pass at the base, as they pin behaviour the base already had; the smith showed each red through `bin/mutation-check` (not rerun here) |
| a deleted probe running 29 rebase spellings under bash and git 2.50.1 in copies of the `repo` fixture, and through the build's and the base's `main()` in an ACTIVE tree | the class table above |
| `bin/evidence-check --strict --ledger <file> .` on 1791270162's fragment and this item's at the head, on 1791270162's at `3d78c220`, and on `seal/releases/0.17.0.md`, `0.18.0.md`, `0.18.2.md`, `0.18.3.md` and the broad-gate fragment at the head | every run exit 0, 0 drifted, 0 broken |
| `git diff --word-diff=porcelain 3d78c220 71e4b3a3` of 1791270162's fragment | hash tokens only |
| `gh pr checks 855` until every leg ended, and the logs of the Ubuntu, macOS and four Windows `pytest` jobs (`gh api …/actions/jobs/<id>/logs`) | every leg passed; git versions and the case's 16.46 s on Windows shard 4, in the CI section above |
| this report copied into the scratch clone, then `bin/evidence-check --strict --ledger` on this item's fragment, `bin/test tests/test_no_real_identifiers.py -q`, and `round_record.py new` with the report as its input | exit 0, nothing refused; 5 passed; the record parsed, with `Needs a fix` and `Loses a record or crashes` both `no`. The clone, and the record written in it, were deleted |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. This report opens nothing that needs a fix, so it comes due now |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — brace expansion hands git words the guard reads as one, in `rebase`, `stash` and `worktree` alike | candidate home: a new issue against the worktree guard's word reading | the orchestrator opens it, and the repository owner decides whether the guard reads brace expansion or names it in §*Known limits* |

## Paste-ready fixes

### ⬜ 2

```python
# hooks/worktree-guard.py, _rebase_names_a_branch, the docstring's third
# paragraph, from "refuses it." on:
    refuses it. `--root` is the one option of `git rebase -h` that changes how
    many words name a branch, and it is read off the words once their
    redirections are off, so `--root>/dev/null` is `--root` too. An option
    taking a value counts its value as a word, as above (git 2.50.1; #854,
    round 3 of work item 1791270162, yellow 1)."""
```

```markdown
seal/ledger/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches.md,
row R1's claim: "off the words bash hands git" becomes
"off the words once their redirections are off"
```

### ⬜ 3

```markdown
seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/changelog.md,
the paragraph's last sentence becomes:

  A rebase of the branch HEAD is on still passes, and so does one carrying
  `--rebase-merges` or another option that takes no value.
```

Needs a fix: no

Loses a record or crashes: no

## Proof

Files opened in this round, in the round's clone at 71e4b3a3 unless named:

- the work item's `routing.md`, `spec.md`, `plan.md`, `overview.md`,
  `changelog.md` and `phases/phase-1.md`
- `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-3-report.md`
- `git diff origin/release/v0.20.0...HEAD` in full: `hooks/worktree-guard.py`,
  `docs/worktree-guard-spec.md`, both ledger fragments,
  `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py`
- `hooks/worktree-guard.py`: 2150–2300
- `docs/worktree-guard-spec.md`: 36–112, 785–820
- `docs/the-evidence-ledger.md`: 110–154
- `tests/test_worktree_guard.py`: 1095–1150, 1815–2110
- `tests/conftest.py`: 543–565, 820–850
- `bin/test`; `bin/evidence-check --help`
- `git rebase -h` under git 2.50.1
- `gh pr checks 855`, `gh pr view 855`, and the CI job logs named above
- the reviewer's instructions: the agent contract, `code-review`, and the
  writing-style skill
