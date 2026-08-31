# spec-to-code map

> Maps spec clauses to the code coordinates that ground them, so the next
> session opens a coordinate instead of re-searching — locating the code is the
> expensive half, and this file exists so it is paid once. Written and checked
> by machines (`evidence-check`); committed so it follows worktrees and other
> machines.
>
> This is SpecSeal's ledger for SpecSeal. It opens with the tree's first
> commit as its baseline, which is the only commit every row here can measure
> from.

## Baseline

| Item | Value |
|---|---|
| Baseline commit | `9829412277fa11f81b61df7850183ae3fa9d8a05` (2026-08-31) — the fallback for rows with no baseline of their own; open with `git show 9829412:<path>` when in doubt |
| Coordinate notation | `<path>:<line>` from the repo root |
| Trust exceptions | none |

Each row's **Checked** column carries the date AND the commit SHA it was read
at, and drift for that row is measured from there. Rows without one fall back
to the baseline above. Re-verify row by row; bumping the header instead
re-dates every claim without re-reading one.

## Scope decisions

Judgments that don't follow from code or documents alone.

| Decision | Content | Grounds |
|---|---|---|
| The ledger opens at one commit | Every row below is stamped at this tree's first commit rather than left to the header alone | A row with no stamp of its own measures from the header, and a header nobody re-reads re-dates every claim at once. Stamping them all at the baseline costs nothing today and makes the first genuine re-verification visible |

## Routing declarations

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The Review and Destination axes are strict; a value outside the vocabulary makes the file not a declaration | `hooks/routing.py:45`, `hooks/routing.py:49` | Read, not run. `parse` returns `None` unless both answers are members | 2026-08-31 `9829412` | The Implementation axis is deliberately lenient at the same coordinate |

## Rider stamps

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| Every `# RIDER:` carries the date and SHA it was verified at, and the SHA is an ancestor of HEAD | `tests/test_a_rider_reaches_its_file.py:111` | Executed: the suite passes on this tree, and the eleven riders are stamped at the baseline commit | 2026-08-31 `9829412` | The stamps were re-cut for this tree; the commits they named before do not exist here |

## Edits that reach the commit gate

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The gate reads a heredoc body as commands, so a heredoc that only patches a file is judged by what its body says | `hooks/commit-review-gate.py:151` | **Executed**, twice independently: a body carrying a commit on its own line returns True under both `cat > f <<'EOF'` and `python3 - <<'PY'`, and False for a body carrying none | 2026-08-31 `f1cd65d` | Deliberate, per legacy #75: a commit hidden in a body used to walk straight past. The agent files now route file edits through the `Edit` tool, so no command line reaches the reader at all. Whether the reader should skip a body being written to a file is Q1 of `specs/1788184145-the-gate-stops-the-session-editing-its-tests/questions.md` |
| Only a segment whose command word is `git` with the `commit` subcommand is counted, so a commit sitting inside a string literal is not | `hooks/commit-review-gate.py:144-147`, assembled in `commit_invocations` at `hooks/commit-review-gate.py:262-286` | **Executed**, round 1's probe. Whole fixture files handed to `_hides_a_commit` are clean — `tests/test_gate_judges_the_repo_it_commits_to.py` and `tests/test_what_the_reader_understands.py` both — while `agents/smith.md` and `README.md` TRIP, each only on its own `[no-review]` waiver example | 2026-08-31 `f1cd65d` | This refutes both readings that preceded it. It is NOT "the fixtures are shell command strings, so the reader finds a commit in them", and it is NOT "the documents are what trip it": issue #34's eight-line PARTIAL patch of a fixture trips as well. A fragment is judged on its own quoting, not on the file it came from |
| A segment the reader cannot expand counts as a commit, so a body with no `git` in it at all can stop the session | `hooks/commit-review-gate.py:148-150`, resolved by `_eval_hides_a_commit` at `hooks/commit-review-gate.py:176-188`, against `EXPANDS` at `hooks/cmdline.py:678` | **Executed**, four bodies: `eval "$CMD"` TRIPS · `eval $(cat f)` TRIPS · `eval "echo hello"` clean (no expansion character) · `print('hello')` clean | 2026-08-31 `f1cd65d` | Fail-closed by design — the docstring says nothing can tell *reduces to a commit* from *reduces to something else* without running the shell. This is the branch a reader misses: searching a patch for a commit and finding none does not clear it. `tests/test_what_the_reader_understands.py:89` is an `eval` fixture, so a partial patch of that file is exactly the case |
| Prose added to a document can flip the gate's verdict on that whole document without containing a commit at all | `hooks/commit-review-gate.py:144-147` | **Executed** while fixing round 1. `agents/warden.md` is clean as a whole; adding one paragraph with a single apostrophe (`the fragment's own quoting`) made it TRIP, because the odd quote flipped the reader's state and put the `[no-review]` row in its probe table into command position. Removing the apostrophe restored `clean`. Round 2 confirmed the parity at the same coordinate: 0 → clean · 1 → TRIPS · 2 → clean · 3 → TRIPS | 2026-08-31 `f1cd65d` | **What is parity-sensitive is the apostrophes ADDED above the waiver row, not the file's absolute count** — measured after round 2's edit, `agents/warden.md` holds 11 apostrophes above that row, an odd number, and the file is still clean. Backticks and double quotes interact, so only the whole-file verdict answers this; a raw count does not. Measure above the waiver row, never below, because quote state flows forward. Pinned by `tests/test_edits_go_through_the_edit_tool.py::test_the_warden_file_does_not_itself_trip_the_commit_gate`. `agents/smith.md` is deliberately not pinned — it has tripped at its own waiver example since before this work |

## Evidence drift

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row reads DRIFTED when its range was touched since the row's own baseline | `skills/evidence-check/scripts/evidence_check.py:202` | Read, not run | 2026-08-31 `9829412` | Every row here shares the baseline, so nothing can drift until the second commit |
