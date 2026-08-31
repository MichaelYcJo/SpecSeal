---
name: verify
description: |
  Evidence protocol for completion claims (the Seal Test): name the proving
  command before running it, show the check can fail, bind the result to a
  tree state, and label every claim executed / read / unverified.
  Use when: about to say done, fixed, passes, or complete; before a commit;
  before handing work to the review chain.
  NOT for: deciding whether the work is worth doing, or reviewing someone
  else's diff (`code-review`).
---

# verify — the smith's own gate before handoff

A completion claim is a mark, and a mark must be *earned*. The community
baseline ("no completion claims without fresh verification evidence") stops
at freshness — it accepts any green command as proof. This protocol demands
more: **a check that cannot fail proves nothing, and evidence that outlives
its tree state proves less than nothing.**

A claim is sealed only when all four conditions hold:

## The four conditions

### 1. Named before run

State the proving command **before** executing it, next to the claim it
proves. Choosing the command after seeing what passes is how a test suite's
green becomes "feature works" — the claim-to-command mapping is the
verification, the run is just its execution.

### 2. Able to fail

Show the check CAN go red. For a bug fix: the reproduction failed before the
change (or fails when the change is reverted). For a new test: it was
observed failing against the pre-change code. A check that has never been
seen red is a counterfeit seal — this is the condition the generic gates
skip, and the one that catches assertion-free tests, mocked-away behavior,
and wrong-file test runs.

#### An absence claim is only as good as the search behind it

"There are no callers", "the original has no such branch", "nothing reads
this column" — these are claims about the whole tree, and their entire
evidence is that one search did not find something. An existence claim comes
with a coordinate anyone can open; an absence claim comes with nothing to
open, so the cost of checking it is asymmetric and it tends to pass unread.

Condition 2 applies to the search itself: **run it against a case you know is
present.** A pattern that finds nothing there was broken, not the tree empty.
Report the command and the scope it ran over, so the next session re-runs it
instead of re-inventing it.

An absence you cannot demonstrate that way is `unverified` and reads "not
found", which is a different sentence from "not there". Never promote one to
a document — a policy or a ledger row built on a search nobody could repeat
is the same defect as a `read` reported as passing, with a longer fuse.

### 3. Bound to the tree

Evidence attaches to a tree state, not to a session. Note the state the
proof ran against (commit + dirty files); **any edit after the run breaks
the seal** — re-run, don't re-tell. Same drift logic the evidence ledger
applies to spec coordinates, applied to your own claims.

### 4. Executed, read, or unverified — labeled

Every claim carries one label. `executed` (ran it, read full output, exit
code checked) · `read` (inferred from reading code — a judgment, not proof)
· `unverified` (say who or what can answer). Reporting a `read` as passing
is the lie this whole skill exists to prevent.

## Procedure

1. List the claims this response is about to make.
2. For each, name the proving command (condition 1). No command exists →
   label `read` or `unverified`, never "should work".
3. Run fresh; read the FULL output; record exit code and the line that
   proves or refutes (conditions 2–3).
4. Any claim red or unproven → report the actual state. The seal is
   withheld, not negotiated.

## Scope — cheap and often, broad and once

Condition 3 decides where a broad check belongs. Evidence binds to a tree
state, so **any run followed by an edit was spent, not banked**. Measured on
one work item here: twenty broad runs, every one of them followed by more
edits — 121 after the first, 1 after the last. Not one of those seals survived
to the handoff, and they cost more than half the session's tool time.

Review rounds are edits you have already scheduled. Sealing the whole suite
before them seals a tree that is going to change.

| When | What runs | Seal |
|---|---|---|
| Each slice | the tests for what you just wrote | `executed`, narrow |
| Phase boundary | your module and the ones it touches, in parallel | `executed`, scoped |
| Handoff to review | nothing broad | the suite is `unverified`, and says so |
| Review rounds 1..n | what the fix touches | `executed`, narrow |
| **After the rounds settle** | full suite, lint, typecheck — **once** | the one broad seal |

Narrowing is not permission to go quiet. A suite you did not run is
`unverified` with who answers it, never omitted — condition 4 is what makes
the smaller scope honest rather than a loophole.

The two ways that loophole reopens are below. Both were measured, and both
looked like a sealed claim at the time.

### The narrow command still has to be able to fail

Condition 2 does not relax when the scope shrinks. A smaller command is still
a command being chosen, and it is easier to choose wrong — it can come back
green because it examined nothing.

Measured: a documentation-only change was sealed with a Python linter aimed at
the docs directory. That directory holds no Python.

```
$ ruff check docs/
warning: No Python files found under the given path(s)
All checks passed!                                        (exit 0)
```

Exit 0, nothing read, and a green line in the seal block. Before a narrow
command counts, say which files it opened. If the answer is none, the honest
row is `unverified`, not a passing one.

What can fail depends on what changed, which is the axis worth picking the
command from:

| What changed | What can fail |
|---|---|
| Prose only — docs, comments, docstrings | Whatever actually parses those files. Often nothing does, and then there is no seal to earn here. |
| A comment or docstring inside source | That the module still imports. |
| Logic | The tests covering that file. |
| A merge, or a dependency bump | The broad gate. What breaks is outside what you edited, so a scope drawn around your own edit cannot see it. |

The last row is the one that gets narrowed by mistake. A merge is the moment
the tree stops being the one you tested.

### The answerer has to exist

`unverified; CI covers it` satisfies condition 4 on its face and voids it
underneath. The row names an answerer; nothing ever checked there was one.

Measured: a session narrowed to a single domain's tests and deferred the rest
to CI. That repository's workflows assigned reviewers, deployed on push to the
default branch, and validated a migration graph. None of them ran the suite,
the default branch had no protection, and the pre-commit hooks were lint and
typecheck — on the committer's machine. The deferred suite had no answerer at
all, and the seal read as though it did.

Resolve the answerer before writing the row:

```
deferral-check .              # is the test suite answered here?
deferral-check . --kind all   # tests, lint, typecheck
```

It separates four outcomes that a reader otherwise collapses into one:
something answers on pull requests · something answers, but only after the
point being deferred · a local hook answers on the committer's machine only ·
nothing answers. Exit 1 means the row you were about to write is not true.

It reads command text rather than a YAML graph, so a runner reached through a
composite action, a reusable workflow, or a script it cannot see reads as
absent. Disagreement with what CI really does is a finding about this tool —
not permission to keep the row.

### And something has to read the row afterwards

An answerer that exists still answers nothing if nobody returns to the row. One
here said the gates had never been seen rendering in a TUI and named the user;
months later the user hit exactly that and asked why every gate is yes/no.

```
unverified-check .                              # what is still open, and where
unverified-check --baseline origin/main specs/  # and nothing was deleted from it
```

It never fails for an open item — punishing an honest row is how sessions learn
to write none. It fails for a section it cannot read, because a tolerant reader
reports zero there and zero reads as "everything has been closed". Close an
item by marking it `✅` with what closed it; the row stays.

## The broad gate — after the rounds, then compare against the base

**It fires after the review rounds settle, never before them.** Nothing broad
runs at the handoff to review; the proof block carries the suite as
`unverified`, and that label is what keeps the narrow scope honest. §Scope
holds the reason and the measurement — a seal taken before the rounds is spent
by the first finding. Findings are the expected case rather than the
exception: the review chain runs up to three rounds, and five while a 🔴 is
open (`docs/review-chain-spec.md`).

**An expensive suite argues for this placement, not against it.** A run that
takes fifteen minutes is a finding about the run and deserves its own ticket.
Moving it ahead of the rounds means paying it twice.

A full suite carries failures that were already there. Attributing them to
this work is a wrong finding; passing over them is a silent pass. Both are
avoided the same way: read the run against the base commit.

**That comparison is reactive.** A baseline answers whose failure this is, so
it is taken once an unexplained failure appears, and only for the tests that
failed — `git stash`, that one file, `git stash pop`. Measured: a session ran a
19,000-test suite serially for a baseline before any failure existed, and was
about to run it a second time after the change.

- **Failing on base too** — not this work's finding. Name it, record it as a
  follow-up, and it does not block.
- **New** — this work broke it. Back to the implement/review loop, and the
  broad gate runs again afterwards.

Measured on one repository: a full suite showed ten failures, all ten
reproducing on the base commit and none of them in the domain being changed.
Without the comparison, every one of them is triage the author cannot act on
and is not allowed to fix.

**Three returns and stop.** This counts trips through the gate, not the
review chain's rounds. A fourth trip is not another bug; it means the narrow
scope is missing a class of breakage, which is an architecture question for
the user — the same reading as the 3+ Fix Rule.

**It does not take the review rounds' exception**, and the difference is worth
stating because the numbers look alike. `docs/review-chain-spec.md` raises the
round cap to five while a 🔴 is open, on the grounds that a round catching a
regression the last fix made — coordinate named, patch already run — is not
the shape the cap was written for. Every return through THIS gate is that
shape: a broad gate goes red because something the fix touched broke. Raising
the cap for the regression case would raise it for the normal case, which is
the one thing it exists to bound.

**Nothing edits between the broad seal and the PR.** The tree that passed is
the tree that ships. One more small fix after the run means the run is stale,
and the gate is paid for again.

## The cost of the run you repeat

Scope decides how often the expensive command fires. It does nothing about
what the command costs, and the narrow run is the one that multiplies — every
slice, every round.

Measure before accepting it. The suspect is usually wrong: one session blamed
SQL echo logging for a slow suite, turned it off, and measured 131s → 137s.
What it actually found was the suite running serially while a parallel runner
sat installed and unused, its recipe written in a `pyproject.toml` comment
with the measured numbers beside it (225s → 83s). A recipe in a comment is not
a recipe. Nobody runs it, and an agent least of all.

So before paying a check's cost repeatedly, spend a minute on where the time
goes, and look for the fast path the project already has: a runner in the
lockfile, a target in the Makefile that is not the default, a line in a README
or a comment. Repairing one is cheaper than paying its absence once per round.

**Capture once, filter locally.** A command re-run to see its output a
different way returns nothing you did not already have. Measured in one
session: the same test scope ran at 194s piped through `tail`, then again at
203s piped through `grep "^FAILED"` — three and a half minutes for a different
view of a result already produced. Redirect to a file and read the file:

```
uv run pytest <scope> > /tmp/run.txt 2>&1; tail -8 /tmp/run.txt
grep '^FAILED' /tmp/run.txt          # same run, second question
```

The tell is a second invocation whose only difference is after the pipe.

`session-cost` reads a finished transcript and reports the split — command
time, model time between calls, the repeats, and how many tools went out per
turn. It is what fills the `cost` row, since none of it is visible from
inside:

```
session-cost --latest          # newest transcript for this repo
session-cost <transcript.jsonl>
```

## Seal block

End with this block. Values that cannot be filled honestly stay `none —
<reason>` (an unfillable row is a finding, not an embarrassment):

```
🔏 verify sealed @ <commit-ish>[+dirty: <files>]
· <claim> — <command> → <key output line> (exit <n>)  [executed]
· <claim> — <where read, file:line>                   [read]
· <claim> — unverified; <who/what answers>            [unverified]
· broad gate: <not yet — due after the rounds settle | ran at <sha> vs base <sha>>
· cost: <n> check runs, <m> minutes of command time
· red proven: <how the check was seen failing, or none — <reason>>
```

The `cost` row is there because nobody notices this from inside. One session
spent 22 of its 26 command-minutes in the test runner across fourteen runs,
and that only surfaced when someone parsed the transcript afterwards —
`session-cost` is that parse, made repeatable. A number
in the report puts it in front of the person who can decide the suite is worth
fixing — the same reason `none — <reason>` is written rather than omitted.

The `broad gate` row is what makes "once" survive a handoff. A session picking
up round 3 watched neither round before it, and no command leaves a trace in
the code it ran against — so it either repeats a run that is already sealed or
ships assuming somebody else made it. It belongs in `round-N.md` too, where
the next session actually looks.

The block feeds forward: the smith ends reports with it, the warden audits
the seal instead of re-deriving it, and `.specseal/` handoffs carry it across
sessions. A seal the warden cannot audit from the block alone was not a
seal.

## Counterfeits (stop on sight)

- Output quoted from an earlier run — freshness is per tree state, not per
  conversation.
- "Tests pass" for a claim no test covers — green suite, unproven claim.
- Satisfaction vocabulary before the run: should, probably, seems, likely.
- A new test that passed on first run and was never seen red (condition 2).
- Partial evidence generalized — one endpoint checked, "API works" claimed.
- A broad run reported as the seal when edits followed it — including the
  one small fix made after it.
- A pre-existing failure counted as this work's, or waved past without
  being named. Both need the base comparison; neither survives it.
- A narrow command that was green because it opened no files — a linter
  pointed at a directory holding none of its language, a test path that
  collected zero tests. Condition 2 does not relax with the scope.
- A check that stopped before reaching the code it was aimed at — a config
  error, a collection error, two modules under one name. The run ends early
  and cheaply, and "it was fast" reads as "it was clean". It is neither a pass
  nor somebody else's problem: that axis now has no answer, and the honest row
  is `unverified` with the cause named. Measured: a `mypy .` that died in four
  seconds on duplicate modules, checked neither the source nor the tests, and
  was the direct reason eleven regressions went out.
- A failure count with no base state behind it. "1 failed" is a claim about
  your change only if you know what the tree failed before you touched it.
- A deferral to an answerer nobody resolved. "CI covers it" in a repository
  where nothing runs it is the `unverified` label doing the opposite of its
  job: it reads as handled.
