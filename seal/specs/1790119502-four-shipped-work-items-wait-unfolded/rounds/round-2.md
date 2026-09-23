# 1790119502-four-shipped-work-items-wait-unfolded — review round 2

| Field | Value |
|---|---|
| Target SHA | 7660a34 |
| Written late | no |
| Ran by | warden on claude-opus-5-5 |
| PR | #516 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `d6ecf3bf62db2e0e73b6579063a9c1c804b7628b..dc222e015f0f891153f83f2fdf8ff2dfbcf1dbb8`, 5 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 5 (the L6 paragraph's carrier list and its "each points at the ladder" claim are both false) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 at `7660a34`, the verifying round over round 1's fix range `3bbc219..96caaea` and its two new units. The orchestrator verified finding 5 by a whitespace-collapsed search of the prose trees: the phrase stands in `templates/sdd-round.md`, which the L6 paragraph's list omits. The fix is to name the phrase to search by rather than a count, since a count is the enumeration that goes stale.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule gave all three acts to the tag push | `docs/branch-and-release.md:43-73` | answered | fix is round 1's (`71c33d1`); verified against both workflows and `publish_release_note.py#title_line_re`; the new case goes red against `d0282bf`'s text |
| 2 | 🟡 Folded rules (a) and (b) gave opposite answers, and Q4 lost its home | `docs/the-evidence-ledger.md:173-202` | answered | fix is round 1's (`4ee07f9`); `seal/ledger.md:78`; #517 body and design comment |
| 3 | ⬜ The acts-table sentence omitted the `###` rows | `docs/the-agent-set.md:96-105` | answered | fix is round 1's (`e2ec58e`) |
| 4 | ⬜ The L6 paragraph omitted `CAPPED_EXIT`'s lag and the carriers | `docs/review-chain-spec.md:299-316` | answered | fix is round 1's (`b6544f6`); the carrier sentence it added is finding 5 |
| 5 | 🟡 The L6 paragraph's carrier list misses `templates/sdd-round.md`, and its claim that each carrier points at the ladder is false | `docs/review-chain-spec.md:309-316` | **fixed** `8b126bc` | fixed at 8b126bc; Executed: whitespace-collapsed search for the phrase; Read each site |
| 6 | ⬜ The checklist box says the note job fails in one direction only | `docs/release-checklist.md:247-249` | **fixed** `d2139d8` | fixed at d2139d8; Read `publish_release_note.py#main`; drifts S9 if edited |
| 7 | ⬜ The headline says two pushes fire all three acts | `docs/branch-and-release.md:44-53` | **fixed** `c26bfd4` | fixed at c26bfd4; Read |
| ⬜ | This item's records: `spec.md`'s `1790076070` destination row and `phases/phase-3.md:52-54` still state rule (b) as "REMOVED decides each"; `spec.md:33,208` still describe the pin; `overview.md:44` and ledger row C4's note carry the "four carriers" count | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/`, `seal/ledger.md` C4 | correction | Read |
| 🟢 | New units pin the right facts and go red for the right reason | `tests/test_the_release_tail_does_not_end_at_the_tag.py` | confirmed | Executed: exit 1 against `d0282bf`'s text, exit 0 at `7660a34` |
| 🟢 | C4's re-verify preserves the claim | `seal/ledger.md` C4 | confirmed | Executed: `evidence-check --strict .` 1468 ok |
| 🟢 | `96caaea` and `36813ff` corrections match the code and G2's replacement | this item's records | confirmed | Read |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over seven modules pinning the edited documents | exit 0 · 169 passed |
| the label-acts case against `d0282bf`'s `docs/branch-and-release.md` | exit 1 · the headline attributes every act to the tag push |
| the same case at `7660a34` | exit 0 |
| `./bin/evidence-check --strict .` | exit 0 · 1468 ok · 0 drifted · 0 broken |
| whitespace-collapsed search for the depth-exit phrase | the phrase stands in `templates/sdd-round.md`, absent from the list |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/settle/SKILL.md` says nothing in `seal/ledger.md` moves | a comment on #511, round 1 | the repository owner |
