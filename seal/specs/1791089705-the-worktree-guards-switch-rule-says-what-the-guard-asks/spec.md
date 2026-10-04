# Feature Specification: the worktree guard's switch rule says what the guard asks

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issue #750, deferred from round 3 of work item
`1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole`
(#745 / #737). That round was the run's last, so its two findings were not
fixed on that branch. Its report,
`seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/rounds/round-3-report.md`
§*Findings* and §*Paste-ready fixes*, is the starting point, and every fence
below was checked against the base `e141980a` by reading (see *Checked against
the base*).

**The guard's behaviour does not change.** The sentence is what is wrong, and
the checks are what let it be wrong unnoticed. No line of
`hooks/worktree-guard.py` that executes changes in this work.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*, the #678 paragraph, the sentence "Each side is read by its words alone: …" | The rule text this work corrects. It is the sentence a person reads to learn when the guard asks. Today it names the words wrongly in two places and leaves a third open (Scope, S1–S3) |
| `skills/agent-contract/SKILL.md` §14 | A fix that changes what a person reads documents it and pins it, in the same commit. The pin rides the sentence |
| `skills/agent-contract/SKILL.md` §15 | Each new or changed case is seen red before it is committed, and the handover says how (acceptance A2–A4) |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class: every place that states `switch_kind`'s words. Enumerated below under *The class* |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | The changelog entry goes in this work item's `changelog.md`, and ledger rows and re-reads go in `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md` |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | `seal/config.md` declares `Ledger frozen from`, so the released rows this work drifts are read again by `Re-read ·` rows in the fragment, never re-stamped in place |
| `docs/review-chain-spec.md` §*The survivor sweep*, "A round record is outside the sweep's corpus on both sides" | The two other copies of the old sentence are in round-3's records of 1791019475 (`rounds/round-3.md`, `rounds/round-3-report.md`), which the sweep does not read. So no `survivors.md` row is expected; the sweep run is what confirms it |

## Scope

### In

**The rule text (one sentence, one docstring).**

- **S1. A checkout carrying `--`.** The sentence excludes only the words after
  `--`, so it counts `checkout feature/x -- README.md` as a switch.
  `switch_kind` returns `None` for any checkout carrying `--` (unless it
  carries `-b`/`-B`), which is right: git restores the file and HEAD stays.
- **S2. A bare `-B`.** The sentence names `checkout -b` only. `switch_kind`
  also counts `-B`, with or without a name after it.
- **S3. `switch -- x`.** The sentence leaves open whether "anything after
  `--`" governs `switch`. `switch_kind` counts it as a switch, and git
  switches.
- **S4. `switch_kind`'s own docstring** says "every `checkout` with a name in
  it counts", which is S1's error in a second place (*The class*, below). It
  is corrected to match. A docstring edit, no executable line.

The corrected sentence is the reviewer's, verbatim:

> a `switch` naming a word or `-`, a `checkout` carrying `-b` or `-B`, a
> `checkout` with no `--` among its words that names `-` or a word other than
> `.`, or a `worktree add`

**The checks (all in `tests/test_guard_resolves_the_tree_it_judges.py`).**

- **C1. The pin.** An assert of the corrected sentence, appended to
  `test_the_guard_policy_says_a_hidden_file_checkout_is_asked`, the case that
  already pins the rest of this paragraph.
- **C2. Three `KINDS` rows**, after the `"checkout with no name"` row:
  `"checkout a name before --"` → `None`, `"checkout -B with no name"` →
  `"switch"`, `"switch -- a name"` → `"switch"`. With them every clause of the
  corrected sentence has a row binding `switch_kind` to it (table below).
- **C3. The dead clause (⬜ 10).** In
  `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`,
  call `wider_only_kinds(..., judged=set())` and read `frozen` from the wider
  splitter's segments, so `own in frozen` can fail.

**The records.** A changelog fragment, the ledger fragment's new row and its
`Re-read ·` rows, and the builder's `overview.md`.

### Out, and why

- **The guard's behaviour.** The ticket and the reviewer agree it is right in
  every case they named (round-3 report, *Executed probes*: real git 2.54).
  Changing it would be mechanism, not a correction to a sentence.
- **A glued short option's value: `switch -cfoo`, `switch -Cfoo`,
  `checkout -bfoo`, `checkout -Bfoo`.** Read, not executed: `switch_kind`
  and the frozen `classify` both test `a in ("-b", "-B")` / `("-c", "-C")`
  and treat a word starting with `-` as no name, so a glued form whose
  value is the only name reads as no kind to both. Git's option parser
  normally accepts a glued short-option value. The corrected sentence and
  `switch_kind` agree on these shapes (neither counts them), so they are not
  this ticket's divergence; whether the guard should ask is a behaviour
  question about both readings. **Who answers it:** the orchestrator, by
  filing it (a measurement settles the git half in one probe).
- **The git facts in the round-3 report's *Facts for the evidence ledger*.**
  The corrected sentence states what the guard reads, not what git does, so
  no claim of this work rests on them. They stay in that report.
- **Re-wording "a word" to "a word not starting with `-`".** Decided against
  in `plan.md` *Alternatives considered*.
- **The 0.18.0 `CHANGELOG.md` bullet for #737.** Round 3 confirmed it names
  no list of words (verdict row "round 2's white 6 is closed"), so finding 9
  does not reach it, and a released section is not edited.
- **`questions.md` D6 of 1791019475** (whether 0.18.0 ships the tree-blind
  questions). 0.18.0 shipped at `e141980a`; it is that work item's carried
  row, not this one's.

### The class (§12), enumerated by search

Every place that states `switch_kind`'s words, found by grepping the tree for
the sentence's phrases ("words alone", "naming a word", "anything after
`--`", "`checkout -b`, or a") outside `.git`:

| Place | States the words? | In this work |
|---|---|---|
| `docs/worktree-guard-spec.md` §*Which tree*, the sentence | yes, wrongly (S1–S3) | S1–S3 |
| `hooks/worktree-guard.py#switch_kind`, docstring | yes, "every `checkout` with a name in it counts" — wrong for a name before `--` | S4 |
| 1791019475 `rounds/round-3.md`, `rounds/round-3-report.md` | quote the old sentence as the finding | no — round records are write-ups, outside the sweep (Grounding) |
| `CHANGELOG.md` 0.18.0 #737 bullet | no list of words (round 3) | no |
| `docs/worktree-guard-spec.md` §A, `hooks/worktree-guard.py#classify` | the frozen, tree-aware reading, a different reader | no |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1. A person reads when the guard asks | Given §*Which tree*, when they read the sentence, then its words are `switch_kind`'s: a checkout carrying `--` (and no `-b`/`-B`) is not a switch, a bare `-B` is, and `switch -- x` is | Read the sentence against `switch_kind` clause by clause (table below) |
| A2. The sentence cannot be reworded silently | Given the pin, when the sentence's word list changes, then `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` fails | Executed: the pin red against the base sentence (`e141980a`), green after S1–S3 |
| A3. The code cannot drift from the sentence on the three words | Given the three `KINDS` rows, when `switch_kind` stops reading any of them as the sentence says, then `test_switch_kind_reads_the_words_alone[<row>]` fails | Executed: each row green at the base; each seen red against one mutant of `switch_kind` that breaks its clause, then reverted: `"-B"` dropped from the `checkout` tuple; the `checkout` branch's `if "--" in args: return None` deleted; `switch` reading only the words before `--` |
| A4. The rule case's `frozen` clause can fail | Given C3, when `wider_only_kinds`'s per-view subtraction is dropped (`kind and kind not in frozen` → `kind`), then `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers` fails | Executed: red against that mutant, green at the fix, mutant reverted. At the base the same mutant leaves the case green (round-3 report) |
| A5. Nothing else moves | Given the edits, when the five modules that read `docs/worktree-guard-spec.md` run, then they pass | Executed: `bin/test` on `tests/test_guard_resolves_the_tree_it_judges.py tests/test_worktree_guard.py tests/test_the_guard_asks_once_per_session.py tests/test_a_creation_is_judged_before_git_runs.py tests/test_one_word_one_meaning.py` |
| A6. The ledger still resolves | Given the drifted rows, when `bin/evidence-check --strict .` runs, then it exits 0 | Executed after the `Re-read ·` rows are written |
| A7. No corrected wording survives | Given the range, when `bin/survivor-check --range e141980a...HEAD` runs, then it reports no survivor, or each is a `survivors.md` row with grounds | Executed |

**Each clause of the corrected sentence and the `KINDS` row that binds it.**
Rows marked *new* are C2's; the rest exist at the base.

| Clause | `KINDS` rows |
|---|---|
| a `switch` naming a word | `switch to a branch`, `switch -c`, `switch -- a name` (*new*) |
| a `switch` naming `-` | `switch -` |
| (a `switch` naming neither) | `switch with no target` → `None` |
| a `checkout` carrying `-b` or `-B` | `checkout -b`, `checkout -b before --`, `checkout -B with no name` (*new*) |
| a `checkout` with no `--` that names `-` | `checkout -` |
| … or a word other than `.` | `checkout a name`, `checkout .` → `None` |
| (a `checkout` with `--`) | `checkout -- path` → `None`, `checkout a name before --` → `None` (*new*) |
| (a `checkout` naming nothing) | `checkout with no name` → `None` |
| a `worktree add` | `worktree add`, `worktree list` → `None` |

## Data & interfaces

No interface changes. Coordinates this work touches:

- `docs/worktree-guard-spec.md#"### Which tree, when the command walks to it"`
  — the sentence (S1–S3).
- `hooks/worktree-guard.py#switch_kind` — docstring only (S4).
- `tests/test_guard_resolves_the_tree_it_judges.py#test_the_guard_policy_says_a_hidden_file_checkout_is_asked`,
  `#KINDS`,
  `#test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`
  — C1–C3.

Released ledger rows these edits drift (read 2026-10-04 by grepping
`seal/ledger.md`, `seal/releases/*.md`; `seal/ledger/` does not exist on the
base):

| Row | File | Cites | Drifted by |
|---|---|---|---|
| K7 | `seal/releases/0.18.0.md`, §1790993140 | `docs/worktree-guard-spec.md#"### Which tree…"@570099db` | S1–S3 |
| `Re-read · M2` | `seal/releases/0.18.0.md`, §1791019475 | the same heading `@570099db` | S1–S3 |
| K5 | `seal/releases/0.18.0.md`, §1790993140 | `hooks/worktree-guard.py#switch_kind@dd9e3aa1` | S4 |

M2 in `seal/releases/0.16.0.md` cites the heading at `@a530d5c6` and is
already read again by the `Re-read · M2` row above; it is reached through that
row. No released row cites any of the three test units C1–C3 edit.

## Checked against the base

Read at `e141980a` (this branch's base, unchanged at `b2936316`), 2026-10-04:

- `docs/worktree-guard-spec.md:631–633` hold the sentence exactly as the
  report's 🟡 9 fence quotes it.
- `hooks/worktree-guard.py#switch_kind` (lines 290–317) is the function the
  report describes: `switch` counts any word or `-`, `--` included as no
  name; `checkout` counts `-b`/`-B` first, then returns `None` on `--`, then
  counts `-` or a word other than `.`. The corrected sentence states exactly
  that order.
- `hooks/worktree-guard.py#wider_only_kinds` (lines 320–366) defaults
  `judged` to the frozen walk's kinds and subtracts it at the end, so the
  rule case's `own in frozen` is dead at the base, as ⬜ 10 says.
- `tests/test_guard_resolves_the_tree_it_judges.py:1204–1236` (the rule
  case), `:1251–1260` (the pin's host) and `:1315–1331` (`KINDS`) match the
  fences' context lines.

Not executed by the framer: the reviewer's "321 passed", "pin red", "rule
case red against the mutant" and "0 of 2,859 differ" are the reviewer's
executions at `5e4984b1`, not re-run here. A2–A7 are where the builder runs
them.

## Open questions → questions.md

None needs a person. `questions.md` lists what the frame decided.

Framed 2026-10-04 by framer, before the build.
