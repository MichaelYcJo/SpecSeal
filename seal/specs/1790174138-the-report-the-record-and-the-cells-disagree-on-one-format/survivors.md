# Survivors — the report, the record and the cells disagree on one format

<!-- What `survivor_check.py --range 0b8dc4b2...HEAD` with every
`seal/specs/*/survivors.md` reports for this branch, and why each report is
not a defect. The range removed `section_body`'s own end-of-section loop and
`swallowed`'s any-`#` scan (#505), the comment in the release-sizing module
saying its reach is unpinned (#366), and the sentences the eight `Broad gate`
carriers used to say; what stands elsewhere shares loop tokens with the
first, and a ledger row's past reading with the second. The one report that
WAS an instance of the class — `chain_check.py`'s own verdict-section reader
ending at any `#` — was corrected rather than excused, and is not a row
here. The quote is the anchor: an exemption stops holding when the standing
text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_a_phase_hands_the_next_one_a_record.py` | if lines[i].strip().startswith("## ") | A test helper reading a phase record's field table to the first `## ` heading — already the same-level rule for a table that sits under no heading at all, and over a phase record rather than a report. It shares three loop tokens with the loop this range removed and none of the defect |
| `seal/ledger.md` | Two cases were added and each was seen red under exactly its own mutation and was the only failure | R1 of `1789172128-…`, recording what that work item measured and then reverted; a past reading, true of that branch. The comment this range removed from the release-sizing module described the same event in the present tense, which phase 6 ended by planting the cases |
| `skills/verify/scripts/unverified_check.py` | for i in range(start_line, len(lines)): if _paragraph_ends_at(lines[i]): return False | A paragraph walk in the reader that ends at a paragraph boundary, not a heading; it shares `len lines if` and `lines i return` with `section_body`'s removed loop and reads a different thing |
| `tests/test_unverified_rows_close.py` | for i in range(start_line, len(lines)): if block_ends_at(lines[i]): return False | The same paragraph walk, pinned by its own module; the shared tokens are the generic loop's, not the section rule's |
| `.github/scripts/gather_changelog.py` | (n for n in range(at + 1, len(lines)) if lines[n].startswith("## ")), len(lines), | The gatherer's append arm (#289, work item `1790173209`, landed on the release branch after this branch was framed) walks a changelog to the next `## ` heading with the same generic `range(…, len(lines))` / `lines[n].startswith` loop shape that `section_body`'s old any-`#` scan had; the shared tokens are the loop's, not the rule this branch removed, and the gatherer's stop at `## ` is the right reader for a changelog, whose sections are all one level. First seen at the merge of `origin/release/v0.15.0` (`0be23b80`), where the range CI reads gained that file |
