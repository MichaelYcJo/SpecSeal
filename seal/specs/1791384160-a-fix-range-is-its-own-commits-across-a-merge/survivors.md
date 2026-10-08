# Survivors — a fix range is its own commits across a merge

`survivor-check --range 4e849e50..88d5fe61` named 7 places that still carry
wording this item's range removed: the first-parent walk of the fragment
notice, `walk_tip`'s starting parent and `commits_after`'s docstring. Each
place was read, and none is live text that states the retired walk. Each is
excused below, one row per place. The rows are of three kinds:

- **A released ledger row, or another work item's historic record.** A row
  under `seal/releases/` is frozen by `Ledger frozen from`; this item's
  fragment carries the `Corrected ·` row for each one #805 made false.
  `1791163983`'s `spec.md` states what that item framed for 0.18.3.
- **This item's own record of what it removes.** It has to quote the
  sentence to name it.
- **Shared wording that states nothing retired.** What `actions/checkout`
  hands a `pull_request` run is still true, and three texts say so.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.18.3.md` | prints one notice naming every first-parent, non-merge commit | a released ledger row: `seal/config.md` declares `Ledger frozen from`, so it is never edited; this item's fragment carries its `Corrected ·` row (`docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*) |
| `seal/releases/0.18.3.md` | the walk starts at the parent that descends from round 1's target | a released ledger row, frozen as above; this item's fragment carries its `Corrected ·` row |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md` | The released sentence | this item's own `spec.md`, listing under *What this removes* the two sentences the build took out; it quotes them to name them |
| `seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/spec.md` | first-parent, non-merge commits in | another work item's historic record: what #797 framed for 0.18.3, which `settle` retires with its process record; the claim's correction is this item's `Corrected ·` row |
| `README.md` | the point where this branch forked from that ref on a branch checkout | `--baseline`'s merge base, still true; it shares only the words for how CI checks a pull request out |
| `skills/verify/scripts/unverified_check.py` | In CI it is the base's tip, because a pull request is checked out as its head already merged into the base. | still true of `actions/checkout`, and about `unverified-check`'s baseline, not the fragment walk |
| `tests/test_a_fragment_left_behind_is_named.py` | the pull request's head merged into the base, the base as the FIRST parent | `ci_merge_ref`'s docstring, still true: it builds that merge, which S8's case reads |
| `seal/releases/0.18.3.md` | the branch's own merge of the base is skipped and the sibling's commits stay off the first-parent walk | a released ledger row, frozen as above; this item's fragment carries its `Corrected ·` row |
| `tests/test_a_fragment_left_behind_is_named.py` | HEAD is no merge, so the walk that read HEAD's parent order went down the base | S7's docstring, telling what the removed walk did on #805's history; true of that walk, and no claim about `own_commits` |
| `tests/test_the_range_rule_states_no_shape.py` | on a topic forked before `a` is owned once that topic has merged | the guard's own case quoting round 3's false sentence, to assert the list catches it |
| `tests/test_the_rules_have_one_owner.py` | PINS: the owner's headline sentence and each carrier naming the section; | another rule's comment in the same table; it shares only the phrase rule 17's comment also uses |
| `tests/test_the_rules_have_one_owner.py` | sentence and each carrier naming the section. | another rule's comment in the same table; it shares only the phrase rule 17's comment also uses |
| `.test_durations` | git commit -m x]": | pytest timing data; it shares two short phrases by chance |
| `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md` | a 🟢, ❓ or ⬜ row, a name with no `.py` path whatever stands beside it | this item's `Corrected · A1` row, stated in the owner's terms; it shares only short phrases with the §*A fix of a fix* sentence phase 6 shortened |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md` | Given CI's merge ref, the branch's own merge of the base, and the octopus of an unrelated head | scenario S8 of the framer's `spec.md`, which names the histories its cases build |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md` | The `fixed` guard's message changes from | the framer's `spec.md`, stating the refusal's words, which S6 pins |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md` | The `fixed` refusal's string is not under the guard | the framer's §*Reframed after round 3*, saying why the refusal's clause is true by construction |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/plan.md` | one owner sentence that is the test itself, no example in prose | the framer's alternatives table, naming the reframe this work built |
| `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/plan.md` | the notice names a sibling's squash as the item's and misses the item's fix | the framer's alternatives table, giving the failure of a rejected design |
