# Feature Specification: the record-before-the-fix sequence has no arm (#345)

<!-- seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

## The correction this spec starts from

**`written_late` is in `skills/code-review/scripts/chain_check.py:2415`, not in
`round_record.py`.** Issue #345's body, this work item's `routing.md`, and the
framing prompt all name it as `round_record.py`'s. It is not there and never
was: `round_record.py` reaches it only through `run_check`, which calls
`chain_check.main`. The work therefore spans **two** scripts, and the issue's
one-line proposal — *move the check* — is not available. §5 of
`skills/agent-contract/SKILL.md` is why this is the first paragraph: three
documents carried the same coordinate and none of them resolved.

**A second correction, smaller and load-bearing.** The issue says the refusal
*"only ever speaks at the pull request"*. It also speaks at the **next round's
`new`**: `round_record.py new` ends in `run_check`, which runs
`chain_check.main --worktree` over every record in the work item, and round N's
record is committed by then. So the true statement is *the refusal cannot speak
about the record being written, only about the ones already committed* — one
round late rather than one pull request late. One round late is still after the
fix pass has read nothing, and still after the point where any repair exists,
so the defect stands. The accuracy matters because it names what the fix has to
change: not *when chain_check runs*, but *what is computable about a record
that has no commit yet*.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | This changes a gate's verdict and adds a pass state to one. The pull request owes that section's answers, and it is why `routing.md` reads *through the review chain* |
| `docs/review-chain-spec.md` §*When the record was written — before the fixes it commissioned* | The states table this work extends. Every state it lists stays true; the work adds rows and removes none |
| `skills/code-review/orchestration.md` §*And commit the record before commissioning the fixes* | The prose sequence that exists and has no arm. This is the sentence the work is trying to stop being only a sentence |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides between the candidate shapes: the one that stops to ask a person is the more expensive, and the difference has to be argued |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to this directory's `changelog.md` and the ledger rows to `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md` |
| `agent-contract` §12 | The defect is a class. The enumeration is below, by construction, and it is finite and small |
| `agent-contract` §14 | The refusal text is read by a person, so it is documented and pinned in the same commit |
| `agent-contract` §15 | Every case this commissions is seen red before it is planted |
| `skills/implement/SKILL.md` §3, top rung | A gate's verdict and the moment it is delivered. `spec.md` and `plan.md` both required |

## The class, enumerated by construction

The class is *a check the orchestrator could act on for free speaks only at the
pull request*, scoped as the framing prompt scoped it: what the
pull-request-time checks verify **about round records**.

**What runs against round records at the pull request is one step.**
`.github/workflows/hygiene.yml:191` runs `chain_check.py`. The step above it
(line 184) fetches the pull-request heads a record may name and checks nothing.
No other hygiene step reads a `rounds/round-N.md`.

**So the class is `chain_check.main`'s per-record loop**, and every member of it
is already reachable at `new` — because `new` ends in `run_check`, which is
`chain_check.main --worktree` over the work item. Enumerated over the loop body
and `check_round`, asking of each what it reads:

| Per-record check | What it reads about the record | Answers at `new`, on the record just written? |
|---|---|---|
| `checked_by` | `read_record` (the text) | yes |
| `fix_surface` | `read_record` | yes |
| `stopping_floor` | `read_record`, plus later records' text | yes |
| `ran_by` | `read_record` | yes |
| `broad_gate` | `read_record`, plus ancestry of SHAs the record's own cells name | yes — `not yet` is the honest early value and the check says so |
| `check_round` | `read_record`, the `Target SHA` row, the `Pass` box, `open_blocking` | yes — `run_check` supplies the draft state so an unticked `Pass` is not an error |
| **`written_late`** | **`added_on_branch` — `git log --diff-filter=A <base>..HEAD -- <rel>`** | **no** |

`written_late` is the one member, and the cause is one function.
`added_on_branch` asks git for the commit that added the record. A record `new`
has just written is not committed, so `git log` returns nothing,
`added_on_branch` returns `None`, and `written_late` returns `([], [])` — it is
already being called at `new` and is already silent there. **Nothing has to be
moved; something has to be computable.**

**What this work item closes:** that one member.

**What it does not close, each with the reason:**

- **`skills/code-review/orchestration.md` §*Verify before posting*'s
  instruction to check whether HEAD moved during the review.** The same
  computation phase 2 adds answers it, and the fact becomes visible. Acting on
  it — deciding the verdicts need a re-pass — stays the orchestrator's
  judgment and gets no arm here. Named because one computation now serves two
  remembered sentences, and only one of them is being armed.
- **Every other hygiene step** — issue claims, the version bump, the changelog
  and ledger folds, `unverified_check`, `survivor_check`, release
  completeness, `seal mode`, the `CLAUDE.md` block, both READMEs. These are
  members of #330's wider class and not of the class as scoped here: none of
  them reads a round record. Each is its own work item.
- **The rest of #330** — the broad gate's spelling, posting a segment's
  reading to the flow log, asking the routing question in one batch. Named in
  that issue, out of scope here.
- **#318, a `bin/` wrapper for `round_record.py`.** Scheduled into 0.11.4 and
  explicitly not this work item's.

## Scope

**In.**

1. `round_record.py new` observes one fact it does not observe today: whether
   the resolved `--target` is the branch's HEAD. Today `build` only checks
   that `--target` resolves (`reader.resolves(root, args.target)`); nothing
   compares it to anything.
2. Where they differ, `new` says so, in the terms the orchestrator has to act
   in: the commits that landed since the reviewer read the target, and the two
   things that can mean.
3. One escape, carrying a written reason, so the check is not a gate with no
   honest way past it. The reason reaches the record, so a state that today
   leaves no trace leaves one.
4. `chain_check.written_late` gains one **pass** state for a record carrying
   that reason: it prints instead of failing.
5. The documentation and the pins: `docs/review-chain-spec.md`'s states table,
   `skills/code-review/orchestration.md`'s sequence section,
   `templates/sdd-round.md`, and cases pinning each.

**Out, with the reason beside each.**

- **Moving `written_late` to `new`, as #345 proposes.** Its two inputs — the
  record's adding commit and the fix SHAs in its own verdict cells — do not
  exist at `new`. The cells read `open` by construction, and the file is not
  committed. A `new` that called it would ship a check that returns `([], [])`
  every time, which is the counterfeit seal `skills/verify/SKILL.md` refuses.
- **Running `written_late` at `close` instead.** `close` is the first moment
  both inputs exist, and it is still after the fix pass. It would detect
  earlier and prevent nothing, and a refusal there blocks the record's own
  update — leaving the round with stale `open` cells. Rejected in `plan.md`'s
  alternatives table with the failure scenario.
- **`new` committing the record and its report itself.** #330's evidence
  favours performing the act over remembering it, and this is the shape that
  would. It is out because `new` returns `run_check`'s exit code and that code
  is legitimately non-zero mid-run, so `new` would either commit a record the
  check just refused or decline and be back to a sentence. It is a separate
  decision with its own gate-change obligations; it belongs in an issue, not
  inside this one.
- **Any change to `written_late`'s existing refusal states.** All eight rows
  of `docs/review-chain-spec.md`'s states table stay true. This work adds a
  ninth and edits none.
- **A new `ORDER_FROM`-style cutoff constant.** The convention
  (`test_the_cutoff_is_this_work_items_own_id`) keys a cutoff to the work item
  that added a **refusal**. Phase 2's refusal fires inside a live run and is
  never applied to a record that already exists, and phase 4's new state is a
  **relaxation** — a record without the reason is judged exactly as it is
  today. Neither owes a cutoff. Stated because a reviewer will ask.
- **#318's `bin/` wrapper**, and **anything about how the fix pass is
  dispatched.** The fix pass is a spawn and has no command for an arm to sit
  on, which is why `new` — the last command before it — is where this lands.

## Naming constraint, because two words are already taken

`tests/test_one_word_one_meaning.py` refuses a word used for two things, and
`CLAUDE.md` §*a thing more than one party can have is named with whose* is the
rule behind it. Two candidate words are already spent in these exact files:

- **declaration** means `routing.md`'s, throughout `chain_check.py`
  (`tracked_declarations`, `declared_for_this_branch`, `nothing_declared`).
  The new reason is not one.
- **arm** means a branch of a check a mutation should kill
  (`skills/verify/scripts/arm_check.py`, `bin/arm-check`) and also the commit
  gate's review arm. #345's own title uses it in a third sense. Do not coin
  with it.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 the ordinary correct round | Given the branch's HEAD is the commit the reviewer read · When `new --target <HEAD>` runs · Then nothing new is printed and the record is written exactly as today | A case asserting the record's bytes and the printed lines are unchanged from the current output, seen red by making the new observation fire unconditionally |
| A2 the fix pass ran first | Given fix commits landed after `--target` · When `new` runs · Then it refuses, naming the commits between, both meanings, and the escape | A case on a three-commit fixture, seen red by reverting the observation |
| A3 the escape writes a trace | Given A2's state · When `new` runs with the escape and a reason · Then the record is written and carries the reason | A case reading the written record's cell, seen red by having the escape write nothing |
| A4 an empty reason is refused | Given A2's state · When the escape carries an empty or whitespace reason · Then `new` refuses | A case, seen red by dropping the emptiness test. This is the shape `nobody — <why>` and `unknown — <why>` already take |
| A5 the declared record passes at the pull request | Given a record carrying the reason whose adding commit descends from its own fix · When `chain_check` runs · Then it prints and does not fail | A case in `tests/test_a_record_precedes_the_fixes_it_commissions.py`, seen red by having `written_late` ignore the cell |
| A6 an undeclared late record still fails | Given the same record without the reason · When `chain_check` runs · Then it fails exactly as today | The existing `test_a_record_added_after_its_own_fix_fails_after_the_cutoff`, still green and unmodified |
| A7 `close` does not lose the reason | Given a record carrying the reason · When `close` applies a fix table · Then the reason is still there | A case, seen red by having `close` rewrite the field block wholesale |
| A8 the refusal text is documented and pinned | The new message and the new pass state appear in `docs/review-chain-spec.md`'s states table, `skills/code-review/orchestration.md` and `templates/sdd-round.md` | Cases of the shape `test_the_spec_carries_the_subsection` already in the module — `agent-contract` §14 |

A2's verdict — refuse, or print and continue — is set by phase 1's
measurement, not by this table. The table's wording says *refuses* because that
is the default the plan carries in; `questions.md` Q1 holds the criterion that
can overturn it.

## Data & interfaces

- `round_record.py`, `new` subparser: one new flag, plus `git rev-parse HEAD`
  through the existing `git(root, *args)` helper at line 848. `--target` is
  already resolved by `reader.resolves`; nothing else about the signature
  moves.
- `chain_check.py`, `written_late` at 2415: one new early return, keyed on a
  value read from the record's own field table through the existing
  `table_rows` / `field` pair.
- `templates/sdd-round.md`'s field block: where the reason lives. The template
  already asks `Target SHA` to hold *both, if HEAD moved mid-review*, and
  `check_round` already accepts more than one SHA there (`SHA_RE.findall`), so
  one of the two candidate homes exists already. `questions.md` Q3 is which.

## Open questions → questions.md

Four rows, in `questions.md` beside this file: one a measurement that phase 1
takes, one a person's, two the work's.
