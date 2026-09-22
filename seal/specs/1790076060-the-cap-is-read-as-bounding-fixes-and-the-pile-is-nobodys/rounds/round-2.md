# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — review round 2

| Field | Value |
|---|---|
| Target SHA | 0fa02520b0325170e55bc0010094cfe38df921ee |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 502 |
| Broad gate | e62b5864 against 756b7b35 |
| Fixes checked by | no fixes to check |
| Fix range | `d124c9129c88d2cce809808d6302f56a2620e607..58f8c4317622aa1daafd44ad655cd7b343664bbe`, 3 commits — the range stops before the merge that absorbed the sibling work item |
| Contract changes | none |
| New units | none — no Python file is touched in the range |
| Needs a fix | no — nothing this branch may fix is open. 🟡 1's repair is a change to what a checker measures and 🟡 2's is a runtime message, both refused by `spec.md` §Out, so each is answered with those grounds and handed to the home named in `## Deferred`. The four ⬜ rows are corrections to the run's own paperwork and `Needs a fix` does not count them. |
| Loses a record or crashes | no — nothing found leaves the root and nothing crashes. 🟡 1 makes a check silent, which is a measurement not taken rather than a record lost; no gate, no parsed field and no checker arm changed on this branch. |

- [x] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes rather than at the branch —
`4ddfde2e..9d9180f8`, two commits, the fixes and the `survivors.md` the sweep
commissioned — with round 1's record as the agenda and its verdicts inherited.

`New units` and `Contract changes` both read none, so there was no unreviewed
finding surface and the job was the answers.

Five claims were handed over. That the enumeration was three sites wider than
the round found, with the round asked to re-run an enumeration of its own by a
different construction rather than the same fifteen needles. That the
paste-ready text would have reddened two pins and was adapted rather than
applied, with both pins to be judged on whether they pass for the reason they
exist. That finding 2's answer states the gap rather than papering it. That
rung 3 is agreement rather than naming and a reader can apply it. And that the
measurement is dated and attributed in four carriers that now agree.

`survivors.md`'s three rows were handed over with the property that makes an
exemption safe — that each degrades to reported-again rather than to silence —
and the round was told to probe it rather than reason about it if it doubted.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | committing `survivors.md` subtracts its own quoted wording from the removed set, so the three rows silence nothing and the check exits 0 having measured none of them | `skills/code-review/scripts/survivor_check.py#wanted`; `.github/workflows/hygiene.yml:254` | deferred #507 | #507 — the repair is a change to what `survivor_check` measures, which `spec.md` §Out scopes this work item away from; reproduced and filed by the orchestrating session; Executed at five ranges: 3 excused at `4ddfde2e..9f8efea4`, 0 candidates at `4ddfde2e..9d9180f8` and at `6d410023...HEAD`, absent at `--floor 1.0`, and reported again when a row's quote is broken. The two trees differ by `survivors.md` alone. The repair is a checker change, which `spec.md` §Out refuses, so the home is an issue |
| 🟡 2 | the depth exit's runtime message is imprecise under the ladder in the same way `CAPPED_EXIT` is, and `overview.md` discloses only the first | `skills/code-review/scripts/round_record.py#DEPTH_EXIT`; `skills/code-review/scripts/chain_check.py:2648` and `:3355`; `seal/specs/…/overview.md` §*Not verified* | answered | corrected at `3b29de2d` — the `DEPTH_EXIT` disclosure row was written into `overview.md` §*Not verified* beside `CAPPED_EXIT`, and the two now name each other as a pair; Read. The fix pass rewrote this rule's destination in three live documents, so the branch treats it as in the class; the constant that prints it to a person was left, correctly, and named nowhere. Same grounds as `CAPPED_EXIT`, so the owed act is the disclosure row and not the reword |
| ⬜ | `spec.md` says §*A fix pass adds the unit that pins it* is Unchanged and §Out says rule 1 is untouched; the fix pass changed that section and two carriers, and no divergence is recorded | `seal/specs/…/spec.md` §Grounding; `seal/specs/…/overview.md` §*Fed back into the spec* | deferred `seal/specs/…/overview.md` | Executed: `git diff 6d410023..4ddfde2e` over `skills/code-review/orchestration.md` touches none of that section, so the change is the fix pass's. A correction to the run's paperwork |
| ⬜ | `survivors.md`'s header states three survivors over the fix range; the range this record names reports zero | `seal/specs/…/survivors.md`, the comment header | deferred `seal/specs/…/survivors.md` | Executed — the same command at both ranges. True of round 1's one-commit range, false of this one |
| ⬜ | `questions.md` Q1's Options cell and `overview.md:12` still read 47% where the four corrected carriers read 48% | `seal/specs/…/questions.md` Q1; `seal/specs/…/overview.md:12` | deferred `seal/specs/…/questions.md` | Read against the four corrected carriers. The copies attributed to #493's own count are history and stand |
| ⬜ | rung 3's bolded opening sentence asserts the naming test the paragraph below it withdraws | `docs/review-chain-spec.md:273` | answered | Read whole. The rung table row and the paragraph's body both state agreement, and the tell is given; the rule ships right, so the cost is a sentence that reads badly |
| 🟢 | no live document now states the filing unconditionally at a capped exit, and the only site left is the disclosed one | `docs/review-chain-spec.md:1347`; `skills/code-review/orchestration.md:163`; `skills/code-review/scripts/chain_check.py:228` | confirmed | Executed: an enumeration of my own, built as co-occurrence of an issue-destination token with an open-finding or exit token over every live carrier, 56 hits read one at a time. It reaches `CAPPED_EXIT` and nothing else |
| 🟢 | both pins pass, and for the reason they exist rather than by luck | `tests/test_the_reopening_is_one.py:593`; `tests/test_the_rules_have_one_owner.py:312` | confirmed | Executed: `bin/test` over both modules, 97 passed, 1 skipped, exit 0 read directly. The subsection carries `deferred <home>` and `deferred #N` together, and `deferred #N` is true of rungs 2 and 3, so the adaptation states a fact rather than preserving a token. The skill-halves assertion is satisfied at `orchestration.md:165`, independently of the depth-exit edit at `:246` |
| 🟢 | an empty `New units` is stated as not being evidence, and the substitute is a coordinate a reader already has | `docs/review-chain-spec.md:84-95` | confirmed | Read. It names the four prose suffixes, says an empty row is not evidence that the run created nothing, names the misreading and the direction it fails in, and sends the reader to the fix range. `Fix range` is a row of every record, so nothing has to be found |
| 🟢 | rung 3 is agreement rather than naming, and no count stands in the shipped text | `docs/review-chain-spec.md:273-285` | confirmed | Read. *An owner written because there was nobody else to write is rung 4's answer* is the tell; the column's most common value is named in words and not as a figure |
| 🟢 | the measurement agrees across the four carriers, is dated, and the share and the open count are no longer one numeral | `docs/review-chain-spec.md:294-301`; `docs/issues-and-milestones.md:86-88`; `seal/specs/…/changelog.md:30`; ledger row C5 | confirmed | Read all four: 89 / 43 closed / 48% / 46 open / 2026-09-22, this run's issue excluded. C5 carries `Corrected 2026-09-22`. 48 and 46 are different numerals |
| 🟢 | the degradation property the exemption rows rest on is real | `skills/code-review/scripts/survivor_check.py#exempted` | confirmed | Executed at `4ddfde2e..9f8efea4`: all three rows return their grounds, and breaking one row's quote reports its candidate again with exit 1. What it does not survive is the file's own commit — 🟡 1 |
| 🟢 | this work item's ledger fragment resolves | `seal/ledger/1790076060-…md` | confirmed | Executed: `bin/evidence-check` scoped to the fragment, 9 ok · 0 drifted · 0 broken, exit 0 read directly |
| ❓ out of verified scope | the full suite, the repository-wide lint and the typecheck | the whole branch | unverified | `agent-contract` §2 — the broad gate is one act with one owner, and the spawn prompt assigns it to the sealer and forbids it here. Answered by the `sealer`. Nothing in this report leaves it open, so the gate has come due: what comes due is the sealer's spawn |

## Paste-ready fixes

```
| Whether `survivor_check.py` should exclude `seal/specs/*/survivors.md` from the range the way it already excludes `rounds/`. A survivors file quotes the surviving wording verbatim — the quote is the anchor, so it always does — and `wanted` subtracts everything the range wrote, so committing the file removes its own three survivors from the check. Measured on this branch: `--range 4ddfde2e..9f8efea4` reports `every survivor is excused by a row above (3)`, and `--range 4ddfde2e..9d9180f8`, the same tree plus that one file, reports `no removed wording is still standing` with the exemption file and without it. The hygiene step and `spec.md` A11 both read the second sentence. This is #365 on a path its exclusion does not cover, and the repair is a change to what a checker measures, which `spec.md` §Out refuses here | the repository owner, through a new issue |
```
```
# A judged survivor's own file, for the same reason and on both sides.
# `seal/specs/<id>/survivors.md` quotes the standing wording verbatim --
# the quote is the anchor -- so a range that adds one writes the removed
# sentence back, `wanted` subtracts it, and the check reports success
# having measured the survivors the file was written to record. #365 is
# the same defect one path over.
```
```
| Whether the depth exit's runtime message — `DEPTH_EXIT` in `round_record.py`, printed when `close` refuses a depth-2 unit, and the same sentence at `chain_check.py:2648` and `:3355` — should be reworded to the ladder. It says a unit a fix pass may not add *is deferred with a named answerer, or becomes an issue*; under the ladder such a unit may take rung 4 instead, so the message is imprecise in exactly the way `CAPPED_EXIT` is. The prose carriers of the same rule were rewritten in this run's fix pass; the message was not, because rewording one is a gate change `spec.md` §Out refuses | the repository owner, through the review chain |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/survivor-check --range 4ddfde2e..9f8efea4 --exempt seal/specs/…/survivors.md` | exit 0; three candidates, all three excused by name, closing line `every survivor is excused by a row above (3)` |
| `bin/survivor-check --range 4ddfde2e..9d9180f8 --exempt seal/specs/…/survivors.md`, and the same without `--exempt` | exit 0 both times; zero candidates, closing line `no removed wording is still standing`. The two trees differ by `survivors.md` and nothing else |
| `bin/survivor-check --range 6d410023...HEAD --exempt seal/specs/…/survivors.md` — the form the hygiene workflow runs | exit 0; zero candidates, `no removed wording is still standing` |
| `bin/survivor-check --range 4ddfde2e..9d9180f8 --floor 1.0` | exit 1 on unrelated below-floor pairs; the two `CAPPED_EXIT` survivors are absent from the list entirely, so the loss is subtraction and not the floor |
| `bin/survivor-check --range 4ddfde2e..9f8efea4 --exempt <a scratchpad copy of the file with row 1's quote broken>` | exit 1; the broken row stops excusing, its candidate is reported again, the other two still excuse |
| `bin/test tests/test_the_reopening_is_one.py tests/test_the_rules_have_one_owner.py -q` | 97 passed, 1 skipped; exit 0 read directly, not through a pipe |
| `bin/evidence-check --ledger seal/ledger/1790076060-…md .` | 9 ok · 0 drifted · 0 broken · 0 external · 0 old-format; exit 0 read directly |
| a co-occurrence enumeration over `docs`, `skills`, `agents`, `templates`, `CLAUDE.md`, `CONTRIBUTING.md` and both READMEs — every issue-destination token whose ±220-character flattened window also carries an open-finding or exit token | 56 hits, read one at a time. No live capped-exit site states the filing unconditionally; thirteen sites in seven files carry the depth/floor spelling |
| `grep -rn 'deferred #N'` over the same live carriers | 6 hits, all of them rung 2, rung 3, or the qualified *where that home is an issue* |
| `git diff 6d410023..4ddfde2e -- skills/code-review/orchestration.md`, over §*A fix pass adds the unit that pins it* | no hunk touches that section, so the fix pass is what changed it |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's one act and was not run in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/review-chain-spec.md:1327`; `skills/code-review/orchestration.md:164`; `skills/code-review/scripts/chain_check.py:228` | round 1's 🔴 1 — fixed |
| round-1 | `docs/review-chain-spec.md:78`; `skills/code-review/scripts/round_record.py:2966` and `:2437` | round 1's 🟡 2 — fixed |
| round-1 | `docs/review-chain-spec.md:264` | round 1's 🟡 3 — fixed |
| round-1 | `docs/review-chain-spec.md:273`; `docs/issues-and-milestones.md:85`; `seal/specs/…/changelog.md`; ledger row C5 | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_the_rules_have_one_owner.py:216` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/specs/1790076060-…/questions.md` | round 1's ⬜ 6 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py#stopping_floor` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py`; `skills/code-review/scripts/round_record.py` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md:2203` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#seal` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_rules_have_one_owner.py:607` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py` | round 1's ⬜ — answered |
| round-1 | the whole branch | round 1's ❓ out of verified scope — unverified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a `survivors.md` added by the range subtracts its own quoted wording from the removed set, so the check reports success having measured nothing — #365's defect on a path the exclusion does not cover | a new issue — rung 3. The finding names a defect in the repository's own gate whose class already cost a release, so it gives its answerer a reason to act. The repair is a checker change `spec.md` §Out refuses on this branch | the repository owner |
| whether the depth exit's runtime message should be reworded to the ladder | `seal/specs/…/overview.md` §*Not verified*, beside the `CAPPED_EXIT` row it matches — rung 1, the branch owns the record | the repository owner, through the review chain |
| `chain_check.py`'s `CAPPED_EXIT` runtime message states the pre-ladder filing rule | already deferred by this branch — `overview.md` §*Not verified*. Carried forward from round 1, not re-opened | the repository owner |
| the 17 rows of `seal/ledger.md` whose cell count differs from their table header | already filed as #501. Carried forward from round 1 | the repository owner |
