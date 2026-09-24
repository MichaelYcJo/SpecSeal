# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — phase 3

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 78610546 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

An unresolved declaration prints only to the run it addresses (#439):
`whole_range` asks ownership before printing `unresolved`; cases S13 and
S14, S13 red first; the branch's own sweep
`bin/survivor-check --range origin/release/v0.15.1...HEAD` with every
`seal/specs/*/survivors.md` prints zero `unresolved` lines; Q5's move probe
driven from Python, its result recorded here.

## What this phase found

**The shape of the change.** `whole_range`'s loop used to append an
unresolved declaration and `continue` before the ownership question was
reached; the question is now asked of every declaration that is either
unresolved or resolved onto this run's range, from the same lazily computed
`changed` list and the one `git diff --name-only` call site, so
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
still counts one call in that scope and `NAMED_EXCEPTION`'s grounds still
rest on `foreign` in the body. A declaration with no owner — an `--exempt`
file passed from outside any `seal/specs/<id>/` — keeps the hand-run reach
and prints, which is the existing G6 case; one owned by a work item the
range touches prints, which is the new S14 arm.

**S15, measured at `78610546` on the working tree over the committed tip
`a509b35a`:** `python3 skills/code-review/scripts/survivor_check.py --range
origin/release/v0.15.1...HEAD --exempt <each of the ten seal/specs/*/survivors.md>`
— exit 0, `examined 383 files`, `against 2 sentence(s)`, **zero
`unresolved` lines and zero `not yours` lines**, where the same command at
`9f846733` prints three `unresolved` lines (`origin/release/v0.10.0`,
`v0.11.0`, `v0.13.2`). The seal reads it again over the finished branch.

**Q5 — the move probe, executed 2026-09-24 from Python in two throwaway
repositories, removed afterwards.** A two-sentence section stated in `a.md`
with its claim quoted in `notes.md`, twelve filler files beside them:

| Shape | Result |
|---|---|
| moved to `b.md` verbatim in one commit | exit 0, `against 0 sentence(s)` |
| moved with the claim reworded (`REPAIRED` for `FOUND`) | exit 1, `notes.md:3` at 2.00, corrected `a.md:5` |

That is the result spec judgment 7 predicted, and no case is planted for
it. But the verbatim move is silent for a reason the judgment does not
name: `against 0`, not *removed and written back*. `git diff --name-only`
runs with rename detection on, so a 100 % move lists `b.md` alone, `a.md`
never enters `paths`, and nothing is removed at all. The reworded two-
sentence section fell under git's similarity threshold, so both paths were
listed and `wanted` did the work the judgment describes.

**A third shape, probed because of that, is a defect the sweep carries
today and outside this work item's phases.** A forty-paragraph section moved
to `b.md` with one sentence reworded is a rename to git (`R096`), so the old
path is not listed, the reworded sentence is never a removed sentence, and
`notes.md`'s copy of the old claim stands unreported: exit 0, `against 0
sentence(s)`. #526's split — sections moved between files that both remain
— is not this shape, because a file that stays is never a rename; a whole
file moved with a small correction is. The repair is `--no-renames` on the
two `git diff --name-only` calls (`corrected`, and `whole_range`'s `changed`
list for the same reason), with a case in the shape above seen red first.
It changes what the range reads, so it is a gate change with its own row in
the gate table, and it is handed back for the orchestrator to file rather
than taken here; `overview.md` §*Not done* carries it too.

**Seen red first, executed 2026-09-24 against the script at `93acc277`:**
S13 at exit 1 with `unresolved  origin/gone..HEAD …` printed. S14's two
arms — the existing G6 case from outside any work item, and the new one
under the work item the range touches — green before and after.

**Mutations, executed at `78610546` from Python, file restored
byte-identical each time:**

| Mutation | Cases run | Result |
|---|---|---|
| an unresolved declaration is appended before ownership again | S13 | red |
| an unresolved declaration is never appended | S14's two arms | red (2 of 2) |
| `owner` is always `None` | S13, the `not yours` cases | red (4 of 4) |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `unresolved` line for a declaration of a work item the range touches nothing of | nowhere — the line was addressed to nobody, and the row it printed for still says what it says in its own `survivors.md`; `docs/review-chain-spec.md` §*The survivor sweep* still says a spec that will not resolve is printed, which is true of the run it addresses |
