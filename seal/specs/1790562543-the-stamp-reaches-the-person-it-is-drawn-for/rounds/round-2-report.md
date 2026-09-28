# Round 2 report — 1790562543, the stamp reaches the person it is drawn for

Round 2, the verifying round. Its target is the diff of round 1's fixes,
a3b76a2f..1d551500 (23e75f53 fixes, cases and ledger; 1d551500
survivors.md), with the branch at 1bddf2ed and draft PR #650. The job is the
answers: for each verdict round-1.md records as closed (the four should-fix
findings 1–4 and the notes 5–7 fixed, note 8 answered as a record
correction), is it actually closed. The finding surface is round 1's
`New units` (three new cases at depth 1), the four existing cases that gained
assertions, the rewritten `drawings` loop in `hooks/sealer-stamp.py`, and the
two survivors.md exemptions.

I stayed inside that diff. round-1.md and round-1-report.md were read for
coordinates, and round 1's confirmed verdicts are carried rather than
re-derived, except where the fix diff touched the code under one of them
(the claim-before-print verdict, re-checked by probe G below).

## How the answers relate

```
round 1 findings 1-8                  every one closed (executed or read)
  └─ the fix wrote "every sealed line names seal-stamp --from"
       └─ two sealed line forms name no command               ⬜ 1
the fix's cases, all eight red at the pre-fix sources (executed)
  ├─ the README side-effects limb cannot fail on its own       ⬜ 2
  └─ the common line's quoting is pinned on no spaced path     ⬜ 3
survivors.md, two exemptions                      both grounds hold
```

Nothing here needs a fix. The three notes are wording and two assertions that
can be narrowed.

## The implementer's account against the code

The orchestrator relayed six facts, and I checked each one I could reach.

- *All eight cases red at a3b76a2f.* Executed: I checked out the eight
  source and document files at a3b76a2f in a clone, kept the new cases, and
  ran them. The result was 8 failed, exit 1. The claim holds.
- *15 single mutants killed.* Not re-run as a set. One mutant I wrote
  myself survived (probe H, ⬜ 2), and the ledger's N9 note says every added
  pin is red "under a mutant of its own sentence". That note is true of the
  pins the note names by sentence, and false of the side-effects limb.
- *The ⬜ 5 case moved its fixture under a directory with a space.* Read at
  `tests/test_the_seal_is_taken_once_by_the_sealer.py:2368`. It holds for
  the no-session line only; see ⬜ 3.
- *survivor-check reported two places, both recorded with quotes.*
  Executed: `survivor_check.py --range a3b76a2f..23e75f53` exits 1 and names
  the two places, and with `--exempt` on this work item's survivors.md it
  exits 0 with both excused. Their grounds are judged below.
- *`evidence_check.py --strict .` exit 0.* Executed in the clone, exit 0.
- *ruff exit 0 on the five changed .py files.* Relayed and not re-run by me.

## Round 1's findings, one by one

**Finding 1 (the recovery on the common line) is closed.**
`DRAWN_AT_TURN_END` (`skills/verify/scripts/broad_gate.py:2418`) now ends
"where none appears, `seal-stamp --from {command}` draws it". The policy
paragraph (`docs/the-broad-gate.md:132`), the orchestrator's rule
(`skills/code-review/orchestration.md:551`) and the sealer's paragraph
(`agents/sealer.md:159`) each name the three silent states. The hook's
docstring (`hooks/sealer-stamp.py:41`) is true as written now. Probe F
built the common line from a real `signal` call and typed its command
through `sh`: exit 0, the stamp drawn, the file renamed.

**Finding 2 (one malformed file loses the others) is closed.**
`drawings` builds the whole block, label included, inside the `try` and
catches `Exception` before it claims. Probe G wrote four files: a malformed
one older than a good one, and two malformed ones newer. The main `Stop`
drew exactly the good one. All three malformed files stayed pending under
their own names, including one whose scale the band refuses. The class
reaches `seal-stamp --from` too, and I looked there: `drawn_from` never
calls `label`, so the second drawer has no build step after its claim.

**Finding 3 (the refusal names `X.drawn.drawn.json`) is closed.**
`drawn_from` (`skills/verify/scripts/seal_stamp.py:688`) names the given
path where it already ends `.drawn.json`. The claim-failure refusal two
lines later still uses `drawn_path(path)`, which is right there: the first
guard has already sent every `.drawn.json` path away.

**Finding 4 (both READMEs omit the hook) is closed.** Both editions carry the
table row, the opt-in list entry, the count ("Eight of the eleven",
"게이트 열하나 중 여덟") and the fourth side effect. I grepped both READMEs,
`docs/` and CONTRIBUTING.md for another gate count and found none. The case
has one weak limb, which is ⬜ 2.

**Note 5 (the unquoted path) is closed on both lines.** `command =
quote(path)` feeds both formats. In probe F the common line's path held a
space. The printed command ran as typed, exit 0, and the same command with
the path unquoted exited 2. The pin is ⬜ 3.

**Note 6 (a gate that "drew") is closed.** `agents/sealer.md:86`,
`docs/the-broad-gate.md:88` and `:113`, the `seal_stamp.py` docstring and
the two `panel` comments now say "measured". Across the tree, "drew the
stamp" survives only in test narration of earlier releases
(`tests/test_the_gate_names_every_step_ci_runs.py:462` and `:690`,
`tests/test_the_gate_asks_the_range_ci_will_ask.py:10`), where the gate did
draw. I judged those historical and left them alone.

**Note 7 (`close --broad-gate` draws nothing) is closed.**
`skills/code-review/orchestration.md:543` says so, and
`test_the_orchestrator_is_told_the_stamp_is_drawn_for_it` pins it.

**Note 8, the paperwork correction, is closed.** spec.md §Scope In 2,
questions.md's settled list, plan.md's Phase 1 and Alternatives rows and
overview.md's *Fed back* section each carry a dated correction pointing at
the divergence row.

**The survivors.md exemptions hold.** Both quoted places are about the
no-session line. That line still says no session was found, still names the
command, and is still the only line saying no hook will draw. The sealer's
paragraph now says "Pass the `SEALED` line on as it came, whole" before it,
so the exempted sentence adds emphasis and contradicts nothing.

## Findings in the fix surface

### ⬜ 1 — "Every sealed line names `seal-stamp --from`" is false for two sealed line forms

*From reading.* The fix states the recovery with the scope *every sealed
line* in five places: `docs/the-broad-gate.md:136`, `agents/sealer.md:160`,
`skills/code-review/orchestration.md:553`, `hooks/sealer-stamp.py:42` and
the comment at `skills/verify/scripts/broad_gate.py:2417`. The work item's
changelog fragment (line 12) and overview.md (line 37) say the same.

`signal` has four endings, and two of them are sealed lines that name no
command:

- `NOTHING_RECORDED`, a green run without `--record`. The orchestrator's
  paragraph itself says two sentences earlier that the `close --broad-gate`
  path runs the gate this way, so that paragraph contradicts itself.
- `VALUES_UNWRITTEN`, where the values file could not be written.

Why it is ⬜: neither line leaves a stamp to recover, and each says so in
its own words, so nobody acts wrongly on the sentence. The behaviour is
right, and a scope word overreaches. The accurate scope is the line that
names a values file, and the paste-ready text below uses it. The pin at
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:455` quotes the
policy sentence and moves with it.

### ⬜ 2 — The README side-effects assertion passes with the side effect deleted

*Executed, probe H.* In `test_both_readmes_list_the_stamp_hook`
(`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:488`), the
side-effects limb asserts the count word ("Four side effects") and
`"specseal-stamp/" in text`. The gate-table row the same case requires also
contains `specseal-stamp/`, so the second half is met by the table. I
deleted the new side-effects clause from `README.md` and kept "Four side
effects". The case passed (1 passed, exit 0).

Why it is ⬜: the README is right today. What stands is a limb that cannot
fail for the sentence it exists for, and a ledger note (N9, "every pin it
added red again under a mutant of its own sentence") that overstates by
that limb. Narrowing the limb to the clause's own words makes the note
true. The fix pass did the same narrowing for the opt-in limb.

### ⬜ 3 — The quoting of the common line is pinned on a path with nothing to quote

*From reading, with probe F executed for the behaviour.* The new assertion
in `test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`
(`tests/test_the_seal_is_taken_once_by_the_sealer.py:2311`) compares with
`quote(path)`. The fixture's path under pytest's `tmp_path` holds only
characters `shlex.quote` leaves bare, so `quote(path) == path`. A mutant
that formats `DRAWN_AT_TURN_END` with `command=path` would pass this case
and every other one. Only the no-session case moves its fixture under a
space.

Why it is ⬜: both lines share one `command` variable today and probe F
shows the common line quoted. The gap is the next edit that splits them.
The paste-ready block moves the S1 fixture under a space the way the S14
case does.

## Regression tests to plant

Each is to be seen red before it is kept (contract §15): the first with the
clause deleted from the README (probe H's mutant), the second with
`command=path` passed to `DRAWN_AT_TURN_END`.

```
tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py
  in test_both_readmes_list_the_stamp_hook                     (⬜ 2)
    each edition's side-effects clause, in its own words
tests/test_the_seal_is_taken_once_by_the_sealer.py
  in test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing (⬜ 3)
    the fixture under a directory holding a space; the path quoted
```

## Facts for the evidence ledger

- `hooks/sealer-stamp.py#drawings`: with a malformed file older than a good
  one and two newer (an `item` that is a list, a scale out of band), one
  main `Stop` draws the good file alone and leaves all three pending.
  Executed, probe G, at 1bddf2ed.
- `skills/verify/scripts/broad_gate.py#signal`: the common line's command,
  for a path holding a space, runs as printed through `sh` (exit 0), and
  the same command unquoted exits 2. Executed, probe F, at 1bddf2ed.
- N9's note in this work item's ledger fragment overstates by the README
  side-effects limb until ⬜ 2 is fixed. Executed, probe H.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | "Every sealed line names `seal-stamp --from`" is false for the `NOTHING_RECORDED` and `VALUES_UNWRITTEN` lines, and the orchestrator's paragraph contradicts its own `close --broad-gate` sentence | `docs/the-broad-gate.md:136`, `agents/sealer.md:160`, `skills/code-review/orchestration.md:553`, `hooks/sealer-stamp.py:42` | open | read: `signal`'s four endings, their constants from `skills/verify/scripts/broad_gate.py:2405`; no stamp is lost, the scope word overreaches |
| ⬜ 2 | The README side-effects limb passes with the side-effects clause deleted, because the table row also carries `specseal-stamp/` | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:488` | open | probe H executed: clause deleted, count kept, case 1 passed exit 0 |
| ⬜ 3 | The common line's quoting is asserted on a path with nothing to quote, so `command=path` on that branch survives | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2311` | open | read; probe F executed shows the behaviour right today |
| 🟢 | round 1's finding 1 is closed — every line that writes a values file names `seal-stamp --from`, and the three silent states are stated where a person looks | `skills/verify/scripts/broad_gate.py:2418` | confirmed | probe F executed; the case red at the pre-fix sources, executed; policy, orchestration and sealer paragraphs read |
| 🟢 | round 1's finding 2 is closed — one malformed file no longer takes the others | `hooks/sealer-stamp.py#drawings` | confirmed | probe G executed: good drawn, three malformed pending; the case red at the pre-fix sources, executed; `drawn_from` read, it builds nothing after its claim |
| 🟢 | round 1's finding 3 is closed — the drawn refusal names a file that exists | `skills/verify/scripts/seal_stamp.py:688` | confirmed | the case red at the pre-fix sources and green at 1bddf2ed, executed; the claim-failure branch read |
| 🟢 | round 1's finding 4 is closed — both READMEs list the hook in all four places | `README.md:192`, `README.ko.md:188` | confirmed | read; the case red at the pre-fix sources, executed; its side-effects limb is ⬜ 2 |
| 🟢 | round 1's note 5 is closed — both line forms quote the path | `skills/verify/scripts/broad_gate.py:2469` | confirmed | probe F executed: typed as printed exit 0, unquoted exit 2 |
| 🟢 | round 1's note 6 is closed — no current sentence says a gate drew the stamp in a sealer | `agents/sealer.md:86`, `docs/the-broad-gate.md:88` | confirmed | read and grepped; three remaining uses narrate earlier releases |
| 🟢 | round 1's note 7 is closed — the `close --broad-gate` path is named as sealed with no stamp | `skills/code-review/orchestration.md:543` | confirmed | read; pinned and red at the pre-fix sources, executed |
| 🟢 | round 1's note 8 is closed — spec, questions, plan and overview carry the dated terminal correction | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md:48` | confirmed | read in the fix diff |
| 🟢 | the two survivors.md exemptions hold — both quoted places are about the no-session line, which still says both things | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/survivors.md:12` | confirmed | `survivor_check.py` executed: exit 1 bare, exit 0 with `--exempt`; grounds read against both files |
| carried | round 1's confirmed verdicts (the divergence, no draw over an unsealed run, no double draw, the hook's scoping) | `hooks/sealer-stamp.py#main` | confirmed | carried from round 1; the one the fix diff touched, claim before print, re-checked by probe G |
| ❓ | S17: the stamp on the owner's screen after the orchestrator's text, unfolded, in colour, once; several stamps in one message rendering whole | the harness | ❓ out of verified scope | carried from round 1; no case can observe a screen; the owner answers on the first real run after merge |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -q -p no:xdist`, in a `git clone --no-local` at 1bddf2ed | 22 passed, exit 0 |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q -k` on the recorded-pipe, no-session, unwritten-values and quote cases | 6 passed, exit 0 |
| The eight fixed cases against the eight source and document files checked out at a3b76a2f | 8 failed, exit 1: each case red before the fix |
| `survivor_check.py --range a3b76a2f..23e75f53`, bare and with `--exempt` on this work item's survivors.md | bare exit 1, two places; exempt exit 0, both excused |
| `evidence_check.py --strict .` at 1bddf2ed | exit 0 |
| Probe F: `signal` for a session under a checkout path holding a space; its command typed through `sh`, and the same command unquoted | typed as printed exit 0, stamp drawn, file renamed; unquoted exit 2 |
| Probe G: four values files (malformed `item` int older, good, `item` a list, scale out of band), then `dispatch.py stop` | exit 0, stderr empty, one label (the good file's); good drawn, three malformed pending |
| Probe H: README.md's side-effects clause deleted with "Four side effects" kept, then `test_both_readmes_list_the_stamp_hook` | 1 passed, exit 0; the limb cannot fail on its own |
| ruff on the five changed .py files | not run in this round; relayed as exit 0 by the orchestrator |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, once, after the rounds settle |

## Paste-ready fixes

### ⬜ 1

`docs/the-broad-gate.md`, the last sentence of the new paragraph (the
policy case at `:455` takes the same words):

```markdown
predates the hook. So every `SEALED` line that names a values file names
`seal-stamp --from <path>` too, and a stamp that did not appear is drawn by
hand from it, once.
```

`agents/sealer.md`:

```markdown
never seen. Pass the `SEALED` line on as it came, whole. Wherever it names a
values file it names `seal-stamp --from <path>` too, because the hook draws
```

`skills/code-review/orchestration.md`:

```markdown
it stands: that command is the person's to type, and never yours. Every line
that names a values file names it, because the hook draws nothing and says
nothing
```

`hooks/sealer-stamp.py`, the docstring, and the comment above
`DRAWN_AT_TURN_END` in the same words:

```python
report, which names the file and `seal-stamp --from` wherever a values file
was written, is
```

### ⬜ 2

`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, in
`test_both_readmes_list_the_stamp_hook`:

```python
    for edition, count, opt_in, effects, clause in (
        (
            "README.md",
            "Eight of the eleven gates",
            # The opt-in list's own words: the count sentence names the stamp
            # hook too, so the bare name would pass with the list unchanged.
            "the two implementer hooks, the stamp hook and the version check.",
            "Four side effects",
            # The clause's own words: the gate-table row carries
            # `specseal-stamp/` too, so the bare directory would pass with the
            # side effect deleted.
            "`<git-common-dir>/specseal-stamp/`, which the stamp hook renames "
            "once drawn and nothing prunes",
        ),
        (
            "README.ko.md",
            "게이트 열하나 중 여덟",
            "구현자 훅 둘, 도장 훅, 버전 확인이다.",
            "네 가지 부수 효과",
            "도장 훅은 그린 뒤 그 파일의 이름을 바꿀 뿐 지우지 않습니다",
        ),
    ):
        text = flat(edition)
        table = [ln for ln in text.split("| ") if ln.startswith("sealer-stamp ")]
        assert table, f"{edition}'s gate table has no `sealer-stamp` row"
        assert count in text, (edition, count)
        assert opt_in in text, (edition, opt_in)
        assert effects in text and clause in text, (edition, effects, clause)
        assert "Seven of the ten" not in text and "게이트 열 중 일곱" not in text
```

### ⬜ 3

`tests/test_the_seal_is_taken_once_by_the_sealer.py`, the head of
`test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`, and one more
assertion after the quoted one:

```python
    spaced = tmp_path / "a checkout" / "repo"
    shutil.move(str(repo), str(spaced))
    repo = spaced
    out, _values = sealed_values(repo, tmp_path, session="s-1")
```

```python
    assert f"`seal-stamp --from {gate_module().quote(path)}`" in said[0], said
    assert " " in path and f"--from {path}`" not in said[0], said
```

Needs a fix: no

Loses a record or crashes: no

Every one of round 1's findings is closed, and this round opened three ⬜
notes and nothing that needs a fix. The broad gate has come due: the next
act is the sealer's spawn. If the orchestrator takes the three notes first,
that edit lands before the sealer, not after it.

## Proof block

Opened: `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/`
(rounds/round-1.md, rounds/round-1-report.md, and the fix diff of spec.md,
plan.md, questions.md, overview.md, changelog.md, survivors.md);
`seal/ledger/1790562543-the-stamp-reaches-the-person-it-is-drawn-for.md`
(the fix diff and rows N7–N9); the fix diff of the seven
`seal/releases/*.md` files; `hooks/sealer-stamp.py` (the fix diff);
`skills/verify/scripts/broad_gate.py` (`quote`, lines 2395–2475);
`skills/verify/scripts/seal_stamp.py` (`write_values`, `read_values`,
`label`, `drawn_from`); `agents/sealer.md` (150–170 and the fix diff);
`docs/the-broad-gate.md` (104–142); `skills/code-review/orchestration.md`
(the fix diff); `README.md` (216–230 and the fix diff); `README.ko.md` (the
fix diff); `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`
(1–80, 195–245, 495–510 and the fix diff);
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (2280–2320 and the fix
diff); `bin/test`; `bin/survivor-check`.
Executed: the runs and probes F–H in the table above, in a scratch clone at
1bddf2ed, and the probe script was a single test_tmp file run once. The
clone, the probe script, its fixtures and every capture are deleted.
Read, not executed: everything else. Unverified: ruff (relayed by the
orchestrator), the broad gate (the sealer), S17 (the owner).
