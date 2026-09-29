# Implementation Plan: arm-check reads every supported `ast`

<!-- seal/specs/1790690762-arm-check-reads-every-supported-ast/plan.md — HOW,
in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

`arm_check.py`'s node-type tables become true for every Python from the floor
to 3.14, and stay checkable that way without anybody's interpreter. Three
moves do it. The two t-string node types join `JoinedStr` and
`FormattedValue` as non-arms. A table beside the classification records which
classified names only some supported Pythons have. The second table case
reads that table and checks the running Python's slice exactly in both
directions. A new CI job runs `tests/test_arm_check.py` at 3.13 and 3.14, and
a case holds the job's versions to the table's bounds, so the next grammar
change is caught by CI and not by whoever upgrades first. One phase.

## Technical context

**What the build edits, and the coordinates it starts from.**

- `skills/verify/scripts/arm_check.py#NOT_ARMS`: the group "an expression that
  computes a value and forks on nothing" gains `Interpolation` and
  `TemplateStr`. A short comment in the group says they are the t-string
  counterparts of `FormattedValue` and `JoinedStr`, and why an interpolation
  tests nothing (spec §*Scope* In-1, M3). The group "a removed alias
  `ast.parse` never produces" keeps its five 3.14 removals. They are classes
  on 3.12 and 3.13, so `grammar()` there lists them and the totality case
  needs them.
- A new constant beside `CLASSIFIED`, the range table (spec §*Data &
  interfaces*). It holds only the seven names measured in M1. The module
  docstring's paragraph "Totality is checked against `ast` itself…" says
  what is true afterwards: each Python checks its own slice, the table
  records the names that differ, and CI runs the check at every bound.
- `tests/test_arm_check.py#test_the_classification_names_nothing_the_grammar_does_not_have`:
  rewritten to S4. It keeps its name, so `docs/the-broad-gate.md`'s
  `Enforced by` line and any reader of the name stay valid. Its message names
  the range table as the repair for both directions.
- New cases S1, S2, S5 and S6 in the same module. S1 and S2 carry
  `pytest.mark.skipif(sys.version_info < (3, 14), …)`, and their t-string
  source is a string literal, so the module parses on 3.12. S6 reads
  `.github/workflows/test.yml` as text through `tests/conftest.py#code_lines`,
  the rule every workflow reader in the suite uses (#482), and takes the
  versions of each job whose run line names `tests/` or
  `tests/test_arm_check.py`.
- `.github/workflows/test.yml`: a new job **after** `ledger`. The placement is
  load-bearing: `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_ci_runs_the_suite_at_the_floor_the_runner_holds`
  reads the text between `  pytest:` and `  ledger:`, and requires every
  version there to be the floor. Suggested name `arm-check-grammar`,
  `ubuntu-latest`, a matrix of `python: "3.13"` and `python: "3.14"`,
  `actions/checkout@v4` with `fetch-depth: 0`, `actions/setup-python@v5`,
  `pip install pytest`, `pytest tests/test_arm_check.py -q`.
  `tests/conftest.py` imports only the standard library and pytest, and no
  case in the module spawns `git` (read), so nothing more is installed. The
  `pytest` matrix comment is rewritten to say what each job's versions are
  for (spec M7).
- `CONTRIBUTING.md` §*Running the checks*, the sentence "CI runs four jobs: …"
  names the new job. **That section may state the floor exactly once**
  (`test_the_suite_has_a_command_that_is_cheap_twice.py`, the case that counts
  `FLOOR_TEXT` in it), so the new words name 3.13 and 3.14 and never 3.12.

**Constraints the edit is written against** (spec C1–C3): no `zip(` with
`strict=` and no `.UTC` in `arm_check.py`, comments included. No bare `zip`
(B905). No three-part version token anywhere under `skills/`. Nothing 3.10+
in `arm_check.py`'s syntax, because its own comment claims 3.9 and M2 measured
that it loads there. A tuple compared with `sys.version_info` is 3.9-safe.

**Two interpreters, and which one a command gets.** This worktree has no
`.venv`, so the first `bin/test` builds one on 3.14 (spec M5), and that is
where S1, S2 and the base's two reds show. For 3.12 and 3.13, from the
worktree root:

```
uv run --isolated --no-project --python 3.12 --with pytest python -m pytest tests/test_arm_check.py -q
uv run --isolated --no-project --python 3.13 --with pytest python -m pytest tests/test_arm_check.py -q
```

**What breaks in six months.** Python 3.15 ships. If it adds or removes a node
type, nothing goes red until someone adds a 3.15 leg to the new job. The
first run on 3.15, in CI or on a contributor's machine, then names the change
exactly. S6 makes the leg part of the fix, because a range bound of 3.15 is
red until CI runs 3.15. The unattended alternative, a floating leg, is
`questions.md` Q3.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Range table in the script, exact per-interpreter check, CI job at 3.13 and 3.14, bounds held to the job** | A bound is declared for a version CI does not run: S6 refuses it. The table and the job drift apart: S6 again. 3.15 adds a node type and nobody adds a leg: nothing is red until a 3.15 run exists (Q3) | **Chosen** |
| B. Only add `TemplateStr` and `Interpolation`, and delete or exempt the five aliases | Deleting them turns the totality case red on 3.12 and 3.13, where they are classes (M1). Exempting the "removed alias" group from the stale check means a name placed in that group is never checked again, in either direction. Either way CI at 3.12 cannot see 3.14 | Rejected: closes the instance, not the class |
| C. Drop the stale-name direction | `test_the_classification_names_nothing_the_grammar_does_not_have`'s docstring gives the reason it exists: a removed name keeps the classified count up while a real one goes missing. That hiding returns | Rejected |
| D. A case that spawns every local interpreter from the floor up (`uv python find`) and checks each | It skips where uv or those interpreters are absent, which is every CI runner. The check then runs only where a contributor happens to have the versions, which is how #684 arrived | Rejected: verification that runs unattended is the project's first goal (`CLAUDE.md`) |
| E. A per-version snapshot of `ast`'s constructors written into the test | A hundred-plus names per version, retyped from `ast`. A snapshot can only be checked on its own interpreter, so it still needs D or A's CI job to mean anything | Rejected: A carries only the names that differ |
| F. Run the whole suite at 3.14 in the `pytest` matrix | Changes the stated rule that the `pytest` job runs at the floor, and its case. Whether the whole suite is green on 3.14 is unmeasured (`questions.md` Q1) | Rejected for this item. Q1's measurement is the ground a later item would stand on |
| G. Pin `bin/test` to the floor | Every local run and every CI run is then at 3.12, so no run anywhere meets a newer grammar. A plugin user on 3.14 still meets the refusal | Rejected (spec §*Scope*, out) |
| H. A floating `3.x` leg | A pull request's verdict could change with no commit, the day a new Python ships. Every record here binds a verdict to a SHA | Rejected as the default. Kept for the owner as Q3, possibly as a non-blocking leg |
| I. `Interpolation` as an arm shape | It tests nothing. The `IfExp` inside it is already counted (M3), so counting the interpolation too would count a non-branch | Rejected |
| J. The range table in the test instead of the script | Splits one fact across two files: a reader auditing `NOT_ARMS` could not see why five of its names are absent on 3.14. `CLASSIFIED` already sets the precedent of a constant held for the case that checks it | Rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The two t-string names in `NOT_ARMS`. The range table. S4 rewritten, S1, S2, S5 and S6 added, each seen red where spec §*User scenarios* says. The new CI job and the rewritten matrix comment. The module docstrings, the two table cases' docstrings and `CONTRIBUTING.md`'s job sentence made true. The `seal/releases/0.9.5.md` row corrected, this item's fragment written, the changelog fragment written | Executed: `tests/test_arm_check.py` on 3.12, 3.13 and 3.14 (the commands above). Executed: `bin/test tests/test_ci_gives_the_checks_what_they_need.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py tests/test_a_script_says_which_interpreter_it_needs.py tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q`, and `tests/test_release_hygiene.py` for the floor case and the version sweep. Executed: `uvx ruff check` and `uvx ruff format --check` on the touched `.py` files. Executed: C2's three runs. Executed: `evidence-check` on the fragment and on `seal/releases/0.9.5.md` | |

**The order inside the phase, because §15 decides it.** Commit at each step.

1. `bin/test tests/test_arm_check.py -q` builds the 3.14 `.venv` and shows the
   base's two reds (S3, the old S4).
2. Write S1 and S2. Seen red on 3.14 at the base, refused.
3. Classify the two names and add the range table. S1, S2 and S3 turn green
   on 3.14.
4. Rewrite S4 and add S5. Seen red by the mutants the spec names, on the
   interpreters it names, then restored.
5. Write S6. Seen red naming 3.14, because no job runs the module there.
   Add the job. Green.
6. Docstrings, the matrix comment, `CONTRIBUTING.md`, the ledger, the
   changelog fragment.

## Ledger

**Corrected in place** (`CLAUDE.md` §*Repo rule — a change writes fragments*,
"its claim first corrected in place with a `Corrected <date>` note"):

- `seal/releases/0.9.5.md`, the row "An arm shape the walk does not recognise
  is refused, not skipped, and the classification is total over the grammar —
  all 122 of this interpreter's AST constructors". The 122 is what 3.12 and
  3.13 have, and it was true where it was measured. "Total over the grammar"
  was false on 3.14 from its release until this item: two constructors
  unclassified, five classified names absent. The note says so, names #684,
  and points at this item's fragment for the per-interpreter claim. Its three
  anchors (`#_refuse_unknown`,
  `#test_every_ast_constructor_is_classified`,
  `#test_an_unclassified_node_type_is_refused_rather_than_skipped`) are units
  this plan does not edit. If the build touches one, it re-reads the row
  against that edit and re-stamps it with a dated note.

No other row anchors a unit this plan edits (read: every
`arm_check.py#…` and `test_arm_check.py#…` anchor in `seal/ledger.md`,
`seal/releases/*.md` and `seal/ledger/*.md`: 22 citations in nine rows, eight
in `seal/releases/0.9.5.md` and one in `seal/releases/0.15.1.md`, found by
grepping the three for anchors on either file). `NOT_ARMS` and
`CLASSIFIED` are anchored by none.

**New rows**, in `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md`,
each executed and dated by the build:

| # | Claim | Anchors |
|---|---|---|
| L1 | A t-string's node types carry no arm, and an interpolation's arms are counted where they stand, exactly as an f-string's | `arm_check.py#NOT_ARMS`, pinned by S1 and S2 |
| L2 | On every Python from the floor to 3.14 the tables name exactly that Python's constructors, with the names only some of them have declared and checked from both sides | the range table's unit, pinned by S3, S4 and S5 |
| L3 | Every version at which the declared ranges change is one CI runs `tests/test_arm_check.py` at | pinned by S6 (the workflow is read by the case, not anchored) |

## Operational impact

None for a user beyond the fix. No new dependency, no new environment
variable, and the command line is unchanged. CI gains one job with two legs on
`ubuntu-latest`, installing only pytest. Whether it is a required check is a
ruleset setting outside the tree (`questions.md` Q2).
