# 1790562540-a-resumed-agents-own-transcript-is-sliced — review round 2

| Field | Value |
|---|---|
| Target SHA | d617b65c7892082de9ff4a1e729cf26b345508ea |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #649 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `47fceb979870cc329b8e3f00455ec008392615c3..8ccb2b359d248b328001b80ed14d3b31b585bc24`, 2 commits |
| Contract changes | none |
| New units | test_no_hint_where_the_only_message_precedes_the_first_call (depth 1) |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790562540 (#637), the verifying round. Its target is the diff of round 1's fixes, f37fe53f..7291825a (328b379d code and cases, 7291825a record corrections, ledger and re-reads), with the branch at d617b65c and draft PR #649. The job is the answers, not new findings: for each verdict round-1.md records as closed (🟡 1, ⬜ 2 and ⬜ 4 fixed, ⬜ 3 and ⬜ 5 answered), is it actually closed. The finding surface is round 1's `New units`: `test_no_hint_where_every_call_sits_in_one_stretch` and `test_a_resumed_file_copied_out_of_subagents_is_still_cut` (depth 1), plus the narrowed hint condition in `main`, which nobody has reviewed. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The narrowed hint names two shapes that cut nothing (a message after the last call, one before the first); only the first is pinned, and a condition wrong for the second leaves both modules green | `tests/test_session_cost.py:3702` | **fixed** `77365e87` | fixed at 77365e87; executed: the mutant *a call starts at or after the first message* leaves 159 passed; the fenced case is green at d617b65c and red under it; the code is correct by reading and on a fixture |
| 🟢 | round 1's finding 1 is closed — the plain hint prints only where the messages cut the calls into two stretches or more | `skills/verify/scripts/session_cost.py:2785` | confirmed | executed: red at 7b4162fd's code, green now; 49 of 49 real own files print it exactly where `--segments` gives two rows or more; the equivalence with `segment_slices` holds by construction (read) |
| 🟢 | round 1's finding 2 is closed — a resumed file copied out of `subagents/` is pinned | `tests/test_session_cost.py:3725` | confirmed | executed: directory mutants on the trigger, the hint, and both each turn this case alone red |
| 🟢 | round 1's finding 3 is closed — the records count five readings in #535 | `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/changelog.md:29` | confirmed | read: changelog and overview say five; executed: `gh issue view 535` shows five whole-transcript comments |
| 🟢 | round 1's finding 4 is closed — the counts paragraph says a resumed agent's own file | `skills/verify/SKILL.md:625` | confirmed | read; the lone-segment paragraph states the narrowed condition too; the section's cases pass (executed) |
| 🟢 | round 1's finding 5 answer stands — the resumed paragraph follows In 2 | `skills/verify/scripts/session_cost.py` | confirmed | read: no hunk in the fix diff touches `report_segments`' resumed paragraph or the legend above it |
| 🟢 | The narrowed condition in `main` is correct, and cannot crash | `skills/verify/scripts/session_cost.py:2785` | confirmed | read: `load` drops calls with an unparsed start; empty `cuts` gives one window; executed on before-first, after-last and mixed fixtures |

## Paste-ready fixes

```python
def test_no_hint_where_the_only_message_precedes_the_first_call(tmp_path):
    """The other shape that cuts nothing: a coordinator message before the
    agent's first call leaves every call in the window after it, so the file
    is one stretch and `--segments` prints one slice with the same span. The
    one-stretch case above builds only the message after the last call, and
    a condition of *a call after the first message* is right there and wrong
    here."""
    path = write_run(
        tmp_path,
        call("a", 0, 10, "git status --short"),
        {
            "agent-smith.jsonl": [
                coordinator_message(600),
                *worked(625, "s1"),
                *worked(640, "s2"),
            ]
        },
    )
    out = " ".join(run([str(own_file(path))]).stdout.split())
    assert "coordinator message in this transcript" not in out, out
    assert out.startswith("span "), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py tests/test_session_cost_post.py tests/test_a_segment_feeds_the_flow_log.py` plus a scratch probe module named test_tmp_r2, at d617b65c, unmutated | exit 0, 196 passed (193 in the three modules, 3 in the probe) |
| 7b4162fd's `session_cost.py` in place, `bin/test tests/test_session_cost.py tests/test_session_cost_post.py` | exit 1, 1 failed, 158 passed: `test_no_hint_where_every_call_sits_in_one_stretch` |
| Mutant: the hint gated on *a call starts at or after the first message*, same two modules | exit 0, 159 passed; the mutant survives (⬜ 1) |
| Mutant: the hint gated on *a call starts before the last message*, same two modules | exit 1, 1 failed, 158 passed: the one-stretch case |
| Mutants: `/subagents/` in the absolute path required by both triggers, by the hint alone, and by `measure_segments` alone, same two modules | each exit 1, 1 failed, 158 passed: `test_a_resumed_file_copied_out_of_subagents_is_still_cut` |
| Fixture, one message at 600s before calls at 625s and 640s: plain and `--segments` | plain starts `span 0.3m (2 tool calls)`, no hint; one slice |
| Fixture, messages at 600s, 9000s and 9500s around calls at 625s and 9010s: plain and `--segments` | plain starts *3 coordinator messages in this transcript*; `--segments` *cut at 3 coordinator messages into 2 slices* |
| The fenced before-first case, at d617b65c and under the surviving mutant | green, and red (1 failed) |
| Every `*.jsonl` under this repository's project directories on this machine, plain and `--json`, at d617b65c | 367 files, 64 with the marker text, 49 taken as an own file; hint present iff `--segments` rows are two or more, 49 of 49; 0 own files with one slice; exit 0 on all 64 |
| `gh issue view 535 --json comments`, comments carrying the whole-transcript phrase | 5 |
| `bin/evidence-check --strict .` in the clone at d617b65c | exit 0; 0 drifted, 0 refused |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — nobody has run it; it comes due now, and it is the sealer's spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:2776` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_session_cost.py:3418` | round 1's ⬜ 2 — fixed |
| round-1 | `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/changelog.md:27` | round 1's ⬜ 3 — answered |
| round-1 | `skills/verify/SKILL.md:625` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:2261` | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:1550` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/session_cost.py` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/session_cost.py:2684` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/SKILL.md:599` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
