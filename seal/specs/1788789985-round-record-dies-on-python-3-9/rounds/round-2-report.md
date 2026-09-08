# Round 2 — the verifying round · `1788789985-round-record-dies-on-python-3-9` (#226, PR #235)

Target `ea2aa70bc536f26d78772b34780676af01e256f9`, base `86e140f`, review
surface `git diff 2b8a50a..ea2aa70` — round 1's seven fixes plus the
orchestrator's two record commits. The worktree was clean at start and at
finish, and nothing was written in it except this file.

Every mutation ran in a `git clone --no-local` of this repository at `ea2aa70`,
under the scratchpad. Each was applied to bytes saved in the probe script and
restored from those bytes; every restore reports byte-identical, and the clone
is clean. The two probe scripts are deleted.

## How the pieces relate, before the detail

The round was asked to attack two refusals and two disclosed blind spots, and
those four are one chain rather than four items.

```
① The report offered a balanced-paren rewrite of the zip half.
   The fix pass measured it, found it a REGRESSION, and kept the shipped half.
        ↓ which leaves
② Two constructs the surviving pattern cannot see, named and NOT closed,
   routed to the owner under the 3+ Fix Rule.
        ↓ and separately
③ The report said nothing parses `seal/follow-up.md`. A test does, and it was
   already red — the report's own fix would have kept it red.
        ↓ and, found while measuring finding 4
④ `load` has a second bare traceback, left as a stamped `# RIDER:`.
```

**All four refusals hold, and I re-derived each rather than reading the
account.** What this round opens is elsewhere: four counts and coordinates in
the work item's own records that finding 1's fix corrected in some files and
not in others.

## ① The zip half was kept, and keeping it was right

**Executed.** I built both patterns and ran each over the shipped tree — 30
files, `git ls-files '*.py'` less `tests/` and `seal/`.

| | shipped `zip\(.*strict=` \| `\b\w+\.UTC\b` | the report's balanced-paren rewrite |
|---|---|---|
| files found in the tree | 6 | the same 6 |
| `zip(xs, f(g(y)), strict=True)` | **matched** | **missed** |
| `zip(` with `strict=` on a later line | missed | matched |

The fix pass's claim that both spellings find the same six files reproduces
exactly, and so does the regression it declined the rewrite for. The rewrite
trades a two-level nested call, which `round_record.py` is one edit away from
writing, for a multi-line call nothing in the tree writes. Declining it is the
better trade.

**Then the harder question: is there a construct in the class that BOTH
patterns miss?** I re-derived the class from the AST rather than from either
pattern — for every shipped file, each `alias.attr` resolved back to the stdlib
module its import binds and asked of the real 3.9.6 interpreter, plus every
`zip(…)` call carrying any keyword at any depth. Six members, the same six, and
no file the AST finds that neither pattern finds.

The construct both miss is the one the fix pass already named — `from datetime
import UTC` used bare. I confirmed it is absent from the tree, and I also swept
the shipped files for the other 3.10/3.11 names that would slip a text scan
(`tomllib`, `pairwise`, `StrEnum`, `TaskGroup`, `file_digest`, `bit_count`,  <!-- NAME NOT IN TREE -->
`contextlib.chdir`, `sys.stdlib_module_names`). No hit. The pattern's limit is
real and the tree does not exercise it.

## ② Not closing the two blind spots is the right call

The fix pass invoked the 3+ Fix Rule — three text spellings tried, each blind
one construct over — and routed the AST walk to the repository owner. I checked
the two halves of that separately.

- **Are the two genuinely absent?** Yes, measured. Neither a multi-line
  `zip(` nor a bare `UTC` exists in any shipped file.
- **Is the routing right?** Yes. An AST walk replaces the mechanism the check
  is built on, and `CONTRIBUTING.md`'s *What a change to a gate must carry*
  asks a separate argument for that. A fix pass adding one would be the change
  that arrives without its argument.

## ③ The `seal/follow-up.md` row was already red, and the report was wrong about it

**Executed, and this is the sharpest correction the fix pass made.** At
`2b8a50a`, before the fix pass touched anything:

```
bin/test tests/test_a_rider_reaches_its_file.py -q   → exit 1
FAILED test_no_schedulable_row_carries_a_coordinate
AssertionError: coordinate-tied rows in the schedulable list: [...]
```

So round 1's *"Nothing in the tree parses this file, so nothing catches it"* is
false, and the report's paste-ready fix — which added `session_cost.py:89` as a
sixth `file.py:NNN` — would have left that case red. The fix pass stripped the
coordinates instead and pointed the row at `spec.md`'s enumeration table.

Both halves are correct at `ea2aa70`:

- **The GFM half.** The blank line at 41 is gone, so the row is a row of
  *Schedulable items with nowhere else to go* and its answerer is a column
  again. Read against the file.
- **The coordinate half.** `bin/test` over both modules is `20 passed`, exit 0.

The two rules of that file — *name an answerer* and *anything tied to a
coordinate is a rider* — now hold together instead of one losing, and the row
says so in its own text.

## ④ A rider is the right disposition for `load`'s traceback

**Executed.** With `chain_check.py` deleted, the real script exits **1** with

```
FileNotFoundError: [Errno 2] No such file or directory: '.../chain_check.py'
```

and `spec_from_file_location('x', '/nope/does_not_exist.py')` returns a spec
with a loader, so the `SystemExit` sentence below it is unreachable from this
call site. The rider's claim is exact.

The question the round was asked is whether a rider is the right home for a
bare traceback in a work item whose thesis is *a bare traceback is the defect*.
I judge that it is, on three grounds.

- **The cause is a different one.** #226's class is *a shipped script meets an
  interpreter older than it needs*. This is *a sibling file is missing from the
  plugin cache* — same symptom, different cause, so §12 does not reach it.
- **The filing is what this repository's own rule asks for.**
  `seal/follow-up.md`'s opening sends anything tied to a coordinate to a
  `# RIDER:` at the line, and the rider is stamped `2026-09-08 at cedc58e` the
  way that rule requires.
- **The contract stopped lying, which is what round 1 actually asked for.**
  Finding 4 was that the docstring said exit 2 where the code exits 1. Both the
  module docstring and `load`'s now say 1, and both are true.

**One claim in the new paragraph I checked rather than took.** It says *"Those
are all three exits, enumerated from this module's own AST"*. There is a fourth
process exit the module's AST cannot see: `argparse` exits **2** on bad
arguments, which I measured directly (`--no-such-flag` → exit 2, no subcommand
→ exit 2). It lands on the code the paragraph already documents as *the input
was unusable*, so the contract is complete and the sentence is honest about its
method. Nothing to fix; recorded so a third round does not re-derive it.

## ⑤ The import exemption is the same deliberate one, and one case already covers it

The fix pass disclosed that the widened AST check sees only module-level
statements that *call* something, so an `ImportFrom` above the guard goes
unseen exactly as `Import` does. I judge that the same deliberate exemption
rather than a hole, and the reason is stronger than the one recorded: ruff's
E402 is selected, so a module-level import **has** to sit above the guard.
There is no placement the check could demand instead.

**But the guard block's own argument for it proves the wrong thing.** It says
the block sits after the imports *"because ruff's E402 is selected and every
shipped script was measured to compile under 3.9, so no import above it can
fail first"*. Compiling is not importing: `from datetime import UTC` compiles
on 3.9 and raises at import.

So I measured what actually catches it, and something does:

| Mutation above `FLOOR` | module suite | the real script on 3.9.6 |
|---|---|---|
| `from datetime import UTC` | **1 failed** — `test_the_script_refuses_at_entry_on_a_below_floor_interpreter` | exit 1, `ImportError` |
| `import tomllib` | **1 failed** — the same case | exit 1, `ModuleNotFoundError` |
| `_EARLY = os.path.abspath(__file__)` (round 1's control) | **1 failed** — the widened AST case | exit 2, the refusal |

- **What is covered** — an import above the guard that fails on 3.9, caught
  end to end on a machine that has a 3.9.
- **What is not** — the same mutation on CI. That case skips where no
  below-floor interpreter exists, which its own docstring says is every CI
  runner, and the raised-floor case that never skips runs on a new interpreter
  and so cannot see an import failure.
- **What it costs today** — nothing. I ran every module-level import of all six
  members of the class under 3.9.6: the only failures are sibling modules
  (`console`, `optin`) failing on `sys.path`, not on the version.

This is `agent-contract` §13 in miniature — a defence that holds only where the
platform supplies the guarantee — but it is disclosed twice already and costs
nothing on disk, so I am not commissioning a fix for it. Recorded as an answer,
not as a finding.

## ⑥ The three `NAME NOT IN TREE` markers exempt only their own lines

**Executed.** With the three markers stripped, `bin/evidence-check` exits **2**
with exactly three refusals, one per marked line, all of them `py_compile`:  <!-- NAME NOT IN TREE -->

```
NOT-IN-TREE  rounds/round-1-asked.md:5   `py_compile`
NOT-IN-TREE  rounds/round-1-report.md:38 `py_compile`
NOT-IN-TREE  rounds/round-1.md:23        `py_compile`
```

With the markers back, exit 0. The names-read count moves 50 → 47, three names
for three lines, so each marked line contributed exactly one readable name and
nothing else on those lines was hidden by the exemption. The marker is the
right instrument here: `py_compile` is a stdlib module the record names on  <!-- NAME NOT IN TREE -->
purpose, not a tree name the record got wrong.

## What this round opens — the count fix reached four files and not the fifth

Every finding below sits under `seal/specs/`, so each is a correction to the
run's paperwork rather than something the release ships. None of them is in
`Needs a fix`.

Finding 1's fix had to carry *six members, five deferred* into every record
that stated the old count. It reached `spec.md`, `changelog.md`, `questions.md`,
the ledger fragment and `seal/follow-up.md`. It did not reach `overview.md`,
and the fix pass's own two edits then made two more of its counts stale.

### ⬜ 9 · `overview.md` still says the class is five files where every other record says six

`seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:21`

The row reads *"the finding is about a class of five files, a rider at one line
cannot say **and four others**"*. The identical sentence in `questions.md:11`
was updated to *"a class of six files … **and five others**"*. Two records
state the same argument with different numbers, and the one that was left is
the one a reader opens first.

### ⬜ 10 · `overview.md` says the new module has eleven cases; it has twelve

`seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:6`

The line labels *eleven cases* as **executed**. `ed7f577` added
`test_the_refusal_is_ascii_because_it_is_written_before_stderr_is_set_up`, and
the module now reports `12 passed` — executed, in the clone at `ea2aa70`. A
count under an *executed* label is the kind of fact round 1's findings 1 and 6
were both about.

### ⬜ 11 · `overview.md` says twelve coordinates; the ledger fragment now carries thirteen

`seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:5`

`fb45bc1` added a seventh anchor to R1. `bin/evidence-check` reports
`seal/ledger/1788789985-round-record-dies-on-python-3-9.md — 13 ok · 0 drifted
· 0 broken`, executed at `ea2aa70`.

### ⬜ 12 · `spec.md`'s `removesuffix` bullet is the one coordinate the line-to-unit sweep missed

`seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:42`

The bullet cites *"`round_record.py:982`'s `removesuffix`"*. That call is at
`:1086`, inside `reach_back`. It was already 72 lines stale before the fix pass
(`:1054` at `2b8a50a`), and the fix pass then moved it a further 32 lines while
converting the other coordinates in the same file to units. A reader opening
`:982` lands on `def landing_values`.

This is round 1's finding 5 arriving a second time inside its own fix, which is
what `round-1-fixes.md` says happened to the §*Scope* citation as well. The
repair is the same one the fix pass already chose: name the unit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A sixth member of the class ships and the case written to stop a sixth cannot see it | `tests/test_a_script_says_which_interpreter_it_needs.py:466` (`:410` at round 1) | answered | Executed at `ea2aa70`: the shipped pattern and the report's rewrite each return the same six files, and an AST re-derivation against the real 3.9.6 returns the same six with no file that neither pattern finds. `session_cost.py` is in `CLASSIFIED`. The zip half was kept on measured grounds and the measurement reproduces — the rewrite misses `zip(xs, f(g(y)), strict=True)`, which the shipped half catches |
| 2 | The `seal/follow-up.md` deferral row is separated from its table, and its text says four | `seal/follow-up.md:41` | answered | Executed: `test_no_schedulable_row_carries_a_coordinate` exits 1 at `2b8a50a` and 0 at `ea2aa70`, so round 1's *"nothing in the tree parses this file"* was false and the report's own fix would have kept the case red. Read: the blank line is gone, the row is inside the table, the count is five |
| 3 | `test_the_guard_precedes_every_other_module_level_act` asserts against one act | `tests/test_a_script_says_which_interpreter_it_needs.py:374` (`:350` at round 1) | answered | Executed: `_EARLY = os.path.abspath(__file__)` above `FLOOR` is now red on that case (`module level calls abspath()`), where the shipped case was green against the same mutation |
| 4 | The rewritten exit-code paragraph reads as exhaustive for pre-write failures | `skills/code-review/scripts/round_record.py:99` | answered | Executed: the real script with `chain_check.py` deleted exits 1 with `FileNotFoundError`, and `spec_from_file_location` returns a spec with a loader for a path that does not exist — the rider's claim is exact. Both docstrings now say 1 and both are true. `argparse` exits 2 on bad arguments, measured, which lands on the code the paragraph already documents |
| 5 | `spec.md` cites pre-guard line numbers into `round_record.py` | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:28` | answered | Read against the AST: `#swallowed` is line 871, `#inherited_rows` 1039, `#signature` 1691 and 1695. The unit names resolve. One bullet in the same file was missed — finding 12 |
| 6 | The ledger fragment's R3 states a count that is wrong | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` | answered | Read: R3 now says six and five, names both surviving blind spots, and records the declined rewrite. Executed: `bin/evidence-check` exits 0, `777 ok · 0 drifted · 0 broken` |
| 7 | `BELOW_FLOOR`'s `§` is written before `__main__` reconfigures stderr | `skills/code-review/scripts/round_record.py:165` (`:158` at round 1) | answered | Executed: with the `§` put back, `test_the_refusal_is_ascii_because_it_is_written_before_stderr_is_set_up` exits 1 naming `['§']`. The new case is seen red against the defect it pins |
| 8 | The widened AST check cannot see an `ImportFrom` above the guard, as it cannot see an `Import` | `tests/test_a_script_says_which_interpreter_it_needs.py:374` | answered | Executed: `from datetime import UTC` and `import tomllib` above `FLOOR` each turn `test_the_script_refuses_at_entry_on_a_below_floor_interpreter` red and each makes the real script exit 1 on 3.9.6, so the module does catch them — on a machine that has a below-floor interpreter, which its docstring says no CI runner does. Read: E402 forces imports above the guard, so the exemption is not a placement the check could demand instead. Every module-level import of all six members of the class was run under 3.9.6 and none fails on the version |
| 9 | `overview.md` says the class is five files and *and four others* where `questions.md` says six and five | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:21` | open | Read: the same sentence in two records with different numbers. Finding 1's count fix reached `spec.md`, `changelog.md`, `questions.md`, the ledger fragment and `seal/follow-up.md`, and not this one |
| 10 | `overview.md` labels *eleven cases* as executed; the module has twelve | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:6` | open | Executed in the clone at `ea2aa70`: `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` reports `12 passed`, exit 0 |
| 11 | `overview.md` says the ledger fragment carries twelve coordinates; it carries thirteen | `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:5` | open | Executed: `bin/evidence-check` reports `13 ok · 0 drifted · 0 broken` for that fragment at `ea2aa70` |
| 12 | `spec.md`'s `removesuffix` bullet cites `round_record.py:982`; the call is at `:1086` in `reach_back` | `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:42` | open | Read against the AST: `removesuffix` is at 1086 now and was at 1054 at `2b8a50a`. The other coordinates in the same file were converted to units in the same commit |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py tests/test_a_rider_reaches_its_file.py -q` in the clone at `ea2aa70`, exit read with `; echo $?` and not through a pipe | `20 passed`, exit **0** |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` alone | `12 passed`, exit **0** — eleven at `804f14b`, twelve now |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` at `2b8a50a`, before the fix pass | exit **1** — `test_no_schedulable_row_carries_a_coordinate`, `coordinate-tied rows in the schedulable list`. Round 1's *"nothing in the tree parses this file"* is disproved |
| The same at `ea2aa70` | exit **0** |
| Both candidate patterns compiled and run over the 30 shipped `.py` | shipped: 6 files · the report's balanced-paren rewrite: **the same 6**. The fix pass's claim reproduces |
| The two patterns against nine synthetic constructs | `zip(xs, f(g(y)), strict=True)` — shipped **matched**, rewrite **missed**. Multi-line `zip(` — shipped missed, rewrite matched. `from datetime import UTC` used bare — **both missed** |
| Class re-derived from the AST: every `alias.attr` resolved to its stdlib module and asked of 3.9.6, plus every `zip(…)` with any keyword at any depth | **six** members, the same six. No file the AST finds that neither pattern finds; no file a pattern finds that the AST does not |
| Shipped tree grepped for `tomllib`, `pairwise`, `StrEnum`, `ExceptionGroup`, `TaskGroup`, `file_digest`, `bit_count`, `contextlib.chdir`, `sys.stdlib_module_names` | no hit — no other above-floor name the text scan would miss |  <!-- NAME NOT IN TREE -->
| Every module-level import of all six members of the class run under `/usr/bin/python3` (3.9.6) | the only failures are `import console` and `import optin`, sibling modules failing on `sys.path` rather than on the version |
| Mutation in the clone: `from datetime import UTC` inserted above `FLOOR` | suite exit **1**, `test_the_script_refuses_at_entry_on_a_below_floor_interpreter`; the real script on 3.9.6 exits **1** with `ImportError`. Restored byte-identical |
| Mutation: `import tomllib` above `FLOOR` | suite exit **1**, the same case; real script exits **1** with `ModuleNotFoundError`. Restored byte-identical |
| Mutation: `_EARLY = os.path.abspath(__file__)` above `FLOOR` (round 1's control) | suite exit **1** on the widened AST case; the real script still exits **2** with the refusal. Restored byte-identical |
| Mutation: the `§` put back into `BELOW_FLOOR` | exit **1** — `the refusal carries ['§'], which prints as an escape under an ASCII stderr`. The one new case is seen red against its own defect |
| The real script with `chain_check.py` deleted, at 3.13 | exit **1**, `FileNotFoundError` traceback. `chain_check.py` restored byte-identical |
| `spec_from_file_location('x', '/nope/does_not_exist.py')` | `spec: True · loader: True` — the `SystemExit` branch in `load` is unreachable from this call site |
| `round_record.py --no-such-flag` and with no subcommand, exits read directly | exit **2** both times — `argparse`'s exit is a fourth process exit the module's AST cannot see, and it lands on the code the docstring documents |
| Exit sites enumerated from `round_record.py`'s own AST | `raise SystemExit(2)` at 191, `raise SystemExit(<f-string>)` at 226, `sys.exit(main())` at 2284 — the docstring's three |
| `bin/evidence-check` at `ea2aa70` | exit **0** — `777 ok · 0 drifted · 0 broken`; the work item's fragment `13 ok` |
| The three `NAME NOT IN TREE` markers stripped, `bin/evidence-check` re-run | exit **2**, exactly three refusals, all `py_compile`, one per marked line; names read 50 against 47 with the markers. Markers restored, exit **0** |
| `bin/test tests/test_a_record_states_what_the_tree_has.py -q` at `ea2aa70` | `58 passed`, exit **0** — the checker the fix pass reported red is green with the markers in |
| The four `zip(…, strict=)` sites mapped to enclosing units from the AST | 871 `swallowed` · 1039 `inherited_rows` · 1691 and 1695 `signature` — `spec.md`'s new unit citations resolve |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1, finding 1 | `skills/verify/scripts/session_cost.py:89` | Still `dt.UTC`, still exits 1 on 3.9.6. Classified and deferred rather than fixed — the standing deferral, not a defect this branch introduced |
| round 1, finding 4 | `skills/code-review/scripts/round_record.py#load` | Carries the stamped `# RIDER:` for the `FileNotFoundError` path. Whoever next opens the function inherits it |
| a prior work item, round 2 finding 9 | `skills/code-review/scripts/round_record.py#fix_table` | The `` `fixed at <sha> — `` `` empty code span visible in this work item's `rounds/round-1.md` rows 1–7 is that finding's, already ridden and stamped `2026-09-06 at 9241a8b`. Not this branch's, and not re-opened here |
| the fix pass | `tests/test_a_script_says_which_interpreter_it_needs.py`, the class check | The two surviving blind spots and the AST walk that would close them are the repository owner's, per the 3+ Fix Rule |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Closing the pattern's two remaining blind spots with an AST walk | `seal/ledger/1788789985-round-record-dies-on-python-3-9.md` R3, `spec.md` §*The class, enumerated by construction*, and the pattern's own comment | the repository owner |
| The five remaining members of the class, still dying below the floor with a bare traceback | `seal/follow-up.md` §*Schedulable items with nowhere else to go* | the repository owner |
| Giving `load` a sentence instead of a `FileNotFoundError` traceback | `# RIDER:` at `round_record.py#load`, stamped `2026-09-08 at cedc58e` | whoever next opens `round_record.py#load` |

## Paste-ready fixes

**Finding 9** — `seal/specs/1788789985-round-record-dies-on-python-3-9/overview.md:21`, the *Where the deferrals go* row's last cell, matching the wording `questions.md:11` already carries:

```
`seal/follow-up.md`'s own opening says a repository with a tracker "should normally hold none of those", and that anything tied to a coordinate is a `# RIDER:` at the line. A rider was weighed and rejected: the finding is about a class of six files, a rider at one line cannot say *and five others*, and nobody opens `gather_changelog.py` before running it. Q1 leaves the tracker-versus-file call to the owner, and it changes where the row lives rather than what it says
```

**Finding 10** — `overview.md:6`, the executed clause:

```
· verified: **executed** — the new module's twelve cases, `tests/test_the_record_is_generated.py`'s 94, seven mutations of the guard, `python3 -m py_compile` at 3.9.6 over every shipped `.py`, the real script under 3.9.6 before and after, `ruff check` and `ruff format --check` on the two changed files. **Unverified** — the full suite, the repository-wide lint and the typecheck, which `agent-contract` §2 reserves for the orchestrator
```

**Finding 11** — `overview.md:5`:

```
· evidence: three rows in `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`, thirteen coordinates, all resolved by `evidence_check --reverify`
```

**Finding 12** — `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md:42`:

```
- **`round_record.py#reach_back`'s `removesuffix`** is 3.9 and is not part of this.
```

## What I did not verify, and who answers it

- **The full suite, the repository-wide `ruff check` and the typecheck** —
  `unverified`. `skills/agent-contract/SKILL.md` §2 reserves the broad gate;
  the **orchestrator** answers. I ran four modules narrowly, named in the probe
  table, plus `bin/evidence-check`. **Broad gate: not yet**, at any SHA on this
  branch — and with nothing open that needs a fix, it is the next step.
- **Behaviour on an interpreter older than 3.9.6** — `unverified`. This machine
  has nothing older, and the ledger fragment already says so. The **repository
  owner** answers it as part of the deferral.
- **Whether `hooks/root-migrate.py:425` is reached while migrating a 0.3.x
  layout** — `read`, carried from round 1 rather than re-derived. The
  **repository owner** answers it as part of the deferral.
- **❓ out of verified scope — none.** Nothing in my prompt asked for a check
  §2 excludes, so there is no declined instruction to name.

Needs a fix: no
Loses a record or crashes: no

Nothing this round found leaves the root or crashes, and nothing it found needs
a fix — findings 9 to 12 are corrections to the run's own records under
`seal/specs/`. One crash still stands in the tree and it is not this round's:
`skills/verify/scripts/session_cost.py:89` exits 1 on 3.9.6 with a bare
`AttributeError`. Round 1 found it, this branch classified it, and it is
deferred to the repository owner with a row in `seal/follow-up.md` — a decision
recorded rather than a defect introduced.

Contract changes: none. `load`'s signature is unchanged; only its docstring and
the rider above it moved.

New units: `test_the_refusal_is_ascii_because_it_is_written_before_stderr_is_set_up` (depth 1).

## Proof block

Opened, in the worktree and in the clone at `ea2aa70`:

- `git diff 2b8a50a..ea2aa70`, whole, split into its code and document halves
- `git show 011beb1`, `git show ea2aa70`
- `skills/code-review/scripts/round_record.py` (module docstring, the guard
  block, `below_floor`, the rider and `load`, `fix_table`, `reach_back`, the
  four `zip` sites)
- `tests/test_a_script_says_which_interpreter_it_needs.py` (module docstring,
  `generator`, `test_the_refusal_is_ascii_…`,
  `test_the_script_refuses_at_entry_on_a_below_floor_interpreter`,
  `test_the_guard_precedes_every_other_module_level_act`, `ABOVE_THE_FLOOR`,
  `CLASSIFIED`)
- `tests/test_a_rider_reaches_its_file.py` (whole file)
- `tests/test_docs_line_wrap.py` (`COVERED`)
- `skills/evidence-check/scripts/evidence_check.py#claim_lines`,
  `skills/evidence-check/SKILL.md` §the records arm
- `seal/follow-up.md` (opening and both tables)
- `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md`,
  `overview.md`, `questions.md`, `changelog.md`
- `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`
- `rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-1-fixes.md`,
  `rounds/round-1-asked.md`
- `.github/scripts/run_tests.py` (`FLOOR`), `bin/test`
- the module-level imports of `.github/scripts/gather_changelog.py`,
  `.github/scripts/fold_ledger.py`, `skills/implement/scripts/seal.py`,
  `hooks/root-migrate.py`, `skills/verify/scripts/session_cost.py`
