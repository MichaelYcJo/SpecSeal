---
name: code-review
description: |
  Two-stage review methodology (spec compliance, then quality) with comparison axes,
  cross-session review records, and re-review inheritance.
  Use when: reviewing a PR or diff, re-reviewing after fixes, orchestrating reviewer agents.
  NOT for: implementing fixes (use implement), style-only linting a formatter can do.
---

# code-review — spec first, then quality

Loaded by the `code-reviewer` agent; also drives the orchestrator running a
review. The default assumption is **"this code has defects"** — try to find
them, not to prove their absence. An ungrounded LGTM is forbidden; when
uncertain, write a question, not a pass.

## Two stages, in order

1. **Spec compliance** — actual code vs. the written spec (`docs/` policies
   first, then `specs/` SDD). Look for both missing *and* unrequested extra
   behavior. Do not trust the implementer's report; read the code.
2. **Quality** — only after stage 1 passes: correctness, error handling,
   security, performance, test quality.

Review scope is not limited to changed files. New code that calls into
untouched files makes *their* query conditions and boundary operators take
effect for the first time — follow every call the change introduces.

## Comparison axes

Fix the axes before starting and cover **all** of them; picking whatever
catches the eye misses something different every time.

| Axis | Compare |
|---|---|
| Inputs | names, types, required/optional, defaults, accepted ranges |
| Authorization | who acts/queries as whom; self/admin/other branches |
| Query scope | which set is targeted: period, ownership, status filters |
| Exclusions & boundaries | excluded states, overlap conditions, **boundary values** (rarely written down — most frequent divergence point) |
| Deliberate non-exclusions | what the spec intentionally does *not* filter; new code tends to "clean it up" |
| Ordering, dedup, response shape | sort keys, tie-breaking, dedup basis, included/excluded fields |
| Error paths | failure conditions, codes, messages; failure vs. empty result. Count **new failure paths the change introduces** separately — someone must classify each as fix or regression |
| State transitions | against the spec's state machine, if one exists |

Distinguish findings from reading vs. findings from execution, always.
Something you did not run is never reported as passing.

### Probes vs. regression tests

| | What | Handling |
|---|---|---|
| Probe | Temporary test to settle what reading can't | You write it, run it, **delete it** (name `test_tmp_*`). The verified fact goes into the report |
| Regression test | Test that should exist but doesn't | **You don't write it.** Hand it over as a list with the target file per row |

Batch probe cases into one file and run once. Never probe what reading answers
— schema constraints, enums, defaults settle "can this state even exist"
claims without running anything. Don't touch `test_tmp_*` files another
session created.

## Cross-session records — `_ai/review-history/PR-<n>/`

**Before starting**, read this directory if it exists. Axes a previous round
already judged are not re-walked — unchanged code keeps its verdict. Probes a
previous round ran are only re-checked for "is it fixed now".

**Right after posting the report**, the orchestrator writes three files
(reviewer workers never write here — parallel writers overwrite each other,
and worker findings are pre-verification):

| File | Contents |
|---|---|
| `round-N.md` | target commit SHA (mandatory — branches move between rounds), verdict table, **executed probe results**, axes inherited from earlier rounds |
| `tests-todo.md` | regression tests to plant, with the destination file per row |
| `evidence-todo.md` | verified facts to merge into `docs/.../\_evidence.md` |

Skipping this step makes review round *n* cost *n* full walks — the next
round re-finds every coordinate from scratch.

## Orchestrator: verify before posting

Never post reviewer output as-is. Check, by opening the coordinates yourself:

1. Coordinates behind every highest-severity finding — heaviest, hardest to retract.
2. "This state can occur" claims — constraints/enums/defaults may forbid the state.
3. Spec citations (clause numbers move while a review runs).
4. Test-pass claims — run them; count skips, which masquerade as passes.

Also check whether HEAD moved during the review; if source changed, those
verdicts need a re-pass. Record both SHAs in `round-N.md`.

## Closing the cycle

When the review is complete and the report delivered, mark the reviewed state
so the commit gate (this plugin's PreToolUse hook) can recognize the cycle:

```bash
git rev-parse HEAD > "$(git rev-parse --git-dir)/claude-preset-reviewed"
```

A commit closes the cycle; the next change starts an unreviewed one.

## Findings format

Severity names carry the required action, not just a rank:

```
🔴 blocks merge     — spec violation or defect; fix before merge
🟡 fix or justify   — divergence with grounds; quote the grounds, confirm intent
🟢 pass             — verified equivalent (different implementation, same behavior, is a pass)
❓ out of verified scope — could not judge; never silently counted as pass
```

Every finding carries `file:line`, what is wrong, why it matters, and a
paste-ready fix for 🔴/🟡. The report is written for posting as a PR comment,
but **the user posts it** — publishing externally is the user's call.

End with the proof block. Fill it only with files actually opened; write
`none — <reason>` otherwise:

```
📋 code-review applied
· spec:     <policy/SDD files and clauses read>
· compared: <files opened for comparison, file:line>
· verdict:  🔴 n · 🟡 n · 🟢 n · ❓ n
```
