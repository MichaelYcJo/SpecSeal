# Round 1 — the fix pass

The fix range is `5cf81b3..4729bbe`, two commits. Every finding of round 1
was open; each was reproduced with a probe before it was touched, and each
fix was shown to bite by breaking it and watching the case go red.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | 60d5354 |
| 2 | fixed | 60d5354 |
| 3 | fixed | 60d5354 |
| 4 | fixed | 60d5354 |
| 5 | fixed | 60d5354 |

## What each fix does, and the command that proves it

**1 — the guard's signal is the field's TYPE.** `theirs` was checked for
presence alone, so `null` — the shape any JSON writer gives the `None` this
work item introduced — counted as an answer, and `normalise_remote` reduced
it to `""`, switching the other-repository check off as well. The refusal now
fires on `not isinstance(theirs, str)`, which covers absence and every
non-string with one test. Pinned by
`test_a_manifest_remote_of_the_wrong_type_refuses`, parametrised over `None`,
`42`, `[]`, `{}` and `True`, asserting exit 1 and the root unchanged.

**2 — the advice names the machine that can fix it.** One closing line
covered two failures with two different next steps. It is now two, and the
ZIP's silence is what decides between them: no re-run here clears that side
whatever this clone's git answers next. Pinned by
`test_the_advice_names_the_machine_that_can_fix_it`, which runs all three
combinations — the zip alone, this clone alone, and both.

**3 — the export names what it could not read.** `manifest_of` returns
`(manifest, unread)` and the export prints a line per omitted field, plus one
sentence for `remote` saying that running the export again writes a zip the
other machine takes in without a flag. Pinned by
`test_the_export_says_what_it_could_not_read` and, in the other direction, by
`test_an_export_that_read_everything_says_nothing_extra`.

**4 — `remote_url`'s docstring enumerates exit 1's third meaning.** A `root`
that is not a repository also exits 1 with both streams empty, so the
docstring now says exit 1 is an answer *only for a caller whose `root` git has
already resolved*, and names why this caller can say that. No code change: the
finding is not reachable through `resolve`, which the reviewer measured and I
re-read rather than re-measured.

**5 — `manifest_of` admits both fields by the same test.** `if head` became
`if head is not None`. Behaviour-identical today, by construction, which is
why no case can catch it — see the mutation table below, where M6 is the one
that survives on purpose.

**2 also lands in both READMEs**, which carried the same wrong reading —
`README.md` said *only the second is a reason to run the command again*, and
`README.ko.md` said the flag's case is worth one re-run first. Both now say
which side's silence decides and what each one means. The export's new output
is documented in both as well.

## What re-enumerating the diff found

Three things, none of them a round-1 finding, all measured rather than
reasoned. The first two are defects the first fix commit introduced, which is
the shape this repository has seven measured instances of.

**E1 — the advice branched on the wrong side, and the case pinned it that
way.** `if mine is None` is right when one side is silent and wrong when both
are: a zip with no `remote` AND a git that timed out here printed *Run this
again if the failure here was transient*, which is finding 2's own defect
re-entered at a narrower coordinate by the fix for finding 2. Worse, the case
I had just written asserted that output as correct. The branch is now
`the_zip_is_silent`, and the case runs all three combinations. Fixed at
`4729bbe`.

**E2 — the flag sentence was keyed on either field.** `manifest_of` returned
a flat list of reasons, so the export could not tell which field went unread.
An export that read the remote and only missed the HEAD SHA printed *the other
machine takes in without a flag* — a fix promised for a refusal that was never
coming, because only `remote` is refused on arrival. The reasons come back
keyed by field. Fixed at `4729bbe`.

**E3 — four escape cases were disarmed by the clock, and this predates the
branch.** `test_a_link_at_the_partial_name_refuses_the_export` and three
siblings name the `<stem>.zip.partial` they plant a link at from
`datetime.date.today()`, the LOCAL date, where `seal.py:542` names it from
UTC. East of UTC the two differ between local midnight and UTC midnight, so
for nine hours a day in this timezone the link lands at a path the export
never touches: the export succeeds, nothing goes outside, and four cases
assert a refusal against nothing.

Measured at `5cf81b3` with no other change in the tree, 2026-09-08 06:50 KST:
all four red, `wrote …-2026-09-07.zip` at exit 0 against a link planted at
`…-2026-09-08.zip.partial`. Round 1 ran the same module green nine hours
earlier, which is the whole point — a case armed or disarmed by the hour it
runs at reports nothing either way. The four now take the stem from
`the_stem_the_export_will_use`, one helper on the same clock the export uses.
What is left is the UTC midnight instant itself, microseconds a day where it
used to be hours.

**One existing case had to move rather than break.**
`test_a_manifest_field_of_the_wrong_type_does_not_raise` asserted that a
wrong-type `remote` imports at exit 0 without raising, which fix 1 makes
false. Its two `remote` rows now go through `--allow-unreadable-remote`,
which is the only path on which such a value still reaches
`normalise_remote` — and `normalise_remote`'s `isinstance` guard, which is
what those rows have always been about, lives on exactly that path. The two
`head` rows are untouched, and the RIDER above the list still applies.

## Executed

| What was run | Result |
|---|---|
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py -q` at `4729bbe` | `96 passed`, exit 0 |
| `bin/test` over `test_docs_line_wrap`, `test_no_real_identifiers`, `test_lint_python`, `test_one_word_one_meaning`, `test_the_pull_request_language_is_the_repositorys`, `test_a_probe_does_not_outlive_its_round` | `164 passed`, exit 0 |
| `bin/test tests/test_release_hygiene.py` (with the five above, before the second commit) | `194 passed`, exit 0 |
| `ruff check` and `ruff format --check` on `seal.py` and the changed test module, via `uvx` | exit 0 and exit 0 |
| The three round-1 probes, rebuilt at `5cf81b3` before any edit | all three red — `7 failed`: five wrong-type values imported at exit 0, the re-run advice printed for a zip-side silence, the export silent about the field it omitted |
| Two probes for E1 and E2 at `60d5354`, before either was touched | both red, with the offending output captured |
| Eight mutations of the changed units, each pattern asserted to match exactly once | seven killed, one survives on purpose — the table below |

Exit codes were read as `cmd >/dev/null 2>&1; echo $?` or from the runner's
own status, never through a pipe. Both probe files are `test_tmp_*`, were run
once, and were deleted before this record was written.

| Mutation | Case that went red |
|---|---|
| M1 the guard's signal back to key presence | `test_a_manifest_remote_of_the_wrong_type_refuses`, 5 red |
| M2 one advice line for both silent sides | `test_the_advice_names_the_machine_that_can_fix_it`, 1 red |
| M2b the advice branches on this clone, not the zip (E1) | `test_the_advice_names_the_machine_that_can_fix_it`, 1 red |
| M3 the export drops the reasons again | `test_the_export_says_what_it_could_not_read`, 1 red |
| M4 the export names a failure that did not happen | `test_an_export_that_read_everything_says_nothing_extra`, 1 red |
| M4b the flag sentence keyed on either field (E2) | `test_the_export_omits_a_head_it_could_not_read`, 1 red |
| M5 the stem back to the local clock (E3) | the four link cases, 4 red |
| M6 `if head is not None` back to truthiness (finding 5) | **none — 96 passed.** Expected: the change is behaviour-identical by construction, which is the whole of finding 5. Recorded rather than hidden |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `agent-contract` §2 reserves them for the broad gate; nine modules were run narrowly instead | the orchestrator, before the pull request |
| Whether E3's residual window — the UTC midnight instant between the case computing the stem and the export computing its own — is worth closing. Closing it means the case planting a link at both candidate names, which is more machinery than the window costs | the repository owner |
| Behaviour on Windows | CI's Windows leg |
