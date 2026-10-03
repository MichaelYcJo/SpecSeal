# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 79eb2872 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 2: 🟡 19's pattern; ⬜ 23's refusal sentence naming both
remedies; the grammar statement in `docs/the-pact.md` §*The pact anchor*; one
display helper for every path `pact-check` prints, the `UNREADABLE` line among
them. Verified by round 3's four missing-slash ids red against `2b1dcb1f`, the
`ntpath` case red with the old `{their_home}/{CONFIG_FILE}` restored,
`fold-check` exit 0 and `test_pact_check.py` green. The spawn added: every
printed path through this phase's helper, every test comparing a printed path
normalising `os.sep`, and a case building paths through `ntpath`; answer Q16.

## What this phase found

**The frame holds.** Round 3's paste-ready pattern went in as written, but its
curly quotes are spelled by code point (`OPEN_QUOTE`, `CLOSE_QUOTE`): ruff's
RUF001 refuses the literal characters, and the edit tool's formatter turned a
`“` escape inside a raw string back into the character.

**Q16: a new function, `pact_check.py#shown`, not `display_name`.**
`display_name` keeps the caller's separators by design, and `load`'s own
refusal is printed before `evidence_check.py` is loaded. `shown` compares
whole segments literally, the way `display_name` does, and prints a path
relative to its repository inside one, `~/`-relative under HOME_DIR, and with
`/` for every separator otherwise.

**The class, enumerated from the source** (every `say(`, `found(` and returned
reason in `pact_check.py` at `ddbd24b9`): `load`'s module path; the
not-a-repository sentence's root; the no-pact and no-origin sentences' repo;
the pact's `UNREADABLE`; the map refusal; `checkout`'s two map sentences and
its sibling list; the `ONE-SIDED` checkout; the config `UNREADABLE` (the one
the note named); every anchor file's place; the `READ` line's checkout. The
`seal/config.md` and `seal/pact.md` labels are literals and already POSIX.
`test_no_line_formats_a_path_without_the_helper` holds the class by reading
the file's f-strings, so a path variable formatted bare is a red case.

**The pact's own `UNREADABLE` changed wording, not only form**: it prints
`seal/pact.md`, relative to the pact's repository, where it printed the
absolute path. The `READ`, `ONE-SIDED` and map sentences print absolute paths
outside `~` as before, now with `/`.

**Mutation: 13 breaks, each red** — the restored `UNREADABLE` line, each
missing-slash alternative and its optional mark and space, the second remedy,
each of the helper's two anchors, its separator respelling, its prefix
comparison, and its drive-and-root check, which survived the first pass and
was killed by two cases added for it (the same segments on another drive, and
a relative path).

**Ledger**: the rows this phase drifts in #735's fragment (P9 and the pact
modules' cases) and the `CONTRIBUTING.md` rows phase 1's re-wrap drifted again
are re-read in one pass at the build's end, with every row the later phases
drift, rather than re-stamped once per phase.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
