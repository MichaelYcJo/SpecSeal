# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — review round 1

| Field | Value |
|---|---|
| Target SHA | cb61be1d0e94b63e530c3a2b0347a4648aad5f77 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 502 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `4ddfde2ee12e99759f22e67efcd65264a96ec0b2..9f8efea4c29bb786ad6d5b8c4db533305a474a3b`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, the three live documents still stating that every finding still open becomes an issue. Findings 2, 3 and 4 are fix or grounds; 5 and 6 are corrections. |
| Loses a record or crashes | no — nothing found leaves the root or crashes. The branch changes no gate, no checker arm and no parsed field, and both Python diffs are comments and docstrings. |

- [x] Pass

## What this round was asked

Round 1, the first reading of the built branch, with nothing to inherit. Spec
compliance against the frame first, and the tickets ranked below `docs/`.

The work changes documents and pins and changes no gate, which is what makes
its correctness hard to see, so the round was pointed at five things rather
than at a diff: that the two bounds are named apart in a way true of what
`chain_check.py` actually does at BOTH exits; that the ownership test's
evidence — each record's `New units` row — can carry the test's weight for the
kinds of finding a capped run leaves; that a reader at a capped exit can tell
which rung of the new ladder they are on without a judgment the documents do
not supply; that the trade `questions.md` Q1 ships on its default states its
cost where a reader meets it; and what the two new `RULES` rows actually pin,
given that the phrase sweep is a substring match over needles that wrap.

The ledger was handed over as claims with coordinates: twenty-two rows drifted
once per anchor, six of them read only during the marker pass, two resting on
measurements taken the same day, and one row repaired for a cell-count defect
that is #501's class.

The broad gate was withheld. What the orchestrating session had already run
was named so the round would not spend itself repeating it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | the reopening exit still says every finding still open becomes an issue, contradicting the ladder the same file ships | `docs/review-chain-spec.md:1327`; `skills/code-review/orchestration.md:164`; `skills/code-review/scripts/chain_check.py:228` | **fixed** `9f8efea4` | fixed at 9f8efea4; Read. The ladder section's first line governs the capped exit; the sentence at 1327 is unqualified. `spec.md` Scope In 5 asks for exactly this correction. `chain_check.py:771` is the same class and is already disclosed in `overview.md` |
| 🟡 2 | `New units` is empty for a prose fix range, so the ownership test decides every documentation finding by default | `docs/review-chain-spec.md:78`; `skills/code-review/scripts/round_record.py:2966` and `:2437` | **fixed** `9f8efea4` | fixed at 9f8efea4; Executed: `measure` over this branch's twenty markdown paths returns `added == []`, cell `none` |
| 🟡 3 | rung 3's test accepts `the repository owner`, which is 409 of 1,170 `Who answers it` cells, so filing remains the default for the largest class | `docs/review-chain-spec.md:264` | **fixed** `9f8efea4` | fixed at 9f8efea4; Executed: the column measured across every round record in the tree |
| 🟡 4 | the 89 / 47% / 47 measurement does not reproduce — 89 issues, 43 closed (48%), 46 open | `docs/review-chain-spec.md:273`; `docs/issues-and-milestones.md:85`; `seal/specs/…/changelog.md`; ledger row C5 | **fixed** `9f8efea4` | fixed at 9f8efea4; Executed against the tracker today, with this branch's own #501 backed out |
| ⬜ 5 | the two `RULES` rows pin the headline sentences and not the rung table, and cannot see a carrier that links and restates | `tests/test_the_rules_have_one_owner.py:216` | **fixed** `9f8efea4` | fixed at 9f8efea4; Read. `flat()` is whitespace-flexible and every needle resolves; the gap is what is left unasserted |
| ⬜ 6 | Q1 names itself as the overturn row for a trade whose directory `settle` removes | `seal/specs/1790076060-…/questions.md` | answered | corrected at `9f8efea4`; Read against `skills/settle/SKILL.md:152`. The durable statement exists in the rung-4 paragraph |
| 🟢 | the two bounds are named apart, and both claims hold against the walk that decides them | `skills/code-review/scripts/chain_check.py#stopping_floor` | confirmed | Read at both exits. After a floor `no` the reopening walk refuses a second fix-closing record, so the reopening bound's terminal record commissions nothing by construction. At a round-cap exit the capped record is itself the floor record, so its own fixes are outside `later`, one verifying round is counted and permitted, and the shipped pair round-6/round-7 of `1790039346-…` is that shape and passed CI |
| 🟢 | no line either Python file computes changed | `skills/code-review/scripts/chain_check.py`; `skills/code-review/scripts/round_record.py` | confirmed | Executed: the range's diff over both files is eight docstring lines and two comment blocks. The corrected comments describe the refusal at `round_record.py:4257` accurately — read against the code |
| 🟢 | twenty-two ledger rows, every `Notes` cell append-only, no prior marker overwritten | `seal/ledger.md` | confirmed | Executed: a cell-level comparison of both ends. One row's `Notes` was not a prefix of its new value — row 2203, where the repair moved a marker in, and the marker text is intact inside the cell |
| 🟢 | the row 2203 repair is correct | `seal/ledger.md:2203` | confirmed | Executed: splitting on unescaped pipes, the old row carried six content cells against a five-column header and no terminator; the new row carries five and is terminated, with `**Re-verified 2026-09-16**` now inside `Notes`. 17 rows of the file still carry the shape — that is #501 and not this branch's |
| 🟢 | the two measurements the late-read rows rest on | `skills/code-review/scripts/round_record.py#seal` | confirmed | Executed: an AST count gives exactly six `raise Refused` sites inside `seal` |
| 🟢 | the two prose constraints hold | `tests/test_the_rules_have_one_owner.py:607` | confirmed | Executed: *at most one more round record* stands once in each of the four named files, four in the tree; `Unless th` returns nothing |
| ⬜ | `chain_check.py` enforces no round cap | `skills/code-review/scripts/chain_check.py` | answered | Read. Only the floor walk and the reopening walk exist; three and five are counted by nobody. The new two-bounds table says *here* in its own `Where it is stated` cell, so it claims no checker and the table is honest |
| ❓ out of verified scope | the full suite, the repository-wide lint and the typecheck | the whole branch | unverified | `agent-contract` §2 — the broad gate is one act with one owner, and the spawn prompt assigns it to the sealer. Answered by the `sealer`, spawned after the rounds settle |

## Paste-ready fixes

```
**After a record that met the floor, at most one later record may close on a
fix.** That one is the verifying round that reopened the run; the record that
reads its fixes ends the run whatever it finds. There the run is `capped`:
every finding still open takes the ladder in §*Where a leftover goes — the
ladder, and why a new issue is not the default*, its verdict reads `deferred
<home>` wherever a home was found, the record's `Fixes checked by` reads `no
fixes to check`, and the pull request says `chain: capped`.
```
```
later record may close on a fix, a second is refused, and the run ends
`capped` — every finding still open takes the filing ladder below, its
verdict reads `deferred <home>` wherever a home was found, the record's
`Fixes checked by` reads `no fixes to check`, and the pull request is
labelled `chain: capped`. `docs/review-chain-spec.md` §*The reopening — one,
and then the run is capped* owns the rule, the refusal and its cutoff.
```
```
finding still open takes the filing ladder, its verdict reads `deferred
<home>`, the record's `Fixes checked by` reads `no fixes to check`, and the
pull request says `chain: capped`. `docs/review-chain-spec.md` §*Where a
leftover goes -- the ladder, and why a new issue is not the default* owns
where a filed finding goes. `deferred <home>` is a closing word for that and
not a fix word; the bare word stays open.
```
```
not add mechanism at all — a rule, a checker, a template section, a walk —
and a finding closable only by one takes the ladder below rather than an
issue by default;
```
```
**`New units` names Python units, so a finding in a document is answered by
the fix range instead.** `round_record.py`'s `measure` skips every prose path
whole, so a round whose fixes were documents writes `New units | none`
however much the branch wrote. There the evidence of ownership is the range
itself: a paragraph this run's own fixes added belongs to the branch on the
same test, read off the diff rather than off the row.
```
```
**The test is the one `seal/follow-up.md` already applies to itself**: the
row names a person, with no condition attached. What that file's own grounds
add is the half a rung has to read — *nobody agreed to open `X`, so nobody
answers*. So the cell has to name somebody the finding gives a reason to act,
and an owner written because there was nobody else to write is rung 4's
answer rather than rung 3's. Nothing new is written to answer it: the
reviewer's `## Deferred` table already carries the column — `Who answers it`
— and the ladder reads that cell, so the decision costs no field, no verdict
word and no question. A cell reading *whoever picks it up* is the same answer
as an empty one.
```
```
When this was written the `from-review` label carried 89 issues, 43 of them
closed — 48% — and 23 of the 46 still open had been opened inside one
three-day window.
```
```
`--label from-review --state all` beside `--state closed` gives the share of
filed findings anybody went on to act on, and that share is why the filing
decision is a ladder rather than a reflex: 43 of 89 were closed when the
ladder was written, and 23 of the 46 still open had been opened inside one
three-day window.
```

## Executed probes

| What was run | Result |
|---|---|
| `measure` from `skills/code-review/scripts/round_record.py`, over the range's twenty markdown paths, in process | `added == []`, `changed == []`, `heuristic == []`; the cell would read `\| New units \| none \|`. Over the whole range it names four constants in `tests/test_the_rules_have_one_owner.py` and nothing else |
| the 1,170 `Who answers it` cells of every `seal/specs/*/rounds/round-*.md`, tallied | 409 read `the repository owner` exactly; about 60 more name the owner in another spelling; about 22 read `nobody …` |
| `gh issue list --label from-review --state all --limit 500` | 90 issues, 43 closed, 47 open; #501 opened today by this branch. Backing it out: 89 / 43 closed / 46 open. 23 of the open ones fall in 2026-09-07…2026-09-09 |
| a cell-level comparison of `seal/ledger.md` at both ends of the range | 22 changed lines; every `Notes` cell append-only except row 2203, whose sixth cell was folded into `Notes` intact; every `Checked` cell moved to 2026-09-22 |
| unescaped-pipe field counts for row 2203 at both ends, against its table header | old: 6 content cells, no terminator. new: 5 content cells, terminated. Header: 5. 17 rows of the file still differ from their header |
| an AST count of `raise Refused` inside `seal`, in `skills/code-review/scripts/round_record.py` | 6 |
| `grep -rn "becomes an issue" docs skills agents templates` | 5 live sites stating the filing with no condition; 9 more carry *deferred with a named answerer, or becomes an issue*, which the ladder does not contradict |
| `grep -rn "at most one more round record"` and `grep -rn "Unless th"` over `docs skills agents templates` | 4 hits, one per named file; 0 hits |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's one act and was not run in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `chain_check.py`'s `CAPPED_EXIT` runtime message states the pre-ladder filing rule | already deferred by this branch — `overview.md` §*Not verified*. Reported here as the fifth site of finding 1's class, not as a new deferral | the repository owner |
| the 17 rows of `seal/ledger.md` whose cell count differs from their table header | already filed as #501 | the repository owner |
