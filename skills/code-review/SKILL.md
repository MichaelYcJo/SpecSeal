---
name: code-review
description: |
  Two-stage review methodology (spec compliance, then quality) with comparison axes,
  cross-session review records, and re-review inheritance.
  Use when: reviewing a PR or diff, re-reviewing after fixes, orchestrating reviewer agents.
  NOT for: implementing fixes (use `implement`), style-only linting a formatter
  can do, or a plain bug-and-cleanup sweep of a diff — Claude Code's built-in
  `/code-review` covers that. This one judges spec compliance before quality and
  carries earlier rounds' coordinates across sessions.
---

# code-review — spec first, then quality

Loaded by the `warden` agent; also drives the orchestrator running a
review. The default assumption is **"this code has defects"** — try to find
them, not to prove their absence. An ungrounded LGTM is forbidden; when
uncertain, write a question, not a pass.

## Two stages, in order

1. **Spec compliance** — actual code vs. the written spec (`docs/` policies
   first, then `specs/` SDD). Look for both missing *and* unrequested extra
   behavior. Do not trust the implementer's report; read the code.
2. **Quality** — only after stage 1 passes: correctness, error handling,
   security, performance, test quality.

The SDD set includes the work item's `overview.md`, which arrives in the diff
rather than needing a search — the change writes it. It is the implementer's
account, so stage 1 governs it: read the code, never adopt what it concludes.
Three sections carry that account. **Where spec and implementation diverged**
declares where the code left the document; **Not verified** is the author's own
list of claims nobody has checked; **Fed back into the spec** holds clauses the
implementer added to the spec set during this change, which is why an account
citing them is citing itself.
Settle what you can and report each result; what only a person can answer stays
open, and the report says which of the two happened. Reviewers do not edit the
file.

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
| Concurrency & atomicity | what can change between the read that decides and the write that acts: state held across an external call or `await`, transaction boundary against lock scope, whether a retry executes twice |

Every axis above the last one is settled by reading a single request from end
to end. The concurrency axis is not: it asks what a *second* actor does while
the first is mid-flight, and no amount of following one path answers it. It was
added after a review walked all eight of the others cleanly and a second
reviewer, working from no list at all, found a window where a reservation was
mutated while an external call was in flight.

### The table is a floor, not a ceiling

A fixed list covers the same ground on a bad day as on a good one, which is
what it is for. The cost is the other half: an axis nobody wrote down is not
reported as unjudged, it leaves no trace at all. `❓ out of verified scope`
records that you looked and could not decide — there is no mark for what was
never on the list.

So name this change's own axes before starting, in the round's first minutes,
the way the base branch and the review-chain marker are settled there. Read the
diff for what could go wrong that the table does not ask about — money and
rounding, time zones, resource lifetime, migration ordering, pagination
stability while writes land — and add those rows for this round. An axis you
name here is walked and reported like any other; the ones above are the
minimum, not the set.

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

## Cross-session records — `specs/<work-item-id>/`

**Before starting**, read this directory if it exists. Axes a previous round
already judged are not re-walked — unchanged code keeps its verdict. Probes a
previous round ran are only re-checked for "is it fixed now".

The records used to be keyed by a pull request number, at
`.specseal/handoff/PR-<n>/`. That number does not exist while the rounds that
would fill the directory are running, so no correct session could create it
and none ever did; `docs/review-handoff-protocol.md` carries the reasoning.
The work item is the key now, and its `routing.md` names the branch.

**Right after posting the report**, the orchestrator writes three files
(reviewer workers never write here — parallel writers overwrite each other,
and worker findings are pre-verification):

| File | Contents |
|---|---|
| `round-N.md` | target commit SHA (mandatory — branches move between rounds), verdict table with the grounds behind each verdict, **executed probe results**, the coordinates carried in from earlier rounds, **deferrals** — what this round took out of scope and the durable home each went to — the **broad-gate state**, `not yet` or the SHA the one full-suite run happened at, and **who checked the fixes** (below) |
| `tests-todo.md` | regression tests to plant, with the destination file per row |
| `evidence-todo.md` | verified facts to merge into `.specseal/map.md` |

Skipping this step makes review round *n* cost *n* full walks — the next
round re-finds every coordinate from scratch.

The directory is **closed at merge, not deleted**: the drained rows move to
their durable homes and a closing note says what went where. A deferral that
leaves this directory leaves what the next round reads, and comes back as a
finding — which is why it is also a row in `round-N.md` rather than only a
line in `.specseal/follow-up.md`.

What carries is **where to look, not what was concluded**. A later round opens
those coordinates and reaches its own verdict; an axis marked clean in round 1
can be broken by the fixes made for round 2, and inheriting that verdict is
exactly how it goes unseen. Earlier verdicts set the agenda — every one needs
an answer this round, on this round's grounds.

Re-deriving the verdict is not re-walking the code. Finding the coordinates is
the expensive half, and both the ledger and `round-N.md` exist so it is paid
once; a later round opens what they name instead of searching again. The cost
added is a re-read at known locations, which is what keeps a round-1 pass from
covering for a round-2 regression.

The test for what may be carried is whether staleness is detectable, not
whether the fact feels durable. A ledger coordinate carries because
`evidence-check` fails when the cited lines move; what the original does
carries because `.specseal/parity.md` pins the baseline SHA it was read at. Both
are re-established when their check fails, or when `parity.md` lists the path
under coordinate-trust exceptions. A verdict on current code carries nothing —
no check exists that would tell you it went stale, which is exactly why the
round has to reach it again.

## Orchestrator: the run ends with a verifying round

A round's findings are closed after it ends, by whoever writes the fixes. Every
round but the last has a reader for those fixes — the round that follows, since
each of its verdicts needs an answer there. The last round's fixes are read by
nobody, and the box saying the review passed is ticked by the session that
wrote them.

That is not an occasional slip. It is how every run ended, and it was measured
twice in a row: the one round that did open the previous round's fixes found
**seven** defects in them, and its own fixes then went in unread.

So a run ends with a **verifying round**, and three things define it.

| | What |
|---|---|
| When | **after the fixes** for the previous round are committed — never before, or it reviews what has already been reviewed |
| Target | the **diff of those fixes**, not the branch. That is what keeps it bounded: it is the cheapest round of the run |
| Job | the answers, not new findings. For each verdict the previous round recorded as closed, is it actually closed |

**A round that opens nothing needing a fix does not consume the cap.** The cap
counts rounds that found something, because it exists to stop a loop that is
not converging, and a round that finds nothing is the loop having converged.
Nothing here runs away: a verifying round that opens something IS a finding
round and consumes the cap like any other, and one that opens nothing is by
definition the last one, because the run ends at it.

The condition is not *this round found nothing* — that would be unbounded, and
it was considered and rejected. A verifying round that raises a 🟡 the smith
answers with grounds has opened nothing needing a fix, and the run ends there.

### Then say who checked them, in the record

`round-N.md` carries `| Fixes checked by |` beside `Pass`, and the two answer
different questions. `Pass` says no finding in this round's table is still
open. This says who opened the work that closed them. Three values, and
`chain_check.py` refuses everything else:

| The cell | When |
|---|---|
| `round-N` | a **later** round opened these fixes and reported on them. It has to exist, and a round can never name itself |
| `no fixes to check` | nothing here closed with a fix. This is the verifying round's own terminal value |
| `nobody — <why>` | the gap, written down. It does not fail the pull request; it prints on every CI run |

Filling it in is the last act of a round, and it reaches back: when the
verifying round finishes, the record it verified gets its cell set to that
round's number. Every record carries the row, not only the newest — `Pass` is
a verdict on the whole review and the last round's speaks for it, while this
is a fact about one round's own fixes. `docs/review-chain-spec.md` holds the
rule and what each refusal costs.

## Orchestrator: verify before posting

Never post reviewer output as-is. Check, by opening the coordinates yourself:

1. Coordinates behind every highest-severity finding — heaviest, hardest to retract.
2. "This state can occur" claims — constraints/enums/defaults may forbid the state.
3. Spec citations (clause numbers move while a review runs).
4. Test-pass claims — run them; count skips, which masquerade as passes.

Also check whether HEAD moved during the review; if source changed, those
verdicts need a re-pass. Record both SHAs in `round-N.md`.

## Orchestrator: closing the cycle

Once the report is verified, mark the reviewed state so the commit gate (this
plugin's PreToolUse hook) can recognize the cycle. Reviewer workers never write
this mark — a review that certifies itself is what the gate exists to catch.

```bash
git rev-parse HEAD > "$(git rev-parse --git-dir)/specseal-reviewed"
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

**Paste-ready means the snippet cannot mislead on its own.** A fix often needs
a name the tree does not have yet — a field the schema never defined, a helper
nobody wrote. Saying so in the paragraph above does not travel: people copy the
block, not the prose around it. Mark every such name inside the snippet, at the
line that uses it:

```python
if requester != order["paid_by"]:   # NAME NOT IN TREE — no order schema found
    raise PermissionError(...)
```

An invented identifier that reads as verified is worse than no suggestion. If
too many names are missing for a snippet to stand, describe the change in
sentences and say which document would have to exist for the code to be
written.

End with the proof block. Fill it only with files actually opened; write
`none — <reason>` otherwise:

```
📋 code-review applied
· spec:     <policy/SDD files and clauses read>
· compared: <files opened for comparison, file:line>
· verdict:  🔴 n · 🟡 n · 🟢 n · ❓ n
```
