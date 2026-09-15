# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `f3b3b62`, `4f4d653` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#142 and its class. Both `_real_records` copies read HEAD via
`git ls-tree -r -z --name-only HEAD -- seal/specs` with a `fullmatch`, so a
staged-uncommitted record is not listed-and-skipped; the third corpus reader in
`tests/test_a_finding_id_is_a_bare_integer.py` is assessed and repaired or named
with the reason; the positive control lands — a fixture record known to be
refused, asserted to produce a failure through the same call path. The stale
`TypeError` clause is answered in this record rather than coded around.

The phase is first because it is the instrument: the two walkers over this
repository's own records are what say whether phases 2–6 broke the tree, and
`1ff0a6c` exists because that answer arrived at a broad gate instead of at a
phase boundary.

## What this phase found

**Q2 is answered, and the answer is *stale in all three*.** Executed
2026-09-15 in a `git clone --no-local` of this repository: two
`round-N-draft.md` siblings committed beside a real record, then the two
walkers and both corpus cases run in the clone. Four cases pass, exit 0, no
`TypeError` anywhere. The clone and the probe were deleted.

The reading behind it, which the measurement confirms rather than replaces:
the crash #142 describes is absent by a **conjunction**, not by one repair.
The sort inside `_real_records` is `sorted(p for p in out.split("\0") if p)`
— a plain path-string sort over strings, which cannot raise — and the keyed
sort is downstream in the caller, behind a `round_number is not None` filter
that landed 2026-09-08 in `14c2a57` (#234), four days after #142 was opened.
The third reader never sorts numerically at all. So #142's clause is **stale
about the outcome and imprecise about the mechanism**: the name it gives the
sort is not the sort that could raise. No case was written for a crash that
cannot happen, and this paragraph is why the ticket's row is answered rather
than unanswered.

**The three readers are not three copies of one defect.** They divide on
where their CONTENT comes from, and the division decides what the repair
buys:

| Reader | Content from | What `ls-files` cost |
|---|---|---|
| `tests/test_chain_check_at_the_pull_request.py#_real_records` | HEAD, via `read_record` | a staged record listed, then silently skipped — every per-record check answers `([], [])` |
| `tests/test_the_reopening_is_one.py#_real_records` | HEAD, same | the same silent skip |
| `tests/test_a_finding_id_is_a_bare_integer.py#committed_records` | the working tree, via `id_cells` | no skip at all — the record is read and counted, so a function named `committed_records` measured a population that is not the committed one |

The third is the quietest and it is why the mutation run had a survivor: with
the listing put back on `ls-files`, all 47 cases in that module stayed green,
because nothing there could notice. It now has a case of its own, and its
docstring states the residual it keeps — content still comes from disk, which
is the right reading for a population measurement over a tree somebody is
editing, and the wrong one for a check on what CI will see.

**Git's pathspec `*` crosses a slash**, so `seal/specs/*/rounds/round-*.md`
handed to git is wider than it reads. All three listers now take the listing
over `seal/specs` and narrow with `RECORD_PATH_RE.fullmatch`, spelled once per
module beside the reader it serves.

**The positive control needed the walk extracted, and the extraction is what
makes it the same call path.** An assertion that reads a `failures` list
cannot tell an empty list from a loop that never collected anything, which is
the whole of #142's second half — so both walks moved into `_record_walk` and
`_capped_failures`, and the controls call those. The fixture for the first is
one record carrying an empty `New units` cell **and** an empty floor row:
`fix_surface` refuses the first on any record and `stopping_floor` the second,
neither grandfathered, so **stubbing either `failures.extend` turns the case
red**. That is stronger than the plan's acceptance, which asked only that both
stubbed together go red.

**Phase 1 drifts a shared-ledger row the plan's drift table does not count.**
`seal/ledger.md` F12 anchors on
`tests/test_chain_check_at_the_pull_request.py#test_this_repositorys_own_round_records_pass_the_per_record_checks`,
whose body lost its loop to `_record_walk`. Re-read on substance: what the
case does is unchanged, so the claim holds, and the residual — the walk it
rests on now lives in a unit the anchor does not cover — is written into the
row rather than fixed by re-pointing it. `evidence-check --strict` is exit 0
after the re-stamp: 1214 ok · 0 drifted · 0 broken.

**For phases 2–6:** the two walkers are now the instrument the plan says they
are, and the narrow command for them is
`bin/test tests/test_chain_check_at_the_pull_request.py tests/test_the_reopening_is_one.py -q`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `TypeError` comment block inside each walker's body, which explained the sibling filter where the sort used to be | `_numbered`'s docstring in each module, which is where the filter now lives. The `TypeError` half of it is also answered above, because it no longer describes anything in the tree |
| `git ls-files` as any corpus reader's listing | nowhere — it was the defect |
