# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 01f192cf |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the orchestrator that chose them is the one to fill this row |

## What this phase was asked

The module: the walker (K1, K2, alias resolution) with its synthetic cases
(S2–S4), the `ALLOWED` table and its liveness half (S5, S6), and the
entry-point half (S7), the repository case judging every tracked `.py`
except `tests/`. Every product site fixed, 15 under `hooks/` and 14 under
`.github/scripts/`, with D7 applied per hook read and S9's `read_mark` case.
`console.to_utf8()` in the three `hooks/git/` entry points, and S8 if M4
shows it red. The House rules bullet (S10). Measure M4 before planting S8,
and M1's product half. Every new case seen red first. Push at the end.

## What this phase found

**M1, product half: 29, equal to the census.** The walker, resolving
imports, named the same 29 product sites the framer's census counted: 15
builtin `open()` under `hooks/` in 11 files, 14 `subprocess.run(text=)` under
`.github/scripts/` in 5 files, none under `skills/*/scripts/`. Seen at
`1ecb019f` as the repository case's first red.

**M4: no.** The unfixed `hooks/git/pre-commit.py`, refusing the S5 commit
under `PYTHONIOENCODING=ascii PYTHONUTF8=0`, exits 1 with no traceback.
Python keeps `backslashreplace` on stderr whatever `PYTHONIOENCODING` says,
so the whole refusal arrived with each `—` and `…` spelled `—` /
`…`, including the waiver it tells the reader to type. D6's *a traceback
in place of the refusal* does not hold, and the frame's failure direction is
milder than it says: the commit was refused before and after, and only the
refusal's legibility changes. S8's own Then, *stderr carries the refusal*,
still fails against the unfixed hook, so S8 is planted in that form:
`tests/test_the_commit_gate_decides_at_the_commit.py#test_the_refusal_reaches_an_ascii_console_as_written`
asserts the refusal arrives exactly as `gate.refusal` builds it. It decodes
stderr as UTF-8 itself, because the module's `g` helper still decodes in the
locale's encoding until phase 2 names it.

**M2: the ticket's account holds.** `uvx ruff check --isolated --preview
--select PLW1514` (ruff 0.16.10) over a scratch file reported
`Path("x").read_text()`, `Path("x").write_text(s)` and `open("x")`, and
passed `p.read_text()` and `p.write_text(s)` on the lines above them. The
module docstring states it as measured.

**W1 answered.** The 9 empty-marker `open(path, "w").close()` sites and the
three writes (`session-lease.py#main`, `version-check.py#due`, and the marker
write) cannot raise on encoding. `version-check.py#running` catches
`ValueError`, `worktree-guard.py#dead_session_ids` and `#fresh_leases` catch
`Exception`, so their reads stay strict. Only
`commit-review-gate.py#read_mark` catches `OSError` alone and takes
`errors="replace"`. `hooks/gate.py#read_mark`, the same function in the newer
module, already read that way.

**Where the frame's K1 table and the signatures differ.** `codecs.open` takes
`encoding` third, not fourth, and `os.fdopen` puts the fd in `open`'s file
slot, so its positions are `open`'s rather than shifted. The walker follows
the signatures. A `*` positional splat counts as unproven beside K2's `**`.
None of these shapes is in the tree. `overview.md` carries each with its
grounds.

**A `.github/scripts/` site is named by replacing `text=True` with
`encoding="utf-8"`**, which puts `subprocess` in text mode by itself.

**The entry-point table's liveness half had nothing behind it** until
`01f192cf`: the first mutation plan showed deleting it would survive. It is
now `lacking_and_gone`, with a classification-of-nothing case and a decline
case.

**Every unit was mutated once, through `bin/mutation-check`, and every one
went red**: 41 in the walker and its tables (each K1 row and rule, each
subprocess flag, the `text=False` exemption, each always-unnamed call, each
K2 shape, both alias forms, the name-alone match, both non-openers, the
qualname, both liveness halves and both declines, the `ALLOWED` skip, the
repair sentence, the corpus, the first-statement and guard tests, an
empty-grounds row) and 7 in the product (`read_mark`'s `errors="replace"`
against S9; each git hook's call against S7, the pre-commit's against S8 as
well; one hook site and one `.github/scripts/` site against S1).

**One rider drifted.** `hooks/review-skill-gate.py#already_asked` carries a
`# RIDER:` stamped against its own hash, and naming the marker's encoding
moved it. The rider says the id is joined raw and an existing marker is never
overwritten, which the edit did not change, so it was re-stamped with
`rider_check.py --reverify --only hooks/review-skill-gate.py`.

**`tests/test_chain_hooks_hardening.py` requires `overview.md`** of a work
item that reached the ladder, so it was opened in this phase rather than at
the close.

**Run at the phase boundary, executed:** the 54 test modules that name an
edited product file or `console` (3431 passed, 79 skipped; the three failures
were the rider and the overview above, and the re-run of those modules with
every module reading `CONTRIBUTING.md` passed 1869, skipped 78); `uvx ruff
check` and `uvx ruff format --check` on every touched file. The suite as a
whole is `unverified`, answerer the sealer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
