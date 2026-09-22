# 1790076080-every-orchestrator-rule-is-a-sentence — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `238dbeafea0dd8b3105bf9ab045371bfcd10fa6b` |
| Base | `origin/release/v0.13.1` at `6d41002398bfeeb55db08cca9b441b68e0267049` |
| Branch | `docs/330-every-orchestrator-rule-is-a-sentence` |
| Inherited | nothing — this is round 1 and the work item's `rounds/` directory was empty |

Read in a `git clone --no-local` of the worktree at the target SHA, with a
`uv` virtual environment inside it. The clone and the one probe file are
deleted; the worktree is clean.

## Stage 1 — spec compliance

The frame is `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`
and the three phase records. Acceptance A1 to A11 are all met, and two of them
are met in a shape the frame did not predict. Both divergences are recorded in
`overview.md` §*Where spec and implementation diverged*, and I judged each
against the frame rather than against the record of it.

**The twenty rows are right, and the case pinning them pins what it claims.**
`spec.md` §Scope states the row set as *every `##` heading whose text begins
`Orchestrator:` in either orchestration file, plus every `###` heading
directly beneath one*, and in the same bullet says the new section *"makes
the section a row of its own table"*. Those two sentences cannot both hold at
nineteen. Counted against the tree: `skills/implement/orchestration.md` has
five marked `##` headings — lines 34, 44, 226, 243 and the new one at 477 —
with three `###` beneath one of them, and `skills/code-review/orchestration.md`
has five with seven. Twenty. Executed the parser against the tree: twenty acts,
twenty rows, no findings.

The self-reference is pinned from two directions rather than one, which is
what makes it hold. `test_the_table_reads_the_section_that_holds_it` asserts
the section is read as an act; the real-tree case asserts an act with no row
fails. Neither alone would catch a table that exempted its own section — the
first passes over a missing row, the second passes over a section the parser
never reaches. Together they close it.

**The flow-log paragraph says what the row would have said, and it does not
read closed.** It names the act, the file
(`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*), the
delivery (`session-cost … --post`), and the sentence the spec §*The limit this
work does not close* demands: *"**And nothing makes it run.**"* It then says
why — the meter sat unreferenced through a day of measurements nobody took,
so the measurement was not taken rather than the posting failing. The same
sentence stands in `skills/verify/SKILL.md` itself. The requirement was met
where it could be met, and the reason it could not be met as a row is stated
in the section rather than left to be found.

**Where the record overstates, it does so in an aggregate.** `overview.md`,
`phases/phase-1.md` and ledger row O1 each say *eight rows* carry a sentence
naming the part of their act the delivery does not reach. Reading all fourteen
delivered rows, eleven do. See the correction below — the claim is a count,
which is checkable, and the discipline behind it holds.

## Stage 2 — quality

### 🔴 1 · `--post` publishes an absolute filesystem path to a public issue tracker

`skills/verify/scripts/session_cost.py`, `emit`, and the two report functions
it captures.

`emit` renders the report into a buffer and hands the whole buffer to `post`,
which writes it as a comment body. Two of the three reports print the
transcript's full path on their empty branch:

- `report_segments` — `print(f"0 segments found beside {path}\n")`
- `report_spawns` — `print(f"0 spawns found in {path}\n")`

In use that path is a transcript under the user's home directory, of the form
`/Users/x/.claude/projects/-Users-x-<repo-path>/<session-id>.jsonl`. It
carries the account name twice and the session id once, and `--post` writes it
into whatever issue the label resolves to.

**The branch that leaks is the documented one.** The command the edited
`skills/verify/SKILL.md` now prints is
`session-cost --segments <the run's transcript> --post --says <file|->`, and
`report_segments`' empty branch fires whenever the named transcript has no
subagent transcripts beside it — which is every segment measured on its own,
the case the surrounding section is written for. `--spawns --post` has the
same branch.

**`main` already treats the path as terminal-only one line away.** With
`--latest` it prints `# {path}` *before* calling `emit`, so that line never
reaches the body. The two reports that print the path themselves were not
given the same treatment, so the rule exists in the file and is applied in one
place of three.

Why it matters beyond tidiness: this is the plugin's first arm that writes
over a network, `CONTRIBUTING.md` §*Hooks stay local and quiet* states the
repository's position as *"anything that would send repository contents,
paths, or prompts is not on the table"*, and `CLAUDE.md` records that both
incidents which forced a history rewrite entered as real identifiers. A
comment on a public tracker is repaired by a person deleting it, which is the
failure direction `plan.md` §*Operational impact* says the design is meant to
avoid.

**Executed**, with `run_gh` replaced: `--segments --post --says <file>` against
a transcript with no subagents posted a body whose fenced reading opens
`0 segments found beside <the transcript's absolute path>`.

### 🟡 2 · An empty `--says` posts a comment with no judgment in it

`skills/verify/scripts/session_cost.py`, `emit` and `comment_body`.

The invariant the whole mode rests on is that the numbers are the script's and
the sentence is not. It is enforced against a missing flag only: `main`
refuses `--post` without `--says`, and nothing reads what `--says` points at.
A `--says` naming an empty or whitespace-only file produces
`comment_body("", reading)` — a body that begins with a blank line and then
the fence, posted, exit 0.

`spec.md` §Scope states the requirement as *"It refuses to post without a
reading"*, not *without the flag*. An empty file is without a reading, and it
is the shape a session reaches by accident: `--says -` with nothing piped in,
or a file a previous step wrote nothing to.

**Executed**: `--post --says <a file holding one space>` posted a body whose
first non-blank character is the opening fence, and exited 0.

### 🟡 3 · The planted trees' path check resolves against the real repository, not the tree under check

`tests/test_every_orchestrator_act_names_its_delivery.py`, `_delivery`:

```python
    if not os.path.exists(os.path.join(ROOT, *path.split("/"))):
```

`findings(root)` takes a root and is documented as answering about it —
*"Empty on a clean tree"* — and every planted case calls it with a temp tree.
`_delivery` alone ignores that root and resolves the named command or check
against `ROOT`, the module's own repository.

**The floor case is what this costs.** `test_a_clean_planted_tree_is_clean`
exists to prove the planted tree carries no defect other than the one each
direction plants. Its table includes `SELF`, whose delivery names
`tests/test_every_orchestrator_act_names_its_delivery.py` — a file `_tree`
never writes. Executed: that path is absent from the planted tree, present in
the repository, and `findings` on the planted tree still returns `[]`. The
floor holds by leak.

The consequence for §15 is narrower but real: `test_a_named_command_must_exist`
shows red for a row naming `bin/does-not-exist`, which is absent from both
trees. What it demonstrates is *a path absent from the repository is named*,
not *a path absent from the tree under check is named* — and the second is
what `findings(root)`'s contract says. A row naming a path that exists in the
repository but not in a tree being checked passes silently.

The real-tree case is unaffected, because there `root` and `ROOT` are the same
directory. Nothing shipped is wrong today; what is wrong is that one of the
four red directions and the floor beneath all four are not testing the tree
they plant.

### 🟡 4 · Row 14's grounds name no part its delivery does not reach

`skills/implement/orchestration.md` §*Orchestrator: which of these acts runs
itself*, the row `And name the fix surface, in the same record`.

The section states its own discipline: *"the grounds of a row whose delivery
reaches only part of its act name the part it does not reach"*, and eleven of
the fourteen delivered rows follow it. This row does not. Its grounds read:

> `close` writes `Contract changes` and `New units` from the fix range, so the
> rows cost no question to anybody. Before it did, one record sat at its
> starting values for two rounds and the six units its fix pass created
> reached the next round only because a reviewer went and looked.

Both sentences are true and neither is a limit — the second is the history
that motivated the command. The cell reads fully delivered.

It is not. `skills/code-review/scripts/round_record.py` documents `New units`
as *"every top-level def, class and module-level constant present at the end
of the range and absent at its start … for a file the AST cannot read the `+`
diff lines are read for `def`, `class`, `function`, `fn`, `func`"*. A fix pass
that adds a template section, a skill rule, a checker's new clause or a walk
adds none of those tokens, so that surface never reaches `New units` at all.
That is the same blind spot the neighbouring row — `A fix pass adds the unit
that pins it` — names explicitly for depth: *"a fix pass that adds mechanism,
a rule or a checker or a template section or a walk, leaves a unit at depth 1
and nothing refuses it"*. Row 12 names it; row 14, which is about the same
derivation, does not.

The table's own paragraph says why this matters here rather than anywhere
else: *"A row that reads closed over a tree that is not is worse than no row
at all, because the next work item picks its subject from this table."*

### ⬜ · `eight rows` is eleven

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`
(divergence row 2), `phases/phase-1.md` §*What this phase found*, and
`seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` row O1's
Notes each state that eight rows carry a sentence naming the part their
delivery does not reach.

Reading the fourteen delivered rows, eleven do: Bootstrap, how the work is
routed, What the answer writes, which of these acts runs itself, the run ends
with a verifying round, The cap is a ceiling, A fix pass adds the unit, And
say what ran the round, And commit the record, The check a round runs reads
everything, and closing the cycle. Two do not — `Then say who checked them`
and `And name the fix surface` — and the first of those is defensible, because
`round_record.py` handles the capped run's last record explicitly and the gap
is covered by the verifying-round row's own check.

The discipline holds; the count does not. O1 is a ledger row, which is where a
number outlives the round that wrote it.

### ⬜ · Q3's grounds are narrower than the section that settles it

`CONTRIBUTING.md`, the bullet beginning **Hooks stay local and quiet**, and
`questions.md` Q3 / `overview.md` §*Not verified*.

**The default (a) holds — I opened the section and it does not need a row.**
But the grounds recorded for it are not the ones the section supplies. The
record's reason is that *both existing entries are touches that fire without
anybody asking*. The section's own scoping is narrower and cleaner: the entire
bullet is about hooks, its sentence reads *"Two hooks reach the network"*, and
the third-entry clause beside it sets conditions *for a hook* — an opt-in
condition, a throttle, silence on failure. `--post` is not a hook and fires on
no hook, so the list does not reach it whether or not it is asked for.

Worth correcting because the recorded reason generalises the wrong way: read
as *this list is for unasked touches*, a future hook that only fires when a
person types something would also be argued out of it, and hooks are exactly
what the list is for. The section's disclosure surface — the README's privacy
section, which the bullet names — is likewise scoped to hooks.

The one sentence in that bullet that does bear on finding 1 is *"Anything that
would send repository contents, paths, or prompts is not on the table."* It
binds hooks and not `--post`, so it is not a rule violation; it is the
repository's stated position on what may leave the machine, and finding 1 is
the first arm that leaves it.

## What was confirmed rather than opened

**The ledger re-stamp is additive and the nine rows are intact.** Counted
every `Re-read <date>` marker in `seal/ledger.md` at base and at head: every
prior date is unchanged and `Re-read 2026-09-22` moves from 18 to 27, exactly
the nine rows the phase record names. No earlier note was overwritten — the
`Re-read 2026-09-13 for #350` note on the row that carried one stands at head,
seven occurrences at both ends. Each of the nine rows changed in three ways:
the anchor hash `7837c909` to `73a9f8fc`, the `Checked` date to 2026-09-22,
and one appended `Re-read` note. `phases/phase-3.md` says both *"each carries
a `Re-read 2026-09-22` note and the `Checked` column moved to that date"* and,
of the re-stamp run alone, *"nine lines changed, and the only change in each is
the hash"*. Those read as contradictory out of context; read as the `--reverify`
run's own diff followed by the notes written separately, they are consistent,
and the tree matches. Not a finding.

**The work item's own six ledger rows resolve.** Executed
`evidence_check.py --ledger seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md .`
in the clone: exit 0, 8 anchors ok, 0 drifted, 0 broken.

**The parser has exactly two readers and the widening changed no behaviour.**
`marked_headings` is called only from its own module's `findings`; `headings`
is read only by the new module. `unverified_check.py` has an unrelated
function of the same name in a different module and is not a caller. The old
body filtered on `match.group(2).lstrip().startswith(MARKER)` and appended
`line.rstrip()`; the new filter is `title.startswith(MARKER)` over a `strip()`ed
title, which differs only in trailing whitespace and cannot change a
`startswith`. The neighbour's 22 cases are green.

**The live post on #496 carries no path.** Read the comment: that run used
`--spawns` on a transcript with eight spawns, so the non-empty branch rendered
and the leaking line never fired. Finding 1 is latent, not realised.

**A11 holds.** Nothing in the diff lands under `hooks/` or
`.github/workflows/`. Checked against the 17-file diff.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `--post` writes the transcript's absolute path, under the user's home directory, into a public issue tracker | `skills/verify/scripts/session_cost.py#emit`, `#report_segments`, `#report_spawns` | open | Executed with the `gh` seam stubbed: `--segments --post` posted a body whose fenced reading opens `0 segments found beside <absolute path>`. `main` already keeps `--latest`'s path line out of the body, so the rule exists in the file and is applied in one place of three |
| 2 | 🟡 `--post` posts a comment with no judgment when `--says` names an empty file | `skills/verify/scripts/session_cost.py#emit`, `#comment_body` | open | Executed: an empty `--says` posted a body opening on the fence, exit 0. `spec.md` §Scope says *refuses to post without a reading*, and the refusal is against the flag only |
| 3 | 🟡 `_delivery` resolves the named path against `ROOT` rather than the root `findings` was given, so the floor case under all four red directions is green by leak | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | open | Executed: the path `SELF` names is absent from the planted tree, present in the repository, and `test_a_clean_planted_tree_is_clean` is still clean. A3 therefore demonstrates *absent from the repository*, not *absent from the tree under check* |
| 4 | 🟡 The row `And name the fix surface, in the same record` names no part its delivery does not reach, against the discipline its own section states | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | open | `round_record.py`'s `New units` reads top-level `def`/`class`/constants and, for a file the AST cannot read, `+` lines for five keywords. A template section, a skill rule or a walk matches none, so that surface never reaches the cell. Row 12 names the same blind spot for depth; this row names none |
| ⬜ | `eight rows` carry a limit sentence; eleven do | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` O1, `overview.md`, `phases/phase-1.md` | correction | Counted all fourteen delivered rows. The discipline holds and the aggregate does not; O1 is a ledger row, where a count outlives the round |
| ⬜ | Q3 ships on the right answer for a reason the section does not supply | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `questions.md` Q3 | correction | Opened `CONTRIBUTING.md`: the bullet is **Hooks stay local and quiet** and its list is of hooks, which settles Q3 more cleanly than *touches that fire unasked*. Default (a) stands; the grounds should name the scope |
| 🟢 | Twenty rows is right, and the case pinning the self-reference pins it | `skills/implement/orchestration.md`, `tests/test_every_orchestrator_act_names_its_delivery.py#test_the_table_reads_the_section_that_holds_it` | confirmed | Executed the parser against the tree: 20 acts, 20 rows, no findings. `spec.md`'s two sentences cannot both hold at nineteen, and the self-reference is closed from two directions rather than one |
| 🟢 | The flow-log paragraph says what the row would have said and does not read closed | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | confirmed | Read: it names the act, the file, `session-cost … --post`, and *"**And nothing makes it run.**"* with the grounds beside it |
| 🟢 | The nine re-read ledger rows are additive; no prior note was dropped | `seal/ledger.md` | confirmed | Every prior `Re-read <date>` count is identical at base and head; `Re-read 2026-09-22` moves 18 → 27 |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is — the repair is either a row rule taking a named list of sections elsewhere, or splitting the `Orchestrator:` marker into two meanings | `overview.md` §*Not done*, named for an issue rather than built here | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so a twenty-first act written without the prefix is counted by nobody | `overview.md` §*Not done*, and the section's own *What this does not catch* paragraph | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a) | the repository owner, who owns that list. See the ⬜ correction above for the grounds the section actually supplies |

## Paste-ready fixes

**Finding 1** — `skills/verify/scripts/session_cost.py`. Replace `emit` and
the three calls to it, so the posted body names the transcript by basename
while the printed report is unchanged. The substitution is exact rather than a
pattern, because `emit` is handed the path it must not publish.

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

The three call sites, each gaining the path it rendered:

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

**Finding 1, the case** — `tests/test_session_cost_post.py`. Red first against
the current `emit`, which posts the path.

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

**Finding 2, the case** — `tests/test_session_cost_post.py`. Red first against
the current `main`, which posts.

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

**Finding 3** — `tests/test_every_orchestrator_act_names_its_delivery.py`.
Thread the root through, and give the planted tree the file its own table
names. Shown red by the floor case, which goes red on the first change alone
and green again on the second.

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

And in `_tree`, so the tree carries what `SELF` names:

```python
    named = os.path.join(base, "tests", "test_every_orchestrator_act_names_its_delivery.py")
    os.makedirs(os.path.dirname(named), exist_ok=True)
    with open(named, "w", encoding="utf-8") as handle:
        handle.write("# the check `SELF`'s row names, so the tree carries it\n")
    return str(base)
```

**Finding 4** — `skills/implement/orchestration.md`, the row
`And name the fix surface, in the same record`. Replace the `Grounds` cell:

```
| And name the fix surface, in the same record | `skills/code-review/orchestration.md` | command: `bin/round-record` | `close` writes `Contract changes` and `New units` from the fix range, so the rows cost no question to anybody. Before it did, one record sat at its starting values for two rounds and the six units its fix pass created reached the next round only because a reviewer went and looked. What the derivation does not reach is a surface with no unit in it: `New units` reads top-level defs, classes and module constants, and for a file the AST cannot read the `+` lines for five keywords, so a fix pass that adds a template section, a skill rule or a walk names an empty surface and nothing refuses it |
```

Needs a fix: yes — findings 1, 2, 3 and 4.

Loses a record or crashes: no

## Proof block

📋 code-review applied

· read: `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
  `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`,
  `changelog.md`, `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md`
  of this work item · the full diff `6d410023...238dbeaf`, 17 files ·
  `skills/implement/orchestration.md` §*Orchestrator: which of these acts runs
  itself* and all twenty rows · `skills/code-review/orchestration.md` headings ·
  `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* ·
  `skills/verify/scripts/session_cost.py` (`emit`, `post`, `open_log`,
  `run_gh`, `comment_body`, `read_says`, `main`, `report_segments`,
  `report_spawns`) · `tests/test_every_orchestrator_act_names_its_delivery.py` ·
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` ·
  `tests/test_session_cost_post.py` · `skills/code-review/scripts/round_record.py`
  (the cell derivations) · `skills/code-review/scripts/chain_check.py` ·
  `bin/session-cost` · `CONTRIBUTING.md` §*Hooks stay local and quiet* ·
  `CLAUDE.md` · `seal/ledger.md` at base and at head
· executed: the nine rows of §*Executed probes* above, in a
  `git clone --no-local` at the target SHA with its own `uv` virtual
  environment. Clone and probe deleted; the worktree is clean
· unverified: the full suite, the repository-wide lint and the typecheck —
  the sealer's, once, after the rounds settle
