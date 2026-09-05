# 1788613827-a-runs-report-carries-one-comparison-table — phase 3

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8887abc |
| Ran by | |

## What this phase was asked

Two documents, one sentence each, and neither restates the table phase 2
wrote.

`docs/review-handoff-protocol.md` §*After the run — the per-segment bars*
names the run-level table beside the three bars and says which judges what:
the bars judge a segment against its kind, the table judges a run against the
last run measured. It links `skills/verify/SKILL.md` §*Measure the segment,
and feed the flow log* rather than repeating the rows, and the sentence must
not read as a new destination for a reading — phase 2's note.

`skills/commit-pr-convention/SKILL.md` §*Pull request bodies* names the chain
section's shape for a work item routed through the review chain: the
comparison table first, then what the rounds found. PR #162 carries that
section in prose and PR #168 as a table; one shape from here. It points at
the table's definition rather than copying the nine rows.

Five constraints came with it. Every new case is seen red before it is
planted, by deleting or mutating the sentence it pins, with the file's own
bytes restored rather than a `git checkout`. Both sentences are text a person
reads and acts on, so each ships with a case. Edits go through the `Edit`
tool. `skills/writing-style/SKILL.md` governs the prose. And a case goes in
an existing module where one fits — `tests/test_the_handoff_before_round_one.py`
and `tests/test_the_pull_request_language_is_the_repositorys.py` named as the
candidates — with the choice explained either way.

`skills/commit-pr-convention/SKILL.md` is in `tests/test_docs_line_wrap.py`'s
`COVERED` at 88 display columns; the two files phase 2 touched are not, so the
habit does not carry over. The `1.2` that
`test_the_advisory_and_the_tying_paragraph_name_one_value` reads out of
`session_cost.py` stays exactly as it stands.

## What this phase found

**One case fits an existing module and the other fits neither, and the reason
is the module's subject rather than the file it reads.** The bars pin belongs
in `tests/test_the_handoff_before_round_one.py` — that module already owns
this document and already pins this very section
(`test_the_protocol_names_a_bar_per_segment_kind`), so a reader asking what
the bars judge finds both answers in one place. The pull request pin fits
neither candidate. `tests/test_the_pull_request_language_is_the_repositorys.py`
does hold `skills/commit-pr-convention/SKILL.md` as its `SKILL` constant, but
every one of its fifty-odd cases is about the language row, and its docstring
says so in its first line; `tests/test_a_segment_feeds_the_flow_log.py` pins
the table's **owner**, not its carriers. So the pull request pin is
`tests/test_the_chain_section_has_one_shape.py`, whose docstring carries that
reasoning.

**Nine of the eleven mutations exist because the first red proves less than it
looks.** Both new prose blocks were absent when the cases first ran, so every
assertion in them went red at once — which is the red phase 2 warned about: a
case red because its subject does not exist has not been seen red for its own
reason. Each assertion was then shown red against a paragraph that exists —
the pointer with the path removed, the pointer with the section name replaced,
the not-a-destination clause deleted, the shape sentence stripped of its
condition, and so on — one mutation per assertion.

**A refusal list of another file's strings rots silently, so it needs a case
of its own.** `test_the_section_points_at_the_tables_definition_rather_than_copying_it`
refuses three row labels taken verbatim from the table in
`skills/verify/SKILL.md`. If that table renames a row, the refusal keeps
passing while guarding a string nobody would paste — a green case over a rule
that has left the repository, which is the failure
`test_the_smiths_definition_mandates_mutating_every_unit_it_added` in the
handoff module was written for. `test_the_pinned_rows_are_the_owners_own`
asserts the three strings are still the owner's; mutation 11 renamed
`| Findings by severity |` in the owner's table and watched it go red.

**The bars section needed a scoped reader, for the reason the pointer section
already had one.** `docs/review-handoff-protocol.md` names
`session_cost.py` two sections above the bars, so a whole-file search for the
pointer would stay green with the paragraph gutted or moved out. Both new
modules read a section, heading to the next heading, rather than the file.

**For phase 4.** `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
is **red on this branch** and closes only when `overview.md` is written — it
reads `seal/specs/*/`, which no phase-3 file touches, so the red is the
missing memo and nothing else. The ledger fragment has four claims available
from this phase: the two sentences, the pointer that replaces a copy of the
rows, and the refusal list guarded by its owner. Nothing here names an issue
number inside a shipped skill; `#162` and `#168` appear in a test docstring
and in this record only.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds. Both sections keep every sentence they had, and the new paragraphs sit after the closing paragraph of one and after the opening paragraph of the other | none |
