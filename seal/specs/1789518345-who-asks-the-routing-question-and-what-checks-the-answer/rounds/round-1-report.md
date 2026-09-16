# Round 1 — who asks the routing question, and what checks the answer

Target SHA `655eaf7c`, branch
`feat/88-399-419-who-asks-the-routing-question-and-what-checks-the-answer`,
range `release/v0.12.0..HEAD`. Reviewed in a `git clone --no-local` at that
commit, deleted at the end of the round. The SHA did not move during the round.

## How the findings relate

Three of the five are one shape, and it is the shape the spawn asked me to look
hardest for: **this branch made three repairs that nothing in the tree holds.**

```
  the repair                              what holds it
  ─────────────────────────────────────   ─────────────────────────────────
  🟡 2  the design gate's SECOND copy,     nothing — pasting it back leaves
        removed past the span plan.md      every module green
        named
  🟡 3  the question's new shape in the    nothing — the block can keep its
        block every session reads          old paragraph and stay green,
                                           `claude_block.py --check` included
  🟡 5  nine ledger anchors re-stamped     nothing — no `Checked` date moved,
        after being re-read                so a re-read reads as a refresh
```

The other two are separate. 🟡 1 is the one new behaviour in the diff that can
misfile a record: `seal` now picks the cell's home from what is on disk rather
than from the declaration, so a work item that declares the review chain and has
not written round 1 yet gets sealed into a file the chain reader never opens.
🟡 4 is a question rather than a defect I could reproduce — the act moved to a
party that may have no way to perform it.

Everything the plan promised as red-first fires. I ran all five of phase 5's and
phase 6's mutations and every one went red; the details are in *Executed probes*.

---

## 🟡 1 — `seal` files the cell where the chain reader never looks

`skills/code-review/scripts/round_record.py:3843-3846` (`seal_home`).

`seal_home` picks the home from what exists on disk and reads no declaration. A
work item whose `routing.md` says `Review | through the review chain` and whose
`rounds/` is still empty — the ordinary state while round 1 runs — takes the
no-rounds branch and gets `broad-gate.md`. `chain_check.py` reads that file only
on the direct arm; on the chain arm it reads the `Broad gate` cell off the last
round record. So the cell is written to a file nothing on that path opens, and
`seal` prints `sealed` over it.

Executed, in a throwaway clone:

```
--- seal exit: 0
--- seal output:
 round-record: sealed seal/specs/1799000000-a-sealed-work-item/broad-gate.md — `Broad gate` | f21a996 against base
seal/specs/1799000000-a-sealed-work-item/routing.md:0  declares `through the review chain` and … /rounds/ holds no `round-N.md`
--- broad-gate.md written: True
--- its cell: f21a996 against base
```

Before phase 5 this path raised, and the raise was a precise refusal. Now the
sealer is told the seal was taken, and the run's evidence sits where the pull
request's reader cannot find it. It fails closed — `chain_check` refuses the
pull request on the round record's `not yet` — so nothing merges unrun. What is
lost is the sealer's answer: it reports success for a seal that does not count,
and the next party has to re-take the run without knowing why.

`seal_home`'s own docstring states two things the code does not do:

- *"The refusal is kept for the path that still means something"* — no refusal
  is kept. `seal` no longer calls `last_record`, and `seal_home` never raises.
- *"`chain_check` reads it from whichever home it finds"* — it does not. The
  home is chosen by the `Review` row, one arm each.

The same misfiling runs the other way: a `straight to the PR` work item that
does have rounds gets sealed onto the last round record, which the direct arm
never reads. One fix covers both, because both come from choosing the home
without reading the declaration.

## 🟡 2 — the removal that went past the named span is held by nothing

`agents/smith.md:113` · `tests/test_a_moved_rule_leaves_its_definition.py:266-281`.

`overview.md`'s divergence row records that the design gate had a second copy
sixty lines below the span `plan.md` located it at — *present 2–3 approaches
with failure scenarios and wait for an explicit go* — and that the builder
removed it too, at `a0b4b97d`. That judgment is right: left standing, the file
would have said *phase 2 is your caller's spawn* in one paragraph and *wait for
an explicit go* in another.

`MOVED_OUT_OF_SMITH` does not name it. Pasting the sentence back and running
the three modules that would hold it leaves them green:

```
*** NOT CAUGHT (green) ***   exit=0  M6 design-gate second copy pasted back into smith.md
                             242 passed in 4.50s
```

`grep -rn "wait for an explicit go\|2–3 approaches" tests/ skills/ agents/ docs/`
returns nothing, so no other module holds it either. The one thing the builder
found by going past the span it was given is the one thing the suite cannot see
come back — which is what `tests/test_a_moved_rule_leaves_its_definition.py`
exists to prevent, in its own file.

## 🟡 3 — the block every session reads can keep the old question

`templates/claude-md-block.md:16` · `CLAUDE.md:16` ·
`tests/test_waiver_decided_at_start.py:841`.

`test_the_preset_block_carries_it_too` asserts the `AXES` values and the
declaration path, and nothing about the question's shape. The stale-count
absences added this round
(`test_the_skill_asks_the_whole_question_in_the_first_batch`) are asserted over
`skills/implement/orchestration.md` and `skills/implement/SKILL.md` only.
Neither reaches the block.

Executed: I reverted the paragraph in `templates/claude-md-block.md` and its
generated copy in `CLAUDE.md` to the old three-checkbox text, left every other
file at HEAD, and ran the five modules that could hold it.

```
claude_block.py --check exit=0  claude-block: CLAUDE.md carries the block templates/claude-md-block.md holds
suite exit=0  176 passed in 8.94s
*** NOT CAUGHT (green) ***
```

`claude_block.py --check` passes because it compares the two copies with each
other, not with the question. This is the defect the builder repaired one file
over — *a presence assertion on a count passed on the copy that should have
moved* — landing on the copy that matters most: `CLAUDE.md` is the one file a
session in an opted-in repository always has, so a block left behind would tell
every session to ask the old question while every other document describes the
new one.

## 🟡 4 — the question moved to a party that may have no way to ask it

`agents/framer.md:228` · `skills/implement/orchestration.md:286`.

Both now say the routing batch is the framer's to ask, as *two questions in one
`AskUserQuestion` call*. The framer is a subagent.

What I measured, in this session: I am `warden`, spawned from `agents/warden.md`,
which like `agents/framer.md` declares no `tools:` key and therefore inherits the
full set. **`AskUserQuestion` is not in my tool list, and `ToolSearch` for it
returns `No matching deferred tools found`.** On that evidence a framer spawned
in this harness cannot put the question to anybody.

I could not settle it: §6 withholds spawning an agent from me, so I cannot run a
framer and watch what it does. What makes it worth raising rather than leaving
is the failure mode if the evidence holds. A framer that cannot ask and is told
to write `routing.md` before its other three files will write one from a guess,
and a recorded answer nobody gave is #151's shape — the thing this work item
exists to end, arriving through the door it opened.

`overview.md`'s *Not verified* table names the neighbouring question — *whether
a session reading the new shape actually asks it in one call* — and answers it
with the orchestrator at the first work item framed after this ships. This one
is prior to that: not *does it ask correctly*, but *can it ask at all*.

**Who answers it:** the repository owner, before this ships — one framer spawn
against a scratch work item settles it.

## 🟡 5 — nine rows were re-read and no `Checked` date says so

`seal/ledger.md` (18 rows changed, 9 distinct anchors) ·
`skills/evidence-check/scripts/evidence_check.py:1577`.

The builder's account checks out on the count: 18 rows moved, they resolve to 9
distinct drifted anchors plus one dead coordinate removed, and
`bin/evidence-check --strict .` exits 0.

What no row records is the reading. Every one of the 18 keeps its old `Checked`
date — 2026-09-02 through 2026-09-15 — beside a hash recomputed on 2026-09-16,
and no `Notes` cell gained a re-read line. `templates/ledger.md` states the rule
the other way round: re-verifying IS re-reading and then running the command.

`reverify`'s own `# RIDER:` names this exact gap and the measurement behind it:

> this rewrites the hash and never the `Checked` column, so the claim that
> somebody re-read the code is made by a person and recorded by nobody. Round 1
> of #120 measured the gap: six rows of `seal/ledger.md` got new hashes on one
> branch and all six kept dates from before the content moved

So the mechanism is a disclosed, pre-existing hole rather than this branch's
invention. What is this branch's is that it reproduced it nine times while its
`overview.md` asserts the reading happened — and the assertion is the one thing
a later reader cannot check, because the column that would carry it was left
alone. The repair is by hand and costs nine cells.

## ⬜ two small ones

**A case names a notice the arm does not emit.**
`tests/test_chain_check_at_the_pull_request.py:658`,
`test_a_direct_declaration_with_no_seal_is_a_notice_on_a_draft`. `direct_seal`
returns `[], []` when `strict` is false, so a draft gets silence, not a notice —
which matches `broad_gate`'s own behaviour and is correct. The case asserts
exit 0 and nothing else, so it would pass either way. Rename it to say silence.

**`spec.md` and `plan.md` still say six.** `spec.md:392` (S20) and
`plan.md:183` say the module states *the six things it cannot see*;
`spec.md:345-367` lists seven bullets and the module carries seven.
`overview.md` discloses the discrepancy and says it was corrected in this work
item's records — the two records still read `six`. A record correction, not a
fix: no behaviour depends on it, and the case asserts the phrases rather than
the number.

## What I checked and found sound

- **The frame arm's four red-first mutations and phase 5's reader mutation all
  fire.** M1–M5 in *Executed probes*. The one that matters most, emptying the
  failure collection before it is returned, takes eight cases red.
- **`frame_mark`'s repair holds.** Reading only the last non-empty line is what
  stops a spec *about* the mark reading as one carrying it, and
  `test_a_mark_that_is_only_QUOTED_does_not_count` fires on the anywhere-search
  mutation because the refusal text it asserts (`END with`) belongs to the
  no-mark branch and not the unfilled-mark one. The case can fail for the right
  reason.
- **`DIRECT_GATE_FROM` was owed.** `plan.md` gave a cutoff to phase 6's arm and
  none to phase 5's; 16 declarations answer `straight to the PR` and none
  carries a `broad-gate.md`, so an arm without it refuses the next release for
  work nobody could have sealed. Shipping one arm with the mechanism and its
  twin without it is the half-copied repair this repository keeps recording.
  Judged correct.
- **All 84 committed declarations parse, and none carries the two new rows.**
  Executed. The plan's other figures hold too: 11 answer `Planning | framer`,
  16 `straight to the PR`, 68 `through the review chain`.
- **`templates/claude-md-block.md` and `CLAUDE.md` agree**, and the template is
  the source — `install.sh` and `.github/scripts/claude_block.py` confirm it.
  `claude_block.py --check` exits 0.
- **The five inverted cases each pin new behaviour rather than merely stopping
  to fail.** `test_every_document_shows_the_third_axis_ROW_not_only_the_count`,
  `test_the_smith_carries_its_own_half_and_not_the_questions` and
  `test_the_questions_are_collected_before_the_work_not_during_it` each assert
  an absence in `agents/smith.md` that the M6 paste-back class would break;
  `test_the_planning_row_is_a_record_and_not_a_checkbox` drops two count
  assertions for assertions over the row's name, and M8 (adding a `Planning` box
  to question 2) takes it red, so the rule it is for still fires;
  `test_the_smith_says_whether_the_frame_holds_before_building_to_it` rebinds
  its slice to `2. **` rather than the phase's old title, which is the right
  repair for a slice that would otherwise raise.
- **`item_began` is behaviour-identical after the refactor.** The `len(parts) < 3`
  guard was dropped, and `item_began_at("")` returns `None` for every input that
  guard covered. Read.
- **The frame arm passes on this branch's own declaration.** `chain_check.py`
  against `release/v0.12.0` reports only the missing round record, which is the
  state a round-1 review opens in.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal` picks the cell's home from what is on disk, so a chain-declared work item with no round record yet is sealed into `broad-gate.md`, which the chain arm never reads; `seal_home`'s docstring states a refusal it does not keep and a reader behaviour that does not exist | `skills/code-review/scripts/round_record.py:3843` | open | Executed in a throwaway clone: `seal` exits 0, prints `sealed …/broad-gate.md`, and the post-write `chain_check` reports the round record still missing. `chain_check.main` reads `broad-gate.md` only inside the `routing.DIRECT` arm |
| 🟡 2 | The design gate's second copy, removed past the span `plan.md` named, is pinned by nothing — pasting *wait for an explicit go* back leaves every module green | `agents/smith.md:113`, `tests/test_a_moved_rule_leaves_its_definition.py:266` | open | Probe M6: 242 passed, exit 0, with the sentence restored. `grep -rn "wait for an explicit go" tests/ skills/ agents/ docs/` returns nothing |
| 🟡 3 | The generated `CLAUDE.md` block and its template can both keep the old three-checkbox paragraph with every case green, `claude_block.py --check` included | `templates/claude-md-block.md:16`, `tests/test_waiver_decided_at_start.py:841` | open | Executed: old paragraph restored in both files, 176 passed over the five plausible modules, `claude_block.py --check` exit 0 |
| 🟡 4 | The routing batch moves to the framer, and a subagent in this harness appears to have no `AskUserQuestion` tool — a framer that cannot ask and is told to write `routing.md` first writes an answer nobody gave | `agents/framer.md:228`, `skills/implement/orchestration.md:286` | open | Measured in this session: `warden` inherits the full tool set under the same frontmatter shape and has no `AskUserQuestion`; `ToolSearch` returns `No matching deferred tools found`. Not settled — §6 withholds spawning a framer from me |
| 🟡 5 | 18 ledger rows were re-anchored and not one `Checked` date or `Notes` cell records the reading `overview.md` says happened | `seal/ledger.md`, `skills/evidence-check/scripts/evidence_check.py:1577` | open | Read: all 18 keep dates from 2026-09-02 to 2026-09-15 beside hashes computed 2026-09-16. `reverify`'s own `# RIDER:` names this gap and #120's measurement of it |
| ⬜ | `test_a_direct_declaration_with_no_seal_is_a_notice_on_a_draft` names a notice `direct_seal` never emits, and asserts only exit 0 | `tests/test_chain_check_at_the_pull_request.py:658` | correction | Read: `direct_seal` returns `[], []` when `strict` is false. The behaviour is right and matches `broad_gate`; the name is not |
| ⬜ | `spec.md` S20 and `plan.md` phase 6 say the module states six things it cannot see; it states seven | `spec.md:392`, `plan.md:183` | correction | Read, and `overview.md` already discloses it. A record correction |
| 🟢 | The frame arm's four red-first mutations and phase 5's reader mutation all fire | `skills/code-review/scripts/chain_check.py:3270` | verified | Probes M1–M5, all non-zero |
| 🟢 | All 84 committed declarations parse; none carries `Automation` or `Answer pressed`; 11 / 16 / 68 on the plan's three figures | `hooks/routing.py:164` | verified | Executed over `git show HEAD:<each>` |
| 🟢 | `templates/claude-md-block.md` is the source and `CLAUDE.md` the generated copy; the two agree | `templates/claude-md-block.md`, `CLAUDE.md` | verified | `claude_block.py --check` exit 0, read directly |
| 🟢 | `DIRECT_GATE_FROM` was owed, on the identical retroactive-red measurement | `skills/code-review/scripts/chain_check.py:696` | verified | 16 direct declarations, none carrying the file, counted |
| 🟢 | The five inverted cases each pin the new behaviour | `tests/test_waiver_decided_at_start.py:147`, `:696`, `:815`, `tests/test_chain_hooks_hardening.py:789`, `:969` | verified | Probes M6 and M8, plus reading each pair |
| 🟢 | `item_began`'s refactor is behaviour-identical, dropped guard included | `skills/code-review/scripts/chain_check.py:1638` | verified | Read, every input the guard covered traced through `item_began_at` |
| ❓ | The full suite, the repository-wide lint and the typecheck | — | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer, and this file hands it to no reviewer. Answered by the orchestrator, by spawning the sealer once the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six changed modules | 463 passed, exit 0 |
| `bin/evidence-check --strict .` | exit 0 — 1263 ok, 0 drifted, 0 broken |
| `.github/scripts/claude_block.py --check` | exit 0 |
| `chain_check.py --baseline release/v0.12.0` on this branch | exit 1, naming only the missing round record; the frame arm is silent, so this branch's own frame passes |
| `routing.parse` over every committed `routing.md` at HEAD | 84 declarations, 0 unparseable, 0 carrying the new rows; 11 `framer`, 16 `straight to the PR`, 68 `through the review chain` |
| M1 — `frame_mark` searches anywhere instead of the last non-empty line | red, 1 failed |
| M2 — the frame arm returns an empty failure collection | red, 8 failed |
| M3 — the approval-line notice promoted to a refusal | red, 1 failed |
| M4 — the frame cutoff comparison dropped | red, 1 failed |
| M5 — the direct arm returns before it looks | red, 3 failed |
| M6 — the design gate's second copy pasted back into `agents/smith.md` | **green, 242 passed — not caught** |
| M7 — question 2's box-table header renamed | red, 3 failed |
| M8 — a `Planning` box added to question 2 | red, 3 failed |
| The old three-checkbox paragraph restored in `templates/claude-md-block.md` and `CLAUDE.md` | **green, 176 passed — not caught**; `claude_block.py --check` exit 0 |
| `round-record seal` on a chain-declared work item with no round record | exit 0, `broad-gate.md` written and the cell filled |
| The broad gate | not yet — not run in this round, and not this agent's to run |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `Checked` column records no re-read, so `--reverify` cannot report the half that was skipped | `skills/evidence-check/scripts/evidence_check.py:1577`'s standing `# RIDER:`, and #120 round 1 | the repository owner — 🟡 5 asks only for this branch's nine rows, not for the mechanism |
| A durable record that a person chose `no work item` | already deferred by `overview.md` §*Not done* as a ticket for the orchestrator to open | the repository owner, at the ticket |
| Promoting the approval-line notice to a refusal | already deferred by `overview.md` §*Not done*; #399's `Done when` asked for a refusal and this ships a notice on a measurement the ticket did not have | the repository owner, after two or three releases carry the notice |

## Paste-ready fixes

🟡 1 — `skills/code-review/scripts/round_record.py`, replacing `seal_home`'s
last two paragraphs of docstring and its body:

```python
    The home is picked from the DECLARATION, never from what happens to be on
    disk. `chain_check` reads `broad-gate.md` on its direct arm alone and the
    last round record on its chain arm, so a chain-declared work item sealed
    into `broad-gate.md` is a cell no reader of that work item ever opens --
    and `seal` printed `sealed` over it. The refusal `last_record` used to
    raise is kept for exactly that state: a work item whose rounds are running
    and whose first record is not written yet.
    """
    found = earlier_records(routing, rounds, sys.maxsize)
    if found:
        return found[-1]
    declared = None
    try:
        with open(os.path.join(item, routing.FILENAME), encoding="utf-8") as f:
            declared = routing.parse(f.read())
    except OSError:
        pass
    if declared is not None and declared["review"] != routing.DIRECT:
        raise Refused(
            f"{os.path.join(item, routing.FILENAME)} declares "
            f"`{declared['review']}` and {rounds} holds no `round-N.md`. For "
            f"that answer the cell belongs on the last round record, and "
            f"`{chain.BROAD_GATE_FILE}` is read only for a work item "
            f"declaring `{routing.DIRECT}` -- written there it would be a "
            "seal nothing reads. Write the round record first; no cell was "
            "written"
        )
    return None, os.path.join(item, chain.BROAD_GATE_FILE)
```

and the case that holds it, in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` beside
`test_seal_writes_a_file_where_no_round_record_exists`:

```python
def test_seal_refuses_a_chain_declaration_with_no_round_record(repo):
    """The home is the DECLARATION's, not whatever is on disk.

    `rounds/` empty is two different states. One is a work item that runs no
    rounds, and its cell belongs in `broad-gate.md`. The other is a work item
    whose rounds are running and whose first record is not written yet, and
    its cell belongs on that record -- filed in the other home it is a seal
    the chain arm never opens, over which `seal` prints `sealed`.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare the chain, rounds not written yet")
    assert not (repo / ROUNDS).exists(), "the fixture is not the no-rounds state"
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert GATE_FILE in out and "round-N.md" in out, (
        "the refusal names neither the home it declined nor the record it wants"
    )
    assert not (repo / ITEM / GATE_FILE).exists(), (
        "the cell went into the home the chain arm never reads"
    )
```

🟡 2 — `tests/test_a_moved_rule_leaves_its_definition.py`, extending the first
entry of `MOVED_OUT_OF_SMITH`:

```python
    "the design gate": (
        "you own this decision, and no skill makes it for you",
        "Ask everything that needs a person here, in one batch",
        # The SECOND copy, sixty lines below the span `plan.md` measured the
        # first at, and the design gate by CONTENT: present approaches and
        # wait for a go. Left standing it would have had the file say `phase 2
        # is your caller's spawn` in one paragraph and `wait for an explicit
        # go` in another. It was removed with the others and held by nothing
        # -- pasting it back left 242 cases green.
        "wait for an explicit go",
    ),
```

🟡 3 — `tests/test_waiver_decided_at_start.py`, replacing
`test_the_preset_block_carries_it_too`:

```python
def test_the_preset_block_carries_it_too():
    """`CLAUDE.md` is the one file a session in this repository always has.

    So it is the copy that matters most, and it was the copy nothing held. The
    block kept its old three-checkbox paragraph and every case stayed green --
    `claude_block.py --check` included, because that command compares the
    template with its generated copy and neither with the question. Asserted
    at BOTH ends, and the absence half is the half that would have caught it.
    """
    for parts in (("templates", "claude-md-block.md"), ("CLAUDE.md",)):
        text = flat(read(*parts))
        where = "/".join(parts)
        assert "seal/specs/<work-item-id>/routing.md" in text
        for answer in AXES:
            assert answer in text, f"{where} lost the answer `{answer}`"
        assert "two questions in ONE `AskUserQuestion` call" in text, (
            f"{where} still asks the old question, and the block is what a "
            "session in an opted-in repository always has in front of it"
        )
        for stale in ("two axes", "three axes", "three checkboxes"):
            assert stale not in text, (
                f"`{stale}` survived in {where}, so every session reads the "
                "shape the rest of the repository stopped describing"
            )
```

🟡 4 — `agents/framer.md`, after the paragraph at line 228:

```markdown
**If you have no way to put the question to a person, do not answer it
yourself.** `AskUserQuestion` is the only shape this batch has, and an agent
that cannot reach it has no second one. A `routing.md` written from a guess is
a recorded answer nobody gave, which is the failure the `Answer pressed` row
exists to end, arriving through the door this act opened. Write no declaration,
hand the batch back in your report with both questions laid out, and let your
caller ask it and write the file. Say in the report that this is what happened,
so the missing declaration is a sentence somebody reads rather than a gap the
commit gate discovers later.
```

🟡 5 — `seal/ledger.md`, `Checked` set to `2026-09-16` on the rows carrying
these nine re-stamped anchors, and nowhere else:

```
skills/code-review/scripts/chain_check.py#main@4d2b2027
skills/code-review/scripts/chain_check.py#broad_gate@e22933ea
skills/code-review/scripts/chain_check.py#"# The vocabulary as a match ORDER, longest spelling first, so the `fixed`"@e4bb7dc9
skills/code-review/scripts/round_record.py#seal@323b8f3f
hooks/routing.py#parse@e7fdae99
agents/smith.md#"## Phases"@61d693d7
skills/implement/SKILL.md#"## Document layout — two roots, three lifetimes"@9b41faf9
skills/implement/SKILL.md#"### 3. The SDD file set"@1feca58a
CLAUDE.md#"## Git">"Routing, decided at the start"@0b59a3ef
```

Needs a fix: yes — 🟡 1 the seal's home is chosen without reading the
declaration, 🟡 2 and 🟡 3 two removals this branch made deliberately that no
case holds, 🟡 4 the framer may have no tool for the act it was handed, and
🟡 5 nine ledger rows whose re-read is recorded nowhere.
Loses a record or crashes: no — 🟡 1 misfiles the `Broad gate` cell rather than
dropping it, and both directions of the misfiling fail the pull request closed.

---

## Proof block

Read at `655eaf7c`, in a `git clone --no-local` at that commit:

`seal/specs/1789518345-…/{spec,plan,overview,questions,routing,survivors,changelog}.md` ·
`skills/code-review/scripts/chain_check.py` ·
`skills/code-review/scripts/round_record.py` · `hooks/routing.py` ·
`agents/{framer,smith,warden,sealer,scribe}.md` ·
`skills/implement/{SKILL.md,orchestration.md}` ·
`templates/{sdd-routing,sdd-spec,claude-md-block}.md` · `CLAUDE.md` ·
`seal/ledger.md` · `seal/config.md` · `bin/test` · `bin/evidence-check` ·
`skills/evidence-check/scripts/evidence_check.py` ·
`tests/{test_waiver_decided_at_start,test_a_moved_rule_leaves_its_definition,test_chain_check_at_the_pull_request,test_chain_hooks_hardening,test_the_seal_is_taken_once_by_the_sealer,test_routing_is_recorded}.py` ·
`gh issue view 88 / 399 / 419`.

Not read: `tests/test_routing_is_recorded.py`'s full body (run, not read line by
line), the unchanged remainder of `chain_check.py` and `round_record.py` outside
the diff and the functions the diff calls.
