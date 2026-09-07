# 1788789985-round-record-dies-on-python-3-9 — questions for the planner

<!-- seal/specs/1788789985-round-record-dies-on-python-3-9/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Do the four deferred members of the class belong in `seal/follow-up.md` at all, or in the tracker? | **`seal/follow-up.md`** — where the handoff sent them, and where they are today. **The tracker** — which is what that file's own opening says: "A **schedulable item in a repository with no tracker** … This repository has a tracker, so it should normally hold none of those." **A `# RIDER:` at each line** — the file's other rule, for anything tied to a coordinate; rejected here because the finding is about a class of five files and a rider at one line cannot say *and four others*, and because nobody opens `gather_changelog.py` before running it | The rows are in `seal/follow-up.md`, naming the repository owner. The handoff asked for that spelling explicitly, and a row in the wrong file is recoverable where a deferral to nobody is not | ⬜ |

**Nothing here blocked the build.** Q1 changes where four rows live, not what
they say or what this work item builds, so the `implement` skill's own test —
*would a different answer change what you build now* — says it is a row rather
than a question that stops the session.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
