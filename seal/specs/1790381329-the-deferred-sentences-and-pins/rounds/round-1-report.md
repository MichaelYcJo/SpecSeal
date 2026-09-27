# 1790381329-the-deferred-sentences-and-pins — review round 1 report

First round. Target SHA `79b6626f`, reviewed against `origin/release/v0.15.5`
(`47e32d57`), range `47e32d57..79b6626f`. Read in a `git clone --no-local` at
`79b6626f` under the session scratchpad
(`<scratchpad>/1790381329-the-deferred-sentences-and-pins/round-1/clone`).
Nothing was written in the worktree except this file. No earlier
`round-N.md` exists, so the implementer's account (`spec.md`, `overview.md`,
the phase records, `survivors.md`, the ledger notes C1–C5 and the re-read
notes) was the only other voice, and every claim of it used below was checked
against the code.

Ran by: specseal:warden on claude-opus-5-5.

## Summary

The six items meet the spec on the axes it names, and each named example is
pinned: `%CD%` itself with a defined `CD`, both settle headings and the summary
line, the `>=` count guard, and both copied-alone rows. Every one of those
pins went red under a mutation of the claim it holds (probes M1, M4–M6,
M8–M12). The #610 loaders do not swallow a real `ImportError` inside a sibling
that is present. The silent-set statements now match `removed_ledger_rows`.

Two things need a fix.

- **🟡 1. The new `seal` refusal says `hooks/config.py` reads *and writes*
  `config.md`.** It only reads. The writer is `seal.py` itself, which is what
  `hooks/config.py`'s own docstring says. It is #590's second-half defect,
  a loader giving a file a purpose it does not have, and nothing pins that
  sentence.
- **🟡 2. The `--baseline` help is not pinned, although the case says it is.**
  The documents case reads `unverified_check.py` as one text, and the tip
  phrase stands there three times. Reverting the help alone to the fork point
  leaves the case green.

The rest are ⬜. Three test sentences are #613 twins, and one is a #616 twin.
One test docstring carries a false count. `seal.py`'s exit-code line misses
its own `parser.error`. One 0.15.3 re-read note sits on the wrong row.

## Spec compliance

- **#610 (read and executed).** `seal.py#refuse_without_hooks` checks both
  `HOOK_PURPOSES` files before the `import` lines. A missing file gives exit 2,
  one sentence per file and no traceback (P2, and the class case).
  `payload_meter.py#_session_cost` checks `session_cost.py` before
  `spec_from_file_location` and exits 2 the same way. A sibling that is
  present but raises is not swallowed: both scripts print the inner
  `ImportError` traceback at exit 1 and never the *cannot read* sentence (P1,
  P3). The class under `skills/` was re-enumerated by construction:
  `spec_from_file_location`, `sys.path`, `runpy`, and both top-level and
  indented bare sibling imports, plus two calls that nothing under `skills/`
  makes: `import_module`, `__import__` (NAME NOT IN TREE: searched for). It is
  the two scripts, as the frame said; the other loaders already raise their
  own refusal or fall back by design. The purpose sentence given to
  `config.py` is false (🟡 1). The docstring's list of exit codes is
  incomplete (⬜ 6), and the test module's count is false (⬜ 5).
- **#611 (read and executed).** The skill names both headings. The documents
  case goes red with the second heading deleted (M5), and the summary-line
  assertion goes red with the old wording restored in `settle.py#main` (M6).
  No other document names either heading: I searched both wordings and the
  summary line across `docs/`, `skills/`, `agents/`, `templates/`, `hooks/`,
  both READMEs and `CONTRIBUTING.md`.
- **#612 (read and executed).** I re-searched by meaning in English and Korean.
  The phrasings were *fork point*, *forked from*, *after the fork*, *moving
  tip*, *갈라진 지점*, *병합 기준*, *fewer rows*, *branch was cut*, *행이 줄*,
  and every `merge-base` / `--baseline` near CI. Every sentence that places
  `unverified-check`'s comparison now names both places, or places nothing.
  The places the frame judged true were re-read and I agree:
  `docs/the-evidence-ledger.md`, `docs/commit-review-gate-spec.md` §the rule
  arm, `unverified_check.py#base_label` and `#retired_by_rule`,
  `docs/release-checklist.md` step 0, and the milestone comment in
  `hygiene.yml`. The ledger's `fork` sentences near `unverified_check`
  anchors are fixture descriptions or already corrected (0.13.0 S1). Both
  workflows trigger on `pull_request` alone and check out with no `ref:`, so
  *the base's tip in CI* holds. The case holds each document except the
  script's help line (🟡 2).
- **#613 (read and executed).** `fix_surface` and `landing_values` now say
  *at a ready pull request*. Three test sentences still state the refusal
  with no timing, one of them in a fixture where the check exits 0 (⬜ 3).
  The two non-twins the frame named (`docs/round-record-spec.md` §the
  `nobody` paragraph, `docs/review-handoff-protocol.md` §what it refuses) are
  norm statements, and I agree with that judgment.
- **#615 (read and executed).** The three statements now say what
  `removed_ledger_rows` does. A removed row is silent only when its id does
  not name it (`named[path][key] >= held[key]` fails), at least one anchor
  left, and no standing row is a superset of the anchors that still resolve.
  The four *at least as many* sentences match `>=`. The new case goes red
  under `==` (M12). The no-id figure re-counted at the target SHA through
  `survivor_check`'s own loaders is 289 of 835 (34.6%). That agrees with the
  289 of 833 recorded at `a31ad5bf`: C4 and C5 carry ids.
- **#616 (read and executed).** The defined-`CD` assertion goes red with the
  environment branch moved after the computed one (M10). The substring row
  goes red with the name cut at `:` before the lookup (M11). `templates/config.md`
  §*Broad gate*, `as_cmd_expands` and `handed_to_shell` no longer claim
  equality with `cmd.exe` beyond the plain form. The test docstring of the
  same case still says *expanded the same way* (⬜ 4). The frame's Q2 (where
  `cmd.exe` resumes after an undefined name) stays unverified with its
  answerer named, and I carry it as ❓.
- **Ledger (read, and executed through `evidence-check`).** 2406 ok, 0
  drifted, 0 broken at the target SHA. The corrected rows (0.13.0 S1, 0.15.4
  S1 ×2) now say what the code does. Every re-read row I opened makes a claim
  that still holds. The re-read notes on the seven `fix_surface` rows, the
  four `landing_values` rows, and the `merge_base` / `main` / `folded_items` /
  hygiene / config rows each name the edit that drifted them. One note sits
  on a row that does not cite the unit it describes (⬜ 7). C1's
  purpose-sentence clause will need a correction once 🟡 1 is fixed. C2–C5
  say what the code does.
- **Survivors (executed).** `survivor-check --range 47e32d57...79b6626f`
  reports the same two places `survivors.md` records, and exits 0 with
  `--exempt` naming that file. I read both grounds and agree with them.

## Findings from reading

### 🟡 1 — `seal`'s refusal gives `hooks/config.py` a purpose it does not have

`skills/implement/scripts/seal.py:104-106`, `HOOK_PURPOSES["config.py"]`:
*it is what reads and writes the root's config.md, the Mode row this command
keeps*. `hooks/config.py` only reads. Its docstring says *the READER moved
here and the writer stayed there*, meaning `seal.py`, and
`skills/settle/scripts/fold_check.py:501` gives the same file *it is what
reads the rows of seal/config.md*. This is the sentence a person reads when
their copy is broken, and it is the shape #590 fixed in `settle.py`, where
every file had been given one purpose. The class case pins only the
`optin.py` sentence: rewording the `config.py` one leaves it green (M2).
Contract §14 asks for the pin in the same commit. The fix below rewords the
sentence and adds a second `seal.py` row whose `absent` column refuses the
false half. It was red at the target SHA and green with the rewording, in the
clone. C1's claim (`HOOK_PURPOSES`) drifts with it and is re-read in the same
pass.

### 🟡 2 — the `--baseline` help is held by nothing

`tests/test_unverified_rows_close.py:1238-1243` adds `unverified_check.py`
to `test_the_documents_state_the_merge_base_footing` with the comment *The
`--baseline` help is a rendered line (#612)*. `spec.md` §#612 says the same
thing is the reason for the row. The case reads the whole file, though, and
`the base's tip` stands in it three times: the module docstring, `merge_base`'s
docstring, and the help. Dropping the phrase from the help alone leaves the
case green (M7), so the one rendered line the row was added for can go back
to the fork point unseen. The fix renders `--help` and reads the help alone.
It was green at the target SHA and red with M7, in the clone.

### ⬜ 3 — three test sentences state the `Pass`-beside-`nobody` refusal with no timing

These are #613's class in `tests/`:

- `tests/test_the_fixes_close_the_record.py:709-710` — *Not `code == 0`: a
  `fixed` verdict leaves `Pass` beside `nobody` on the last record, which the
  check refuses*. The fixture is judged as a draft (`round_record.run_check`),
  and the case exits **0**. I added `assert _code == 0` in the clone and it
  passed.
- `tests/test_the_fixes_close_the_record.py:469-472` — *the check refuses
  `Pass` beside it on the last record (phase 3 measured exit 1 here)*.
- `tests/test_the_rules_have_one_owner.py:346-348` — *the check refuses that
  pair on the last record*.

No behaviour is wrong. The frame's search for this class did not cover
`tests/`.

### ⬜ 4 — the variable case's docstring still says *expanded the same way*

`tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216-218`: *so the part is
expanded the same way before it is asked whether it is a directory*. This is
the phrase phase 6 removed from the comment above `command_names_backslashed`
in `handed_to_shell`. The same docstring's *no environment holds* clause was
corrected, and this one was left.

### ⬜ 5 — the copied-alone module says *Six shipped scripts load a sibling*

`tests/test_a_script_copied_alone_exits_2.py:4`. Nine do. `survivor_check.py`
and `broad_gate.py` load siblings and raise their own refusal, and
`evidence_check.py` falls back by design. The number is the count of scripts
this case holds, and the sentence says it is the count that load a sibling.
It is contract §5's aggregate, and the spec asked the old *four* to go for
the same reason.

### ⬜ 6 — `seal.py`'s exit-code line gives 2 one meaning

`skills/implement/scripts/seal.py:77-79`: *2 a file this command loads from
`hooks/` is not there*. `seal.py:2466` calls `parser.error(... cannot be
given together)`, which is exit 2 for a refusal `seal` itself wrote, and
argparse's usage error is also 2. The old *There is no third one* was
already false for the same reason. The new line is still exhaustive in form.

### ⬜ 7 — a 0.15.3 re-read note describes a unit its row does not cite

`seal/releases/0.15.3.md:60` (A2). The note added by this work item reads
*`handed_to_shell`'s docstring and comment now point at `as_cmd_expands` …*,
but A2's grounds do not cite `handed_to_shell`. What drifted A2 was
`templates/config.md` §*Broad gate* and
`test_the_template_says_which_positions_are_rewritten`, and the note then
runs on with no full stop: *and the claim holds `templates/config.md`
§*Broad gate* moved only in its `%VAR%` sentence*. The note looks copied from
A1, the row above it. This is a paperwork correction and not a fix.

## Findings from execution

Every finding above except ⬜ 7 was confirmed by a probe listed below. ⬜ 3's
first bullet and 🟡 1, 🟡 2 were executed; ⬜ 4, ⬜ 5, ⬜ 6 and ⬜ 7 are
read.

## Regression tests to plant

- `tests/test_a_script_copied_alone_exits_2.py` `CASES`: the second
  `seal.py` row in the 🟡 1 fence.
- `tests/test_unverified_rows_close.py`: the help case in the 🟡 2 fence,
  beside `test_the_documents_state_the_merge_base_footing`.

## Facts for the evidence ledger

- C1 (`seal/ledger/1790381329-the-deferred-sentences-and-pins.md`): once 🟡 1
  lands, `HOOK_PURPOSES` drifts; the claim should add that the `config.py`
  sentence says it *reads* `config.md`, and that a second `CASES` row holds
  it (red at `79b6626f`).
- C3: once 🟡 2 lands, add the help case to the grounds; its claim of the
  `--baseline` help is then held by a case that reads the help alone.
- Executed at `79b6626f`: 289 of 835 anchored live ledger rows (34.6%) carry
  no id `ROW_ID` reads.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal`'s missing-sibling sentence says `hooks/config.py` reads and writes `config.md`; it only reads, and the sentence is unpinned | `skills/implement/scripts/seal.py:104` | open | `hooks/config.py`'s docstring names `seal.py` as the writer; `fold_check.py:501` says *reads*; M2 green |
| 🟡 2 | the `--baseline` help the documents case was extended for is not held by it: the tip phrase stands three times in the file | `tests/test_unverified_rows_close.py:1238` | open | M7: help reverted alone, case green; the proposed help case red under M7 |
| ⬜ 3 | three test sentences state the `Pass`-beside-`nobody` refusal with no timing; one fixture exits 0 | `tests/test_the_fixes_close_the_record.py:709` | open | executed: `assert _code == 0` passes in that case; the other two at `tests/test_the_fixes_close_the_record.py:469` and `tests/test_the_rules_have_one_owner.py:346`, read |
| ⬜ 4 | the variable case's docstring still says the part is *expanded the same way* | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:217` | open | read; the phrase phase 6 removed from `handed_to_shell` |
| ⬜ 5 | the copied-alone module says six shipped scripts load a sibling; nine do | `tests/test_a_script_copied_alone_exits_2.py:4` | open | read; `survivor_check.py`, `broad_gate.py`, `evidence_check.py` load siblings too |
| ⬜ 6 | `seal.py`'s exit-code line gives 2 one meaning; `parser.error` at `:2466` is also 2 | `skills/implement/scripts/seal.py:77` | open | read |
| ⬜ 7 | A2's re-read note describes `handed_to_shell`, which A2 does not cite, and runs two sentences together | `seal/releases/0.15.3.md:60` | open | read; correction, not counted in `Needs a fix` |
| 🟢 | #610: both scripts exit 2 with a sentence for a missing sibling and do not swallow a real `ImportError` in a present one | `skills/implement/scripts/seal.py:112`, `skills/verify/scripts/payload_meter.py:145` | confirmed | P1–P4, M1, M4; class re-enumerated by construction under `skills/` |
| 🟢 | #611: both headings named, summary line pinned | `skills/settle/SKILL.md:118` | confirmed | M5, M6 red |
| 🟢 | #612: every sentence placing the comparison names both places; the frame's non-twins are true | `docs/one-root-by-lifetime.md:197` | confirmed | tree-wide search in both languages; M8, M9 red |
| 🟢 | #615: three silent-set statements match `removed_ledger_rows`; count guard pinned | `skills/code-review/scripts/survivor_check.py:1081` | confirmed | read against the code; M12 red; 289 of 835 recounted |
| 🟢 | #616: defined-`CD` precedence and the substring bound pinned on `%CD%` itself | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:250` | confirmed | M10, M11 red |
| 🟢 | ledger: corrected rows true, re-read rows hold, no drift | `seal/releases/0.13.0.md:8` | confirmed | `evidence-check` 2406 ok / 0 drifted / 0 broken |
| ❓ | where `cmd.exe` resumes scanning after an undefined `%NAME%` | `skills/verify/scripts/broad_gate.py:1284` | ❓ out of verified scope | macOS only; `overview.md` names a Windows run of `cmd.exe`, by whoever next changes the broad gate's `cmd.exe` path |

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

Every mutation was applied in the clone, run on its narrow selection, and
reverted with `git checkout`; `git status` was clean after each probe.

## Paste-ready fixes

### 🟡 1

`skills/implement/scripts/seal.py`, `HOOK_PURPOSES`:

```python
HOOK_PURPOSES = {
    "config.py": "it is what reads the root's config.md, whose Mode row this "
    "command keeps",
    "optin.py": "it is what finds the repository's seal/ root",
}
```

`tests/test_a_script_copied_alone_exits_2.py`, `CASES`, after the existing
`seal.py` row:

```python
    (
        "skills/implement/scripts/seal.py",
        ["mode", "--check"],
        "it is what reads the root's config.md",
        "reads and writes",
    ),
```

### 🟡 2

`tests/test_unverified_rows_close.py`, after
`test_the_documents_state_the_merge_base_footing`:

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

### ⬜ 3

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

### ⬜ 4

```text
tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216-218
    """#596, round 1's 🟡 3 and round 2's 🟡 1. `cmd.exe` expands `%VAR%`
    before it reads a command name, so the part is expanded before it is
    asked whether it is a directory, as far as `as_cmd_expands` models it: a
    name from the
```

### ⬜ 5

```text
tests/test_a_script_copied_alone_exits_2.py:4
Six of the shipped scripts that load a sibling are held here, in one of two
shapes. (`survivor_check.py` and `broad_gate.py` raise their own refusal, and
`evidence_check.py` falls back by design.) Five import it by file path: ...
```

### ⬜ 6

```text
skills/implement/scripts/seal.py:77-79
Exit codes: 0 done · 1 nothing was written, and the message says why · 2 a
file this command loads from `hooks/` is not there, so nothing was read, or
the arguments were unusable (argparse's usage error, and a mode given with
`--check` or `--apply`). Every refusal here names the file, the path, or the
flag that gets past it.
```

### ⬜ 7

```text
seal/releases/0.15.3.md:60, A2 — replace this work item's note with:
**Re-read 2026-09-26 in work item 1790381329 (#616):** `templates/config.md`
§*Broad gate* moved only in its `%VAR%` sentence, and the template case's
needles were re-cut with it; the positions it states and the examples it
names are unchanged, and the claim holds
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the `config.py` purpose sentence and its pin), 🟡 2 (the `--baseline` help pin)
Loses a record or crashes: no

The broad gate has not come due: this round leaves two findings open, so the
sealer's spawn waits for the round that closes them.

## Proof

Opened in the clone at `79b6626f`: `spec.md`, `overview.md`, `survivors.md`,
`questions.md`, `changelog.md`,
`seal/ledger/1790381329-the-deferred-sentences-and-pins.md`, the full range
diff of `skills/`, `templates/`, `tests/`, `.github/`, `docs/`, both READMEs
and `seal/releases/` (word diff);
`skills/implement/scripts/seal.py` (docstring, loader, exits, `parser.error`),
`skills/verify/scripts/payload_meter.py` (`_session_cost`, `main`),
`skills/verify/scripts/broad_gate.py` (`load`, `as_cmd_expands`,
`handed_to_shell`), `skills/verify/scripts/unverified_check.py`
(`merge_base`, `base_label`, `retired_by_rule`, `main`),
`skills/code-review/scripts/survivor_check.py` (`ROW_ID`, `ledger_rows`,
`removed_ledger_rows`), `skills/code-review/scripts/round_record.py`
(`run_check`), `skills/code-review/scripts/chain_check.py` (module docstring
§the draft excuse, `pass_checked`), `skills/settle/SKILL.md` §1,
`skills/settle/scripts/settle.py` (docstring exits, headings), `hooks/config.py`
(docstring), `.github/workflows/hygiene.yml` and `templates/hygiene.yml`
(triggers, checkout, the unverified step), `docs/the-evidence-ledger.md`
§*The unverified record*, `docs/commit-review-gate-spec.md` §the rule arm,
`docs/round-record-spec.md` §the `nobody` paragraph,
`docs/review-handoff-protocol.md` §what it refuses, `docs/review-chain-spec.md`
§the survivor sweep and §the draft excuse, `skills/code-review/orchestration.md`
§#598, `agents/smith.md` §Fixes checked by, the test files named in the
findings, and issues #610, #611, #612, #613, #615 and #616.
