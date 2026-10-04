# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 30f41fdc |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Count the corpus again with the build (A11, after) and report any new
question with its shapes rather than absorbing it; write `changelog.md`, the
ledger fragment with its new rows and a `Re-read ·` row for every released
row the change drifted, and `overview.md`; run `bin/evidence-check --strict
.`, `bin/survivor-check` over the range and `tests/test_no_real_identifiers.py`.

## What this phase found

**M2, after: the build newly asks none of the 25,741 pairs, and stops
asking none.** Executed by the deleted corpus probe with the build's
`hooks/`, over the same pairs phase 1 read, tree-blind as D3 counts: 356
pairs hold a switch and 47 a creation in the frozen reading, the same 356 and
47 as at `94d7b2e0`, pair for pair; candidate C fires on 0. No pair holds a
quoted or unquoted `<` or `>` inside a `checkout` or `switch` word, and the
81 pairs with an `&`- or pipe-led operator inside one hold the switch in the
frozen segment, as at the base. So the prompt budget the change spends on
the recorded runs is zero, and §*Known limits* carries both zeros.

**W2: one released row was false, six were re-read.** `bin/evidence-check
--strict .` named 15 drifted coordinates across `seal/releases/0.16.0.md`,
`0.18.0.md` and `0.18.1.md`. `--reverify --into` wrote seven `Re-read ·`
rows; each cited row was read against the change:

- M2 (0.16.0), K5, K6, K7, N1 and `Corrected · G17` (0.18.0) still hold:
  what drifted them is the new paragraph, the new limit and `_bare_words`'s
  and `switch_kind`'s bodies, and none of them claims the words those read.
- G1 (0.18.1) does not: it states the sentence that named `-b` or `-B` as a
  `checkout`'s only creating options. Its row became `Corrected · G1`, with
  the rewritten sentence as its claim.

D1–D4 are this item's own claims. The records arm then refused one record
name, `_names_anew` in `plan.md`'s alternatives (a function of round 3's · NAME NOT IN TREE
fence, which never merged), and that line now says `NAME NOT IN TREE`.
`--strict` exits 0: 5,281 ok, nothing drifted, broken or malformed.

**`survivor-check` over `94d7b2e0..a803c4ed` named one place**: another work
item's `plan.md` describing `hooks/cmdline.py#unglued`, which this branch did
not touch and which still behaves as that sentence says. It is in
`survivors.md` with the quote and the grounds, and the run with the
exemption excuses it.

`tests/test_no_real_identifiers.py` passed. The probes, the scratch
repositories, the copy of `94d7b2e0`'s hooks and the corpus extract under the
session scratchpad were deleted after this record was written; nothing from
the corpus was committed except the counts.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probes lived outside it | none |
