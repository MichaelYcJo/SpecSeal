# a-language-row-that-governs-four-things — review round 4

<!-- The verifying round for round 3's fixes (target: the diff
adc3b9d..133ddf3). Nothing needing a fix, which by the stopping rule closes
the run: a round finding nothing that breaks a gate and nothing that misleads
a person ends it. Written by the review orchestrator, which implemented this
work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from adc3b9d, reviewed at 133ddf3 |
| PR | none yet |
| Broad gate | a73de50 against `origin/release/v0.5.0`: `pytest tests/ -q -n auto` 1647 passed · 1 skipped; `ruff check .` clean; `ruff format --check .` 85 files; `evidence_check.py --strict .` 455 ok · 0 drifted · 0 broken; `unverified_check.py --baseline` exit 0 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

## What this round was asked to attack

The same question a fourth time — **did this fix derive one level and leave
the next by hand?** — with four places named: every module-level string
either checker matches against a record, against the derivation; whether
round 3's three-unreachable claim holds or the patterns are built from
constants; whether any other message in `chain_check.py` spells a constant by
hand; whether the twelve move spellings are honestly described and whether
any fires on ordinary prose; and whether the two backticked emoji read
consistently elsewhere.

## The answer, after four rounds of the same question

**No.** This is the first of the four where the fix did not leave a level by
hand.

The reviewer imported both checkers and put every module-level literal they
match against a record — twenty of them — against the flattened section, in
the backticked form the assertion requires. All twenty are there, including
the two emoji this diff delimited. The constants the derivation does not
reach are all non-language: separators, arrows, ref namespaces, an invisible-
character set, a directory skip list, and one filename the list's **Code**
bullet already governs.

And round 3's deferral holds under checking, which the previous one did not:
`PASS_RE`, `CHECKER_RE`, `routing.ROUND_RE` and `fold_ledger.MARKER_LINE_RE`
each build their literal inline inside the pattern. There is genuinely no
constant to name.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 🟡 1 | 🔴 and four more unreached by the derivation | `tests/…`, `templates/config.md` | answered — reproduced across all twenty literals | reviewer imported both modules and checked each backticked form against the section |
| r3 ❓ 2 | three strings said to have no constant | `chain_check.py`, `fold_ledger.py` | answered — the claim holds, which the previous round's cost estimate did not | reviewer read all four patterns |
| 🟢 1 | `skills/implement/SKILL.md` restates the markers half by hand and still writes `✅` unbackticked with 🔴 absent | `skills/implement/SKILL.md:50` | pass — no action. The same sentence points at `templates/config.md` for every checker-matched string and closes with *and the other markers*, so it misleads nobody. Recorded because it is round 2's 🟡 4 one file over and no round had seen it | reviewer grepped; no case pins that clause |
| 🟢 2 | five messages in `chain_check.py` write `none` by hand while `NONE_WORD` exists, and one names three of five `CLOSED_WORDS` | `chain_check.py:959, 1411, 1419, 1445, 1462, 1583` | pass — every one agrees with its constant today, and `none` is on the exclusion list as fixed English, so nothing can drift under them | reviewer ran an AST scan for non-docstring strings carrying a constant's value |
| 🟢 3 | the twelve move spellings and their comment | `tests/test_the_settings_have_a_front_door.py` | pass — the comment states the limit rather than hiding it, and none of the twelve fires on this skill's prose | reviewer ran all twelve plus a near-miss scan |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: twenty derived literals, backticked, against the section | twenty ok |
| reviewer: every module-level constant in both checkers against the derived set | only non-language constants unreached |
| reviewer: the four regular expressions round 3 deferred | each builds its literal inline — no constant to name |
| reviewer: an AST scan of `chain_check.py` for hand-written constant values in messages | six sites, all agreeing with their constants |
| reviewer: twelve move spellings against the skill, with a near-miss scan | none hit, none near |
| orchestrator: full suite, `ruff check .`, `ruff format --check .`, `evidence_check --strict` | see the Broad gate row |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–3 | `templates/config.md`'s *What no row governs* and its two derivations | changed in every round; closed here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/implement/SKILL.md` restates the markers half by hand | this record | the repository owner, at the next edit of that file |
| Six messages in `chain_check.py` spelling a constant's value | this record | the repository owner |
| Three strings behind regular expressions with no literal to derive | round 3's record | the repository owner |
| The mirror paragraph; whether `routing.md` and the todo files are governed | round 1's record | the repository owner |
