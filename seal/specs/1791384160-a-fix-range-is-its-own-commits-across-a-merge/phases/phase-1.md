# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 6d12e2ea |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`plan.md` phase 1: write `chain_check.py#own_commits`, the one reading of the
commits a range owns, with its parse measured first (Q1). Make
`fragment_left_behind` walk it from round 1's target to HEAD, take each
record's range and *after the last round* from it, and name a commit when no
owned fragment-changing commit descends from it (Q2). Remove `walk_tip` and
`commits_after`, and rewrite the module docstring's fragment row. See S7 and
S9 red first, and re-document S8's three cases. Write the rule's home in
`docs/the-record-layout.md`, rewrite the fragment section there to say the
owned-commit walk, and link the home from `docs/round-record-spec.md` §*The
fix range*.

## What this phase found

**The frame holds, with one sharpening.** `spec.md` §*In* says a sibling's
commit "descends from `a` never". That is true for every range this work
reads, because each start is on the branch after the build: round 1's target,
or a round's `Fix range` start. It is not true of a range that starts at the
fork point. The measurement probe started there by mistake, and a sibling
commit on the base was listed as owned, because it does descend from the fork
point. Nothing in either script hands `own_commits` such a start, so this
changes no code. The home says the rule in terms of descent and makes no
claim about where a start sits.

**Q1, measured on git 2.50.** Each commit is `\x01<full> <short>\0`, then a
`\n` before its first entry, then `<status>\0<path>\0` per entry. A commit
that changed nothing is its header alone, so the next token is the next
header. A rename under `--no-renames` is `D` of the old path and `A` of the
new. A start that does not reach its end gives empty output at exit 0. The
parse walks the NUL-separated tokens by position rather than splitting on
`\x01`, so a path holding `\x01` or a newline is never read as a header.
`commits_after` split on `\x01`, and that guess is gone with it.

**Q2, measured.** `rev-list --ancestry-path ^<target> F1 F2` lists every
commit that any `F` reaches and that descends from the target, each `F`
included. One call is enough. A case now plants a fragment change on each of
two lines of history (`test_a_fragment_brought_along_on_each_of_two_lines_clears_both`),
and narrowing the call to the newest `F` turns it red. Without that case the
narrowing survived every other case of the module, because each of them has
at most one fragment commit outside the line of the newest.

**Q4.** Both cases kept their shapes. Their names changed too, because each
name stated `walk_tip`'s premise. The first case now also asserts that the
topic's commit is named, which is S9's first half and the red leg against the
first-parent walk.

**Seen red first (§15)**, all against 4e849e50 with the cases as written:

| Case | Red at 4e849e50 |
|---|---|
| S7, `test_a_branch_rebuilt_on_the_base_names_its_own_commits_and_not_the_siblings` | the sibling's squash named *after the last round*, and the lagging fix not named — #805's report exactly |
| S9, `test_a_topic_merged_into_the_branch_names_the_branchs_fix_and_the_topics_commit` | the topic's commit not named |
| S9, `test_a_fragment_change_clears_exactly_the_commits_it_descends_from[False]` | no notice at all: the fragment's last change in the first-parent list came after the topic's merge |

**Mutations, through `bin/mutation-check`, each red:** `--ancestry-path`
removed from `own_commits` (S7); the descent test dropped (5 cases); the
fragment commits narrowed to the newest (the two-lines case); a record's
owned commits widened to HEAD (the attribution case); the commits after the
last round emptied (both `after the last round` cases).

**The work item's records named what the tree no longer has.** `evidence-check
--strict` refused `spec.md`'s `walk_tip` and `questions.md` Q4's two old case
names. Each line now carries `NAME NOT IN TREE`, which is the checker's own
remedy and leaves the sentence as the framer wrote it. `plan.md`'s
`own_units` is refused the same way until phase 2 writes it.

**The ledger fragment is named for the whole work-item id**,
`seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md`.
The spawn prompt said `seal/ledger/1791384160.md`. The fold reads the
heading and the marker from the file name (`.github/scripts/fold_ledger.py`),
and every fragment in this repository's history carries the full id, so the
shorter name would fold under a heading that names no work item.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `chain_check.py#walk_tip`, the reading of HEAD's parent order | nowhere: `own_commits` needs no tip, and the home says why parent order is not read |
| `chain_check.py#commits_after` and its `--first-parent` walk | `chain_check.py#own_commits`, which keeps its `--no-renames` and its oldest-first order |
| the three `rev-list` calls in `fragment_left_behind` | `own_commits` over each record's range and over `<end>..HEAD` |
| the sentence *where the checkout is CI's … the walk starts at the pull request's own head* in `docs/the-record-layout.md` | the same section's sentence that CI's checkout reads the same commits, and the new section's rule |
| 0.18.3's claims on the first-parent walk (`S1, S5, S8, S10` and `S2, S3, S4, S6`) | two `Corrected ·` rows in this item's ledger fragment |
