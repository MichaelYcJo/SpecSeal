# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — round 1's fix pass

<!-- Read by `round_record.py close`, which applies this table to
rounds/round-1.md. One row per finding round 1 left OPEN. -->

| Field | Value |
|---|---|
| Answers | round 1, target `ae2d0ac` |
| Fix commits | `62c22ca` — the whole pass, plus `<this commit>` for `survivors.md` and this table |
| Ran by | unknown — the resume message named no model for this segment; the orchestrator fills this row |

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `62c22ca`. The case's premise moved from *no committed declaration answers the fourth axis* to *every declaration that OMITS an optional row reads as unanswered on that axis*, which is the claim the row exists for. Seen red first at HEAD (1 failed, 30 passed, exit 1, naming this work item's `routing.md`), green after (31 passed, exit 0). §15 on the new assertion: with `hooks/routing.py` mutated so an absent `Planning` row reads as `framer`, the new assertion is red naming `1788177600-the-tree-that-arrives-without-its-history/routing.md`, exit 1; the parser was restored from bytes kept before the mutation, not from HEAD. **Measured, and it decided the guard's shape**: 0 of 73 declarations omit `Implementation` and 72 omit `Planning`, so the vacuity guard covers the two axes together — per axis it would be red the day it was written. **One limit, stated rather than left to be found**: because nothing omits `Implementation`, this case's `Implementation` arm is unexercised by the tree — mutating that default to `smith` leaves this case green (exit 0) and is caught by three fixture-based cases in the same module (exit 1). The guard is what will notice if `Planning` ever reaches the same state |
| 2 | fixed | `62c22ca`. The paragraph now scopes itself to the three sections #292 moved and names the order as the exception that gained the prefix. **The paste-ready text was not pasted on trust and one word of it was wrong**: it read *The order above is the exception*, and the order section is at line 31, below the paragraph at line 23. It reads *The order below* |
| 3 | deferred the repository owner | Issue #351 sends two standing rules to `docs/issues-and-milestones.md` and `spec.md` ends the second one; whether the ticket's `Done when` may be narrowed that way is the owner's call and no measurement settles it. Untouched, as the resume message directed — no edit to `spec.md`, the records or the tracker |
| 4 | answered | Corrected at `62c22ca`. `overview.md`'s `· verified` line names thirteen modules with a count each — 45 · 32 · 23 · 43 · 13 · 11 · 2 · 86 · 9 · 58 · 29 · 31 · 65 — and 447 passed over the thirteen together, exit 0, each also run on its own. The `## Not verified` row stops saying *nine modules* and points at that list. **Both earlier figures were real runs of unnamed sets**: the first nine of that list sum to 264 and the first eleven to 351, which is why neither could be reproduced. The replacement docstring in finding 1's case carries no count either, for the same reason — the one it replaced said *the twelve committed here* and *Seventy-two declarations* about a tree holding 73 |
| 5 | answered | Corrected at `62c22ca`. 33 becomes 32 in `overview.md` and in all three places in `survivors.md`. Measured at `62c22ca`: `every survivor is excused by a row above (32)`, exit 0, and the reported places split 29 records to 3 loaded files, so the arithmetic is 29 + 3. The `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` bullet is withdrawn and replaced by a paragraph saying what it got wrong — the place is not among the 32 (`grep -c` returns 0) and the docstring there is about pytest-xdist being installed by the workflow rather than by the virtualenv, not the deadlock the bullet described |
| 6 | answered | Corrected at `62c22ca`. R3's appended note was R1's, byte-identical, arguing an exemption count R3 does not claim. R3 now records its actual reason — its fourth coordinate re-anchored from `@08730484` to `@98c5bec1` because that test function's docstring lost the clause about the deleted checklist — and says the refusal's routes and message are untouched. Verified not identical afterwards |
| 7 | answered | Corrected at `62c22ca`. `seal/ledger.md:1646`'s first of two independent reasons named a file this branch deleted and an entry it removed. The sentence goes to the past tense and gains what #351 did to it, so the second reason is named as the one that stands. The reviewer's discriminator is the right one: this was inside the row's grounds, not an observation of a commit, which is why it differs from `:343` and `:1524` |
| 8 | answered | Corrected at `62c22ca`. *The five divergences above* becomes *six*. Phase 6's row moved up under phase 5's and the two prose paragraphs follow the completed table — the prose was moved rather than the row deleted, as directed. **The first move left a blank line between rows 5 and 6, which breaks the table exactly as the prose did**; it was caught by parsing the table back and asserting the contiguous data rows are `1 2 3 4 5 6`, which they now are |
| 9 | fixed | `62c22ca`. Three doubled `Checked` cells re-padded — measured at 3 doubled against 467 single, and 0 doubled afterwards. Three Notes cells gained a sentence break before the appended note. `docs/issues-and-milestones.md:35` and `:39`, at 56 and 48 columns inside a paragraph wrapped near 75, re-wrapped. **The class had two more instances the round did not report, both mine**: `plan.md`'s phase 1 and 2 Status cells were written `\|` + backtick with no space, by the same script that doubled the date cells. Both re-padded. The verdict is `fixed` rather than `answered` because one half of this finding is in a loaded document rather than in a record |

## What this pass did not add

No new unit and no mechanism. Finding 1 replaced the body and docstring of an
existing case; nothing new was declared, no rule, checker, template section or
walk was added, and no `phases/phase-N.md` or `plan.md` phase row was written.

One anchor drifted from the corrections and was re-verified rather than left:
`docs/issues-and-milestones.md#"## A milestone answers *when*, and takes three
shapes"`, this work item's own S3 row, because correction 9 re-wrapped a
paragraph inside that section. `@41eb5b00` → `@95e3a483`, the claim re-read
(`git grep -n "sized in work items"` still returns that one line), and the
re-anchoring written into the row's Notes — because an unrecorded re-anchoring
is what finding 6 was.

## Verification of this pass

| What was run | Result |
|---|---|
| `bin/test -q tests/test_routing_is_recorded.py` before the fix | 1 failed, 30 passed, exit 1 |
| the same, after | 31 passed, exit 0 |
| the same, with `hooks/routing.py` mutated so an absent `Planning` row reads as `framer` | exit 1, the new assertion naming an omitting declaration |
| the same, with the `Implementation` default mutated to `smith` | this case exit 0 — arm unexercised; the module exit 1 from three fixture cases |
| `bin/test -q` over the nine modules the fix touches | 340 passed, exit 0 |
| `bin/test -q` over the thirteen named in `overview.md`, together | 447 passed, exit 0 |
| `bin/test -q tests/test_waiver_decided_at_start.py` | 17 passed, exit 0 |
| `bin/evidence-check --strict .` | 1 drifted, exit 2 → re-read, `--reverify`, then 1121 ok · 0 drifted · 0 broken, exit 0 |
| `bin/unverified-check --baseline origin/release/v0.11.1 seal/specs/` | exit 0 |
| `uvx ruff check .` · `uvx ruff format --check .` | exit 0 each |
| `bin/survivor-check --range bfe8cdb..62c22ca --exempt .../survivors.md` | 5 places, exit 1 → each opened and given a row → all 5 excused, exit 0 |
| broad gate | **not run.** The `sealer`'s, once these findings close (contract §2) |
