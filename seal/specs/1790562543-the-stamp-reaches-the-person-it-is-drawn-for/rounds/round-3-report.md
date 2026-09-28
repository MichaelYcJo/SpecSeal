# Round 3 report — 1790562543, the stamp reaches the person it is drawn for

Round 3, the verifying round and the run's last. Its target is the diff of
round 2's fixes, 34a029c9..f66eae08 (one commit), with the branch at
ea6689c6 and draft PR #650. The job is the answers: are round 2's ⬜ 1, ⬜ 2
and ⬜ 3 actually closed. Round 2 recorded `New units: none`, so the fix diff
has no unreviewed unit in it, and I stayed inside that diff.

round-2.md and round-2-report.md were read for coordinates. Round 2's
confirmations of round 1's findings, and round 1's own confirmed verdicts,
are carried rather than re-derived: the fix diff changes wording, two test
assertions and one test fixture, and touches none of the code those
verdicts rest on.

## How the answers relate

```
round 2's three notes                      all three closed (executed)
  └─ ⬜ 1's narrowing was spliced into five paragraphs by hand
       ├─ two tool files keep an unwrapped line               ⬜ 1
       └─ three work-item files keep an unwrapped line        ⬜ 2 (paperwork)
```

Nothing here needs a fix. Both findings are line wrapping: the words and the
behaviour are right, and no check reads the lines they are on.

## The implementer's account against the code

- *`round_record.py close` for round 2 exited 0 (3 fixed).* Read: round-2.md
  carries `fixed` `f66eae08` on all three rows and `Needs a fix | no`. I did
  not re-run it.
- *182 passed over three modules, exit 0.* Not re-run as that set. I ran the
  two modules the fix touched plus the wrap check that covers three of its
  documents: 205 passed, exit 0 (executed, below).
- *`evidence_check.py --strict .` exited 0.* Executed at ea6689c6, exit 0.
- *Four mutants went red.* Executed, and the claim holds: I wrote the same
  four mutants myself and each turned its case red (probe M1–M4).
- *survivor-check over the range with --exempt exited 0.* Executed: over
  34a029c9..f66eae08 it exits 0 bare and with `--exempt`, and says no removed
  wording is still standing.
- *Seven release rows were re-read with notes.* Read: seven rows across
  0.9.3, 0.12.0, 0.12.2, 0.15.1 (two), 0.15.3 and 0.15.4 gained a dated
  `Re-read 2026-09-28 in round 2's fix pass` note, and each names the one
  sentence that changed. evidence-check exit 0 confirms their hashes.
- *The N9 note was corrected in place.* Read: N9 carries **Corrected
  2026-09-28** naming the side-effects pin and the narrowed Claim.

## Round 2's findings, one by one

**⬜ 1 (the scope word) is closed.** The four places round 2 named now say
the line names `seal-stamp --from` wherever it names a values file:
`docs/the-broad-gate.md:136`, `agents/sealer.md:159`,
`skills/code-review/orchestration.md:553` and `hooks/sealer-stamp.py:42`.
The comment above `DRAWN_AT_TURN_END` (`skills/verify/scripts/broad_gate.py:2417`)
names `NOTHING_RECORDED` and `VALUES_UNWRITTEN` as the two lines that name
none. The work item's changelog fragment, overview.md, survivors.md and the
N9 Claim moved with them. I searched the tree for *every sealed* and the
variants round 2 quoted. What remains is the negative pin, round records
quoting the old sentence, and the earlier `Re-read` notes in the release
files, each followed by the new note that supersedes it. The orchestrator's
paragraph no longer contradicts its own `close --broad-gate` sentence.
Probe M4 restored the old policy sentence, and the policy case went red.

**⬜ 2 (the README side-effects limb) is closed.** The limb now reads each
edition's clause in its own words. Neither clause occurs in the gate-table
row: the English row says the file is renamed `.drawn.json` and the clause
says *which the stamp hook renames once drawn and nothing prunes*, and the
Korean row and clause differ the same way. Probes M1 and M2 deleted each
edition's clause with its count word kept, and the case went red for each.

**⬜ 3 (the pipe case's quoting) is closed.** The S1 fixture now runs under
`a checkout/repo`, so `quote(path)` and the bare path differ. The new line
asserts both that the path holds a space and that the unquoted form is
absent. Probe M3 formatted `DRAWN_AT_TURN_END` with `command=path`, and the
case went red. The class has one other member, the no-session case at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:2385`, which already ran
under a spaced path. The quoting unit case at `:2620` names its own paths.

## Findings in the fix surface

### ⬜ 1 — Two tool files keep a line the narrowing splice left unwrapped

*From reading.* Two paragraphs the fix narrowed were not re-wrapped after
the splice:

- `skills/code-review/orchestration.md:554` is the single word `nothing` on
  a line of its own. The wrap check covers this file, but it measures only
  lines that are too long, so a short line passes.
- `hooks/sealer-stamp.py:43` is 92 columns in the module docstring. ruff
  selects no `E501` here and `ruff format` does not reflow docstrings, so
  nothing reads it (ruff check and format --check both exit 0, executed).

Why it is ⬜: markdown renders the first as one paragraph and Python never
shows the second to anyone but a reader of the source. Both lines say what
they should. This is the splice-without-re-wrap failure that the wrap
check's own docstring names. It lands here as a line that is short or wide
rather than one the limit refuses.

### ⬜ 2 — Three work-item files keep an overlong line (a correction)

*From reading.* Under the work item, the same splice left three lines past
88 columns: `changelog.md:14` (92), `overview.md:39` (90) and
`survivors.md:6` (96). None of these files is wrap-checked. The changelog
fragment is copied verbatim into `CHANGELOG.md` at the release, where no
check reads it either. These are the run's paperwork, so this is a
correction and not a fix. It is outside `Needs a fix`.

## Regression tests to plant

None. The three cases round 2's fixes changed were each seen red under
their own mutant this round (M1–M4).

## Facts for the evidence ledger

- N9's corrected note is true: `test_both_readmes_list_the_stamp_hook` is
  red with either edition's side-effects clause deleted and its count kept,
  and `test_the_policy_names_what_enforces_the_drawing_and_what_nothing_does`
  is red with the old *every sealed* sentence restored. Executed, M1, M2,
  M4, at ea6689c6.
- N1's S1 case now pins the quoting of the common line on a path holding a
  space, and is red with `command=path` passed to `DRAWN_AT_TURN_END`.
  Executed, M3, at ea6689c6.

## The broad gate

Not yet. My report leaves nothing that needs a fix, so the gate comes due
once the orchestrator verifies this report and writes round-3.md. What comes
due is the sealer's spawn, after this branch is merged with release/v0.15.7
as the prompt says.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The narrowing splice left `nothing` alone on a line in the orchestrator's paragraph and a 92-column line in the hook's docstring | `skills/code-review/orchestration.md:554`, `hooks/sealer-stamp.py:43` | open | read; ruff check and format --check exit 0 on the hook, executed; the wrap check measures width only; deferral candidate, see Deferred |
| ⬜ 2 | Correction: three work-item files keep a line past 88 columns from the same splice | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/changelog.md:14`, `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/overview.md:39`, `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/survivors.md:6` | open | read; paperwork, outside Needs a fix; deferral candidate, see Deferred |
| 🟢 | round 2's note 1 is closed — the recovery is scoped to the lines that name a values file, in every copy | `docs/the-broad-gate.md:136`, `agents/sealer.md:159`, `skills/code-review/orchestration.md:553`, `hooks/sealer-stamp.py:42`, `skills/verify/scripts/broad_gate.py:2417` | confirmed | read, and the tree grepped for the old scope; probe M4 executed: the old sentence restored, the policy case red |
| 🟢 | round 2's note 2 is closed — the README side-effects limb can fail on its own in both editions | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:500` | confirmed | probes M1 and M2 executed: each clause deleted with its count kept, the case red |
| 🟢 | round 2's note 3 is closed — the common line's quoting is asserted on a path holding a space | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2319` | confirmed | probe M3 executed: `command=path`, the case red; the class's other member already spaced |
| carried | round 2's confirmations of round 1's findings 1–8 and the two survivors.md exemptions, and round 1's confirmed verdicts | `hooks/sealer-stamp.py#main`, `skills/verify/scripts/broad_gate.py#signal` | confirmed | carried from round 2; the fix diff touches wording, two assertions and one fixture, none of the code under them; survivor-check over the fix range exits 0, executed |
| ❓ | S17: the stamp on the owner's screen after the orchestrator's text, unfolded, in colour, once; several stamps in one message rendering whole | the harness | ❓ out of verified scope | carried from rounds 1–2; no case can observe a screen; the owner answers on the first real run after merge |

## Paste-ready fixes

### ⬜ 1

```markdown
is drawn. Wherever the `SEALED` line names `seal-stamp --from`, quote it as
it stands: that command is the person's to type, and never yours. Every line
that names a values file names it, because the hook draws nothing and says
nothing where it cannot: a `python3` under 3.12, a working directory outside
the sealed clone, or a plugin older than the hook.
```

```python
macOS — where this draws nothing and the `SEALED` line in the sealer's
report, which names the file and `seal-stamp --from` wherever a values file
was written, is what remains. The same line is what remains where the main
session's working directory is outside the sealed clone, and where its
plugin predates this hook; `docs/the-broad-gate.md` §*Where the stamp is
drawn* states all three.
```

### ⬜ 2

```markdown
  was sealed, and draws nothing at a subagent's end. Every line that names a
  values file names `seal-stamp --from <path>` too, quoted for the shell,
  because the hook draws nothing and says nothing where it cannot: a
  `python3` under 3.12, a session outside the sealed clone, or a plugin older
  than the hook. A run with no session says so; a values file that cannot be
  written leaves the run sealed and says nothing will be drawn. The hook
  builds each stamp whole before it claims the file, so a malformed values
  file is left pending and takes no other file's drawing with it.
```

```markdown
failure, the `SEALED` line in the sealer's report names the file and
`seal-stamp --from` wherever a values file was written — true since round
1's fix pass, which added the command to the common line — and changing the
floor is a decision about every script that copies it. The hook's docstring
states it.
```

```markdown
Round 1's fix pass (`survivor-check --range a3b76a2f..23e75f53`) reported two
places. Both share wording with the orchestrator's old sentence about the
no-session line, which the range widened to every line naming a values
file. Each place is about the no-session line alone, which still says no
Claude Code session was found and still names `seal-stamp --from`, so
neither is a claim the range corrected.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_docs_line_wrap.py`, `-q -p no:xdist`, in a `git clone --no-local` at ea6689c6 | 205 passed, exit 0 |
| `ruff check` and `ruff format --check` on the four changed .py files | exit 0 and exit 0 |
| Probe M1: README.md's side-effects clause deleted with "Four side effects" kept, then `test_both_readmes_list_the_stamp_hook` | 1 failed, exit 1 |
| Probe M2: README.ko.md's clause deleted with "네 가지 부수 효과" kept, then the same case | 1 failed, exit 1 |
| Probe M3: `DRAWN_AT_TURN_END` formatted with `command=path`, then `test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing` | 1 failed, exit 1 |
| Probe M4: the old *every sealed `SEALED` line* sentence restored in `docs/the-broad-gate.md`, then `test_the_policy_names_what_enforces_the_drawing_and_what_nothing_does` | 1 failed, exit 1; the clone clean after all four |
| `bin/survivor-check --range 34a029c9..f66eae08`, bare and with `--exempt` on this work item's survivors.md | exit 0 both; no removed wording is still standing |
| `bin/evidence-check --strict .` at ea6689c6 | exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, once, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — two unwrapped lines in `skills/code-review/orchestration.md:554` and `hooks/sealer-stamp.py:43` | candidate for rung 1: the branch owns both lines, and the re-wrap is whitespace only (paste-ready above) | the orchestrator of this run, who decides whether it rides the merge with release/v0.15.7 or stays in round-3.md |
| ⬜ 2 — three overlong lines in the work item's changelog.md, overview.md and survivors.md | candidate for rung 1 as a paperwork correction (paste-ready above) | the orchestrator of this run, who writes the work item's paperwork |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round: round-2.md, round-2-report.md, the full diff
34a029c9..f66eae08 (all 17 files), `docs/the-broad-gate.md`,
`skills/code-review/orchestration.md`, `hooks/sealer-stamp.py`,
`skills/verify/scripts/broad_gate.py`, `README.md`, `README.ko.md`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`,
`tests/test_docs_line_wrap.py`, `ruff.toml`, this work item's
`seal/ledger/1790562543-the-stamp-reaches-the-person-it-is-drawn-for.md`,
changelog.md and overview.md, and `docs/review-chain-spec.md` §*Where a
leftover goes*.
