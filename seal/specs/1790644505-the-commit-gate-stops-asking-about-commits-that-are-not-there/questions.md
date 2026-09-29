# the commit gate stops asking about commits that are not there — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row below needs a person, and none blocks the build.** The owner set the
constraint in the spawn prompt: no command shape may read silent where
`release/v0.16.0`'s gate judges it. The tickets and the prompt left the
following judgments open, and the tree answered each of them. The grounds are
in `spec.md` or in `plan.md`'s Alternatives table. They are listed here so
nobody reopens them as questions:

- **Where the prompts came from.** Four `ask`s in session `ab2760f5…`: three
  from D's smith and one from the orchestrator. The deny budget for the main
  checkout had been spent at 22:59:41 by the orchestrator's own loop. Read
  from the transcripts (`spec.md` §*Where the four prompts came from*).
- **Whether #662's reading is wrong.** It is not. The gate carries the `cd`'s
  failure branch past a `;` or a newline, as a shell does
  (`docs/commit-review-gate-spec.md` §*Two operators consume one, not one*).
- **Whether #665's reading is wrong.** It is not. Reading a heredoc body as
  shell is deliberate (legacy #75, `seal/ledger.md` §*Edits that reach the
  commit gate*, contract §9).
- **Whether the gate changes at all.** Its decision changes under the
  `automation` press. Its reading does not (`plan.md` Alternatives D, against
  A, B, C and F).
- **Whether the fix belongs on the agent side.** Partly. §9 was in force and
  broken, so a written rule alone is measured to fail. Contract §17 is the
  second half of the chosen design, not the whole of it (Alternative E).
- **What signal says "automation".** The person's harness-written press, read
  by the guard's existing reader. The `Automation` row of `routing.md` is not
  read: in the measured run the session's own branch had no declaration at all,
  and the guard spec refuses a model-written file as consent.
- **Which repository the press is read against.** The session's own, which is
  the root of the payload's `cwd`. An unreadable target has nothing else to
  read it against, and the standing to speak already comes from there.
- **Whether a `per axis` run with its first box ticked counts.** It does not,
  for the guard spec's measured reason. The consequence is stated in `spec.md`
  §*Scope*, Out.
- **Whether the automation reason offers `[no-review]`.** It does, last, and
  only for a commit that belongs to no work item. `skills/implement/SKILL.md`
  §1 says a waiver is one command's and the implementer's, and `agents/smith.md`
  calls it the last way past the gate.
- **Whether both arms change.** Both do. The deny-or-ask choice is shared by
  the review arm and the parity arm in `main`, and a parity prompt in an
  automation run breaks the same promise.
- **Where the written half goes.** A new contract §17, not a spawn-prompt
  habit (the contract's preamble) and not a copy in `agents/smith.md`
  (`tests/test_a_moved_rule_leaves_its_definition.py`).
- **What happens to the issues' acceptance boxes.** #665's first box
  (*silent where declared*) is replaced by S4 (*refused under the press*).
  #662's second box (the reverse direction pinned) is kept, inside S7.
  Rewriting the issues is the orchestrator's act.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Would the measured run have been read as `automation`? Does `worktree_consent.automation_answered(<root of the main checkout>, "ab2760f5-ebe2-4d22-80a0-dc951c2921de", "")` return `True` on the owner's machine? **Read** already: the 2026-09-28 21:50:02 result entry is `type: user` with `isSidechain: false` and `cwd` the main checkout. Its first question is single-select, with labels `automation (Recommended)`, `per axis` and `no work item`, answered `automation (Recommended)`. All four of the reader's conditions hold on paper | **a measurement**: one call, by the builder in phase 1, outside the suite (no case may read a real transcript) | **True:** the design removes all four measured prompts, and phase 1 proceeds. **False:** the reader rejects a shape that reading accepted. Phase 1 finds which condition before building on it and records a divergence row in `overview.md`, because the frame's claim that the measured run is covered would then be false | True | ⬜ |
| Q2 | Does the refusal loop? At the next `automation` run after this ships, how many commit-gate denies does each session take, and how many were the same command re-issued unchanged? | **a measurement**: taken by the orchestrator of that run, from its own transcript, by the method `spec.md` §*What was measured before this frame* used. Post it to the open flow-measurement log as the segment ends | **None repeated:** the reason's text is enough. **Repeats:** the reason is reworded first, and a mechanism (a count of refusals naming the command) is a new work item carrying `CONTRIBUTING.md`'s four requirements | The reason's text bounds it | ⬜ |
| Q3 | Does the commit gate import `automation_answered` from `hooks/worktree_consent.py`, or does the reader move to a module both gates import? | **the work** | **Import in place:** no ledger row moves, and the commit gate loads one more module in the same process (`sys.modules` deduplicates it under `dispatch.py`). **Move:** rows A1–A3 of `seal/releases/0.15.5.md` and W3 of `seal/releases/0.15.6.md` are REMOVED there and re-claimed in this work item's fragment | Import in place | ⬜ |
| Q4 | The exact wording of the automation reason | **the work**, pinned by S5 (contract §14) | Constrained by `spec.md` §*Scope* item 3: its order, what it names, and that it does not name `AskUserQuestion` | As `spec.md` states | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
