# 1790562540-a-resumed-agents-own-transcript-is-sliced — review round 1

| Field | Value |
|---|---|
| Target SHA | 7b4162fd7b2e481b1e494cdb3110a9b58423a438 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #649 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 1, the plain hint claims a wait inside the span of a file whose calls fall in one stretch |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790562540 (#637), a first round against the whole branch `fix/637-a-resumed-agents-own-transcript-is-sliced` at 7b4162fd, base origin/release/v0.15.7 (1fa25931), draft PR #649. Judge spec compliance against spec.md first (In 1–6, D1–D11, S1–S12, and the trigger chosen as the coordinator marker rather than the `subagents/` directory), then quality. The class to enumerate: every path through `session_cost.py` that reads one transcript and decides whether it has segments or slices (`--segments`, `--spawns`, `--json`, `--post`, plain, `--latest`), and every sentence in skills/, docs/, both READMEs and test docstrings that states what `--segments` or the plain reading prints for an agent's own file. Confirm that no existing printed line or JSON shape moved for a file without the marker, and that item B's units (`FAMILIES`, `family`, `analyse`, `report`, the comparability lines at the end of `report_segments`) carry no hunk. The hint's position after `--latest`'s path line was read, not executed, by the builder (overview.md `## Not verified`): judge whether it needs a case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The plain hint says the span covers the waits between stretches for a file whose calls all fall in one stretch, where the span covers no wait and `--segments` prints one slice of the same figure | `skills/verify/scripts/session_cost.py:2776` | open | executed on a fixture (C1); reachable, 0 of 47 real marker files; the causal clause is the builder's wording and In 4 did not ask for it |
| ⬜ 2 | In 1's "a resumed file copied out of `subagents/` is still cut" is pinned by no case | `tests/test_session_cost.py:3418` | open | coverage probe: the trigger and hint gated on `/subagents/` leave 157 passed; code correct by reading |
| ⬜ 3 | The changelog and overview count four whole-transcript fix-pass readings in #535; there are five | `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/changelog.md:27` | open | record correction; five comments opened with `gh issue view 535`; also `overview.md:19` |
| ⬜ 4 | The counts paragraph says a header stands in for the counts given any agent's own file; only a resumed one gets it | `skills/verify/SKILL.md:625` | open | read; a marker-less agent file prints the empty branch |
| ⬜ 5 | The resumed paragraph on an own-file page says only the file's opening could be joined | `skills/verify/scripts/session_cost.py:2261` | open | In 2 asks for it as on a walked page; the legend above says no spawn was joined; no change owed |
| 🟢 | The trigger is the coordinator marker and not the directory | `skills/verify/scripts/session_cost.py:1550` | confirmed | read; the walked-whatever-its-markers case is planted |
| 🟢 | No printed line or JSON shape moved for a file without the marker | `skills/verify/scripts/session_cost.py` | confirmed | executed, base against head, 316 real files by four modes; the 47 marker files differ by the hint and `own_file` rows only |
| 🟢 | Own-file slices equal the walked slices for the same agent | `skills/verify/scripts/session_cost.py:1550` | confirmed | executed, 48 of 48 real marker files |
| 🟢 | Item B's units carry no hunk | `skills/verify/scripts/session_cost.py` | confirmed | executed, `git diff -U0` hunk headers |
| 🟢 | The hint lands after the `--latest` path line, and no case is owed | `skills/verify/scripts/session_cost.py:2684` | confirmed | executed (C2); by construction in `main`, the hint's position before `span` is pinned |
| 🟢 | D1–D11 corrected, and no further sentence in the class is false | `skills/verify/SKILL.md:599` | confirmed | read; searched skills, docs, agents, templates, hooks, both READMEs and test docstrings |

## Paste-ready fixes

```python
    # The line says the span covers a wait between stretches of work, so it
    # needs two stretches. A marker does not guarantee them: a coordinator
    # message after the agent's last call, or before its first, leaves one
    # window with calls, the span covers no wait, and `--segments` prints one
    # slice of the same figure.
    cuts = [] if beside else resume_cuts(path)
    stretches = sum(1 for w in in_windows(cuts, calls, lambda c: c["start"]) if w)
    restarted = len(cuts) if stretches > 1 else 0
```
```python
def test_no_hint_where_every_call_sits_in_one_stretch(tmp_path):
    """A coordinator message after the agent's last call cuts nothing: the
    window after it holds no call, so the file is one stretch, its span covers
    no wait, and `--segments` prints one slice with the same span. A line
    saying the span covers the waits between stretches is false there."""
    path = write_run(
        tmp_path,
        call("a", 0, 10, "git status --short"),
        {
            "agent-smith.jsonl": [
                *worked(625, "s1"),
                *worked(640, "s2"),
                coordinator_message(9000),
            ]
        },
    )
    out = " ".join(run([str(own_file(path))]).stdout.split())
    assert "coordinator message in this transcript" not in out, out
    assert out.startswith("span "), out
```
```python
def test_a_resumed_file_copied_out_of_subagents_is_still_cut(
    resumed_segment, tmp_path
):
    """In 1: the trigger is the marker, never the directory. A resumed
    agent's file copied anywhere else is cut the same way, and its plain
    reading carries the same line. Every other own-file case sits under
    `subagents/`, so a directory condition added to either trigger kept them
    all green."""
    copied = tmp_path / "copied-agent.jsonl"
    copied.write_text(own_file(resumed_segment).read_text())
    rows = segments_of(copied)["rows"]
    assert [(row["slice"], row["slices"]) for row in rows] == [(1, 2), (2, 2)], rows
    assert segments_of(copied)["own_file"] is True
    out = run([str(copied)]).stdout
    assert out.startswith("1 coordinator message in this transcript,"), out
```
```
  because `--segments` could not split it: four in #577, five in #535 and
```
```
   holding. Given a resumed agent's own file, nothing is walked or joined,
   and a header naming the file and its coordinator messages stands in their
   place.
```

## Executed probes

| What was run | Result |
|---|---|
| Base (1fa25931) and head (7b4162fd) session_cost.py imported in-process, plain, `--segments`, `--json` and `--spawns` over every `*.jsonl` under ~/.claude/projects/ for this repository's project directories (363 files, 47 with the own-file trigger) | exit 0; 316 marker-less files identical in stdout and exit in all four modes, except one live session transcript whose `segments.rows` changed between passes as its agents wrote; 47 marker files differ by the hint block (plain) and by `rows` and `own_file` (`--json`) only, `--spawns` identical |
| The 47 marker files: slices against coordinator messages plus one | 0 files cut into one slice, 0 with fewer slices than messages plus one |
| Fixture C1: two calls, then a coordinator message answered in text only, under `main/subagents/` | plain prints the hint and `span 0.5m (2 tool calls)`; `--segments` prints `cut at 1 coordinator message into 1 slice` and one 0.5m row |
| Fixture C2: `PROJECTS` pointed at a fixture project whose newest file is a resumed agent's; `--latest` and `--latest --segments` | exit 0 both; `# <path>`, blank, hint; and `# <path>`, blank, own-file header |
| Coverage probe: the `measure_segments` trigger and the hint condition both gated on `/subagents/` in the absolute path; `bin/test tests/test_session_cost.py tests/test_session_cost_post.py` | exit 0, 157 passed, so the mutant survives; restored with `git checkout` and the clone's status read clean |
| `bin/test tests/test_session_cost.py tests/test_session_cost_post.py tests/test_a_segment_feeds_the_flow_log.py` at 7b4162fd, unmutated | exit 0, 191 passed |
| S12 over every marker file: own-file rows against the walked rows from the session's main transcript, label fields dropped | 48 marker files at run time, 48 equal, 0 differ |
| `gh issue view` 496, 535, 577, 601 and 619, fix-pass comments by the phrase naming their source | #577 4, #535 5 and #601 6 whole transcript; #496 4 and #619 3 harness figures; #535's five opened and read |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — nobody has run it; the sealer runs it once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
