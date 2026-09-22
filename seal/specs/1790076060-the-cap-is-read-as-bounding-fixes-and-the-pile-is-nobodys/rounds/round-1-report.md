# Round 1 — review report

| Field | Value |
|---|---|
| Work item | `1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys` |
| Branch | `docs/492-the-cap-bounds-rounds-not-fixes` |
| Target SHA | `cb61be1d0e94b63e530c3a2b0347a4648aad5f77` |
| Base | `origin/release/v0.13.1` at `6d41002398bfeeb55db08cca9b441b68e0267049` |
| PR | #502 |
| Round | 1 — no earlier record, nothing inherited |

Stage 1 was spec compliance against `spec.md`, `plan.md`, `questions.md` and
`phases/phase-1.md`…`phase-4.md`. Stage 2 was quality. The diff is 23 files:
twenty documents, two Python files changed only in comments and docstrings,
and one test module.

## What the account claimed, and what I found

The build's account reaches this round through `overview.md`, the four phase
records, `questions.md` and the spawn prompt. Five of its claims were opened.

- **Claimed** (phase 4, `questions.md` Q2): the seven standing copies of
  *every finding still open becomes an issue* "are not in the class — every
  one of them is about the reopening bound, where the sentence is still
  true", and the only imprecise place is `chain_check.py`'s `CAPPED_EXIT`.
  **Found false for three of them.** The ladder this branch ships governs the
  capped exit by its own first line, so the sentence is no longer true at the
  reopening bound either. Finding 1.
- **Claimed** (`spec.md` Scope In 1, `overview.md`): the ownership test costs
  nobody a judgment because `New units` already holds the evidence.
  **Found empty for prose.** Executed against this branch's own range:
  `New units` reads `none` over twenty changed documents. Finding 2.
- **Claimed** (`docs/review-chain-spec.md`, `docs/issues-and-milestones.md`,
  `changelog.md`, ledger row C5): the label carried 89 issues, 47% of them
  closed, 23 of the 47 still open inside one three-day window. **Found: 89
  issues, 43 closed (48%), 46 open.** Finding 4.
- **Claimed** (`questions.md` Q3, phase 4): the two Python files changed in
  comments and docstrings only. **Confirmed**, by diff and by reading the
  refusal the corrected comments describe.
- **Claimed** (phase 4): twenty-two ledger rows re-read, no prior marker
  overwritten, row 2203 repaired. **Confirmed**, by a cell-level comparison
  of both ends of the range.

## 🔴 1 — the reopening exit still tells the reader to file everything

`docs/review-chain-spec.md:1327`, `skills/code-review/orchestration.md:164`,
`skills/code-review/scripts/chain_check.py:228`

The branch's new §*Where a leftover goes — the ladder, and why a new issue is
not the default* opens with *At the bound, or earlier when a round returns
nothing blocking*, so it governs every capped exit, the reopening bound
included. Three screens further down, the reopening subsection still reads:

> There the run is `capped`: every finding still open becomes an issue, its
> verdict reads `deferred #N` …

Under the ladder a finding that names nobody must **not** become an issue —
it takes rung 4 and stays in the round record and the pull request body. So
the owner document contradicts itself on the rule this work item exists to
ship, and the contradiction is inside one file.

**Why it matters, and who meets it.** The reopening subsection is where a
reader goes when a run is capped — that is what it is for. A reader who goes
there reads the pre-ladder instruction and files every open finding, which is
the 47%-pile behaviour #493 was raised against. The new paragraph the branch
added directly beneath this sentence corrects the *fix* half of the exit and
leaves the *filing* half standing.

**The class, enumerated.** `grep -rn "becomes an issue" docs skills agents
templates` returns five live sites where the filing is stated with no
condition:

| Site | What it says | State |
|---|---|---|
| `docs/review-chain-spec.md:1327` | every finding still open becomes an issue | not corrected, and the owner |
| `skills/code-review/orchestration.md:164` | the same sentence | not corrected, and a rule-14 link carrier |
| `skills/code-review/scripts/chain_check.py:228` | the same sentence in the module docstring | not corrected — and this is the docstring the branch edited, two lines above its new paragraph |
| `agents/smith.md:305` | a finding closable only by a rule, a checker, a template section or a walk *is an issue* | not corrected; `spec.md` scopes the underlying rule out, but not this sentence |
| `chain_check.py:771` (`CAPPED_EXIT`) | the same sentence as a runtime message | disclosed in `overview.md` §*Not verified* with the repository owner named |

`spec.md` Scope In 5 asks for exactly this: *every place in the tree that
repeats the sentences above becomes a link naming the owner*. Four of the
five were missed because the sweep looked for wording the range **removed**,
and this wording was not removed anywhere — which `questions.md` Q2 says of
`CAPPED_EXIT` and does not draw for the other four.

Only the last row is answered. The first three are a live disagreement in
loaded documents and a fix is owed; `agents/smith.md:305` can be answered
with grounds if the smith holds that #493's out-of-scope line covers the
sentence as well as the rule.

## 🟡 2 — the ownership test has no evidence for a prose finding

`docs/review-chain-spec.md:78-80`, against
`skills/code-review/scripts/round_record.py:2966-2971` and `:2437`

The new section says the ownership question is answered without judgment:

> The evidence is already written down: each record's `New units` row names
> the units that round's fixes added, so the question is answered by reading
> the run's own records rather than by judging, and it costs nobody a
> question.

`measure` skips every path ending in `PROSE_SUFFIXES` — `.md`, `.markdown`,
`.txt`, `.rst` — before both the AST pass and the diff-line heuristic, so a
fix range made of documents contributes no units at all. Executed against
this branch's own range: twenty markdown paths, `added == []`, and the cell
would read `| New units | none |`.

So for a documentation work item — which this one is — the row is empty
whatever the branch wrote, and a reader applying the test literally answers
*not a unit this run created* for a paragraph the run created three commits
ago. The rule then sends it down the ladder to rung 3 or 4, which the section
itself names as the expensive direction.

This is not hypothetical for the next round of this very review: every
finding above is located in a document, and `New units` for this branch names
four constants in one test module and nothing else.

The section's own measured instance already shows the gap. It says the
character-level oracle "was the branch's outright" — that one was settled by
judging, not by reading a row.

## 🟡 3 — rung 3's test does not discriminate, so filing stays the default

`docs/review-chain-spec.md:264-269`

The test is quoted from `seal/follow-up.md`: *the row names a person, with no
condition attached*. Measured over the column the ladder reads — 1,170
`Who answers it` cells in `seal/specs/*/rounds/round-*.md` — the values are:

| Value | Rows | Which rung it selects |
|---|---|---|
| `the repository owner` exactly | 409 | rung 3 — a person, no condition |
| other spellings naming the owner | ~60 | rung 3 |
| `the orchestrator` / `the sealer` | ~120 | rung 3 |
| `nobody …` | ~22 | rung 4 |

`the repository owner` is a person with no condition attached, so it passes
rung 3's test as written, and it is what 35% of the column already reads. A
ladder whose third rung accepts the most common cell in the column files what
is filed today, which is the outcome the section's own measurement argues
against.

`seal/follow-up.md`'s reasoning is sharper than the sentence the ladder
borrows: *nobody agreed to open `X`, so nobody answers*. The test the ladder
needs is agreement, and what it quotes is naming.

Rungs 1 and 2 are unaffected and are where the ladder's measured instance
(round 7 sending seven findings to one open issue) actually sat. What is left
undecided is the rung-3/rung-4 boundary, which is the boundary `questions.md`
Q1 ships a trade on.

## 🟡 4 — the measurement behind the ladder does not reproduce

`docs/review-chain-spec.md:271-277`, `docs/issues-and-milestones.md:81-89`,
`seal/specs/…/changelog.md`, ledger row C5

> the `from-review` label carried 89 issues with 47% of them closed, and 23
> of the 47 still open had been opened inside one three-day window

Executed today: `gh issue list --label from-review --state all --limit 500`
returns **90** issues, 43 closed and 47 open. One of the 90 is #501, opened
by this branch at 12:26 today and labelled `from-review`. Backing it out
gives the snapshot the sentence describes: **89 issues, 43 closed — 48% —
and 46 open.** The three-day window figure holds: 23 of those open issues
were opened between 2026-09-07 and 2026-09-09.

Two of the three numbers are therefore wrong, and the second one is wrong in
a way that hides it: 89 with 47 open implies 42 closed, which is self-
consistent arithmetic that the tracker does not hold. `47%` and `47` are also
the same numeral in one sentence meaning a share and a count, which is what
makes the pair read as checked.

The direction of the error is small and does not overturn the argument. What
it costs is the thing `docs/issues-and-milestones.md`'s new paragraph is for:
a reader re-taking the query gets 43/89 and cannot tell whether the label set
moved or the number was wrong.

## ⬜ 5 — what the two `RULES` rows pin, and what they cannot see

`tests/test_the_rules_have_one_owner.py:216-252`

Both rows work: `flat()` collapses all whitespace, so each needle survives
the wrapping in its file, and each of the twelve link strings resolves. What
they pin is narrower than the two rules:

- **Rule 13** pins one sentence — the ownership test — plus seven carriers
  naming the section. *Three and five count rounds*, the two-bounds table and
  the `Fixes checked by` paragraph are unpinned. The section **title** is
  pinned indirectly, seven times over, because every link string quotes it.
- **Rule 14** pins the headline sentence plus five carriers. The four rungs
  themselves are unpinned: a rung could be reordered, reworded or deleted and
  both new cases stay green.

And the shape neither row can see is the one finding 1 reports. The assertion
is a substring test of the link string against the carrier read through
`flat`; a carrier that names the owner **and** also
states a contradicting sentence passes. `skills/code-review/orchestration.md`
is a rule-14 link carrier that does exactly that, at line 164.

Naming it rather than fixing it: the file's own convention is one sentence
per link, and existing carriers restate before they link too
(`agents/smith.md:300-306` for the no-mechanism rule), so this is house shape
rather than a regression. What is worth adding is an assertion on the rung
table, in the way rule 4's case already asserts `chain: capped` and
`deferred #N` beside its link count.

## ⬜ 6 — `questions.md` Q1 names an overturn row that `settle` removes

`seal/specs/…/questions.md`, Q1's default cell

The cost of rung 4 is stated where a reader meets the rule — the fourth
rung's own paragraph in `docs/review-chain-spec.md`, and again in
`overview.md` and in the changelog fragment. That part of the trade is
handled well: nobody has to go looking.

Q1 then says **This row is where it is overturned.** `skills/settle/SKILL.md`
removes the work item's directory at a later release, which takes that row
with it — the same disappearance the rung-4 paragraph names for the findings.
The durable statement does exist (*the repository owner is who overturns it*,
in the rung-4 paragraph), so nothing is lost; what is imprecise is Q1's
sentence pointing at itself as the durable home.

Nothing the branch writes makes the trade harder to overturn than Q1 claims,
beyond the ordinary: rule 14 pins the headline sentence in six files, which
is the repository's standard cost for a rule and is disclosed by the pin
file's own docstring.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | the reopening exit still says every finding still open becomes an issue, contradicting the ladder the same file ships | `docs/review-chain-spec.md:1327`; `skills/code-review/orchestration.md:164`; `skills/code-review/scripts/chain_check.py:228` | open | Read. The ladder section's first line governs the capped exit; the sentence at 1327 is unqualified. `spec.md` Scope In 5 asks for exactly this correction. `chain_check.py:771` is the same class and is already disclosed in `overview.md` |
| 🟡 2 | `New units` is empty for a prose fix range, so the ownership test decides every documentation finding by default | `docs/review-chain-spec.md:78`; `skills/code-review/scripts/round_record.py:2966` and `:2437` | open | Executed: `measure` over this branch's twenty markdown paths returns `added == []`, cell `none` |
| 🟡 3 | rung 3's test accepts `the repository owner`, which is 409 of 1,170 `Who answers it` cells, so filing remains the default for the largest class | `docs/review-chain-spec.md:264` | open | Executed: the column measured across every round record in the tree |
| 🟡 4 | the 89 / 47% / 47 measurement does not reproduce — 89 issues, 43 closed (48%), 46 open | `docs/review-chain-spec.md:273`; `docs/issues-and-milestones.md:85`; `seal/specs/…/changelog.md`; ledger row C5 | open | Executed against the tracker today, with this branch's own #501 backed out |
| ⬜ 5 | the two `RULES` rows pin the headline sentences and not the rung table, and cannot see a carrier that links and restates | `tests/test_the_rules_have_one_owner.py:216` | open | Read. `flat()` is whitespace-flexible and every needle resolves; the gap is what is left unasserted |
| ⬜ 6 | Q1 names itself as the overturn row for a trade whose directory `settle` removes | `seal/specs/1790076060-…/questions.md` | open | Read against `skills/settle/SKILL.md:152`. The durable statement exists in the rung-4 paragraph |
| 🟢 | the two bounds are named apart, and both claims hold against the walk that decides them | `skills/code-review/scripts/chain_check.py#stopping_floor` | confirmed | Read at both exits. After a floor `no` the reopening walk refuses a second fix-closing record, so the reopening bound's terminal record commissions nothing by construction. At a round-cap exit the capped record is itself the floor record, so its own fixes are outside `later`, one verifying round is counted and permitted, and the shipped pair round-6/round-7 of `1790039346-…` is that shape and passed CI |
| 🟢 | no line either Python file computes changed | `skills/code-review/scripts/chain_check.py`; `skills/code-review/scripts/round_record.py` | confirmed | Executed: the range's diff over both files is eight docstring lines and two comment blocks. The corrected comments describe the refusal at `round_record.py:4257` accurately — read against the code |
| 🟢 | twenty-two ledger rows, every `Notes` cell append-only, no prior marker overwritten | `seal/ledger.md` | confirmed | Executed: a cell-level comparison of both ends. One row's `Notes` was not a prefix of its new value — row 2203, where the repair moved a marker in, and the marker text is intact inside the cell |
| 🟢 | the row 2203 repair is correct | `seal/ledger.md:2203` | confirmed | Executed: splitting on unescaped pipes, the old row carried six content cells against a five-column header and no terminator; the new row carries five and is terminated, with `**Re-verified 2026-09-16**` now inside `Notes`. 17 rows of the file still carry the shape — that is #501 and not this branch's |
| 🟢 | the two measurements the late-read rows rest on | `skills/code-review/scripts/round_record.py#seal` | confirmed | Executed: an AST count gives exactly six `raise Refused` sites inside `seal` |
| 🟢 | the two prose constraints hold | `tests/test_the_rules_have_one_owner.py:607` | confirmed | Executed: *at most one more round record* stands once in each of the four named files, four in the tree; `Unless th` returns nothing |
| ⬜ | `chain_check.py` enforces no round cap | `skills/code-review/scripts/chain_check.py` | answered | Read. Only the floor walk and the reopening walk exist; three and five are counted by nobody. The new two-bounds table says *here* in its own `Where it is stated` cell, so it claims no checker and the table is honest |
| ❓ out of verified scope | the full suite, the repository-wide lint and the typecheck | the whole branch | unverified | `agent-contract` §2 — the broad gate is one act with one owner, and the spawn prompt assigns it to the sealer. Answered by the `sealer`, spawned after the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `measure` from `skills/code-review/scripts/round_record.py`, over the range's twenty markdown paths, in process | `added == []`, `changed == []`, `heuristic == []`; the cell would read `| New units | none |`. Over the whole range it names four constants in `tests/test_the_rules_have_one_owner.py` and nothing else |
| the 1,170 `Who answers it` cells of every `seal/specs/*/rounds/round-*.md`, tallied | 409 read `the repository owner` exactly; about 60 more name the owner in another spelling; about 22 read `nobody …` |
| `gh issue list --label from-review --state all --limit 500` | 90 issues, 43 closed, 47 open; #501 opened today by this branch. Backing it out: 89 / 43 closed / 46 open. 23 of the open ones fall in 2026-09-07…2026-09-09 |
| a cell-level comparison of `seal/ledger.md` at both ends of the range | 22 changed lines; every `Notes` cell append-only except row 2203, whose sixth cell was folded into `Notes` intact; every `Checked` cell moved to 2026-09-22 |
| unescaped-pipe field counts for row 2203 at both ends, against its table header | old: 6 content cells, no terminator. new: 5 content cells, terminated. Header: 5. 17 rows of the file still differ from their header |
| an AST count of `raise Refused` inside `seal`, in `skills/code-review/scripts/round_record.py` | 6 |
| `grep -rn "becomes an issue" docs skills agents templates` | 5 live sites stating the filing with no condition; 9 more carry *deferred with a named answerer, or becomes an issue*, which the ladder does not contradict |
| `grep -rn "at most one more round record"` and `grep -rn "Unless th"` over `docs skills agents templates` | 4 hits, one per named file; 0 hits |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's one act and was not run in this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `chain_check.py`'s `CAPPED_EXIT` runtime message states the pre-ladder filing rule | already deferred by this branch — `overview.md` §*Not verified*. Reported here as the fifth site of finding 1's class, not as a new deferral | the repository owner |
| the 17 rows of `seal/ledger.md` whose cell count differs from their table header | already filed as #501 | the repository owner |

## Paste-ready fixes

🔴 1 — `docs/review-chain-spec.md:1324-1329`, replacing the paragraph:

```
**After a record that met the floor, at most one later record may close on a
fix.** That one is the verifying round that reopened the run; the record that
reads its fixes ends the run whatever it finds. There the run is `capped`:
every finding still open takes the ladder in §*Where a leftover goes — the
ladder, and why a new issue is not the default*, its verdict reads `deferred
<home>` wherever a home was found, the record's `Fixes checked by` reads `no
fixes to check`, and the pull request says `chain: capped`.
```

🔴 1 — `skills/code-review/orchestration.md:162-169`, replacing the clause
after the dash and keeping the link sentence that follows it:

```
later record may close on a fix, a second is refused, and the run ends
`capped` — every finding still open takes the filing ladder below, its
verdict reads `deferred <home>` wherever a home was found, the record's
`Fixes checked by` reads `no fixes to check`, and the pull request is
labelled `chain: capped`. `docs/review-chain-spec.md` §*The reopening — one,
and then the run is capped* owns the rule, the refusal and its cutoff.
```

🔴 1 — `skills/code-review/scripts/chain_check.py:227-230`, the module
docstring, replacing the sentence above the paragraph this branch added:

```
finding still open takes the filing ladder, its verdict reads `deferred
<home>`, the record's `Fixes checked by` reads `no fixes to check`, and the
pull request says `chain: capped`. `docs/review-chain-spec.md` §*Where a
leftover goes -- the ladder, and why a new issue is not the default* owns
where a filed finding goes. `deferred <home>` is a closing word for that and
not a fix word; the bare word stays open.
```

🔴 1 — `agents/smith.md:304-306`, if the smith does not answer it with
grounds:

```
not add mechanism at all — a rule, a checker, a template section, a walk —
and a finding closable only by one takes the ladder below rather than an
issue by default;
```

🟡 2 — `docs/review-chain-spec.md`, a paragraph after the one ending *it
costs nobody a question*:

```
**`New units` names Python units, so a finding in a document is answered by
the fix range instead.** `round_record.py`'s `measure` skips every prose path
whole, so a round whose fixes were documents writes `New units | none`
however much the branch wrote. There the evidence of ownership is the range
itself: a paragraph this run's own fixes added belongs to the branch on the
same test, read off the diff rather than off the row.
```

🟡 3 — `docs/review-chain-spec.md`, replacing the test paragraph under the
rung table:

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

🟡 4 — `docs/review-chain-spec.md`, in §*What the ladder is measured against*:

```
When this was written the `from-review` label carried 89 issues, 43 of them
closed — 48% — and 23 of the 46 still open had been opened inside one
three-day window.
```

🟡 4 — `docs/issues-and-milestones.md`, in the `from-review` paragraph:

```
`--label from-review --state all` beside `--state closed` gives the share of
filed findings anybody went on to act on, and that share is why the filing
decision is a ladder rather than a reflex: 43 of 89 were closed when the
ladder was written, and 23 of the 46 still open had been opened inside one
three-day window.
```

The same two numbers stand in `seal/specs/1790076060-…/changelog.md` and in
ledger row C5, and both take the same correction.

Needs a fix: yes — finding 1, the three live documents still stating that
every finding still open becomes an issue. Findings 2, 3 and 4 are fix or
grounds; 5 and 6 are corrections.
Loses a record or crashes: no — nothing found leaves the root or crashes.
The branch changes no gate, no checker arm and no parsed field, and both
Python diffs are comments and docstrings.

---

## Proof block

**Read** — `docs/review-chain-spec.md` (the new §*The cap bounds rounds*, the
new §*Where a leftover goes*, §*The reopening* 1318-1345),
`docs/issues-and-milestones.md`, `docs/review-handoff-protocol.md`,
`agents/warden.md`, `agents/smith.md`, `agents/sealer.md`,
`skills/code-review/orchestration.md`, `templates/sdd-round.md`,
`tests/test_the_rules_have_one_owner.py`,
`skills/code-review/scripts/chain_check.py` (`run_reopened`, `wrote_fixes`,
`stopping_floor` and its walk, `CAPPED_EXIT`),
`skills/code-review/scripts/round_record.py` (module docstring, `top_units`,
`measure`, `units_named_earlier`, `close`'s surface writer, `seal`'s
last-record refusal), `seal/follow-up.md`, `seal/ledger.md` (the 22 changed
rows), `seal/ledger/1790076060-…md`, the work item's `spec.md`, `plan.md`
excerpt, `questions.md`, `overview.md`, `changelog.md`,
`phases/phase-4.md`, `seal/specs/1790039346-…/rounds/round-6.md` and
`round-7.md`, `skills/settle/SKILL.md` (the removal lines).

**Executed** — the nine runs in `## Executed probes` above. No file was
written in the worktree except this report; no probe file was created, so
none was left behind.

**Unverified** — the broad gate, answered by the `sealer`.
