# survivors — 1789356180-the-two-halves-of-one-generator-refuse-each-other

<!-- `survivor-check --range e1ac870..HEAD` reported seven places still
carrying wording this range removed. ONE was a live defect and is not in this
table: `seal/ledger.md`'s R1 row claimed `anything else is refused`, which
stopped being true when a `#` cell with no digit became a row that commissions
nothing. That row's clause was corrected in place — and corrected again by
round 1's finding 6, which found the first correction true of the verdict
table and silent about the fix table — with a re-read note added,
per `CLAUDE.md`'s rule that a branch must touch the shared ledger when leaving
it alone would leave it false. The six below are reports that are correct as
reports.

Each row quotes the standing text, so the exemption stops holding the moment
that text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/overview.md` | `**A pre-existing defect in `fix_table` was found by round 2 and deferred to a rider.**` | A closing memo of a work item that shipped, describing a defect it found and deferred. It asserts a PAST state — what round 2 found and what it did about it — which is exactly the property that lets a record live beside the contract (`skills/implement/SKILL.md` §*Document layout*). The defect it names is the one this branch repaired; rewriting the memo would make it assert that round 2 found nothing |
| `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/overview.md` | `Read 2026-09-06 at `aed3ca0`, and visible in this work item's own `rounds/round-1.md`, rows 1 to 3.` | The same memo, and the sentence is a dated reading against a named commit. A reading taken on a day does not stop having been taken because the code later changed; re-dating it would falsify the one thing it records |
| `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/overview.md` | `The repair belongs at the `note` line rather than in `chain.SEPARATORS`, which is shared with the `deferred` home and with `chain_check`'s own readers` | The same memo, recording where that work item decided the repair belonged. This branch made the repair exactly there, so the sentence describes what happened rather than a claim that has gone stale. What the memo's REASON got wrong is recorded in this work item's `phases/phase-3.md` and in its ledger fragment, which is where a correction belongs |
| `tests/test_a_finding_id_is_a_bare_integer.py` | `And with eight rows and no coordinates, finding the pair is a manual scan.` | The module docstring's account of what #227 cost when it was reported. It is history, and it is still accurate history — the refusal it describes is the one that existed then. The live rule is stated in the function docstring and in `docs/review-chain-spec.md`, both of which this branch rewrote |
| `tests/test_a_finding_id_is_a_bare_integer.py` | `want = generator.RECORD_LABEL if on_record else generator.FIX_TABLE_LABEL` | Not prose. The checker matched the code fragment `on record else` against the same fragment in the case's own body, which this branch restructured — a self-match inside one edited function, not a copy that was left behind |
| `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/spec.md` | `Given a record whose verdict rows carry round-prefixed ids · When `close` runs · Then it refuses naming the format (`a bare integer`) and quoting the` | A shipped work item's acceptance scenario, and it still holds: a round-prefixed id carries digits, so `close` refuses it exactly as written — this branch added a second refusal at `new` without removing that one. `tests/test_a_hand_edited_record_still_meets_the_rule_at_close` is the case that keeps it true |

## Round 1's fix pass — `c9912a4..HEAD`

<!-- Five more, from rewriting the grounds sentence in five carriers and the
overview row beside them. ONE survivor of that range was a live stale claim and
is not in this table: `plan.md`'s *What breaks in six months* paragraph still
said the direction this fails in is a finding nobody is asked to close, which
round 1's 🔴 1 showed is one step short — `Pass` is ticked over it. That
paragraph is the approved plan's own text, so it is left standing and a dated
correction note sits under it. -->

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/changelog.md` | `The change is toward the cheaper mistake, and the documents now say so.` | This is the corrected sentence, not a leftover of the removed one. It shares two phrases with `docs/review-chain-spec.md`'s version of the same rule because both state the same trade — which is what the two documents are supposed to do |
| `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/phases/phase-1.md` | `The last row is the one that matters: the frame's 103 is low by more than half, and phase 3's acceptance re-measures it.` | Phase 1's record of what phase 1 measured, and still exactly true — the count is 210 against the frame's 103. The overview's version of the sentence was rewritten because its ROW changed, not because the fact did |
| `seal/specs/1788331011-two-roots-hold-three-lifetimes/overview.md` | `12 rows in other fragments re-verified at `a4206b0`, after phase 2's re-point 5 more re-verified` | A different work item's closing memo, matched on the phrase `one row in` and a stray `phase 3's`. Neither carries any claim this range touched |
| `seal/specs/1788331011-two-roots-hold-three-lifetimes/overview.md` | `after PR #90's CI, one row in a *What CI settled* section for the by-hand test running under `bash -c`` | The same memo and the same phrase match, on a second line. Nothing about the finding id or the `#` cell appears in it |
| `seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/spec.md` | `An absent one is written from the folder.** Every repository that has a `config.md` today has one row in it` | A shipped work item's spec, matched on `one row in` — a phrase common enough to collide with anything. It is about `config.md`, which this range does not touch |

