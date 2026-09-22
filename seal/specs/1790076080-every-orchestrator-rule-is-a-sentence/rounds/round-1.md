# 1790076080-every-orchestrator-rule-is-a-sentence — review round 1

| Field | Value |
|---|---|
| Target SHA | 238dbeafea0dd8b3105bf9ab045371bfcd10fa6b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 498 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `238dbeafea0dd8b3105bf9ab045371bfcd10fa6b..da35172fc5deaff640f89989fad447788ac90e04`, 4 commits |
| Contract changes | emit → round-1-report.md, round-1.md, main; _delivery → round-1-report.md, round-1.md, pytest |
| New units | test_a_named_path_is_resolved_against_the_tree_under_check (depth 1); test_the_posted_body_does_not_carry_the_transcripts_path (depth 1); test_the_spawns_report_leaks_no_path_either (depth 1); test_an_empty_reading_is_refused_rather_than_posted (depth 1); test_an_empty_reading_is_refused_before_the_log_is_looked_up (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first reading of the built branch, with nothing to inherit. The
round was asked for spec compliance first and quality second, against the
frame rather than against #330, and was pointed at four things in particular.

The two places the build reports the frame did not hold, each to be judged
rather than accepted: the table ships twenty rows where `spec.md` says
nineteen, because the section holding the table is itself an act; and phase 3
had no row to flip, so the flow-log act is carried as a paragraph — whether
that paragraph still says nothing makes the act run is the question, because a
closed-looking row is the failure the spec names.

The twenty rows' cells as the deliverable: each `Delivered by` answers *when
the orchestrator forgets this act, what notices*, so each row's section and
each cell's path were to be opened, and a row whose delivery reaches only part
of its act and carries no sentence saying so is a finding.

The decision shipped on a default: no row added to `CONTRIBUTING.md`'s list of
the plugin's network touches for the first arm that writes over the network.

And the claims with coordinates behind them: nine rows of `seal/ledger.md`
re-read against a drifted anchor, a contract change to `marked_headings`
reaching another module's callers, and six new units in `session_cost.py`.

The broad gate was withheld. The narrow suites and the lint the orchestrating
session had already run were named so the round would not spend itself
repeating them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `--post` writes the transcript's absolute path, under the user's home directory, into a public issue tracker | `skills/verify/scripts/session_cost.py#emit`, `#report_segments`, `#report_spawns` | **fixed** `ef010857` | fixed at ef010857; Executed with the `gh` seam stubbed: `--segments --post` posted a body whose fenced reading opens `0 segments found beside <absolute path>`. `main` already keeps `--latest`'s path line out of the body, so the rule exists in the file and is applied in one place of three |
| 2 | 🟡 `--post` posts a comment with no judgment when `--says` names an empty file | `skills/verify/scripts/session_cost.py#emit`, `#comment_body` | **fixed** `ef010857` | fixed at ef010857; Executed: an empty `--says` posted a body opening on the fence, exit 0. `spec.md` §Scope says *refuses to post without a reading*, and the refusal is against the flag only |
| 3 | 🟡 `_delivery` resolves the named path against `ROOT` rather than the root `findings` was given, so the floor case under all four red directions is green by leak | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | **fixed** `ef010857` | fixed at ef010857; Executed: the path `SELF` names is absent from the planted tree, present in the repository, and `test_a_clean_planted_tree_is_clean` is still clean. A3 therefore demonstrates *absent from the repository*, not *absent from the tree under check* |
| 4 | 🟡 The row `And name the fix surface, in the same record` names no part its delivery does not reach, against the discipline its own section states | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | **fixed** `ef010857` | fixed at ef010857; `round_record.py`'s `New units` reads top-level `def`/`class`/constants and, for a file the AST cannot read, `+` lines for five keywords. A template section, a skill rule or a walk matches none, so that surface never reaches the cell. Row 12 names the same blind spot for depth; this row names none |
| ⬜ | `eight rows` carry a limit sentence; eleven do | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` O1, `overview.md`, `phases/phase-1.md` | correction | Counted all fourteen delivered rows. The discipline holds and the aggregate does not; O1 is a ledger row, where a count outlives the round |
| ⬜ | Q3 ships on the right answer for a reason the section does not supply | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `questions.md` Q3 | correction | Opened `CONTRIBUTING.md`: the bullet is **Hooks stay local and quiet** and its list is of hooks, which settles Q3 more cleanly than *touches that fire unasked*. Default (a) stands; the grounds should name the scope |
| 🟢 | Twenty rows is right, and the case pinning the self-reference pins it | `skills/implement/orchestration.md`, `tests/test_every_orchestrator_act_names_its_delivery.py#test_the_table_reads_the_section_that_holds_it` | confirmed | Executed the parser against the tree: 20 acts, 20 rows, no findings. `spec.md`'s two sentences cannot both hold at nineteen, and the self-reference is closed from two directions rather than one |
| 🟢 | The flow-log paragraph says what the row would have said and does not read closed | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | confirmed | Read: it names the act, the file, `session-cost … --post`, and *"**And nothing makes it run.**"* with the grounds beside it |
| 🟢 | The nine re-read ledger rows are additive; no prior note was dropped | `seal/ledger.md` | confirmed | Every prior `Re-read <date>` count is identical at base and head; `Re-read 2026-09-22` moves 18 → 27 |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle |

## Paste-ready fixes

```python
def emit(args, render, path=None):
    """Print the report, or capture it and post it. Returns the exit code.

    **What is printed locally and what is posted are not the same text.**
    `report_segments` and `report_spawns` name the transcript by its full
    path, which lives under the user's home directory and carries the account
    name. `--post` writes into an issue tracker, so the captured body carries
    the basename instead. `main` already keeps `--latest`'s `# <path>` line
    out of the body by printing it before this call; this is that same rule
    for the reports that print the path themselves.
    """
    if not args.post:
        render()
        return 0
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        render()
    body = buffer.getvalue()
    if path:
        short = os.path.basename(str(path))
        for form in (os.path.abspath(str(path)), str(path)):
            body = body.replace(form, short)
    says = read_says(args.says)
    if not says.strip():
        print(
            f"`--says {args.says}` gave no reading, so nothing was posted. "
            f"The numbers are this script's and what they say is not, and an "
            f"empty reading posts a fence with nothing above it — which is "
            f"the judgment nobody made that `--says` exists to refuse"
        )
        return 1
    return post(body, says, args.label)
```
```python
        return emit(
            args,
            lambda: report_spawns(
                spawns, path, len(calls), timings["span_s"] if timings else 0.0
            ),
            path,
        )
```
```python
        return emit(args, lambda: report_segments(segments, path), path)
```
```python
    return emit(args, render, path)
```
```python
def test_the_posted_body_does_not_carry_the_transcripts_path(
    monkeypatch, tmp_path, transcript
):
    """`--post` writes into an issue tracker, and a transcript path lives
    under the user's home directory. The report prints it; the body must not.
    `report_segments`' empty branch is the one the documented invocation hits
    whenever the named transcript has no subagents beside it, which is every
    segment measured on its own."""
    module = _cost()
    says = tmp_path / "says.md"
    says.write_text("one call, ten seconds of it\n", encoding="utf-8")
    _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    bodies = {}
    stub = module.run_gh

    def capture(args):
        if args[:2] == ["issue", "comment"]:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as handle:
                bodies["text"] = handle.read()
        return stub(args)

    monkeypatch.setattr(module, "run_gh", capture)
    monkeypatch.setattr(
        module.sys,
        "argv",
        [
            "session_cost.py",
            str(transcript),
            "--segments",
            "--post",
            "--says",
            str(says),
        ],
    )
    assert module.main() == 0
    assert str(transcript) not in bodies["text"]
    assert os.path.dirname(str(transcript)) not in bodies["text"]
    assert os.path.basename(str(transcript)) in bodies["text"]
```
```python
def test_an_empty_reading_is_refused_rather_than_posted(
    monkeypatch, capsys, tmp_path, transcript
):
    """The invariant is that the numbers are the script's and the sentence is
    not. Enforced against the missing flag alone, `--says` naming an empty
    file posts a fence with nothing above it — and that is the shape a session
    reaches by accident, with `--says -` and nothing piped in."""
    module = _cost()
    says = tmp_path / "empty.md"
    says.write_text("   \n", encoding="utf-8")
    seen = _gh(monkeypatch, module, listing=_listing((42, "OPEN")))
    monkeypatch.setattr(
        module.sys,
        "argv",
        ["session_cost.py", str(transcript), "--post", "--says", str(says)],
    )
    assert module.main() == 1
    assert _posted(seen) == [] and _opened(seen) == []
    assert "no reading" in capsys.readouterr().out
```
```python
        out += _delivery(root, act, rel, known[key], delivered, grounds)
```
```python
def _delivery(root, act, rel, level, delivered, grounds):
    """The `Delivered by` cell's own defects, as lines.

    Paths resolve against `root`, the tree `findings` was given, and never
    against this module's own repository: a planted tree checked against the
    repository is green for files it does not carry, which is the floor case
    passing by leak rather than by being clean.
    """
```
```python
    if not os.path.exists(os.path.join(root, *path.split("/"))):
```
```python
    named = os.path.join(base, "tests", "test_every_orchestrator_act_names_its_delivery.py")
    os.makedirs(os.path.dirname(named), exist_ok=True)
    with open(named, "w", encoding="utf-8") as handle:
        handle.write("# the check `SELF`'s row names, so the tree carries it\n")
    return str(base)
```
```
| And name the fix surface, in the same record | `skills/code-review/orchestration.md` | command: `bin/round-record` | `close` writes `Contract changes` and `New units` from the fix range, so the rows cost no question to anybody. Before it did, one record sat at its starting values for two rounds and the six units its fix pass created reached the next round only because a reviewer went and looked. What the derivation does not reach is a surface with no unit in it: `New units` reads top-level defs, classes and module constants, and for a file the AST cannot read the `+` lines for five keywords, so a fix pass that adds a template section, a skill rule or a walk names an empty surface and nothing refuses it |
```

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_every_orchestrator_act_names_its_delivery.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py tests/test_session_cost_post.py`, in a clone at the target SHA | 46 passed — matches the phase records |
| Coverage probe — `--segments --post --says <file>` on a transcript with no subagent transcripts, `run_gh` replaced | The posted body's fenced reading opens `0 segments found beside <the transcript's absolute path>`. Finding 1 |
| Coverage probe — `--post --says <a file holding one space>`, `run_gh` replaced | Exit 0, one comment posted, body's first non-blank character is the opening fence. Finding 2 |
| Coverage probe — `findings()` on the module's own planted clean tree, asserting the path `SELF` names is absent from that tree | Absent from the tree, present in the repository, findings still `[]`. Finding 3 |
| The parser against the tree — `acts()`, `rows()`, `findings()` | 20 acts, 20 rows, no findings |
| `evidence_check.py --ledger seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md .`, in the clone | Exit 0 — 8 ok, 0 drifted, 0 broken |
| Every `Re-read <date>` marker in `seal/ledger.md`, counted at base and at head | Every prior date identical; `Re-read 2026-09-22` 18 → 27 |
| `gh issue view 496`, the last comment | Read. A `--spawns` reading over eight spawns; the leaking branch never fired |
| The broad gate — full suite, repository-wide lint, typecheck | not yet. It is the sealer's, once, after the rounds settle; this round did not run it and must not |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is — the repair is either a row rule taking a named list of sections elsewhere, or splitting the `Orchestrator:` marker into two meanings | `overview.md` §*Not done*, named for an issue rather than built here | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so a twenty-first act written without the prefix is counted by nobody | `overview.md` §*Not done*, and the section's own *What this does not catch* paragraph | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a) | the repository owner, who owns that list. See the ⬜ correction above for the grounds the section actually supplies |
