# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 7455bd60 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The reviewer-facing standard — #503, #437, `&lt;!--`. `agents/warden.md`
§Report: example rows in the skeleton (`🟡 1`, bare `🟢 … confirmed`, `❓`),
the five markers and `✅` not among them, the `&lt;!--` sentence, `###`
allowed under the two fenced sections, the three requirements of a carried
closure beside the no-id sentence. `skills/code-review/SKILL.md` §Findings
format and `docs/review-chain-spec.md` §*A verdict row that commissions
nothing*: the worked row. `templates/sdd-round.md`'s comment: the same row.
Cases A15 (the skeleton executed through `new`) and A16 (the documents
pinned). `changelog.md` fragment; `overview.md` closed; every ledger row of
the fragment written. Measure Q7: does `new` accept `✅` in the `#` cell. The
spawn prompt added what this release had already learned: every rule the
orchestrator had been typing into spawn prompts by hand should be a sentence
the reviewer reads.

## What this phase found

**The frame holds for this phase.** The skeleton was at the place `plan.md`
named, with two header rows and no example; the no-id sentence in §Role was
where the three requirements go; §Findings format and the spec's subsection
each had the *earlier round's number goes in the Finding cell* paragraph the
worked row now follows.

**Q7, executed: accepted.** A scratch repository driven from Python (contract
§8), a report whose verdict table carries `| ✅ | the fix holds | … |
verified | read |` beside a `🟡 1`, and `round_record.py new` at `0ce4987b`:
exit 0, the record written, the tick row copied through as a row that
commissions nothing, `Pass` unticked for the 🟡. So the sentence the frame
wrote — *admitted and not a marker* — stands, and what keeps a reviewer from
writing a sixth vocabulary is the sentence in the skeleton, pinned.

**What the run had already learned reached the standard as sentences.** The
`#` cell filled on every row and the four shapes it takes; `🟢`/`⬜`/`❓` for a
row that commissions nothing; the verdict word `confirmed` for a carried
closure, never `fixed`, with the reason the cap gives; `&lt;!--` for a comment
opener; `###` allowed under the two fenced sections. The two things the prompt
named that belong to the fix pass rather than the reviewer — `close` refusing
a ⬜ row with no id in a fixes table, and a Verdict cell reading `fixed <sha>`
— are already `skills/implement/SKILL.md` §5's and `agents/smith.md`'s, and
were left there. The scratchpad collision of two parallel wardens is an
orchestration fact rather than a report-format one, and is handed back rather
than written into the reviewer's file.

**Seen red against HEAD's `agents/warden.md`** (executed; the committed file
restored from git over the phase 5 text, then the phase 5 text put back from
a kept copy):

```
FAILED tests/test_the_record_is_generated.py::test_the_reviewers_skeleton_is_a_report_the_generator_accepts
E       assert 2 == 3
FAILED tests/test_the_report_standard_is_one_in_three_places.py::test_every_carrier_shows_the_same_carried_closure_row
FAILED tests/test_the_report_standard_is_one_in_three_places.py::test_the_warden_names_the_five_markers_and_the_tick_as_not_one
FAILED tests/test_the_report_standard_is_one_in_three_places.py::test_the_warden_tells_the_reviewer_to_write_the_opener_escaped
FAILED tests/test_the_report_standard_is_one_in_three_places.py::test_the_warden_allows_subheadings_under_the_two_fenced_sections
FAILED tests/test_the_report_standard_is_one_in_three_places.py::test_the_warden_says_where_the_severity_goes
6 failed
```

A15's first run on the phase 5 text failed on its own filter — it counted
the probes and deferred header rows as examples — and reads the verdict table
alone now; the generator accepted the skeleton at exit 0 on both runs.

**Then green** (executed): the seven selected cases 7 passed; the four
document-pinning modules that read the warden, the skill and the template
(`test_docs_line_wrap`, `test_the_reviewers_report_reaches_the_record`,
`test_a_finding_id_is_a_bare_integer`, `test_one_word_one_meaning`) 130
passed.

**Six mutations, each restored** (executed): the row deleted from the
template — the carrier case red; the row's `confirmed` made `fixed` in the
spec — the same; the tick sentence, the opener sentence and the `###`
permission each deleted or negated in the warden — their own pin red; the
skeleton's carried row numbered — the executed skeleton case red, because
`new` then keys a row no fix table is asked to close.

**Ledger:** A6 and A7 in the fragment. Eight rows anchored on the warden's
§Report, §Verdicts and §Paste-ready fixes, the skill's §Findings format and
the spec's two sections carry a dated note.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the two-header-row skeleton in `agents/warden.md` §Report, which showed the columns and no shape for the `#` cell | the same fence, with three example rows |
