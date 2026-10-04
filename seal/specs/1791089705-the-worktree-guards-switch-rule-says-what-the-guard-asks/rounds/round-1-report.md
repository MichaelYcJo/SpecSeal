# Round 1 report — 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks

Target `80445412` on `docs/750-the-worktree-guards-switch-rule-says-what-the-guard-asks`,
against `release/v0.18.1` at `edee5ca2`. Reviewed by warden in a
`git clone --no-local` of the target under the session scratchpad; the clone
and every probe file were removed before this report was written.

## What this round was asked

Round 1 of work item `1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks` (#750, PR #765). The target is `80445412`, against `release/v0.18.1` at `edee5ca2`.

Spec compliance first. Check that the rule sentence in `docs/worktree-guard-spec.md` §*Which tree* says what `switch_kind` does, clause by clause. Then check that the pin, the three `KINDS` rows and the rule case (C3) each fail when the thing they hold changes. Compare the sentence against `switch_kind` over a generated set of `checkout` and `switch` commands built by construction, and do not rely on the `KINDS` rows alone.

Quality second. The smith changed one coordinate in the frame's `spec.md` to write out a heading in full, and wrote three `Re-read ·` rows (M2, K5, K7). Judge both.

The orchestrator verified the guard module, the hygiene modules and the line-end module (343 passed) and ruff on the two changed Python files at the target. The release head carries 10 drifted rows from the wave-one squashes. They belong to a parallel chore, not to this item.

## Summary

Nothing in this round needs a fix. The corrected sentence and `switch_kind`
agree on every word list a generator built, and each check the item adds
turns red against the change it holds. Three ⬜ remain: a test comment that
describes the case's frozen half as it was before this commit, a frozen half
that is stricter than the rule it claims to check, and a closing memo that
lists `evidence-check --strict` as executed without its exit, which is 2 at
the target.

## Stage 1 — spec compliance

### The sentence says what `switch_kind` does (executed and read)

**Read, clause by clause** against `hooks/worktree-guard.py:290-322`:

| Sentence clause | `switch_kind` line |
|---|---|
| a `switch` naming a word or `-` | the `switch` branch: any argument that is `-` or does not start with `-` |
| a `checkout` carrying `-b` or `-B` | the `checkout` branch's first test, `-b`/`-B` anywhere among the words |
| a `checkout` with no `--` among its words | the second test, `"--" in args` returns `None` |
| … that names `-` or a word other than `.` | the third test |
| a `worktree add` | the `worktree` branch, unchanged by this item |

The order matters only for `checkout -b x --`, and the sentence lists the
`-b`/`-B` clause as its own alternative, so the `--` clause cannot take it
back. That is `switch_kind`'s order too.

**Executed, by construction.** A probe read the corrected sentence literally
(a word is one that does not start with `-`, as the sentence sets it beside
`-`, `-b`, `-B` and `--`) and compared it with
`switch_kind(parse_git(["git", sub, *words]))` for every word list of length
0 to 4 over a 14-word alphabet (`x`, `.`, `-`, `--`, `-b`, `-B`, `-c`, `-C`,
`-q`, `--detach`, `-f`, `-bfoo`, `README.md`, `-p`), for `switch` and
`checkout`: 82,742 commands, 0 differ. The same probe reading the base
sentence differs on 6,136 of them, so it can fail.

The reading of "a word" as a word not starting with `-` is the one `plan.md`
alternative 2 chose to leave implicit; the sentence's own contrast with `-`
and `-b`/`-B` carries it, and the `switch with no target` row (`--detach` →
`None`) binds the code side. I take that decision as made, not as a finding.

### Each check fails when the thing it holds changes (executed)

Each mutant was applied in the clone, the module run, and the file restored
with `git checkout` from HEAD, a clean status asserted after each.

| Check | Mutant | Result |
|---|---|---|
| C1, the pin | `docs/worktree-guard-spec.md` restored to `edee5ca2` | `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` red |
| C2, `checkout -B with no name` | `-B` dropped from `switch_kind`'s `checkout` tuple | that row red alone |
| C2, `checkout a name before --` | the `checkout` branch's `--` return deleted | that row and `checkout -- path` red |
| C2, `switch -- a name` | `switch` reading only the words before `--` | that row red alone |
| C3, the rule case | `kind and kind not in frozen` → `kind` | `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers` red at the target; green with the base test file and the same mutant |

The `checkout a name before --` row is not redundant with `checkout -- path`:
a `switch_kind` that excluded only the words after `--`, which is what the
base sentence said, leaves `checkout -- path` green and turns this row red.

**What C3 gave up, checked.** The rule case now passes `judged=set()`, so it
no longer goes through the `- set(judged)` subtraction at the end of
`wider_only_kinds`. The mutant `return wider - set(judged)` → `return wider`
turns the same seven cases red with the base test file and with the target's
(`test_candidate_c_reports_nothing_the_frozen_reading_found`, five
parameters; `test_a_hidden_switch_behind_a_judged_one_adds_no_question`;
`test_a_hidden_creation_behind_a_judged_one_adds_no_question`). The rule case
was not among them before either, so no coverage was lost.

### The class (§12)

The frame enumerated the places that state `switch_kind`'s words by grepping
four phrases. I re-ran that search and widened it to every non-record line
naming `switch_kind`. Outside this item's own records, the tree states the
words in exactly the two places this item corrected: the sentence and the
docstring. The other hits are the frozen `classify`, code comments that say
`switch_kind` reads any word as a name (true of both readings), and records
of earlier work items. `bin/survivor-check --range edee5ca2...80445412`
reports three removed sentences and none standing.

The glued short-option shapes (`switch -cfoo`, `checkout -bfoo`) are already
deferred, to #764, by the frame's *Out*; the probe's alphabet included
`-bfoo` and the sentence and `switch_kind` agree on it (neither counts it).

## Stage 2 — quality

### The `spec.md` coordinate (read and executed)

`spec.md:159` now writes K7's heading in full, *Which tree, when the command
walks to it*, with the stamp `570099db` kept. The shortened form was a locator nothing resolves; the full heading is the
one K7 cites in `seal/releases/0.18.0.md:136`, and the hash is kept. The
records arm now reads it as `DRIFTED`, which a live work item's records may
be. The edit changes no meaning of the approved frame, and the closing memo's
divergence table records it. Confirmed.

### The three `Re-read ·` rows (read and executed)

- **K5** (`seal/releases/0.18.0.md:134`) claims the views' kinds and what is
  reported. The diff of `hooks/worktree-guard.py` touches only lines of
  `switch_kind`'s docstring, so no executable line moved; the claim holds.
- **K7** (`seal/releases/0.18.0.md:136`) claims the policy chooses no segment
  or tree through `hooks/cmdline.py`, asks it one question, and puts what only
  it finds to the person, consent first. The sentence edit touches none of
  the three; the claim holds.
- **M2** (`seal/releases/0.16.0.md:248`) claims the `cd` half of the accepted
  cost and that a git behind a redirection or a zsh prefix is not git to the
  frozen reading, now asked. The sentence edit changes which words make a
  kind, not either half; the claim holds. One row citing the 0.16.0 root
  answers the 0.18.0 `Re-read · M2` row of the same family:
  `bin/evidence-check --strict .` reports no drift for M2, K5 or K7 and
  `11 ok · 0 drifted` for this item's fragment.

The G1 row's "321 passed" over the five policy-reading modules reproduces at
the target.

## Findings

### ⬜ 1 — the comment beside `judged=set()` describes the frozen half this commit replaced

`tests/test_guard_resolves_the_tree_it_judges.py:1221-1223`. The comment says
the default `judged` subtracts what the frozen walk's words hold, "which is
this case's own frozen half". Six lines below, the same commit replaced that
half: `frozen` is now the frozen parser over the wider splitter's segments
(`split_segments_with_separators`), not `walk_command`. The two sets agree on
every generated shape today, so nothing is wrong at run time. A reader of the
comment is told the case reads the frozen walk, though the case reads the wider
splitter's segments. Fix or justify.

### ⬜ 2 — the rule case's frozen half is the whole command, the rule's is the view's sources

`tests/test_guard_resolves_the_tree_it_judges.py:1228-1231`. `POLICY_RULE`
asks wherever a view's kind is held by "none of the frozen segments the view
was made from". The case reads `frozen` over every segment of the command, so
it flags a kind that some other segment holds even where the rule would ask.
That makes the case stricter than the rule it says it checks. Today's
generator yields no shape where the two differ (the case is green), so this
can only become a false red if multi-segment shapes are added. Recorded, no
fix asked.

### ⬜ 3 — correction: the closing memo lists `evidence-check --strict` as executed with no result

`seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/overview.md:12`.
The `verified: executed` line names `evidence-check --strict` among the
checks that ran, with no exit status. `spec.md` A6 asks for exit 0. At the
target it exits 2. This item's fragment is clean (`11 ok · 0 drifted`) and
M2, K5 and K7 no longer drift; the 10 drifted rows are the wave-one rows
(`fake_venv`, `VERSIONS_OF_ANOTHER_PRODUCT`, `templates/config.md`) the
orchestrator assigned to a parallel chore. The memo should say so rather
than list the run among passing checks (agent contract §4). A paperwork
correction, outside `Needs a fix`.

## Regression tests to plant

None. The three `KINDS` rows, the pin and C3 are already planted and were
each seen red above.

## Facts for the evidence ledger

None new. G1's executed claims reproduce at the target. Only one differs:
`spec.md` A6's exit 0 does not hold at the target, for the reason in ⬜ 3.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the comment beside `judged=set()` says the default subtracts this case's own frozen half; the same commit moved that half off the frozen walk | `tests/test_guard_resolves_the_tree_it_judges.py:1221` | open | read: `frozen` at line 1230 is built from `split_segments_with_separators`, the comment names the frozen walk |
| ⬜ 2 | the rule case's `frozen` is the whole command's segments, stricter than the per-view condition `POLICY_RULE` states | `tests/test_guard_resolves_the_tree_it_judges.py:1228` | open | read; executed: green at the target, so no generated shape separates the two today |
| ⬜ 3 | the closing memo lists `evidence-check --strict` as executed with no result, and it exits 2 at the target | `seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/overview.md:12` | open | executed: exit 2, the 10 wave-one rows; this item's fragment is clean. A paperwork correction |
| 🟢 | the corrected sentence states `switch_kind`'s words, clause by clause and in its order | `docs/worktree-guard-spec.md:631` | confirmed | read against `hooks/worktree-guard.py:290-322`; executed: 82,742 generated commands, 0 differ; the base sentence differs on 6,136 |
| 🟢 | the pin and each of the three new `KINDS` rows fail when what they hold changes | `tests/test_guard_resolves_the_tree_it_judges.py:1266` | confirmed | executed: four mutants, each red on its own row; the `before --` row is the only one red under the base sentence's reading |
| 🟢 | C3 makes the rule case fail when the per-view subtraction is dropped, and loses no coverage of the judged subtraction | `tests/test_guard_resolves_the_tree_it_judges.py:1224` | confirmed | executed: red at the target, green with the base test; the judged-subtraction mutant reds the same seven cases before and after |
| 🟢 | `switch_kind`'s docstring states the same words in `classify`'s order, and no executable line changed | `hooks/worktree-guard.py:296` | confirmed | read: the diff touches docstring lines only |
| 🟢 | the `spec.md` coordinate written out in full resolves and changes no meaning | `seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/spec.md:159` | confirmed | executed: the records arm reads it as `DRIFTED`, not refused; read: the heading is K7's |
| 🟢 | the `Re-read ·` rows for M2, K5 and K7 are honest; each cited claim holds after the edit | `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md:2` | confirmed | read against `seal/releases/0.16.0.md:248` and `seal/releases/0.18.0.md:134`, `:136`; executed: no drift for M2, K5, K7 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` at `80445412` | 135 passed |
| the corrected sentence read literally against `switch_kind`, every word list of length 0 to 4 over 14 words, `switch` and `checkout` | 82,742 compared, 0 differ |
| the base sentence, same set | 6,136 differ |
| pin: `docs/worktree-guard-spec.md` restored to `edee5ca2` | the pin case red |
| `-B` dropped from `switch_kind`'s `checkout` tuple | `checkout -B with no name` red, 17 others green |
| the `checkout` branch's `--` return deleted | `checkout -- path` and `checkout a name before --` red |
| `switch` reading only the words before `--` | `switch -- a name` red alone |
| `kind and kind not in frozen` → `kind`, target test file | the rule case and `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` red |
| the same mutant, base test file | only `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` red |
| `return wider - set(judged)` → `return wider`, target and base test files | the same seven cases red in both |
| `bin/test` over the five modules that read `docs/worktree-guard-spec.md` | 321 passed |
| `bin/evidence-check --strict .` at `80445412` | exit 2: 10 drifted rows, all wave-one; this item's fragment 11 ok, 0 drifted |
| `bin/survivor-check --range edee5ca2...80445412` | exit 0, 3 removed sentences, none standing |
| the broad gate (full suite, lint, typecheck) | not yet, and not this round's: the sealer's, after the rounds settle |

Needs a fix: no

Loses a record or crashes: no

Nothing this round found is open at 🔴 or 🟡, so the broad gate comes due:
the sealer's spawn, once the orchestrator has verified this report.

## Proof block

Files opened this round, at `80445412`:

- `docs/worktree-guard-spec.md` (the #678 paragraph, through the diff)
- `hooks/worktree-guard.py` (`walk_command` tail, `switch_kind`, `wider_only_kinds`, `classify`)
- `tests/test_guard_resolves_the_tree_it_judges.py` (lines 1150-1365)
- `seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/spec.md`, `overview.md`, `phases/phase-1.md`, `changelog.md`, `plan.md` (alternatives and phases), and the diffs of `plan.md`, `questions.md`, `spec.md` since `dc0553fb`
- `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md`
- `seal/releases/0.16.0.md:248`, `seal/releases/0.18.0.md:134`, `:136`, `:152`
- `bin/test`
