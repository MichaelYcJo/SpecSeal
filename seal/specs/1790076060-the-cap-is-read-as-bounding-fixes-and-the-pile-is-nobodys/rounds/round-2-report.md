# Round 2 — review report

| Field | Value |
|---|---|
| Work item | `1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys` |
| Branch | `docs/492-the-cap-bounds-rounds-not-fixes` |
| Target SHA | `0fa02520b0325170e55bc0010094cfe38df921ee` |
| Base | `origin/release/v0.13.1` at `6d41002398bfeeb55db08cca9b441b68e0267049` |
| PR | #502 |
| Round | 2 — the verifying round, at the diff of round 1's fixes |

The target was `4ddfde2ee12e99759f22e67efcd65264a96ec0b2..9d9180f8`, two commits.
Round 1's `New units` reads `none` and `Contract changes` reads `none`, so the
range adds no unreviewed finding surface and the round is the answers.

Round 1's verdicts are inherited. Its coordinates were opened rather than
re-found; its conclusions were re-derived, and one of them — that the nine
carriers of *deferred with a named answerer, or becomes an issue* are outside
the class — rested on ground the fix pass then changed, so it is re-derived
below rather than carried.

## What the fix pass claimed, and what I found

- **Claimed**: the class was three sites wider than round 1 found, and after
  the pass no live document tells a reader that a finding still open at a
  capped exit becomes an issue. **Confirmed for the capped exit**, by an
  enumeration of my own. **Narrowed for the class**: three of the seven sites
  are the *depth* exit, a different rule with a different owner, and that
  rule's other spelling still stands in thirteen live places. Below.
- **Claimed**: the paste-ready text would have reddened two pins, so it was
  adapted. **Confirmed, and both pins pass for the reason they exist** —
  executed, exit 0.
- **Claimed**: an empty `New units` is not evidence, and the fix range is the
  evidence instead. **Confirmed.** The new paragraph states the gap rather
  than papering over it, and names a coordinate a reader at a capped exit
  already has.
- **Claimed**: rung 3 is agreement rather than naming, with no count in the
  shipped text. **Confirmed on both halves**, with one sentence pulling
  against the paragraph that follows it (⬜ below).
- **Claimed**: the measurement is dated and attributed in four carriers that
  agree. **Confirmed for the four.** Two further carriers still read the old
  share (⬜ below).
- **Claimed**: each `survivors.md` row returns its grounds on the text as it
  stands, and nothing once its quoted run is broken, so it degrades to
  *reported again*. **Confirmed at the tree the rows were written against,
  and false at the tree that ships them.** Committing the file removes the
  three survivors from the check entirely. That is 🟡 1.

## 🟡 1 — the survivors file disarms the check for the survivors it records

`skills/code-review/scripts/survivor_check.py:566-571` (`wanted`), against its
own §*What is excluded, by construction rather than by list* at lines 63-81;
`.github/workflows/hygiene.yml:254`

The degradation property the rows rest on is real, and I reproduced it at the
commit they were written against. At `4ddfde2e..9f8efea4` the check finds three
candidates, all three are excused by name, and the report closes with `every
survivor is excused by a row above (3)`. Breaking one row's quote drops that row
out, reports its candidate again and exits 1. That half of the claim holds.

At the range this record names it does not hold. At
`4ddfde2e..9d9180f8` — the same tree plus `survivors.md` and nothing else — the
check finds **zero** candidates and prints `no removed wording is still
standing`, with the exemption file and without it. The same is true at the form
CI runs, `origin/<base>...HEAD`. The candidate does not fall below the floor: at
`--floor 1.0` it is absent from the list altogether.

`wanted` is why:

> ```
> def wanted(gone, written):
>     """The n-grams worth looking for: removed, and not written back."""
> ```

`survivors.md` is added by the range and quotes the surviving wording verbatim —
the quote is the anchor, so it always does. Every n-gram of the survivor
therefore lands in `written`, is subtracted from the removed set, and the
places carrying it stop being reachable.

**This is #365's defect one file over, and the module already documents it.**
Its §*What is excluded* says a round record and a reviewer's report "quote the
defective wording verbatim — that is what they are for", and that the exclusion
had to cover "both sides of the range's path list, not its added side alone".
`survivors.md` sits in `seal/specs/<id>/`, not in `rounds/`, so it is on the
added side and excluded by nothing.

**Why it matters, and who meets it.** `spec.md` A11 is *`survivor-check`
against the base, and its report read line by line*. Taken against the base on
the tree that ships, that report reads `no removed wording is still standing` —
which the module's own comment at lines 975-979 says is the false one of the
two facts it was built to tell apart. The grounds three rows carry are read by
nothing, and the hygiene step on every pull request into a release branch exits
0 having measured none of them. Thirty-three `survivors.md` files already stand
in this tree, so this is the tool's defect and not this branch's — but this
branch is where it is visible, and nothing in the tree records it.

**What this branch can do, and what it cannot.** Adding `survivors.md` to the
exclusion is a change to what a checker measures, which `spec.md` §Out refuses
by name. So the answer here is grounds plus a disclosure, and the repair itself
belongs to an issue.

## 🟡 2 — a second runtime message went imprecise, and only the first is disclosed

`skills/code-review/scripts/round_record.py:2569` (`DEPTH_EXIT`), and the same
sentence at `skills/code-review/scripts/chain_check.py:2648-2649` and `:3355`;
against `seal/specs/…/overview.md` §*Not verified*

The branch's ladder made `CAPPED_EXIT` imprecise, and `overview.md` discloses
that with the repository owner named. The fix pass then rewrote the *depth*
exit's destination in three live documents — `agents/smith.md:305-306`,
`skills/code-review/orchestration.md:244-247`, `skills/implement/SKILL.md:553-556`
— which is the branch deciding that this rule's destination is in the class
too. The constant that prints that rule's destination to a person was not
disclosed:

> ```
> DEPTH_EXIT = "deferred with a named answerer, or becomes an issue"
> ```

`close` prints it when it refuses a depth-2 unit, and `chain_check.py` prints
the same sentence at two more refusals. Under the ladder a finding there may
take rung 4 instead, so the message is now imprecise in exactly the way
`CAPPED_EXIT` is — and a fix pass that reads it at the moment of refusal is
told to open an issue, which is the pile #493 was raised against.

**The class, re-enumerated by a different construction.** I built the
enumeration as co-occurrence over two vocabularies rather than as a needle
list: every occurrence of an issue-destination token in a flattened live
carrier whose ±220-character window also carries an open-finding or exit
token, over `docs`, `skills`, `agents`, `templates`, `CLAUDE.md`,
`CONTRIBUTING.md` and both READMEs. It returns 56 hits. Read one at a time:

- **For the capped exit, seven is the number and the answer is clean.** No live
  document now states the filing unconditionally at a capped exit; the only
  site left is `CAPPED_EXIT`, which is disclosed. Confirmed independently.
- **For the depth exit it is not a count of one class.** The sibling spelling
  stands at thirteen sites in seven files:
  `docs/review-handoff-protocol.md:412`, `docs/review-chain-spec.md:127` and
  `:1466`, `skills/code-review/orchestration.md:194`, `:238` and `:319`,
  `skills/code-review/scripts/chain_check.py:170`, `:2648` and `:3355`,
  `templates/sdd-round.md:171` and `:214`,
  `skills/code-review/scripts/round_record.py:2569`, `agents/smith.md:287`.

Ten of the thirteen are prose that points at a ladder paragraph standing near
it, so a reader who follows the pointer gets the right rule; those are house
shape rather than a defect. The three that point at nothing are the runtime
messages, and they are the ones a person reads and acts on. Ledger row C6
records the sweep rather than a carrier list, which is the right call — what
the row does not say is that the sweep's needles reach one spelling of the
destination and not the other.

## ⬜ — `spec.md` calls a section Unchanged that the fix pass changed

`seal/specs/…/spec.md` §Grounding, the `skills/code-review/orchestration.md`
row, and §Out's fifth bullet; `seal/specs/…/overview.md` §*Fed back into the
spec*

The Grounding table says of §*A fix pass adds the unit that pins it, and that
unit ships unreviewed*: **Unchanged**, and §Out says of rule 1 of #493's two,
*this work does not touch it*. The build honoured that — `git diff
6d410023..4ddfde2e` over that file touches none of it. Round 1's fix pass then
changed the section, and the same rule's sentence in two of its carriers.

The change itself is defensible: Scope In 4 states the ladder as the general
rule, and round 1's finding 1 asked for it by coordinate. What is missing is
the record of the divergence. `overview.md` §*Fed back into the spec* reads
`none`, and §*Where spec and implementation diverged* carries one row that is
about something else. A reader comparing the spec with the tree finds a
contradiction and no note saying which side moved.

## ⬜ — `survivors.md`'s header states a count no run at this range produces

`seal/specs/…/survivors.md`, the comment header

It reads *`survivor-check` over the fix range reports three places still
carrying the wording it removed*. That is true of round 1's fix range, the one
commit `4ddfde2e..9f8efea4`. It is false of the two-commit range this record
names, where the same command reports zero, and false at CI's range. Written
against a tree that no longer exists, in a file whose whole purpose is to be
re-read later.

## ⬜ — two carriers still read the old share

`seal/specs/…/questions.md` Q1, the Options cell; `seal/specs/…/overview.md:12`

The four carriers claim 5 names agree, are dated and are re-derivable: 89
issues, 43 closed, 48%, 46 open, on 2026-09-22, this run's own issue excluded.
The share and the open count are no longer one numeral. Verified in
`docs/review-chain-spec.md:294-301`, `docs/issues-and-milestones.md:86-88`, the
changelog fragment and ledger row C5, which carries `Corrected 2026-09-22`.

Two more carriers state the gap as the branch's own claim and still read the
old figure. `questions.md` Q1's Options cell reads *the 47% gap stays the
pile*, in the same row whose Default cell the fix pass rewrote.
`overview.md:12` reads *acting on one ran at 47%*, which is the sentence the
changelog fragment carries corrected to 48%. The copies in `spec.md:9`,
`routing.md:20` and `plan.md:62` are attributed to #493's own count and are
history, so they are right as they stand.

## ⬜ — rung 3's test paragraph opens against its own conclusion

`docs/review-chain-spec.md:273-285`

The paragraph now does the work: it says an owner written because there was
nobody else to write is rung 4's answer, gives the tell a reader applies, and
quotes no count. The rung table's own row 3 reads *the finding names a party
who will act on it*, which is the agreement form. A reader can apply it.

What pulls against it is the bolded opening, kept from the earlier text:
*\*\*The test is the one `seal/follow-up.md` already applies to itself\*\*: the
row names a person, with no condition attached* — and eight lines later, *it
is why naming is not the test*. The bold is the part that scans. Nothing is
wrong behind it and the rule ships right, so this is a sentence that reads
badly rather than a defect.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | committing `survivors.md` subtracts its own quoted wording from the removed set, so the three rows silence nothing and the check exits 0 having measured none of them | `skills/code-review/scripts/survivor_check.py#wanted`; `.github/workflows/hygiene.yml:254` | open | Executed at five ranges: 3 excused at `4ddfde2e..9f8efea4`, 0 candidates at `4ddfde2e..9d9180f8` and at `6d410023...HEAD`, absent at `--floor 1.0`, and reported again when a row's quote is broken. The two trees differ by `survivors.md` alone. The repair is a checker change, which `spec.md` §Out refuses, so the home is an issue |
| 🟡 2 | the depth exit's runtime message is imprecise under the ladder in the same way `CAPPED_EXIT` is, and `overview.md` discloses only the first | `skills/code-review/scripts/round_record.py#DEPTH_EXIT`; `skills/code-review/scripts/chain_check.py:2648` and `:3355`; `seal/specs/…/overview.md` §*Not verified* | open | Read. The fix pass rewrote this rule's destination in three live documents, so the branch treats it as in the class; the constant that prints it to a person was left, correctly, and named nowhere. Same grounds as `CAPPED_EXIT`, so the owed act is the disclosure row and not the reword |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a `survivors.md` added by the range subtracts its own quoted wording from the removed set, so the check reports success having measured nothing — #365's defect on a path the exclusion does not cover | a new issue — rung 3. The finding names a defect in the repository's own gate whose class already cost a release, so it gives its answerer a reason to act. The repair is a checker change `spec.md` §Out refuses on this branch | the repository owner |
| whether the depth exit's runtime message should be reworded to the ladder | `seal/specs/…/overview.md` §*Not verified*, beside the `CAPPED_EXIT` row it matches — rung 1, the branch owns the record | the repository owner, through the review chain |
| `chain_check.py`'s `CAPPED_EXIT` runtime message states the pre-ladder filing rule | already deferred by this branch — `overview.md` §*Not verified*. Carried forward from round 1, not re-opened | the repository owner |
| the 17 rows of `seal/ledger.md` whose cell count differs from their table header | already filed as #501. Carried forward from round 1 | the repository owner |

## Paste-ready fixes

🟡 1 — `seal/specs/…/overview.md`, a new row in §*Not verified*. The checker
change itself is the issue's, and its one-line form is given below the row so
whoever files it does not have to re-derive it.

```
| Whether `survivor_check.py` should exclude `seal/specs/*/survivors.md` from the range the way it already excludes `rounds/`. A survivors file quotes the surviving wording verbatim — the quote is the anchor, so it always does — and `wanted` subtracts everything the range wrote, so committing the file removes its own three survivors from the check. Measured on this branch: `--range 4ddfde2e..9f8efea4` reports `every survivor is excused by a row above (3)`, and `--range 4ddfde2e..9d9180f8`, the same tree plus that one file, reports `no removed wording is still standing` with the exemption file and without it. The hygiene step and `spec.md` A11 both read the second sentence. This is #365 on a path its exclusion does not cover, and the repair is a change to what a checker measures, which `spec.md` §Out refuses here | the repository owner, through a new issue |
```

The change that issue carries, for reference — `survivor_check.py`, the
predicate that drops `rounds/` from both sides of the range's path list:

```
# A judged survivor's own file, for the same reason and on both sides.
# `seal/specs/<id>/survivors.md` quotes the standing wording verbatim --
# the quote is the anchor -- so a range that adds one writes the removed
# sentence back, `wanted` subtracts it, and the check reports success
# having measured the survivors the file was written to record. #365 is
# the same defect one path over.
```

🟡 2 — `seal/specs/…/overview.md`, a second row in §*Not verified*, beside the
`CAPPED_EXIT` row:

```
| Whether the depth exit's runtime message — `DEPTH_EXIT` in `round_record.py`, printed when `close` refuses a depth-2 unit, and the same sentence at `chain_check.py:2648` and `:3355` — should be reworded to the ladder. It says a unit a fix pass may not add *is deferred with a named answerer, or becomes an issue*; under the ladder such a unit may take rung 4 instead, so the message is imprecise in exactly the way `CAPPED_EXIT` is. The prose carriers of the same rule were rewritten in this run's fix pass; the message was not, because rewording one is a gate change `spec.md` §Out refuses | the repository owner, through the review chain |
```

Needs a fix: no — nothing this branch may fix is open. 🟡 1's repair is a
change to what a checker measures and 🟡 2's is a runtime message, both refused
by `spec.md` §Out, so each is answered with those grounds and handed to the
home named in `## Deferred`. The four ⬜ rows are corrections to the run's own
paperwork and `Needs a fix` does not count them.
Loses a record or crashes: no — nothing found leaves the root and nothing
crashes. 🟡 1 makes a check silent, which is a measurement not taken rather
than a record lost; no gate, no parsed field and no checker arm changed on
this branch.

---

## Proof block

**Read** — `seal/specs/…/rounds/round-1.md` and `round-1-report.md`,
`spec.md`, `overview.md`, `questions.md`, `changelog.md`, `survivors.md`,
`seal/ledger/1790076060-…md` (all six rows), the fix range's diff over
`docs/`, `agents/`, `skills/`, `tests/` and `seal/`;
`docs/review-chain-spec.md` (§*The bound has a floor*, §*Where a leftover
goes*, §*The reopening*, and the new `New units` paragraph),
`docs/issues-and-milestones.md`, `docs/review-handoff-protocol.md:412`,
`skills/code-review/orchestration.md:161-250` and `:315-320`,
`skills/implement/SKILL.md:545-560`, `agents/smith.md:283-325`,
`agents/warden.md:127`, `templates/sdd-round.md:171`, `:214`, `:436`,
`tests/test_the_reopening_is_one.py:575-610`,
`tests/test_the_rules_have_one_owner.py:216-330`,
`skills/code-review/scripts/survivor_check.py` (module docstring §*What is
excluded*, `weights`, `weigh`, `wanted`, `carriers`, `exempted`, `report`),
`skills/code-review/scripts/chain_check.py:165-235`, `:770-780`, `:2640-2660`,
`:3350-3360`, `skills/code-review/scripts/round_record.py:2565-2575`,
`.github/workflows/hygiene.yml:215-260`, `CONTRIBUTING.md` (the runner),
and the base at `6d410023` for `docs/review-chain-spec.md`, `agents/smith.md`
and `skills/code-review/orchestration.md`.

**Executed** — the eleven runs in `## Executed probes`. The enumeration ran
from a script in the session scratchpad, outside the repository; no probe file
was written into the tree and none was left behind. The only file this round
wrote in the worktree is this report.

**Unverified** — the broad gate, answered by the `sealer`.
