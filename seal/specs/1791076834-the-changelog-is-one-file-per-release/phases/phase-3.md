# 1791076834-the-changelog-is-one-file-per-release — phase 3

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | c2f81269 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The shipped survivor sweep: one changelog-path predicate in
`survivor_check.py` (spec D5), the module docstring and
`docs/review-chain-spec.md`'s two paragraphs rewritten to name both shapes,
and S10 cases beside the existing ones, each seen red against the old
`path == CHANGELOG` comparison. Verified by the survivor module, the GFM
module, the gather module's survivor case, and the sweep run over this
branch's own range.

## What this phase found

**One predicate, `a_changelog`, at every site the spec named.** The root
`CHANGELOG.md`, or `changelog/<version>.md` at the root where the version is
`VERSION_HEADING`'s shape (`RELEASE_FILE`). `sentences`, `corrected`'s
`newly_released` arm and `score`'s split arm ask it in place of
`path == CHANGELOG`; `CHANGELOG` stays, because a test monkeypatches it.

**Q8: the monkeypatch did not keep its shape.** `gathered_fragments` reads
more than one path now, so it has to know the tree. It takes the listing as
an optional `paths` argument and lists the tree with `tracked` itself where
the caller has not; `corpus` hands over the listing it already made, so the
pool costs no second `ls-tree`. The two cases that monkeypatched
`read_blobs` to answer `{CHANGELOG: text}` now pass `paths` and answer for
the paths asked, and the GFM case runs for both shapes with a positive
control (the same marker on a line of its own is read). The assertion holds
for both, as Q8 required.

**The path-list census caught the new listing.**
`test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
failed on `gathered_fragments` reaching `tracked`, and was right to:
`FILTERED_BY_ITS_CALLERS` now declares it, filtered by `a_changelog`, with
the reason beside it. Before the declaration every mutation run below
stopped at `no baseline`, which reads as a mutation that changed nothing;
the first batch's output was that, and it was rerun.

**Two arms are reachable only through a release file holding live prose.**
`corrected`'s held count and `score`'s split matter where a changelog has
text above its first version heading, which a release file the gather
writes never has. The mutation that spelled either back to
`path == CHANGELOG` survived the new cases, so the two root-file cases that
pin them (`…moves_the_unreleased_section…` and
`…replaces_an_entry_with_a_gathered_rewording…`) are parametrized over both
paths, and both mutations went red there.

**Each changelog's markers are read on their own.** A fence one file leaves
open would otherwise hide the next file's marker; a case with the open fence
in the file read first pins it.

**Seen red (§15), executed.** The new cases against `e141980a`'s sweep: 8
failed. Through `mutation-check`, each red: `sentences`'s arm, the held
count's arm and the split arm spelled `path == CHANGELOG` (the last two after
the parametrization), `gathered_fragments` reading the root file alone, its
markers read as one joined text, a release file of any name, and the root
file dropped from the predicate. Dropping the `^` from `RELEASE_FILE`
survived, and is the same pattern: `re.match` anchors at the start already.

**The sweep over the build range** (executed, `e141980a..c2f81269`): 90
sentences removed, three places reported, all in released ledger files and
none under `CHANGELOG.md` or `changelog/`. Phase 4 answers them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence in `gathered_fragments`'s docstring that it reads one file with no path list | the same docstring: every changelog path at the revision, the listing taken from the caller or from `tracked` |
