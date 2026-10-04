# 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The routing answer is `automation`, and the
spawn prompt said to decide open choices with grounds. The ticket leaves no
product question open: it states the behaviour is right and only the
sentence is wrong. Each `D` row is ticked as decided by the frame, not as
answered; a reviewer who opens what its grounds cite can overturn it.

**Judgments the ticket left open that the tree answered**, listed so nobody
reopens them:

- whether the work needs a phase split (D1);
- whether the reviewer's sentence is taken verbatim (D2);
- whether `switch_kind`'s docstring is in scope (D3);
- whether a changelog fragment is owed for a docs correction (D4);
- what the ledger fragment holds (D5);
- whether glued short-option values (`switch -cfoo`, `checkout -bfoo`) ride along (D6);
- where the pin lives (D7).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| D1 | One phase or several? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | one phase, two commits · or a phase per finding. A phase boundary between 🟡 9 and ⬜ 10 hands nothing forward, and §14 forbids splitting the sentence from its pin | one phase; commit A = sentence, docstring, pin, `KINDS` rows; commit B = the rule case | ✅ decided by the frame (`plan.md` *Summary*) |
| D2 | Take the reviewer's sentence verbatim, or tighten "a word"? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | verbatim: verified by the reviewer over 2,859 shapes · tightened: judged by reading only, and the pin text changes | verbatim | ✅ decided by the frame (`plan.md` alternative 2) |
| D3 | Correct `switch_kind`'s docstring too? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | yes: it states the same words and is wrong for a name before `--` (contract §12) · no: leaves one instance of the class | yes, docstring only; one more `Re-read ·` row (K5) | ✅ decided by the frame (`spec.md` *The class*) |
| D4 | Is a changelog fragment owed? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | yes: the policy text a person reads changed, and `docs/the-record-layout.md` sends a change's entry to `changelog.md` · no: behaviour is unchanged. Precedent: 1791019477, a docs-only work item, wrote one | yes, one `### Fixed` bullet | ✅ decided by the frame |
| D5 | What does the ledger fragment hold? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | one row for the sentence ↔ `switch_kind` ↔ C1/C2, plus `Re-read ·` rows for K7, `Re-read · M2` and K5 · or also the round-3 git facts. The corrected sentence makes no claim about git, so those facts ground nothing here | the row and the three re-reads; the git facts stay in the round-3 report | ✅ decided by the frame (`spec.md` *Out*) |
| D6 | Do glued short-option values ride along? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | ride along: a behaviour change to `switch_kind` and to the frozen `classify`, which is mechanism outside a sentence fix · file it: the sentence and `switch_kind` already agree on those shapes | out of scope; the orchestrator files it with the coordinates in `spec.md` *Out* | ✅ decided by the frame |
| D7 | Where does the pin live? | a person, decided by the frame. The tree gives the grounds; overturning them is a person's call | the existing `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` (the reviewer's placement, already pins this paragraph) · a new case | the existing case | ✅ decided by the frame (`plan.md` alternative 4) |
| M1 | Does `survivor-check --range e141980a...HEAD` report a survivor of the old sentence? | a measurement | none expected: the only other copies are round records, which the sweep excludes (`docs/review-chain-spec.md`) · a survivor gets a `survivors.md` row with grounds | none | ⬜ the builder runs it (`spec.md` A7) |
| W1 | The docstring's exact wording | the work | any wording that states the corrected sentence's order (`-b`/`-B` first, then `--`, then `-` or a word other than `.`) | the builder's | ⬜ phase 1 |

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
