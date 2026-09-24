# 1790221963-a-release-writes-the-gathered-text-back — phase 1

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/phases/phase-1.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1d177b26 |
| Ran by | unknown — the spawn prompt did not hand the value over, and the template forbids the segment naming itself; the orchestrator fills it |

## What this phase was asked

The #557 filter, as the paste-ready fix in #557's body: a gathered
fragment's sentences read at `a` by the gatherer's path,
`seal/specs/<id>/changelog.md`, held and never written. `corrected`'s
docstring saying why. The three module sentences that say a gather deletes
or retires a fragment, made true, because the gatherer deletes nothing.
Cases G1 (H1k, #557's verbatim), G2 (H1, red under a mutation reading the
held set at `b`) and G3 (H2k), each seen red at `61f0d0d8` first.

## What this phase found

**The frame held.** The fix applied to `61f0d0d8` as written, and the three
cases were red there exactly as round 3 of step A measured at `0c335744`:
each exit 0 with `against 2 sentence(s)` (executed, the working tree's
`survivor_check.py` byte-identical to `61f0d0d8`'s). With the fix the module
is 99 passed, 96 before plus the three cases, including
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`:
the fragment list is built from markers, not from a git path listing.

**G2 is the only case the read-at-`b` mutation reddens.** With
`read_blobs(root, b, fragments)` in place of `a`, 1 failed and 14 passed
over every release, changelog and fragment case (executed from Python, the
file restored byte-identical and `tests/__pycache__` cleared). G1 and G3
leave the fragment standing at `b`, so they cannot tell the two ends apart,
which is why G2 exists.

**One sentence of the paste-ready comment was not true of both gatherers,
and was reworded.** #557's comment said the fragment is read at `a`
*by the path the gatherer globs, which the release does not delete*. A
gatherer that deletes the fragment is the case G2 pins, so the sentence was
false for exactly the gatherer that reading at `a` exists to serve. It now
says the fragment stands at `a` *whether the release leaves the fragment or
deletes it*. The code is #557's verbatim.

**The three *deletes / retires* sentences** now name both shapes: this
repository's gatherer leaves the fragment in place (and `settle` retires the
work item later, `gather_changelog.py`'s own docstring), a gatherer that
deletes it or a range that edits a gathered one would put its sentences in
the range as removed. The module docstring's released-changelog paragraph
also gains one sentence saying the gathered text is held and never written,
so the module's account of that exclusion states the new rule.

G2's fixture deletes the fragment with `os.remove` before `build`, whose
`git add -A` stages the deletion.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence *a release that removes no live sentence writes nothing, which keeps a gathered release's text out of `written`* (`corrected`'s docstring) | `corrected`'s docstring: a gathered fragment's text is held and never written, and a release that removes no live sentence writes nothing at all. Ledger rows F1 and C2 carry the same false clause and are corrected in phase 4 |
| *a release's gathering commit deletes each fragment* (module docstring), *the range that gathers it deletes it* (`#307` comment), *the release that gathered it is what retires the file* (`a_gathered_fragment`) | The same three places, reworded to be true of a gatherer that leaves the fragment and one that deletes it |
