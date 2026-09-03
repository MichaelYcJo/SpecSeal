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
| Bring `agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`, together. `spec.md` of work item 1788433011 put this out of scope as a sweep at 148 and 160 columns; after phase 3 of that item the scribe has **one** prose line over the limit (measured 2026-09-03) and the smith is unmeasured until phase 4 lands. Covering one and not the other reads as an oversight, so the two go in one change with the argument `CONTRIBUTING.md` asks of a change to what a test guards | the repository owner, after phase 4 of 1788433011 lands and the smith's maximum can be re-measured |

## Riders waiting on a file another branch holds

| Target | Who must answer |
|---|---|
