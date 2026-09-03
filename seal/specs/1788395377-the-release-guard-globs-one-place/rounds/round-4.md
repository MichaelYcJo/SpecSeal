# 1788395377-the-release-guard-globs-one-place — review round 4

<!-- The verifying round for round 3's fixes (target: the diff afb3217..d21b13a,
three hunks). It opened nothing needing a fix, so the run ends here and this
round does not consume the cap. It did correct round 3's record: three of the
five exit codes that record calls 0 are 1, at this commit and at the base
alike, because the value read was a pipe's rather than the checker's. Written
by the review orchestrator, which is also this work item's implementer. -->

| Field | Value |
|---|---|
| Target SHA | d21b13a (the fix diff from afb3217); HEAD 796ef3d at review time, record-only. One further commit, 476e67f, re-wraps a changelog line this round noted |
| PR | none yet |
| Broad gate | 171cfc0 against `origin/release/v0.5.0`: `pytest tests/ -q -n auto` 1438 passed · 1 skipped; `ruff check .` clean; `ruff format --check .` 81 files formatted; `evidence_check.py --strict .` 357 ok · 0 drifted · 0 broken; `unverified_check.py --baseline` 16 overviews · 36 open · 15 closed · 0 unreadable; `chain_check.py --baseline` exit 0 once this record is committed. **Its first run, at 476e67f, failed one case** — see the row below |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 🔴 1 | the planted case built its expected path with `os.path.join` around a literal `/`, failing the windows leg | `tests/test_chain_hooks.py:220` | answered — the fix is round 3's, this round reproduced its closure | reviewer executed with both `ntpath` and `posixpath`: the splat form passes on each, the literal form passes on posix and fails at the first loop item on nt — which is why a local suite could never have caught it. The splat changes nothing for the two entries with no slash: `split("/")` returns a one-element list and the joined string is identical |
| r3 1b | whether the same shape exists elsewhere | `tests/` | answered | reviewer executed an AST sweep for a literal `/` inside any `os.path.join` argument across `tests/`: zero. Round 3's claim that this was the only one holds |
| r3 1c | whether the planted case is empty | same case | answered | reviewer executed a mutation — the hook's todo paths put back inside `rounds/` — and the case failed with its own message |
| r3 1d | whether the comment's citation is true | `hooks/review-history-guard.py:152-158` | answered | reviewer read it: the block says the literal-slash join produced `specs\item/rounds` on Windows and that CI's windows leg caught it. Both idiom sites it names are real |
| r3 🟡 2 | the changelog credited the spec with a reason only the skill gives | `changelog.md:19-21` | answered — reproduced | reviewer read both: the spec's cell carries the rule and a different reason (why *now*), the skill carries the plurality reason. The new wording splits them correctly. The reviewer noted the summary dropped `unbounded`; 476e67f puts it back |
| r3 🟡 3 | the memo's `Fed back into the spec` read Nothing beside a header naming three changed documents | `overview.md:50-57` | answered — reproduced | reviewer read `templates/sdd-overview.md:60`'s definition against the new text: the answer is the template's sense, and the three documents are named as a change rather than a clause |
| 🟡 A | **round 3's own record is wrong about three exit codes.** It lists `chain_check --baseline`, `fold_ledger --check` and `gather_changelog --check` as exit 0; all three are exit 1, at this commit and at `afb3217` alike. The reviewer reproduced the mistake before catching it — reading `$?` after a pipe reports the pipe's status, not the checker's | `rounds/round-3.md` §Executed probes | answered here rather than by editing round 3: a record is what a round saw, and the correction belongs in the round that made it. The true values are in this record's probe table | reviewer executed all five without a pipe, at both commits |
| 🟡 A2 | what those three exit codes mean, since two of them never run on this pull request | `.github/workflows/hygiene.yml:69, 87, 144-148` | pass — no action | reviewer read: the fold and gather steps exit 0 early unless the base is `main`, and the workflow's own comment calls an unfolded fragment on a feature branch legitimate. `chain_check` runs on every pull request and its one failing line is the last round's unchecked `Pass` — which this record, with its box checked, is what closes |
| 🟡 B | a 125-column line in the changelog paragraph | `changelog.md:21` | fixed at 476e67f, and `unbounded` restored with it | reviewer measured; the repository has longer lines elsewhere and enforces no width here, so this is an editing mark rather than a violation |

## The broad gate found what four rounds could not

Its first run, at `476e67f`, failed one case:
`tests/test_handoff_outlives_the_merge.py::test_the_instructing_documents_name_rounds_as_the_destination`.

That case asserts every mention of `round-N.md` in the hook carries its
directory within forty characters, spelled `rounds` or `ROUNDS_DIR`, because
two of the three places build the path in an f-string and never hold the
literal. Round 2's fix introduced a third spelling — `where`, which *is*
`os.path.join(rel, routing.ROUNDS_DIR)` — so the rendered message was right
and the pin could not see it. Spelled out at `171cfc0` the message is
byte-identical and both checks hold; executed both ways, the pin fails against
`where` and passes against the explicit form.

**No round could have found it, by contract.** Every round runs slices of the
files its diff touched, and this pin lives in a file the branch never opened.
Four rounds read the hook, the skill, the spec, the test and the records, and
none of them ran a file that reads the hook's source as text. That is what the
one broad run is for, and it is the first time in this session it has caught
something the rounds did not.

| Check at `171cfc0` | Result |
|---|---|
| `pytest tests/ -q -n auto` | 1438 passed · 1 skipped |
| `ruff check .` · `ruff format --check .` | clean · 81 files formatted |
| `evidence_check.py --strict .` | 357 ok · 0 drifted · 0 broken |
| `unverified_check.py --baseline … seal/specs/` | 16 overviews · 36 open · 15 closed · 0 unreadable |
| `chain_check.py --baseline …` | exit 0 with this record committed; exit 1 before it, on the last round's unchecked `Pass` |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the hook's output and the case's expectation under `ntpath` and `posixpath`, with and without the splat | splat passes on both; the literal fails on nt at the first item |
| reviewer: the splat against the two slash-free entries | identical strings on both dialects |
| reviewer: an AST sweep of `tests/` for a literal `/` inside an `os.path.join` argument | zero |
| reviewer: the hook mutated to put the todo paths back inside `rounds/` | the planted case fails with its own message |
| reviewer: `pytest tests/test_chain_hooks.py -k "history_guard or posting_reminder"` | 6 passed |
| reviewer: `evidence_check.py --strict .` | 357 ok · 0 drifted · 0 broken, exit 0 |
| reviewer: `unverified_check.py --baseline origin/release/v0.5.0 seal/specs/` | 16 overviews · 36 open · 15 closed, exit 0 |
| reviewer: `chain_check.py --baseline origin/release/v0.5.0` at `796ef3d` and `afb3217` | exit 1 at both — the last round's `Pass` unchecked |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` at both commits | exit 1 at both — fragments unfolded and ungathered, which is the pre-release state and never runs on this pull request |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–3 | `tests/test_chain_hooks.py`'s planted case, `tests/test_the_set_a_work_item_always_has.py`'s case, `hooks/review-history-guard.py`'s posting branch | the three units this run changed in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A ledger row re-hashed twice with no re-read note | issue #97, on 0.6.0 | the repository owner |
| Five prose mentions of the old path, one folding into the gathered ledger at the next release | round 1's record and the pull request body | the repository owner, at the release |
| The guard refusing a real release with a real open row | `overview.md` §Not verified | the repository owner, at the first release that meets one |
