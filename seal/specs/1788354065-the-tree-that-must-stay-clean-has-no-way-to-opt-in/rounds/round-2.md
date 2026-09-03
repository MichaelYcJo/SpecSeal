# 1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in — review round 2

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/rounds/round-2.md —
the verifying round the run ends on: it opened round 1's fix diff
(f049003..50a6eda) and nothing needing a fix, so it does not consume the
cap. Written by the review orchestrator after the report was verified and
the broad gate ran. -->

| Field | Value |
|---|---|
| Target SHA | ab66282 (the fix diff is f049003..50a6eda; ab66282 is round-1's record edit only) |
| PR | #95 |
| Broad gate | ab66282 vs origin/release/v0.5.0 — `pytest tests/ -n auto` 1369 passed · 1 skipped, `ruff check .` clean, `ruff format --check .` 80 files formatted, `evidence_check.py --strict .` 299 ok · 0 drifted · 0 broken, `unverified_check.py --baseline` exit 0 (14 overviews · 32 open · 15 closed · 0 unreadable). The delta after the run is this record, round-1's `Fixes checked by` cell, one unit name in `evidence-todo.md`, and `pr.ko.md` — docs-only, the non-invalidating class |
| Fixes checked by | round-3 |
| Contract changes | none — the fix for 🔴 M changed one test assertion; no hook code, no printed text |
| New units | none — the fix for 🔴 M added no unit |
| Needs a fix | yes — 🔴 M, opened by PR #95's windows CI leg after the reviewer answered `no`: a second gate-prompt assertion still spelled the path with slashes |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1-1 | round-1 🔴 1 (the gate's hint raised before judging; an allow) | `hooks/commit-review-gate.py#declaration_hint`, `#judge` | answered — the fix is 1f27eac's, this round reproduced its closure | executed: the planted test red against f049003's hook (`ValueError` at `judge`), green now; six hint shapes read (no home → the shared literal; home under top → `.git/seal/specs/…`; a linked worktree → `../<main>/.git/seal/specs/…`, with spaces too; shared → `seal/specs/…`; `top=""` → literal); nothing but `ValueError` can raise — `home=""` returns the literal before `os.path.join` |
| 🔴 1-2 | round-1 🔴 2 (`dirty` raised at session start) | `hooks/ledger-migrate.py#dirty` | answered — 2078984's fix reproduced | executed: red against f049003, green now; the mixed run (the root's path raising, an uncommitted `docs/**/_evidence.md`) is refused with "not touching work in progress" and the ledger untouched — handled, untested in the suite (🟢 4) |
| 🟡 1-3 | round-1 🟡 3 (the switch commands and the cwd) | READMEs, `templates/seal-README.md`, `seal/README.md` | answered — f53d615's fix reproduced | executed: the subdirectory test red against f049003's READMEs (`A  src/seal/ledger/f.md`), green now; the block run by hand from `src/` both ways (`A  seal/ledger/f.md` → `[]`, the ledger back under `.git/seal/`); `cmp` says the template and the root README are identical |
| 🟡 1-4 | round-1 🟡 4 (where the version is read) | `skills/implement/SKILL.md` §Bootstrap | answered — f53d615's fix reproduced | executed: with `CLAUDE_PLUGIN_ROOT` set → `v0.4.0`; unset → `KeyError` traceback (loud, nothing left as `v<version>`) — 🟡 A below |
| 🟡 1-5 | round-1 🟡 5 (the local-mode ending) | `hooks/ledger-migrate.py#main` | answered — 2078984's fix reproduced | executed, including from a linked worktree of a local root, which takes the local ending — right, that root has no history either; a shared repository's worktree finds `<worktree>/seal` first and keeps the diff ending |
| 🟢 1-6 | round-1 🟢 6 (one git process per commit) | `hooks/commit-review-gate.py#judge` | answered | executed: git processes counted through a `subprocess.run` wrapper — 10 → 9 when the arm is silent, the one fewer being `rev-parse --git-common-dir` |
| 🟢 1-7, 🟢 1-9, 🟢 1-10 | the three sentences | `hooks/optin.py`, the READMEs, `chain_check.py#declared_for_this_branch` | answered | read |
| ❓ 1-8 | round-1 ❓ 8 (the removed S12 row) | `seal/ledger.md` §1788331011, `seal/ledger/1788354065-…md` | answered — nothing lost | executed: `--strict .` 299 ok; the fragment row carries the five surviving anchors; the removed row's first Notes sentence lives in the fragment's phase-2 S12 row and its "each test file re-run" label went honestly from Executed to Read. The rule question itself stays the owner's (Deferred) |
| 🟢 1-P5 | tests-todo row 5, green on first run | `tests/test_the_root_migrates_itself.py#test_a_stamped_local_mode_repository_leaves_an_old_layout_branch_alone` | discriminates | executed: `has_root` reverted to the release branch's inline form → the test fails at `assert stamped(hook, d)` |
| 🟢 fix-surface | round-1's `Contract changes` and `New units` | `rounds/round-1.md` | truthful | callers grepped over `hooks tests skills templates .github`: `judge` and `declaration_hint` from the gate only, `dirty` from its `main` and one existing test (signature unchanged), `declared_for_this_branch` from `chain_check.py#main` only; `switch_block` bounds its section and asserts the fence; every fixture under `tmp_path` |
| 🔴 M | `tests/test_routing_is_recorded.py::test_the_second_prompt_names_it_too` asserted the literal `seal/specs/<work-item-id>/routing.md` in the gate's reason; since phase 1 the hint is joined with `os.path.join`, so the windows leg of PR #95 (run 33643327406) read `seal\specs\…` and failed — phase 1 had fixed the first prompt's assertion in the same file and missed this one | `tests/test_routing_is_recorded.py#test_the_second_prompt_names_it_too` | fixed — 46c658d: the assertion joins the path the way the platform spells it (the file's first-prompt shape); every other `/`-literal in `tests/` was grepped and is document text, a negative assertion, or a ledger coordinate; the anchored row re-verified | opened by CI, not by the reviewer; `ntpath.join` reproduces the mismatch and `posixpath` the match |
| 🟡 A | with `CLAUDE_PLUGIN_ROOT` unset the bootstrap's one-liner prints a `KeyError` and the skill does not say what to do next — a session might guess a version | `skills/implement/SKILL.md` §Bootstrap | answered with grounds — no fix: `skills/update/SKILL.md` already relies on the same variable in a Bash command, so the precedent stands; the failure is loud and leaves nothing as `v<version>`; a sentence forbidding a guess is one line for the next time that section is opened (Deferred) | executed |
| 🟢 B | `rounds/evidence-todo.md` still named `chain_check.py#committed_declarations`, a unit that does not exist, after round-1's record said both files were corrected | `rounds/evidence-todo.md` | answered — the unit name in `evidence-todo.md`, the orchestrator's own record file, is corrected in this record's commit; no code, nothing for a round to open | read |
| 🟢 C | `COMMON`/`TOP` are defined after their first use in the test module | `tests/test_first_setup_asks_once.py` | record only — cosmetic, runtime-correct | read |
| 🟢 D | the mixed dirty shape (a raising root path plus an uncommitted `_evidence.md`) is handled but untested | `tests/test_local_mode_resolves_under_the_git_dir.py` | record only — optional plant, named in Deferred | executed by probe |

## Executed probes

| What was run | Result |
|---|---|
| the eight planted tests + one README test + five probes at HEAD | 15 passed |
| the same eight against f049003's tree (`git archive`) with HEAD's conftest and tests | 8 failed / 2 passed (the two: the shared-ending half, and the P5 pin whose fix was phase 1's) |
| the two 🔴 failures' cause (`--tb=short`) | `ValueError` at `judge`'s `relpath`; `ValueError` in `dirty`'s generator |
| `has_root` reverted to the release branch's form, P5 pin | fails at `assert stamped(hook, d)` |
| `declaration_hint` on six shapes and `top=""` | as recorded above |
| git processes per commit (worktree, local root, declaration present / absent) | HEAD 10 / 9; f049003 10 / 10 |
| the mixed dirty probe | refused; the ledger untouched |
| the switch block by hand from `src/`, both ways | `['A  seal/ledger/f.md']` → `[]` |
| the migration ending from a linked worktree | "this root has no git history …" |
| the version one-liner, variable set / unset | `v0.4.0` / `KeyError` |
| `evidence_check.py --strict .`; `cmp` of the two READMEs; `fold_ledger.py --check` | 299 ok · 0 drifted · 0 broken; identical; exit 1 naming only the unfolded fragment, 0 open evidence-todo rows |
| the broad gate at ab66282 (orchestrator) | see the field above |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/commit-review-gate.py#declaration_hint` | the one unit the fix created; its six shapes are the map for any later change to the hint |
| round-1 | `hooks/ledger-migrate.py#dirty`, `#main` | the local-mode ending's key ("is `home` `<root>/seal`") and the skipped-path rule |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 1-8 whether CLAUDE.md's REMOVED rule should say what a multi-anchor row does | the PR body | the repository owner |
| 🟡 A one sentence forbidding a guessed version when `CLAUDE_PLUGIN_ROOT` is unset | this record; the next change that opens §Bootstrap | nobody — recorded |
| 🟢 D the mixed dirty shape as a test | this record only | nobody — recorded |
| S11 Windows two-drive on a real machine; Q9 the template on a runner; `evidence-check .` by CLI from a linked worktree | the PR body's Not verified; CI's windows leg for the rest of S11 | CI / the owner |
