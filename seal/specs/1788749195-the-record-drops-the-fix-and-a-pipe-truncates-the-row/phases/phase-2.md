# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — phase 2

<!-- seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 30acdd9 |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Carry the reviewer's paste-ready fixes into a section of the record,
extracted with `fenced_after` from a heading the findings format names. The
empty arm writes a record rather than refusing — a verifying round that opens
nothing writes no fix, and `spec.md` has that as a scenario rather than an
edge case.

`plan.md`'s Alternatives are settled: not the report kept verbatim below the
tables, and not a sibling `round-N-report.md`.

## What this phase found

**The heading is `## Paste-ready fixes`, and #187's own suggestion was
`## Fix sketches`.** The name was changed on purpose. The findings format
calls the artefact *a paste-ready fix* four paragraphs running, and the same
skill uses *sketch* for the thing that fails: §*Verdicts that close too early*
records three blocking findings that *"arrived as sketches that read as
paste-ready and were not."* A heading naming the failure would be the one word
in the record with two meanings.

**The mechanism needed nothing new, and that was the plan's claim to check.**
`fenced_after` already copies every fenced block under a heading, verbatim and
prose excluded; it gained a second caller and no code. What did change is one
constant.

**A section with no table needed the guard's heading list to become its own
constant.** `swallowed`'s first loop iterated `REPORT_TABLES`, which is a list
of (heading, header) pairs, and the new section has no header. Splitting the
guard's two questions apart:

| Loop | Reads | Why that list |
|---|---|---|
| headings | `READ_HEADINGS` | every heading the generator looks up — a fence can take any of them, and the record then answers absence with its own wrong value |
| rows | `REPORT_TABLES` | only a table can lose its rows to a fence while its heading stands |

`test_a_fence_that_takes_a_section_the_generator_reads_is_refused` asserts its
own parametrization equals `READ_HEADINGS`, so the new section is guarded and
gets a case by one constant gaining a member — which is the argument that
constant was introduced for in #169, now with an instance behind it.

**The record's own answer for absence is what makes the omission visible.**
`plan.md` accepted that a reviewer can omit the heading and mitigated it the
way the four tables are mitigated. In practice the mitigation is the sentence:
the section reads `no paste-ready fix in the report`, which states what the
generator observed rather than that none was needed, and beside an open 🔴 in
the verdict table two rows up it is the gap written down. Distinguishing *the
round needed none* from *the reviewer wrote none* is not something the
generator can do, and claiming either would be the record asserting something
nobody checked.

**The two repairs did not meet, which is what the phase order bought.** A
paste-ready fix reaches the record as a fenced block, and `fenced_after`
copies a fence whole — nothing in this phase goes through `row_cells`. Had
the section arrived first, a reviewer would have had one round in which the
only durable home for a fix was still the Grounds cell, which is exactly the
compounding #189 measured.

**The section sits between `## Verdicts` and `## Executed probes`**, because
the fix belongs beside the finding it answers and the record is the fix pass's
agenda. Nothing reads the record positionally — every reader looks a heading
up — so the placement is for the person.

**An open fence under the new heading was already refused before this phase,
and by the right rule.** `swallowed`'s report-wide never-closed half fires on
it, because an unclosed fence runs to the end of the file. What was NOT
already refused is an opener hidden inside an HTML comment: that one is
invisible to `swallowed`, which reads the comment-stripped text, and an opener
to `fenced_after`, which reads `raw` — and it now reaches the second section
too. `test_a_fence_opened_inside_a_comment_under_the_paste_ready_heading` is
the new instance of that class; it was green for the plain unclosed fence and
red for the hidden one.

**The gate argument** (`CONTRIBUTING.md` §*What a change to a gate must
carry*). This adds a section to the file `chain_check` gates a pull request
on, and `chain_check` reads named sections — so a record written before this
phase, having none, is the state every reader already handles. The failure
direction is one new refusal, and it is narrow: a fence opened inside an HTML
comment under the new heading, which is the shape that would otherwise write a
record with an open fence in it and blank every section below. Prompt budget:
zero — the refusal is an exit code to the session running the generator, not a
question, and every other arm writes a record. Platform: no process
inspection, no path resolution, no encoding boundary.

**What phase 3 inherits.** The heading is `## Paste-ready fixes` and it has
to reach three documents: `skills/code-review/SKILL.md` §*Findings format*,
which is where a reviewer reads what a report owes;
`agents/warden.md` §Report, which
`test_the_wardens_report_headers_are_the_generators_constants` already reads
the table headings out of the generator and looks for; and
`templates/sdd-round.md`, which names the record's sections. The generator's
constant is `PASTE_READY`, so any pin should read it from there rather than
typing the heading a second time.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `swallowed`'s heading loop over `REPORT_TABLES` | `READ_HEADINGS`, a superset of it. The row loop below still reads `REPORT_TABLES`, and the docstring now says which loop reads which and why the two lists differ |
