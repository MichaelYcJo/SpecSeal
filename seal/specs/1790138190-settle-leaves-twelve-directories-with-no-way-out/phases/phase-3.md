# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b0db71e |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The rule arm in `settle`. The report's own heading for a released spec-less
directory; `--retire` removes it with no marker; a directory with an open
memo row or an open `evidence-todo.md` row kept and named. For every
directory it would retire, by either arm, the report lists the open
`## Not verified` rows, the paths outside `seal/specs/` citing into it (a
`specs/<id>…/` path, never a marker or a bare id), and the `tests/` files
naming `seal/specs`. The predicate lands in `unverified_check.py` beside
`folded_items`, asked of the working tree here. `skills/settle/SKILL.md` §1
and §4, `docs/the-evidence-ledger.md`'s *kept by name* rule, and both
READMEs' `settle` row move in this commit. Verified by A4, A5 as cases seen
red first; a case that a guard-held rule-arm directory stays; `./bin/settle`
on this branch listing the ten released spec-less directories with
`1788177600` and `1788395377` named as kept and their four rows printed; the
settle module, `tests/test_one_word_one_meaning.py`,
`tests/test_docs_line_wrap.py`.

## What this phase found

**Nine cases, six seen red first** — executed at `26de1ec` with the cases
added and neither script touched: `6 failed, 75 passed`. The three that
passed there are controls whose property holds with no rule arm at all
(nothing retired a spec-less directory yet): *an open evidence-todo row keeps
a spec-less directory*, *an unreleased spec-less directory is not a
candidate*, *the predicate is what settle asks*. Each earned its red from a
mutation below. The document pin
`test_the_documents_say_a_spec_less_directory_is_retired_by_the_rule` was
seen red with the four document edits stashed (`1 failed`), then green.

**Fifteen mutations, and three survived the first pass** — executed after
committing `2453405`. All three were in the predicate: `settle` checks
`spec.md` and the evidence-todo guard before the predicate decides, and only
ever asks it of a present directory, so through `settle` the predicate's own
spec condition, its absent-directory answer and its evidence-todo read were
never observed. The CI readers of phase 4 ask it of a merge-base where
neither check has run, so a hole there would have been live.
`test_the_predicate_asks_every_condition_itself`, parametrised over the
working tree and `HEAD`, closes it (`b0db71e`): the three re-run red. The
other twelve were red on the first pass. `git status` clean after each run.

**`./bin/settle` on this branch, exit 0** (executed, read directly):
`no spec.md: 8 to retire by the rule, 2 kept by it`. Under *retired by the
rule*: `1788217118`, `1788220055`, `1788276387`, `1788425222`, `1788824000`,
`1788938400`, `1789024700`, `1789053786`. Under *kept by the rule*:
`1788177600` with *whether the hooks fire on Windows from this tree* and *the
conformance evals*; `1788395377` with *The guard refusing a real release
with a real open row …* and *The broad gate* — four rows, as G1 said.
`ungrouped` is down to `1788184145` and `1790119502`, the two that wrote a
spec. The takes listing says *nothing open, and nothing outside seal/specs/
cites into it* for all eight, and 45 `tests/` files under the readers
heading — G8's `grep -rln` count.

**The citation scan was checked against an independent read** (executed):
`git grep -c "specs/<id>" -- ':!seal/specs'` for each of the eight finds
only two hits, both `CHANGELOG.md` provenance markers
(`<!-- specs/1788824000-… -->`, `<!-- specs/1788276387-… -->`), which the
scan rightly does not count. An abbreviated path (`specs/1788184145-…/`) is
matched by prefix, which is how this repository's prose spells a long id.

**The evidence-todo rule moved beside the predicate.** The predicate reads
`evidence-todo.md`, and `settle.py#open_rows` held the rule; a second copy in
`unverified_check.py` is the duplicated-reader shape the plan exists to
avoid. So the rule is `unverified_check.py#todo_open_rows` and
`settle.py#open_rows` delegates to it. `.github/scripts/fold_ledger.py`
keeps its own copy for the reason `settle.py#open_rows`'s docstring already
gave: release automation is not a shipped script.

**The predicate returns a boolean, and a second function names the rows.**
`retired_by_rule(root, ref, directory)` is the one question every reader
asks; `open_record_rows(root, ref, directory)` is what `settle` prints for a
kept directory and for the takes listing. An overview whose section cannot
be read is one row saying so, never zero rows.

**Slice** (executed): the settle module, `tests/test_one_word_one_meaning.py`,
`tests/test_docs_line_wrap.py`, `tests/test_unverified_rows_close.py` —
`260 passed`; `ruff check` and `ruff format --check` clean on the three
changed `.py` files.

**Rows**: `seal/ledger.md` S4 (`1790027178`) **corrected** — its clause said
the removal happens *only where `docs/` records its fold*, which the rule arm
made false; the clause names the second condition and a dated `Corrected`
note says why. R1 and R2 on `settle.py#main` re-read: only the `--retire`
help text changed. `--reverify` moved `retire`, `open_rows` and `main` (×2);
`evidence-check --strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-evidence-ledger.md`'s *A released work item that wrote no `spec.md` states no rule, and it is kept by name* — overturned by D3 | the same paragraph: *it is retired by that rule, with no marker*, narrowed by the open-row condition and marked as a judgment the owner may overturn |
| `skills/settle/SKILL.md` §1's *three lists beside them* and its *Those are yours to place, or to leave* for a spec-less item | §1's *A released work item with no `spec.md` is not yours to place* |
| `skills/settle/SKILL.md` §4's *removes the directory of every released work item whose fold is recorded, and nothing else* | the same sentence, naming the rule arm |
| the evidence-todo rule's body in `settle.py#open_rows` | `unverified_check.py#todo_open_rows` (moved, not changed) |
