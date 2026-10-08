# a round-record cell has one reader (#866) — questions for the planner

<!-- seal/specs/1791384155-a-round-record-cell-has-one-reader/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** The owner pressed
`automation` (`routing.md`), and every row below is a measurement or the
work's.

**Judgments the issue left open that the tree answered.** Listed so nobody
reopens them; the grounds are in `spec.md` §*The five judgments, decided* and
in `plan.md`'s Alternatives table.

- Which copy becomes the one reader: `chain_check.py`'s, for every judgment.
  `docs/round-record-spec.md`'s opening names the check as the authority for
  how a row is read, and the three other scripts already load that module.
- Where it lives so all four can import it: in `chain_check.py` itself. No
  new module; `tests/test_a_script_copied_alone_exits_2.py` gains no row.
- What a bare `yes` means everywhere: no reopening at the gate (refused above
  `NEEDS_FROM`, printed below), refused at the writer, and *cannot answer* on
  the panel, which prints `<R>` alone. Never `capped`.
- Which direction an unknown pull-request state fails in: ready, as
  `docs/round-record-spec.md` §*`Pass` has to be checked* already rules, with
  `gh` asked first as a second observed source. The generator's and the gate's
  draft payloads were the rejected override under another name.
- Whether the broad gate's chain arm needs a parameter: yes, `--sealing`,
  because it checks the `Broad gate` cell the same run then writes. It excuses
  that one arm on the last record and is printed.
- `Location`: `depth_two` moves to `path_forms`; the cell gains no column.
  Measured: 0 of 61 `fixed` rows in the tree name a unit without a path, and
  #823's own count found 0 of 179 at three tags.
- The deferred home's grammar: what stands after `deferred` up to the first
  ` — `, as `close` writes it; an issue is a home that is exactly `#N`.
- A doubled close is read at the head of the Grounds cell, where `close`
  writes it; prose later in the cell is prose.
- Duplicate rows and boxes fail the record at the pull request, matching the
  generator's refusal. Measured: none in the tree's 22 records.
- The walks, the run cut and the premature-gate test change no verdict; they
  become one function each.
- Nothing from `seal/follow-up.md` is this work's prerequisite: its rows on
  `chain_check.py --worktree` reading declarations and on scripts below the
  interpreter floor are untouched by any phase.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | What does `gh pr view --json isDraft` print and exit in the four states the check meets — no pull request for the branch, a draft, a ready one, `gh` not logged in — and does the stub `gh` S7 places on `PATH` reproduce each? | a measurement | one run of each in a scratch repository; the answers become S7's fixtures. Reading says a missing pull request exits 1 with *no pull requests found*, which is `unknown` | unknown for every non-zero exit and for stdout that is not a JSON object with a boolean `isDraft` | ✅ measured 2026-10-08 in phase 4: no remote, no pull request for the branch and a refused token each exit 1 with one stderr line; a draft and a ready one exit 0 with `{"isDraft":true}` / `{"isDraft":false}`. The default held; the suite's stub `gh` reproduces each answer it is asked for (`phases/phase-4.md`) |
| M2 | Which released ledger rows drift at each phase, and does each claim still hold? `spec.md` counts 172 by `grep`; only `evidence-check` after the edit names them for certain | a measurement | `evidence-check` after each phase's edit; `--reverify --into` this item's fragment with `--checked <date>`, the claim corrected first where the edit made it false (rows on location_units, pull_request_is_ready, draft_env, and any row stating the panel's `startswith`) | re-read every drifted row at the phase that drifted it, never at the end | ⬜ |
| W1 | Do the document replacements fit under the 1,000-line ceiling? `docs/review-chain-spec.md` is at 999 and `docs/round-record-spec.md` at 994, and phases 2, 3, 4, 6 and 7 each replace a sentence in one of them | the work | each phase measures `wc -l` after its edit. If a replacement does not fit, the phase that meets it cuts the document at a `##` heading into a sibling file carrying its fold markers whole and its `Enforced by:` lines, as `docs/the-record-layout.md` §*F1* records for `docs/commit-review-gate-spec.md`, and re-anchors the ledger coordinates on the moved headings in the same phase. The other option — writing the sentence only in this `spec.md` and leaving the document false until `settle` folds — is refused: `docs/round-record-spec.md` says *update spec and code together* | replace, measure; cut only where a replacement cannot fit | ⬜ |
| W2 | Does the environment-leak case at `tests/test_the_seal_is_taken_once_by_the_sealer.py:9425` still have a consequence to assert once `--sealing` excuses the fixture's `Broad gate: not yet`? | the work | phase 4 runs the case with the runner's payload set and reads what fails now: `GITHUB_HEAD_REF` naming another branch makes the declaration *not this branch's*, which is one observable consequence. If nothing observable remains, the case is replaced by one asserting the payload is read as given, so the clearing fixture keeps its teeth | keep the case's purpose; re-pin the consequence that exists | ✅ decided 2026-10-08 in phase 4: no failure is left to observe, so the case asserts the judgment — the chain arm's kept output names the runner's payload, where the cleared run names `gh` (`phases/phase-4.md`) |
| W3 | Does #835's registry land before phase 7, and in what shape does it take a reader's class? | the work | phase 7 reads `origin/release/v0.21.0` for #835's files; if the registry exists, the table in `spec.md` §*Data & interfaces* is entered there in its shape; if not, the table stays in `spec.md` for #835 to read | the table in `spec.md` | ⬜ |

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
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
