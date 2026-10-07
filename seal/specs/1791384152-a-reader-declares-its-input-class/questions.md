# a reader declares its input class (#835) — questions for the planner

<!-- seal/specs/1791384152-a-reader-declares-its-input-class/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Decided from the tree, so nobody reopens them

The ticket left these open and the repository answered them; the grounds are
in `spec.md` §*The decisions* and `plan.md` §*Alternatives considered*.

- **The registry is the code, not a table.** The house rule against a shared
  registry, the 1,000-line ceiling, #834's finding about copied judgments, and
  the follow-up list's rider precedent decide it. Q1 below carries the
  ticket's wording to the owner because `agents/framer.md` says a ticket
  asking for what policy forbids is a row, never a silent override.
- **Only code readers declare; test pins do not.** A pin's class is its
  assertion's shape by the inventory's own rule. The four test helper
  modules are code and are in.
- **The population is by construction**, from a K1 list of calls the test
  owns, and a call K1 does not know is a K1 row, never an exemption.
- **The transition is a census that only shrinks**, hashed with the ledger's
  own functions, emptied by #834's build.
- **Rule 2 is a `## Removes` section in `spec.md`, read by the records arm**
  as claims of absence; not a ratchet, not a pull-request-body reader, not a
  second script.
- **The per-phase removal table retires**, because it is a second record of
  the fact the section records once.
- **The `docs/` home is a new document**, `docs/the-reader-registry.md`,
  because no document owns the area (settle §2); the rules' one-sentence
  statements go in `CONTRIBUTING.md` §*What a change to a gate must carry*
  with links.
- **The item lands after the other 0.21.0 chains and before #834's build.**
  The order is the cost control (`plan.md` §*Operational impact*); it changes
  when the item ships, not what it builds.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The reopen comment on #835 says "the registry the test reads is the inventory table, given its `docs/` home by #834's build", and #834's spec says "the table's permanent home under `docs/`". This frame puts the table's judgments into the code's docstrings and gives `docs/` the rule, because a table every reader change edits is the shared registry `CONTRIBUTING.md` §*House rules* refuses, the inventory is 2,287 lines against a 1,000-line ceiling, and a table beside the code is the copied judgment #834 found disagreeing with itself. Does the owner want the table under `docs/` anyway? | a person (the repository owner) | (a) as framed: declarations in the code, `docs/the-reader-registry.md` states the rule, the inventory's parts stay in #834's directory as the reading of a moment. (b) a table under `docs/`, which needs an `Over the ceiling` entry or a split into eight documents, is a shared file across parallel branches, and leaves the code's docstrings a second copy. (c) both: the docstrings as the registry and a generated listing under `docs/` regenerated at each release by #834's script — a file no branch edits, which is the one shape of (b) the house rule allows; it costs a generator and a release step | (a) | ⬜ |
| Q2 | Does `evidence_check.py#py_spans` key a top-level function by its bare name and a method by `Class.method`, so that the census's `path#unit` is the ledger's own spelling and `resolve_unit` finds it? | a measurement | the build runs `py_spans` over one hook and reads the keys; if a top-level unit's key is not its bare name, the census writes the key `py_spans` gives, and the document says so | the keys are the ledger's spelling (`docs/the-evidence-ledger.md` cites `path#function` and `path#Class` that way) | ⬜ |
| Q3 | The exact K1 list at landing, and the population count it gives. The framer's probe measured 654 units with the list in `spec.md`; the build's walker resolves `subprocess` and `shlex` through imports, which can move the number | the work | the build measures, pins K1 in the test as the encoding test pins `OPENERS`, and writes the count into `docs/the-reader-registry.md` as the reading at landing | 654 at this frame's tree, 2026-10-08 | ⬜ |
| Q4 | Where in `file_claims` the `## Removes` section's lines are cut, and whether `claim_lines` or a sibling function carries the section state; the status word for a named removal that still stands and its exit grade | the work | phase 2 reads `claim_lines`' aside state and cuts the section the same way; `STANDING` is the word unless a vocabulary test refuses it, and it is graded as `NOT_IN_TREE_STATUS` is | `STANDING`, graded like a stated name the tree lacks | ⬜ |
| Q5 | Has #867's one config reader landed when phase 2 starts? | a measurement | if yes, `Removes from` reads through it; if no, `frozen_from` is generalised to `cutoff_row(root, item)` and `frozen_from` calls it, so one reader exists either way (`plan.md` §*Seams*) | read the tree at phase 2's first commit | ⬜ |
| Q6 | The value of `Removes from`: every 0.21.0 work item framed before this item lands must stay unbound, because their fragments are still live on the release branch until the fold | the work | the build writes the epoch second of the write; a sibling framed after that second is bound | `date +%s` at the write | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
