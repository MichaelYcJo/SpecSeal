# 1788501054-a-check-reports-clean-while-something-is-missing — phase 3

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-3.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 55ae839 |
| Ran by | specseal:smith on opus |

## What this phase was asked

Build phase 3 only: make `chain_check.py` refuse a round record whose
**adding** commit descends from a commit its own verdicts name as the fix,
behind a fifth cutoff; give `docs/review-chain-spec.md` the subsection; make
`templates/sdd-round.md` say what the check does. Each refusal seen red at a
named SHA, a case for the well-written record that must keep passing, and the
rebase caveat settled and written into the message or the spec.

Coordinates given rather than searched for: `SHA_RE:517`, `is_ancestor:937`,
`verdict_of:1135`, `FIX_WORDS:327`, `round_records:693`, `item_began:1300` —
every piece already exists, and what is missing is the question. The four
cutoff subsections at `:651`, `:681`, `:717`, `:749` and `Ran by`'s at `:779`,
which a fifth follows.

The one design point the plan settled: the refusal reads the **adding**
commit, never the last one, because a correct record is written with `open`
cells and updated to `fixed at <sha>` when the fixes land, so its last commit
legitimately descends from the fix.

The one thing the plan left to settle: whether to read the record's first
commit on the branch or accept that a rebase can turn a passing record
failing, and say so in the message either way.

## What this phase found

**The rebase question is settled by reading `<baseline>..HEAD`, and that
choice buys a second grandfathering for free.** A record that arrived before
the base has no adding commit in that range, so nothing is claimed about it —
the same *no claim* `check_round` already makes for a record the pull request
does not touch. And a rebase replays a branch's commits in order, so a record
added before its fix on the branch is still added before it afterwards: a
passing record cannot be turned failing. What a rebase does change is the SHA
the verdict cell names, which then resolves to nothing and makes no claim — so
a rebase can turn a **failing** record passing. That direction is the safe one
and it is stated in the spec rather than left to be found; closing it would
mean matching rewritten commits by patch id, a second mechanism for a case
nobody has met.

**`--diff-filter=A` is the whole check, and eleven mutations nearly missed
it.** Dropping it — reading *the oldest commit that touched the file* instead
of *the commit that added it* — survived every case in the file, including the
updated-in-place one, because a file that was added and then modified has the
same oldest-touching commit either way. The case that separates them is a base
that MOVES under a long branch: the record's own adding commit leaves the
range and the commit that updated its verdicts stays inside it, and that
commit descends from the fix because updating the verdicts is what a correct
record does. `test_a_record_added_before_the_base_and_updated_on_the_branch_passes`
is that case, and its docstring says it cannot be red at HEAD. Eleven
mutations, none surviving, after it was added.

**A fix the round did not commission had to be excluded, or the check would
fail the second round of every run.** Round N+1's record is committed after
round N's fixes by construction, and its verdict table answers round N's
findings — so a cell reading `fixed at <round N's fix>` is ordinary. The
discriminator is the record's own `Target SHA`: a fix commit that is an
ancestor of what the round reviewed was already in the tree when the round
ran, so the round cannot have commissioned it.
`test_a_fix_this_round_did_not_commission_passes` is that case, and the
mutation that drops the filter is red only on it.

**Seven identical paragraphs is a failure people scroll past.** The real
record measured for #150 names one fix commit in seven verdict cells, and the
first working version printed the whole message seven times. The failures are
grouped by the RESOLVED commit — so an abbreviation in one cell and a full
hash in another are one commit — and the single message names every row that
carries it.

**Seen red against the two real records, executed.** Both work items were
squashed into `release/v0.8.0`, so their branch commits are reachable from no
ref and live only in the object database; a `--shared` clone sees them through
the alternate. With `ORDER_FROM` patched to 0 in a copy of the checker — the
grandfathering is not what was being measured — the refusal fires on both:
`1788486395`'s `rounds/round-1.md` added by `c79988a`, descending from
`1ead0b1`, naming it across 🔴 1 and 🟡 2–7; and `1788491830`'s added by
`0516e09`, descending from `d4b3307`, across 🟡 1–5. Exit 1 for each. That is
#150's *Done when* line, and the probe was deleted after it ran.

**This branch is held to its own rule from its first round.** `ORDER_FROM` is
this work item's own second, so `round-1.md` of this chain is the first record
in the repository the refusal reads. `chain_check.py --baseline
release/v0.8.0` on this branch currently fails on `holds no round-N.md`, which
is the state before any round has run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
