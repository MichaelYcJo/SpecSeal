# a unit the extractor cannot bound is refused (#870, #848) — questions for the planner

<!-- seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**What the tickets left open that the tree answered, so nobody reopens it.**

- *Refuse, or read more shapes* (#870's first question). #834's table and the
  brief: the readers that converged refused the unknown; the family #848
  belongs to is the one that reads text it does not control. Refuse.
- *Brace matching for brace languages and refuse the rest, or one rule per
  language* (#870's second question). One walk for the bracket family, one
  block rule for YAML, `ast` for Python, nothing else: a per-language parser
  is refused by `evidence-ci`'s single-file vendoring, and the narrowest
  promise is refused by this repository's own seven bare YAML rows and by
  #848's reporter losing the anchor the issue is about. `plan.md`
  §*Alternatives considered* holds each.
- *What verdict a refusal takes.* `docs/the-evidence-ledger.md` §*A row is a
  content anchor*: only the major level can be `BROKEN`, and an unresolvable
  major unit is. `templates/evidence-check.yml`: "A broken coordinate fails
  either way." So `BROKEN`, exit 2 under both readings, with the reason and
  the remedy on the line, and no new verdict word.
- *The Python `SyntaxError` fall-through.* Executed: a multi-line `def`
  through the indentation rule hashes lines 1–3 of 5. Same hole as #848.
  Refuse, naming the interpreter.
- *Whether the closing line joins the span.* Left out, so a row the old rule
  bounded right keeps its hash and an installer's upgrade wave holds only real
  drift.
- *What an installer sees, and where the release says it.* The changelog
  fragment under `### Changed`, gathered into the release's file and the
  GitHub Release; the commit hook and the CI copy change at two different
  moments (`spec.md` §*Scope*, last paragraph). Under a freeze the repair is
  the policy's existing `Corrected ·` row.
- *The opener's never-matching shapes* (receivers, generics, typed constants).
  Out of scope: `BROKEN` today, the loud direction.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | For each suffix on the day-one brace list (`.ts .tsx .js .jsx .mjs .cjs .c .h .cc .cpp .hpp .cs .java .kt .kts .swift .go .rs`), which string, char and comment forms does the lexer blank, and which raw-string forms does it refuse as unlexable? | the work | (a) the C-family set alone — `//`, `/* */`, `"…"`, `'…'`, `` `…` `` — and a language whose other forms re-balance a brace is a known limit; (b) one form table per suffix with a case each, and a suffix joins the list only with its table. (b) is the allow-list #835 rule 1 describes; (a) is cheaper and is the six-month failure `plan.md` names | (b), with the forms the phase finds in each language's own grammar; a form it cannot lex is a refusal, never a guess | ✅ answered by phase 2: (b). Nine families, the table in `evidence_check.py#_literal_at`'s docstring, a fixture per family holding a bracket in each form and each form mutated red (`phases/phase-2.md`). Forms not lexed (JS regex literals, JSX text, C# raw-string holes, preprocessor branches) are listed there and in `SKILL.md` §*Known limits* |
| Q2 | How many rows of this repository's own ledgers change verdict under the new rules? | a measurement | `bin/evidence-check --strict .` on the branch after phase 3 against the same command on `main`: 0 new `BROKEN` and 0 new `DRIFTED` is the expected answer, because the 24 `.yml` and 1 `.cmd` rows are 18 quoted lines and 7 bare YAML keys whose spans the block rule keeps (executed 2026-10-07: 32–128, 146–164, 46–138). Any other number is a finding for the phase, not a question | 0 and 0 | ⬜ |
| Q3 | How many rows of a consuming repository's ledger change verdict on upgrade? | a measurement | `evidence-check --strict .` at 0.21.0 in that repository, run by its installer; the one known instance is #848's reporter. The number is theirs to read and does not block this build; the changelog fragment tells them what each verdict means and what to run | unknown; the fragment is written so the number needs no reply | ⬜ |
| Q4 | What shape does `resolve_unit` return so a refusal and its reason reach `judge`, `rider_check.py#region_lines` and `survivor_check.py`'s `resolves` in one reading? | the work | (a) a three-field namedtuple `(places, resurrected, refused)` and all three callers unpack it in one commit; (b) the two-tuple stays and a separate `bounding_rule`/reason call is made first — two readings of one coordinate, which #809 showed describes one row two ways. (a) is the default; the constraint is one reading, not the tuple | (a) | ✅ answered by phase 1: neither (a) nor (b) — `Resolution`, a tuple that unpacks as the old pair and carries `refused` as an attribute, so the reason comes back from the one call and the 21 call sites that unpack the pair keep reading (`overview.md` §*Where spec and implementation diverged*) |

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
