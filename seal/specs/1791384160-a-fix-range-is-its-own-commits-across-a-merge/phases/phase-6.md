# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 89c55c33 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 6, the texts. Rewrite `docs/the-record-layout.md` §*A range
owns the commits that descend from its start* to hold:

- the owner sentence of `spec.md` §*In*;
- what the test does not read;
- the two limits;
- the count-vs-surface sentence;
- the shape module, named as where a shape is answered;
- no example by shape or by time.

Replace the fragment section's CI sentence with the input statement. Make the
docstrings of `own_commits`, `fragment_left_behind`, `fix_pass_units` and
`touched`, `skills/code-review/orchestration.md` §*And name the fix surface,
in the same record*, and `docs/round-record-spec.md` §*A fix of a fix* and
§*The fix range* say *the range's own commits* and name the section, defining
nothing. Replace rule 17's sentence. Add the guard case, with its word list
settled against the rewritten texts (Q6), and see it red with round 3's 🟡 2
sentence pasted into the home (S14, S16).

## What this phase found

**The guard's list is the proposed one plus one pattern** (Q6). The nine
words and phrases the frame proposed are all on it. Round 1's false sentence
used none of them: it said a merged-in commit "descends from `a` never". So
the list also holds `descends? from \S+ never`, and
`test_the_list_catches_the_sentences_the_rounds_found` asserts that each of
the three rounds' false sentences, as it stood in the tree, trips the list.
Nothing was removed from the list. Two sentences that needed a listed word
were reworded:

- the home's account of #860 and #805 now says "another work item's" where
  it said "a sibling's";
- `fragment_left_behind`'s silent-state table now says round 1's target is
  "gone from this clone once its branch merged", where it said "squashed
  away".

**What the guard reads.** It reads the home's section whole, the four
docstrings whole, and in four files (the orchestration, the round-record
spec, `chain_check.py` and `round_record.py`) every sentence holding the
link `§*A range owns the commits that descend from its start*`. It does not
read the fragment section: that section's rule paragraph needs "a
sibling's squash" to say which integration commit owes a fragment, and that
is no claim about ownership. The fragment section's input sentence was
written to the list anyway.

*Corrected after round 4 (⬜ 3, ⬜ 4):* reading the four docstrings whole made
the guard refuse a true row, and "gone from this clone once its branch
merged" was a false rewording of it, because a merge commit keeps the target.
The row says "squashed away" again. The guard now reads the home's section
and the linking sentences only, and each of the four docstrings reaches it
through its own linking sentence. Its docstring now says it is a word list,
which a shape stated in other words passes.

**Seen red (§15), each by `bin/mutation-check`, executed:**

- round 3's 🟡 2 sentence pasted back into the home turns the home case red;
- "a sibling's units" pasted into `touched`'s docstring turns that case red;
- "a squash on the base" pasted into the orchestration's linking sentence
  turns the linking case red;
- rule 17's owner sentence with "exactly" deleted turns rule 17 red.

**`own_commits`' docstring now names the shape module and the git command,
and nothing else.** "A start that does not reach its end gives `[]`" stays,
because it is what git returns and a caller reads it. It says nothing about
the shape of a history.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| every example by shape or by time in the home and its carriers | `tests/test_a_range_owns_what_git_lists_for_it.py`, one case per history (phase 5) |
| the fragment section's claim that CI reads what a branch reads | the input statement in the same section, and S17's case |
| rule 17's sentence *owns the non-merge commits that descend from `a`* | the owner sentence the code runs |
