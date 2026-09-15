# survivors — 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red

<!-- `survivor-check --range aa3000d..HEAD` at the close of phase 3 reported
four places still carrying wording this range removed. None is a live defect,
and the reason all four are reports rather than findings is the same one: this
work item REBUILDS a seam that was reverted, so the wording it removes is
wording the released 0.11.4 correctly describes as absent.

Each row quotes the standing text, so the exemption stops holding the moment
that text changes.

**Re-run over the whole branch at the close of phase 6 and it reports none.**
`survivor-check --range aa3000d..HEAD` at `25a2639`: 989 files examined against
102 removed sentences, *no removed wording is still standing*. The four rows
below are kept rather than deleted, because they record what the range looked
like when it was measured and because the range is re-resolved on every run —
a later phase's edits are what put those four out of reach, not a repair to
any of them. -->

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_a_finding_id_is_a_bare_integer.py` | `` `round-*.md` is git's pathspec and git has no way to say "and then a number", so it also returns the three files the review chain writes beside a record `` | `committed_records`'s own docstring, and the sentence is true where it stands. What this range did was move the SAME true statement out of two walkers' bodies into `_numbered`'s docstring in each of them; the third reader keeps its copy because the third reader still does the filtering itself. A correction here would delete a true sentence from the one function that needs it |
| `seal/specs/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records/spec.md` | `Given a record edited on disk and not committed · When `chain_check --worktree` runs · Then it judges the edited cell` | A shipped work item's acceptance scenario, about a different reader and a different question: `chain_check --worktree` is the mode that deliberately judges the working tree. This range changed what the TEST-side listers read, and left that mode alone. The match is on the phrase *a record edited on disk and not committed*, which both sentences use for opposite reasons |
| `CHANGELOG.md` | `Writing 🟢, ❓ or ⬜ with no number on a row that really is an open finding still writes a finding no fix table will be asked to close, and nothing catches that` | The released 0.11.4 section, and it is accurate history: the verdict arm was reverted at `1ff0a6c` before that release, so nothing DID catch it in what shipped. Rewriting it would make a released changelog describe behaviour the release did not have. What this work item changes is stated in its own `changelog.md` fragment |
| `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/changelog.md` | `Writing 🟢, ❓ or ⬜ with no number on a row that really is an open finding still writes a finding no fix table will be asked to close, and nothing catches that` | The fragment the row above was gathered from, same release, same grounds. It is the source of a shipped sentence, so it is history for the same reason |

<!-- Re-run at the close of round 1's fix pass. `survivor-check --range
53259ab..HEAD` at `df404e2`: 989 files against 15 removed sentences, three
places still standing. All three are inside `round_record.py` itself, and all
three are the SAME report — the third refusal 🔴 2 removed shared its phrasing
(`raise Refused(f"round-…`, `no cell was written`, `round-{n + 1}.md`) with the
two refusals that were deliberately kept and with `reach_back`'s. Correcting
any of them would delete a refusal that is still right.

The three rows are the neighbours the removal left behind, not copies of it. -->

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/scripts/round_record.py` | `mine = f"round-{n}" filled = 0 for i, cells in body` | `reach_forward`'s walk and the coordinate refusal below it — one of the two refusals the round left standing on purpose. Round 1's 🔴 2 removed the EMPTY-FILL refusal that followed this loop; this one refuses a row naming a coordinate round N's verdict table does not hold, which is still a record nobody can carry words into, and `test_the_reach_forward_refuses_a_coordinate_the_verdict_table_lacks` pins it |
| `skills/code-review/scripts/round_record.py` | `path = os.path.join(rounds, f"round-{n + 1}.md") if not os.path.exists(path): return None` | `reach_forward`'s head — the silent state where round N+1 does not exist, and the unreadable-table refusal just below it, the other refusal kept. A record whose `## Inherited coordinates` cannot be read has no honest place for the words at all, which is a different state from a table that names nothing from round N, and `test_the_reach_forward_refuses_a_next_record_with_no_inherited_table` pins it |
| `skills/code-review/scripts/round_record.py` | `text = read_text(path, f"earlier record round-{n - 1}.md")` | `reach_back`, the other direction entirely — it sets round N-1's `Fixes checked by`, and this range did not touch it. The match is on the `round-{n - 1}.md` shape the removed refusal also used |
