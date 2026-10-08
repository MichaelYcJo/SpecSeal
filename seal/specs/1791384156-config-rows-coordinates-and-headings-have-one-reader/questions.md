# config rows, the ledger coordinate and a markdown heading each have one reader (#867) — questions for the planner

<!-- seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the issue left open that the tree answered

Listed so nobody reopens one; the grounds are in `spec.md` §*Judgments the
tree answered*, numbered the same way.

1. A doubled config row is refused, not read first-wins or last-wins
   (`docs/the-pact.md`'s *its first row is not the answer*; 0 doubled rows in
   this repository's config and its 86 declarations).
2. An unreadable `seal/config.md` is refused by a command and silent in a
   hook; an absent one declares nothing everywhere (`declared_pacts` and
   `mode-gate.py#unreadable` already draw the line, each for its own kind).
3. The coordinate grammar is `ANCHOR_RE`, reached by import; the copies
   disagree today on 2 + 9 spans of 8,218 and on 47 row keys.
4. A heading is CommonMark's ATX heading on shown lines; setext is not read
   because the tree's 35 setext headings are all front matter.
5. The released rows the heading rule moves (at most 28 citations) are
   re-read and re-pointed in this work item's fragment under the freeze.
6. A `#NNN`-led prose line is not a heading in the record readers either.
7. The one heading reader is `unverified_check.py`'s, not `hooks/blocks.py`'s.
8. The vendored checker keeps a twin held equal by a case; `vendored_config_rows`
   gains the case it does not have.

Two formats the issue lists are filed rather than built — the table grammars
in `hooks/` and the live-line rules — with the grounds in `spec.md` §*Scope*
and the issue texts in `plan.md` §*Operational impact*. No row below needs a
person before the build starts.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which of the released heading-path rows go DRIFTED and which go BROKEN once `.md` regions are computed on shown lines, and what each `Corrected ·` row re-points to | the work | the checker's own run in phase 5 names each row; a DRIFTED row takes a `Re-read ·` row through `--reverify --into`, a BROKEN one (a heading that exists only inside a fence, measured for two `agents/warden.md` headings) takes a `Corrected ·` row anchored on the heading that holds the fence | the probe of 2026-10-07 counts at most 28 citations across the release files, fewer distinct rows; the exact set is the phase-5 run's | ✅ phase 5, executed 2026-10-08: 24 citations DRIFTED (`CONTRIBUTING.md` §*Running the checks* 16, `agents/warden.md` §*Report* 4, the two READMEs' §*Shared or local* 2 each), re-read; 4 BROKEN (the fenced `## Verdicts` and `## Paste-ready fixes`), corrected to `## Report` (`phases/phase-5.md`) |
| Q2 | Does the vendored config twin disagree with `hooks/config.py` on any shape the equality case's table holds, once the table holds a doubled row, an empty value, an escaped pipe, a stray separator, a second header and no header | the work | equal on every shape: the twin stays as it is and the case pins it; a disagreement on a fence-free shape: the twin is corrected to the reader, which is the direction the other twins' cases take | the inventory's row E46 says the twin differs only in knowing no fence or comment, read not executed; phase 2's case executes it | ✅ phase 2, executed 2026-10-08: the twin disagreed on three fence-free shapes — a stray separator, a second header, an empty item — and was corrected to the reader (`phases/phase-2.md`) |
| Q3 | Do any setext headings markdown-it finds in the tree stand outside a front-matter block, so that leaving setext out of the heading rule changes where a cited section ends | a measurement | none: the limit is stated and the oracle case asserts it; some: that file's headings are read differently by GitHub and by the checker, and the rule gains setext with the oracle's answer as its ground | measured 2026-10-07 with markdown-it 4.2.0 over 768 tracked `.md` files: 35 setext headings, every one a front-matter line under its `---` closer (`skills/*/SKILL.md`, `evals/*/graders/*.md`, one issue template); none in a body | ✅ |

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
