# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 137bf447 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

The readers widen: `evidence_check.py#default_patterns`,
`hooks/evidence-advisor.py#failing_rows`, `hooks/ledger-migrate.py#HOME_GLOBS`,
`correction_check.py` (`RELEASES`, `ledger_listing`, the docstring's *What it
reads* and the cross-path limit) and `settle.py#coordinates` each read
`seal/releases/*.md`; each seen red first with a fixture whose rows sit in a
release file; `skills/evidence-check/SKILL.md`'s `--ledger` row and
`skills/settle/SKILL.md` §4 name the third address; the `default_patterns`
rows re-read.

## What this phase found

**The frame's list of readers held.** `grep -rn 'ledger", "\*.md"\|ledger/\*\.md'`
over `hooks/`, `skills/`, `.github/` and `tests/` at `9f5902e5` found the five
readers the spec names and no sixth outside `hooks/root-migrate.py#LEDGER_GLOBS`,
which the spec leaves as it is.

**Nine cases, each red before the reader widened, executed at `9f5902e5`
with the test edits applied and the readers untouched** — `10 failed, 214
passed` over the six modules. The tenth red was
`test_the_bound_covers_every_candidate_marker_site_the_corpus_carries`,
red on `cc.RELEASES` not existing yet, because `ledger_corpus` reads it. The
nine:

| Case | Reader it pins | Red on |
|---|---|---|
| `test_the_defaults_render_the_names_they_have_always_rendered` (re-pointed) | `default_patterns` | the list had three names |
| `test_a_row_in_a_release_file_is_read_by_the_default_run` | `default_patterns` via `main` | `1 ok` where two rows stood |
| `test_a_narrowed_run_names_the_release_file_it_did_not_read` | `skipped_by_narrowing` | the notice named nothing |
| `test_reverify_re_stamps_a_drifted_row_in_a_release_file` | `reverify` | the file kept `00000000` |
| `test_the_evidence_advisor_reports_a_broken_row_from_the_local_ledger[releases/0.4.0.md]` | `failing_rows` | no BROKEN line |
| `test_an_old_format_row_in_a_release_file_is_migrated_too` | `HOME_GLOBS` via `ledgers` | `1 row` migrated, the file untouched |
| `test_a_marker_lost_from_a_release_file_is_reported` | `ledger_listing` | exit 0, nothing named |
| `test_a_release_file_is_read_as_well_as_the_gathered_ledger` | `coordinates` | beta stayed `tests only` |
| `test_a_row_in_a_release_file_is_read_by_the_guard` | `anchored_rows`, asserted once | the directory was removed |

**`anchored_rows` needed no edit of its own** beyond its docstring's
enumeration: it loads the checker and calls `default_patterns`, which is the
spec's S4 as written. `coordinates` needed the loop: it opened `LEDGER` by
name.

**Seven units drifted, nine rows re-read.** `evidence-check .` after the edits
reported `7 drifted`; the rows citing them are `seal/ledger.md` lines 133,
435, 436, 469, 940, 2386, 2435, 2446 and 2586 (line numbers at `137bf447`,
for opening). Each got a dated `Re-read 2026-09-24 (#547)` note before
`--reverify .` re-stamped them (`10 rows re-verified` — row 435 cites two
of the drifted units). `--strict .` exit 0 after.

**Line numbers the spec cites for `seal/ledger.md` are off by two on this
base.** The spec's line 2521 (the self-anchored row) and the ticket's
2658/2661 and 2703/2706 were read at `9f846733`; C's tip `9f5902e5`
re-stamped rows above them, and here the self-anchored row is at 2519 and
the `1790173106` markers at 2656/2659. Phase 3 anchors on content, so
nothing is built on the numbers.

**Ruff.** `RUF005` on the first spelling of `coordinates`' list
(concatenation); rewritten as unpacking. `ruff format` reflowed two test
assertions.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
