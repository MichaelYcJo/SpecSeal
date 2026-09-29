# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — phase 1

<!-- seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9ee5b9b1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 1, the gate. `main` reads the `automation` press only
after a stop is decided, through `worktree_consent.automation_answered`
against the root of the payload's `cwd`; under it both decision sites return
`deny` with a new reason for both arms. `hooks/cmdline.py` and every function
named in `spec.md` property 1 stay byte-identical. `docs/commit-review-gate-
spec.md` gains the automation row, the amended *Why a deny, and why only
once*, the #662/#665 paragraph and `Enforced by:` lines.

The spawn prompt added: the frame's invariant is the whole point of the item,
so `git diff origin/release/v0.16.0 -- hooks/cmdline.py` stays empty, and S7
is built BEFORE the gate change and kept green through the phase. S7 is every
false-silent shape from work item D's rounds 2 and 3 and #662's reverse
direction, stopping with and without the press. It also asked for the
pull-request lines `CONTRIBUTING.md` §*What a change to a gate must carry*
requires, drafted here.

## What this phase found

**The frame holds.** Every coordinate it names was opened before building:
the two decision sites and `already_asked` in `hooks/commit-review-gate.py`,
`hooks/worktree_consent.py#automation_answered`, the fixture in
`tests/test_the_guard_asks_once_per_session.py`, and work item D's round 2
and 3 reports on `fix/28-a-gate-that-fails-to-load-says-so`. Q1 was measured
once outside the suite and is `True`.

**S7 came first and never went red.** `tests/test_no_shape_the_base_stops_
reads_silent.py` was committed at `80df4da4`, before any gate edit, and passed
on the unchanged gate. It stayed green at every commit of the phase. It went
red when the press branch was mutated to return silence, at the unreadable
site and at the resolved site, one at a time.

**The base reads no commit after a reserved word on the same line.**
`for d in a b; do git -C $d commit -m x; done` returns no invocation from
`commit_invocations` at `release/v0.16.0`, and so do `do git commit`, `then
git commit` and `while …; do git commit` written on one line. The multi-line
form is read. So `spec.md` S3's "a commit inside a `for` loop over a variable"
has nothing to refuse in its one-line form, and the case uses the measured
loop's shape, whose `git` follows a `;`. The base hole is a silent the
release branch already has and a reading change this item may not make;
`overview.md` §*Not done* carries it for the orchestrator to file.

**Choices the frame left open, settled here.** The reader is imported in
place (Q3) inside a `try`, so a reader that fails to load is no press rather
than a gate with no verdict. Under the press `already_asked` is not
consulted, so no marker is written. The press read has one more guard than
the reader's own: an exception is no press, because `hooks/dispatch.py` skips
a gate that raises and a skipped gate is silence. Both READMEs gained a
sentence, because their gate row said every later stop is the plain
confirmation. Q4's wording is `AUTOMATION_WAYS`.

**What each new case was seen red against.**

| Case | Seen red by |
|---|---|
| S1, S1 parity, S2, S3 (two shapes), S4, S5 | the unchanged gate, before `5eb0bd8d` |
| S5, each of its eleven sentences | deleting that sentence from `AUTOMATION_WAYS`, one at a time, in a deleted probe |
| S7, both cases | the resolved site returning silence under the press; the corpus also with the unreadable site doing so |
| S8, and the press read only on a stop | refusing under the press before the declaration is read |
| the press read against the session's own repository | reading it against the target instead |
| a reader that raises or did not load is no press | the `try` around the reader removed |
| the parity arm offers its own waiver | the waiver fixed to `[no-review]` |
| the unreadable site's automation text | `unreadable_reason` ignoring `automated` |

S6's cases and S8 pass at the base too, as `spec.md` says they should.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* Every new case was seen failing, against the unchanged
  gate or against a mutation of the new code; the table above names which.
  S7, the case that holds the invariant, passes at the base by construction
  and goes red when the automation branch returns silence.
- *Failure direction: it blocks more, never allows more.* Under the press,
  every stop that asked now refuses. An `ask` let the commit through on a
  click and a `deny` never does. A wrong refusal costs the model a turn and a
  re-issue; a wrong allow would be a commit nobody judged, which the owner
  ranked worse than a prompt. A misread press only moves a stop between its
  two refusing forms, and every way of not reading it is today's answer.
- *Prompt budget.* An automation session: zero questions to a person from
  this gate, where the measured run had four. An attended session: unchanged,
  one refusal then a prompt per stop. A `per axis` run with its first box
  ticked still meets the prompts, as it does from the worktree guard. What an
  unattended stop now costs is one model turn per refused command, and more
  if the model re-issues it unchanged; only the reason's text bounds that, and
  Q2 measures it at the next automation run.
- *Why nothing cheaper reaches the same guarantee.* Narrowing the reading was
  tried in work item `1790635415` and read real commits silent. A written rule
  alone was in force and broken. Allowing under the press is a false silent.
  A refusal the agent handles itself is the cheaper instrument this section
  names.
- *An outage is excluded.* A refusal on every invocation needs a commit with
  no readable form. `git -C <absolute path> commit` in a command of its own is
  readable for every repository the gate can name, and for one it cannot, the
  last way on is to hand the commit back.
- *Platform honesty.* The transcript reader is the guard's, with the guard's
  coverage; nothing here inspects processes. The cases ran on macOS only.
  Windows is CI's `windows-latest` leg.
- *The issues' first boxes were replaced, not built.* #665's "silent where
  its directory is declared" is S4's "refused under the press", because
  silence there is the reading change the constraint forbids. #662's second
  box, the reverse direction, is kept inside S7.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
