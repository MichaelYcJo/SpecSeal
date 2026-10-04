# the broad gate re-runs the test command at the base — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

Nobody was asked anything during this run (`routing.md`: `Answer pressed` =
`automation`). Every row below therefore carries the default the build uses,
and none of them blocks it.

**Judgments the tickets left open that the tree answered** — listed so nobody
reopens them. Grounds are in `spec.md` and `plan.md`'s Alternatives table.

| Judgment | Answered by |
|---|---|
| Find the runner by measurement (the first prefix whose output carries pytest's summary), not by name, not by a config row | `CLAUDE.md`'s first goal; `plan.md` Alternatives A–E |
| A prefix, not a part run alone | Alternative B: a part alone can fake `failing on base too` |
| Keep this repository's row lint-first; rewrite rule 3 rather than the row | commit `7a39f2f7` (#634), the owner's reorder |
| The cut keeps substrings of the row; no tokenise-and-re-render | `broad_gate.py#command_names_backslashed`'s docstring |
| `( … )` and `{ …; }` groups are not modelled and read `new?` | `templates/config.md` §*What is refused, and what stays allowed* (no shell parser) |
| A branch-side `ERROR`-only failure stays uncompared | out of this work's class: an absence, not a false word (`spec.md` Out) |
| #748 polls the marker with a re-unlink per window, not a PID | `plan.md` Alternative H |

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does a file the BASE reports as `ERROR` (it cannot be collected, or its setup errors) read `failing on base too`? The tree could not settle it: `README.md` and `skills/verify/SKILL.md` define the word as "not this work's finding", and whether an error that predates the branch is a *failure* for that purpose is what the word should mean, which no document states | a person — the repository owner | **yes**: the base already fails it, so the branch did not break it; the word stays a measured one because a line names the file. **no**: such a file reads `new?` with "errors at the base", and the reader decides | yes — `spec.md` Scope 3 | ⬜ decided-by-framer |
| Q2 | What does rule 3 of `templates/config.md` §*Choosing a value* now recommend about ORDER? The tree could not settle it: the rule's only reason (the comparison used the first command) is gone, and whether the template should still prefer runner-first is advice to every repository | a person — the repository owner | **state both, recommend neither**: the rule becomes "the runner is a part of the row a cut can stop after", and says runner-first costs one base run and lint-first re-runs the earlier parts per prefix. **keep recommending runner-first** for cost. **recommend lint-first** as #634 chose here | state both, recommend neither — the rule is about what the comparison can measure, and order is the repository's trade | ⬜ decided-by-framer |
| Q3 | The exact text pytest prints for an interrupted collection and for a maxfail stop under `-q`, in the version `bin/test` installs. The tree could not settle it: no file in it records either banner | a measurement | one probe in a scratch directory per banner, before phase 3's reading is written | the build measures it in phase 3 and records the strings in `phases/phase-3.md` | ⬜ |
| Q4 | The exact wording of each `new?` reason (no prefix ran pytest; the base run was interrupted). Unknowable until the reading is written; `spec.md` fixes only that each starts `new?` and says the comparison was not measured | the work | phase 3 writes them, phase 4 pins them (§14) | — | ⬜ |
