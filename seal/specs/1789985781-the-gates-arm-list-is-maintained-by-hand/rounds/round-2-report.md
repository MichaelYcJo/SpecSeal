# 1789985781-the-gates-arm-list-is-maintained-by-hand — review round 2 report

Round 2, the verifying round. Target SHA `9637b43eaa4f5f664f032a1594ec1c721dcc62fd`,
over the fix range `8ac8dd93b0750ab297db6efd2da721ece5da648d..c0b0d7120cf1b4e57082efeb2ec36b2beebaa3df`,
three commits. Reviewed in a `git clone --no-local` at that SHA; the tree under
review was read and never written.

Round 1 did not meet the floor — its second terminal line read
`Loses a record or crashes: yes`, for finding 5. **This round meets it.** The
crash is closed, reached rather than read: the pre-fix unit raises and the
post-fix unit returns a value, measured side by side out of git.

## What this round opened

One 🟡, and it is round 1's finding 2 **one class wider than the fix went**.

### 🟡 1 · The class round 1 corrected has two more instances, and one of them ships

`skills/verify/SKILL.md:352-355` and
`seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:29`
each attribute the class *whether a mirrored arm asks the same question its
step asks* to **#423**. That is the attribution round 1's finding 2 rejected,
and both lines are new on this branch.

The fix at `c0b0d71` corrected four coordinates — `spec.md:119`,
`overview.md:97`, `phases/phase-2.md:39` and ledger row G4 — and reported the
enumeration as a widening from the two the paste-ready fix named. The
enumeration stopped two short of the class.

**Why it costs something, and why the shipped copy is the one that matters.**
`gh issue view 423` reports state OPEN, milestone `release: 0.12.2`, so #423
closes when this release reaches `main`. `gh issue view 473` reports state
OPEN, milestone `backlog: gates & hooks` — a durable home, opened by this fix
pass for exactly this fact. `skills/verify/SKILL.md` ships to every repository
that installs the plugin: within days of the release it will tell every reader
of the sealer's own skill to go to a closed issue for a class that issue never
held. That is finding 2's defect in the most durable of its six copies, and it
arrived in the same commit range that repaired the other four.

`questions.md:29` is the second coordinate and the lighter one — it records
what the framing settled, and a reader may argue the frame's belief is what
that file is for. `spec.md` is also a frame document and was corrected there
in so many words (*The frame named #423 here, and review round 1 corrected
that*), so leaving the sibling uncorrected leaves the branch saying both
things.

## What this round verified, and how

### Round 1's finding 5 — reached, not read

`workflow_text` was driven directly against a `release` job written in
latin-1, in both versions of the file, the pre-fix one written out of git:

- pre-fix (`8ac8dd9`): raised `UnicodeDecodeError: 'utf-8' codec can't decode
  byte 0xe9 in position 45: invalid continuation byte`
- at the target SHA: returned `None`, and `coverage_line` on that answer
  returned `None`

The case that pins it is red against `except OSError` alone and nothing else
is — see the mutation table below.

### The mutation anchor trap — measured across the file, not taken on account

The overview reports a 24th mutation that missed its anchor. That is accurate
and it is worse than the account suggests: **it fails silently.** A naive
first-occurrence replace of `    except (OSError, ValueError):` lands at
`broad_gate.py:463`, inside `config_text`, and leaves the module green at exit
0 with nothing red — so a reviewer reading the result sees *the mutant
survived* where the mutation never reached the unit.

I then went looking for every other anchor in the file that could do the same.
`broad_gate.py` carries 23 non-trivial duplicated lines; the ones a mutation
this branch reports could plausibly have targeted are three:

| Ambiguous anchor | Lines | What a first-occurrence replace does |
|---|---|---|
| `    except (OSError, ValueError):` | 463, 1423 | **silent** — module green, nothing red |
| `            return handle.read()` | 462, 1422 | loud — 7 cases red, none of them the intended one |
| `        CORRECTIONS_NAME,` | 1373, 1735 | loud — 12 cases red, the `PARTITION` tuple broken |

Only one anchor in this file can report a passing case as evidence of a pin
that does not exist, and it is the one the branch found. Every other mutation
the branch reports either has a unique anchor or fails loudly enough that a
mis-landing could not have been written up as *reddens it alone*.

### The four new units, judged as code rather than as fixes

`test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`,
`test_a_step_no_row_classifies_is_not_said_to_carry_a_reason` and
`test_a_step_a_row_excludes_is_still_pointed_at_its_reason` each go red on
their own mutation and on no other case's. Driven, one mutation at a time,
restored from bytes kept outside git.

`test_a_step_a_row_excludes_is_still_pointed_at_its_reason` **is
load-bearing, and the question it answers is the right one.** Without it, the
cheapest repair for finding 3 is to delete the pointer to `PARTITION` from the
excluded half — and
`test_a_step_no_row_classifies_is_not_said_to_carry_a_reason` stays green
through that edit: its `said.split("no arm mirrors it in", 1)` collapses to
one element, its own `or` clause passes, and the clause it asserts lives in
the other half of the sentence. So finding 3 would have closed with
`spec.md` §Scope 5's whole deliverable deleted. The case was written green and
shown red by deleting the pointer, which is §15 satisfied by the only means
available: the behaviour it pins already existed.

`UNCLASSIFIED_WORKFLOW` is a fixture and it is correct — `jobs:` at column 0,
the job key at two spaces, one step name `PARTITION` carries and one it does
not, and neutral values throughout.

### Round 1's finding 1 — the audit, not the edit

`Six of the eight` now stands nowhere in the tree except round 1's own
quotation of the finding and its paste-ready fix. The new split is true of the
workflow, checked step by step against `.github/workflows/hygiene.yml` rather
than against any record:

- **could not run here at all (4)** — the pull request's body
  (`issue_claims_check.py`, which reads `PR_BODY` and whose only exit is
  `return 0`), the fetch of `refs/pull/*/head`, the tracker
  (`release_completeness_check.py` through `gh`), and *both READMEs move
  together*, whose entire body emits `::warning::` and never exits non-zero
- **could run here (4)** — *a change to what ships must move the version*,
  which is inline `bash` with no script, and the three that run
  `gather_changelog.py`, `fold_ledger.py` and `claude_block.py`

The two copies the builder reports as *tightened from an `or`* are
`changelog.md:31` and the `overview.md` divergence row; the five it reports as
already exact are exact. The audit holds.

### Round 1's finding 4

`.github/workflows/hygiene.yml` declares `jobs:` at line 24 with `release:` as
its only key. `lint`, `pytest` and `ledger` are jobs of
`.github/workflows/test.yml`. The corrected assert message and the corrected
`spec.md` §Scope Out row both say so.

### Round 1's finding 2, on its own grounds

#473 exists, is OPEN, and sits in `backlog: gates & hooks` rather than in a
release milestone. Its body carries the measurement and names both arms. The
deferral has a home that outlives 0.12.2 — for the four coordinates the fix
reached. 🟡 1 above is about the two it did not.

### The divergence from the paste-ready fix — sound

Round 1 proposed a `seal/follow-up.md` row for the guard divergence and the
builder declined it, on the grounds that #473 already exists and that file's
own rule prefers a tracker. That reading is right. `seal/follow-up.md`'s
header states that a schedulable item belongs there only *in a repository with
no tracker*, and a fact with an open issue and a row in that file has two
homes, which is the state finding 2 was about. The row this branch **did** add
to that file is a different shape — it names no ticket, because none exists
for it.

### The trailing-comment claim — checked

`tests/test_ci_gives_the_checks_what_they_need.py#strip_comments` keeps a line
unless `line.lstrip().startswith("#")`, so a trailing ` # why` survives it
exactly as it survives `job_steps`. The gap is shared with the reader
`job_steps` follows, and the branch did not open it. Recording it as a
correction and writing it into the docstring is the right disposal.

### `workflow_text` swallows nothing it should surface

The `try` block holds `os.path.join`, `open` and `read` and nothing else. The
only `ValueError` reachable besides `UnicodeDecodeError` is `open`'s *embedded
null byte* for a root the rest of the gate could not use either. And the pair
is not a widening this branch invented: `config_text` at `broad_gate.py:458`
— the same three lines, nine hundred lines earlier in the same file — has
caught `(OSError, ValueError)` since before this work item. The fix follows the
file's own idiom.

### The new sentence cannot be misread

Driven on both shapes. Against the real workflow the line carries one clause;
against a mixed repository it carries two, and the two populations are named
apart with no name in both:

> …runs 4 steps and this seal answers 1. Not answered, each with the reason no
> arm mirrors it in `broad_gate.py#PARTITION`: both READMEs move together. In
> no row of `broad_gate.py#PARTITION` at all, so this gate has no reading of
> them and answers nothing for them: deploy to staging; notify the channel.

### The ledger fragment rows after the drift

`evidence_check.py .` unscoped: exit 0,
`total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`. The three
re-anchored coordinates — `job_steps@afc42ebb`, `coverage_line@f3dd1189`,
`workflow_text@1f3fd87c` — all resolve.

Round 1's ⬜ about R2's line number is closed: the row now reads *the
`resolve_base(root, args.base)` call* in place of *line 1633*. That spelling
occurs exactly once in the file, and the count the claim rests on still holds
— `args.base` appears three times (`:1611`, `:1665`, `:1670`) and exactly one
of them is a read. The line it used to name has since moved to 1670, which is
the rot the correction removed, arriving inside one release.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The class round 1's finding 2 corrected has two more instances, and the fix reached neither. Both attribute *whether a mirrored arm asks its step's question* to #423, which is milestone `release: 0.12.2` and closes with this release; #473 is the home the same fix pass opened. `skills/verify/SKILL.md` ships to every installation | `skills/verify/SKILL.md:352-355`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/questions.md:29` | open | Both lines are new on this branch. `gh issue view 423` — OPEN, milestone `release: 0.12.2`; `gh issue view 473` — OPEN, milestone `backlog: gates & hooks`, body naming both arms and the guard. The four coordinates the fix did reach say the opposite of these two, so the branch states both things |
| 🟢 | Round 1's finding 5 is closed, reached rather than read | `skills/verify/scripts/broad_gate.py:1423` | answered | **Executed.** `workflow_text` driven against a latin-1 `release` job in both versions of the file, the pre-fix one written out of git: `8ac8dd9` raised `UnicodeDecodeError ... byte 0xe9 in position 45`; the target SHA returned `None`, and `coverage_line` on that answer returned `None`. The case is red against `except OSError` alone and is the only case that is |
| 🟢 | Round 1's finding 1 is closed, and the audit behind it holds rather than only the edit | `skills/verify/scripts/broad_gate.py:1310` | answered | **Executed and read.** `Six of the eight` survives nowhere but round 1's own quotation of the finding. The 4/4 split checked step by step against the workflow: *both READMEs move together* emits `::warning::` and never exits non-zero; `issue_claims_check.py`'s only exit is `return 0`; the version-bump step is inline `bash` with no script; three steps run `.github/scripts/` scripts. Two copies tightened from an `or`, five already exact |
| 🟢 | Round 1's finding 3 is closed, and both halves are pinned | `skills/verify/scripts/broad_gate.py:1467`, `tests/test_the_gate_names_every_step_ci_runs.py:781` | answered | **Executed.** Merging the two populations back reddens `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason` and nothing else; deleting the `PARTITION` pointer from the excluded half reddens `test_a_step_a_row_excludes_is_still_pointed_at_its_reason` and nothing else. Without the second case the first stays green through the pointer deletion, so the second is load-bearing rather than decorative |
| 🟢 | Round 1's finding 4 is closed | `tests/test_the_gate_names_every_step_ci_runs.py:284`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:79` | answered | **Read.** `.github/workflows/hygiene.yml` declares `jobs:` at `:24` with `release:` as its only key; `lint`, `pytest` and `ledger` are jobs of `.github/workflows/test.yml`. Both corrected sentences say exactly that |
| 🟢 | Round 1's finding 2 is closed for the four coordinates the fix reached, and #473 is a durable home | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G4 | answered | `gh issue view 473`: OPEN, milestone `backlog: gates & hooks`, body carrying the measurement and naming both arms. The two coordinates the fix did NOT reach are finding 1 above |
| 🟢 | No other mutation this branch reports could have landed silently somewhere other than where it was aimed | `skills/verify/scripts/broad_gate.py` | answered | **Executed.** The file carries three ambiguous anchors a reported mutation could have used. `    except (OSError, ValueError):` lands at `:463` in `config_text` and leaves the module GREEN — the silent trap, and the one the branch found. `            return handle.read()` lands at `:462` and reddens 7 cases; `        CORRECTIONS_NAME,` lands at `:1373` in `PARTITION` and reddens 12. Both of those fail too loudly to have been written up as *reddens it alone* |
| 🟢 | The new `UNCLASSIFIED_WORKFLOW` path prints nothing a reader misreads | `skills/verify/scripts/broad_gate.py:1467` | answered | **Executed** on both shapes. Against the real workflow one clause; against a mixed repository two, with no step name in both and each clause saying plainly which population it holds. The panel count is unchanged and says only how many are unanswered, which is true whatever the reason |
| 🟢 | `workflow_text` swallows no error it should surface, and the widened catch is the file's own idiom | `skills/verify/scripts/broad_gate.py:1408` | answered | **Read.** The `try` holds `os.path.join`, `open` and `read` alone; the only other reachable `ValueError` is `open`'s embedded-null-byte refusal for a root the rest of the gate could not use. `config_text` at `:458` has caught `(OSError, ValueError)` since before this work item |
| 🟢 | The builder's divergence from the paste-ready fix on finding 2 is sound | `seal/follow-up.md` | answered | **Read.** That file's own header admits a schedulable item only *in a repository with no tracker*; #473 is open and durable, and a second home for one fact is the state finding 2 was about. The row this branch did add there names no ticket, so it is the shape the file admits |
| 🟢 | The trailing-comment gap is shared with the reader `job_steps` follows, so the branch did not open it | `tests/test_ci_gives_the_checks_what_they_need.py:37` | answered | **Read.** `strip_comments` keeps a line unless `line.lstrip().startswith("#")`, so a trailing ` # why` survives it exactly as it survives `job_steps`. Recording it and writing it into the docstring is the right disposal |
| 🟢 | The ledger fragment rows resolve after the three re-anchorings, and round 1's line-number correction holds | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md` R2 | answered | **Executed.** `evidence_check.py .` unscoped: exit 0, `1398 ok · 0 drifted · 0 broken`. `resolve_base(root, args.base)` occurs once; `args.base` three times at `:1611`, `:1665`, `:1670`, exactly one a read. The line the row used to name has already moved to 1670, so the rot the correction removed was live |
| ⬜ | Two ledger fragment rows say the fix pass *widened the claim*, and no Claim cell was edited. G7 still reads *A repository with no `.github/workflows/hygiene.yml`*, which a latin-1 workflow is not; G6's claim says nothing about the two populations. The widening lives in Notes only | `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` G6, G7 | correction | Under-claim rather than over-claim, so nothing in the ledger is false — but a re-reader auditing G7 against its Claim never reaches the case the third test pins, and the Claim column is the checkable half |
| ⬜ | No case renders both clauses of the new coverage sentence together. `UNCLASSIFIED_WORKFLOW` leaves `excluded` empty and the real workflow leaves `unknown` empty, so the joined sentence a mixed repository actually gets is pinned by nothing | `tests/test_the_gate_names_every_step_ci_runs.py:743` | correction | Driven by hand and correct — the two comprehensions are disjoint by construction, so this is a coverage note and not a defect. Recorded because the mixed sentence is the one a reader has to parse |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_names_every_step_ci_runs.py -q` in a `git clone --no-local` at the target SHA | exit 0 — `23 passed in 8.59s` |
| `evidence_check.py .` unscoped, no `--ledger`, same clone | exit 0 — `total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `3 work items read · 92 unread · 223 names read · 0 refused · 0 drifted` |
| `workflow_text` driven against a latin-1 `release` job, pre-fix and post-fix, the pre-fix module written out of git | pre-fix raised `UnicodeDecodeError ... byte 0xe9 in position 45`; post-fix returned `None`, and `coverage_line` on it returned `None` |
| Mutation: `workflow_text` back to `except OSError`, anchored on its own body | exit 1 — red: `test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was`, alone |
| Mutation: the naive first-occurrence form of the same substitution | landed at `broad_gate.py:463` in `config_text`; exit 0, **nothing red** — the silent trap reproduced |
| Mutation: `coverage_line`'s two populations merged back into one | exit 1 — red: `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`, alone |
| Mutation: the `PARTITION` pointer deleted from the excluded half | exit 1 — red: `test_a_step_a_row_excludes_is_still_pointed_at_its_reason`, alone |
| Mutation: naive first-occurrence `return handle.read()` → `return None` | landed at `:462` in `config_text`; exit 1, 7 cases red — loud |
| Mutation: naive first-occurrence delete of `        CORRECTIONS_NAME,` | landed at `:1373` inside `PARTITION`; exit 1, 12 cases red — loud |
| `coverage_line` rendered against the real workflow and against a mixed fixture | both clauses correct and disjoint; panel count `3 of 4` on the mixed fixture |
| The broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** It is the sealer's one run, after the rounds settle; `agent-contract` §2 keeps it out of this round, and the last round record's `Broad gate` cell is the sealer's to write. It comes due once finding 1 is answered |

Every mutation was applied alone, with its anchor count asserted before the
substitution, and restored from bytes kept outside git. The probe script and
the clone are deleted; the tree under review is clean.

## Paste-ready fixes

```markdown
**What the count does not say** is whether a mirrored arm asks the same
question its step asks. The partition says a step is on the list; two readers
of one question can still disagree about what they are checking. **#473 is
the work item about that class**, opened with the one live instance this
repository has: the gate runs the `survivors` and `corrections` arms
unconditionally where the workflow skips both steps on a `main` base.
```

```markdown
- **This is not the class of whether a mirrored arm asks its step's
  question.** That one is #473's; this one is whether the step is on the list
  at all. The frame wrote #423 here and review round 1 corrected it: #423 is
  about the base the gate resolves, and it ships in this release.
```

Round 1's finding 5 is closed and reached, so the floor round 1 missed is
met. Nothing this round opened leaves the root or ends a run on a traceback.

Needs a fix: yes — finding 1, the two uncorrected copies of the class round 1's finding 2 repaired, one of which ships in `skills/verify/SKILL.md`
Loses a record or crashes: no

## Proof block

Opened in the clone at the target SHA, or in the tree under review read-only:

- `skills/verify/scripts/broad_gate.py` — `job_steps`, `PARTITION` and its
  header, `workflow_text`, `unanswered`, `coverage_line`, `config_text`, the
  arm list and the `coverage_line` call site
- `tests/test_the_gate_names_every_step_ci_runs.py` — the four new units and
  `test_the_gate_runs_no_arm_the_partition_does_not_account_for`
- `tests/test_ci_gives_the_checks_what_they_need.py` — `strip_comments`
- `.github/workflows/hygiene.yml` — the job list and all thirteen `release`
  steps, plus the bodies of the four excluded with no local answer
- `.github/workflows/test.yml` — the job list
- `.github/scripts/issue_claims_check.py` — its exits
- `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/` —
  `rounds/round-1.md`, `rounds/round-1-report.md`, `spec.md`, `overview.md`,
  `questions.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`
- `seal/ledger/1789985781-the-gates-arm-list-is-maintained-by-hand.md` and
  `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md` —
  read as fragments; `seal/ledger.md` was not opened whole
- `skills/verify/SKILL.md` — the block this branch adds
- `seal/follow-up.md` — the header rule and the row this branch adds
- `CLAUDE.md`, `bin/test`
- `gh issue view 423`, `gh issue view 473`
