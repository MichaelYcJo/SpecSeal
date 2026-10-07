# Feature Specification: a fix range is its own commits across a merge (#860, #805)

<!-- seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/round-record-spec.md` §*The fix range — `Fix range`* | the row states the commits a round's fixes were measured over, and `fix_surface` measures from that same range, so the two agree by construction. What *the range* holds is what this work decides, and the section is where that decision links from |
| `docs/round-record-spec.md` §*The fix surface — `Contract changes` and `New units`* | `New units` is the verifying round's finding surface, a list of units nobody has reviewed. A sibling's unit, reviewed at its own pull request, is not on that surface |
| `docs/round-record-spec.md` §*The depth in `New units`* | the generator already attributes a unit to the one commit that added it, per `fixed` row, rather than to the range's two ends. This work generalises that attribution from the `fixed` commits to every commit the range owns |
| `docs/the-record-layout.md` §*A commit after the build brings its changelog fragment along* | the notice names the item's own commits after the build; it prints and never refuses; it is silent where it has no line to draw. The walk that finds those commits is what this work changes |
| `docs/review-chain-spec.md` §*`New units` names Python units, so a finding in a document is answered by the fix range instead* | *the evidence of ownership is the range itself*, read off the diff. With a merge in the range the diff is the merge's too, and this work makes that sentence true again |
| `CLAUDE.md` §*The goal a design is chosen against* | a reading observed from git's own history replaces a reading of parent order that no party here controls; nothing new stops to ask |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `close` is a gate on the record. Each new refusal is seen red first, its direction is stated below, and it costs zero prompts |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | the class is enumerated by construction (every reader of *a range's commits* in the two scripts); the notice's and the refusals' text is pinned; every case is seen red first |

## Scope

### The defect, in one shape

Two readers walk git history over a range that holds a merge, and both read
what the merge brought in as the item's own.

- `skills/code-review/scripts/round_record.py#touched` diffs the range's two
  ends. Round 1 of work item `1791270164` closed over `99bcad40..092004bb`,
  which held the branch's merge of `origin/release/v0.20.0`, and `close` wrote
  111 entries into `New units`, 109 of them a sibling's (#860, that item's
  `rounds/round-2-report.md` ⬜ 4). Round 2 then had 109 rows it could only
  mark ❓.
- `skills/code-review/scripts/chain_check.py#walk_tip` reads the parent order
  of HEAD alone. One commit above a merge made from the base's side, the
  fragment notice walks down the base, names a sibling's squash as *after the
  last round* and misses the item's own late fix (#805, probe H of
  `1791163983`'s round 2).

Both read the shape of a merge, which the inventory's part 3 classes as
*observed, unknown passed* (rows 79, 80, 119). Neither asks git which commits
descend from the range's start, which is the one fact that separates the
item's commits from the merged side's whatever the parent order.

### Measured in this frame

Executed 2026-10-07 in the worktree where `1791270164`'s commits still
resolve (its branch was squashed; the clone keeps them):

| Reading of `99bcad40..092004bb` | Count |
|---|---|
| `git rev-list --count` | 9 commits, the count the record states |
| `--ancestry-path` | 6, the 5 own commits and the merge `f6d39425` |
| `--ancestry-path --no-merges` | 5 |
| `--first-parent --no-merges` | 5, the same here because the merge was made from the branch |
| paths in `git diff --name-only -M` between the ends | 74 |
| paths the 5 own commits changed, as a union | 9 |
| top-level names `git diff` adds in `tests/test_the_seal_is_taken_once_by_the_sealer.py` between the ends | 22 |
| of those, added by an own commit | 2 |

The last two rows decide the design. Restricting the diff to the own commits'
paths is not enough. A file an own commit touched still carries twenty of the
merged side's units at the range's ends, so the filter has to be per unit,
not per path. `round_record.py`'s own report said 109 of 111, which is the
same fact read at the record.

### In

One reading of *the commits a range owns*, in `chain_check.py`, that every
reader of a range in the two scripts imports:

**A range `a..b` owns the non-merge commits that descend from `a` and that
`b` reaches** — `git log --ancestry-path --no-merges <a>..<b>`. A sibling's
commit reaches `b` only through a merge and descends from `a` never, so it is
not owned whatever side the merge was made from. The merge commit itself is
not owned, and a change made only inside its conflict resolution is invisible
to both readers, which is the limit the fragment notice already declares and
this work keeps.

What imports it, and what each stops doing:

| Reader | Today | After |
|---|---|---|
| `round_record.py#touched` | `git diff --name-status -M a b`, no `-z` | the union of the owned commits' changed paths, deletions left out; `-M` is not needed, because a rename read as `D` old plus `A` new leaves the same new path after the `D` filter |
| `round_record.py#close`, the surface | `measure` over the two ends and the paths above | `measure` over the two ends and the owned paths, then `added` and `changed` kept only where an owned commit added or changed that unit — the per-unit filter the measurement above requires |
| `round_record.py#unit_adders` | its own `measure` per `fixed` commit | a reading of the per-commit pass above, restricted to the `fixed` commits |
| `round_record.py#fix_pass_units` (`Fix of a fix`) | `touched` over the previous record's range, `ast.dump` at both ends | the same two-ends comparison, kept only for units an owned commit added or changed |
| `round_record.py#close`, the `fixed` guard | `is_ancestor(full, b) and not is_ancestor(full, a)` | the commit is one of the range's owned commits. A `fixed` row naming the merge, or a commit the merge brought in, is refused with the reason, nothing written |
| `round_record.py#parse_range` | refuses a moving end | also refuses a start that is not an ancestor of its end, nothing written. Under `--ancestry-path` such a range owns nothing, and a silent empty surface is the shape the inventory calls *unknown passed* |
| `chain_check.py#commits_after` and `#walk_tip` | `--first-parent --no-merges` from a tip `walk_tip` picks by HEAD's parent order | the owned commits of `<round 1's target>..HEAD`; `walk_tip` is removed. CI's merge ref needs no special case, because the sibling's commits on its first-parent side descend from no target |
| `chain_check.py#fragment_left_behind`, the three `rev-list` calls | `a..b` for each record's range, `end..tip` for *after the last round* | the owned commits of each, from the same reading |
| `chain_check.py#fragment_left_behind`, *after the fragment last changed* | the position of the fragment's last change in a linear list | a commit is named when no owned commit that changed the fragment descends from it. On a linear history that is every commit after the fragment's last change, which is what the notice named before; where history branches inside the item the answer no longer depends on how git orders two commits neither of which descends from the other |

Three readers of git path output gain `-z`, because the class is the same (a
git listing read as quoted text, so a name `core.quotePath` quotes never
matches) and each is one token: `touched` through the shared reading,
`tracked_at` (`ls-tree -r --name-only`), and `call_sites`' split of `git grep
-n` on `:`. Measured here: `git grep -n -z` emits `<rev>:<path>\0<line>\0<text>`
per match, so the parse becomes two partitions on NUL and one on the first
`:`. One fixture, a file whose name git would quote, is the red case for all
three.

The rule's text, with the limit, in one home, and the two scripts' docstrings
and `skills/code-review/orchestration.md` §*And name the fix surface, in the
same record* linking it rather than restating it. The home is
`docs/the-record-layout.md`, a new section beside the fragment rule that
already lives there, because `docs/round-record-spec.md` stands at 994 lines
under the repository's 1000-line ceiling (`seal/config.md`, `Document line
ceiling`) and `docs/review-chain-spec.md` at 999. `docs/round-record-spec.md`
§*The fix range* links the home in one sentence.

Every refusal and every notice text this changes is pinned by a case seen
red first (§15), and every case that reproduces #860 or #805 is planted as
the shape the issue measured: a merge of the base inside a `close` range with
a sibling's unit in a file an own commit also touched; a merge made from the
base's side below HEAD with one own commit on top.

### What this removes

- `chain_check.py#walk_tip`, a reader of HEAD's parent order, and its three
  cases' premise.
- `commits_after`'s own `git log`, `touched`'s own `git diff`, and the three
  `rev-list` calls in `fragment_left_behind`, folded into one reading.
- `unit_adders`' own per-commit `measure` loop, which becomes a reading of the
  pass this work adds.
- The two `is_ancestor` calls of `close`'s `fixed` guard.
- The `core.quotePath` guess in three readers.
- The released sentence *the first-parent commits after round 1's `Target
  SHA`* and *where the checkout is CI's … the walk starts at the pull
  request's own head*, in `docs/the-record-layout.md` and `chain_check.py`'s
  module docstring. The claim went with its code, so the 0.18.3 ledger rows
  that carry it (`S1, S5, S8, S10` and `S2, S3, S4, S6`, which also anchor on
  `walk_tip`) are corrected in this item's fragment, as `docs/the-evidence-ledger.md`
  §*A released row is read again in the branch's fragment* says, never in the
  released file.

### The input class of each reader this changes

| Reader | Class | Unknown input |
|---|---|---|
| `own_commits` (new) | observed: git's own ancestry | git failing returns None and the caller decides; a start that does not reach its end owns nothing, and `close` refuses it |
| `touched`, `fix_pass_units`, the surface filter | observed | a file the AST cannot read keeps the diff-line heuristic, a guess, as today and unchanged |
| `parse_range`, the `fixed` guard | owned text, then observed ancestry | refused, naming the shape |
| `fragment_left_behind` | observed | prints only; silent where no line can be drawn, as today |
| `tracked_at`, `call_sites`' path parse | observed, verbatim | a path with a NUL cannot exist in git |

### Old records, and the `*_FROM` cutoffs

No cutoff is added, and `item_began_at` is read by nothing this work adds.

- A written row is never re-derived. `chain_check.fix_surface` and
  `fix_of_a_fix` read the record's cells, not git, so a record written before
  this change keeps its row and passes exactly as it did. Round 1 of
  `1791270164` keeps its 111 entries; that record is a process record its
  release retires, and its own run closed ⬜ 4 as a correction deferred to
  #860.
- `round_record.py new` re-derives `Fix of a fix` from the previous record's
  `Fix range` at run time. For a run in flight across the plugin update the
  count can only fall, never rise, which is the permissive direction
  `landings` already documents and the one that costs no stop.
- The fragment notice prints only.
- The generator's two new refusals bind the `--range` and the `## Fixes`
  table handed to `close` now, not any record. `docs/round-record-spec.md`
  §*The fix range*: *the grandfathering is the checker's and not the
  generator's*.

### Out

| Left out | Why, and who answers |
|---|---|
| the `Fix range` row's count, `N commits` | stays git's own `a..b` count on both the writer and the checker. Its job is to catch an end that moved, and both sides read the same number; an own-commit count would disagree with every record written since `RANGE_FROM` and need a cutoff of its own, which the brief's direction refuses. The home says in one sentence that the count and the surface read the range two ways |
| `survivor_check.py#corrected` over `--range` | CI hands it `origin/<base>...HEAD`, a merge-base range, so a merge of the base contributes nothing there. A hand-typed `a..b` holding a merge is the same class one script over; the repository owner decides whether it takes the shared reading, through an issue the orchestrator opens |
| `chain_check.py#added_on_branch` and `written_late`'s reading of a merge's first parent | a different question, which commit added a record, with its own measured rules (#529) |
| `correction_check.py`'s first-parent fallback | #836 and #867's files |
| `item_began_at` grandfathering a non-numeric work-item name | the inventory's note is #835 and #867's class, a reader that lets the unknown through; this work adds no reader of it |
| `call_sites`' reach being a textual prediction | a guess by design, classed so in the inventory; only its path parse changes here |
| three readers of `git ls-tree` (`tracked_at`, `chain_check.tracked_files`, `survivor_check.tracked`) becoming one | two take a revision and one a directory at HEAD; #866 and #867 own the one-reader class. This work changes one token in one of them |
| `round_record.py`'s records-level findings and the run's end | #837 |
| the round-record cells with several readers | #866; the seams are in `plan.md` |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a merge of the base inside a `close` range, file level | Given a `--range` whose commits hold a merge of the base that brought a sibling's new unit in a file no own commit touched / When `close` runs / Then `New units` names the own commit's unit alone and the sibling's unit is absent | a case in `tests/test_the_fixes_close_the_record.py`, red against `touched` as it stands |
| S2 the same, unit level | Given the sibling's unit and an own commit's unit added in the SAME file / When `close` runs / Then `New units` names the own unit alone | a second case, red against a path-level restriction as well as against today's code; this is the measured 22-against-2 shape |
| S3 `Contract changes` | Given a merged sibling commit that changed a unit's signature and an own commit that changed another's / When `close` runs / Then `Contract changes` names the own change alone, with its reach at the range's end | a case in the same module |
| S4 `Fix of a fix` | Given a previous record's `Fix range` holding a merge that brought a unit, and this round's open finding whose `Location` lands in that unit / When `new` runs / Then the row reads `no`; and `first` when the `Location` lands in a unit an own commit of that range added | a case in `tests/test_a_fix_of_a_fix_is_counted.py` |
| S5 a start that does not reach its end | Given `--range a..b` where `a` is not an ancestor of `b` / When `close` runs / Then it refuses, names both ends and the shape, and writes nothing | a case beside `test_a_range_end_that_moves_is_refused` |
| S6 a `fixed` row naming a commit the range does not own | Given a `fixed` row naming the merge commit, and another naming a commit the merge brought in / When `close` runs / Then each is refused with the reason that the surface is not measured on it, and nothing is written | two cases beside `test_a_fixed_row_without_a_resolving_commit_inside_the_range_is_refused` |
| S7 #805's shape | Given a lagging fix, a sibling's squash on the base, the branch reset to the base with the old branch merged in (first parent the base), then one more own behaviour commit / When `chain_check` runs / Then the own commit is named and the sibling's squash is not | a case in `tests/test_a_fragment_left_behind_is_named.py`, red against `walk_tip` as it stands |
| S8 the shapes that already hold | Given CI's merge ref, the branch's own merge of the base, and the octopus of an unrelated head / When `chain_check` runs / Then the item's commit is named and no sibling's or stray commit is, with `walk_tip` gone | the existing cases, their docstrings rewritten for the new reading |
| S9 history that branches inside the item | Given a side topic with a behaviour commit merged into the branch after the build / When `chain_check` runs / Then the topic's commit is named too; and given a later own commit on the main line that changed the fragment, none of the commits it descends from are named, the topic's included only where the fragment commit descends from it | two cases, the first red against the first-parent walk |
| S10 a path git would quote | Given a unit added in a file whose name holds a non-ASCII character / When `close` runs / Then `New units` names it, a `Location` in that file resolves through `tracked_at`, and `call_sites` names a reach inside that file | one fixture, three assertions, red against the three readers as they stand |
| S11 the record format is unchanged | Given every existing case of the two scripts' suites / When they run / Then they pass, and a record written before this change reads the same at `chain_check` | the six modules that read `round_record.py` and `chain_check.py`, run at a phase boundary |
| S12 one home | Given the rule's home and its carriers / When the one-owner test runs / Then each carrier links the home by section and none restates it | `tests/test_the_rules_have_one_owner.py`, a new rule entry |
| S13 the released claims that went with their code | Given the 0.18.3 rows anchoring on `walk_tip` and stating the first-parent walk / When `evidence-check` runs on the branch / Then it is green, with `Corrected ·` rows in this item's fragment citing them and no released file changed | `bin/evidence-check` |

## Data & interfaces

- **New, `chain_check.py#own_commits(root, a, b)`** → `[(full, short,
  [(status, path), …])]`, oldest first, from `git log --ancestry-path
  --no-merges --no-renames --name-status -z --format=%x01%H %h --reverse
  <a>..<b>`; None where git fails; `[]` where `a` does not reach `b`. The
  parse follows `commits_after`'s, whose `--name-only -z` form it replaces;
  the exact separators `--name-status -z` emits are a measurement the build
  takes before the parser is written (`questions.md` Q1).
- **New, `round_record.py#own_units(reader, root, commits)`** → `{(path, unit):
  {full, …}}` for every unit a listed commit added or changed between its
  parent and itself — `ast.dump` per top-level unit of a `.py` file, the
  diff-line heuristic for a non-Python, non-prose file, as `fix_pass_units`
  and `measure` read them today.
- `touched`, `fix_pass_units`, `unit_adders`, `parse_range`, `close`,
  `tracked_at` and `call_sites` keep their signatures. `commits_after` and
  `walk_tip` are removed; `fragment_left_behind` keeps its signature and
  its return shape.
- The record's rows, their vocabulary and `Fix range`'s count are unchanged.
  What changes is which units the two surface rows name and which commits the
  notice names.
- Two new refusals from `close`, at exit 2 with nothing written, each naming
  the shape (S5, S6). The `fixed` guard's message changes from *lies outside
  --range* to *is not one of the range's own commits: a merge, or a commit a
  merge brought in*.
- Ledger: this item's fragment carries the new claims, `Corrected ·` rows
  for the 0.18.3 `S1, S5, S8, S10` and `S2, S3, S4, S6` rows, and a re-read
  of 0.19.0's `A1` row, whose claim about `Fix of a fix` now reads *the
  range's own commits added or changed*.
- No new dependency. Bare `--ancestry-path` has been in git since 1.6, and
  every CI leg runs a 2.x.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline. No row
there is a person's.

Framed 2026-10-07 by framer, before the build.
