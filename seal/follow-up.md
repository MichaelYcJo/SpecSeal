# Follow-up

**What belongs here, and it is a narrow list.**

A **schedulable item in a repository with no tracker** — something a person
could plan, in a project that has nowhere else to file it. This repository has
a tracker, so it should normally hold none of those.

**Every row names a person, with no condition attached.** An answerer column
reading `repository owner, next time X is opened` is a
condition wearing a person's clothes: nobody agreed to open `X`, so nobody
answers. A row that
cannot name who answers it does not belong in this file.

**Anything tied to a coordinate is a `# RIDER:` comment at the line it is
about.** `grep -rn "RIDER:"` is the repository-wide list, and it needs no file
kept in sync. A rider is not "someone should do this" — it is *"if you open
this file, do this too"*, and its whole value is arriving at the person who
opens the file. Moving it to the coordinate is what makes `next time X is
opened` do its job instead of being written down as though a person had
promised it.

An issue is no better for that purpose. It reaches whoever browses the
tracker; nobody greps the issue list before editing a hook. And a rider has no
completion of its own — it closes when the file it rides on is next changed,
which nothing can schedule.

**What that costs.** Nothing forces a rider to be deleted, so a comment can
outlive the fix it asked for and the next reader cannot tell a live one from a
spent one. Each therefore carries the date and SHA it was verified at. The
judgment is that a rider outliving its fix costs a confused reader for a
minute, while a rider nobody ever sees costs the defect. **This is written
down so it can be overturned**: if the stamps go stale faster than they are
read, the trade was wrong and the list comes back.

## Schedulable items with nowhere else to go

| Item | Who must answer |
|---|---|
| `evidence-check` ignores a ledger row whose coordinate is malformed instead of naming it. Found while writing a row during round 1's fix pass of #237: a coordinate written `path#unit@0` — a placeholder hash that is not eight hex characters — produced **no row at all**. Executed: the total stayed at 771 with the row present, `--strict` reported `0 broken`, and `--reverify` reported `0 rows re-verified`; the same row with `@00000000` was picked up and re-verified on the next run. So a typo in a hash does not drift and does not break, it removes the claim from the ledger silently, which is the one direction a checker of claims must not fail in. The fix is to count a row whose coordinate cell does not parse and name it, the way an old-format row is named; the judgment it needs is whether that counts as BROKEN or as a fourth state, since a row nobody can resolve is not a claim that drifted | the repository owner |
| Bring `agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`, together. `spec.md` of work item 1788433011 put this out of scope as a sweep at 148 and 160 columns. Both are now measured, with that test's own rules, at phase 4 of that item (2026-09-03, `4b85d80`): the scribe has **one** prose line over the limit (`:22`, 160 columns) and the smith **two** (`:22`, 148; `:95`, 109) — three lines in total, which is a rewrap and not a sweep. The size argument is therefore spent, and what is left is the one that decides it: adding a path to `COVERED` changes what a test guards, which `CONTRIBUTING.md` asks a separate argument for, and covering one definition and not the other reads as an oversight. So the two go in one change, with that argument | the repository owner |

## Riders waiting on a file another branch holds

| Target | Who must answer |
|---|---|
