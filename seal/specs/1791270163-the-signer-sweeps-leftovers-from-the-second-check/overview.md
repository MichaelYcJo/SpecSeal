# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this item; `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/post-review-check-2.md` (findings ⬜ 1–⬜ 4, *Paste-ready fixes*); `docs/the-pact.md` (the statement under the `1791239490` fold marker); `seal/releases/0.19.0.md` rows `Corrected · P8`, R1, R6; `templates/sdd-phase.md`, `templates/sdd-overview.md`
· evidence: `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md` — `Re-read · Corrected · P8`, `Corrected · R1`, `Re-read · R6` (with the phase 1 plants in its grounds)
· verified: executed — the plant probe before and after phase 1, the S4 case red then green, two `mutation-check` runs red and one SURVIVED then pinned, the sweep module (21 passed), the six pact-reading modules (3447 passed), `bin/evidence-check` (exit 0, 6417 ok · 0 drifted · 0 broken; records 0 drifted), the changelog dry run (exit 0); read — the docstrings against the new behaviour

## Why this work exists

The second post-review check of #830 left four leftovers open; after this work a block directly under the pact policy's statement is swept again, a glued old header is quoted as the file holds it, and the two released ledger rows that overstated the code are corrected in this item's fragment.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A fourth glued shape in the S4 loop | `spec.md` S2 names three `under` shapes; `bin/mutation-check` with `.strip()` removed from the new quote SURVIVED over three pact modules (73.1 s) | an indented `  \| Signatory \|` shape added to the same loop, `quoted` stripped; the same mutation then red | agent contract §15 and `agents/smith.md` §*Verify*: a unit this work added that stays green while broken has nothing behind it. No new `def`, so `docs/the-pact.md`'s `Enforced by:` targets do not move |
| `plan.md` §*Technical context* wrote the three released rows' coordinates as live stamps | `bin/evidence-check`'s records half read them as stamps about the tree and reported 2 DRIFTED once phases 1 and 2 moved the units, which `broad-gate --strict` turns into NOT SEALED | the sentence keeps the hashes and states them as "at hash `…`", outside the coordinate shape | the sentence describes what the released rows carry, a past state, and a stamp asserts the present one; records half then 0 drifted |
| The `Corrected · R1` claim | ⬜ 4's fence adds the stray-row exception only | it also says the line is quoted as written | phase 2 made that true, and a corrected claim that omits it would be one shape short again |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate: the full suite, the repository-wide lint and the typecheck | the sealer, once after the review rounds settle; `routing.md` was answered again as `automation` (`through the review chain`, `open the pull request`), so no segment before it runs any of the three |
| ✅ `correction-check` over the range: no correction marker dropped at a merge, and no released ledger file changed under `Ledger frozen from` | executed 2026-10-06 by smith over `a9d7b0e..944ad17`, exit 0 (no merge commit in the range; no released ledger file changed); CI runs it again at the pull request |
| `survivor-check` over the range | each review round's fix pass, over that pass's fix range (`agents/smith.md` §*Phases*, item 3); round 1's fix pass ran it over its whole fix range from `5bc0a48f`, exit 0, no removed wording still standing, and a later round's fixes take their own run |

## Not done

The `cmarkgfm` alternative for the policy span (`plan.md` §*Alternatives considered*) was not taken. The widened regex lists GFM's paragraph-interrupting blocks by hand, and `plan.md`'s *What breaks in six months* names the cost; nothing in this build made the list look too brittle to keep.

## Fed back into the spec

none — the work answered `questions.md` M1 (three rows, exit 0) and W1 (a `test_tmp_` probe), and neither changes a clause.

## Next

Phases 1–3 are committed. Nothing in `plan.md` is left. `routing.md` was answered again as `automation`, so the review rounds run and the sealer owes the broad run above once they settle.
