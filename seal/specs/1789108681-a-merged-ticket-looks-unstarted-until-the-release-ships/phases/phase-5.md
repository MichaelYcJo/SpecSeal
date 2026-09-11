# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — phase 5

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `d18aa20` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

`seal/specs/<id>/changelog.md`, any ledger rows in `seal/ledger/<id>.md`, and
the closing memo. Verified by the fragment conventions in `CLAUDE.md` and by
`unverified_check` on the memo's `## Not verified` table.

## What this phase found

**The record checker refused a record, and it was right.**
`evidence_check.py --strict .` exited **2** on
`phases/phase-2.md:55`: the record spells `GITHUB_TOKEN`, and nothing outside
`seal/` carries that name — the workflows here pass `${{ github.token }}` into
`GH_TOKEN`, which is what `gh` reads. It is GitHub's own name for the token a
workflow run is given, quoted verbatim from their reference, so the line
carries `NAME NOT IN TREE` with that reason rather than being paraphrased.
Paraphrasing would have turned a reading of the documentation into a claim
about it, which is the one thing a `read`-labelled fact must not become.
`tests/test_a_record_states_what_the_tree_has.py` fails on the same finding,
so this was a red suite and not only a red checker.

**Eight rows, seventeen coordinates, and the ones worth a row are the ones a
later session would otherwise re-derive.** Not every acceptance criterion —
S1, S5, S7 and S11 are pinned by cases and by nothing subtle, so a row would
only repeat the case name. What went in is the reasoning that is invisible in
the diff: which of the two label directions fails and why, that the re-run
guarantee is structural rather than an assumption about GitHub, that
`gh issue list` and REST `/issues` disagree about pull requests, that a
milestone which does not exist answers with an empty list and exit 0, and the
fork-point range.

**The `## Not verified` table has four rows and every one names a person or an
agent.** Two of them — Q3, and S12 — are answerable only after this branch's
own squash, because both need a real run of a workflow this branch adds. A
fourth was added while writing the memo rather than carried from a phase: the
`permissions:` block newly stated on `hygiene.yml` is argued to be narrower
than whatever it replaces and nothing has run it, and this branch's own pull
request is the first run.

**Nothing in `seal/follow-up.md` was a prerequisite of this work and nothing
in it is closed by it.** Read in full at the start. The rows there are about
the evidence checker, the chain check's worktree flag, two agent definitions'
line wrap, a survivor-check exclusion, five scripts below the interpreter
floor, a refusal's untested half, a third `Status` value, and the third
routing axis's template pin — none of them touches the tracker or the release
gate.

**The fragments go where `CLAUDE.md` says and neither shared file is
touched.** `CHANGELOG.md` and `seal/ledger.md` are unmodified in this
branch's diff; the entry is
`seal/specs/<id>/changelog.md` and the rows are
`seal/ledger/<id>.md`. Nothing this branch removes is cited by an existing
`seal/ledger.md` row, so the removal case that forces the shared file open
does not arise.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
