# 1791076836-every-rule-claude-md-restates-has-one-home — review round 1

| Field | Value |
|---|---|
| Target SHA | f7e82f09552474ea4255852b4f35d55910e388e9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #767 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `8a0e440b2c210f141ed19829d4fd689ac68ad98e..0be7deb4132436ee7eb928165099579a4d2c81f8`, 6 commits |
| Contract changes | none |
| New units | test_a_paste_into_the_block_template_is_named (depth 1) |
| Needs a fix | yes — 🟡 1, the ratchet reads none of `templates/claude-md-block.md`; 🟡 2, `agents/warden.md` still cites `CLAUDE.md` for the identifiers rule |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item `1791076836-every-rule-claude-md-restates-has-one-home` (#730, PR #767). The target is `f7e82f09`, against `release/v0.18.1` at `edee5ca2`.

**Spec compliance (first).**
- Does each `CLAUDE.md` link row still carry what a session needs to act correctly without opening the home? `CLAUDE.md` is loaded into every session and the homes are not. That is the trade the frame's D2 states.
- Does each home now hold everything the `CLAUDE.md` copy said?
- Do the pins fail when the link or the home moves?
- Does the ratchet fail on a pasted copy and stay quiet on the measured debt?

**Quality (second).**
- Does the ratchet measure what it claims? Check normalisation, the window, the sanctioned preamble, and `on_disk`.
- The smith re-stamped #757's fragment row E5 in place after the merge. Judge that.

**Pre-verified by the orchestrator, at the target:** the changed and hygiene modules (308 passed), ruff on the changed Python files, and `claude_block.py --check`.

**Not this item's.** The release head carries 10 drifted rows from the wave-one squashes. #766 re-reads them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The ratchet drops every file's generated region, so `templates/claude-md-block.md` is read as zero words and a paste into it is named by nothing | `tests/test_no_passage_is_pasted_into_a_second_file.py:105` | **fixed** `f610089f` | fixed at f610089f — `d63e6e8e`; Executed: 0 of 767 words read; a 30-word paste inside the region named nothing, the same paste into `templates/sdd-spec.md` was named. Docstring, spec D5, ledger O3 and the changelog fragment say only `CLAUDE.md`'s copy is dropped |
| 🟡 2 | A fifth citation names `CLAUDE.md` as the identifiers rule's place, and `LINKED` does not hold it | `agents/warden.md:404` | **fixed** `211c492d` | fixed at 211c492d; Spec Scope 2 and S5. The enumerating grep `real identifier` cannot match `no-real-identifiers`. Executed: the fix passes 117 cases, and `unlinked` names the target's sentence |
| ⬜ 3 | A comment cites `CLAUDE.md:39` verbatim for a sentence this branch removed | `tests/test_chain_hooks_hardening.py:917` | **fixed** `b9025b17` | fixed at b9025b17; Read: line 39 at the base was the batch sentence, and at the target it is the link paragraph. The case does not depend on it |
| ⬜ 4 | The records call 2,091 *distinct runs* when it is the sum of per-pair counts; 1,197 distinct windows are shared | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:10` | answered | corrected at `b042462f`: ledger O4, `phase-2.md`, Q1 and the overview give the per-pair sum and the distinct 15-word windows apart, measured at three trees; Executed. A correction to the run's paperwork, which `Needs a fix` does not count. The same wording is in `phases/phase-2.md`, `questions.md` Q1 and `overview.md` |
| 🟢 | The four `CLAUDE.md` link rows carry path and section, trigger and act with its values, and no table, incident or reasoning | `CLAUDE.md:40` | confirmed | Read against spec D2 and the four homes; the merge act matches all four pull-request rows of the home's table |
| 🟢 | Each home holds everything its removed copy said, and the identifiers home gained the history-rewrite reason | `CONTRIBUTING.md:265` | confirmed | Read: the merge home, §*House rules*, and steps 1 and 2 of `skills/implement/SKILL.md` |
| 🟢 | The ratchet names a paste and passes the measured debt: `BASELINE` equals the module's own counts in both directions | `tests/test_no_passage_is_pasted_into_a_second_file.py:193` | confirmed | Executed in the scratch clone: 68 files, 188,585 words, 103 pairs; a planted paste into `templates/sdd-spec.md` was named |
| 🟢 | #757's E5 row re-stamped in place in #757's fragment is the documented repair, and its claim holds | `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md:79` | confirmed | `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: re-stamp a fragment's row in place. Executed: `evidence-check --strict` does not name E5 |
| 🟢 | The census classifies the ratchet's `corpus` as a positive sweep that skips the missing half | `tests/test_a_shrunken_corpus_declines_to_judge.py:174` | confirmed | Read against the `on_disk` docstring; executed: the census module passed |
| ❓ | Whether the claims of three of the five `Re-read ·` rows still hold against §*House rules* | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:13` | ❓ out of verified scope | Two rows were read against the current sections (the conflict-rule correction and C5). The two other `Corrected ·` rows and the 0.4.0 row were not. The smith's reading is the record; the orchestrator answers whether a second reading is wanted |

## Paste-ready fixes

```python
def readable(rel, text):
    """TEXT as the ratchet reads REL: `CLAUDE.md`'s generated region dropped.

    Only that copy is sanctioned (spec O1). The template it is generated from,
    `templates/claude-md-block.md`, carries the same markers and is a rule
    document like any other, so its region is read."""
    return GENERATED.sub("\n", text) if rel == "CLAUDE.md" else text


def tree():
    texts = {}
    for rel in corpus():
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            texts[rel] = readable(rel, f.read())
    return texts
```
```python
    ("agents/smith.md", "templates/claude-md-block.md"): 13,
```
```python
    for skipped in (fenced, readable("CLAUDE.md", block), heading):
        assert not shared_counts({"a.md": skipped, "b.md": run}), skipped
    # The template the region is generated from is read: its markers are
    # not a licence anywhere but in `CLAUDE.md`.
    template = readable("templates/claude-md-block.md", block)
    assert shared_counts({"a.md": template, "b.md": run}) == {("a.md", "b.md"): 1}
```
```python
def test_a_paste_into_the_block_template_is_named():
    """The block `install.sh` distributes is a rule document: a paste into
    it is named like a paste anywhere else, markers or not."""
    texts = tree()
    paste = a_sentence_of(texts["CONTRIBUTING.md"])
    rel = "templates/claude-md-block.md"
    planted = texts[rel].replace(
        "specseal:start -->", "specseal:start -->\n" + paste, 1
    )
    assert planted != texts[rel]
    texts[rel] = planted
    assert [f for f in over_baseline(texts, BASELINE) if rel in f]
```
```markdown
The no-real-identifiers rule (`CONTRIBUTING.md` §*House rules*) is enforced
over every tracked file, and §8 of the contract is what told you to write your
clone's absolute path out. So the probe row that records the command you ran
is the row that turns `tests/test_no_real_identifiers.py` red at the pull
request, after your round has ended and where nobody can ask you what you
meant. Name paths relative to the repository root, and spell a user path
`/Users/x/`.
```
```python
    # The fifth citation, spelled `no-real-identifiers`, which the
    # enumerating grep's `real identifier` did not match (round 1).
    "agents/warden.md": ("identifiers",),
```
```python
    "agents/warden.md",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the ratchet, the pin module, `tests/test_the_ledger_rules_have_one_home.py` and the census module, at f7e82f09 in the scratch clone | 34 passed |
| `evidence-check --strict --ledger` on #730's fragment | exit 0, 48 ok, 0 drifted |
| `evidence-check --strict --ledger` on #757's fragment | exit 2, one DRIFTED on `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv`, one of the release head's drifted rows that #766 re-reads; E5 not named |
| Probe: the template's words after the ratchet's normalisation | 0 of 767 |
| Probe: 30 words of `CONTRIBUTING.md` pasted inside the template's region, and the same paste into `templates/sdd-spec.md` | template: nothing named; `templates/sdd-spec.md`: named |
| Probe: the region dropped from `CLAUDE.md` only | one pair changes, `agents/smith.md` with the template, 0 to 13 |
| Probe: `shared_counts` against `BASELINE`, with the totals | equal both ways; 68 files, 188,585 words, 103 pairs, per-pair sum 2,091, 1,197 distinct shared windows |
| Probe: `SECTION` matches longer than 15 words | 7, each the one heading *Where a leftover goes*, wrapped |
| Fix 1 applied in the scratch clone: the ratchet and the census module, then ruff check and ruff format on the module | 25 passed; ruff clean |
| Fix 2 applied in the scratch clone with fix 1: the pin module, the ratchet, `tests/test_the_reviewers_report_reaches_the_record.py`, `tests/test_every_agent_reads_the_contract.py`, `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py` | 117 passed |
| `unlinked` with fix 2's `LINKED` over the target's `agents/warden.md` | `[('agents/warden.md', 'identifiers')]`, red as intended |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
