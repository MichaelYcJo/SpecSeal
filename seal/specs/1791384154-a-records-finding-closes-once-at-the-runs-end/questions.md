# 1791384154-a-records-finding-closes-once-at-the-runs-end — questions for the planner

<!-- seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. -->

**What the tree answered, so nobody reopens it** (`spec.md` §*Judgments the
tree answered* holds the grounds): records-level means the ⬜ marker and not
the `Location` path; a note is carried open where it stands and closed there;
the run's end is the last record reading `no fixes to check`; no new record
vocabulary and no new cell; the corpus is grandfathered by cutoff; new text goes
to `skills/code-review/orchestration.md` and nothing into the two documents at
the ceiling; the subcommand is `notes`; a stopped run's notes close at its
`second`; the seam with #866 is one imported reader.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May the notes commit (`notes --at <sha>`) touch a path outside `seal/` and `tests/`? A ⬜ is *reads badly while the behaviour and the fact stay right*, so by definition its correction changes no behaviour — but in this repository a `docs/`, `agents/` or `SKILL.md` sentence IS behaviour (the SDD ladder's top rung), and a message's wording in a `.py` is pinned by a test. The tree cannot answer it: rule 1 says *corrected in the closing commit* of what the checks refuse and *corrected in passing or not at all* of prose, and names no path. Why a person: it decides what a note may change with no reader but the broad gate, which is a product line | a person — the repository owner | (a) **unbounded**: the commit may touch any path; the ⬜ definition is the bound and the broad gate (suite, lint, text pins) is the reader. One act closes everything, and a mis-graded ⬜ can carry a behaviour change past every reader. (b) **bounded**: `notes --at` refuses a commit that touches a `behaviour_path` (`chain_check.py:4430`, one import, no copy) — a code- or docs-located ⬜ then closes `answered` (stands) or `deferred <home>` (filed), never by an edit, which turns *only a 🔴 or 🟡 commissions a fix pass* into a check. More notes are filed; #834's 18-of-33 figure counts filings as the cost | (a), built in phase 2. (b) is one additive arm and reopens nothing if chosen later; the build does not wait | ✅ (a), the repository owner, 2026-10-08: unbounded — the notes commit may touch any path, and the broad gate is its reader |
| Q2 | Of the 35 ⬜ rows the corpus closed `fixed`, how many fix commits touched a path outside `seal/` and `tests/`? This is Q1's cost in numbers | a measurement — the orchestrator or phase 2, with `refs/remotes/pull/*/head` fetched: for each of the 14 records, `git diff-tree --no-commit-id --name-only -r <a>..<b>` over its `Fix range`, counted against `chain_check.behaviour_path` | n/a | ⬜ |
| Q3 | Which test assertions quote the sentences phase 3 and 4 reword — the `left with no row in the fix table` refusal (`tests/test_a_finding_id_is_a_bare_integer.py`), the SKILL's ⬜ line (`tests/test_the_rules_have_one_owner.py:353` pins *never counted by Needs a fix* and `Needs a fix counts 🔴 and 🟡 only`), `agents/smith.md`'s fix-table paragraph (`:391` pins the `corrected at <sha>` spelling in the owner and the smith), and `tests/test_no_passage_is_pasted_into_a_second_file.py`'s `BASELINE` for the document pairs the carriers touch | a measurement — `grep -n` over `tests/` for each quoted phrase before the edit, in the phase that edits it | n/a | ⬜ |
| Q4 | The exact wording of the four lines a person reads: `close`'s refusal of a ⬜ row, `notes`'s refusal before the run's end, `seal`'s refusal naming open notes, and `new`'s carried-count line. §14 pins each in the commit that writes it | the work — phases 1–3, recorded in each `phases/phase-N.md` | n/a | ⬜ |
| Q5 | Whether `reach_forward` takes an `into=` parameter or `notes` loops it over every later record of the run; `inherited_rows` is first-seen-wins across rounds, so round K's coordinate sits under round K in every later record's `## Inherited coordinates`, and all of them owe the new word | the work — phase 2, measured against a three-record fixture | n/a | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
