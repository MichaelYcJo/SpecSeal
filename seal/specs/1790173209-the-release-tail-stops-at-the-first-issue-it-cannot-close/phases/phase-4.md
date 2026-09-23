# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 4

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-4.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 48f81864 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#363. `shipped_tags(root)` via `conftest.git_listing`; `timers_in(…,
shipped=frozenset())` keeps a tagged version; `timer_offenders` passes the
root's tags; a real-tree case asserts tags are readable; the refusal text's
*A version BELOW the running one is history* sentence widens to *below, or
tagged*; `docs/release-checklist.md` §3's table row updated; R1/R3 rows
re-read and `--reverify`. Verified by S9 (seen red), S10 (fixture + real
tree), S11 (the bumped, untagged version still refused),
`test_a_version_below_the_running_one_is_history_and_is_kept` unedited and
green, `evidence-check --strict` green after `--reverify`.

## What this phase found

**The spec's S10 fixture could not go red, so the fixture tags its running
version instead.** S10 wrote *`plugin.json` at `0.2.0`, a tag `v0.1.0`, a
loaded file naming `0.1.0`, `0.2.0`, `0.3.0`; then `timer_offenders(root)`
names `0.2.0` and `0.3.0` only* — which is what the unfixed sweep answers
too, because `0.1.0` is below the running version and history either way.
The case tags `v0.2.0` and expects `0.3.0` alone; that is the reading that
was red at `7fac7bec` and the one the shipped set changes. A tag that is not
version-shaped (`v-not-a-version`) is in the fixture as well, and is dropped.

**The rule is stated in more places than the frame listed.** §12: the class
is *every sentence that says what the sweep refuses*. Besides the checklist
§3 row and the refusal text, `docs/release-checklist.md` §5's statement
(*covers every version at or above the running one*) and two paragraphs of
`docs/issues-and-milestones.md` said it — the one explaining why the two
releases are named rather than numbered, which ended *#363 is where that is
repaired, and not here*, and the one under the rolling log's title saying
*a version below the running one is history and is kept*. All four carry the
tagged clause now. The named-rather-than-numbered paragraph keeps its prose
citations, on new grounds (a description reads the same on every release);
`test_the_two_releases_are_cited_without_a_version_number` still pins them.

**Red at `7fac7bec`, quoted:**

```
E       TypeError: timers_in() got an unexpected keyword argument 'shipped'
E       NameError: name 'shipped_tags' is not defined
E       NameError: name 'shipped_tags' is not defined
3 failed, 41 deselected in 0.45s
```

Green at `fbfa199b`: `52 passed` over `tests/test_release_hygiene.py
tests/test_a_release_is_sized_by_a_criterion.py`; `119 passed` after the
document edits over those two plus
`tests/test_a_release_rolls_the_flow_measurement_issue.py
tests/test_the_release_tail_does_not_end_at_the_tag.py
tests/test_no_real_identifiers.py tests/test_the_changelog_is_gathered_at_release.py`.

**Mutations**, six, in the ledger fragment's P4 row. The one that survived
— the refusal text losing the tagged route — is what §14 is about: a change
to what a person reads, pinned in the same commit by a `TAGGED` assertion in
the routes case, red (1) since.

**On this tree the widening changes no verdict today.** `plugin.json` names
the version the last release tagged, the tag is readable, and nothing under
the loaded set names that version, so the sweep reports no offender with or
without the change. What changed is what a document MAY say from here.

**The shared ledger.** Nine rows drifted, because three documents and four
units the rows anchor on changed. R1 (the timer rule) is corrected — *may
not name one at or above it* reads *… and not tagged*, the exemption count
unchanged because history is not an exemption. R3 (the two releases named
in prose) is re-read: the off-by-one it filed is repaired and the prose
citations stay for a different reason. S4 (the tracker document states the
rule the way the check behaves) is corrected for the tagged clause in both
halves. G5, T1, C5, R5, R1-sizing and R3-refusal are re-read with the claim
holding. `evidence-check --strict` exits 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *#363 is where that is repaired, and not here* in `docs/issues-and-milestones.md` | the same paragraph, which now says the repair landed and why the citations stay prose |
