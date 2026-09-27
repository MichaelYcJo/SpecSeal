# 1790381329-the-deferred-sentences-and-pins — review round 2 report

Verifying round. Target SHA `a6f836c1`. The target is the fix diff
`e195cf09..fd22baee`: `4379b60a` holds the fixes and `fd22baee` records the
survivors. `a6f836c1` only closes round 1's record. I read it in a
`git clone --no-local` at `a6f836c1` under the session scratchpad
(`<scratchpad>/1790381329-the-deferred-sentences-and-pins/round-2/clone`).
Nothing was written in the worktree except this file.

Ran by: specseal:warden on claude-opus-5-5.

I read the implementer's account as claims: the fix commit's message, the new
ledger notes, the `survivors.md` rows and round 1's fix table. I checked each
claim used below against the code at the target SHA. I carried round 1's
coordinates and did not carry its verdicts. Each of round 1's seven findings
is answered below on my own grounds.

## Summary

Both yellow findings are closed, for the named example and for its class.

- The `seal` refusal now says `hooks/config.py` reads `config.md`. Every
  purpose sentence that every sibling loader under `skills/` prints matches
  the file it names.
- The `--baseline` help has a pin of its own. The pin goes red when either
  half of the phrase is dropped from the help alone. The documents case stays
  green under the same mutation, which confirms the reason the new case
  exists.

Round 1's five paperwork-level findings are closed at their coordinates. The
class sweep for ⬜ 3 found one more twin that round 1 and the fix pass both
missed. A test comment says `close` "still exits 1" on the `Pass`-beside-
`nobody` notice, but in a draft it exits 0. I ran that case to confirm it
(new ⬜ 1). The fix pass's reflowed docstrings also left three ragged lines
(new ⬜ 2). Neither changes any behaviour.

Nothing opened here needs a fix, so the sealer's spawn has come due.

## What round 1 found, and what stands now

### Round 1's 🟡 1: closed, example and class (read and executed)

`skills/implement/scripts/seal.py:104-108`, `HOOK_PURPOSES["config.py"]` now
reads *it is what reads the root's config.md, whose Mode row this command
keeps*. That is true in both halves. `hooks/config.py`'s module docstring says
*the READER moved here and the writer stayed there*, meaning in `seal.py`.
`seal.py` uses only its reading names from it: `config_rows`, `declared_mode`,
`fence_map`, `unfenced` and the constants. The `Mode` row is written by
`seal.py`, so *this command keeps* is accurate.

The pin is `tests/test_a_script_copied_alone_exits_2.py`, `CASES`, the second
`seal.py` row. Its needle is *it is what reads the root's config.md* and its
absent column is *reads and writes*. Two probes each turned it red on its own,
and the other seven rows stayed green:

- the old sentence put back (probe M1);
- a different false purpose that avoids the absent phrase, *it is what writes
  the root's config.md* (probe M2).

**The class.** I enumerated every loader under `skills/` by construction, as
every file carrying `spec_from_file_location`, `sys.path.insert` or `runpy`.
There are nine. I read each purpose sentence against what the caller actually
uses from the file it names:

| Loader | File named | Sentence | Holds |
|---|---|---|---|
| `seal.py` | `hooks/config.py` | reads the root's config.md | yes: reader only |
| `seal.py` | `hooks/optin.py` | finds the repository's seal/ root | yes: `repo_root`, `home_at`, `home_paths`, `git_common_dir` |
| `payload_meter.py` | `session_cost.py` | reads a transcript's spawns and finds their subagent transcripts | yes: C2's re-read note names the four names used, and I confirmed them |
| `round_record.py` | `chain_check.py`, `unverified_check.py`, `hooks/routing.py` | the checker this command writes records for · where the work item's records are read from · reads the work item's routing.md | yes |
| `settle.py` | `unverified_check.py`, `evidence_check.py`, `hooks/optin.py` | where the fold record is read from · resolves a ledger row's anchor · finds the seal/ root | yes: `folded_items`, `todo_open_rows`, `live_lines` |
| `fold_check.py` | `unverified_check.py`, `hooks/optin.py`, `hooks/config.py` | where the fold's markers are read from · finds the seal/ root · reads the rows of seal/config.md | yes |
| `survivor_check.py` | `unverified_check.py`, `evidence_check.py`, `hooks/optin.py`, `hooks/routing.py` | says what a retirement is · says when a ledger row's anchor left the code · says where local mode's seal/ root is · says whose a local-mode declaration is | yes |
| `chain_check.py` | its two readers | no purpose sentence; `main` catches the load and prints one reason | nothing to judge |
| `broad_gate.py`, `evidence_check.py` | — | no missing-sibling purpose sentence | nothing to judge |

No other loader gives a file a purpose it does not have.

### Round 1's 🟡 2: closed, and the new unit is pinned (read and executed)

`tests/test_unverified_rows_close.py`, `test_the_baseline_help_names_both_places`,
is the one unit the fix created (depth 1 in round 1's `New units`). I judged
it as new code:

- It renders `uc.main(["--help"])` and joins whitespace before the substring
  test, so argparse's line wrapping cannot split the needle.
- The needle has no hyphen, so textwrap's hyphen breaking cannot reach it.
- Every word in it is shorter than argparse's minimum help width, so no word
  can be broken either.
- The rendered `--help` carries the phrase only in the `--baseline` help. The
  parser description is the one-line summary, and I read the whole rendered
  output to confirm it. So the case reads the help alone, as its docstring
  says.

Mutations in the clone, each applied alone:

- M3, the tip half dropped from the help only: the new case went red and
  `test_the_documents_state_the_merge_base_footing` stayed green (9 passed).
  That reproduces round 1's M7 and shows why the new unit was needed.
- M4, the fork-point half dropped from the help only: the new case went red.

The unit is anchored in C3's grounds
(`#test_the_baseline_help_names_both_places@d07e75c6`), and `evidence-check`
resolves it. The comment on the documents row now says why that row cannot
hold the help.

### Round 1's ⬜ 3: closed at its three coordinates, and the class has a fourth member

The three sentences now carry *at a ready pull request*. They are
`tests/test_the_fixes_close_the_record.py:469-472`, `:709-711` and
`tests/test_the_rules_have_one_owner.py:346-349`. I checked the added clause
*(phase 3 measured exit 1 here, before #598)* against history. The sentence
dates from #161's run (merged 2026-09-05), and #598's draft excuse landed in
`aa0e45e` (2026-09-25), so the clause is true.

I searched for the class by meaning across the whole tree, rounds excluded.
English: *beside `nobody`*, *`nobody` beside*, *`Pass` beside*, *refuses
(that|the) pair*, `nobody` near *refus*, and *exits 1 on the chain*/*notice
about*. Korean: *`nobody` 옆/거부/실패/막*, *`Pass` 옆*, *`Pass` 가 체크*,
*준비 … nobody*. Every hit was read in context.

- `README.ko.md:210-211` and `:605-606` say *리뷰 준비가 된 PR*, so they
  carry the timing.
- `tests/test_the_fixes_close_the_record.py:926-931` says *judged as READY*.
- `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:513-514`
  describes a hypothetical end that its own `run` helper judges with no
  payload. A run with no payload is judged as ready, so that sentence is true.
- `tests/test_the_last_rounds_fixes_are_checked.py:628` and its cases run with
  no payload too.

One sentence is a twin: `tests/test_the_fixes_close_the_record.py:2323-2325`
(new ⬜ 1 below).

### Round 1's ⬜ 4: closed, example and class (read)

`tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216-219` now says *as far
as `as_cmd_expands` models it*. I searched the tree in English for *the same
way*, *exactly*, *identical*, *as `cmd.exe` does/would/expands*, and *the way
`cmd`* near `cmd`, `%VAR%` or *expan*. In Korean I searched for 같/똑같/그대로/동일
near `cmd`/`%`/확장. Only three sentences outside the rounds describe the
expansion:

- `skills/verify/scripts/broad_gate.py:1345-1346`;
- `templates/config.md:209-212`;
- this docstring.

All three bound the claim to the model or to the plain form. The one *exactly
as before* at `templates/config.md:217` is about positions left unrewritten,
not about the expansion. *A defined `CD` wins, as it does in `cmd.exe`* is the
precedence that round 1's M10 pinned.

### Round 1's ⬜ 5: closed (read)

The module docstring no longer states a count. It says not every loader is
held here and names the three that are not: `survivor_check.py`,
`broad_gate.py` and `evidence_check.py`. The construction enumeration above
gives nine loaders under `skills/`: six held and those three. The sentence is
therefore complete as written. The hooks import each other as one shipped
directory, and a hook is never run as a copy on its own, which is outside
this module's subject.

### Round 1's ⬜ 6: closed, every exit-2 path (read)

- **`seal.py`.** It has three exit-2 paths: `refuse_without_hooks` raises
  `SystemExit(2)`, `parser.error(... cannot be given together)` exits 2 at
  `:2468`, and argparse's own usage errors exit 2 (a missing subcommand, a bad
  choice, an unknown flag). The new line names all three. Its *any two of a
  mode, `--check` and `--apply`* matches `len(given) > 1`. No interpreter
  floor exists in this file, and the line claims none. Every other refusal is
  `return 1`.
- **`payload_meter.py`.** It also has three exit-2 paths: `below_floor` at
  `:113-116`, the missing sibling at `:154`, and argparse's usage error. The
  line names all three. Its 1 is `CalibrationError` and *no agents*, as
  stated.

Neither docstring's exit paragraph is rendered. `seal`'s description is a
literal string, and `payload_meter`'s is only the docstring's first
paragraph. So contract §14 asks for no pin here.

### Round 1's ⬜ 7: closed (read)

`seal/releases/0.15.3.md:60`: A2's note now concerns what A2 cites, which is
`templates/config.md` §*Broad gate* and the template case. It no longer runs
two sentences together. The `handed_to_shell` note stands on A1 (`:59`),
which cites `broad_gate.py#handed_to_shell`. `survivor-check` over the fix
range reports the two places `survivors.md` now records, and I agree with
both sets of grounds.

### Ledger notes (read, and executed through `evidence-check`)

- **C1, corrected.** The claim now names both purposes, and each matches the
  code. The note's *red against the old sentence* is what M1 reproduced. Its
  ⬜ 6 sentence matches the docstring.
- **C2, re-read.** The claim now lists argparse's usage error, which is true.
  The note's four `session_cost` names are the ones `payload_meter.py` uses.
- **C3, corrected.** The grounds gained the new unit's anchor. The claim
  sentence was already true of the documents. What was false was the pin that
  the verified-behaviour cell implied for the help, and the note says so. M3
  reproduced the note's *red with the tip dropped from the help alone while
  the documents case stayed green*.
- **C5, re-read (⬜ 4).** Accurate. The assertions are unchanged, as the diff
  shows.
- **`seal/releases/0.11.4.md:61, :63` and `seal/releases/0.8.1.md:31`.** The
  three re-read notes (⬜ 3) each describe exactly the comment or docstring
  edit that the diff shows. Each re-stamped hash resolves.

`evidence-check` at the target: 2407 ok, 0 drifted, 0 broken.
`correction-check --range e195cf09...a6f836c1` exits 0.

## Findings from execution

### ⬜ 1: a fourth #613 twin says `close` exits 1 where it exits 0

`tests/test_the_fixes_close_the_record.py:2323-2325`, in
`test_re_closing_a_half_restored_record_is_refused_for_every_word`:

> 0 or 1: a green `close` still exits 1 on the chain-check notice about
> `Pass` beside `Fixes checked by: nobody`, which is unrelated and is what
> #427's own reproduction reported.

`close` runs the check through `round_record.run_check`. That function tells
the check `draft` unless `pull_request_is_ready` says otherwise, and in a test
repository it never does. Since #598 the pair prints in a draft and does not
fail. I tightened the assertion in the clone to `code == 0`, and it passed for
all three parameters (`fixed`, `answered` and `deferred`). The `fixed` output
carries the `nobody` notice. The other two land on `no fixes to check`, so no
notice prints at all. The sentence dates from #427 (`48d4021`, 2026-09-18),
which is before #598.

This is round 1's ⬜ 3 class: a test sentence that states the refusal with no
timing, in a fixture where the check exits 0. It is the twin that round 1's
first bullet already found at `:709`. Round 1's search and the fix pass's
search both missed it, because it says *notice* and *exits 1* rather than
*refuses*. No behaviour is wrong, and the loose `in (0, 1)` still admits the
real outcome. A reader who trusts the comment is told the draft run fails. A
fence follows under the fixes heading.

## Findings from reading

### ⬜ 2: the fix pass's reflowed docstrings left ragged lines

- `tests/test_a_script_copied_alone_exits_2.py:9` is 108 columns wide. The
  rewritten lines above it were rewrapped, and the old tail *In the first
  four 1 means a finding or a refusal* was joined onto the last of them.
- `tests/test_the_fixes_close_the_record.py:472` is 115 columns wide, because
  *(phase 3 measured exit 1 here, before #598).* was inserted without
  rewrapping.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:219` holds only *name
  from the*.

`ruff check` and `ruff format --check` pass on all seven touched files,
because the selection has no E501 and the formatter does not rewrap
docstrings. So nothing enforces the wrap. It is a reading cost and nothing
more.

### Carried: where `cmd.exe` resumes after an undefined `%NAME%`

This is round 1's question, still unverified. The claim rests on a platform I
cannot run here, and the docstring claims neither answer.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's yellow finding 1 is closed — `HOOK_PURPOSES` says `hooks/config.py` reads `config.md`, and every loader's purpose sentence matches its file | `skills/implement/scripts/seal.py:104` | confirmed | executed: M1 and M2 each red on the second `seal.py` row; read: nine loaders enumerated by construction, every sentence checked against the names used |
| 🟢 | round 1's yellow finding 2 is closed — `test_the_baseline_help_names_both_places` reads the `--baseline` help alone and is pinned | `tests/test_unverified_rows_close.py:1283` | confirmed | executed: M3 and M4 each red on the new case, the documents case green under M3; anchored in C3 |
| 🟢 | round 1's finding 3 is closed at its three coordinates | `tests/test_the_fixes_close_the_record.py:469` | confirmed | read; the *before #598* clause checked against history; the class's fourth member is ⬜ 1 below |
| 🟢 | round 1's finding 4 is closed, example and class | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216` | confirmed | read; tree-wide search in English and Korean, three expansion sentences, all bounded |
| 🟢 | round 1's finding 5 is closed — no count, and the three unheld loaders are the complete set | `tests/test_a_script_copied_alone_exits_2.py:3` | confirmed | read; nine loaders under `skills/` by construction |
| 🟢 | round 1's finding 6 is closed — both exit-code lines name every exit-2 path | `skills/implement/scripts/seal.py:77` | confirmed | read; `seal.py` three paths, `payload_meter.py` three paths |
| 🟢 | round 1's finding 7 is closed — A2's note concerns what A2 cites | `seal/releases/0.15.3.md:60` | confirmed | read; `survivor-check` places recorded in `survivors.md` |
| 🟢 | the fix pass's ledger notes say what the code does | `seal/ledger/1790381329-the-deferred-sentences-and-pins.md:3` | confirmed | read C1, C2, C3, C5 and three release re-reads; `evidence-check` 2407 ok / 0 drifted / 0 broken |
| ⬜ 1 | a test comment says a draft `close` exits 1 on the `Pass`-beside-`nobody` notice; it exits 0 | `tests/test_the_fixes_close_the_record.py:2323` | open | executed: `code == 0` held for all three parameters; a twin of round 1's finding 3, first bullet |
| ⬜ 2 | the fix pass's docstring rewrap left three ragged lines | `tests/test_a_script_copied_alone_exits_2.py:9` | open | read; also `tests/test_the_fixes_close_the_record.py:472`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:219` |
| ❓ | where `cmd.exe` resumes scanning after an undefined `%NAME%` | `skills/verify/scripts/broad_gate.py:1284` | ❓ out of verified scope | carried from round 1; macOS only; a Windows run of `cmd.exe`, by whoever next changes the broad gate's `cmd.exe` path |

## Paste-ready fixes

### ⬜ 1

```python
    # 0 or 1 because the exit is not what this case judges. Judged as a
    # draft, as `round_record.run_check` tells the check on a local run,
    # `Pass` beside `Fixes checked by: nobody` prints and `close` exits 0; at
    # a ready pull request the pair is refused and it exits 1, which is what
    # #427's own reproduction reported before #598. The refusal below is
    # exit 2.
    code, out, _first = close(repo, 1, table, f"{a}..{b}")
    assert code in (0, 1), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the five touched test modules (copied-alone, fixes-close-the-record, gate, rules-have-one-owner, unverified), at `a6f836c1` | exit 0: 440 passed, 1 skipped |
| `ruff check` and `ruff format --check` on the seven touched Python files | exit 0 both: all checks passed, 7 files already formatted |
| `evidence_check.py .` at `a6f836c1` | exit 0: 2407 ok · 0 drifted · 0 broken |
| `survivor_check.py --range e195cf09...fd22baee` | exit 1: two places, `seal/releases/0.15.3.md:59` and `spec.md:208`, both the rows `fd22baee` added to `survivors.md` |
| `correction_check.py --range e195cf09...a6f836c1` | exit 0 |
| M1: the `config.py` purpose put back to *reads and writes* | copied-alone `seal.py1` red, 7 passed |
| M2: the `config.py` purpose reworded to *it is what writes the root's config.md* | copied-alone `seal.py1` red, 7 passed |
| M3: the tip half dropped from the `--baseline` help only | `test_the_baseline_help_names_both_places` red; the documents case green (9 passed) |
| M4: the fork-point half dropped from the `--baseline` help only | `test_the_baseline_help_names_both_places` red |
| `assert code == 0` put in place of `in (0, 1)` in `test_re_closing_a_half_restored_record_is_refused_for_every_word` | held for all three parameters (⬜ 1); the file restored |
| `unverified_check.py --help` rendered | the tip phrase appears in the `--baseline` help only |
| the broad gate — full suite, repository-wide lint, typecheck | not yet — the sealer's, after the rounds settle; nothing here ran it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: no
Loses a record or crashes: no

The broad gate has come due. This round leaves nothing that needs a fix: the
two ⬜ rows are for the orchestrator to take or leave, and the ❓ is carried
with its answerer named. What comes due is the sealer's spawn at the tip that
closes this round, not a run for the session reading this.

## Proof

Opened in the clone at `a6f836c1`:

- round 1's `round-1.md` and `round-1-report.md`, `survivors.md`, and
  `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`;
- the fix diff `e195cf09..fd22baee` in full: `skills/`, `tests/`, the ledger
  fragment and `seal/releases/` (word diff);
- `seal/releases/0.15.3.md` rows A1 and A2;
- `skills/implement/scripts/seal.py`: the docstring's exit line,
  `HOOK_PURPOSES`, `refuse_without_hooks`, `main` and its argparse set-up,
  every `return`/`SystemExit` found by grep, and what it uses from `optin` and
  `config`;
- `skills/verify/scripts/payload_meter.py`: the docstring's exit line,
  `below_floor`, `_session_cost`, `main`;
- `hooks/config.py`: the module docstring and function list;
- the loader and purpose lines of `round_record.py`, `settle.py`,
  `fold_check.py`, `survivor_check.py` and `chain_check.py`;
- `round_record.py#run_check`;
- `skills/verify/scripts/unverified_check.py`: the `--baseline` help and its
  rendered `--help`;
- `skills/verify/scripts/broad_gate.py:1340-1350` and
  `templates/config.md:205-218`;
- `tests/test_a_script_copied_alone_exits_2.py:1-30`, the gate case's
  docstring, and `tests/test_the_fixes_close_the_record.py:240-262`,
  `:455-500`, `:922-950` and `:2285-2330`;
- `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:186-202` and
  `:505-542`, and `tests/test_the_last_rounds_fixes_are_checked.py:128-140`
  and `:626-660`;
- `ruff.toml` and `bin/test`.

The mutation probe (one file named test_tmp_mutations.py, under the round's
scratch directory and outside the clone) ran once and was deleted. Every
mutated file was restored with `git checkout`, and the clone's
`git status --short` was empty afterwards.
