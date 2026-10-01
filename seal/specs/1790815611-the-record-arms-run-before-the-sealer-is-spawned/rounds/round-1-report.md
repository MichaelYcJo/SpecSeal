# Round 1 — review report, work item 1790815611 (#638)

Target `7ff69cb4` on `feat/638-the-record-arms-run-before-the-sealer-is-spawned`,
base `release/v0.17.0` at `cd24f516`, diff `cd24f516..7ff69cb4`. Reviewed in a
`git clone --no-local` of the branch at the target, under the round's own
scratch directory. Stage 1 against `spec.md` S1–S10 and `plan.md`'s phases,
then quality, with the gate attacked as a gate.

## Summary

The code does what S1–S10 ask. No path from `--preflight` reaches
`round_record.py seal`, the values file, the stamp, a `SEALED` line or a cell.
The arm list is the gate's own, and the row's refusals still apply. One claim
in the work item's records is false, and it was found by running it:

- The build says #535's `fixed at` instance, as today's generator writes it,
  "passes the preflight and the sealer" and fails only at a ready pull
  request. Run in the fixture, the preflight passes it (exit 0), and then the
  sealer's `round_record.py seal` refuses it with exit 2 — after every check,
  and so after the suite. That is exactly the cost #638 exists to remove, on
  the ticket's own instance, and the preflight does not remove it. The
  records point the owner's follow-up at the wrong place (🟡 1).

The rest is ⬜: an empty `--record` value that is not refused, a wall-clock
figure taken on a loaded machine, and the class enumeration.

## Stage 1 — spec compliance

**Ask 1 — a preflight can never seal.** Read and executed.

- `skills/verify/scripts/broad_gate.py:2342-2344` refuses `--record` beside
  `--preflight` before any arm runs. The checks happen after the row, base and
  HEAD refusals and before `keep` is made, so S4's "nothing run" holds. The
  argv order does not matter: argparse fills `args.record` either way. The
  same holds for `--record=X` and for every prefix abbreviation (`--rec`,
  `--reco`). `--r` is ambiguous with `--root`, so argparse refuses it with
  exit 2. `--pre` resolves to `--preflight` and is honoured.
- `broad_gate.py:2457-2459` returns 0 before `seal_record`, `panel`, the
  terminal drawing and `signal`. `broad_gate.py:2446-2456` returns 1 with the
  head replaced. So no preflight path reaches the values write or a stamp.
- The redirect in `main` (`broad_gate.py:2645-2652`) is decided by
  `parse_known_args`, so an older installed copy hands `--preflight` to the
  tree's copy unparsed. Run the other way, with a tree copy older than the
  running one, the old copy refuses the unknown flag with exit 2 and runs
  nothing. Either way nothing is sealed.
- Executed: with `if not args.preflight:` mutated to `if True:` and the
  `--record` refusal deleted, four of the seven preflight cases went red
  (S1, S2, S4, S7). Reverted afterwards.

**Ask 2 — the arms.** The suite's assignment sits under a condition, and
every other `checks[...] = run(...)` runs in both modes in the same order.
`PARTITION`, `SKIPPED_AT_MAIN` and `hygiene.yml` are untouched (`git diff`
names none of them). `skipped_at_main` is read before either mode's arms, so
a preflight at `main` leaves the same two arms out. `run` returns a `Check`
and does not raise on a non-zero child, so a failing arm does not stop the
ones after it. The failure loop collects every one of them, and S3 shows
the failure form under the preflight head. S1's `record_arms` reads the arm
list off `gate`'s AST rather than typing it, so an arm later placed under
the preflight condition turns S1 red. Executed: the preflight over this
clone kept `ledger`, `unverified`, `chain`, `survivors`, `corrections` and
`mode`, in that order.

**Ask 3 — the row's refusals and base resolution.** The preflight branch
sits below `missing_row`, `not_as_written`, the HEAD refusal and
`resolve_base`. `args.base` is still read once
(`tests/test_the_gate_asks_the_range_ci_will_ask.py`, green). S6's two cases
pass.

**Ask 4 — the orchestration text.** Read against the code, and true:

- `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens
  before round 1, and a phase is re-run*: the paragraph it points at, *A
  refusal about the `Broad gate` row goes to a person*, exists at line 581.
- `skills/implement/orchestration.md`'s order step and its acts-table Grounds
  cell, `skills/verify/SKILL.md`'s sentence, and `templates/config.md`'s row
  and prose all match the code. The docstring the template now points at
  lists arms 1–7 in run order.
- `tests/test_every_orchestrator_act_names_its_delivery.py` is green.

"A session that skips it loses only time" is true of the record arms. 🟡 1
is about what it does not ask.

**Ask 5 — left open by the build.**

- (a) **None of the 30.86 s is the preflight's own doing.** This round ran
  the preflight over the clone at the target: 10.79 s wall clock, exit 0. The
  `ledger` arm finished 6.62 s after start, and `evidence-check --strict .`
  run alone took 7.06 s. Nothing before the first arm costs anything
  measurable. The build's figure came from a run with two DRIFTED rows on a
  machine running other sessions. ⬜ 3 is about the figure shipping in the
  changelog.
- (b) **Half true.** Executed with a probe over the sealer module's fixture.
  Round 2 was generated with `fixed at <sha>` and left as `new` wrote it:
  `Fixes checked by` reads `nobody — the fixes are not yet written` beside a
  ticked `Pass`. The preflight exits 0 and `chain_check` on a draft exits 0.
  On a ready payload it exits 1. **The full gate with `--record` is not a
  pass**: every check passes, then `round_record.py seal` refuses with exit 2
  (`nobody` on the LAST record, where `no fixes to check` is the only value
  `seal` accepts). The record says the sealer passes it. The sealer does not,
  and it refuses after the suite. Whether the preflight should ask `seal`'s
  pre-write refusals is plan.md alternative E, which the spec scoped out, so
  building it is the owner's call (Deferred). Correcting the records is this
  branch's (🟡 1).
- (c) **S7 proves what S7 claims, and less than its label.** The case shows
  three things. The preflight runs `chain` under the draft payload. A
  `closed_with_a_fix` refusal comes back as `PREFLIGHT FAILED` with `chain`
  named. The row is never invoked. Its docstring says honestly that the cell
  is written by hand. What it cannot show is that the ticket's instance, as
  written today, is caught. Probe (b) shows it is not, and 🟡 1 carries that.

**Ask 6 — the ledger.** Executed in the clone: `bin/evidence-check .` exit 0,
`total: 3180 ok · 0 drifted · 0 broken`. `--strict .` exit 0. The handover
said 3152. The difference is a count and not a failure, and this round
counted 3180 at the target. All 27 re-stamp notes are dated 2026-10-01. Each
note names what moved in the anchored unit and why the claim still holds,
and the ones checked against the diff are true. They are the `gate` notes in
0.10.0, 0.12.0 and 0.15.7, the `main` notes, the orchestration and acts-table
notes, and the six `templates/config.md` notes. 0.15.7 N2's corrected claim
is true of the code: a green preflight writes and draws nothing and prints
`PREFLIGHT PASSED`. Its new clause is pinned by the fragment's P1 rather than
by an anchor in N2's own cell. That is allowed, so it is not a finding.

**Ask 7 — the class.** ⬜ 4 lists every place found. None is false, because
skipping the preflight costs only time. No other document says a green run
without `--record` prints `SEALED`: `broad_gate.py#signal`'s
`NOTHING_RECORDED` describes the full gate, and N2 was the one claim of that
shape, now corrected.

**Out of scope, read for merge safety.** The sibling branch for #666 changes
`skills/verify/scripts/seal_stamp.py#not_sealed`'s head to a composed name, and keeps it as the first
element of the list. `gate`'s `form[0]` replacement still lands on the head.
S3 and S7 assert both the `PREFLIGHT FAILED` start and that no line begins
`NOT SEALED`. So a merge that moved the head would turn them red rather than
ship silently. Whoever merges the second branch decides whether the preflight
head should carry the composed names too.

## Stage 2 — quality

### 🟡 1 — the records say the sealer passes #535's current shape, and it refuses it after the suite

`seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/overview.md:35`
and `phases/phase-2.md:36-47` state that a generated record with a verifying
round's `fixed at` "passes both the preflight and the sealer, which judge a
draft, and fails after the pull request is marked ready". Executed: the
sealer's run refuses it at `round_record.py seal`, exit 2, after every check
passed. The message is `round-2.md's Fixes checked by reads nobody — …, and
this is the LAST record, where no fixes to check is the only value seal
accepts`.

Why it matters:

- The ticket's own instance still reaches the sealer, and the suite runs
  before the refusal. The preflight was built to remove exactly that cost.
- The overview sends the owner to `chain_check`'s draft/ready asymmetry,
  when the gap is `seal`'s pre-write refusals. That is alternative E, which
  the overview's §*Not done* names for #456 alone.
- The changelog fragment lists "a chain refusal over a `fixed at` verdict"
  among the instances, beside a preflight that reads as their remedy.

A reader of the release notes would take that instance as caught early, and
it is not.

### ⬜ 2 — an empty `--record` beside `--preflight` is not refused

`broad_gate.py:2342` tests `if args.record:`, so `--record ""` or `--record=`
beside `--preflight` is taken as no record and the preflight runs. Nothing is
sealed, because `item` stays None. But S4 and the docstring say `--record`
beside the flag is refused. The full gate has always read an empty value as
absent. Read, not run.

### ⬜ 3 — the changelog ships 30.86 s as this repository's preflight time

`changelog.md`'s "On this repository it took 30.86 s, most of it the ledger
arm" is one measurement, taken during a run with drifted rows on a loaded
machine. This round measured 10.79 s at the target, with the ledger arm at
about 6.6 s. The overview's row saying "why the ledger arm costs that was not
measured" can now say it is `evidence-check --strict` alone: it costs the same
with the preflight around it as without.

### ⬜ 4 — the class: places that name the sealer's spawn with no step before it

None of these is false, and each is listed so the enumeration is on record:

- `skills/code-review/scripts/chain_check.py:3839`, `:3861` and `:4176`.
  Printed messages telling the reader to spawn the `sealer`. 0.10.0 S9 puts
  printed messages in the owner class.
- `README.md:56` and `README.ko.md:54`, the chain diagram's `sealer → broad
  gate`.
- `docs/review-chain-spec.md:567`, "Then the `sealer` takes the broad gate
  once". This is a policy document, and the spec left `settle` to fold it.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: a case that builds
  #535's shape the way `round_record.py new` writes it today (no hand edit).
  It runs the preflight and asserts exit 0, then runs the full gate with
  `--record` and asserts exit 2 with `no fixes to check is the only value`
  on stdout. It pins the fact 🟡 1 corrects. If alternative E is built, the
  first assertion flips to exit 1. Plant it only if the owner wants the
  current boundary pinned. Otherwise the corrected sentences are enough.

## Facts for the evidence ledger

- A verifying round whose verdict reads `fixed at <sha>`, generated by
  `round_record.py new` and not edited, passes `broad-gate --preflight`
  (exit 0). The full gate with `--record` refuses it at `seal` (exit 2) after
  every check has passed. Executed 2026-10-01 in this round's probe. The
  anchors are `skills/code-review/scripts/round_record.py`'s `seal`
  subcommand and `skills/verify/scripts/broad_gate.py#gate`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The records say #535's current `fixed at` shape passes the sealer and fails only at a ready pull request; the sealer's `seal` refuses it with exit 2 after every check, so the ticket's instance still costs a suite and the follow-up is pointed at the wrong place | `seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/overview.md:35` | open | executed: a probe over the sealer module's fixture, round 2 generated by `new` and not edited — preflight exit 0, chain on a draft exit 0, chain on a ready payload exit 1, full gate with `--record` exit 2 at `seal`; `phases/phase-2.md:36-47` and `changelog.md` carry the same claim |
| ⬜ 2 | `--record ""` beside `--preflight` is taken as no record rather than refused | `skills/verify/scripts/broad_gate.py:2342` | open | read: `if args.record:` is falsy on an empty value; no seal path opens, because `item` stays None |
| ⬜ 3 | The changelog ships one loaded-machine wall clock as this repository's preflight time | `seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/changelog.md` | open | executed: 10.79 s at the target in the round's clone, ledger arm about 6.6 s, `evidence-check --strict .` alone 7.06 s |
| ⬜ 4 | Three printed messages, both READMEs' chain diagram and the review-chain policy name the sealer's spawn with no step before it | `skills/code-review/scripts/chain_check.py:3839` | open | read; none is false, because skipping the preflight costs only time |
| 🟢 | No path from `--preflight` reaches `seal`, the values file, the stamp, a `SEALED` line or a cell, in any argv order, with `--record=`, with a prefix abbreviation, or through the tree-copy redirect | `skills/verify/scripts/broad_gate.py#gate` | confirmed | read; executed: two mutations turned four preflight cases red |
| 🟢 | The preflight runs every arm the full gate runs except the row, in order, `PARTITION` and `SKIPPED_AT_MAIN` unchanged, and a failing arm does not stop the others | `skills/verify/scripts/broad_gate.py#gate` | confirmed | executed: the preflight over the clone kept six arms in order; eight modules 373 passed |
| 🟢 | The row's refusals and base resolution apply under `--preflight` | `skills/verify/scripts/broad_gate.py#gate` | confirmed | read; S6's two cases green |
| 🟢 | The orchestration, verify and template text is true to the code, and the acts table still reads | `skills/code-review/orchestration.md` | confirmed | read; `tests/test_every_orchestrator_act_names_its_delivery.py` green |
| 🟢 | The ledger re-stamps and 0.15.7 N2's correction are true, and the whole ledger anchors | `seal/releases/0.15.7.md` | confirmed | executed: `evidence-check .` and `--strict .` exit 0, 3180 ok, 0 drifted |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the sealer module, `test_broad_gate_rule.py`, `test_the_rules_have_one_owner.py`, `test_the_gate_names_every_step_ci_runs.py`, `test_the_gate_asks_the_range_ci_will_ask.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `test_every_orchestrator_act_names_its_delivery.py`, `test_one_word_one_meaning.py` | exit 0, 373 passed |
| `bin/evidence-check .` and `bin/evidence-check --strict .`, unscoped, in the clone | exit 0 both, `3180 ok · 0 drifted · 0 broken`, about 7.1 s each |
| `broad_gate.py --preflight --base cd24f516` over the clone, outputs kept | exit 0, `PREFLIGHT PASSED   7ff69cb against cd24f51`, 10.79 s; arms finished at ledger 6.62 s, unverified 7.30, chain 7.55, survivors 10.64, corrections 10.73, mode 10.80 |
| A probe module (one file, run once, deleted): #535's shape generated by `new` and not edited, then the preflight, chain on draft and ready payloads, and the full gate with `--record` | preflight exit 0; chain draft exit 0; chain ready exit 1; full gate exit 2 at `round_record.py seal`, no cell written |
| Mutations: the row's condition read as `if True:`, and the `--record` refusal deleted; the preflight cases of the sealer module | 4 failed, 3 passed; reverted, clean tree |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The preflight does not ask `round_record.py seal`'s pre-write refusals, so #456's unchecked `Pass` and #535's current `nobody`-on-the-last-record shape both reach the sealer after a suite (plan.md alternative E) | a new issue, named in `overview.md` §*Not done* | the repository owner |

## Paste-ready fixes

### 🟡 1

In `overview.md` §*Not verified*, the third row:

```markdown
| A verifying round's `fixed at` verdict, as `round_record.py` writes it today, leaves `Pass` beside `nobody — the fixes are not yet written` on the last record. The preflight passes it (exit 0, executed in round 1), and the sealer's run refuses it at `round_record.py seal` with exit 2 after every check has passed, because `seal` accepts only `no fixes to check` on the last record (executed in round 1). So #535's instance, as written today, still costs a suite: it is a `seal` refusal, not a record-arm refusal, and the preflight does not ask `seal`'s refusals (`plan.md` alternative E) | the repository owner |
```

In `overview.md` §*Not done*, the first paragraph:

```markdown
A dry run of `round_record.py seal`'s three record refusals was not built
(`plan.md` alternative E). Two instances therefore still reach the sealer and
are refused after its suite: #456's unchecked `Pass` box, and #535's
`fixed at` in a verifying round as `round_record.py new` writes it today
(`nobody` on the last record, which `seal` refuses; round 1 executed it). It
is named here as a follow-up for the owner, as the plan asked.
```

In `phases/phase-2.md`, the paragraph headed *What the table means for the
ticket's instance*, replace from "So a generated record" to the end of that
paragraph:

```markdown
So a generated record with #535's verdict no longer reaches the chain arm as
a refusal: it passes the preflight. It does not pass the sealer.
`round_record.py seal` refuses `nobody` on the last record with exit 2, after
every check has passed (executed in round 1), so the instance still costs a
suite and is caught by `seal`, not by an arm. The preflight cannot catch it
without asking `seal`'s refusals, which `plan.md` alternative E left out.
This is written into `overview.md` §*Not verified* with the owner named.
```

In `changelog.md`, after "each found by the sealer after its suite.":

```markdown
  The preflight catches the record-arm refusals among them. A refusal that
  `round_record.py seal` raises, such as an unchecked `Pass` or `nobody` on
  the last record, still reaches the sealer.
```

### ⬜ 2

```python
    if args.record is not None:
        if args.preflight:
            raise Refused(PREFLIGHT_RECORD)
    if args.record:
        item = os.path.abspath(args.record)
        if not os.path.isdir(item):
            raise Refused(f"broad-gate: --record {args.record} is not a directory")
```

Needs a fix: yes — 🟡 1, the records' claim that the sealer passes #535's current shape

Loses a record or crashes: no

## Proof block

- spec: `seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/spec.md`, `questions.md`, `overview.md`, `phases/phase-2.md`, `changelog.md`, `plan.md` (alternatives table), `seal/ledger/1790815611-the-record-arms-run-before-the-sealer-is-spawned.md`
- code: `skills/verify/scripts/broad_gate.py` (docstring, `shipped_gate`, `draft_env`, `failure_lines`, `seal_record`, the preflight block, `gate`, `signal`, `main`), `skills/verify/scripts/seal_stamp.py#not_sealed`, `skills/code-review/scripts/chain_check.py` (`checked_by` head, `closed_with_a_fix`), `skills/code-review/orchestration.md` lines 515–580, `agents/sealer.md` lines 76–100, `README.md` lines 40–70, `docs/review-chain-spec.md` lines 555–600, `docs/the-broad-gate.md` lines 80–100
- tests: the diff of `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_broad_gate_rule.py`, `tests/test_the_rules_have_one_owner.py`
- ledger: the word diff of all twelve `seal/releases/*.md` files in the range, 0.15.7's changed rows in full
- executed: the probes table above; read: everything else; unverified: the full suite, repository-wide lint and typecheck, answered by the sealer
