# 1788789330-the-update-notice-names-the-expensive-move — review round 3

| Field | Value |
|---|---|
| Target SHA | 89333dd |
| Ran by | warden on claude-opus-5 |
| PR | 233 |
| Broad gate | passed at e82ef31 + the marker commit, after `release/v0.9.1` was merged in — 2561 passed, 2 skipped; `ruff check .` and `ruff format --check .` both exit 0 |
| Fixes checked by | nobody — the run is capped and no round follows; both corrections were applied by the orchestrator in the closing commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of `1788789330-the-update-notice-names-the-expensive-move` (ticket #134, PR #233), at target `89333dd`, base `86e140f`. The verifying round for round 2's fixes, and the last round this work item gets: rounds 1 and 2 both closed on fixes, so the record after this one ends the run whatever it finds.

The diff was `279628b..89333dd`, whose substance is `db5b9cd` and `760ac3e`. Rounds 1 and 2 were inherited rather than re-litigated.

The context was three fixes of one bug. Round 1 found the case pinned words and the fix rewrote the case; round 2 found the rewrite pinned words one level down and the fix pinned by position plus a four-word adversative list; the orchestrator's own re-run then found a fourth mutation alive against that — `unmeasured, yet it is picked up`, the negation moved to the near side of the adversative and `yet` absent from the list, measured at `e678c47` as `18 passed` with the notice telling a user the reload picks up the new install. The 3+ Fix Rule was invoked at that point and the shape was changed rather than extended: `760ac3e` deletes four predicates and pins `notice()`'s whole output as an exact string, keeping `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` beside it.

That decision was the one thing in the branch nobody had reviewed, and it is what this round was pointed at. Does the exact pin hold the guarantee — and what does it NOT catch? Specifically: a person who edits the notice and updates the expected string in the same commit passes both cases unless the docstring case independently stops them, and that claim was to be tested by mutating the notice AND the golden string together, the way a careless editor actually would. Was deleting the four predicates a loss — enumerate what each asserted and say for each whether the exact pin subsumes it. Is the trade-off stated honestly in the case's docstring, and does the message a future editor sees tell them what to do. Do the two `NAME NOT IN TREE` markers exempt only their own lines, and is there a third site naming a now-deleted local. And does anything else in the tree still carry a distance or a count about that pair, after `130 lines above` was removed rather than corrected.

The bound was stated plainly: an unfounded finding here does not merely cost a comment, it spends the item's last round, and a round that opens nothing needing a fix does not consume the cap.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, and no finding carrying two rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The exact pin's docstring and the ledger row say the docstring case is a second net against a careless golden-string update; measured, an added overclaim and a `yet`-flipped gap both pass both cases with the golden brought along | `tests/test_version_check.py:101` | **fixed** `8a31d08` | fixed at 8a31d08 — ``. The docstring at `tests/test_version_check.py` and row S1·S2·S3 of `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` both said the two cases hold together against a careless golden-string update. The round measured that they do not: with the golden brought along in the same edit, an added overclaim, `unmeasured, yet it is picked up`, the restart named first, and the `measured` and `skill bodies` labels dropped all pass at `18 passed`. Both sentences now say what the pair actually holds — the scope qualifier, and nothing else — and name the message as an instruction to a person rather than a check. The row's hash over the edited case was re-anchored with `evidence-check --reverify` in the same commit; Executed in a `--no-local` clone at `89333dd`. Overclaim added to the reload's claim with the golden updated → `2 passed`, exit 0; `unmeasured, yet it is picked up` with the golden updated → `2 passed`, exit 0; scope phrase replaced with the golden updated → `1 failed`, exit 1, so the docstring case's net is removal only. Five of the seven deleted assertions' properties, including clause S1's ordering, leave the whole module at `18 passed` once the golden moves. Sibling site: `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` row S1·S2·S3, same sentence. `tests/test_version_check.py:135-140` states the opposite and is correct |
| 2 | ⬜ `round-2.md`'s `Fixes checked by` reads `nobody — the fixes are not yet written`; `db5b9cd` and `760ac3e` are ancestors of `89333dd` and this round read them | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-2.md:9` | **fixed** `8a31d08` | fixed at 8a31d08 — ``, by `round_record.py new` itself, which set `round-2.md`'s `Fixes checked by` to `round-3` when this record was written; Read. `docs/review-chain-spec.md:680` makes that value correct at landing and stale afterwards. A record location, so `Needs a fix` does not count it |
| 3 | ✅ Round 2's finding 1 — the by-hand comments now point at the load paragraph | `README.md:325` | answered | Read. `README.md:314` is the load paragraph and `:325` the fenced block; `README.ko.md:305` and `:317` the same. Both say *above* |
| 4 | ✅ Round 2's finding 2 — the exact pin refuses the mutation the fourth predicate let through | `tests/test_version_check.py:109` | answered | Executed. `yet`-flipped gap without a golden update → `1 failed`, exit 1. Baseline `18 passed`, exit 0 |
| 5 | ✅ Round 2's finding 3 — `README.md:182` no longer counts the banner's lines | `README.md:182` | answered | Read. The sentence now names the two moves and carries no count |
| 6 | ✅ Both `NAME NOT IN TREE` markers exempt their own line and nothing wider, and no third site names the deleted local | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-1-report.md:162` | answered | Executed. `bin/evidence-check .` exit 0, `0 refused`, on the clean tree; exit 2 naming `round-1-report.md:162` with the marker stripped; exit 2 naming a third unmarked prose mention added to `round-2-fixes.md` |

## Paste-ready fixes

```python
    What this does NOT do is check a REWORDING. An author who changes the
    notice and pastes the new text in here passes both cases — measured, with
    the golden brought along each time: an overclaim added to the reload's
    claim, the gap flipped to `unmeasured, yet it is picked up`, the restart
    named before the reload, and the `measured` and `skill bodies` labels
    dropped. Every one left the module at `18 passed`.

    The one property the pair still holds across a rewording is the scope
    qualifier, because
    `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`
    looks for it independently. Everything else is carried by the message
    below, which is an instruction to a person rather than a check.
```
```
So `notice()`'s whole output is pinned as an exact string at `760ac3e`. **What that pin holds is the text as it stands, not any future text.** Measured against six mutations that leave the golden alone, it kills six. Measured again with the golden updated in the same edit — which is what an author rewording the notice does — an added overclaim and `unmeasured, yet it is picked up` both pass, and so do the restart named first, the `measured` label dropped, the `skill bodies` subject dropped, and two of the three axes dropped: `18 passed`, exit 0, each time. The second case holds exactly one property across a rewording, the scope qualifier, and the rest is carried by the assertion message, which a person reads rather than a checker.
```
```
bin/evidence-check . --reverify
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_version_check.py -q` at `89333dd`, `--no-local` clone | exit 0, `18 passed`. Baseline |
| `test_tmp` probe — `yet`-flipped gap, golden NOT updated, both cases | exit 1, `1 failed, 1 passed`; `test_the_warning_names_the_cheap_move_before_the_expensive_one` fails. The orchestrator's M9 finding re-derived |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — overclaim ADDED to the reload's claim, golden updated in the same edit, both cases | **exit 0, `2 passed`.** The notice then tells a user the reload re-reads the copy just installed |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — `unmeasured, yet it is picked up`, golden updated in the same edit, both cases | **exit 0, `2 passed`** |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — scope phrase replaced with `you just installed`, golden updated, both cases | exit 1, `1 failed, 1 passed`; the docstring case fires. Control |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — five reWORDINGS with the golden updated, whole module: restart named first · `measured` dropped · `skill bodies` dropped · gap negation dropped · two axes dropped | **exit 0, `18 passed` on all five** |  <!-- NAME NOT IN TREE -->
| `bin/evidence-check .` on the clean clone | exit 0. `seal/ledger.md` 764 ok, the fragment `12 ok · 0 drifted · 0 broken`; records arm `9 names read · 0 refused` |
| `bin/evidence-check .` with the marker stripped from `round-1-report.md:162` | exit 2, `NOT-IN-TREE … round-1-report.md:162  \`reload_claim\`` |
| `bin/evidence-check .` with a third unmarked prose mention of `reload_claim` appended to `round-2-fixes.md` | exit 2, naming that new line. The markers exempt their own line only |  <!-- NAME NOT IN TREE -->
| `git show 279628b:hooks/version-check.py \| md5` vs `89333dd` | identical, `cfa60c3f9db6b018076e2927c962cb65`. The notice text did not move in round 2's fixes |
| `diff` of `^def ` lines in `tests/test_version_check.py` across `279628b..89333dd` | same fifteen names, line numbers only. No unit added or removed |
| `git status --porcelain` in the clone after every probe | clean; both mutated files restored byte-identical, verified by digest |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/version-check.py:154` | round 1's 1 — open |
| round-1 | `tests/test_version_check.py:96` | round 1's 2 — open |
| round-1 | `hooks/version-check.py:148` | round 1's 3 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | round 1's 4 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/overview.md:21` | round 1's 5 — open |
| round-1 | `hooks/ledger-migrate.py:4` | round 1's 6 — open |
| round-1 | `README.ko.md:310` | round 1's 7 — open |
| round-2 | `README.md:325` | round 2's 1 — fixed |
| round-2 | `tests/test_version_check.py:117` | round 2's 2 — fixed |
| round-2 | `README.md:182` | round 2's 3 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the presence-and-order assertions should be restored BESIDE the exact pin, so a rewording is checked rather than only trusted. They were collateral in `760ac3e`, not defeated: what defeated the four predicates was blindness to an ADDED clause, and a presence check's blindness is in that same direction, which the exact pin already covers for the current text | an issue at the cap, and `seal/follow-up.md` named in the PR body | the repository owner |
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md` §5 | the repository owner. Carried from rounds 1 and 2 |
| How the four-line `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships. Carried from rounds 1 and 2 |
| The `141 cases` figure in `round-1-fixes.md` | round 1's fix record | the orchestrator. Carried from round 2; nothing in this round turns on it |
