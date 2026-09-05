# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — questions for the planner

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | How much of #161's staged plan does 0.8.1 carry? | **generator + four rules + the mechanical set** — reaches the three-hour target · rules + mechanical only — a day, and the 50 min of record-writing per round stays · all of it plus a probe-runner — a new field, against the moratorium | generator + rules + mechanical | ✅ the repository owner, 2026-09-05 |
| Q2 | What happens to the floor's reopening exception? | **bounded to one** — a second record closing on a fix after the floor is refused, the run ends `capped` · removed entirely — every verifying-round finding is an issue; on the last branch round 7's floor bug and the Windows set would have shipped as issues | bounded to one | ✅ the repository owner, 2026-09-05 |
| Q3 | Routing — implementation, review, destination | smith · through the review chain · open the pull request | — | ✅ the repository owner, 2026-09-05, `routing.md` |

## Assumptions, stated rather than asked

| # | Assumption | Why it does not change what is built |
|---|---|---|
| A1 | The fix surface is derived by AST for Python files; for other languages `close` lists added definitions by a diff-line heuristic (`def`, `class`, `function`, `fn`, `func`) and says so in the cell's trailing comment | This repository is Python. A user repository in another language gets a measured-but-coarser cell rather than a pending one, and the limit is written where it is read |
| A2 | The warden's report and the smith's fix table are saved to the session's scratch directory and not committed; the generated record is their durable form | Committing a second file per round is a new file the checker would have to learn to ignore, and the record already carries every cell the report contributed |
| A3 | This branch's own records are written by the generator from round 1, and the rules bind its rounds from round 1 | The last branch applied the rules from round 14 and ended two rounds later; a branch that ships a writer nobody has used is the class #161 counts |
| A4 | `deferred <home>` is the closing word for a capped run's findings — in `CLOSED_WORDS`, not `FIX_WORDS`, and bare `deferred` stays open | The alternative, a new `Needs a fix` value, changes a row the reviewer owns; a verdict word changes only the vocabulary the orchestrator's script writes |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
