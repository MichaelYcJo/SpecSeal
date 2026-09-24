# 1790221963-a-release-writes-the-gathered-text-back — phase 3

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/phases/phase-3.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 6ac7a028 |
| Ran by | unknown — the spawn prompt did not hand the value over, and the template forbids the segment naming itself; the orchestrator fills it |

## What this phase was asked

#555: G5 (P6d, a release entry written directly with no marker and no
fragment, nothing lost) seen red with the `lost` guard removed and the
filter kept; G6 (P6, a gather with nothing lost) seen red only with both
removed; each single removal's result on G6 recorded (Q2).

## What this phase found

**Q2: green under each single removal, red with both, as `spec.md`
judgment 4 read it.** Three mutations from Python over the 24 release,
changelog, fragment and prose cases, the file restored byte-identical and
`tests/__pycache__` cleared after each (executed):

| Mutation | Red | Green |
|---|---|---|
| `if len(gone) == lost:` → `if False:` (guard off, filter kept) | G5 alone | the other 23, G1 (H1k) and G3 (H2k) among them |
| the filter's `sentence.key not in shipped` → `True` (filter off, guard kept) | G1, G2, G3, G4 | the other 20, G5 and G6 among them |
| both off | G1–G6 | the other 18 |

So each unit now has a case that goes red when that one alone is removed:
the guard G5, the filter G1–G4, the marker blank G4 (phase 2). G6 pins
neither alone and says so in its docstring. That is the §15 failure #555's
body would have planted had P6 been its only case.

Unmutated, the 24 cases passed. G5 and G6 are pins, so neither is red at the
tip, and each was shown red by the mutation that names what it pins.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
