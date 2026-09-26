# 1790381329-the-deferred-sentences-and-pins — review round 1

| Field | Value |
|---|---|
| Target SHA | 79b6626f7a5100c16e1030dce88e57b3f3462368 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 623 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e195cf09b8ad35330e14ca0e2e427097591ec40b..fd22baee76fdec4db6295b37b2668fe90601d1b4`, 2 commits |
| Contract changes | none |
| New units | test_the_baseline_help_names_both_places (depth 1) |
| Needs a fix | yes — 🟡 1 (the `config.py` purpose sentence and its pin), 🟡 2 (the `--baseline` help pin) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790381329 reviews the build at 79b6626f against spec.md and plan.md (frame 0a88663a, approved 09034979). It covers the six deferred issues: #610's exit 2 for a missing sibling, #611's settle headings, #612's unverified-check footing, #613's `at a ready pull request` qualifier, #615's silent set, and #616's `%CD%` precedence. Each is a sentence or a pin. The classes are every twin of each sentence in the tree, found by meaning in English and Korean, and whether each pin goes red when its claim goes false.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal`'s missing-sibling sentence says `hooks/config.py` reads and writes `config.md`; it only reads, and the sentence is unpinned | `skills/implement/scripts/seal.py:104` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; `hooks/config.py`'s docstring names `seal.py` as the writer; `fold_check.py:501` says *reads*; M2 green |
| 🟡 2 | the `--baseline` help the documents case was extended for is not held by it: the tip phrase stands three times in the file | `tests/test_unverified_rows_close.py:1238` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; M7: help reverted alone, case green; the proposed help case red under M7 |
| ⬜ 3 | three test sentences state the `Pass`-beside-`nobody` refusal with no timing; one fixture exits 0 | `tests/test_the_fixes_close_the_record.py:709` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; executed: `assert _code == 0` passes in that case; the other two at `tests/test_the_fixes_close_the_record.py:469` and `tests/test_the_rules_have_one_owner.py:346`, read |
| ⬜ 4 | the variable case's docstring still says the part is *expanded the same way* | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:217` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; read; the phrase phase 6 removed from `handed_to_shell` |
| ⬜ 5 | the copied-alone module says six shipped scripts load a sibling; nine do | `tests/test_a_script_copied_alone_exits_2.py:4` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; read; `survivor_check.py`, `broad_gate.py`, `evidence_check.py` load siblings too |
| ⬜ 6 | `seal.py`'s exit-code line gives 2 one meaning; `parser.error` at `:2466` is also 2 | `skills/implement/scripts/seal.py:77` | **fixed** `4379b60aaa05bc5cb58eb4836355e36c248eadb9` | fixed at 4379b60aaa05bc5cb58eb4836355e36c248eadb9; read |
| ⬜ 7 | A2's re-read note describes `handed_to_shell`, which A2 does not cite, and runs two sentences together | `seal/releases/0.15.3.md:60` | answered | corrected at 4379b60aaa05bc5cb58eb4836355e36c248eadb9: A2's note now concerns what A2 cites (`templates/config.md` §*Broad gate* and the template case's needle); the `handed_to_shell` note already stands on A1, which cites it; read; correction, not counted in `Needs a fix` |
| 🟢 | #610: both scripts exit 2 with a sentence for a missing sibling and do not swallow a real `ImportError` in a present one | `skills/implement/scripts/seal.py:112`, `skills/verify/scripts/payload_meter.py:145` | confirmed | P1–P4, M1, M4; class re-enumerated by construction under `skills/` |
| 🟢 | #611: both headings named, summary line pinned | `skills/settle/SKILL.md:118` | confirmed | M5, M6 red |
| 🟢 | #612: every sentence placing the comparison names both places; the frame's non-twins are true | `docs/one-root-by-lifetime.md:197` | confirmed | tree-wide search in both languages; M8, M9 red |
| 🟢 | #615: three silent-set statements match `removed_ledger_rows`; count guard pinned | `skills/code-review/scripts/survivor_check.py:1081` | confirmed | read against the code; M12 red; 289 of 835 recounted |
| 🟢 | #616: defined-`CD` precedence and the substring bound pinned on `%CD%` itself | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:250` | confirmed | M10, M11 red |
| 🟢 | ledger: corrected rows true, re-read rows hold, no drift | `seal/releases/0.13.0.md:8` | confirmed | `evidence-check` 2406 ok / 0 drifted / 0 broken |
| ❓ | where `cmd.exe` resumes scanning after an undefined `%NAME%` | `skills/verify/scripts/broad_gate.py:1284` | ❓ out of verified scope | macOS only; `overview.md` names a Windows run of `cmd.exe`, by whoever next changes the broad gate's `cmd.exe` path |

## Paste-ready fixes

```python
HOOK_PURPOSES = {
    "config.py": "it is what reads the root's config.md, whose Mode row this "
    "command keeps",
    "optin.py": "it is what finds the repository's seal/ root",
}
```
```python
    (
        "skills/implement/scripts/seal.py",
        ["mode", "--check"],
        "it is what reads the root's config.md",
        "reads and writes",
    ),
```
```python
def test_the_baseline_help_names_both_places(capsys):
    """#612: the `--baseline` help is a rendered line (contract §14). The
    documents case above reads the whole file, where the module docstring and
    `merge_base`'s docstring carry the same phrase, so it cannot see the help
    go back to the fork point. The help is rendered and read on its own. Red
    with the tip dropped from the help alone."""
    with pytest.raises(SystemExit):
        uc.main(["--help"])
    rendered = " ".join(capsys.readouterr().out.split())
    assert (
        "the fork point on a branch checkout and the base's tip in CI" in rendered
    ), rendered
```
```text
tests/test_the_fixes_close_the_record.py:709-710
    # Not `code == 0`: a `fixed` verdict leaves `Pass` beside `nobody` on
    # the last record, which the check refuses at a ready pull request; this
    # run is judged as a draft, where it prints.

tests/test_the_fixes_close_the_record.py:471-472
    check refuses `Pass` beside it on the last record at a ready pull request
    (phase 3 measured exit 1 here, before #598). `close` derives ...

tests/test_the_rules_have_one_owner.py:347-348
    `Pass`, and the check refuses that pair on the last record at a ready
    pull request — a reader
```
```text
tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216-218
    """#596, round 1's 🟡 3 and round 2's 🟡 1. `cmd.exe` expands `%VAR%`
    before it reads a command name, so the part is expanded before it is
    asked whether it is a directory, as far as `as_cmd_expands` models it: a
    name from the
```
```text
tests/test_a_script_copied_alone_exits_2.py:4
Six of the shipped scripts that load a sibling are held here, in one of two
shapes. (`survivor_check.py` and `broad_gate.py` raise their own refusal, and
`evidence_check.py` falls back by design.) Five import it by file path: ...
```
```text
skills/implement/scripts/seal.py:77-79
Exit codes: 0 done · 1 nothing was written, and the message says why · 2 a
file this command loads from `hooks/` is not there, so nothing was read, or
the arguments were unusable (argparse's usage error, and a mode given with
`--check` or `--apply`). Every refusal here names the file, the path, or the
flag that gets past it.
```
```text
seal/releases/0.15.3.md:60, A2 — replace this work item's note with:
**Re-read 2026-09-26 in work item 1790381329 (#616):** `templates/config.md`
§*Broad gate* moved only in its `%VAR%` sentence, and the template case's
needles were re-cut with it; the positions it states and the examples it
names are unchanged, and the claim holds
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the five touched modules (copied-alone, settle, gate, unverified, survivor), at `79b6626f` | exit 0: 551 passed, 1 skipped |
| `evidence_check.py .` at `79b6626f` | exit 0: 2406 ok · 0 drifted · 0 broken |
| `survivor_check.py --range 47e32d57...79b6626f` | exit 1: the two places `survivors.md` records; with `--exempt` naming it, exit 0, both `exempt` |
| `correction_check.py --range 47e32d57...79b6626f` | exit 0: no merge commit in the range |
| M1: `refuse_without_hooks()` call removed | copied-alone `seal.py` row red |
| M2: `config.py` purpose reworded | green — the sentence is unpinned (🟡 1) |
| M3: `seal`'s closing sentence reworded | green — unpinned, as the other loaders' closing sentences are |
| M4: `payload_meter.py` file check removed | copied-alone `payload_meter.py` row red |
| M5: second heading deleted from `skills/settle/SKILL.md` | documents case red |
| M6: summary line reworded in `settle.py` | report case red |
| M7: tip phrase dropped from the `--baseline` help only | documents case green, 9 passed (🟡 2) |
| M8: tip phrase dropped from `README.md` | red |
| M9: tip phrase dropped from `templates/hygiene.yml` | red |
| M10: environment branch moved after the computed `CD` | variable case red |
| M11: variable name cut at `:` before the lookup | variable case red |
| M12: count guard `>=` read as `==` | split-row case red |
| P1: `seal.py` beside a `hooks/` whose `config.py` imports a missing module | exit 1, traceback naming the inner module, no *cannot read* |
| P2: `seal.py` beside a `hooks/` holding `optin.py` only | exit 2, one sentence for `config.py`, no traceback |
| P3: `payload_meter.py --calibrate` beside a `session_cost.py` that raises | exit 1, traceback naming the inner error, no *cannot read* |
| P4: `seal.py --help` with `config.py` missing | exit 2 |
| `assert _code == 0` added to `test_a_fix_commit_carries_no_empty_code_span` | passed — the check exits 0 there (⬜ 3) |
| the 🟡 1 fence applied: the new row alone, then with the rewording | red at `79b6626f`; green after, 8 passed |
| the 🟡 2 fence applied: at `79b6626f`, then under M7 | green; red |
| no-id count through `survivor_check`'s loaders at `79b6626f` | 289 of 835 anchored live rows (34.6%) |
| the broad gate — full suite, repository-wide lint, typecheck | not yet — the sealer's, after the rounds settle; nothing here ran it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
