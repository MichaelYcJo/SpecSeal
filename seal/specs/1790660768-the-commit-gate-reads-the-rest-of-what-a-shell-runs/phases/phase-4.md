# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 4

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | bc2ddabe |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 4: the merged view for the operators the splitter cut
(`spec.md` P6, decision 3). It glues a segment that ends in a bare operator to
the next across `&` or `|`, and glues an `&` onto a following segment that
begins with `>`, folding chains. `commit_invocations`, `_reads_a_commit` and
`names_an_unknown_command` read it beside the original segments. It adds only
what no part found, with the directory of the part holding the command word
or host. S6 is seen red at `86256492`. S6's control holds:
`commit_invocations` on `git commit -m x 2>&1 | tail -1` equals its base
list. The round-1 controls followed by `2>&1` stay silent.

## What this phase found

**The splitter is untouched, and the view is two functions.** `merged_view(items)`
returns `(parts, tokens)` for every group of two or more parts, and
`merged_segments(command)` returns the tokens alone for the two boolean
readers.

- `_reads_a_commit` reads the merged segments after its own, and so does
  `names_an_unknown_command`. Both answer with a boolean, so reading more only
  adds.
- `commit_invocations` now keeps, per segment, which kinds it found (`commit`,
  `eval`, `string`), through a helper `_segment_invocations` that holds the
  loop body as it was. A group adds a kind only where none of its parts found
  that kind. That is what keeps S6's control to the base's single invocation,
  `2>` among its arguments.

**A leading `&>` was phase 1's already.** `&>/dev/null git commit` arrives as a
first segment that begins with `>/dev/null`, with `&` as its separator, and
phase 1's reader reads past that. It is planted with the phase 4 rows and was
green before this phase.

**Two mutants survived the first run, and each changed something.**

- *Gluing across any separator.* A bare operator before `&&`, `||` or `;` is
  something bash refuses (executed: `bash -c 'echo x > && echo y'` gives a
  syntax error). So the separator test in the view only ever meets input no
  shell runs. The pin that first held it compared group sizes and passed
  either way. It now names the exact groups, including those two refused
  inputs, and the mutant is killed.
- *Taking the first part's directories.* This one could not be killed, and
  `overview.md` says why. The owner computation was removed, and the group's
  additions take the last part's directories.

**Seen red.** 38 cases failed at `b94054ae` against phase 3's reader, which
has no view, and so against `86256492`'s. The controls, S6's control and the
`&>f git` row passed there, as each must.

**Mutants.** Each ran alone under `PYTHONDONTWRITEBYTECODE=1` and was restored
from saved bytes. After each run the tree held only the committed state plus
the edit then in progress.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | no gluing at a bare operator | `sh -c 2>&1` |
| 2 | gluing after any last word | `MERGED[&>>f after a word]` |
| 3 | no `&>` gluing | the same |
| 4 | gluing across any separator | `SEPARATE[a bare operator before &&]`, once added |
| 5 | no gluing at `\|` | `>\|f git` |
| 6 | the glued token loses its separator | `MERGED[>\|f]` |
| 7 | no chain | `a chain: >&2 2>&1 git` |
| 8 | the word reader reads no merged segment | `sh -c 2>&1 $CMD` |
| 9 | `_reads_a_commit` reads no merged segment | `a commit behind 2>&1 in $( )` |
| 10 | `commit_invocations` reads no view | `sh -c 2>&1` |
| 11 | a group adds a kind a part found | `test_a_commit_the_splitter_already_found_is_not_found_twice` |

**Verification.** Executed at `bc2ddabe`: the 26 modules, 1472 passed and 1
skipped, exit 0. The frame's 42 shapes through `main()` at `86256492` and at
`be3a447f`: all six S6 rows moved from silent to deny, and the S6 control
stayed silent in a declared repository. None moved from deny to silent.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* 38 cases at `b94054ae`, and every changed branch has a
  mutant a case kills.
- *Failure direction.* The view is read beside the segments the splitter
  made and never instead of them. A group adds only a kind of invocation
  that none of its parts found. `commit_invocations` on `git commit -m x
  2>&1 | tail -1` is the base's list, pinned.
- *Prompt budget.* A commit, a string, an `eval` or `watch` behind `2>&1`,
  `>&2`, `<&0`, `>&-`, `>|f` or `&>f` now meets the gate. Commands that
  commit nothing meet no new stop from the view alone: the round-1 controls
  behind `2>&1` and `>&2`, and followed by `2>&1` and `2>&1 | tail -1`, all
  stay silent in a declared repository (planted).
- *Why nothing cheaper.* Teaching the splitter these operators moves every
  segment in both gates and in the walk, and `cd W 2>&1 && git commit` would
  then read silent where `86256492` stops (`plan.md` Alternatives B).
- *Platform honesty.* String reading only.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
