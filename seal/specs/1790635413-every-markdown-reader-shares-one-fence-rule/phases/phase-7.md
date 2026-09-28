# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 56a47561 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 7: `fence_opener`'s docstring — the paragraph naming "the
readers #584 names" is rewritten as the readers that stay apart, each with
its reason from `spec.md`. The ledger fragment carries this work's claims,
and `changelog.md` its entry. Verified by `git grep` for `#584` in
`unverified_check.py` and the files above returning only what this phase
meant to leave.

## What this phase found

- **The docstring is two lists now**: the readers that ask the rule, with
  the readers #584 brought over named as a group, and the readers that keep
  a rule of their own, each with the reason `spec.md` §*Out of scope* gives.
  The closing sentence says a new reader belongs in one of the two, where it
  used to say *on this list*.
- **The `git grep` check**: over `unverified_check.py`, the eight code files
  the phases edited, `evidence_check.py` and `skills/evidence-check/SKILL.md`,
  every `#584` left is a provenance note on a change this work made, except
  `evidence_check.py`'s comment that `fence_opener`'s docstring "names the
  readers #584 has not brought over yet". That one is left for work item C,
  as `questions.md` D4 decided, and it still resolves: the docstring names
  those readers.
- **One sentence outside the plan was false after the work.**
  `skills/evidence-check/SKILL.md` said "Some readers elsewhere in the plugin
  still keep a rule of their own, and #584 tracks them." It now names the
  readers that ask the rule and sends the reader to the docstring for those
  that stay apart (contract §12).
- **`survivor-check` over the whole range** reported one place, a test
  docstring whose sentence about closing fences is still true under the
  shared rule; `survivors.md` records it with the quote.
- **The changelog entry says what a consumer can see change**: a
  `seal/config.md` row inside a closed comment stops being read.
- **`overview.md`** is the closing memo, with the divergences recorded as
  each phase met them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence in `fence_opener`'s docstring that the other readers #584 names still keep their own and #584 is where each is answered | the same docstring's list of readers that keep a rule of their own, each with its reason |
| `skills/evidence-check/SKILL.md`'s "#584 tracks them" | `fence_opener`'s docstring, which that sentence now points at |
