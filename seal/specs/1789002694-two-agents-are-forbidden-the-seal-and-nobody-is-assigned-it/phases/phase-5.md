# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `bf16087` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build the five items `phases/phase-4.md` carried, adding row 5 to `plan.md`'s
Phases table as part of the work. Four of the five are one subject and may be
one commit; the capped run is separate.

**One.** The capped run cannot reach its seal, measured with a fixture in
phase 4 and holding. The repair is `seal`'s condition: refuse where a finding
is still OPEN in the verdict table, which `Pass` already answers one row down,
rather than where the reviewer's `Needs a fix` reads `yes`. Keep the other two
refusals. A case seen red first, and the docstring's *Three refusals* block
saying what changed and why.

**Two.** *After the rounds settle* is a moment where the condition is a row.
Name the row at `agents/warden.md:51`, `skills/verify/SKILL.md:249` and
`:361`, `skills/code-review/orchestration.md:469`, `agents/smith.md:187`, and
in `agents/sealer.md` too, since a sealer spawned early is what the row
prevents.

**Three.** `agents/warden.md:22` calls its review mark a seal. Rewrite the
opening to name what it keeps, hold the rest of the paragraph's meaning, and
let it link to item 4's rule.

**Four.** Nothing says one seal is final. The owner stated the rule — every
agent seals what it verified, and the one seal over the whole project is the
sealer's — and the paragraph names the two properties already in the design
rather than inventing others: scope and form. `skills/verify/SKILL.md` owns
it, `agents/sealer.md` and `agents/warden.md` each carry one sentence naming
the owner, and phase 4's judgment, asked for and standing unless found
otherwise, is that it belongs in `tests/test_the_rules_have_one_owner.py`'s
`RULES` table.

**Five.** A bare *the seal* is ambiguous the moment more than one exists.
Every reference to an instance names whose; the concept and its formats stay
bare. `tests/test_one_word_one_meaning.py` is the home, and the absence
assertion has to exclude the concept's own terms.

Two cautions phase 4 paid for: a re-stamp reads nothing, so a row whose claim
these edits falsify is corrected by reading; and the phase range is not the
range CI reads, so `survivor-check` runs over both.

**Two additions arrived mid-phase from the coordinator.** A row for #331 in
`docs/flow.md`'s 0.10.1 section, written from the issue, carrying the reason
the census waits for the agent set. And the general rule behind item 5 —
when a document names a thing more than one party can have, it names whose —
stated in one place and linked from the other, with the relationship to its
enforcement said in whichever file states it.

## What this phase found

**Items 1 and 2 contradict each other, and item 1 wins.** The handoff states
item 2's condition as *the last round record's `Needs a fix` reads `no`* and
calls it exact, and phase 4's record adds that it is *the first thing
`round_record.py seal` refuses on — so the mechanism is right and only the
words are vague*. Item 1 is the finding that the mechanism is **not** right:
that refusal is the one that makes a capped run unsealable, and removing it is
the repair. Both items were written in the same handover, and the row item 2
names is the row item 1 deletes.

So the row this phase wrote into the six carriers is **the last round record's
`Pass` box, checked**. It answers item 2's actual complaint — a row a machine
reads, rather than a moment a reader has to pick — and it is the row item 1
left standing. `Needs a fix: no` is the ordinary way a run arrives there and
is named as such wherever the new row is: the two part only on a capped run,
which is exactly the case that produced both items. `skills/verify/SKILL.md`
§*The broad gate* states the distinction and the four carriers link to it.

**The word `Needs a fix` now has two readers asking two questions, and that is
deliberate.** `chain_check`'s floor bound reads it to ask whether the run
REOPENED, which is the reviewer's own answer and stays the reviewer's; `seal`
asked *has the run ended* of the same row and now asks the `Pass` box instead.
Six of the seven survivor reports over this phase's range are that split
showing up as shared identifier n-grams — `chain.FLOOR_NO`, `chain.yes_or_no`,
`chain.field(rows, chain.NEEDS)` — and each is exempted with the reader it
belongs to named.

**The removed refusal was enumerated in six places and `survivor-check` saw
one.** `skills/verify/scripts/broad_gate.py`'s docstring listed all three in a
parenthesis and was the one report. `agents/sealer.md` listed them twice, the
seal module's own docstring called the refusal *the rounds have not settled*,
this work item's changelog fragment described them to a reader with none of
the code, and `seal/ledger/<item>.md`'s S6 stated all three as its claim. The
four the checker could not see share no wording with the lines the range
removed, which is what it measures — contract §12 is what found them, and
this is a worked instance of the enumeration reaching further than the check.

**`seal/ledger.md` is the one CI reads, and `--reverify` scoped to it is
honest only after the rows are read.** Six rows drifted there and all six
hold: two about the smith's phase rules, two about who writes the report and
the record, one about the file's seam, one about the config template's table.
The one worth naming is R5, which claims that **both** definitions that run a
test LINK the handoff section rather than restating the rule — this phase
added a sentence to both of those paragraphs, and it kept the pattern by
linking `skills/verify/SKILL.md` for a second rule rather than restating that
one either.

**A ledger coordinate whose hash is not eight hex characters is skipped in
silence.** Two rows were first written with `@PENDING` as a placeholder, and
`evidence-check` reported `34 ok · 0 drifted · 0 broken` with six coordinates
in the file that resolve to nothing — the same count as before the rows
existed. `@00000000` was read, reported as drift and re-stamped. So a
mistyped stamp is invisible where a wrong one is loud, and nothing in this
work item asked for that. It is written into `questions.md` rather than fixed
here.

**The `Pass` refusal's message now says what it does NOT read.** With the
`Needs a fix` refusal gone, `Pass` is the only thing answering *has the run
ended*, and a reader who has just watched a `Needs a fix: yes` record seal
needs the two rows told apart at the one moment the difference bites. Contract
§14 is why the sentence is pinned as well as written.

**Every case was seen red before it was committed, and the mutation for item 1
is the revert.** The three cases of item 1 were run against the old
`round_record.py` and all three failed, one of them printing the old
refusal's own text — phase 4's measurement reproduced by the case rather than
by a probe. The three of item 2 and the six of items 3–5 were run against the
documents as they stood, restored from held bytes rather than from `HEAD`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `round_record.py seal`'s first refusal, on `Needs a fix` reading `yes` | Nowhere — the condition it was reaching for is *a finding is still open*, and the `Pass` box answers that one row down from the verdict table rather than from prose. The docstring's *Three refusals* block is now *Two refusals* plus a paragraph saying what the third was, what it cost, and why the box replaces it |
| The enumeration of three refusals in `broad_gate.py`'s docstring, `agents/sealer.md` twice, the seal module's docstring, the changelog fragment, and `seal/ledger/<item>.md`'s S6 | The same six places, now naming two. S6 also lost the coordinate on the renamed case; its claim moved to S10 |
| `agents/warden.md`'s opening claim on the word *seal* | The same paragraph, naming the **review mark**, with one sentence linking `skills/verify/SKILL.md` §*Every agent seals what it verified, and one of them is final* — which is the rule that makes several seals correct and one of them final |
| The bare *the seal* at seven instance references — four in `skills/verify/SKILL.md`, one in `README.md`, one in `agents/sealer.md`, one in `templates/config.md` | The same sentences, each naming whose. `tests/test_one_word_one_meaning.py`'s sweep is what keeps them named: every bare `the seal` in a file that instructs somebody has to be the concept or one of its formats |
| The seal block's `due after the rounds settle` placeholder | The same line, `due when the last round record's `Pass` is checked` |
