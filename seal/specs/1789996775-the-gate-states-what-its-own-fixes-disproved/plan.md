# Implementation Plan: the gate states what its own fixes disproved

<!-- seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-21 by the repository owner, when `smith` was spawned.
The `automation` preset was pressed once for the whole 0.12.3 run, and the
spawn carried this plan as the build's contract (`routing.md`).

## Summary

Three issues, one shape. `#423` measured things, fixed the code, and left the
sentences that had described the old behaviour standing — in a docstring a
reader meets first, in three operational statements, and three times in the
gate's own test module. None of them changes what the gate does, and every one
of them is a statement a reader believes.

Four phases, in the order the risk runs. #461 and #465 are self-contained code
and comment work with cases behind them. #464 splits: its code half is a
docstring, and its records half is the one that needed a judgment, which
`spec.md` A5 now states and `questions.md` records the grounds for.

The branch is `fix/the-gate-states-what-its-own-fixes-disproved`, off
`release/v0.12.3`. Routing is declared: `smith` builds, the review chain
reviews, the pull request opens, and the run does not stop to ask.

## Technical context

**What this builds on** — all coordinates read, none executed by this frame.

- `skills/verify/scripts/broad_gate.py#names_a_branch` (line 374) — six lines,
  a docstring and one `git check-ref-format --branch` call. Not a ledger
  anchor, so A1 drifts nothing.
- `skills/verify/scripts/broad_gate.py#moved_line` (line 303) — the `reads`
  branch at the `if base.ref == runner` fork is where A2 lands. `runner` is
  `REMOTE_LABEL.format(ref=base.given)`, which is how `origin/@{-1}` gets
  built out of a spelling no runner has.
- `skills/verify/scripts/broad_gate.py#panel` (line 1534) — A3 is its first
  and last docstring paragraphs. The rows and the elision code are untouched.
- `tests/test_the_gate_asks_the_range_ci_will_ask.py` `:19`, `:68`, `:377` —
  all three confirmed still standing in the working tree, word for word as
  round 3 quoted them. The replacements are paste-ready in
  `seal/specs/1789956662-…/rounds/round-3-report.md` §*Paste-ready fixes*.
- `seal/specs/1789956662-…/spec.md`:184 (`seal_stamp.py#letter` row),
  `plan.md` §*Operational impact* first bullet, `overview.md`:37,
  `changelog.md`:54 — the four record sites.
- `seal/ledger.md` R4 (`moved_line@f312f19b`) and R5 (`panel@e2c844e8`) of
  work item 1789956662 — the two anchors this work drifts.

**The constraint that shapes A2.** #461 forbids hand-rolling a pattern in
place of `git check-ref-format`, because round 1's finding 6 already replaced
one and the hand-written guard moved the defect one step down rather than
closing it. So the separation A2 needs has to be a git answer, and
`names_a_branch` is not it — `--branch` accepts `@{-1}` by design, which is
the whole of #461's first half.

**What breaks in six months.** A2's guard answers *can a runner's checkout
hold a ref spelled like this*, and it answers it by asking git about a
constructed full refname. If a later change builds the runner ref differently
— a second `REMOTE_LABEL`, a configurable remote — the guard is asked about a
string that is no longer the one printed, and it goes quiet while the sentence
goes wrong again. The case A2 plants pins the printed sentence rather than the
guard, which is what keeps that failure loud: the text is what a reader sees,
and §14 is why the text is what gets pinned.

**What breaks for A5.** `settle` (`docs/one-root-by-lifetime.md`) folds
`seal/specs/<id>/` into `docs/` at a release and removes the directory. Every
correction phase 4 writes lives in a directory that is scheduled to disappear,
and the marker comment goes with it. That is accepted rather than worked
around: the corrections are about what a reader of the shipped work item
believes while it is still there, and anything that must outlive the release
is already in the ledger row A7 corrects.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A1 alone — fix the docstring, leave `moved_line` as it is | `seal/ledger.md`'s R4 row keeps recording as **Executed** a claim the same work item disproved. The next reader of that row trusts it, and the gate's printed line is what the sealer quotes into a report | **Rejected.** #461 asks for the decision to be made, and the tree makes it: the row's own wording is the design intent |
| A2 by narrowing R4's ledger claim instead of the code — record that the line can name a runner ref for a degenerate spelling | Cheapest by far and it ships a gate that knowingly prints a false sentence into a report a person reads. `agent-contract` §14 is about exactly that surface | **Rejected**, and kept here because it is the option a reviewer will ask about |
| A2 guarded by a pattern written in `broad_gate.py` (`"@{" not in given`) | #461's *Not this*, and it is not a hypothetical — round 1's finding 6 removed a hand-written guard that had moved the defect to `origin/HEAD` instead of closing it. A pattern here would close `@{` and leave whatever git refuses next | **Rejected by the ticket.** Q3 measures the git-backed replacement |
| A2 by dropping the runner clause wherever the given spelling is not what the workflow would spell | Needs no new command and is the fallback if Q3's measurement comes back the wrong way. It says less than the current line does in the ordinary fork case, which is the case round 1's finding 2 added the clause for | **Held as the fallback**, chosen only if Q3 says `check-ref-format` on a full refname does not separate the spellings |
| A5 by writing the corrections somewhere new — a `corrections.md` in this work item pointing at the shipped one | Nothing reads it. The false sentence stays where the reader meets it, and the correction sits in a directory the reader has no reason to open | **Rejected.** The repository's own precedent is a marker at the sentence (`phases/phase-3.md`:34) |
| A5 by rewording the false sentences with no marker | A record of a past state that quietly becomes true is a record nobody can audit — `phases/phase-3.md` writes that sentence down about this exact act | **Rejected** |
| A5 extended to the round and phase records of work item 1789956662 | The audit trail every correction cites stops being a record of what was found when. Round 3 already ruled on `phases/phase-1.md`: it is read in sequence with `phases/phase-2.md`, which records the divergence | **Out of scope**, stated in `spec.md` |
| A4 extended to `CHANGELOG.md` §0.12.2 without asking | `CONTRIBUTING.md` names one branch that edits that file and it is not this one. A released record amended by a branch that policy says does not edit it is the kind of thing found at the pull request | **Q1**, a person's row, with *leave* as the default |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#461.** Q2 and Q3 measured first, then `names_a_branch`'s docstring stating the property that was measured (A1), then `moved_line`'s runner clause guarded by the git answer Q3 returns (A2), with its paragraph rewritten to say what the line now promises | A case over `moved_line` driven with a given spelling no full refname can hold, **seen red first** against the code as it stands — round 2's finding 10 quotes the exact red output — and green after (§15). The case asserts the printed sentence, not the guard (§14). `tests/test_the_gate_asks_the_range_ci_will_ask.py` and `tests/test_the_seal_is_taken_once_by_the_sealer.py` stay green | 4d8e6f74 |
| 2 | **#465.** The three statements at `:19`, `:68` and `:377` replaced with round 3's paste-ready text (A6) | `grep -n "byte-identical\|exactly as it did\|reading as it did"` over the module returns no surviving claim that the other module was untouched; the module stays green. Q4 measured here: `survivor-check` over the range, and a `survivors.md` row with grounds if it fires | b4a8f0f4 |
| 3 | **#464, code half.** `panel`'s first docstring paragraph replaced with what `phases/phase-3.md` records as true, and the elision's grounds no longer assuming the dropped prefix is `origin/` (A3) | Nothing executes differently, so the check is that it does not: the existing case over `panel` and over the rendered stdout stays green with nothing edited in it | 04946a4d, corrected at f7c9dd39 |
| 4 | **#464, records half.** The `seal_stamp.letter` row of the shipped `spec.md`, and the evidence label on the baseline half in `changelog.md`, `plan.md` §*Operational impact* and `overview.md` — each under the A5 marker (A4, A5). Then the evidence write in one pass: `seal/ledger.md` R4 corrected and R5 re-read (A7), and this work item's own fragment `seal/ledger/1789996775-….md` | `evidence-check --reverify .` names what it changed and `bin/evidence-check` reports 0 broken. `grep -c CORRECTED` over the four record files matches the number of statements corrected. `correction-check --range origin/release/v0.12.3...HEAD` reports no lost marker. Q1's default is built and the divergence is a row of this work item's `overview.md` §*Not verified* naming the owner, plus a `seal/follow-up.md` item | cfa718ce |

Status is empty, or the commit that closed the phase — never a tick and never
`done`.

## Operational impact

- **Behaviour: one printed sentence, for one input class.** A2 changes what
  `moved_line` prints where `--base` was given a spelling a runner's checkout
  cannot hold. No exit code moves, no verdict moves, no resolution moves.
  `agents/sealer.md` has the sealer quote that line verbatim into a report,
  which is why it is pinned by a case rather than only corrected.
- **Prompt budget: zero.** Nothing here adds a question to any session.
  `CONTRIBUTING.md` §*What a change to a gate must carry* says this is the
  clause a passing suite cannot report, so it is repeated in the pull request
  body.
- **No new dependency, no new env var, no migration.** Q3's candidate,
  `git check-ref-format` on a full refname, is the same command the file
  already calls with a different flag.
- **The shared ledger is touched, and that is the rule being followed rather
  than broken.** A7 corrects and re-reads two existing rows of
  `seal/ledger.md`, which `CLAUDE.md` requires of a branch that leaves a row's
  claim false — *appended is the word, and a removal is not one*. New claims
  go to this work item's own fragment. If that file conflicts at the merge,
  resolve it hunk by hunk and read both sides: never `--ours`, never
  `--theirs`.
- **`--reverify` re-stamps more rows than the drift report names**, which is
  an open row of `seal/follow-up.md` measured on this repository's own tree
  while #468 was built: the lenient run reported one drifted coordinate and
  `--reverify` re-verified five rows. Phases 1 and 3 drift two units cited by
  three rows in total — `moved_line` by R4 alone, `panel` by R5 of work item
  1789956662 and G6 of work item 1789985781. Read all three by hand before
  running `--reverify`, and say in the phase record that you did.
- **`unverified-check --baseline` reads this work item's `overview.md` row
  count against the fork point.** Phase 4 ADDS a row there under Q1's default
  and removes none, so the arm is satisfied. It also reads the shipped work
  item's `overview.md`: phase 4 edits its prose and must not touch its
  `## Not verified` table, or the count moves for a reason nobody intended.
  Read, not executed.
- **`survivor-check` is the arm most likely to speak**, because phases 2 and 3
  remove wording that near-identical sentences elsewhere still carry. Q4 is
  that measurement, and a `survivors.md` row with the grounds is the answer —
  never a reword chosen to quiet the checker.
- **A released `CHANGELOG.md` section is deliberately left unlabelled** while
  Q1 stands. A reader of `CHANGELOG.md` §0.12.2 meets the sentence without the
  label this work adds three files over. That is disclosed, not silent: it is
  a row of this work item's `overview.md` §*Not verified* and an item in
  `seal/follow-up.md`, both naming the repository owner.
