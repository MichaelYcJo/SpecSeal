- **A second fold for one version joins its section, and the ledger heads
  each version once (issue #540).** `fold_ledger.py --version X.Y.Z` run
  again for a version `seal/ledger.md` already heads used to write a second
  `## X.Y.Z` heading below everything — the ordinary shape when a release
  pull request goes red and a fragment lands after the preparation commit,
  and `seal/ledger.md` carried a second `## 0.9.3` from exactly that through
  seventeen ledger sections (`0.9.4` to `0.15.0`) while the ticket said
  nobody had run the fold twice. The second
  heading is removed, the fold now appends the late work items into the
  section the ledger already heads and keeps that section's first date over
  `--date` and today, `--dry-run` prints the heading it joins, and
  `fold_ledger.py --check` refuses a ledger that heads a version twice,
  naming both lines; `tests/test_release_hygiene.py` refuses the same on
  every pull request, as it already did for `CHANGELOG.md`. The release
  checklist says the fold answers as the gather does.
- **The comment every `broad-gate.md` is written with states the rule the
  writer follows (issue #542).** The comment `round-record seal` writes into
  a `straight to the PR` work item's `broad-gate.md`, and `kept_broad_gate`'s
  docstring, described the `Broad gate` cell as it stood before 0.15.0's
  same-run fix — *a run taken again is written in front, and the earlier one
  stays behind it*; *the count of runs*. Both now say what the code does: a
  run at a new commit, or at this one against another base, is written in
  front and the earlier stays behind it as `earlier run`; a run the newest
  entry already records — the same commit against the same base — replaces
  it, and the count of entries is the count of distinct comparisons. A case
  reads the written file for the sentence, so a third rewording cannot reach
  every `broad-gate.md` unpinned, and the two further documents that stated
  the replaced rule — the handoff protocol's `Broad gate` row and the
  orchestration skill's sealer paragraph — say the same in one clause each.
- **A finding whose coordinates sit at two depths is written as two findings
  (issue #366, second half).** `round-record close` keys its depth-2 refusal
  on a finding's `Location` and refuses every unit that finding's fix commit
  added in the file, so a finding with one coordinate inside a unit an
  earlier round's fixes created and another outside had its depth-1 units
  refused beside the depth-2 one. The reviewer splits it, one depth per
  finding: the sentence is one text in `agents/warden.md`,
  `skills/code-review/SKILL.md` and `docs/review-chain-spec.md`, pinned to
  each other, and `depth_two` is unchanged — its refusal already names the
  finding whose fix added the unit, which is the one to split next round.
  The three cases of the first half shipped in 0.15.0; the owner chose the
  convention over a finer check, and #366 closes.
