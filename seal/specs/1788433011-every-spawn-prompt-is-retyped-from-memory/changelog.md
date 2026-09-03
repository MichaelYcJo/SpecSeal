<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The rules every agent works under now live in one file the agent already
  has, instead of being retyped into each spawn prompt from memory.** Half of
  every prompt was identical to the last one, so a rule that failed to be
  recalled went missing with nothing recording that it had. It had already
  happened twice: one rule arrived at round 2 of a seven-round chain and
  round 1 ran without it, and another arrived at round 3 after two rounds had
  each rediscovered it. The new `agent-contract` skill is that file — sixteen
  numbered sections holding what is true of `smith`, `warden`, `scribe` and
  whichever agent is added next: how an exit code is read, what an agent must
  not run, what a spawn prompt may narrow and may not widen, which labels a
  report keeps apart, what reaching an agent in prose is worth, what an agent
  must not write, how a probe is named and how it drives git, that edits go
  through the `Edit` tool, how reads and runs are batched, what language the
  records are written in, where a `seal/…` path resolves, and the four method
  lessons the review chain paid for. **It arrives with nothing typed**: each
  agent's definition lists it under `skills:`, so it is injected at startup,
  before the agent's first tool call, and no agent resolves a path. A section
  number is never reused and never re-ordered, so a prompt can say *§3 is
  narrowed this round* and a round record still means the same thing when
  someone opens it six months later.
  **One thing you will see that is not an agent's behaviour.**
  `agent-contract` appears in the skill listing, because that listing is how
  the harness injects it. It is not a procedure to invoke: its frontmatter
  carries `user-invocable: false` and its description says it is injected
  into agents rather than run.
  **Each agent definition keeps only what is its own.** `agents/warden.md`
  keeps where it works — a `git clone --no-local` at the target SHA, with a
  `uv` venv because `pytest` is not installed for the system interpreter —
  its report format, the verifying round's re-derivation, and the records it
  must not write. `agents/smith.md` keeps the specification set, the design
  gate, the routing declaration, vertical slices, mutation-testing what it
  added, its hand-back and the 3+ Fix Rule. `agents/scribe.md` keeps
  resolving the original checkout, an absence carrying its search, and facts
  with coordinates and no verdicts. What each had been duplicating is gone
  from all three, and a definition that carries a section's own sentences
  again fails the suite rather than passing unnoticed.
  **`docs/review-handoff-protocol.md` stops being the interim home**, which
  it had named itself since it was written, and moves to draft 0.9. The
  section that carried those rules is a pointer at the contract and the
  definitions, and what stands in its place is the one rule that was always
  the document's own: a prompt carries what is specific to the round and
  nothing else.
  **The orchestrator is bound by the same contract**, and the two skills it
  reads — `implement` and `code-review` — say so. It never opens
  `agents/*.md`, so a contract reaching only the agents would have missed the
  party whose forgetting started this: the headline failure was an
  orchestrator breaking a rule it had put into every prompt it sent.
  `user-invocable: false` permits that load and does not oblige it, which is
  why the obligation is written where the orchestrator reads. (#107)
