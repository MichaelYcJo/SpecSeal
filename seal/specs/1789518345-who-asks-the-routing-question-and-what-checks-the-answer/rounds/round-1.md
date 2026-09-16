# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — review round 1

| Field | Value |
|---|---|
| Target SHA | 655eaf7c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 421 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 the seal's home is chosen without reading the declaration, 🟡 2 and 🟡 3 two removals this branch made deliberately that no case holds, 🟡 4 the framer may have no tool for the act it was handed, and 🟡 5 nine ledger rows whose re-read is recorded nowhere. |
| Loses a record or crashes | no — 🟡 1 misfiles the `Broad gate` cell rather than dropping it, and both directions of the misfiling fail the pull request closed. |

- [ ] Pass

## What this round was asked

Round 1 of the run, against the whole branch — there is nothing earlier to
inherit. Spec compliance first against `spec.md`'s acceptance rows and
`plan.md`'s seven phases, then quality.

This is the third work item in this release whose subject is a check that
cannot fail, and the first two each produced a repair that was itself held by
nothing. So the round was pointed hardest at the two rules that came out of
those: pin the function the production path calls rather than the helper
beside it, and check that a case's own assertion can fire before a fixture's
guard does.

It was also asked to check three things the build reported rather than to
trust them: that the mark is read from the foot of `spec.md` and not from
anywhere in it, that the nine drifted ledger rows were re-read rather than
only re-stamped, and that five existing cases inverted by this work now pin
the new behaviour rather than merely stopping to fail.

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

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `Checked` column records no re-read, so `--reverify` cannot report the half that was skipped | `skills/evidence-check/scripts/evidence_check.py:1577`'s standing `# RIDER:`, and #120 round 1 | the repository owner — 🟡 5 asks only for this branch's nine rows, not for the mechanism |
| A durable record that a person chose `no work item` | already deferred by `overview.md` §*Not done* as a ticket for the orchestrator to open | the repository owner, at the ticket |
| Promoting the approval-line notice to a refusal | already deferred by `overview.md` §*Not done*; #399's `Done when` asked for a refusal and this ships a notice on a measurement the ticket did not have | the repository owner, after two or three releases carry the notice |
