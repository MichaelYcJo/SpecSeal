# 1791076836-every-rule-claude-md-restates-has-one-home — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a41946af |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Ship the method. Add the repository-wide verbatim ratchet (spec D5): its
corpus, its normalisation with wrapped section names, `WINDOW` from one
source, a baseline measured on phase 1's tree with the sanctioned agent
preamble marked, and a failure message that names the act; see it red
against a planted paste and green against a planted deletion. Rewrite F4's
paragraph of `docs/the-record-layout.md` and nothing else in that document,
naming #755 as the remainder issue. Write the closing records: the ledger
fragment, `changelog.md` naming #755, `overview.md` and this record. Before
handing back, fetch; if `release/v0.18.1` moved, merge it in without
rebasing and re-measure the baseline.

## What this phase found

**The release branch moved, and the baseline was taken twice.** On phase 1's
tree the ratchet measured 67 files, 184,317 words and 102 pairs, whose
per-pair counts of shared 15-word windows sum to 2,064 over 1,170 distinct
windows, and 197 maximal runs counted pair by pair. `CLAUDE.md` ↔
`docs/branch-and-release.md` is no longer a pair. `origin/release/v0.18.1` then
moved to `edee5ca2` (#756, #757, #758) and was merged in at `8484c1f2`. After
the merge: 68 files, 188,585 words, 103 pairs, a sum of 2,091 over 1,197
distinct windows, 204 maximal runs. (Corrected in round 1's fix pass, ⬜ 4:
this paragraph called the sums *distinct runs*.)
#756 added `templates/pact-review.md`, which shares 10 runs with
`docs/the-pact.md`, and raised `docs/the-pact.md` ↔
`skills/evidence-check/SKILL.md` from 4 to 21. Both went into `BASELINE` at
`7660cff3` as measured. Neither is this branch's copy, and both are #755's to
weigh.

**These numbers are not the framer's, and Q1 expected that.** The framer's
probe at `07aec0f2` reported 108 pairs and 229 maximal runs, with the
`CLAUDE.md` ↔ `docs/branch-and-release.md` pair among them. The probe was
deleted, so its normalisation cannot be compared line by line. The module's
own `shared_counts` is what `BASELINE` is checked against, and that is the
measurement written into the table.

**The unit counted is a distinct window, not a maximal run.** A 17-word
identical run is three windows. Counting windows is what makes the ratchet
monotone under a paste: a longer paste always raises the count, where a
run count can stay flat as a new paste joins an old run.

**`CLAUDE.md` ↔ `CONTRIBUTING.md` is still a pair, at 14.** It is #715's
fragment-rule link sentence (*Which file a change writes — its changelog
entry, its ledger rows, …*), carried in both files. The prompt keeps that row
word for word, so it is baseline debt like the others.

**The ten pairs of agent definitions are marked sanctioned** in a comment
naming `tests/test_every_agent_reads_the_contract.py`. framer ↔ smith also
shares its `skills:` frontmatter list, and smith ↔ warden carries debt of its
own beyond the preamble (153 against 65), cluster (b) of the remainder.

**The census of path-listing scopes needed the new corpus.** It found the
ratchet's `corpus` only once the module was staged, and then failed until
the scope was classified as applying `on_disk`. The ratchet skips a missing
file rather than declining: a file that is not on disk can only lower a
count.

**Seen red (§15), executed through `mutation-check` one break at a time.**
Red: the bound raised past any count, the bound made exact (`!=`), the
section name stopped at a line break, the generated region kept, fences
kept, headings kept, Korean editions kept, every pair's count flattened to
one, the longest run cut short, and the `on_disk` skip removed (red through
the census module). Three survived at first: the path-form section name, the
lowercasing, and the `on_disk` skip run against the ratchet alone. The first
two each got a case and then went red; the third is the census's to hold.
Against the tree, a sentence of `CONTRIBUTING.md` pasted into
`docs/branch-and-release.md` was named as *7 runs of 15 words where 0 were
measured; the longest is 21 words*, with the act.

**The merge drifted ledger rows, and only some were this branch's.** Where my
identifiers bullet and #757's encoding bullet both now sit, `CONTRIBUTING.md`
§*House rules* moved under four released rows and #757's E5 row. I read each.
All still hold, because none is about either bullet. This fragment's
re-reads were re-stamped, and E5 was re-stamped in place in #757's fragment.
That is what `docs/the-evidence-ledger.md` §*A released row is read again in
the branch's fragment* says for a fragment row. Ten other rows are drifted on
`origin/release/v0.18.1` alone, before this merge, on files this branch never
touched: `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv`,
`tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` and
`templates/config.md`. Nothing here read them, so they are left, and the
hand-back names them.

**`survivor-check --range edee5ca2..HEAD`** reported seven places, every one
a home carrying the wording `CLAUDE.md`'s removed copies held, or the
`CONTRIBUTING.md` application phase 1 kept. Each is in `survivors.md` with a
quote and its grounds.

**Narrow runs, executed on the merged tree.** The 40 modules that read
`CLAUDE.md` or `CONTRIBUTING.md`, or that this branch touched, with the
hygiene set and the wrap, fold and encoding modules: 2180 passed.
`claude_block.py --check` exit 0; `bin/fold-check` exit 0; `git diff -U0
e141980a -- docs/the-record-layout.md` is one hunk inside F4.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| F4's *not built* paragraph in `docs/the-record-layout.md` | the same paragraph, rewritten as built; the remainder it named is #755 |
