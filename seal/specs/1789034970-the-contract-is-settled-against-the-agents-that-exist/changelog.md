<!-- seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The agent contract no longer contradicts the agent it ships beside.** §2
  forbade the full suite, the repository-wide lint and the typecheck to every
  agent and handed them to the orchestrator, which is not an agent at all —
  and `sealer`, whose entire procedure is that run, received that sentence
  before its first tool call. It shipped with a paragraph in its own
  definition saying so, and that paragraph carried its own expiry. §2 now says
  the broad gate is a single act taken once after the rounds settle, that
  whether it is yours is what your own definition says, and that one
  definition in this plugin hands it over. Nothing about narrow-and-often
  changed, and the three agents whose files stay silent still run none of the
  three checks. (#120)
- **§6 stopped carving exceptions and started naming writes.** It used to say
  an agent writes no durable record, with each real write excepted in the
  definition that held it — two of four agents already had one, and the same
  shape gives five agents four exceptions. It now says *what you write is
  named in your own definition and nothing else*. A definition that names no
  write names none, which is where every agent starts and what the next one
  inherits. The four acts withheld from every agent whatever its file says are
  unchanged: post nothing, push nothing, open no pull request, spawn no agent.
  `warden`'s report and parity mark are the same two writes under a different
  rule, and its definition says so with a bound the old word carried
  implicitly — there is no third. (#120)
- **A probe leaves nothing behind, whatever kind of thing it made.** §7
  defined a probe as one file named `test_tmp_*`, run once, deleted — and a
  probe that creates a git worktree satisfies every word of that while leaving
  something behind. One did, during a review round: its probe files were
  deleted, its report said so, and the worktree surfaced two work items later
  when `git switch` refused a branch a worktree already held. The file rule
  stays, because it is right for the common case and it is what that reviewer
  correctly followed. What is added is that the rule is about leavings — a
  worktree, a branch, a checkout, a scratch clone, a virtual environment — and
  that those are examples rather than a list, because the next leaving is a
  kind nobody has met and an enumeration that predates it reads as permission.
  The rule says whose leaving it is, too: what the probe made for itself is
  what goes, and a thing the repository's own tooling builds to be reused is
  not your probe's leaving even when your probe's run created it. And the
  procedure a reviewer actually follows says the same — `code-review`'s
  Probes row used to state deleting one named file as the whole obligation,
  which is the row the reviewer in the story above was following. (#120)
- **The routing declaration's `Implementation` row now says how to answer
  it.** The row has asked `smith` · `the session` since it was added and has
  never carried a criterion, so it is answered by habit — and the other two
  axes need none, because a wrong answer in either is contradicted at the next
  commit when the gate stops recognising the file. The criterion: is this work
  finding out or writing down? Finding out goes to `scribe`, because a large
  input and a small output is what a subagent boundary is for; writing down
  stays with the session, which already holds the context a delegate would
  re-buy. The one case `smith` answers is a diff large enough to threaten what
  the orchestrator still has to hold — and the threshold there is a number
  nobody has, which the template says rather than inventing one. What it does
  name is the axis: replaceability, not cost. (#120)
- **No section was added, retired or renumbered.** The contract stays one
  file, sixteen sections, so every `§N` in every round record this repository
  has written still means what it meant. Splitting it was weighed and refused:
  the defect was contradiction rather than irrelevance, and a line drawn at
  four agents would be redrawn when the fifth arrives. (#120)
- **A round record's terminal lines may wrap, and the generator no longer
  drops what comes after the wrap.** `Needs a fix:` and `Loses a record or
  crashes:` are the two lines that say whether a review run continues, and the
  generator matched one physical line — so a reviewer whose sentence reached
  the margin had the rest of it silently cut, and the cell still read as a
  finished sentence. It happened to this work item's own round 1, which
  shipped ending mid-clause at *the one that reopens the*. The value is now
  joined across the wrap and stops at a blank line, at the other terminal
  label, or at a line opening a new markdown block, and `agents/warden.md`
  says so where it shows the two lines: **leave a blank line under the pair**,
  which markdown wants anyway. **That last stop is known to be incomplete in
  both directions** — it passes plain prose and stops a continuation beginning
  with an issue number — which #339 carries with the verified fix; the blank
  line is the stop that covers every shape. (#120)
