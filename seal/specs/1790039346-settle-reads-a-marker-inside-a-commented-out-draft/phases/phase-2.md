# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — phase 2

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `29368ff2` |
| Ran by | `specseal:smith` on Fable 5.1 — the agent definition names no model, the spawn passed no override, and the spawning session named its own model in the prompt |

## What this phase was asked

**The single-scan pin pins a single scan.**
`test_one_comment_scanner_serves_both_readers` keeps its two behaviour (NAME NOT IN TREE)
assertions and replaces the two agreement assertions with a module-level stub
of `comment_scan` that both readers answer from; its docstring says what it
now asks. Finding 4 of round 3. No shipped file changes.

Verified by A6 red by mutation — a private copy of the walk inlined into
`strip_comments` passes today's case and fails the new one — then
`tests/test_unverified_rows_close.py` green. Ledger row anchored on the case.

## What this phase found

**Round 3's finding 4 reproduced exactly, in both halves.** The mutation is a
private copy of `comment_scan`'s walk written into `strip_comments`'s body,
applied by a script that asserts its pattern matched once and restored from a
byte copy kept beside it, never from HEAD.

- Against the case as it stood at `3cdfd8ad`: `1 passed`, exit 0. The two
  agreement assertions compare `comment_scan`'s output with each reader's,
  and a correct private copy agrees.
- Against the rewritten case: `1 failed`, exit 1, on
  `uc.strip_comments(lines) == ["SENTINEL"]` — the reader with its own walk
  answered `['prose ', '', ' and prose again', '']` while the stub was in
  place.
- Restored, the module runs `109 passed` at exit 0; `ruff check` and
  `ruff format --check` over the file exit 0.

**The stub yields `(False, "SENTINEL")`, not `(True, …)` as round 3's
paste-ready form had it.** `opens_outside_a_comment` over one plain line
really answers `[True]`, so a `True` stub could not tell the stub's answer
from the real one for a single-line input. `False` can, and phase 3 needs
exactly that: its `live_lines` is asserted against the same stub over a
one-line input, where the real answer would be `True`.

**`monkeypatch.setattr` rather than the try/finally the report showed.** Same
act, and the fixture restores the module even when the assertion before it
fails, which a `finally` also does but a reader has to check.

**What phase 3 inherits.** The stub form above, and the module baseline this
closed at: `109 passed` in `tests/test_unverified_rows_close.py`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the two agreement assertions (`comment_scan`'s pairs against each reader's list) | none — they were the assertion the case's name over-promised, and the stub assertions replace what they were meant to pin |
