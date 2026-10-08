# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 951b0a1d |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 4: `SKILL.md`'s three sections and the `BROKEN` verdict row;
the `docs/the-evidence-ledger.md` paragraph with `Enforced by:`; the
docstrings' input class in #835's three words; `changelog.md` with the
installer paragraph; `seal/ledger/<work-item-id>.md` rows for the new
clauses; the sentences *In* 5 removes are gone. Cases S11, S12. The spawn
added: ledger rows go in `seal/ledger/1791384159-a-unit-the-extractor-cannot-bound-is-refused.md`;
a released row is re-read with `evidence-check --reverify --into <that file>
--checked 2026-10-08`; a sibling's fragment row still under `seal/ledger/` is
re-stamped in place.

## What this phase found

**Every released row the rewrite drifted was read, and one claim had become
false.** `seal/releases/0.4.0.md`'s "An anchor resolves to a symbol span via
the stdlib `ast`, or to a quoted line of text" recorded, as verified
behaviour, the fall-through to the text rule for a file that will not parse.
It takes a `Corrected ·` row. The other fourteen released rows held and take
`Re-read ·` rows, written by `--reverify --into` narrowed with `--ledger` to
this fragment and the six release files that hold them.

**The `--into` run was narrowed on purpose.** Unnarrowed it would have
written `Re-read ·` rows for `agents/warden.md#"## Report"` in
`seal/releases/0.9.2.md` and `0.18.1.md` and re-stamped five rows of
#867's fragment on the same coordinate, none of which this item read or
changed. That drift came with `origin/release/v0.21.0` and stands at this
branch's head as eight `DRIFTED` rows; it is named in the hand-back.

**#867's fragment had two claim rows on the rewritten units**, K23 and its
`Corrected ·` row on fenced sections. Both describe the `.md` arm, which this
work reaches through `bounding_rule` and did not otherwise change; their
hashes were re-stamped in place by hand, with a Notes trace, because an
in-place `--reverify` of that file re-stamps its `warden.md` rows too. Its
older `Re-read · H1` row stays as written; the survivor sweep names it and
`survivors.md` holds the grounds.

**`SKILL.md`'s Ruby and Lua sentence was the class, not one sentence.**
"Swift, Kotlin, Go, Ruby and Lua end no statement with a semicolon" stood in
the skill and in `generic_units`' comment; Ruby and Lua have no bounding rule
now, so both read Swift, Kotlin and Go.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SKILL.md`: "lands on the closing brace in a brace language, because the brace sits at the declaration's own indent" | §*Resolving a unit without a parser*'s suffix table and the two rules beneath it |
| `SKILL.md`'s Known-limits bullet "a language-aware rule for what closes a block is the per-language parser this deliberately does not have" | the Known-limits bullets on the walk's forms and on what an installer sees on upgrade |
| `SKILL.md`'s region row "a symbol elsewhere" | three rows: a brace language, a YAML key, any other file |
| Ruby and Lua in the semicolon sentence, in the skill and in `generic_units` | Swift, Kotlin and Go |
