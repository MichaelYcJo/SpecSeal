# 1791384156-config-rows-coordinates-and-headings-have-one-reader — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | bad39695 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 2: every command reads config through phase 1 and refuses
at exit 2 naming the row or the path — `evidence_check.py#frozen_from` (with
`vendored_config_rows` and a twin of the value rule, held equal by S4's
shape table), `correction_check.py#cutoff_at`, `fold_check.py#config_rows`
(its first-wins row reader removed), `broad_gate.py#broad_command`, `seal.py`
refusing two `Mode` rows naming both lines, `pact_check.py` unchanged;
`templates/config.md` and `skills/evidence-check/SKILL.md` say what a
doubled row and an unreadable file do. Verified by S1's command half, S2,
S3 and S4, one case per command, the unreadable fixtures a directory and a
non-UTF-8 file.

## What this phase found

**`seal.py` was already done.** Phase 1 built it, because `declared_mode`'s
new kind reached `seal mode` the moment it landed (`phases/phase-1.md`).
`test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe`, which this
phase's row asked to be re-read, still holds as written: the person's row
below a bare pipe is past the table's end, so the reader sees one row, and
its docstring's sentence *every reader takes the first* is about that one
row. Nothing to correct there.

**Q2, measured: the twin disagreed on three shapes.** Against 5623d728's
`vendored_config_rows`, a stray separator and a second header were stepped
past, so the rows of a second table were read as this one's, and `|| x |`
was a row with an empty item (probe over the case's own shape table,
deleted). The twin was corrected to the reader — the direction every other
twin's case takes — and the case now holds it equal over fourteen shapes and
four file states. `CONFIG_ROW_RE` stays as it was, because
`notify_may_be_always` judges a line by that shape on its own; the twin
reads `VENDORED_CONFIG_ROW_RE`, `hooks/config.py#CONFIG_ROW` spelled again.

**`correction-check` could not tell an unreadable config at a commit from
any other.** `git show <rev>:seal/config.md` prints a tree's listing at exit
0, and the call decoded with `errors="replace"`. `config_at` asks
`git cat-file -t` first and decodes the blob strictly, and its sentence names
the cause it checked: *a tree in git, not a file*, or the codec's words. A
mutation removing the not-a-blob arm survived until the case asserted the
cause, because `cat-file blob` refuses a tree too and the refusal arrived
anyway in other words.

**Two readers of the freeze that `plan.md` does not name.**
`settle.py#anchored_rows` and `hooks/evidence-advisor.py#main` read
`frozen_from` and took a refusal as *not frozen*. Spec §*What this delivers*
says the freeze arm never turns off because the file could not be read, so
both read a refusal as frozen: `settle` keeps answering a released row with a
`Corrected ·` row, and the advisor keeps naming the frozen repair and quotes
no refusal (it is a hook). Recorded in `overview.md` as inferred during
implementation.

**`evidence-check` without `--reverify` reads no config row**, so it is not
among the commands that refuse; S1 and S3 name `evidence-check` and mean the
arm that reads the freeze. Two older cases in
`tests/test_a_signer_records_a_pact_change.py` drove an unreadable config
into the pact record's `LEFT` path at exit 1; they now meet the freeze
read's refusal at exit 2 first, the ledger untouched either way, and their
docstrings say so.

**Direction and prompt budget.** Every change refuses more, in commands
only, at exit 2 with nothing judged; no hook gains a stop. Budget 0.

**Seen red (§15).** The new cases ran against 92bc47e3's parent's commands
with phase 1's `hooks/config.py` in place (`git stash` of the six scripts):
34 failed and 4 passed. The four that held at the base held for a stated
reason — `pact-check`'s two (unchanged, the shape is S3's floor), the
advisor's undecodable shape and `settle`'s doubled shape (the lenient and
last-wins reads landed on a value) — and each docstring says which.
`mutation-check`, every verdict `red` except one equivalent mutant in
`config_at` (an absent path read as `""` holds no row either): the twin's
stop rule and item pattern, its doubled arm and `lexists` arm,
`frozen_from`'s two refusals, the advisor's and `settle`'s `refused` arms,
`config_at`'s not-a-blob arm (after the case named the cause) and strict
decode, `cutoff_at`'s two refusals, `fold-check`'s unreadable and doubled
refusals and its `or None`, `broad_command`'s two refusals.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `fold_check.py#row_value` · NAME NOT IN TREE, the module's first-wins row reader | `hooks/config.py#value_of`, read in `fold_check.py#declared`; 0.15.3's F5 row is corrected in the fragment |
| `evidence_check.py#config_reader` · NAME NOT IN TREE, which loaded `config_rows` alone | `evidence_check.py#config_rule`, which loads the reader's three units or the twins |
| `broad_gate.py`'s own opening of `config.md` | `hooks/config.py#config_text`; `broad_gate.py#config_text` is its text half |
