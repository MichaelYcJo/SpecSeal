# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 92b505d7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

M3's after-counts over both corpus cuts (A12), each moved pair reported with
its shape and any pair outside the class or quieter reported as a defect;
`changelog.md` for what phases 2 and 3 built; the ledger fragment with the new
rows and a `Re-read ·` row for every released row the change drifts, written
with `evidence-check --reverify --into seal/ledger/<id>.md --checked
2026-10-05` (W1); `overview.md`. Checked by `bin/evidence-check --strict .`,
`bin/survivor-check` over the range and `tests/test_no_real_identifiers.py`.

## What this phase found

**M3 after: nothing moved outside the class, and nothing went quieter.**
Executed by the same deleted probe as phase 1, replaying each pair through a
copy of `hooks/` taken from the branch at `0b22544d` and comparing with
`a3aa139a`'s replay pair by pair:

| Reader | Cut 1 (25,741 pairs) | Cut 2 (36,199 pairs) |
|---|---|---|
| `checkout` segments whose verdict moved (#790) | 0 of 403 | 0 of 647 |
| of them, quieter | 0 | 0 |
| pairs whose `[worktree-ok]` read moved (#780) | 2, both read before and not after | 2, the same two |
| pairs whose `[shared-tree-ok]` read moved | 0 | 0 |
| pairs whose token read went from no to yes | 0 | 0 |

Both moved token reads are the class: in one the token sits in a commit
message passed through a quoted here-document, in the other in a Python edit
script fed to `python3 -`. Neither command creates a worktree or switches a
branch, by the frozen walk or by candidate C, so neither reaches a row that
reads the token, and the guard's answer on both pairs is unchanged. The
#790 half moved no pair: no recorded `checkout` names a message search or a
merge-base shorthand, and no recorded name resolves only through a remote
other than `origin`. The guess half is read against each pair's directory as
it stands on the build day, and 172 of cut 1's 403 segments and 363 of cut 2's
647 name a directory that is gone, where both copies read no ref; those are
counted as unchanged, not as measured.

So the prompt budget, over the recorded runs: no new question for either
change.

**The replay round 1's fix pass ran, and what it can and cannot show** (added
by round 2's fix pass, ❓ of round 2). The fix pass re-ran the comparison
through `main()` rather than `classify`, with this selection rule: from the
same transcripts, every distinct command and directory pair whose command
text contains the substring `checkout`, `[worktree-ok]` or `[shared-tree-ok]`;
cut 1 is those among the Bash uses before 2026-10-03T11:06:22+09:00 (581
pairs), cut 2 those among every use recorded when the fix pass extracted the
corpus on 2026-10-05 (1,044 pairs of 36,937). Each pair was run through
`a3aa139a`'s `hooks/` and through the fix pass's, with the session count
stubbed to two states (no other session, detection reliable; no other
session, detection unusable), the choice marker and the consent record
stubbed so nothing was written, and the decisions compared: none moved, none
went quieter. The probe was deleted, so the counts are this record's word
and not re-checkable. It is a no-regression check over recorded traffic and
nothing more: no recorded command holds a `checkout` that only #790's lookups
read, so the replay never reached the reordering in `main` that round 1's
🟡 3 added. The evidence for that reordering is
`test_a_newly_read_checkout_in_front_takes_no_question_away`,
`test_the_first_newly_read_checkout_is_the_one_judged` and the 31 commands
round 2's reviewer ran through `main()` at three versions.

**W1: two released claims no longer held, six drifted and still hold.**
`bin/evidence-check --strict .` reported 18 drifted coordinates across
`seal/releases/0.15.6.md`, `0.16.0.md`, `0.18.0.md`, `0.18.1.md` and
`0.18.2.md`. Each citing row was read against the change before anything was
written:

- **D4** (0.18.2) said the policy names the one rule read past the base; it
  now names two. `Corrected · D4` carries the new claim.
- **K7** (0.18.0) said the policy says the guard asks `hooks/cmdline.py` one
  question; the consent read now has it take bodies out too, and §*Which
  tree*'s sentence was amended to say so (`3243edd1`). `Corrected · K7`
  carries it.
- **W8** (0.15.6), `_judgment_text`'s docstring; **M2** (0.16.0) and **K6**
  (0.18.0), the accepted cost and the unplaceable-tree limit; **Corrected
  G17** (0.18.0), the Windows limits; **Corrected G1** (0.18.2), the
  `switch_kind` sentence and `KINDS`, whose only change is the comment round 2
  asked for; **D1** (0.18.2), `classify` reading through `read_switch_words`.
  Each still holds, and `evidence-check --reverify --into` wrote its
  `Re-read ·` row. G1 (0.18.1) is superseded by `Corrected · G1` and takes no
  row of its own.

After the two corrections and the reverify, `bin/evidence-check --strict .`
exits 0: 5,634 ok, 0 drifted, 0 broken.

**A release-hygiene check refused the first policy sentence.** It named the
milestone by its version, and `tests/test_release_hygiene.py` refuses a loaded
file naming a version not yet released; the sentence now names "the milestone
of the release that ships it" (`3243edd1`, `overview.md`).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probes, their results, the scratch repositories and the two copies of `hooks/` lived in the session scratchpad and are deleted | none |
