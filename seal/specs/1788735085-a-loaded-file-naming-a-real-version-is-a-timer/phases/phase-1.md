# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `62287e9` |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Widen `test_no_loaded_file_hardcodes_the_running_version` to refuse every
version at or above the running one, over version-shaped tokens with an
optional `v` prefix. Give `RECORDS_OF_A_MOMENT` a `docs/experiments/` entry
with its argument, declare the illustrative version and bash's each with its
reason, and make the failure message name the file, the line, the token and
what to write instead. The illustrative value must assert that it is neither
shipped nor shipping.

The case had to be seen **red** first against line 28 of
`docs/issues-and-milestones.md` on the unmodified document, with fixtures for
a below-running version, an at-or-above one and the illustrative one.

## What this phase found

**The check had to be renamed, and `plan.md` did not settle that.**
`test_no_loaded_file_hardcodes_the_running_version` becomes false about itself
the moment it refuses `0.9.0`, which is not the running version. It is now
`test_no_loaded_file_names_a_version_at_or_above_the_running_one`, and three
loaded documents plus one ledger note named it by the old name. The one
reference left alone is
`seal/specs/1788661274-…/rounds/round-2.md`: a round record names what the
check was called at the moment it ran, and rewriting it would falsify the
record — the same reasoning `docs/issues-and-milestones.md` already applies to
rolling-log titles.

**The enumeration in `plan.md`'s technical context is short by one token.**
Re-run here over the same nine prefixes at `6f96eab`, the loaded set is 64
files and carries `v0.3.0` at line 156 of `docs/issues-and-milestones.md`, on
the same line as the `0.2.0` the table does list. It changes nothing — both
are below the running version and both are kept — but the `v`-prefixed
spelling is the one a regex can silently drop, so it is the token the
enumeration could least afford to miss. The five distinct bare tokens the plan
names are otherwise exactly what is there.

**The mutation run found a missing case and a hollow assertion**, and both are
in the committed phase rather than in a note. Eleven mutations, one at a time
with `tests/__pycache__` cleared between each:

- Comparing the tokens as **text** instead of as numbers survived every
  fixture. `0.10.0` is above `0.8.3` and every string comparison disagrees —
  and `0.10.0` is the version #179's own body names as the one the next author
  writes. `test_a_two_digit_component_compares_as_a_number` was added for it.
- Dropping the regex's lookaround was caught only by the walk over the real
  tree, not by the case written for it. The case asserted that `1.2.3.4` reads
  as no version, and the first three components of `1.2.3.4` are the
  illustrative version — so the exemption answered `[]` whether the lookaround
  was there or not, and the assertion pinned nothing. It is now `2.0.1.5`, and
  the case goes red on that mutation.

After both, every mutation is caught and each of the seven fixtures goes red
on at least one.

**This phase's commit leaves the suite red on purpose.** The widened case
fails on the one offender it was written for, which is the redness
`CONTRIBUTING.md` §*What a change to a gate must carry* asks a gate change to
show. Phase 2 is what turns it green, and the two commits are what record
that the case can fail.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the name `test_no_loaded_file_hardcodes_the_running_version` | `docs/flow.md`, `docs/issues-and-milestones.md`, `docs/release-checklist.md` and `seal/ledger.md`'s S15 note all now carry the new name; the ledger note keeps the old one beside it so a reader coming from an older record can follow it |
| the substring test `version() in f.read()` | replaced by `timers_in`, whose behaviour is pinned by seven fixtures rather than by the tree happening to be clean |
