# 1790260566-a-row-inside-a-fence-reads-as-live — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ed84a4cd |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The ledger walks skip a closed fence (#444). `evidence_check.py` loads the
reader and uses phase 1's rule in `check_ledger`/`check_text` over a file,
`old_format_rows`, `migrate` and `reverify`. A closed fence's lines are not
read, an unclosed fence's lines are, and character offsets are kept for the
two writers. `skills/evidence-check/SKILL.md` states the ledger rule.
Correct `docs/the-evidence-ledger.md`'s "because the checker reads those
too" and `settle.py#anchored_rows`'s future-tense #444 sentence, keeping the
behaviour. Delete the `#444` row from `seal/follow-up.md` after one probe
each of `round_record.py` and `chain_check.py`. Cases S1 and S2 seen red, S3
pinning the direction, `test_a_fenced_anchor_still_keeps_the_directory`
still green, and Q3's count recorded.

## What this phase found

**The frame does not hold in one place: the checker is also vendored.**
`skills/evidence-ci/SKILL.md` has an adopter copy `evidence_check.py` alone
into a repository's `tools/`, and `tests/test_evidence_check.py#vendored_copy`
builds that shape. `unverified_check.py` is not beside such a copy, so the
load `spec.md` §*Data & interfaces* prescribes would stop every CI run that
vendored the checker. `plan.md` §*Operational impact* named the installed
plugin's layout only. Built instead: `fence_rule()` loads the shared reader
where the reader and this skill's `SKILL.md` are beside the script, the test
`seal_home` already uses. It asks a vendored pair of the same two functions
where they are not. An agreement case holds the pair in step with the shared
rule over phase 1's shape table. `questions.md` Q6 records the default and
the two alternatives. `overview.md` records the divergence.

**The four walks share one blanking.** `quoted_lines(lines)` walks the
shared delimiter rule and returns the lines of every fence that closes.
`unquoted(text)` blanks those lines to spaces and keeps every character
offset. `check_ledger` hands `check_text` the unquoted text. `reverify`
finds its matches in the unquoted text and splices from the original,
because the offsets are equal. `migrate` skips a quoted line by index.
`old_format_rows` unquotes its own input, because
`hooks/ledger-migrate.py` asks it whether to migrate at all. A quoted old
coordinate there would offer a migration that `migrate` then leaves alone,
at every session start. The class was the four walks the frame named plus
that one caller. `hooks/evidence-advisor.py` goes through `check_ledger`,
and the records arm reads a line at a time through `check_text` and is
phase 4's.

**Cases seen red (executed).** `c52e8350`'s checker was swapped in from a
saved copy and the cases run. Then the file was restored from the saved
copy of this tree and compared byte for byte:

| Case | Against `c52e8350` |
|---|---|
| S1 `test_a_fenced_example_row_is_not_checked` | red: `BROKEN nosuchfile.py#nothing file not found`, exit 2 |
| S2 `test_the_writers_leave_a_fenced_example_byte_for_byte` | red: `--reverify` rewrote the fenced `00000000` |
| S3 `test_an_unclosed_fence_still_holds_its_rows` | green on both, as a direction pin should be |
| `test_a_vendored_copy_skips_a_fenced_example_too` | red: the vendored copy reported the example BROKEN |
| `test_the_vendored_fence_rule_agrees_with_the_shared_one` | red with the vendored opener's info-string clause removed, then restored |

S2 stops at its first assertion, so `--migrate`'s half was shown by a
separate probe on a scratch ledger. `c52e8350`'s `--migrate` rewrote the
fenced old coordinate to an anchor, and this tree's left it byte for byte.
The probe was deleted.

**The two readers the follow-up row left unmeasured (executed, probes
deleted).** `chain_check.py#field` over `table_rows(readable(...))` returns
None for a `| Needs a fix | yes |` row that stands only inside a closed
fence, and `yes` when the fence is removed. `round_record.py#table_body` over
a `## Verdicts` section holding a fenced example verdict table above the
real one returns the real row alone. Both read through `readable`, which
carries phase 1's rule. The `#444` row left `seal/follow-up.md`.

**Q3 (executed).** No anchor in `seal/ledger.md` or the 30 release files sits
inside a closed fence, because none of those files has a fence line. A grep
for a triple backtick or tilde anywhere in them finds one file,
`seal/releases/0.4.0.md`, inside a table cell. The frame's count of 11
matches the word `fence` in 19 files, and a fence line in 0.
`evidence-check --strict .` counts 2,067 anchors before the reader change
and 2,067 after it, so #444 moves no verdict in this repository's ledger.

**The ledger moved, and each row was re-read (executed).** The code edit
drifted 10 anchors in 9 rows plus this work item's own `fence_opener`:
`seal/releases/0.4.0.md` rows 22, 29, 30, 32, 46, 59 and 67,
`seal/releases/0.8.3.md` row 13, `seal/releases/0.14.0.md` G3 and
`seal/releases/0.15.1.md` S1. Each got a dated note, and `--reverify`
re-stamped it. **One claim was false after the edit and was corrected in
place:** 0.4.0 row 30, "A 0.1.0 row is loud, never invisible", now reads "A
0.1.0 row outside a fenced block that closes is loud", with a `Corrected
2026-09-25` note. G3's "every ledger row the checker reads … inside a fence
included" still holds, because the guard now reads a superset, and its note
says so. Then the phase's three rows went into the fragment. The first draft
of P2-1 quoted a `path:line` coordinate and was itself reported OLD-FORMAT,
which is the rule still working on a real row. It was reworded.
Final: `2081 ok · 0 drifted · 0 broken · 0 old-format`, exit 0. The 14 new
anchors are this work item's.

**A rider moved too.** `evidence_check.py#reverify` carries a `# RIDER:`
about the `Checked` column. The rider was read, and this phase does not
answer it. `rider_check.py --reverify --only
skills/evidence-check/scripts/evidence_check.py` re-stamped it, which moved
the unit's hash again, so the three rows anchored on `reverify` were
re-stamped once more.

**Two more sentences said the checker reads a fenced row**, found by grep
for the claim rather than for the coordinate the frame named.
`skills/settle/SKILL.md` §*4. Retire what the policy absorbed* said "because the checker
reports a fenced anchor broken too".
`tests/test_settle_reads_before_it_removes.py#test_a_fenced_anchor_still_keeps_the_directory`'s
docstring said "evidence-check reads an anchor inside a fence as a coordinate
like any other". Both now give the direction ground, and the case's
assertions are unchanged. `test_the_documents_say_the_retirement_keeps_an_anchored_directory`
pinned the policy's old sentence and now pins the new one.

**Modules run (executed).** Every module that reads a file this phase
edited. The list is phase 1's 57, plus every module naming
`the-evidence-ledger`, `evidence_check.py`, `evidence-check/SKILL`,
`follow-up` or `docs`, for 79 in all. The first run: 3 failed and 3276
passed. The failures were the rider stamp (`test_a_rider_reaches_its_file`,
two cases) and the pinned policy sentence. After the repairs, a second run
found one line of `skills/settle/SKILL.md` over the wrap limit. After that
repair, `tests/test_docs_line_wrap.py` and
`tests/test_settle_reads_before_it_removes.py` gave 128 passed, and
`tests/test_a_rider_reaches_its_file.py` 29 passed. `uvx ruff check` and
`format --check` over the edited Python files are clean.

**What `CONTRIBUTING.md` §*What a change to a gate must carry* asks:**

- **The case seen red:** the table above.
- **Failure direction:** the checker reads fewer lines, which allows more.
  That is taken only for a fence that closes, which is certainly a
  quotation. An unclosed fence is read, and S3 pins it. What it costs is
  written in `skills/evidence-check/SKILL.md` and the changelog: a real claim
  written inside a closed fence is no longer checked, and nothing says so.
  This repository has no such row (Q3).
- **Prompt budget:** 0.
- **Platform note:** pure text processing. `unquoted` keeps `\r\n` endings as
  they are and blanks only other characters, so CRLF offsets hold. Run on
  macOS only, and CI runs the Linux leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/follow-up.md`'s `#444` row | this phase: the checker skips a closed fence, and the two readers it left unmeasured were probed |
