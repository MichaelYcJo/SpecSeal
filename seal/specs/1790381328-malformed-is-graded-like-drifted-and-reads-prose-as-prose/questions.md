# MALFORMED is graded like DRIFTED, and rule (a) reads prose as prose — questions for the planner

<!-- seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

The owner pressed `automation` for the whole of `release: 0.15.5` and is not
available mid-run. The one decision that needed a person, #606's Q1, was
answered in the batch before the first edit: **(b)**, `MALFORMED` is graded
like `DRIFTED` (`routing.md` §*Why this way*). No row below needs a person.
Every row carries the default the build proceeds on.

## What the ticket left open and the tree answered

Listed so nobody reopens them. The grounds are in `spec.md` and in `plan.md`
*Alternatives considered*.

- **The fourth observation is in scope.** `` `@lru_cache  # memoized` `` and
  `` `x = 1  # see @jane` `` are the same class as #614's items 2 and 3 (prose
  refused, in the same unit), and `malformed_rows`' docstring already says a
  decorator is prose "in a span or out of one". Fixed by the glued-marks rule,
  not by the ordering rule, which leaves the second shape refused.
- **The notice stays one sentence** and names both verdict words; a second
  sentence chosen by cause would restate the grading beside `exit_code`,
  which the notice's own comment refuses.
- **The CI `ledger` job's warning changes, and its grading does not.** Making
  CI read stdout to fail on `MALFORMED` would undo the owner's answer.
- **`README.md`, `README.ko.md`, `CONTRIBUTING.md` and
  `docs/the-evidence-ledger.md` are not edited.** None states `MALFORMED`'s
  grading, and every sentence they carry about drift stays true.
- **`OLD-FORMAT` keeps exit 2 under both readings.** The owner answered for
  `MALFORMED` and was told the two would part.
- **Test names stay where they remain true**, so the ledger rows citing them
  drift rather than break. One case is renamed, `test_a_malformed_row_is_silent`. · NAME NOT IN TREE
  After the change it is the opposite of silent, and no ledger row cites it.
- **`PATH_HASH_RE` gets a lower bound and no upper one**: six is the fewest
  hex characters `ANCHOR_RE` takes and the remedy tells a writer to use eight;
  a 40-character SHA after a path must stay named.
- **Q1 of work item 1790297087 is ticked in that directory's `questions.md`**
  by this branch, with the owner's answer and date. The row reads ⬜ default
  (a), and the `exit_code` comment sends readers to it.
- **The empty-`Code grounds` question** (round 3's ❓ of work item
  1790297087) is not this work's. It is not in #614 or the milestone, and it
  stays with the repository owner where round 3 left it.

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does any existing case in the four modules that read this arm (`test_a_row_points_by_content.py`, `test_evidence_check.py`, `test_dispatch.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py`) change verdict under phase 1's rule (a), beyond the ones `spec.md` names? | a measurement — phase 1's boundary run of those modules. The framer executes nothing, and reading every fixture against four rule changes is what the run does in seconds | A case that fails because a prose shape is now silent was pinning the defect: its assertion follows the rule, with the grounds in `phases/phase-1.md`. A case that fails because a coordinate went silent is a trade `spec.md` did not state: stop, and state it or narrow the rule | the builder runs them and settles each in `phases/phase-1.md` | ⬜ |
| Q2 | Which ledger rows beyond the four `spec.md` lists does this work drift or make false? | the work — `evidence-check .` after phases 1 and 2 names every drifted row, which is the authority; the framer's list was read by `grep` over anchors | Claim holds: re-read, `--reverify`, dated `Re-read` note. Claim false: `Corrected <date>` note first, under `CLAUDE.md`'s rule for an edited row | whatever phase 3's run names | ⬜ |
| Q3 | Does `survivor-check` report places other than `SKILL.md`'s `OLD-FORMAT` row, and is each one a correct statement standing where it is? | the work — phase 3 runs the sweep over the branch | A correct statement (a released `CHANGELOG.md` section, a shipped work item's record, the `OLD-FORMAT` row) is exempted in this directory's `survivors.md` with its grounds. One still stating the old grading as current is corrected | exempt what is history or `OLD-FORMAT`'s; correct anything that states 0.15.4's `MALFORMED` grading as current | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records it; it does not travel back to the framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
