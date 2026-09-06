# 1788613827-a-runs-report-carries-one-comparison-table — phase 4

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | becaf95 |
| Ran by | |

## What this phase was asked

The closing set, in four files. `overview.md` from
`templates/sdd-overview.md`, written first because
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
was red on this branch and this file is what turns it green — only what the
diff cannot show, with `## Not verified` in the one shape a machine reads and
the orchestrator named as the answerer for the broad gate.
`seal/ledger/1788613827-….md`, a fragment rather than an append to
`seal/ledger.md`, with no header, coordinates carrying no line number and no
commit, and the `Checked` column holding the date the code was read; the
rows to consider were named, the judgment of which survive was left here, and
a claim not verified by opening the code was not to get a row. Then
`evidence-check`, with its whole output read rather than its exit code alone,
and every row resolving. `seal/specs/…/changelog.md`, matched to a fragment
another work item already wrote rather than written under `CHANGELOG.md`'s
`## Unreleased`. And `docs/flow.md`'s #170 box ticked — that one box and
nothing else, since the other three items of 0.8.2 are not this branch's.

Five constraints came with it. Edits through the `Edit` tool, the session's
auto-mode note about `sed` notwithstanding. `skills/writing-style/SKILL.md`
governs the prose in all four. `docs/flow.md` is not in
`tests/test_docs_line_wrap.py`'s `COVERED`, and the surrounding wrap is
matched anyway. No real domain, user path or org name reaches a committed
file — the runner path in the spawn prompt is a fact about one machine. And
the full suite, the repository-wide lint and the typecheck are not run here;
they are the orchestrator's broad gate after the rounds.

## What this phase found

**The unscoped `evidence-check` found five drifted rows in `seal/ledger.md`,
and four of them are this branch's.** The fragment read `19 ok · 0 drifted`
on its own, which is exactly the report #153 was opened about: a scoped run
says nothing about the rows a branch broke in the shared ledger, and those
are the rows with the longest reach. Phases 2 and 3 enlarged four sections
that seven existing rows cite — `## The handoff before round 1`, its
`### After the run — the per-segment bars` subsection, `## Pull request
bodies` (four rows), and `## Measure the segment, and feed the flow log`.
Each claim was re-read against the enlarged section and each still holds:
the handoff's four requirements and the pointer at the meter are where they
were, the three bars and the `1.2`/`1.8` tie are untouched, the pull request
section's FIRST line — which is what S1 pins, by position rather than by
phrase — did not move because both new paragraphs sit after the
writing-style sentence, and F5's absence claim survives because phase 2's
nine rows and four paragraphs name no issue number and no milestone.

**The fifth drifted row was left, and proving it was not this branch's took
two commands rather than a judgment.** `templates/config.md#"# Repository
config"` is cited by one row, S8. `git diff --quiet a9a827b HEAD` over
`templates/config.md` and over `seal/ledger.md` both exit 0, so the two
inputs to that verdict are byte-identical to `main` and the row was already
drifted there — it arrived with the 0.8.1 merge and nobody re-stamped it.
Re-stamping it here would put another branch's change into this diff under
this branch's name, and it blocks nothing:
`.github/workflows/test.yml`'s ledger job runs the unscoped check with
`set +e`, fails only at exit 2 or above, and turns exit 1 into a
`::warning::`, on the stated grounds that drift is *a true statement about a
branch mid-flight* and a check that is always red gets ignored. So a local
exit 1 on drift is the designed reading and not a failure to chase.

**`--reverify` has no way to re-stamp some drifted rows and not others**, so
the shared ledger was re-stamped whole and the one hash this branch did not
earn was reverted by hand to `45edf260`. That is one `Edit` over a value the
same run had just printed as `45edf260 -> 541502a6`, which is why it is
auditable; a session doing this from memory would have no such line.

**The fragment stamps 20 coordinates and the checker reads 19.**
`session_cost.py#token_totals` is cited by both R1 and R2 — the counting
rule and the two-counters decision are different claims over one unit — and
the checker resolves each distinct coordinate once. The pair of numbers is
not a miscount and needs no reconciling.

**The overview's red was confirmed both ways rather than inherited.** The
spawn prompt labelled it executed by the orchestrator; §5 makes that a claim
with a coordinate. Removing the file and running `-k overview` exits 1 on
`AssertionError` at `tests/test_chain_hooks_hardening.py:909`, restoring it
exits 0 — the file's own bytes kept and put back, never a `git checkout`,
because at that moment three other files of this phase were uncommitted.

**For the review chain.** `plan.md` row 4's Verified by cell asks for
`uv run pytest tests/ -q` and `uvx ruff check .`; both were declined under
contract §2 and §3 and are rows of `overview.md` §Not verified with the
orchestrator named. That is the first divergence in the memo's table. This
phase adds no unit and no case — it writes records, a fragment and one
checkbox — so there is nothing here for §15's red or for a mutation battery,
and the two commands that judge it are `evidence-check` and the nine modules
that read what it wrote.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds. The single value it overwrote is one hash in `seal/ledger.md`, restored to what it already held | none |
