# 1790221963-a-release-writes-the-gathered-text-back — phase 2

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/phases/phase-2.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c90821fb |
| Ran by | unknown — the spawn prompt did not hand the value over, and the template forbids the segment naming itself; the orchestrator fills it |

## What this phase was asked

The marker line, conditional on Q1: plant G4 (a gathered fragment whose
body opens with a plain sentence equal to `FOUND`, in the gatherer's layout,
under the H1 release shape) and run it with phase 1 in place. Only if it is
red, blank a `MARKER` line in `newly_released`'s `released` closure with a
comment saying why. If it is green, change nothing and record the
measurement.

## What this phase found

**Q1: red.** With phase 1's filter in place G4 exited 0 with `against 2
sentence(s)` and `no removed wording is still standing` (executed). The
released text's sentence keys, printed through the module's own
`newly_released`, were `1 0 0 2026 01 01` (the heading),
`specs 1700000003 a shipped item the verdict cell is written by …
afterwards` (the marker's words fused with `FOUND`) and the fragment's
second sentence. The fused key is in no fragment, so the filter missed it
and `FOUND`'s grams reached `written`, exactly as `spec.md` judgment 3 read
it.

**The blank landed as planned**, `MARKER.sub("", only_released(text))` in
the closure, so both ends of the range are read the same way. With it the
module is 100 passed. With the blank removed by mutation (Python, the file
restored byte-identical, `tests/__pycache__` cleared) the whole module ran
1 failed, 99 passed, and the one failure was G4. So nothing else in the
module leans on the marker being read as prose, including the four real
ranges.

**Q4: the fixture imports the gatherer's own `section` by path**
(`gathered_section` in the module), the frame's default. One divergence
from the framing: Q4 said `tests/test_the_changelog_is_gathered_at_release.py`
*loads* the gatherer. It runs it as a subprocess and imports nothing. The
import still works because `gather_changelog.py` puts `hooks/` on
`sys.path` itself before importing `console`. The case asserts that the
section it built still has the body directly under the marker, so a
gatherer that starts writing a blank line there turns the case red with a
sentence saying so rather than leaving it green for the wrong reason.

`MARKER` is defined below `newly_released` in the file. It is read when the
closure runs, never at import, so the order is harmless.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
