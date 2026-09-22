# the release tail is three acts no document names — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing".

Fourteen survivors, in five groups, and none of them a defect. The cause is
concentrated: **this range removes `seal/ledger.md`'s R2**, a row whose Notes
cell argued the whole `size:` prefix case in about 700 words. The check reads
every sentence of a removed row as wording this range corrected, so every
place that ever restated that argument now matches it.

But R2 was removed for one conjunct of its CLAIM — *and nothing reads it* —
and not because its Notes went wrong. The prefix argument those Notes made is
still true, still in the live document, and untouched by this work. So the
echoes are echoes of an argument that still stands.

The written-out rows rather than a `| Range | Grounds |` row, deliberately.
That escape is for a range that deletes a shipped SECTION, where the count
runs to three figures; fourteen judgments are payable, and each one anchors on
its own sentence so the exemption expires when that sentence changes. A range
row would expire on nothing. -->

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/phases/phase-3.md` | `So the section states no second exception, and` | An earlier work item's phase record, stating what was true at its own SHA. `tests/test_a_release_is_sized_by_a_criterion.py` keeps `seal/specs/` out of its own sweep for exactly this reason, in as many words: *an earlier work item's records state what was true at their own SHA and are not rewritten.* What it echoes is R2's Notes, and the claim it restates — that the section needs no exception because `size:` is a topic — is still true after this range |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/phases/phase-3.md` | `only the **value** is spent when the release ships` | Same record, same rule. The subject/value split is what this range leaves standing: the live document still says the subject sits in the prefix and the verdict in the value. Nothing here made it false — what became false is that nothing reads the label |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/phases/phase-3.md` | `That is a divergence from` | Same record. It notes that work item's own divergence from its own `spec.md`, which is a fact about a decision taken then. This range has no opinion on it |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/phases/phase-3.md` | `asks a label to name a concern that outlives a schedule` | Same record. The sentence is a quotation of the live section's own rule, which this range does not touch |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/changelog.md` | `The prefix is what keeps it inside the rule the same section opens with` | That work item's changelog fragment, already gathered into the released `## 0.11.1` section. A shipped entry is a record of a moment and is not rewritten by a later branch; rewriting one would falsify the released section it was gathered into |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/questions.md` | `gives the milestone field to *when* and a label to a concern that outlives a schedule` | That work item's `questions.md`, inside a closed ✅ answer recording what the repository owner decided on 2026-09-12 and why. The reasoning it cites is the live section's, unchanged by this range, and editing an answered row would misreport what was decided |
| `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/overview.md` | `is still named as the standing precedent for a label that is not a topic` | That work item's closing memo, in a divergence row explaining why it wrote no exception into the section. Still accurate: `flow-measurement` is still the one label there that is not a topic, and this range adds no exception either |
| `CHANGELOG.md` | `The prefix is what keeps it inside the rule the same section opens with` | The released `## 0.11.1` entry. `CHANGELOG.md` is append-only by release and a shipped entry describes what that release shipped; the prefix argument it describes is still the live rule |
| `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-1.md` | `by its private name is deliberate and is commented where it happens` | An earlier work item's phase record, describing `label_merged_on_release_branch.py`'s docstring as it stood at that SHA. This range moved the reader to `close_issues_on_release.py` and rewrote that docstring into a delegation, so the record now describes a past state — which is what a phase record is for. `phases/phase-4.md` and ledger row T3 carry the move and why |
| `docs/issues-and-milestones.md` | `So the subject sits in the prefix and the verdict in the value, which is the shape` | **A live sentence this range deliberately left alone, because it is still true.** It matches only because R2's Notes paraphrased it and R2 was removed. What this range falsified is *nothing reads this label*, which is a different sentence three paragraphs down and was reworded in the same commit as the case pinning it |
| `.github/scripts/close_issues_on_release.py` | `A number that names nothing reaches this from two directions` | The docstring of `_issue_api`, in the module that OWNS the 404-tolerant read. The wording this range removed is the SIBLING's restatement of the same fact, deleted when its `issue_labels` became a delegation. This is the original and it is now the only copy, which is the direction the change was in |
| `.github/scripts/close_issues_on_release.py` | `Neither is a reason to fail a release` | Same docstring, same reason. Nothing about how a missing number is treated changed here |
| `tests/test_a_merged_ticket_says_so_on_the_tracker.py` | `A typo in a merged body is input, not a failure` | The case that pins the behaviour those docstrings describe, re-run green under this range and a control on the reader's move. It states the fact because it tests it |
| `.github/scripts/label_merged_on_release_branch.py` | `for issue, source in sorted(wanted.items()): carried, exists = issue_labels(repo, issue)` | Not wording at all: the two scripts have always walked the same `{issue: the pull request that claimed it}` map with the same skip-and-continue shape, and the check is matching structural phrases. This range edited the closing script's loop to take a spent label off; the signal's loop is untouched and correct, and making them differ to quiet a report would be the opposite of what this range did everywhere else |

<!-- Round 1's fix pass adds the four below. All of them echo one removed
sentence: the assertion message in `tests/test_release_hygiene.py` that
finding 6 replaced when the two flag checks were bound to the call's argv.
The message was rewritten; the RULE it stated — adding a label is the
sibling's act at the squash — is unchanged and is still stated where it
belongs. -->

| `.github/scripts/close_issues_on_release.py` | `It never ADDS a label` | The canonical statement of the rule, in the docstring of the module it is about. Finding 6 rewrote an assertion MESSAGE that paraphrased this docstring; the docstring is the original and is still true — that script still adds no label, which is what the reworked assertion now checks against the call's own argv rather than against the whole file |
| `tests/test_release_hygiene.py` | `at the squash rather than at the close), and a second writer of labels is how two scripts come to disagree` | The docstring of the very case whose message finding 6 replaced, a few lines above it. The reasoning did not move out of the case — the docstring explains why the property is idempotency rather than the verb, and the new message says what the one edit may carry. Deleting the docstring to silence a report about the message would remove the explanation and keep the check |
| `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md` | `refuses `--add-label` outright — adding a label is the sibling's` | This work item's own phase 4 record, describing what that phase did at its own commit. It is accurate about that moment, and the fix pass's own change to the same case is recorded in round 1's fix table rather than by rewriting the phase record |
| `tests/test_a_merged_ticket_says_so_on_the_tracker.py` | `assert '"--add-label",' in folded, "the script stopped adding"` | The opposite claim about the other script, matched on code shape. `label_merged_on_release_branch.py` is the script that DOES add the label, and this is the positive assertion that it still does. The two cases are a matched pair — one forbids the flag, one requires it — and they read alike because they are about the same flag in the two modules that must disagree about it |

<!-- Round 2's fix pass adds the two below. Both are the folded-substring
reader this range removed from ONE case, still standing in two other cases
about two other scripts. They are correct where they are in the sense that
matters here — neither script changed, so neither case's verdict moved — and
converting them is a change to two modules this work item has no finding
against, by a fix pass that may not add mechanism. The CLASS is disclosed as
a row of `seal/follow-up.md` rather than silently exempted. -->

| `tests/test_a_release_cannot_ship_an_untrue_milestone.py` | `for forbidden in ("edit", "close", "create", "delete", "comment", "reopen")` | The same forbidden-verb list, folded, over `release_completeness_check.py` — a different script, which this range does not touch, in a case this work item has no finding against. What round 2 proved is that a fold does not survive a comment between the argv's words, so this reader has the weakness the one over `close_issues_on_release.py` had; the class is a `seal/follow-up.md` row with the owner named. Converting it here would rewrite an unrelated module's check on a fix pass |
| `tests/test_a_merged_ticket_says_so_on_the_tracker.py` | `release-branch merge closes it for something nobody has received` | The same reader over `label_merged_on_release_branch.py`, and the same judgment. This one also asserts the POSITIVE — that the script still creates the label and still adds it — which is the direction a fold cannot silently pass: a missing string fails the case rather than quietly satisfying it. Only the forbidden half carries the weakness |
