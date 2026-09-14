# Feature Specification: a wrapped terminal line is not one value

<!-- seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Three tickets, one seam. A reviewer's report is a hand-wrapped document and a
round record is a table whose cells a checker reads, and `terminal_value` in
`skills/code-review/scripts/round_record.py` is the one place a value crosses
between them. #309 is the value lost at the line break, #339 is the guard that
was supposed to make the join safe and is wrong in both directions, and #340 is
the conformance document that never learned the join exists.

**The frame's main finding is that the three are not three defects.** They are
one defect at three stages of its own repair: the join closed #309 in general,
`BLOCK_START` reopened it for the shapes this repository writes most, and the
document a second implementation is built from was never told either half.

## What the tree says that the tickets do not

Every number and every claim below was re-derived against
`fix/309-339-340-a-wrapped-terminal-line-is-not-one-value` at `5e09345`, under
`skills/agent-contract/SKILL.md` §5. Three of the tickets' own statements do
not survive that read, and each one changes what the work is.

### 1. #309's headline defect is already fixed, and its residue is #339

#309 was filed 2026-09-09 against `rounds/round-1.md` of work item
`1788926756`, whose two terminal rows still stand truncated in the tree:

```
| Needs a fix | yes — findings 1 and 7 ship reader-facing sentences that are |
| Loses a record or crashes | no — every defect is a sentence, the arithmetic is |
```

The fix #309 asks for — *read a value until the next field, blank line, or
heading* — landed at `393da64`, which is in this branch's history. **Read**:
`terminal_value` now joins the physical lines and stops at a blank line, at the
other terminal label, or at `BLOCK_START`.

So what is left of #309 is not the general case. It is the set of
continuations `BLOCK_START` cuts, which is #339 — and that set contains the
shape #309's own record was written in, because this repository writes an issue
number at the head of a line constantly.

### 2. Four places describe the guard, and none of them calls it sound

#339 says the round 3 fix pass *wrote, in the code, in `agents/warden.md` and
in `docs/review-handoff-protocol.md` — seven places — that `BLOCK_START` is
sound and that stopping on it is never wrong.* That is true of
`backup/120-before-rewrite`, which does not exist in this clone, and not of
this line of history.

**Read** 2026-09-14, `grep -rn "cannot begin with\|never wrong" agents/ docs/
templates/ skills/ tests/ .github/ hooks/ bin/`: both phrases return nothing,
and `git log -S "never wrong"` over the four files returns no commit. The only
copies live inside
`seal/specs/1789034970-.../rounds/round-4-report.md`, which is a round record
and asserts a past state correctly.

What the tree actually carries is **four** places describing the stop rule,
enumerated by `grep -rn "new markdown block"` over the shipped roots:

| Carrier | What it says |
|---|---|
| `skills/code-review/scripts/round_record.py#BLOCK_START` | the constant's comment — *the shapes a report puts next to a terminal line without one* |
| `skills/code-review/scripts/round_record.py#terminal_value` | the docstring — *stops at a blank line, at the other terminal label, or at a line opening a new markdown block* |
| `agents/warden.md` §*Report* | the same three stops, as an instruction to the reviewer |
| `tests/test_the_record_is_generated.py#test_prose_below_the_terminal_block_is_not_swallowed` | the same three stops, as the case's grounds |

The difference matters to the size of this work and not to its direction. Four
descriptions have to be made true of the pattern that ships; no overstatement
has to be retracted. **The correction is owed in both directions** — this spec
does not carry #339's number forward, and whoever reads #339 next should be
told the seven is the backup branch's.

### 3. #340 is larger than it says: the template carries nothing either

#340 says *`templates/sdd-round.md` says it in prose*. **Read**: `grep -n
"wrap\|physical line\|one value\|blank line" templates/sdd-round.md` returns
nothing. The template's prose about `Needs a fix` and `Loses a record or
crashes` runs from line 165 to 200 and never mentions the wrap.

So the sentence is missing from **two** carriers, not one: the conformance
document and the template a round record is written from. `agents/warden.md` is
the only shipped file that has it.

### 4. The defect has a sibling, and the repository already ships the cure

Three modules in this tree answer the same question — *where does a run of
hand-wrapped prose stop*:

| Module | Pattern | `#120's parser` | `---` |
|---|---|---|---|
| `.github/scripts/issue_claims_check.py#BLOCK_START` | markers require the space CommonMark requires; four whole-line alternatives | joins | stops |
| `skills/code-review/scripts/round_record.py#BLOCK_START` | a bare `#`, pipe and `>`; `[-*+]` and `\d+\.` require a space; two fence openers. No whole-line alternative | **truncates** | **passes** |
| `skills/code-review/scripts/survivor_check.py#BLOCK` | a bare `[-*+>#]` class; `\d+[.)]` requires a space; one whole-line run of `-*_=` | **splits the sentence** | stops |

**Read**, by applying each pattern as written. The bare `#` in the middle row
is what truncates `#120's parser is the one that matters.`; the bare `[-*+>#]`
in the bottom row is the same class one module over, and its whole-line
alternatives are already correct. `issue_claims_check.py`'s own comment names
the trap — *`#22` at the start of a line is this defect hard-wrapped* — and
`seal/ledger.md:1670` records it as executed by mutation.

`skills/agent-contract/SKILL.md` §12 is why the sibling is in scope: the
finding names a coordinate and the fix is owed to every instance the same cause
produces. What differs is the failure direction, and the spec says so below
rather than treating the two as interchangeable.

## The judgement the release asked for: one change, not two or three

The milestone groups the three and asks whether one is separable. **They travel
as one change.** The grounds, in the order they bind:

1. **#309 and #339 are the same line.** #309's residue is the set
   `BLOCK_START` cuts. Two branches would edit one constant, and the second
   would be re-deriving the first's measurement to know what it had left.
2. **#340's sentence cannot be written before the pattern is chosen.** A
   conformance document that says where the join stops has to name the stops
   that ship. Written first, it is written twice; written after, a second
   implementation built in between truncates — which is the milestone's own
   reason for grouping them.
3. **The edit surfaces overlap.** #339's four descriptions and #340's two
   additions both land in `agents/warden.md` §*Report* and in
   `templates/sdd-round.md`'s prose. Splitting them drifts the same ledger
   anchors twice and puts two branches in one paragraph of a file the review
   chain reads.

**#340 is the one that is genuinely separable**, and it is not separated. It is
docs-only, it breaks no test, and a branch could carry it alone. What that
would cost is the thing the release is cut to prevent: between the two merges,
the document that defines a conforming tool describes a behaviour the shipped
tool no longer has, and a second implementation written from it is wrong on
purpose.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `terminal_value` refuses a report, so this is a gate's guard. The failure direction and the prompt budget are stated below, and `plan.md` phase 1 carries the red run |
| `skills/agent-contract/SKILL.md` §12 | The class is *a marker class with no space requirement reads `#N` at the head of a line as a block opener*, and it has two instances in this tree. Scope is drawn on the class, not on #339's coordinate |
| `skills/agent-contract/SKILL.md` §15 | The truncation direction is pinned by nothing today. Every case this work plants is seen red first, and `plan.md` says against what |
| `skills/agent-contract/SKILL.md` §5 | Why all three tickets' claims were re-measured rather than carried: three of them do not hold against this tree, and each one changes the scope |
| `skills/agent-contract/SKILL.md` §14 | The four descriptions are what a person reads before deciding whether to check a cell. Changing the pattern without them ships a fix whose documentation argues against checking it |
| `CLAUDE.md` §*a change writes fragments* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`; never `CHANGELOG.md` or `seal/ledger.md` |
| `docs/review-handoff-protocol.md` §*A conforming tool* | The document #340 is about. It is the reason the protocol is a carrier here rather than a reference |
| `skills/implement/SKILL.md` §3 | Top rung: this changes what a checker accepts and what a reviewer is instructed to write. Hence a framer, hence this file |

## Scope

### In

- **`round_record.py#BLOCK_START`** — narrowed to the pattern
  `issue_claims_check.py` already ships, plus the two fence openers this module
  needs. Both directions close at once: a continuation beginning `#`, `**`,
  `<`, `1)` or an indent joins, and `---`, `___` and a setext underline stop.
- **The truncation direction, pinned.** Nothing in the tree distinguishes the
  correct pattern from the defective one on a continuation. The swallow
  direction is already pinned by
  `test_prose_below_the_terminal_block_is_not_swallowed`, and both stay green.
- **The four descriptions**, made true of what ships, each naming what the
  guard does **not** cover. The blank line stays the only stop that covers
  every shape, and that sentence is what keeps the next reader from widening
  the marker list again.
- **#340 — the protocol and the template.** The conformance statement (*a
  wrapped terminal line is one value; here is where the join stops*) reaches
  `docs/review-handoff-protocol.md`, and `templates/sdd-round.md` gains it in
  the **prose** about the same fields.
- **`survivor_check.py#BLOCK`**, the sibling instance of the same class.
- The two fragments, and the re-stamping `evidence-check` asks for.

### Out, with the reason beside each

- **#309's comment — the two `close` defects.** A `deferred` row's grounds
  reduced to the home alone, and the empty code span in a `fixed` row's
  grounds. The release cut puts *which values each half accepts* in the third
  work item, and this one is *how a value is read across a line break*. **This
  exclusion is Q2 and it is not safe on its own**: neither #321, #323, #341,
  #273 nor #353 covers either defect, so excluding them here drops them from
  the release, and #309's own comment argues they are the same seam. A person
  decides before the first edit.
- **A migration of the round records already truncated.** A round record
  asserts what a reviewer wrote at a past SHA, and the machine-read half
  survives the cut: `chain.yes_or_no` reads the verdict word before the first
  separator, so `yes — findings 1 and 7 ship reader-facing sentences that are`
  still computes the reopening bound `docs/review-chain-spec.md` wants. What
  was lost is the reason a person reads, and re-writing it now would make a
  past-state document assert something nobody wrote. **Q5 measures whether any
  record truncated to the bare verdict word**, which is the one shape that
  would change this answer.
- **Sharing one pattern constant across the three modules.**
  `.github/scripts/` and `skills/*/scripts/` ship on different paths and are
  not importable from each other. `plan.md` §*Alternatives considered* carries
  it, and the pin that replaces it is a case comparing the two spellings.
- **The `Needs a fix` row of `templates/sdd-round.md`.** #340's own trap:
  `seal/ledger.md:89` quotes that row verbatim as an anchor, the first attempt
  broke it, and this repository answers a broken anchor by removing the row —
  which is wrong here, because the row's claim is still true. The guidance goes
  in the template's prose, where its other guidance already lives.
- **Widening `BLOCK_START`'s marker list.** The repair is a narrowing. See
  `plan.md`.
- **Any new parsed field or ledger row the record must carry.** Rule 8 of
  `tests/test_the_rules_have_one_owner.py`, the 0.8.x moratorium, is untouched.

## The gate answer `CONTRIBUTING.md` asks for

- **Failure direction: the change makes the gate refuse less and join more.**
  A report that today produces a truncated cell will produce a whole one, and
  a report that today produces a whole cell is unaffected. Nothing that
  currently passes begins to fail.
- **Why that direction is the cheaper mistake here.** The two errors are not
  symmetric and #339 says why. A truncated value reads as a finished sentence,
  so nobody looks; a swallowed one reads as wrong at a glance. The narrowing
  reduces the silent error and leaves a visible one, which is the trade the
  join was made for in the first place.
- **Prompt budget: zero added, and one path to fewer.** `terminal_value` puts
  no question in front of a person — it refuses or it writes. The only way this
  work could add one is Q1 answered *refuse*, which would stop a run whose
  report omitted a blank line, at whatever minute the record is generated. The
  default answer is *join*, on this project's first goal.
- **Platform honesty.** Nothing here inspects a process or a path. The patterns
  carry `\r*$` on their whole-line alternatives, which is what keeps a CRLF
  checkout reading the same as an LF one, and that is the only platform-shaped
  clause in the change.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A continuation beginning with an issue number joins | Given a report whose `Needs a fix:` line wraps onto `#120's parser is the one that matters.` / When `new` generates the record / Then the cell holds both halves joined by one space | A case parametrised over the four shapes `#N`, `**bold**`, `<div>` and an indented line, each seen red against the pattern at `5e09345` |
| A block opener under the pair still stops the join | Given a report with a heading, a list item, a table row or a block quote directly under the terminal pair / When `new` generates the record / Then the cell holds the terminal value alone | `test_prose_below_the_terminal_block_is_not_swallowed` stays green, and the existing mutation run stays red with the branch deleted |
| A thematic break stops the join | Given a continuation line of `---`, `___`, `***` or a setext underline / When `new` generates the record / Then the join stops before it | A case at all four shapes, red against the current pattern, which passes every one of them |
| A reviewer reads what the guard does not cover | Given `agents/warden.md` §*Report* / When a reviewer reads the terminal-line instruction / Then it names the blank line as the only stop that covers every shape | A case pinning the sentence, seen red with it stashed (§14, §15) |
| A second implementation reads the rule | Given `docs/review-handoff-protocol.md` / When a conforming tool is built from it / Then it is told that a wrapped terminal line is one value and where the join stops | A case in `tests/test_the_rules_have_one_owner.py`'s shape: the owner states it, every other carrier links it |
| The template does not break an anchor | Given the guidance added to `templates/sdd-round.md` / When `evidence-check` runs / Then `seal/ledger.md:89`'s quoted `Needs a fix` row is unbroken | `evidence-check --strict` reports 0 broken, and the row's own anchor hash is unchanged |
| The sibling reads a wrapped sentence as one | Given `survivor_check.py` segmenting prose whose second line begins `#120` / When the check scores it / Then the two lines are one sentence | A case at that shape, red against `BLOCK` as it stands |
| Nothing that passed begins to fail | Given the whole record module / When the suite runs / Then the 104 cases of `tests/test_the_record_is_generated.py` are green plus the new ones | `bin/test` over the module, then the broad gate once, by the sealer |

## Data & interfaces

No schema, no endpoint, no new field. What changes is one regular expression,
one sibling regular expression, and the prose of four carriers plus two
additions.

**The anchors this work is expected to move**, so the builder re-stamps rather
than discovers:

| Anchor | Expected |
|---|---|
| `agents/warden.md#"## Report"@008ab85b` (`seal/ledger.md:986`, R7) | **DRIFTED.** The wrap paragraph is inside that section. The claim — the report carries the three tables under the generator's headings plus the two terminal lines — is untouched, so this is a re-read and a re-stamp |
| `` templates/sdd-round.md#"\| Needs a fix \| <`yes — <what>` · `no`. The reviewer's own answer — what stands after the colon in its `Needs a fix:` line, never the whole line> \|"@9a509e35 `` (`seal/ledger.md:89`) | **Unchanged.** The row is not edited; the prose below it is. If this anchor moves, the edit went in the wrong place |
| `.github/scripts/issue_claims_check.py#BLOCK_START@33aff484` (`seal/ledger.md:1670`) | **Unchanged.** This module is the model and is not edited |
| `agents/warden.md#"## Role">…` (`seal/ledger.md:89`) | **Unchanged.** A different section |

`CLAUDE.md` says a row whose anchor a change removes is REMOVED, not
re-pointed. None of the above is that case: every claim survives its edit, so
every one of them is a re-read and a re-stamp.

## Open questions → questions.md

Six rows, and three of them need a person before the first edit: whether the
join is kept or replaced by a refusal (Q1), whether #309's comment travels with
this work or is opened as a ticket against the cells work item (Q2), and which
file owns the wrap rule once two more carriers state it (Q3). The other three
are a measurement or the work, and none of them waits on anybody.
