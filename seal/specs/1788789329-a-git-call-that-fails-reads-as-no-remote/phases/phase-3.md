# 1788789329-a-git-call-that-fails-reads-as-no-remote — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 3c366c2 |
| Ran by | unknown — the spawn prompt named no model, and the template forbids a segment sourcing this from its own idea of what it is. The orchestrator that spawned this segment is the party that can fill it |

## What this phase was asked

Put the new flag where a person looks for it — both READMEs — and write the
two fragments this repository's conventions require: the changelog entry to
`seal/specs/<work-item-id>/changelog.md` and the ledger rows to
`seal/ledger/<work-item-id>.md`, never to `CHANGELOG.md` or `seal/ledger.md`.
A coordinate is `path#major@hash`, never a line number.

## What this phase found

**`seal/ledger/` did not exist.** The 0.9.0 release folded every fragment into
`seal/ledger.md` and removed the directory, so this work item creates it
again. Nothing needed doing about that — a fragment needs no header of its own
— but a session expecting to copy a sibling's shape has none to copy, and the
shape had to be read out of git history instead
(`seal/ledger/1788700685-two-value-shaped-odd-rows-end-the-report.md`, added
at `2f9cb97`).

**A placeholder hash has to be six to twelve hex digits or the row is not a
row.** `ANCHOR_RE` requires `[0-9a-f]{6,12}`, so `@0` matched nothing and
`evidence-check` read the whole fragment as `0 ok · 0 drifted · 0 broken`
at exit 0 — the silence its own `OLD_COORD_RE` comment says is the one
unacceptable outcome, arriving through a different door. `@00000000` parses,
and `--reverify` then stamped all fourteen anchors. Worth knowing before
writing a fragment by hand: the exit code does not distinguish *every row is
fine* from *no row was read*, and the count line is what says which.

**The Korean README needed a sentence the English one carries inside a
parenthesis.** The English enumeration can hang *"a separate flag, because
`there is no remote` and `nobody could say` are different facts"* off the list
item; the same construction in Korean puts a long insertion between the object
and its particle, which `writing-style` §*영어를 옮길 때는 구조를 버리고 뜻만
가져온다* names as the first thing that goes wrong. The reason moved to a
paragraph of its own after the list, which also gives it room to say the thing
a user actually needs: try running it again before reaching for the flag.

**One gate fired on a document rather than on code**, and it is the same one
phase 1 met: `test_release_hygiene.py` reads any three-part version number in
a loaded file as a release timer. The measurement `git 2.50.1` is in
`remote_url`'s docstring, and the row added to `VERSIONS_OF_ANOTHER_PRODUCT`
in phase 1 covers it for this file only — pinned to the file, so the token
cannot walk through anywhere else.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase only adds | none |
