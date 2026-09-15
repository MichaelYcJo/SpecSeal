# Implementation Plan: the checker is wrong about itself, and nothing goes red

<!-- seal/specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-15 by the repository owner, when `smith` was spawned.

<!-- Fill this in at the spawn: reading this plan and spawning the builder IS
the approval. `routing.md` already records the routing batch the same way —
the verb, the date, who, and the moment it was given — and the two are pinned
against each other. -->

## Summary

Six tickets, three packages, six phases. Every phase ends with **a state that
is green today going red**, because that is the only thing that distinguishes
this work from the edits it is made of.

The order is not the ticket order and it is not arbitrary. Phase 1 repairs the
two readers that walk this repository's own 176 records, because those readers
are what every later phase is measured by — and one of them is the reader
`1ff0a6c` was written for. Phases 2 and 3 rebuild the seam that revert took
out. Phase 4 takes `seal`'s two defects together, in one module, in one order
that matters. Phases 5 and 6 take the two refusals that are wrong about
themselves.

**Nothing in this plan runs the broad gate.** `skills/agent-contract/SKILL.md`
§2 assigns it to `agents/sealer.md`, once, after the rounds settle.

## Technical context

### The seam #395 has to rebuild, and where the code for it is

`1ff0a6c` reverted two commits together. Both are readable:

- `7b2c0d7` — the verdict-column arm. It adds `OPEN_WORD = "open"` above
  `verdict_rows`, and an `elif` branch inside the row loop that appends to
  `owed` when the `#` cell commissioned nothing and the `Verdict` cell reads
  the open word. It also widens the `owed` refusal message to name the third
  way a row can owe an answer.
- `fec2c88` — the bound and the boundary. It adds `says_open(word)` and moves
  the arm's test onto it, and it repairs five carriers of the overturned claim.

**Read both with `git show` before writing anything.** The paste-ready blocks
in `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-4-report.md`
are the corrections **on top of** those two commits, not replacements for them.

### The boundary, stated precisely, because three readings are in play

`chain_check.verdict_of` ends a vocabulary word on **a space or a comma**:

    if s == word or s.startswith(word + " ") or s.startswith(word + ","):

`chain.SEPARATORS` is `" "`, an em dash, an en dash, `-`, `:` and `,` —
`chain_check.py:497`. It is **not** what `verdict_of` uses, and five carriers
say it is. Three readings, and only the third satisfies every carrier:

| Reading | `open` | `open — deferred` | `open, comment only` | `open-ended question` | `open: see 5` | `opened in round 2` |
|---|---|---|---|---|---|---|
| equality (`7b2c0d7`) | yes | no | no | no | no | no |
| `chain.SEPARATORS` (`fec2c88`) | yes | yes | yes | **yes — wrong** | **yes — wrong** | no |
| space or comma (**chosen**) | yes | yes | yes | no | no | no |

The third is also the one that decouples the open verdict from a constant five
other readers share. That coupling is why S5 of `spec.md` exists as a scenario
of its own: a boundary change alone leaves the coupling in place, and the next
session to widen `SEPARATORS` for an unrelated reader widens this silently.

### `seal` already knows which record it is holding

    reader, routing, root, _item, rounds = where(args)
    n, path = last_record(routing, rounds)

`last_record`'s own docstring is *(N, path) of the highest-numbered `round-N.md`
on disk*. The lastness is not inferred from the repository at the predicate —
it is the **selection criterion of the line above it**. This decides #335; see
below.

### #335 closes the cheapest route to the state #334 needs

This is the one cross-ticket interaction in the work item, and it is invisible
from either ticket.

`broad_gate.py` discriminates two endings of `seal`:

- a refusal **before** the write → no `round-record: sealed` line → the gate
  says *no cell was written*;
- the cell written, and the chain check `seal` runs **after** the write then
  fails → a `round-record: sealed` line **is** printed → the gate says *the
  cell WAS written*.

#334's repair is a case over the **real** pair, which means it needs a fixture
that genuinely reaches the second state. Today the easiest way to reach it is
#335's own defect: put `round-1` in a last record's `Fixes checked by`, and
`seal` writes the cell and the chain check refuses that same row. **Phase 4
removes that route.** So the phase takes both tickets and must name a second
route to the written-then-refused state — a record whose cell `seal` accepts
and whose chain state the check refuses for an unrelated reason (a stray
record under `rounds/`, a `Target SHA` git cannot resolve, an earlier record's
row). Whichever route is chosen is asserted as the route, so the case does not
quietly stop reaching the state it was written for.

### Two tickets cite a sentence to a file that does not hold it

#333 and #334 both attribute to `templates/sdd-round.md`:

> A refusal is read by whoever is stopped by it, so the half that says what to
> do is the half that has to survive a reword

**`templates/sdd-round.md` does not contain it** — that file holds no
occurrence of the word `reword` at all. `skills/implement/SKILL.md` §1 says to
verify clause numbers a ticket cites, and this is that check firing.

**Where the sentence does live**, measured 2026-09-15 over the whole tree,
case-insensitive and whitespace-normalised so a line wrap cannot hide it:

| File | Wording |
|---|---|
| `seal/follow-up.md` §*Schedulable items with nowhere else to go*, inside the row about the unparseable `Broad gate` cell | the sentence exactly as the tickets quote it, with **so** |
| `tests/test_a_release_cannot_ship_an_untrue_milestone.py#test_the_refusal_says_what_to_do_about_it` | the docstring, with **and** in place of *so* |

Two hits, nowhere else.

**Neither of those is a home a citation should rest on, and that is the point
for smith.** `seal/follow-up.md` is a scheduling list — its own opening says
what belongs in it — and a test docstring is not policy either. The principle
*is* ratified, in `docs/`, in its own words, and those are the two coordinates
to cite:

- `docs/review-chain-spec.md` §*The depth in `New units`* — **The refusal names
  the exit because a refusal that does not is a wall.** This is the one that
  bears on #333, because it is the depth rule's own paragraph.
- `docs/review-handoff-protocol.md` §*The fix-surface rows — what the fixes
  changed, and what they created* — *a refusal with no exit stops the chain
  rather than the unit*.

So the instruction is **cite the ratified wording**, not *move the sentence to
a new home*. The work the tickets ask for is unchanged; only what smith quotes
in a comment or a docstring changes.

**Do not repair the tickets by adding the sentence to `templates/sdd-round.md`.**
That would make a mis-citation true by moving the tree, which is this work
item's own defect class.

### One half of #142 is already closed, and the ticket does not know

#142 says the lister *sorts before filtering, so `round-2-draft.md` raises
`TypeError`*. **The name it gives that sort is not the sort that could raise
it**, and the two halves have to be kept apart or the phase writes a case for a
crash that cannot happen.

| Where | What it actually does |
|---|---|
| `_real_records` itself, both copies (`tests/test_chain_check_at_the_pull_request.py`, `tests/test_the_reopening_is_one.py`) | `return sorted(p for p in out.split("\0") if p)` — a **plain path-string sort**. It sorts before any filtering, exactly as #142 says, and it cannot raise: every element is a string. |
| The caller in each module (`:1816` and `:442`) | `sorted(rels, key=lambda r: routing.round_number(...))` — the **numeric** sort, which is the one that raises on a `None`. In both modules the `round_number is not None` filter runs **before** it. |
| `tests/test_a_finding_id_is_a_bare_integer.py` | filters on `round_number`, and never sorts numerically at all. |

So the crash is absent by a conjunction rather than by one repair: the sort
inside `_real_records` is not keyed, and the keyed sort downstream is filtered
first. `tests/test_chain_check_at_the_pull_request.py` carries a comment saying
the `TypeError` happened and that this was the reader that did not drop the
siblings; its filter landed 2026-09-08 in `14c2a57` (#234), four days after
#142 was opened on 2026-09-04.

**What phase 1 must not do is read #142's clause as naming the string sort and
"fix" it.** The clause is stale about the outcome and imprecise about the
mechanism, and the phase says both in `phases/phase-1.md` rather than leaving
the ticket's row looking unanswered.

Read, not executed. Q2 of `questions.md` is the measurement that confirms it.

### Where this work item's durable rows go

| What | Where | Note |
|---|---|---|
| Evidence rows | `seal/ledger/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red.md` | The directory does not exist yet — 0.11.4's release folded the last fragments away. Creating it is the fragment's own first write. No header: every row carries its own anchor. |
| Changelog entry | `seal/specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/changelog.md` | Never `CHANGELOG.md`'s `## Unreleased`. |

**Neither `seal/ledger.md` nor `CHANGELOG.md` is appended to.** One shared-ledger
row is adjacent and must not be appended to: `seal/ledger.md` S12 (`broad_gate.py#gate`,
`broad_gate.py#seal_record`, and the stubbed case) states three coordinates all
on the *reading* side of #334's seam. This work adds a coordinate on the
*writing* side; that is a new claim in the branch's own fragment, not an
amendment to a standing row, and nothing this work does removes that row's
anchors.

`plan.md` names these. It does not write them.

### The drift this work will cause in the shared ledger, counted before it happens

**Appending to `seal/ledger.md` is forbidden. Re-stamping a row this work
drifts is not, and it is not optional.** A ledger anchor is content-derived, so
changing a unit moves its hash and the row degrades to DRIFTED, which means
*re-read the claim and say whether it still holds*. That edit lands in
`seal/ledger.md` because that is where the row is, and the file already carries
the precedent in its own text — several rows end with *Re-read 2026-09-14 by
work item 1789356180 … which drifted this anchor*.

Counted on the shared file today, by unit this work changes:

| Phase | Units it moves | Shared-ledger rows anchored there |
|---|---|---|
| 2 | `verdict_rows`, `finding_number`, `build`, `id_refusal` | 1 + 2 + 4 + 1 |
| 3 | `finding_number`'s docstring, `id_refusal` | as above |
| 4 | `seal`, `last_record`; `broad_gate.py#gate`, `#seal_record` if touched | 3 + 1 + 3 + 1 |
| 5 | `depth_two`, `close` | 1 + 2 |
| 6 | `inherited_rows`, `close`, `new` | 1 + 2 + 2 |

Two of those rows make claims this work changes rather than merely moves, and
they are re-read on their substance, not re-stamped: **R2**, which asserts
*`close` … refuses a depth-2 unit before any cell is written* and is anchored
on `depth_two` (phase 5 changes what the refusal says, not when it fires — so
the claim holds and the note says why), and **S12 at `seal/ledger.md`**, whose
three coordinates are the reading side of the seam phase 4 binds.

**Do this at a phase boundary, in one write**, not one edit per row — the
`implement` skill's *draft as you go, write in one pass*. `evidence-check
--reverify` recomputes and names what it changed; a re-stamp with no re-read
behind it is the failure the Checked column exists to prevent.

## The two judgments — decided here, with the document that decides each

Both tickets state a judgment and refuse to settle it. Neither needed a person:
the documents answer both, which is `skills/implement/SKILL.md` §1's test.

### #335 — may `seal` know that the record it is holding is the last one?

**Yes. `round-N` is refused on a last record, and `no fixes to check` becomes
the only value `seal` accepts.**

**The document that decides it is `docs/review-handoff-protocol.md`**, §*The
Fixes checked by field — who opened the closing*:

> Only a later round may be named, so the **last** record of a finished run can
> only read `no fixes to check` or `nobody — <why>`. That is the shape of the
> rule rather than a limitation of it.

> Reading only the last record makes `round-N` unreachable — a checker has to
> be later, and the last record has no later round.

`docs/review-chain-spec.md` §*What the record carries* says the same twice, and
`skills/code-review/orchestration.md`'s three-value table says a `round-N`
*has to exist, a round can never name itself, and its own `Target SHA` has to
be later than this record's*. So the rule is already stated **about the last
record**, in ratified policy, in three documents. Enforcing it where the value
is written is not a new inference.

**The argument this overturns, and where the quote actually comes from.**
Issue #335's body introduces it as *written in that work item's records* and
quotes it. Searched 2026-09-15 over the whole tree, case-insensitive and
whitespace-normalised, on three separate fragments of it — `no grounds to
derive`, `pins into a subcommand`, `gives the same answer today` — **it
resolves in no file in the repository.** So it is the tracker's wording about
#30's reasoning, not a passage anybody can open in `seal/specs/`, and it is
cited here as what it is. The answer below does not depend on its provenance;
it is answered on the merits either way.

> refusing everything but `no fixes to check` gives the same answer today, but
> it pins into a subcommand a conclusion `chain_check.checked_by` derives from
> the repository, and `seal` has no grounds to derive it.

It has two grounds, and neither is a derivation. First, `seal` does not
*derive* lastness — it **selects by it**, on the line above the predicate
(`n, path = last_record(routing, rounds)`), and a subcommand whose whole
docstring reads *Set the LAST record's `Broad gate` cell* is not importing a
fact when it uses the one it chose the file with. Second, both parties are
reading the same ratified sentence rather than one copying the other's
conclusion — which is what `docs/review-chain-spec.md` §*Where the numbering is
chosen is where the rule is stated* asks for: *not only at the point of
refusal*.

**What it gives up, stated rather than left to be found.** The refusal's own
sentence — *The row holds one of three values* — stops being true at the place
it is printed, so §14 applies and the new text is pinned in the same commit.
And `nobody — <why>`, which the protocol allows on a last record, stays refused
by `seal`: `seal` runs with `Pass` ticked, and `orchestration.md` says `nobody`
beside a checked `Pass` on the run's last record fails the pull request. `seal`
refusing it keeps the cell out of a state its own check rejects, which is the
subcommand's stated promise.

**Failure direction: blocks more.** A last record whose cell honestly reads
`no fixes to check` is unaffected — the docstring already notes *a capped run
reads `no fixes to check` here, so this costs it nothing*. **Prompt budget:
zero.** The refusal replaces a refusal, one step earlier and without a written
cell; nothing new reaches a person.

### #333 — should the refusal still fire when the attribution is only file-level?

**Yes. It fires, and the message says the attribution is file-level and names
every candidate finding rather than asserting one.**

**The documents that decide it are two, and they decide different halves.**

*That it fires* is decided by `docs/review-chain-spec.md`'s own depth table,
which already chose this direction for the neighbouring case:

> | an entry below depth 1 | **fails** — it names no level the rule defines,
> and read permissively it sits under the bound |

The same document takes the same direction for every verdict it cannot read —
*A bare `deferred` … stays OPEN — the direction every verdict the checker
cannot read takes* — and `chain_check.py` states the cost of the other
direction in as many words: the permissive reading is *the wrong direction for
the only enforcement left*. `CONTRIBUTING.md` §*What a change to a gate must
carry* supplies the asymmetry: a wrong deny costs a prompt, and a wrong allow
here ships a depth-2 unit that, by `skills/code-review/orchestration.md` §*A
fix pass adds the unit that pins it*, **is read by nobody**.

*That the message must change* is decided by `templates/sdd-round.md`:

> The depth goes per entry rather than in a row of its own, because a single
> fix pass can answer a finding in code that predates the run and a finding
> inside an earlier unit in the same breath, so one number for the whole round
> would be false of one of them.

A per-file answer is structurally unable to produce what the record is required
to state per entry. So the repair is not *stop firing*; it is *stop asserting a
per-entry fact the walk did not establish*.

**Why the one countervailing precedent does not reach.**
`docs/review-chain-spec.md` deliberately chose `allow` once, for the pending
fix-surface arm, and gave its reason: *a rule about which English sentences
mean not yet is the enumeration over an unbounded domain*. #333's domain is
bounded — a fix range, its commits, its units. And
`round_record.py`'s own use of `CLAUDE.md`'s first goal to *avoid* a refusal
(*a refusal here would stop an unattended run over the legitimate case to
catch the unlikely one*) does not reach either: this refusal fires only where a
range **both** adds a unit to a file **and** carries a `fixed` row whose
Location is inside a unit an earlier record's `New units` names. That
conjunction has fired once, on #30, and it was correct.

**Failure direction: blocks more, and unchanged from today** — file-level
attribution already refuses. What changes is the sentence. **Prompt budget:
zero added.** The exit the message names is unchanged and already stated:
`deferred with a named answerer, or becomes an issue`.

## #331's trap, and how the new figure is taken

#395's docstring figure is **the sixth wrong measurement in this release**,
across four work items and four authors, and every one was an aggregate taken
without opening the coordinates. This one is the first taken *with the module's
own reader* and still wrong — which matters, because *use the module's reader*
is the repair everybody has reached for.

So the replacement is not *re-run the reader*. It carries four things, in the
docstring, beside the number:

1. **The population, named exactly.** Round 4 measured six populations looking
   for 127 and none yields it — records alone give 95, records plus this work
   item's reports give 108, records plus every report in the tree give 570. A
   figure whose population is unstated is unfalsifiable, and that is what let
   `127` stand. Write *committed `round-N.md` records that parse*, not *the
   records*.
2. **The date it was taken**, because the corpus grows.
3. **The reader it was taken through**, by name (`table_body`, or
   `chain_check`'s verdict reader), so the next person re-derives it the same
   way rather than a defensible different way.
4. **Every figure in the sentence re-derived at the same commit in the same
   pass** — not only the one that was wrong. The two neighbouring claims (*15
   of 25 admitted rows outside `CLOSED_WORDS`*, *0 newly refused*) reproduce
   today, and re-deriving them together is what makes the triple one
   measurement instead of three of different ages.

**The figure is a claim, so it takes a ledger row**, in this work item's
fragment, with the command in the evidence cell. §5 of the contract: an
aggregate is not a coordinate — the number can be checked while the claim it
stands for cannot — so the row exists to give the number a coordinate somebody
can reopen.

**What must not happen:** carrying `95 / 7 / 88 over 1,704 rows` across from
round 4's report. That figure was taken at `151792e` against a corpus this
branch has already grown, and copying it is the sixth failure repeated with a
different number.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#395: correct the five carriers to say `chain.SEPARATORS` instead of narrowing the test** | The code keeps over-refusing `open-ended question` and `open: see 5`, and the open verdict stays coupled to a constant five other readers share — so widening `SEPARATORS` for any of them silently widens this. Five rewrites buy a worse behaviour. | **Rejected.** Round 4 executed the narrow test: it reaches all 95 committed cells, excludes both over-refusals, and leaves both modules green. One change makes five sentences true. |
| **#395: ship the four prose fixes only, leaving the seam reverted** | The verdict-column arm is what the ticket's second comment widened the scope to carry. Without it there is no `says_open`, no `OPEN_WORD`, and no case to repair — three of the four "fixes" have no code to apply to, and the defect round 2 opened (a row whose Verdict reads `open` admitted at exit 0 with `Pass` ticked) stays shipped. | **Rejected.** The ticket's body and its second comment disagree; the comment is later and is the owner's widening. |
| **#342: drop the verdict word from the `Why` cell entirely** | Honours *coordinates carry; conclusions do not* and needs no new reach. But the word is what tells the fix pass what it is reopening, and rounds older than N-1 carry words that are already final and correct — so this discards accurate information from every earlier round to fix staleness that reaches one round's rows. | **Rejected**, and recorded here because it is the reading the template's own sentence invites. |
| **#342: order `close --round N-1` before `new --round N`, so the inheritance reads closed words** | Costs no code at all. But it makes correctness depend on an orchestration order nothing enforces: a run that spawns the verifying round first reproduces the defect silently, and the generator cannot tell it happened. `docs/review-chain-spec.md`'s ordering rule requires the record committed **before** its fixes exist, so the two orders are both reachable by design. | **Rejected** as the whole repair. May still be stated as guidance; the code must not depend on it. |
| **#342: reach forward from `close` into round N's inherited rows** | `close` writes into a file other than the one it was given. That is new for `close` and not new for the generator — `new` already reaches back into round N-1 through `reach_back`, refusing rather than guessing when the cell is unreadable or already names a different round. The same refusal shape carries. | **Chosen.** Symmetric with the reach that exists, independent of spawn order, and it refuses loudly where it cannot act. |
| **#334: a shared constant the two packages both import** | The two files sit in different skill packages and neither imports the other; `broad_gate.py` reaches `round_record.py` by path and runs it as a subprocess. A shared name means deciding where a constant lives that two packages read, and the tree has no precedent for it — a design argument this release has no room for. | **Rejected**, as the ticket argues. |
| **#334: a case over the real pair** | Costs a fixture and depends on a reachable written-then-refused state, which phase 4 must name because #335 removes the current one. It binds the behaviour rather than the token, which is the shape this repository has reached for before. | **Chosen.** |
| **#333: refuse only on an exact commit-level match** | Silent where a fix pass answers two findings in one commit, which is a shape `skills/implement/SKILL.md` neither forbids nor makes rare — it asks for a commit at the smallest step that stands on its own, not one commit per finding. A genuine depth-2 unit then ships unreviewed, and the ticket says so: *refusing only on an exact match would have let it through if the commits had been squashed differently*. | **Rejected.** See §*The two judgments*. |
| **#142: assert on the same loop harder** | The ticket forecloses it: *what closes it is a positive control through the same call path — a fixture record known to be refused, asserted to produce a failure — not another assertion on the same loop*. An assertion that reads the same `failures` list cannot distinguish an empty list from a loop that never ran. | **Rejected.** |
| **Six work items, one per ticket** | Six routing declarations, six frames, six review chains, for six instances of one cause in three files that two review rounds found together. And #334/#335's interaction is invisible from either ticket, so two of the six would be built against each other. | **Rejected.** |

## Phases

Vertical slices. Each ends with something runnable and verified, and the
**Verified by** column names what a `smith` runs — narrow, at the phase
boundary, never the broad gate.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| **1** | **#142 and its class.** Both `_real_records` copies read HEAD via `git ls-tree -r -z --name-only HEAD -- seal/specs` with a `fullmatch`, so a staged-uncommitted record is not listed-and-skipped; the third corpus reader in `tests/test_a_finding_id_is_a_bare_integer.py` is assessed and repaired or named with the reason; the positive control lands — a fixture record known to be refused, asserted to produce a failure through the same call path. The stale `TypeError` clause is answered in the record rather than coded around. | `tests/test_chain_check_at_the_pull_request.py`, `tests/test_the_reopening_is_one.py`, `tests/test_a_finding_id_is_a_bare_integer.py`. **§15 is shown by mutation**: both `failures.extend(errors)` replaced with `pass` must turn a case red, and the handover says so. | `f3b3b62`, `4f4d653` |
| **2** | **#395's behaviour.** The verdict-column arm from `7b2c0d7` is back, bounded at `VERDICT_COL` (not the header width), with the open word ended on **a space or a comma**. Six shapes refused; the four-cell row that merely lacks its grounds still written short at exit 0; `new` and `close` both refuse a numbered short row at exit 2 rather than raising `IndexError`. The `assert code in (0, 2)` hedge becomes one answer. A case pins that widening `chain.SEPARATORS` does not widen the open verdict. | `tests/test_a_finding_id_is_a_bare_integer.py`, then `tests/test_chain_check_at_the_pull_request.py` and `tests/test_the_reopening_is_one.py` — **phase 1's repaired walkers over this repository's own records are the check that `1ff0a6c` was written for**, and they run here, at this phase's boundary, not at the pull request. | `2901671` |
| **3** | **#395's prose and its figure.** The docstring measurement is re-taken by the method in §*#331's trap*, with population, date and reader beside it, and all three figures of the sentence re-derived in one pass. `OPEN_WORD`'s comment stops describing the exact match that was replaced. The boundary claim is made accurate in every carrier (`round_record.py` ×2, `docs/review-chain-spec.md`, the case docstring, and the shared-ledger sentence — the last **as a new row in this work item's fragment**, not an edit to `seal/ledger.md`). The short-row guard's single-row raise gets the sentence ⬜ 5 asked for; the three-word line from the rewrap is closed. | `tests/test_the_rules_have_one_owner.py`, `tests/test_a_finding_id_is_a_bare_integer.py`, `tests/test_docs_line_wrap.py`. The figure itself is verified by re-running the named reader and quoting the command. | `dd6af99` |
| **4** | **#335 and #334 together, in one module and in this order.** First: `seal` refuses `round-N` on a last record **before** the write — four values (`round-1`, `round-9`, `round-2.md`, `ROUND-1`), each exiting 2 with no cell written and no `round-record: sealed` line; the refusal's three-value sentence is rewritten and pinned (§14). Then: the case over the real pair — the real `seal` against a fixture record in each of the two endings, asserting what the gate prints, with the second route to the written-then-refused state named and asserted as the route. | `tests/test_the_seal_is_taken_once_by_the_sealer.py`. **The mutation is the acceptance**: change `round_record.py`'s `sealed` print to any other word and a case must go red, where 130 pass today. | `ed0dc56` |
| **5** | **#333.** `depth_two` attributes a unit to the row whose fix commit added it, using the commits `close` already resolves for the fix table, and falls back to the file-level answer only where a range cannot resolve one. The refusal still fires on the fallback, and its message says the attribution is file-level and names every candidate finding rather than asserting one. The exit sentence is unchanged. | `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, `tests/test_the_fixes_close_the_record.py`. Cases built on the measured #30 shape (two findings in one file, each inside a round-1 unit) and on a single-commit range that forces the fallback. | `703cf9c` |
| **6** | **#342.** `close --round N-1` reaches forward into `round-N.md`'s `## Inherited coordinates` and brings the rows inherited from round N-1 to the words that round's verdict cells now carry, printing what it filled the way it already prints `Contract changes` and `New units`. It refuses rather than guesses where the record is unreadable or the rows are absent, and says nothing where round N does not exist yet. | `tests/test_the_record_is_generated.py`, `tests/test_the_fixes_close_the_record.py`. A two-record fixture: close N-1, read N, assert the words agree — red against the tree today. | |

**Status is empty, or the commit that closed the phase.** A tick is refused and
so is `done`. Re-read this column after any rebase.

**What a phase discovers and the next phase needs** goes to
`seal/specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

### Why the phases group this way

Not by ticket number, and not one per ticket. Three things decided the
grouping, and each moved a boundary:

- **Phase 1 is first because it is the instrument.** The two walkers over this
  repository's own records are what say whether phases 2–6 broke the tree, and
  `1ff0a6c` exists because that answer arrived at a broad gate rather than at a
  phase boundary. Repairing the instrument before using it is the whole
  ordering argument.
- **Phases 4, 5 and 6 are one module each.** `test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_the_record_is_held_to_the_floor_and_the_depth.py`,
  `test_the_record_is_generated.py`. A phase whose verification is one module
  is one narrow run; two tickets in one module is one phase (#335 + #334), and
  two tickets in one file but two modules is two (#333, #342).
- **Phases 2 and 3 split behaviour from prose** because the prose depends on
  the behaviour: what the docstring should say about the boundary is not
  decidable until the boundary is chosen, and the figure cannot be re-taken
  until the reader it is taken through is the reader that ships.

### The rule that keeps the pinning units out of a review round

`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it,
and that unit ships unreviewed* forbids a fix pass to add mechanism, and **two
of this work item's repairs are mechanism**: #334's case over the real pair,
and #142's positive control. Both are new units.

They are in phases 1 and 4 for that reason. A round that finds them missing can
only defer them to an issue, and this work item would ship with the two things
it exists to add sitting in the tracker.

## Operational impact

No migration, no new environment variable, no new dependency.

**Compatibility, and it is the row a reader will miss.** After phase 4, a last
record whose `Fixes checked by` reads `round-N` can no longer be sealed. No
committed record in this repository is in that state — the value is refused by
`chain_check` today, which is the whole of #335 — but a **user's** repository
mid-run could be, and what they meet is a refusal at exit 2 where they
previously met a written cell and a failing check one step later. That is
strictly the better message and it is a behaviour change; the changelog
fragment says so in the user's words, and the refusal says what to write
instead.

**Prompt budget for the work item: zero added.** No phase puts a new question
in front of a person. Every refusal this work adds or rewrites replaces a
refusal, a traceback, or a silent pass.
