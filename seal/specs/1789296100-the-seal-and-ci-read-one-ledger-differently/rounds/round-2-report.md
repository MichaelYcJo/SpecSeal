# 1789296100-the-seal-and-ci-read-one-ledger-differently — review round 2 report

| Field | Value |
|---|---|
| Target SHA | `bc70e7d90cde357247e82477a712b2447ccc907d` |
| Base | `37f73213c0c1629140d89d86cc36107983d3401c` (round 1's target) |
| Branch | `fix/354-the-seal-and-ci-read-one-ledger-differently` |
| Round | 2 — the verifying round, over `git diff 37f7321..bc70e7d` |
| Agents spawned | none |

**No agent was spawned for this round** (contract §6). Every read, probe and
run below was taken in this session.

## What this round was

Round 1's fixes were written by a fix pass and read by nobody. This round is
the reading. Its surface is the fix diff and round 1's nine verdicts, not the
branch — round 1's judgments of the build are inherited, and nothing in this
diff reopens one.

**Round 1's fixes hold.** Seven closures are confirmed on my own grounds,
three of them by execution; the answered finding is the orchestrator's cell
and was filled; the deferred one reached #379 with the class written out. The
one thing I opened is a correction to the work item's own paperwork, which
`Needs a fix` does not count.

## How to read the grades

`🔴` blocks · `🟡` fix or justify · `⬜` correction, nothing ships wrong.
Every finding says how it was established — **read** or **executed**.

## Finding 1 is fixed, and the rewrite is stronger than the block it replaced

**Established: executed.**

The fix pass declined to paste round 1's block and wrote an AST reader
instead. I ran the mutation round 1 ran, and four more, to settle whether the
new case earns that.

`failure_loop` walks `gate()` to the one loop over `checks.items()` and
`test_a_failing_ledger_check_is_what_reaches_the_failure_form` asserts three
things about it: the loop skips a check on `not check.failed` and on nothing
else, its last statement collects every check it let through, and the one
branch on a non-empty `failures` is what takes the failure form. Each of the
five mutations below is a different way to make the gate lenient about the
ledger, and every one goes red on the assertion that owns it — with the case
named in the failure and no `NameError` anywhere. The module is **14 passed**
unmutated, exit 0 read directly.

| Mutation applied to `gate()` | The rewritten case says |
|---|---|
| `if name == LEDGER or not check.failed: continue` — round 1's own | red: *the failure loop skips a check on something other than that check's own result* |
| a separate `if name == LEDGER: continue` above the existing skip | red, same assertion, both tests listed |
| the `if failures:` branch stops calling `stamp.not_sealed` | red: *the failure form is no longer taken* |
| the loop stops appending the ledger check to `failures` | red: *the loop no longer ends by collecting every check it let through* |
| the failure form leaves the branch and the name stays further down the file | red on the same assertion |

The three stated reasons for the rewrite hold, and two of them are measured
rather than argued:

- **A string search cannot tell an exemption from a reinforcement.** I added an
  enrichment branch `if name == LEDGER:` inside the loop, exactly parallel to
  the `if name == SUITE:` already there — not a skip, not a lenience. The
  rewritten case stays **14 passed**; round 1's `assert "LEDGER" not in loop`
  goes red. That is a false positive the repository would have paid for at the
  next edit of the loop.
- **`in src[head:]` does not read the branch.** Under the fifth mutation —
  the failure form replaced, and `stamp.not_sealed(` left standing in a comment
  below — all three of round 1's assertions pass while the rewritten case goes
  red. The old block would have certified a gate that no longer refuses.
- **The slice pulls in a line that is not in the loop.** Confirmed: the text
  between `failures = []` and `if failures:` carries
  `sys.stderr.write("broad-gate: outputs kept under …")`, which sits after the
  loop, not inside it. Read, and reproduced by the slice itself.

`import ast` is at `:29` of the module at this SHA, so the wrong-reason red
the fix pass reported is gone. None of my five mutations produced one.

Both new units are **depth 1**, verified by reading
`skills/code-review/orchestration.md` §*New units*: both pin `gate()` in
`skills/verify/scripts/broad_gate.py`, which predates this branch, and neither
answers a finding inside a unit an earlier round's fixes created. The fix pass
added **no mechanism**: the diff touches no file under `skills/*/scripts/`,
`hooks/` or `.github/scripts/` — the only code file it changes is the test
module, and every other file in it is a document.

## Findings 2, 4, 5, 6, 8 and 9 are fixed on my own grounds

**Established: executed for 2, read for the rest.**

**Finding 2 — the count is right and the row is findable.** I re-applied the
checker's own `ANCHOR_RE` per ledger file at this SHA. Seven
coordinate-shaped tokens in `seal/ledger.md` are dropped whole; two of them —
`#analyse@e52dee1b` at `:1830` and `#spawn_cuts@570c32bb` at `:1859` — carry no
path and sit in Notes cells as prose shorthand, so **five is the right number**
and it is the orchestrator's number rather than a repetition of the
reviewer's. The five sit in rows citing
`tests/test_a_rider_reaches_its_file.py`, `tests/test_what_the_reader_understands.py`,
`skills/code-review/scripts/chain_check.py` twice, and
`.github/workflows/hygiene.yml`, which is exactly what the rewritten row names.
Dropping the line numbers costs a reader nothing: each name greps to one place,
and the row says why the positions were left out. I also ran the checker
narrowed to that one ledger — **`1148 ok · 0 drifted`, exit 0** — so the figure
the row quotes is true at this SHA and not only at round 1's.

**Finding 6 — the prose and the table now agree, and so do the three
documents.** The SKILL's table is four rows, one reader each, and its opening
sentence reads *Four readers … Three of them read its exit code … the fourth
never reaches the exit code at all*. `CONTRIBUTING.md:21` reads *Three readers
of the exit code*, and the three its own block names are the bare script call,
CI's `ledger` job and `broad-gate`. `spec.md` opens at *three readers of one
exit code* and names the advisor as the fourth at `:80`. I grepped every
reader-count sentence in the five documents S5 lists plus this work item's
records: no surviving statement says three without saying of what.

**Findings 4 and 5 — the corrections reached the files a reader opens.**
`spec.md` §*Data & interfaces* now names `broad_gate.py#gate` with the line
ranges, `overview.md` §*Fed back into the spec* no longer reads *None* and
carries both corrections as *inferred during implementation*, and the
divergence table gained the `seal/ledger.md` row with the grounds round 1
asked for. The fragment's third Notes cell stops describing the contract as
naming the wrong unit, which it no longer does.

**Findings 8 and 9 — the two sentences say what the code does.** The SKILL now
says `--migrate` and `--reverify` *are writers, not readings of drift: each
returns 1 for the rows or ledgers it could not rewrite*, which is the
correction round 1 asked for and is right about both returning 1.
`CONTRIBUTING.md` narrows to *a check run that comes back exit 1*. The
fragment's header comment now says the `####` is a body heading that `demote`
moves two levels, and no longer contradicts the line under it.

**The four re-verified rows say why each claim survives.** `17ebf41` re-stamped
three `seal/ledger.md` rows (R3, R4, S1 — all citing `CONTRIBUTING.md`
§*Running the checks*) and the fragment's fourth row. Each Notes cell gained a
sentence naming what the edit did and why the claim is still true: *reworded
that same paragraph … still no version number in it*; *reworded two sentences
inside that paragraph and moved no command*; *reworded the paragraph above it
and left `Name a module` untouched*; and for the fragment, *split the anchored
table into four rows … `broad-gate` and `--strict` still stand in that one
block, and the case is green*. The three shared-ledger rows carry
`2026-09-10 · 2026-09-13` in `Checked`, so the re-reading is dated rather than
replacing the earlier one. This is a re-reading, not a new date.

## ⬜ 1 · The reader-count reword left three paragraphs unreflowed

**Established: read.**

The same edit in three files changed a phrase mid-paragraph without reflowing
around it, so each paragraph now has one line that does not sit with the rest:

- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md:8`
  — 101 columns, in a file whose other prose lines sit at 65-81.
- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md:11`
  — a 16-column orphan reading *differently, and*.
- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md:7`
  — a 30-column orphan reading *so. `evidence-check` — the*.

Nothing goes red: none of these paths is in `tests/test_docs_line_wrap.py`'s
`COVERED` list, and that module is 23 passed at this SHA. The changelog one is
the only one with reach, because `.github/scripts/gather_changelog.py`
concatenates the fragment into the released section as it stands, so the orphan
line ships into `CHANGELOG.md` at the release. Rewrapping each paragraph is the
whole repair.

This is the work item's own paperwork, so it is `⬜` and out of `Needs a fix`
per `agents/warden.md`'s paperwork rule. I name it because the sealer's run
cannot see it and the release gathers one of the three.

## What I could not judge

| Item | Who answers |
|---|---|
| Whether `broad-gate`'s own end-to-end run prints no notice at exit 2 — still the branch's only open behaviour question, already in `overview.md` §*Not verified* | the sealer |
| The full suite, the repository-wide lint and the typecheck — not run at any SHA on this branch. Contract §2 forbids all three to this round | the sealer |
| `hooks/evidence-advisor.py` on a drifted tree — read, never run. Round 1's deferral stands and this diff does not touch it | the review chain, or a later work item |
| Which side gives between `agents/framer.md` and the overview case (#379) | the repository owner |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 is fixed, and the AST rewrite is strictly stronger than the paste-ready block it replaced | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` · `skills/verify/scripts/broad_gate.py` | answered | executed — five mutations of `gate()`, each red on the assertion that owns it, no wrong-reason red; a reinforcing `LEDGER` branch leaves the case green while round 1's string assertion goes red; a failure form moved out of the branch passes all three of round 1's assertions and fails this one |
| 2 | Round 1's finding 2 is fixed: the row names the third shape, its five live instances and the files they sit in | `seal/follow-up.md` §*Schedulable items with nowhere else to go* | answered | executed — the checker's own `ANCHOR_RE` per ledger file returns seven dropped tokens, two of them path-less prose shorthand at `seal/ledger.md:1830` and `:1859`, so five is right; the narrowed run reports `1148 ok · 0 drifted`, exit 0 read directly |
| 3 | Round 1's finding 3 reached #379 and the divergence row now names the class rather than this work item's scheduling | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | answered | read — the row names all three framer commits of the release and points at #379; the fix is a shared surface and stays out of this branch |
| 4 | Round 1's finding 4 is fixed: the divergence table carries the `seal/ledger.md` row with the grounds | same file, §*Where spec and implementation diverged* | answered | read |
| 5 | Round 1's finding 5 is fixed: the contract names `gate`, and *Fed back into the spec* carries both corrections | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md` | answered | read |
| 6 | Round 1's finding 6 is fixed: the table is one row per reader and every surviving count says what it counts | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` · `spec.md` | answered | read — a grep of every reader-count sentence in the five documents S5 lists |
| 7 | Round 1's finding 7 is closed: the four `Ran by` cells are the orchestrator's and were filled | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/` | answered | read — the fix pass left the phase records untouched, which is correct |
| 8 | Round 1's finding 8 is fixed: both writers are named as writers, and both return 1 | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` | answered | read |
| 9 | Round 1's finding 9 is fixed: the header comment and the `####` under it now say the same thing | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | answered | read |
| 10 | The reader-count reword left one unreflowed line in each of three files; the changelog one ships into `CHANGELOG.md` at the release | `spec.md:8` · `overview.md:11` · `changelog.md:7` | open | read — measured column widths against each file's own prose; no covered path, `tests/test_docs_line_wrap.py` is 23 passed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` at the target SHA | **14 passed** in 0.61 s, exit 0 read directly |
| Five mutations of `gate()` in `skills/verify/scripts/broad_gate.py`, each run against that module and each restored from bytes held in the mutating process | every one **1 failed, 13 passed**, exit 1, the new case named in the failure and the assertion that owns the mutation quoted. No `NameError` in any run |
| A sixth mutation adding a reinforcing `if name == LEDGER:` enrichment beside the existing `if name == SUITE:` | **14 passed** — the rewritten case is green, while round 1's `assert "LEDGER" not in loop` evaluates False on the same tree |
| Round 1's three paste-ready assertions evaluated against the tree where the failure form has left the `if failures:` branch | all three pass while the rewritten case fails — the measurement behind the fix pass's second reason |
| The checker's own `ANCHOR_RE` applied to `seal/ledger.md` and the fragment, against every backticked coordinate-shaped token in each | seven dropped in the shared ledger, two path-less prose shorthand; **five row anchors**, in the files the rewritten row names. The fragment drops none |
| `evidence_check.py --ledger seal/ledger.md .` | **`1148 ok · 0 drifted · 0 broken · 0 external · 0 old-format`**, exit 0 read directly — the figure the follow-up row quotes, true at this SHA |
| `bin/test tests/test_docs_line_wrap.py -q` | **23 passed** — none of the three unreflowed paths is covered, so nothing goes red |
| `git status --porcelain` after every probe and again at the end | empty each time. Each mutated file was restored from bytes held in the mutating process and compared byte for byte; no probe file was written inside the repository |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch, and it is not this round's to take (contract §2). With this round opening nothing that needs a fix, it is what comes due next: the sealer's spawn, not a run for the session reading this to assemble |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it — three shapes now, five live instances in the shared ledger | `seal/follow-up.md` §*Schedulable items with nowhere else to go*, the existing row, which this diff extended. Already deferred; round 2 confirms the row's count and its instances | the repository owner |
| The framer / overview-case contradiction | #379. Already deferred by round 1's fix pass, and the divergence row now points at it | the repository owner |
| Whether `broad-gate`'s own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |
| `round_record.py`'s `fix_table` cuts the SHA out of the middle of its own code span and leaves both backticks standing, so every `fixed` verdict in `round-1.md` reads *fixed at `<sha>` — `` —*. **Already ridered**, at the `note` line of that function, stamped `Verified 2026-09-08 against fix_table@884956f3`, and it predates this branch. Named here only so it is not re-reported as new | the repository owner, at the rider |

Needs a fix: no

Loses a record or crashes: no

Nothing in the fix diff moves an exit code, writes outside the root, or can
crash — the only code file it touches is a test module, and the rest is prose.
Finding 10 is a line width in three documents. Round 1's own answer to this
question stands unchanged.

## Proof block

**Executed**

- `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` — 14 passed
- six mutations of `gate()`, each run against that module, each restored byte for byte
- round 1's three paste-ready assertions evaluated against two mutated trees
- the checker's own `ANCHOR_RE` applied per ledger file against every backticked coordinate-shaped token
- `evidence_check.py --ledger seal/ledger.md .` — 1148 ok, 0 drifted, exit 0
- `bin/test tests/test_docs_line_wrap.py -q` — 23 passed
- `git diff`, `git show` and `git log` over `37f7321..bc70e7d`, including `--word-diff` over `17ebf41`
- `gh pr view 378`
- `git status --porcelain` after each probe and at the end — empty

**Read**

- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/rounds/`: `round-1.md`, `round-1-report.md`
- the same work item's `spec.md`, `overview.md`, `changelog.md` and the four phase records, as changed by this diff
- `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` — the header comment and all four rows, cells named
- `seal/ledger.md` — rows R3, R4 and S1, `Checked` and `Notes` cells; `seal/follow-up.md` — the header and the extended row
- `skills/evidence-check/SKILL.md` §*Which reader graded your tree*, `CONTRIBUTING.md` §*Running the checks*
- `skills/verify/scripts/broad_gate.py` — `gate()` from its head through the failure loop and the `if failures:` branch
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` — `failure_loop` and the new case
- `skills/code-review/orchestration.md` §*New units* and `templates/sdd-round.md`, for what depth 1 means
- `skills/code-review/scripts/round_record.py` — `fix_table` and the rider in it
- `tests/test_docs_line_wrap.py` — `COVERED`
- `CLAUDE.md`, `agents/warden.md`, `skills/agent-contract/SKILL.md`

**Unverified**

- the full suite, the repository-wide lint and the typecheck — the sealer's, after the rounds settle (contract §2)
- `broad-gate`'s own end-to-end run on this branch — the sealer's
- `hooks/evidence-advisor.py` on a drifted tree — read, never run
