# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — questions for the planner

<!-- seal/specs/1791384158-the-broad-gate-reads-its-counts-from-the-recorder/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, so nobody reopens them.** The three tickets left
these open and the tree answered each; the grounds are in `spec.md`
§*Read by this frame* and `plan.md` §*Alternatives considered*.

- **Observed or named (#852)**: observed. pytest calls the keyboard-interrupt
  hook for `pytest.exit()` whatever return code it chose, and leaves
  `session.shouldfail` and `session.shouldstop` set on the session handed
  to `pytest_sessionfinish`; both are read in hooks the recorder already
  implements or can (R1, R2; Alternatives B, B2, B3). The exit code stays
  as the net for what no hook sees (R3).
- **Where the counts come from (#869)**: the category pytest's own summary
  counts a report under, written by the recorder by calling the teststatus
  hook as the terminal reporter does, and counted by the gate (R4, R5;
  Alternatives A, A2, A3). `warnings` and `deselected` are not recorded:
  neither is a report's category and the owner's `suite` row names passed
  and skipped (decision 6 of #832; Alternative G). Where somebody wants
  them, each is one hook on the recorder and one key in the counter.
- **What an unread line does (#869)**: it is counted per keyed file, said
  on the failure form, refuses the counts, and turns `new` into `new?` at
  the base; the verdicts the record holds are kept (Alternatives C, C2, C3).
- **Retire or keep the scale (#853)**: retired, all four things #853 lists;
  `read_values` ignores a `scale` an older file carries; the gate writes
  none; the one window is in this repository and is named (Alternatives E,
  E2, E3). The one-per-`Stop` budget rule stays, over two rungs: with the
  disc, then without.
- **Where the release seal's counts come from (#869, "where it can")**: the
  same record, through the gate's reader loaded by path, the way
  `release_seal.py` already loads the review chain's readers (Alternatives
  F, F2, F3). Where the record cannot be read, no image is attached and the
  job says why, as it does today for a JUnit file it cannot read: the suite
  row is the one row `release_seal.py` refuses the whole image over, because
  a release seal above counts nobody can vouch for is the counterfeit
  `verify` names.
- **How a malformed chart is refused (#869)**: at the gate's `load`, with
  the sibling's own sentence, before anything runs (Alternatives D, D2).
  `seal-stamp` on its own keeps its traceback and `spec.md` says why.
- **The sealer's words**: `new`, `failing on base too` and `new? …` are
  unchanged; two reasons join the `new?` family and the sealer passes them
  on unedited (`docs/the-broad-gate.md` §*One act, one owner*).
- **#825's Q1 and Q2** stand as built, (a). Nothing here reopens the
  five-row table.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q-M1 | On pytest 6.1, 7.0 and 9.1 (and 9.1 with pytest-xdist 3.8 under `-n 2`): does the keyboard-interrupt hook fire on a `pytest.exit(returncode=r)` in a test for `r` in 0, 1, 5 and `None`, and on a `KeyboardInterrupt`; is `session.shouldfail` a non-empty string at `pytest_sessionfinish` after `-x` and after `--maxfail=2`, for a failed test and for a failed collection in both orders (the broken file collected first and last, exits 1 and 2); is `session.shouldstop` set under `--stepwise`; does the teststatus hook, called from a plugin's `pytest_runtest_logreport` with `report` and `config`, return `error` for a failed setup, `xfailed`, `xpassed`, `skipped` and `passed` as pytest's own line counts them; and does a skipped collect report reach `pytest_collectreport` with `report.skipped`? The frame read all of it at 9.1.1 (`spec.md` R1–R5) and none of it on the two older builds | a measurement — phase 1, its first act, through `uvx --with pytest==<v>` the way #849 round 2 ran its ten stops | yes on all three: the design stands and `RAN_TO_ITS_END`'s comment names the builds each exit and each flag was measured on · no on an older build for one hook or flag: the recorder reads it with `getattr` and a default, the floor sentence in its docstring names the oldest build the fact held on, and the exit net keeps that stop as 0.20.0 had it | yes, by reading pytest 9.1.1 and the age of the names (the keyboard-interrupt hook and the two flags predate 6.1 by years) | ✅ measured in `phases/phase-1.md`: yes on 6.1, 7.0 and 9.1 for every hook and flag, with the recorder and with a probe; under xdist `pytest.exit` in a worker is exit 3 with no hook called, which the exit net keeps |
| Q-M2 | Over this repository's own suite run once through `bin/test -q` with the recorder's four variables set, and once more with one module carrying a module-level `pytest.skip`, one xfail and one xpass added for the run: is the string `suite_counts(record)` gives equal to pytest's printed summary line with its clock removed and `warnings` left out? A disagreement is a finding about the category rule or the `collect` reading, never a rounding | a measurement — phase 1 or 3, one run each, the two lines side by side in the phase record | equal: S5 holds on the real suite · not equal: the difference names which hook or which counting rule the frame misread, and the phase record says which before the counter is kept | equal, by reading `_pytest/terminal.py` :625–636, :800–804, :1455–1470 | ⬜ |
| Q-W1 | Which of the cases that read `suite_counts`, `COUNTS_RE`, `NO_SUMMARY` or a printed summary fixture (`LONG_SUITE`, `768 passed, 1 skipped in 9.1s`, the cases at `tests/test_the_seal_is_taken_once_by_the_sealer.py` :1924–1933, :3493–3540, :3670–3690, :4351–4380, :5907–5929 and `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` :595–640) move to a record fixture, which retire with the regex, and what each asserts now | the work — phase 3, `phases/phase-3.md` lists each with before and after | — | — | ⬜ |
| Q-W2 | The exact list of released ledger rows `evidence-check` names as drifted after phases 1–5, and which of them this work's edits made false (`Corrected ·`) rather than merely moved (`Re-read ·`). `spec.md` S15 is the frame's reading of that list; the checker's output at the close is the list | the work — phase 6, from `evidence-check --reverify --into … --checked <date>`'s own output, each `Corrected ·` row's grounds naming the sentence that changed | — | S15's list | ⬜ |
| Q-W3 | Which of the parametrised scale cases collapse to one case over the one disc, which retire with the band, and whether the byte-for-byte fixture captured at 5623d728 is taken from `seal-stamp --shape` alone or from both forms (the block form carries colour codes that a terminal's width does not change, so both should be stable) | the work — phase 5, before the first edit to `seal_stamp.py`, the capture command in `phases/phase-5.md` | — | both forms, over `SAMPLE_ROWS` | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This item has none**: every product question the
  three tickets raise is answered in the tickets themselves (#853 asks for
  the retirement; #852 asks for the settlement; #869 names the three asks)
  or by the owner's decision 6 of #832, and the one cost a person bears —
  the compatibility window of `spec.md` Scope 5 — is the owner's own plugin
  update, which every hook change already costs them.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Q-M1 is phase 1's first act, before the recorder is written against
  a reading of one build; Q-M2 is one run and two lines side by side.
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
