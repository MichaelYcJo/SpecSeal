# 1788272986-the-fixes-are-what-open-the-next-round — questions

<!-- Decisions only a human can make, extracted so nothing ships on a silent
assumption. One batch before the first edit; rows added later say so. -->

## Q0 — the run's authorization (answered before the first edit)

The repository owner pre-authorized this run to the pull request: routing was
answered in issue #57's "Already decided" section and committed as
`routing.md` before the first edit, plan approval is delegated to the review
chain and the pull request (the user is asleep; the spawn prompt records the
delegation), and the issue's own scope note sets the prompt budget to zero —
*any new question put to a person* is out of scope. Everything below is
therefore an assumption recorded with grounds, not a question waiting on a
reply.

## Q1 — the `Contract changes` entry format *(assumed)*

**Assumed**: units are separated by `;`, and a unit is separated from its
reach by `→` (or the typed `->`). Grounds: the issue specifies the semantics
(each unit "with the call sites it reaches") and no syntax; `;` cannot
collide with the commas a reach list needs, and the arrow is the one
separator no existing row vocabulary uses (`—` belongs to `nobody — <why>`).
A different answer changes one function (`fix_surface`) and two placeholder
rows, so nothing downstream is built on the choice.

## Q2 — a malformed row on a grandfathered record *(assumed)*

**Assumed**: only the ABSENT row is grandfathered; a row that is present but
malformed (an empty cell, a unit with no reach) fails on any record.
Grounds: the grandfathering exists because a merged record has no honest
repair — writing reach rows for fixes nobody re-read would fabricate a
review. A malformed row has an honest repair on any record (fix the
formatting, or write `none`), which is the line `chain_check.py` has always
drawn: it fails only for what the author can always fix. No pre-cutoff
record in this repository carries either row, so today the branch is
unreachable on real history either way.

## Q3 — where the three written rules live *(assumed)*

**Assumed**: one subsection of `skills/code-review/SKILL.md`'s findings
format ("Verdicts that close too early"), not three scattered paragraphs and
not `docs/`. Grounds: the issue says "into the code-review skill where they
belong; judge placement"; the three share a shape (a closing that arrives
too early) and the findings format is where verdicts are written. The
mutation-score rule is worded to travel with the number ("stated where the
number appears") — the reporter of a score states what it licenses, which
the skill can instruct and a checker cannot verify.
