# Implementation Plan: the fixes are what open the next round

<!-- specs/1788272986-the-fixes-are-what-open-the-next-round/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Approval

**Approval was given in advance**, by the repository owner: issue #57's
"Already decided" section records the routing, and this overnight run was
pre-authorized to the pull request (recorded in `questions.md` as its first
entry). The session does not stop for a go; anything that would otherwise be
raised becomes a `questions.md` row at the coordinate it is about.

This work sits on the top rung twice over — it changes a CI check's verdict
(`chain_check.py` gains refusals) and it changes the instructions two agents
read and act on — so `spec.md` and this file are owed whether or not anyone
is waiting to approve them.

## Summary

Ten regressions on `1788229400-…` each traced to the fix that opened it, and
the largest class — four of ten — was a fix that changed a unit's contract
while not every place that contract reaches was revisited. The diff names the
changed signature; `grep` names the reach; a person reading a diff missed all
four. So the reach becomes a row a machine refuses to lose: `round-N.md`
gains `Contract changes` and `New units`, `chain_check.py` refuses a new
record without them and a unit listed without its reach, and the verifying
round is told that what `New units` names is a finding surface. Around that
sit the four review-skill rules the same measurement bought: a security row
in the axes table, the OS-boundary precondition clause on paste-ready fixes,
and three written rules about verdicts that close too early.

## Technical context

- `skills/code-review/scripts/chain_check.py` — `checked_by` is the model:
  read on every record, `(errors, notices)` back to `main`, grandfathering by
  `item_began(rel)` against a cutoff constant. The new `fix_surface` follows
  it exactly, with its own `SURFACE_FROM = 1788272986`.
- `chain_check.py` `field`, `table_rows`, `reader.visible`, `EMPHASIS`,
  `SEPARATORS` — the row is read through the shared reader like every other
  row, and `none` is matched as a prefix the way `verdict_of` matches its
  vocabulary, so `none — <reason>` is an answer.
- `templates/sdd-round.md` — the field table a session copies; the two rows
  go in as placeholders beside `Fixes checked by`, with the reach-back rule
  (filled when the fixes land) in the comment.
- `docs/review-handoff-protocol.md` — the field table and a new subsection;
  the draft moves to 0.7. `docs/review-chain-spec.md` — a refusal subsection
  beside the `Fixes checked by` one, since that document is the authority for
  what the pull-request check refuses.
- `skills/code-review/SKILL.md` — the axes table, the paste-ready rule, the
  verifying-round section, the record-contents row, and the new subsections.
  `agents/warden.md` — the verifying-round bullet, which currently reads
  *answers rather than new findings* and would send the reviewer past the
  new-unit surface.
- `tests/test_the_last_rounds_fixes_are_checked.py` — its `record()` builds
  records for a work item begun at `1799000000`, which is after the new
  cutoff, so it gains the two rows with `none`; everything else it pins is
  untouched. `tests/test_chain_check_at_the_pull_request.py` builds only
  grandfathered items and needs nothing.
- `specs/*/rounds/round-*.md` — every existing record predates
  `SURFACE_FROM` (the newest work item with records is `1788229400`), so all
  of them print rather than fail; none is edited.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Rows + checker refusals, grandfathered at a new cutoff** | An old work item reopened later still writes records under its original id and stays excused — the same trade `STRICT_FROM` records | **Taken.** The issue names this shape explicitly |
| Reuse `STRICT_FROM` as the cutoff | The eight merged `1788229400` records (begun after `STRICT_FROM`, before this work) fail a pull request that touches their declaration, and the only repairs are fabricating reach rows for fixes nobody re-read or never touching that item again | Rejected — it is the exact failure the grandfathering exists to avoid, one constant later |
| Enforce the reach by running `grep` in CI against the named units | The checker would need to parse every language's call syntax — an enumeration over an unbounded domain, which is written rule 6's own shape | Rejected; the row is the contract, the session with the diff open is the enumerator |
| Prose only, no checker change | The rule joins the two corrections round 6 already tried informally, which worked once and lived in a transcript | Rejected — the issue exists because prose was already tried |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The SDD set: `spec.md`, this plan, `questions.md` with the pre-authorization and the assumptions, `overview.md` opened | `unverified_check.py` on the set | |
| 2 | The machine-checked rows: `fix_surface` in `chain_check.py` with `SURFACE_FROM`, the two template rows, the protocol at draft 0.7, the review-chain-spec refusal subsection, and `tests/test_the_fixes_name_their_surface.py` — every case run red against the unfixed tree first | the new test file, `test_the_last_rounds_fixes_are_checked.py`, `test_chain_check_at_the_pull_request.py`, `test_handoff_outlives_the_merge.py`, `test_the_handoff_before_round_one.py`, `ruff` | |
| 3 | The skill rules: the security axis row, the OS-boundary precondition clause, the finding-surface rule in the skill and `agents/warden.md`, the fix-surface subsection, and the three written rules; pins extended in `test_review_axes.py` and the new test file | `test_review_axes.py`, the new test file, `test_the_last_rounds_fixes_are_checked.py` (warden/skill needles), `test_docs_line_wrap.py` | |
| 4 | The fragments and the memo: `changelog.md`, `.specseal/map/1788272986-….md` with executed rows, `overview.md` closed, this table's Status column | `evidence_check.py`, `gather_changelog.py --check`, `unverified_check.py` | |
| 5 | The broad gate, once: full pytest, ruff, and the four checkers, with output read | the run itself | |

Phase 2 is one vertical slice — a record written from the template, refused by
the check when it lies, passing when honest — and it lands before phase 3
because the skill prose describes rows that must exist first.

## Operational impact

**A behaviour change in CI, and it is the point.** A pull request touching a
chain-declared work item begun on or after `1788272986` now fails when any of
its round records lacks `Contract changes` or `New units`, or lists a changed
unit without its reach. Every record in every earlier work item prints a
notice instead. Failure direction: the gate blocks more, never allows more —
a wrong refusal costs an edit to a record the author can always make, and a
wrong allow is the measured 4-of-10 regression class shipping unread.

**Prompt budget: zero.** Both rows are written by the session that already
has the fix diff open; nothing asks a person anything, per the issue's own
scope note.

No migration script, no new environment variable, no new dependency.
`plugin.json` is untouched; the pull request lands on `release/v0.3.0` and
the changelog entry is this work item's fragment.
