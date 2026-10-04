# every rule CLAUDE.md restates has one home (#730) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nobody was asked anything during this run, by the routing answer (`Automation` = `yes`).** The tickets and the spawn prompt left several judgments open. The tree answered them, and they are listed here so that nobody reopens them. Each one is decided in `spec.md`, with its grounds written where a reviewer can open them:

- **The three homes are the ones the issue proposed.** Spec Scope 1–3. The tree agrees for each: `docs/the-record-layout.md` §*The root records* gives `CONTRIBUTING.md` *how a contribution is made and checked*. `docs/branch-and-release.md` already holds the fuller, current table. `skills/implement/SKILL.md` §2 holds the generic cadence and tells the reader to look up the repository-specific half.
- **What a link-only `CLAUDE.md` row carries:** path + section, the trigger, and one act sentence, with no table, reasoning, history or home sentence. Spec D2, generalised from the *named with whose* precedent row.
- **The commit row applies §2 and does not restate it.** Spec D3.
- **A fourth restatement in `CLAUDE.md`** (the goal's batch sentence) is in scope. It was found by going through `CLAUDE.md`'s sections one at a time. Spec D1, Scope 4.
- **`CLAUDE.md`'s generated block is out of scope** as a sanctioned, checked copy. Spec O1. Grounds: #292's owner answer Q1 and `tests/test_the_claude_md_block_has_one_source.py`.
- **The method ships as both:** a verbatim ratchet check, and a recorded one-off paraphrase pass. Spec D5, D6.
- **The pin is a sibling module, not an extension of #715's.** Spec D4.
- **The ratchet fails on an increase only**, not on a decrease. Spec D5. Grounds: the fragment rule against shared files.
- **The remainder becomes one issue, cut by cluster.** Spec D7. Grounds: the leftover ladder and #223.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the ratchet's baseline, measured after phase 1, match the framer's count at `07aec0f2` (99 debt pairs and 219 runs, minus the `CLAUDE.md` ↔ `docs/branch-and-release.md` pair)? | a measurement: the builder runs the module after phase 1 | Same: record it. Different: the corpus moved with the wave-1 merge-in, and the builder records the new numbers in the phase 2 record and in the F4 paragraph. The difference changes no code, so nothing waits on it. | The numbers measured at build time win, and the framer's are the reference. | ✅ measured by the build 2026-10-04: different. After phase 1, 67 files and 184,317 words; 102 pairs share 2,064 distinct 15-word runs, 197 maximal runs, ten pairs of them the sanctioned agent preamble; `CLAUDE.md` ↔ `docs/branch-and-release.md` is no pair. After the release branch was merged in at edee5ca2, 68 files, 103 pairs, 2,091 runs, 204 maximal runs. The table holds the second (`phases/phase-2.md`) |
| Q2 | Which sentences of each home are the D4 needles? | the work: phase 1, after the homes are edited | Any sentence that only the home writes and that the link row does not need. The tree cannot fix the choice before phase 1 has written the homes' final text. | The builder chooses them, two per rule, as #715's module did. | ✅ chosen by phase 1 2026-10-04: two per rule, three for the merge rule (its table row among them), and a fourth rule for the question batch; `RULES` in `tests/test_the_rules_claude_md_names_have_one_home.py` (`phases/phase-1.md`) |
| Q3 | The lead sentence of `docs/the-record-layout.md` §*What is decided and not built yet* (*F1 is built; the other three are not yet*) goes stale once F4 (and F2/F3) are built. Who corrects it? | the work: whichever of #728, #729 and #730 squashes into `release/v0.18.1` last | This branch does not edit outside F4's paragraph (spec D8, O5). The tree cannot settle the order the three branches land in. Correcting it is a one-line edit on the last branch to land, or in the release-prep commit. | The orchestrator, at the last of the three squashes, or at the release prep if all three land without it. | ⬜ |
| Q4 | What is the remainder issue's number? | the work: the orchestrating session files it from `spec.md` §*The method and its result* (spec D7) | No agent may post (contract §6), so it cannot be filed inside the build. Until it is filed, the F4 paragraph and the changelog fragment say *the remainder issue*. | The orchestrator files it and fills in the number before the pull request is marked ready. | ✅ filed by the orchestrator as #755 before the build; the F4 paragraph, the ratchet's docstring and the changelog fragment name it |

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
