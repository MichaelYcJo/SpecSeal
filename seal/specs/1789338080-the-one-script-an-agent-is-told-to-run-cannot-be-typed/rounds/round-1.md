# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — review round 1

| Field | Value |
|---|---|
| Target SHA | 8208928 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 388 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | test_a_one_word_command_name_is_not_a_locator (depth 1) |
| Needs a fix | yes — 🟡 1, 🟡 2, 🟡 3, 🟡 4 and 🟡 5. None of the five is a spec failure; each is fix or justify, and 🟡 2 and the user-facing half of 🟡 3 are answerable with `spec.md` as written. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the branch's first review, against the whole diff `release/v0.11.4...8208928` with nothing inherited. Spec compliance first against the work item's own `spec.md`, `plan.md`, `questions.md` and phase records, then quality.

Four places were named to attack, in this order, each because a claim rests on it rather than because a defect was known to be there.

1. **The new check's enumeration and its classification arm.** The build's own report had disclosed that two units survived the first mutation sweep — `is_wrapped` reading `all` and `any` alike, and `unwrapped_pairs` returning an empty list, which runs no cases and reports success — and that two further cases were added for them. Whether the twelve units now partition what they claim to partition was named as the load-bearing question.
2. **`seal/ledger.md`.** A branch that removes nothing must not touch the shared file; this one re-stamped eleven hashes because whole-section anchors drifted under the document sweep. Whether each of the eleven claims is still true, and whether the diff really is hashes alone, was named as checkable rather than as a thing to take on the branch's word.
3. **The nine documents.** Whether each locator is actually reachable, and whether any of them broke a phrase `tests/test_the_rules_have_one_owner.py`'s `GENERATOR_NAMED` pins — the build had reported meeting exactly that and moving three locators rather than splitting the pinned phrases.
4. **The scope fence.** `round_record.py`'s arguments, output and verdicts belong to the other two work items of this release, and were to have not moved here.

What arrived as coordinates rather than being left to find: the target SHA, the base, the draft pull request number, the four owner-and-work answers in `questions.md`, and the scope fence's eight ticket numbers.

What the orchestrator had already executed at this HEAD, handed over so the round would not repeat it: six modules — the two new ones plus `test_docs_line_wrap.py`, `test_the_rules_have_one_owner.py`, `test_the_release_check_watches_what_ships.py` and `test_a_rider_reaches_its_file.py` — 261 passed, 8 skipped, exit 0, the eight skips all from the new module's own parametrisation over scripts no shipped document names; `ruff check` and `ruff format --check` on the two new test files, both exit 0.

The broad gate was withheld by name: it is the sealer's single act after the rounds settle, and no segment in this round was to take it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The locator rule cannot fail for `seal.py`: its command name is the bare word `seal`, which every document in this repository contains | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:124` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Executed** 2026-09-14: `reachable` answers true for `seal.py` against three documents that never name it, and against a synthetic line carrying no locator. No document names `seal.py` today, so no case is wrong — the case is unfalsifiable, which is what Q1's general form was chosen to prevent |
| 🟡 2 | The class pin asserts the file and the twin and not the executable bit, where `plan.md` says it generalises the four-assertion form | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:211` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Executed** 2026-09-14: `X_OK` is asserted in four modules, each for its own wrapper; eight of the twelve pairs have nobody asking. All twelve are `100755` today. `spec.md` §In item 4 asks only for a pair, so this is answerable with the spec |
| 🟡 3 | `NO_WRAPPER` claims `chain_check.py` is *invoked in none of them*; what is asserted is *followed by a flag in none of them*, and `templates/config.md` lists it beside three bare commands | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` · `templates/config.md:165` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Executed** 2026-09-14: every line of a shipped document naming `chain_check.py` printed and read; `templates/config.md:165` is a four-item list of checks the sealer runs, three typeable and one not, and `command_forms` cannot see it. Narrowing the sentence is in scope; adding the path to that line is the user-facing change `spec.md` §Out refused |
| 🟡 4 | `agents/warden.md` names the generator at line 138 and says where it is at 186 — two mentions and 48 lines later, in the file the incident's three `warden` segments were reading | `agents/warden.md:138` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Executed** 2026-09-14: mention lines are 138, 182, 186, 290, 350, 379; the locator is at 186. `questions.md` Q4 answers *beside its first mention*, and `phases/phase-3.md` records the placement as *one sentence later*, which is true of the other two files and not of this one. `spec.md`'s stated property (at least once) is met |
| 🟡 5 | *The generator both rows name* — one row of that table names the generator, not two | `skills/implement/SKILL.md:521` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Read** 2026-09-14: the table has three rows; `round-N.md` names the generator twice and the other two name the review orchestrator. The locator in the same sentence is correct, so nothing breaks |
| ⬜ 6 | *All three places that DO invoke it* undercounts: `skills/verify/scripts/broad_gate.py` and `skills/code-review/scripts/round_record.py` also invoke `chain_check.py` | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | **fixed** `5a8f6ac` | fixed at 5a8f6ac; **Executed** 2026-09-14: `git grep chain_check` over the tree outside `tests/` and `seal/`. Both carry the full path, so *reachable everywhere it is reached* holds and only the count is wrong |
| ⬜ 7 | Eleven `seal/ledger.md` rows were re-read and re-stamped and their `Checked` dates did not move | `seal/ledger.md` | answered | Disclosed in `overview.md` §Not done, measured there, and filed as #387. Its location is the shared ledger, so `agents/warden.md` §Role puts it outside `Needs a fix` |

## Paste-ready fixes

```python
    command = command_name(script)
    # A command name with no hyphen in it is an ordinary English word --
    # `seal.py` answers to `seal` -- and this repository's prose is full of
    # it, so the bare-word form cannot tell a locator from a sentence. Those
    # scripts are reachable by path only, which is a reader that can fail.
    if "-" not in command:
        return script in text
    typed = re.search(rf"(?<![\w-]){re.escape(command)}(?![\w-])", text) is not None
    return typed or script in text
```
```python
def test_a_one_word_command_name_is_not_a_locator():
    """`seal.py` answers to `seal`, and every document in this repository
    contains that word. Read as a locator it makes the rule unfalsifiable for
    that script, which is the one thing Q1's general form was chosen to
    prevent."""
    seal = "skills/implement/scripts/seal.py"
    assert not reachable("The sealer takes the seal after the rounds.", seal)
    assert reachable("It lives at `skills/implement/scripts/seal.py`.", seal)
```
```python
    assert os.access(posix, os.X_OK), (
        f"`bin/{command}` ships without its executable bit, so the command "
        "resolves on PATH and then refuses. The form this generalises -- "
        "`tests/test_unverified_rows_close.py::test_the_wrapper_is_present_"
        "and_executable` -- asks for file, twin, exec bit and target"
    )
```
```python
        "Named in four shipped documents and shown with a flag in none of "
        "them -- which is what `test_an_unwrapped_script_is_shown_in_no_"
        "command_form` asserts, and the whole of it. A flag is the only "
        "sound tell in prose, so a bare mention in a list of checks is not "
        "caught: `templates/config.md` names it beside three commands. "
```
```markdown
(`evidence-check`, `unverified-check`,
`skills/code-review/scripts/chain_check.py`, `survivor-check`)
```
```markdown
  `round_record.py new` copies it into the row of the same name in
  `round-N.md` — that generator is
  `skills/code-review/scripts/round_record.py`, typed as `round-record`. An
  answer the report format has no field for is a decision
```
```markdown
The generator that row names is `skills/code-review/scripts/round_record.py`,
and the review orchestrator types it as `round-record`.
```
```python
        "Every place that invokes it carries its full path -- "
        "`.github/workflows/hygiene.yml`, `templates/hygiene.yml` and "
        "`docs/release-checklist.md` by hand, and "
        "`skills/verify/scripts/broad_gate.py` and this skill's own "
        "`round_record.py` in code -- so it is reachable everywhere it is "
        "reached. "
```

## Executed probes

| What was run | Result |
|---|---|
| `reachable` from the new pin, applied to each of the nine documents as they stand at `release/v0.11.4` | false for all nine — the pin was red against every document before the sweep, independently of the branch's own account |
| `seal/ledger.md` at the base and at HEAD, every eight-hex anchor hash normalised to one constant, compared | byte-identical; 2110 lines both sides, 11 differing lines, exactly one hash change each, 7 distinct anchors |
| every line of every `.md` under `agents/`, `skills/`, `templates/` matched against `round_record.py` followed by whitespace and a dash | no hits — no typed form of the old spelling survives the respelling |
| the pin's two enumerations, printed | 12 scripts (11 wrapped, `chain_check.py` not), 43 documents, 13 wrapped document/script pairs, 4 unwrapped; all 13 carry both accepted forms |
| `reachable` for `skills/implement/scripts/seal.py` against three documents that do not name it, and against a synthetic line with no locator | true in all four — finding 🟡 1 |
| the same with the hyphen guard of paste-ready fix 1 applied | all 13 real pairs still green, synthetic `seal.py` line red |
| `git ls-tree HEAD bin/` | all twelve POSIX wrappers `100755`, all twelve twins `100644`; nothing is broken today |
| `pytest tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` in a clone at `8208928` | exit 0, 75 passed — three gates the orchestrator did not run that the branch's new prose and the new `bin/` pair could have turned red |
| the broad gate — the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's single act under `skills/agent-contract/SKILL.md` §2 and no segment here has taken it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
