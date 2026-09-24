# 1790206436-the-runs-instruments-cost-wall-clock — questions for the planner

<!-- seal/specs/1790206436-the-runs-instruments-cost-wall-clock/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered

Listed so nobody reopens them; the grounds are in `spec.md` §*Judgments the
tree answered*, one number each. **No row below needs a person**, so nothing
in this frame blocks the build.

1. #475's open decision — which copy of the gate the sealer runs — is the
   copy the tree being gated ships, because that is the copy CI runs; the
   released copy's measured cost was a false refusal that stopped an
   unattended run (1).
2. An adopted `.venv` without `pytest-xdist` is given it in one install
   step, not refused and not left serial (2).
3. `-n auto` is the default for the narrow form as well as the whole suite;
   the caller's own `-n`, `-p no:xdist` or `--pdb` wins (3).
4. The redirect lives in `broad_gate.py`, not in the `bin/` wrapper pair (4).
5. The stamp's new row reads `tree <version>` or `plugin <version>`; the full
   path goes to stderr, where the moved-base line already goes (5).
6. The clone directory is `<scratchpad>/<work-item-id>/round-<n>/clone` and
   the capture file carries the work item id; #544's `r<N>-<id>` spelling
   would satisfy the same pin, and one spelling per definition is what the
   pin holds (6).
7. #544's *stronger answer* — a per-agent scratchpad — is the harness's and
   not the repository's; measured on this framer's own spawn, the scratchpad
   is session-scoped today and the orchestrator named a sub-directory by
   hand. The assumption written down and continued on: no per-agent
   scratchpad exists, and the definitions name the sub-directory so nobody
   has to (7).
8. The three tickets are one work item in three independent phases; no
   ticket is deferred (7).

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | What does `bin/test -q` cost on this machine once it runs parallel, and what share of the sealer's run are the gate's own arms once the suite is no longer the larger half? #337's *one number nobody has*. Two readings: phase 1's cold build in a scratch clone (the suite alone), and the sealer's run over this branch (the suite beside the six arms, read off `outputs kept under broad-gate-<random>/` and the panel's counts). A third, if the run happens to take it: the same suite while sibling chains run theirs | a measurement — phase 1 for the first, the sealer's report for the second | the readings go into `phases/phase-1.md`, the changelog fragment (with the date and the machine, never as a bare figure) and `overview.md`; the second becomes the flow log's reading for the segment | ⬜ half-answered 2026-09-24 in phase 1: the cold build was measured (1.6 s cold, 0.9 s warm, one module — `phases/phase-1.md`) and the suite alone was **not** run, because the spawn prompt keeps the whole suite off this segment and the sealer takes it once; the changelog fragment carries the 0.15.0 run's before figure and the preparation's hand-run after figure (`4397 passed in 3m04s`, this machine, 2026-09-24) as the configuration now made the default. The second reading is the sealer's report over this branch, and the orchestrator reads it off there; the third is taken only if that run happens to overlap a sibling's |
| M2 | Under `-n auto`, does the row's output still carry what the gate parses — the `FAILED path::name` short-summary lines `failing_files` reads and the `N passed … in 12.3s` line `suite_counts` reads? The 0.15.0 preparation's run printed the counts line under `-n auto` (4397 passed in 3m04s), and every CI leg has printed it for every release, so the counts half is read as settled; the `FAILED` half is one probe: a fixture with one failing test run through `bin/test` in a scratch clone, output read for the `FAILED` line | a measurement — one probe in phase 1, driven from Python, deleted after | assume both hold; if the `FAILED` line is absent under xdist, phase 1 records it in `phases/phase-1.md` and the gate's base comparison keeps working only through `-p no:xdist` in the row, which is then a `questions.md` row for the repository owner | ✅ answered 2026-09-24 in phase 1: both hold. A probe with one failing and one passing case, run through `bin/test <probe> -q` from Python and unlinked in `finally`, printed `FAILED tests/<probe>::test_tmp_one_fails - assert 1 == 2` and `1 failed, 1 passed in 0.55s` under `-n auto`, exit 1 (`phases/phase-1.md`) |
| W1 | Which flags beyond `-n…`, `--numprocesses…`, `-p no:xdist`/`-pno:xdist` and `--pdb` make pytest refuse `-n auto` beside them, and so belong on the runner's withholding list? pytest's own `UsageError` for `--pdb` under distribution is the one this frame knows from the tree's absence of evidence either way; `--sw`/`--stepwise`, `--lf` with `-x`, and `-s` are candidates the phase meets by trying them | the work — phase 1, by running each candidate once against the built environment and reading pytest's answer | the four named; a candidate that pytest refuses joins the list with its error quoted in the case's docstring, and one it accepts is left to pass through | ✅ answered 2026-09-24 in phase 1: none joins. `--sw`, `--lf -x`, `-s`, `-x` and `--trace` were each accepted beside `-n auto` (pytest 9.1.1, pytest-xdist 3.8.0). The frame's reason for `--pdb` was half right: xdist refuses it beside an explicit count (`-n 2 --pdb` exits 4 with its `UsageError`) and collapses `-n auto --pdb` to zero workers itself, so the flag stays on the list because withholding is the shorter route to the same serial run; `caller_decided`'s docstring and the A4 case carry the measurement |
| W2 | The spellings this frame leaves to the phase: the install-step function's name and where in `main` it is called; the xdist marker's glob on each platform; where the `gate` row sits in the panel (between `from` and the first blank, or after `chain`) and therefore where `"gate"` lands in `HISTORICAL_ROWS`; the exact sentence each definition carries for A11–A13 within 88 columns | the work — phases 1 to 3 decide each where they meet it and `phases/phase-N.md` records it | as `plan.md` §*Technical context* sketches them | ✅ answered 2026-09-24 across phases 1–3: `add_xdist(venv)`, called in `main` directly after `ensure` returned; `site_packages(venv)` is `Lib/site-packages` on Windows and `sorted((venv/"lib").glob("python*/site-packages"))` elsewhere, with `has_xdist` asking for an `xdist` directory under any of them; the `gate` row sits between `from` and the first blank, so `"gate"` follows `"from"` in `HISTORICAL_ROWS`; the sentences are in `phases/phase-3.md` and the definitions themselves |

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
