<!-- seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The agent that writes a work item's spec is no longer the agent that
  builds against it.** `framer` is a fifth agent definition. Spawn it where
  the SDD ladder already calls for a `spec.md`, and it reads the repository
  widely, collects everything a person has to answer into one batch, and
  writes `spec.md`, `plan.md` and `questions.md`. It writes no code and
  builds nothing. Until now one `smith` did both halves, which left the
  reviewer's *spec compliance first* comparing the work against its own
  description of itself — a contract and an account of what got built are
  not the same document, and nothing in the chain could tell them apart.
  The three writes are named in `agents/framer.md` itself, which is the
  whole of the permission under the §6 that shipped in 0.10.0; no exception
  is carved anywhere, and the definition assigns no broad gate, so §2 still
  names exactly one that does. Nothing existing is renamed and nothing is
  withdrawn: a session that never spawns it works as it did. (#84)
- **The two skills a design gate reaches for move with it, and the smith
  now says whether the drawing holds before building to it.**
  `feature-planner` and `confidence-check` were callable from `smith`'s
  design gate, which is the one moment a build is deciding rather than
  applying — and that moment is the framer's now. Each skill is named as
  callable in exactly one `agents/*.md`, counted from the glob rather than
  from a list, so the next move takes the clauses with it. The other half is
  what the smith gains: **its first act on a frame is to say whether the
  frame holds**, at the head of its requirements phase, with the phase
  record named as where a *no* goes. It happened twice unprompted during an
  earlier build and lived in no document. It sits before the design gate
  rather than after, because a frame judged after that gate is judged after
  its questions have already been put to a person. (#84)
- **A plan now records who approved it and when, and a question records who
  can answer it.** `templates/sdd-plan.md` gains an `Approved <date> by
  <who>` line, written when the builder is spawned, in the spelling
  `templates/sdd-routing.md`'s `Answered` line already has — until now
  nothing told a later session or CI that a person had seen the plan at all.
  `templates/sdd-questions.md` gains a column for **who can answer this
  row** — *a person* · *a measurement* · *the work* — and says outright that
  the framer opens rows without owning their answers. That file held three
  kinds of question and could not tell them apart, so a row a measurement
  settles and a row only the repository owner can settle looked identical,
  and the batch put to a person carried both. (#84)
- **The routing declaration gains a fourth axis, `Planning`, and a session
  that declares an agent it never spawned is told so once.**
  `templates/sdd-routing.md` gains a `Planning` row answering `framer` or
  `the session`, on exactly the terms the `Implementation` row already has:
  optional, absent reads as not answered, and an answer outside the
  vocabulary reads as unanswered rather than as *this file is not a
  declaration* — nothing decides a commit on it, so a typo there must not
  re-ask the review question on a branch whose answer is committed. Every
  declaration already written parses unchanged and reads `planning: None`;
  no migration, and no file has to be rewritten. **It is a record and not a
  fourth checkbox**: the ladder decides when the framer runs, so nobody is
  asked. The mark is a second constant inside `hooks/implementer.py` rather
  than a second module beside it — the file is named for the axis and not
  for the agent, and a mark written by one hook and read by another in two
  spellings is a mark that is written and never found. Spawning `framer`
  writes `<git-dir>/specseal-planner` the way spawning `smith` writes
  `specseal-implementer`, and after a commit where either declared agent
  left no mark, one line names the declaration — **one line for both axes,
  never one each**, once per repository per session, and it never blocks.
  (#84)
