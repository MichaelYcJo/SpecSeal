# 1790119502-four-shipped-work-items-wait-unfolded — review round 3

| Field | Value |
|---|---|
| Target SHA | c75f6a7 |
| Written late | no |
| Ran by | warden on claude-opus-5-5 |
| PR | #516 |
| Broad gate | 6b45fce against b0cbd34 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 at `c75f6a7`, the verifying round that ends the run: it reads round 2's fix range `d6ecf3b..dc222e0` and the C4 and S9 re-verifies. Under the reopening rule, anything new is a deferral candidate. The orchestrator re-ran the narrow slice and `evidence-check --strict` at the target before the spawn: 95 passed, 1468 ok.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule gave all three acts to the tag push | `docs/branch-and-release.md:43-73` | answered | carried from round 2; the one sentence the range changed there is 7 |
| 2 | 🟡 Folded rules (a) and (b) gave opposite answers, and Q4 lost its home | `docs/the-evidence-ledger.md:173-202` | answered | carried from round 2; the range corrected only this item's records to match it |
| 3 | ⬜ The acts-table sentence omitted the `###` rows | `docs/the-agent-set.md:96-105` | answered | carried from round 2; not in the range |
| 4 | ⬜ The L6 paragraph omitted `CAPPED_EXIT`'s lag and the carriers | `docs/review-chain-spec.md:299-316` | answered | carried from round 2; its carrier sentence is 5 |
| 5 | 🟡 The L6 paragraph's carrier list misses `templates/sdd-round.md`, and its claim that each carrier points at the ladder is false | `docs/review-chain-spec.md:309-317` | answered | `8b126bc` holds. Executed: whitespace-collapsed search over tracked files finds prose carriers only in the four kinds named; both comma spellings match; no false member. Read: each site's pointer |
| 6 | ⬜ The checklist box says the note job fails in one direction only | `docs/release-checklist.md:247-251` | answered | `d2139d8` holds. Read: `publish_release_note.py#main`, `#run`, `#release_exists`, `#title_from`, and the workflow's `v*` trigger |
| 7 | ⬜ The headline says two pushes fire all three acts | `docs/branch-and-release.md:50` | answered | `c26bfd4` holds. Read: both workflow triggers and the directory bullet |
| 🟢 | Round 2's correction: rule (b), the pin citation and the carrier count in this item's records | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/` | confirmed | Read against `docs/the-evidence-ledger.md` §*The fold* and G2's replacement note; grep for a four-carrier count outside round records finds none |
| 🟢 | C4's re-verify preserves the claim | `seal/ledger.md` C4 | confirmed | Read: only the L6 paragraph changed under the anchor. Executed: `evidence-check --strict` 0 drifted; `test_the_rules_have_one_owner.py` green |
| 🟢 | S9's re-verify preserves the claim | `seal/ledger.md` S9 | confirmed | Read: only the box's failure sentence changed under §6. Executed: `grep -c "on the tag"` returns 0 |
| ⬜ | The release-note script's module docstring and its A3 case docstring still name fewer failure directions than the corrected box | `.github/scripts/publish_release_note.py` module docstring; `tests/test_a_release_publishes_its_note.py:188` | deferred round-3.md | new this round and outside the fix range; rung 4, see Deferred |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `./bin/evidence-check --strict .` | exit 0 · 1468 ok · 0 drifted · 0 broken |
| `bin/test -q` over nine modules pinning the edited documents and the release-note job | exit 0 · 189 passed, 1 skipped (`test_the_reopening_is_one.py:564`, a release branch not fetched in the clone) |
| whitespace-collapsed search for *or becomes an issue* over `git ls-files` | prose carriers in `docs/` (2 files), `agents/smith.md`, `skills/code-review/orchestration.md` (3 sites), `templates/sdd-round.md` (2 sites); every other hit is a record, a runtime string or a test pin |
| `grep -c "on the tag" docs/release-checklist.md` | 0 |
| line width over the three edited documents | no line the range wrote exceeds 88 |
| broad gate — full suite, lint, typecheck | not yet. Not this round's to run. Nothing is left open, so the sealer's spawn is now due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/branch-and-release.md:43-73` | round 1's 1 — fixed |
| round-1 | `docs/the-evidence-ledger.md:173-195` | round 1's 2 — fixed |
| round-1 | `docs/the-agent-set.md:96-104` | round 1's 3 — fixed |
| round-1 | `docs/review-chain-spec.md:299-309` | round 1's 4 — fixed |
| round-1 | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/` | round 1's ⬜ — correction |
| round-1 | `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | `tests/` | round 1's 🟢 — confirmed |
| round-1 | tree | round 1's 🟢 — confirmed |
| round-1 | `docs/` | round 1's 🟢 — confirmed |
| round-1 | `docs/`, `tests/` | round 1's 🟢 — confirmed |
| round-1 | `spec.md` G2 | round 1's ❓ — out of verified scope |
| round-2 | `docs/the-evidence-ledger.md:173-202` | round 2's 2 — answered |
| round-2 | `docs/the-agent-set.md:96-105` | round 2's 3 — answered |
| round-2 | `docs/review-chain-spec.md:299-316` | round 2's 4 — answered |
| round-2 | `docs/review-chain-spec.md:309-316` | round 2's 5 — fixed |
| round-2 | `docs/release-checklist.md:247-249` | round 2's 6 — fixed |
| round-2 | `docs/branch-and-release.md:44-53` | round 2's 7 — fixed |
| round-2 | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/`, `seal/ledger.md` C4 | round 2's ⬜ — correction |
| round-2 | `tests/test_the_release_tail_does_not_end_at_the_tag.py` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger.md` C4 | round 2's 🟢 — confirmed |
| round-2 | this item's records | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The release-note script's docstrings name fewer failure directions than the corrected checklist box | round-3.md, and the pull request body | nobody has agreed to act on it — rung 4 |
