# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 3c1be03a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#590. `fold_check.py#load`, `settle.py#load` and `round_record.py#load`
refuse a sibling script that is not beside them at exit 2, with a stderr
sentence naming the path and what the file is for. `settle.py`'s sentence
stops calling `hooks/optin.py` the fold record's reader. The `# RIDER:` on
`round_record.py#load` is discharged and removed, and the three sentences
calling it open are corrected. One parametrized case runs each of the four
scripts copied alone, `chain_check.py` included to pin the 2 it already
gives, and is seen red before the fix. `chain_check.py` is not edited.
Answer `questions.md` Q1 where the phase meets it.

## What this phase found

- **The frame holds, with one part built differently.** `plan.md` said to
  give `settle.py#load` the `purpose` parameter `fold_check.py#load` has.
  The tree answered against that: 22 call sites in `tests/` call
  `settle.load(path, name)` and `round_record.load(path, name)` with two
  arguments, and two cases monkeypatch `settle.load` with a two-argument
  lambda. So `settle.py` and `round_record.py` keep `load(path, name)` and
  look the purpose up in a module-level `PURPOSES` table: by path in
  `settle.py`, by file name in `round_record.py`, because two of its three
  paths are `chain_check.py`'s and exist only after that file has loaded.
  No call site can pass the wrong purpose that way. The first run of every
  module that reads the three scripts, 21 cases red with
  `TypeError: load() missing 1 required positional argument`, is what
  showed it.
- **The plan listed two of `settle.py`'s siblings and there are three.**
  `settle.py` also loads `evidence_check.py` (`CHECKER`, in the anchor
  guard). It has its own purpose now: what resolves a ledger row's anchor.
  `round_record.py` likewise loads `unverified_check.py` and `hooks/routing.py`
  in `where`, besides `chain_check.py` at import; all three have entries.
- **`chain_check.py`'s sentence names the path through the `OSError` text**
  (`[Errno 2] … '<path>'`) and its purpose as "the shared reader". The class
  case asserts that phrase for it, and the framer's measurement held: exit 2
  at `1880cf92`, untouched.
- **Q1's answer** is in `questions.md`: `round_record.py` with no arguments,
  `fold_check.py` and `settle.py` with `--root <empty dir>`, and
  `chain_check.py` with `--baseline HEAD --root <empty dir>`.
- **Seen red (§15).** The class case, with the code as it stood at
  `1880cf92`: 3 failed, 1 passed — `fold_check.py` and `settle.py` exit 1
  with a sentence, `round_record.py` exit 1 with a `FileNotFoundError`
  traceback, `chain_check.py` green. After the fix, 4 passed. Five mutations
  at `3c1be03a`, each restored from the bytes read before it, each red:
  `fold_check.py#load`'s exit back to 1 (1 red), `settle.py`'s
  `hooks/optin.py` purpose back to the fold record's (1), `settle.py#load`'s
  exit back to 1 (2), `round_record.py`'s `chain_check.py` purpose reworded
  (1), and `round_record.py#load`'s file check removed (1).
- **Verified by (executed, 2026-09-25):** every module in `tests/` that
  names one of the four edited scripts, 35 modules in one `bin/test` call.
  The first run was 1700 passed, 8 skipped, 21 failed on the signature
  above; after the fix, the four failing modules with the four the plan
  names and the new one, 9 modules, 544 passed. `ruff check` and
  `ruff format --check` clean on the seven changed files. S3's grep, for
  `rider on .round_record.py#load. is still waiting` and `own open rider`,
  found nothing outside this work item's own frame.
- **No caller reads exit 1 from the three.** Re-grepped `skills hooks
  .github bin` for `returncode == 1` and the like: the one hit is
  `evidence_check.py`'s own `exit_code`, unrelated.
- **Ledger.** `seal/releases/0.15.3.md` G1 anchors `fold_check.py#load` and
  the fold-check copied-alone case; both drifted, the claim still holds (it
  says the refusal names what the file is for, and not which code), so the
  row gained a `Re-read 2026-09-25` note and was re-stamped there. The new
  claim is M1 in this work item's fragment.
- **Writing the fragment turned `plan.md` into a record `evidence-check`
  reads**, because a work item with a fragment has not shipped and its
  records' names are resolved. The plan's ledger list spelled G1's anchor as
  the script's bare file name with its old hash, a path relative to nothing,
  which read as BROKEN. It now names the full path without a hash; the run exits 0 with
  11 names read in this work item.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `# RIDER:` above `skills/code-review/scripts/round_record.py#load` (Verified 2026-09-08 against `load@643ea575`) | Nowhere: it asked for this fix, which discharges it. `load`'s docstring says a rider stood there until #590 answered it |
| `round_record.py`'s docstring paragraph arguing a missing sibling is exit 1 | Its replacement in the same docstring, which says 2 and why |
