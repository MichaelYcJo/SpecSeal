# Survivors — the worktree guard allows a listed shape and asks the rest

This range deletes four shipped readings of the worktree guard — the option
table and its reader, the name lookups and guesses, #790's slot rule and
candidate C — with the cases and policy sentences that described them.
`survivor-check --range a9d7b0e5...HEAD` reported 105 places after phase 4,
and every one was read:

- the released ledger (`seal/releases/0.15.6.md`, `0.16.0.md`, `0.18.0.md`
  to `0.18.3.md`, `0.4.0.md`), which never changes; each row whose claim a
  removal falsified has a `Corrected ·` row in this work item's fragment;
- the records of the work items that built the readings (1790993140,
  1791019475, 1791089705, 1791119071, 1791163981), which say what was true
  when they were written;
- `hooks/cmdline.py`'s description of its own redirection reader, which
  stands, since the guard's copy of that reading is what left;
- three sentences of `docs/worktree-guard-spec.md` that stay true (the
  frozen reading's paragraph, and #686's fallback with its count);
- phrase coincidences in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
  and one docstring of `tests/test_guard_resolves_the_tree_it_judges.py`.

The places that were defects were corrected in the range: §*Creation
consent*'s #678 and #790 sentences, `walk_command`'s docstring, and two
comments of the test module.

| Range | Grounds |
|---|---|
| `a9d7b0e5...HEAD` | the deleted readings' sentences stand in the released ledger and in the records of the work items that built them, by design, and each falsified released row is corrected in this work item's fragment; the code and policy places left are true where they stand, each read in phases 3 and 4 |
| `origin/release/v0.20.0...HEAD` | the same range as CI spells it, with the same grounds. Measured from #841's squash rather than the base, it reports 147 places at `974dc542`: the 105 above, places repeating the two rows this range removed from #841's fragment (S5 and its `Re-read · D1`, whose claims went with the retired cases), and #841's own records of the sampler this range retired, records of 1790815613 and 1791128260, `seal/releases/0.15.1.md`, and `.test_durations`, whose entries for the retired cases drop no case from the Windows shards (`CONTRIBUTING.md` §*Running the checks*) and leave with the next refresh, which takes a CI run |
