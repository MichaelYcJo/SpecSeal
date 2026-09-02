# the ledger fragments fold at release — questions for the planner

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. The spawn prompt pre-answered the design gate's questions (mirror
`gather_changelog.py`; the word is *fold*; one release sequence, documented
where the gather is). What is below is what it did not. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should a work item released in an EARLIER version, whose `evidence-todo.md` was never drained, block THIS release? The design record says "any released work item"; the ticket says "any work item". Both readings include it, and `settle` (#83) will skip such an item rather than stop | (a) block, and the remedy is one drain commit on the release branch — the guard is about what the tree holds. (b) scope the guard to work items whose fragment is being folded, so an old item's stale file is ignored — quieter, and it lets the state the guard exists to catch persist across releases | (a). Written into `spec.md` §"Which work items". Both files in the tree today are drained, so nothing blocks now | ⬜ |
| Q2 | Where the folded section lands in `map.md`. The changelog inserts at the top because it is read newest-first; the ledger is read by area, and its top holds the notation a reader needs before any row | (a) append at the end, newest last. (b) insert above the first `##` area, mirroring the gather exactly | (a). `spec.md` §"Data & interfaces" has the reasoning; nothing measures from the position | ⬜ |
| Q3 | Whether `--check` also runs the evidence-todo guard on a release pull request, or only looks for fragments left behind | (a) both — a hand fold or a release branch where rows were moved by hand still meets the guard at the last moment anyone is looking. (b) fragments only, the literal mirror of the changelog check | (a). `plan.md` alternative E | ⬜ |

Answered rows feed back into `docs/one-root-by-lifetime.md`'s "Decided after
the thread" table before this directory's work merges, or stay as defaults
named in the pull request body.
