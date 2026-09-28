# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — review round 2

| Field | Value |
|---|---|
| Target SHA | 1bddf2edfc444c634e4b84bd91ce3b94b632afa8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #650 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790562543 (#400), the verifying round. Its target is the diff of round 1's fixes, a3b76a2f..1d551500 (23e75f53 fixes, cases and ledger; 1d551500 survivors.md), with the branch at 1bddf2ed and draft PR #650. The job is the answers, not new findings: for each verdict round-1.md records as closed (🟡 1–4 and ⬜ 5–7 fixed, ⬜ 8 answered as a record correction), is it actually closed. The finding surface is round 1's `New units` (three new cases at depth 1), the four existing cases that gained assertions, the rewritten `drawings` loop in hooks/sealer-stamp.py, and the two survivors.md exemptions, which nobody has reviewed. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

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

## Paste-ready fixes

```markdown
predates the hook. So every `SEALED` line that names a values file names
`seal-stamp --from <path>` too, and a stamp that did not appear is drawn by
hand from it, once.
```
```markdown
never seen. Pass the `SEALED` line on as it came, whole. Wherever it names a
values file it names `seal-stamp --from <path>` too, because the hook draws
```
```markdown
it stands: that command is the person's to type, and never yours. Every line
that names a values file names it, because the hook draws nothing and says
nothing
```
```python
report, which names the file and `seal-stamp --from` wherever a values file
was written, is
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2413`, `hooks/sealer-stamp.py:40`, `docs/the-broad-gate.md:124` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/sealer-stamp.py:92` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:683` | round 1's 🟡 3 — fixed |
| round-1 | `README.md:107`, `README.md:181`, `README.md:390`, `README.ko.md:102`, `README.ko.md:383` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2409` | round 1's ⬜ 5 — fixed |
| round-1 | `agents/sealer.md:86`, `docs/the-broad-gate.md:88` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/code-review/orchestration.md:539` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md:48` | round 1's ⬜ 8 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:2383` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2341` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py#claim` | round 1's 🟢 — confirmed |
| round-1 | `hooks/sealer-stamp.py#main` | round 1's 🟢 — confirmed |
| round-1 | the harness | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
