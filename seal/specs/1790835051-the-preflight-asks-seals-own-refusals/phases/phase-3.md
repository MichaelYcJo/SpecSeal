# 1790835051-the-preflight-asks-seals-own-refusals — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 6c690d51 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The documents: the preflight paragraph in `skills/code-review/orchestration.md`;
the `Grounds` cell in `skills/implement/orchestration.md`; one sentence each in
`skills/verify/SKILL.md` and `templates/config.md`; the appended sentence in
`seal/specs/1790815611-…/changelog.md`. Pins for S11 in
`tests/test_broad_gate_rule.py`, red first against the unedited documents. The
order line in `skills/implement/orchestration.md` stays untouched.

## What this phase found

**The frame's list of documents is the whole list.** Every document that
says what the preflight runs was enumerated by searching for `preflight`
across `README.md`, `README.ko.md`, `CONTRIBUTING.md`, `docs/`, `agents/`,
every `skills/*/SKILL.md` and `templates/`. Only the four the spec names carry
the sentence, so neither README moves and `agents/sealer.md` stays untouched.
The sentences inside `broad_gate.py` that said the same thing were phase 2's.

**The paragraph's last sentence stays true and says more.** *A session that
skips the preflight loses only time* still holds, because the sealer's run
still raises every refusal the preflight asks. It now says the sealer asks
`seal`'s refusals too, and that it refuses them after its suite. The two acts
a `seal` refusal sends a reader to are written in the paragraph: the
verifying round where `Fixes checked by` reads `nobody`, and the open finding
where `Pass` is unchecked. Both are `seal`'s own sentences.

**#638's changelog sentence went in at the end of the paragraph it
answers**, not at the end of the file. The file ends under `### Changed`,
and the sentence it answers is in `### Added`. It is dated and names #702 as
the entry after it, so the release section reads the gap and its closing in
order.

**Red, as shown.** All three pins were red against the unedited documents.
The third holds two documents, so `skills/verify/SKILL.md` was edited first
and the case run again: it went red on the template alone. After the commit,
three mutations ran through `bin/mutation-check`, each red: the verifying
round dropped from the paragraph, the ask dropped from the acts-table
grounds, and `seal`'s refusals dropped from the template's sentence.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
