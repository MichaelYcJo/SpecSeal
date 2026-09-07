# 1788789330-the-update-notice-names-the-expensive-move — review round 4

| Field | Value |
|---|---|
| Target SHA | 73ab600 |
| Ran by | warden on claude-opus-5 |
| PR | 233 |
| Broad gate | passed at e82ef31 — 2561 passed, 2 skipped; `ruff check .` and `ruff format --check .` both exit 0. The three records written after it change no code |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4 of `1788789330-the-update-notice-names-the-expensive-move` (ticket #134, PR #233), at target `73ab600`, base `86e140f`. A verifying round over two prose corrections, small on purpose.

Round 3 opened one 🟡: the exact-pin case's docstring and ledger row S1·S2·S3 both claimed the two cases hold together against a careless golden-string update, and round 3 measured that they do not — with the golden brought along in the same edit, an added overclaim and `unmeasured, yet it is picked up` both pass at `18 passed`. The orchestrator applied round 3's paste-ready corrections itself rather than commissioning a fix pass, because the run was capped and what the two sentences said was measurably false. `chain_check` then refused the checked `Pass` and was right to: those corrections are fixes nobody had read, which is the state #33 measured at a 100% hit rate. This round is the way out that costs no round.

The diff was `89333dd..73ab600` and nothing else: the test docstring's paragraph, the ledger row's corresponding sentence, the `--reverify` that re-anchored the row's hash over the edited case, `NAME NOT IN TREE` markers on the record lines naming a deleted local and deleted probe files, and the records' `Broad gate` cells.

The question was narrow and was to be answered by measurement rather than reading: is what the two sentences now say TRUE? Each shape the new text claims passes was to be run with the notice and the golden string mutated together, the way an author rewording it would — an overclaim added to the reload's claim, the gap flipped, the restart named first, the `measured` label dropped, the `skill bodies` subject dropped. And the new text's claim that EXACTLY ONE property survives a rewording was to be attacked from the other side: drop the scope qualifier while updating the golden and see it go red, then look for a second property that also survives.

The bound was stated: rounds 1, 2 and 3 all closed on fixes, so anything this round opens is capped there and becomes an issue rather than a fix; and neither manufacturing a finding nor softening a real one was acceptable, because both cost the same thing — the truth of a record that says what a check does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 Both corrected sentences say the second case holds *exactly one* property across a rewording; it holds two — the notice must name `/reload` in some sentence, and that same sentence must carry the scope qualifier | `tests/test_version_check.py:108` | deferred #238 | Executed in a `--no-local` clone at `73ab600`. `/reload-plugins` replaced with `a plugin reload`, golden updated in the same edit, whole module → exit 1, `1 failed, 17 passed`, `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` raising at `tests/test_version_check.py:163`. Sibling sites, same sentence: `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3` row S1·S2·S3, and `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:35`. Round 3 had already recorded the property at `round-3-report.md:67` |
| 2 | ⬜ The fix note's Grounds cell opens with an empty backtick pair where the one-line summary belongs | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:35` | open | Read. Same at `:36`, and three times in `round-2.md`, so it is the generator's shape rather than this commit's. A record location, so `Needs a fix` does not count it |
| 3 | ✅ Round 3's finding 1 — the six shapes the corrected docstring and ledger row list as passing all do pass | `tests/test_version_check.py:101` | answered | Executed, each with the notice and the golden mutated together, whole module: overclaim appended to the reload's claim, gap flipped to `unmeasured, yet it is picked up`, restart named before the reload, `measured` label dropped, `skill bodies` subject dropped, two of the three axes dropped — `18 passed`, exit 0, every one. A rewrite-only control that changes no meaning also stays at `18 passed` |
| 4 | ✅ The scope qualifier does hold across a rewording, as claimed | `tests/test_version_check.py:164` | answered | Executed. Qualifier dropped with the golden updated → exit 1, `1 failed, 17 passed`; qualifier moved into a sentence of its own, so it no longer sits in the reload's sentence → exit 1, `1 failed, 17 passed`. Both fire the second case |
| 5 | ✅ The row's re-anchored hash is over the file as it now stands | `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3` | answered | Executed. `bin/evidence-check .` → exit 0, the fragment `12 ok · 0 drifted · 0 broken`; `bin/evidence-check . --reverify` → exit 0 and `git status --porcelain` empty afterwards, so `d2062fee` is what the current content hashes to |
| 6 | ✅ The `NAME NOT IN TREE` markers exempt only their own lines | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:70` | answered | Executed. Baseline exit 0, `0 refused`. Marker stripped off `round-3.md:70` → exit 2, that line named. An unmarked new line naming the two absent names appended to `round-3.md` → exit 2, both named at the new line. The same appended to `round-3-report.md` → exit 2, named there. Records restored byte-identical |
| 7 | ❓ out of verified scope — the `Broad gate` cell's `2561 passed, 2 skipped` and the two `ruff` exits | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:8` | unverified | §2 keeps the full suite, the repository-wide lint and the typecheck out of a round's hands, so this round ran neither. The cell names the SHA it ran at, which is auditable. What the orchestrator answers: the gate ran at `e82ef31` plus the marker commit, and `73ab600` — a one-character record change — landed after it, so the stamp is one record-only commit behind HEAD and will be further behind once round 4's own record lands |

## Paste-ready fixes

```python
    Two properties survive a rewording, and both are in
    `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`:
    some sentence of the notice names `/reload`, and that same sentence
    carries the scope qualifier. Measured with the golden brought along —
    `/reload-plugins` swapped for `a plugin reload` fires the first, and the
    qualifier moved into a sentence of its own fires the second, `1 failed,
    17 passed`, exit 1 each time. Everything else is carried by the message
    below, which is an instruction to a person rather than a check.
```
```markdown
The second case holds two properties across a rewording: some sentence of the notice names `/reload`, and that same sentence carries the scope qualifier. Measured with the golden brought along — `/reload-plugins` swapped for `a plugin reload` fires the first, the qualifier moved into a sentence of its own fires the second, `1 failed, 17 passed`, exit 1 each time. The rest is carried by the assertion message, which a person reads rather than a checker.
```
```markdown
Both sentences now say what the pair actually holds and name the message as an instruction to a person rather than a check. Round 4 measured that they understate it by one: the second case also fires when no sentence of the notice names `/reload`, which `round-3-report.md:67` had already recorded.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_version_check.py -q`, `--no-local` clone at `73ab600` | exit 0, `18 passed`. Baseline |
| Control — the notice and golden rewritten with no change of meaning | exit 0, `18 passed`. The rewrite mechanism itself changes no verdict |
| Overclaim appended to the reload's claim, golden updated in the same edit | exit 0, `18 passed`. Not caught |
| Gap flipped to `unmeasured, yet it is picked up`, `restart` kept, golden updated | exit 0, `18 passed`. Not caught |
| Gap flipped, `so restart for those` dropped with it, golden updated | exit 1, `1 failed, 17 passed`; `test_the_warning_names_both_commands_in_order` fires. Outside the pair — the mutation's own artifact, recorded so the row above is not read as a clean pass |
| Restart named before the reload, golden updated | exit 0, `18 passed`. Not caught |
| `measured` label dropped, golden updated | exit 0, `18 passed`. Not caught |
| `skill bodies` subject dropped, golden updated | exit 0, `18 passed`. Not caught |
| Two of the three axes dropped, golden updated | exit 0, `18 passed`. Not caught |
| Scope qualifier dropped, golden updated | exit 1, `1 failed, 17 passed`; `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` fires. Caught, as claimed |
| Scope qualifier moved into a sentence of its own, golden updated | exit 1, `1 failed, 17 passed`; the same case fires. Caught |
| **`/reload-plugins` replaced with `a plugin reload`, golden updated** | **exit 1, `1 failed, 17 passed`; the same case fires at `tests/test_version_check.py:163`, `the notice names no reload for the docstring to disagree with`. Finding 1** |
| `bin/evidence-check .` on the clean clone | exit 0. `seal/ledger.md` 762 ok, the fragment `12 ok · 0 drifted · 0 broken`, records arm `0 refused` |
| `bin/evidence-check . --reverify` on the clean clone | exit 0, `git status --porcelain` empty afterwards. No anchor moved |
| `bin/evidence-check .` with the marker stripped off `round-3.md:70` | exit 2, `NOT-IN-TREE … round-3.md:70`, `1 refused` |
| `bin/evidence-check .` with an unmarked new line naming the two absent names appended to `round-3.md` | exit 2, both named at the new line, `2 refused` |
| `bin/evidence-check .` with an unmarked new line appended to `round-3-report.md` | exit 2, named at the new line, `1 refused` |
| `git diff 89333dd..73ab600 -- tests/test_version_check.py hooks/version-check.py`, `^def` lines | no line added or removed. No unit added, none renamed |
| `git status --porcelain` in the clone after every probe | clean. Both mutated files asserted byte-identical against their originals at the end of each script |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/version-check.py:154` | round 1's 1 — open |
| round-1 | `tests/test_version_check.py:96` | round 1's 2 — open |
| round-1 | `hooks/version-check.py:148` | round 1's 3 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | round 1's 4 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/overview.md:21` | round 1's 5 — open |
| round-1 | `hooks/ledger-migrate.py:4` | round 1's 6 — open |
| round-1 | `README.ko.md:310` | round 1's 7 — open |
| round-2 | `README.md:325` | round 2's 1 — fixed |
| round-2 | `tests/test_version_check.py:117` | round 2's 2 — fixed |
| round-2 | `README.md:182` | round 2's 3 — fixed |
| round-3 | `tests/test_version_check.py:101` | round 3's 1 — fixed |
| round-3 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-2.md:9` | round 3's 2 — fixed |
| round-3 | `tests/test_version_check.py:109` | round 3's 4 — answered |
| round-3 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-1-report.md:162` | round 3's 6 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain |  |  |
