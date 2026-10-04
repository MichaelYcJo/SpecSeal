# Round 1 report — every rule CLAUDE.md restates has one home (#730)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | f7e82f09 |
| Base | `release/v0.18.1` at edee5ca2 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the branch at the target, in the session scratchpad; the worktree was read and not written, apart from this file |

## What the account asserted, and what the code showed

The spawn prompt, `overview.md`, `phases/phase-2.md`, `survivors.md` and the
ledger fragment were read in full and checked against the tree.

- **Claimed: each `CLAUDE.md` link row carries the home's path and section,
  the trigger, and the act with its values (spec D2).** Confirmed by reading.
  The merge row says a pull request into `release/vX.Y.Z` is squashed and one
  into `main` takes a merge commit. That matches all four pull-request rows of
  the home's *Which button* table, the release-prep and hotfix rows included,
  which the old copy had lost. The identifiers row carries `example.com` and
  `/Users/x/`. The commit row names both of step 2's conditions and says both
  hold here. The goal paragraph folds the batch sentence into its link to
  step 1. None of the rows carries a table, an incident or reasoning.
- **Claimed: each home holds everything the removed copy said.** Confirmed
  by reading. `docs/branch-and-release.md` §*Work accumulates on a release
  branch* holds the six-row table, the rider-stamp incident in its corrected
  form, both rulesets and the release-prep pull request. `CONTRIBUTING.md`
  §*House rules* now carries the history-rewrite reason. Step 2 of
  `skills/implement/SKILL.md` carries the squash condition, the declaration
  condition, the `Target SHA` reason and the worktree-guard reason. Step 1
  carries the one-batch rule and the mid-run cost.
- **Claimed: the four code comments were every citation of `CLAUDE.md` for
  the identifiers rule (spec Scope 2, S5).** Not so. The enumerating grep was
  `real identifier`, and a fifth citation spells it `no-real-identifiers`
  (finding 2).
- **Claimed: the ratchet reads every tracked `*.md` under `templates/`, and
  drops `CLAUDE.md`'s generated region (module docstring, spec D5, ledger
  O3, changelog fragment).** Not so for one file. The region is dropped from
  every file that carries the markers, and `templates/claude-md-block.md` is
  nothing but that region, so the ratchet reads 0 of its 767 words
  (finding 1).
- **Claimed: `BASELINE` is the measured state, 68 files, 188,585 words and
  103 pairs (ledger O4).** Confirmed by execution: the module's own
  `shared_counts` equals `BASELINE` exactly, in both directions. The record's
  *2,091 distinct runs* is a different number from the one it names
  (finding 4).
- **Claimed: #757's E5 row was re-stamped in place in #757's fragment.**
  Confirmed, and it is the documented repair. `docs/the-evidence-ledger.md`
  §*A released row is read again in the branch's fragment* says that a
  citation into a fragment is refused and that the fragment's row is
  re-stamped in place instead. The claim still holds: the encoding bullet in
  §*House rules* states all four things E5 lists. `evidence-check --strict`
  does not name E5.
- **Claimed: the census entry for the ratchet's `corpus` is honest.**
  Confirmed by reading. The `on_disk` docstring in `tests/conftest.py` says
  that a positive sweep judges what remains and ignores the missing half. The
  ratchet is that kind of sweep, and `test_the_corpus_is_found` is its
  liveness floor.

## Findings from reading and execution

### 🟡 1 — The ratchet never reads the template `install.sh` distributes

`tests/test_no_passage_is_pasted_into_a_second_file.py:105`, in `words`.

`GENERATED.sub` runs on every corpus file, not only on `CLAUDE.md`. The
template `templates/claude-md-block.md` opens with the start marker and ends
with the end marker, so the whole file normalises to zero words.

- **Executed:** 30 words of `CONTRIBUTING.md` pasted inside the template's
  region were named by nothing. The same paste appended to
  `templates/sdd-spec.md` was named.
- **Why it matters:** this is the block every user's `CLAUDE.md` receives.
  It is the corpus file a paste reaches furthest from. The module docstring,
  spec D5, ledger O3 and the changelog fragment all say only `CLAUDE.md`'s
  copy is dropped. So the check is blind to one of the files it claims to
  read, and nothing says so.
- **A second cost:** the same regex runs over prose that quotes the markers.
  Two files do today, `skills/update/SKILL.md` and
  `skills/preset-setup/SKILL.md`. Both quote the pair on one line, so they
  lose only a few words. A document that quoted the start marker in one
  paragraph and the end marker further down would lose everything between
  them.
- **Measured effect of the fix:** limiting the drop to `CLAUDE.md` adds one
  pair, `agents/smith.md` with the template at 13. That pair belongs in
  `BASELINE`, as debt or as sanctioned under spec O1. The fix below records
  it as measured. With the fix applied in the scratch clone, the ratchet and
  the census modules pass (25 passed), and ruff check and ruff format are
  clean. The new case is red against the target (the first probe above).

### 🟡 2 — A fifth citation still sends the identifiers rule to `CLAUDE.md`

`agents/warden.md:404`: *The no-real-identifiers rule (`CLAUDE.md`) is
enforced over every tracked file*.

Spec Scope 2 says four comments cite `CLAUDE.md` for this rule. S5 says that
afterwards none does. The four came from `git grep -n -i 'real identifier'`,
which cannot match the hyphenated spelling. Contract §12 asks for the class
to be enumerated, not the instances the first search found.

- **Why it matters:** `CLAUDE.md` is now a link row. This sentence names as
  the rule's place a file that no longer holds the rule.
- **Why `LINKED` cannot catch it:** the pin module's `LINKED` covers only the
  four found citations, so the fifth can never turn it red.
- **Who reads it:** the sentence sits in the warden's *Report* section, where
  a reviewer is told the rule applies to its own prose.

A grep for `real.identifier` over the tree outside `seal/` and
`CHANGELOG.md` finds no other citation.

- **Executed:** with the fix below applied in the scratch clone, 117 passed
  across the pin module, the ratchet, the reviewer-report module, the
  contract-preamble module, the wrap module, the identifiers module and the
  one-word module.
- **Seen red:** `unlinked` over the target's `agents/warden.md` returns
  `[('agents/warden.md', 'identifiers')]`, so the new `LINKED` row fails
  without the repointed sentence.

### ⬜ 3 — A comment quotes a `CLAUDE.md` line this branch removed

`tests/test_chain_hooks_hardening.py:917` cites *go in **one batch** before
the first edit* as `` `CLAUDE.md:39` verbatim ``. At the base, line 39 was
that sentence, already with different emphasis. At the target, line 39 is the
link paragraph, and the sentence is gone from `CLAUDE.md`. The comment
records a spelling #422 measured, and the case it explains (`BATCH_PHRASE`)
does not depend on it. So this is a stale coordinate a reader cannot follow,
not a defect. Saying *`CLAUDE.md`'s goal section before #730* instead of the
line number would keep it true.

### ⬜ 4 — The record calls a per-pair sum "distinct runs" (correction)

`seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:10`,
row O4, says *103 pairs sharing 2,091 distinct 15-word runs*.
`phases/phase-2.md`, `questions.md` Q1 and the `overview.md` divergence table
use the same wording.

- **Executed:** 2,091 is the sum of the per-pair counts. The tree holds
  1,197 distinct 15-word windows shared by two or more files, because a
  window shared by three files is counted in three pairs. The table and the
  check are right. Only the sentence in the records misnames the number.
- **Answer:** this is paperwork under `seal/`, so it is a correction and not
  a fix. *the pairs' counts sum to 2,091* is the accurate wording, and the
  phase 1 figure of 2,064 needs the same change.

## Regression tests to plant

- `tests/test_no_passage_is_pasted_into_a_second_file.py`: a paste inside the
  template's region is named, and the generated-region case shows the
  template's region being read. Both are in the fix for 🟡 1.
- `tests/test_the_rules_claude_md_names_have_one_home.py`: `agents/warden.md`
  in `LINKED` and `CARRIERS`, which is the fix for 🟡 2.

## Facts for the evidence ledger

- O3 names `words` and the generated-region case. The fix for 🟡 1 moves the
  drop from `words` into a new helper that `tree` calls, so O3's coordinates
  drift, and its wording *drops `CLAUDE.md`'s generated region* becomes true
  as written. O4 gains the new pair.
- O1's coordinates on `LINKED` and `CARRIERS` drift with the fix for 🟡 2,
  and its wording *the four code comments* gains the warden sentence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The ratchet drops every file's generated region, so `templates/claude-md-block.md` is read as zero words and a paste into it is named by nothing | `tests/test_no_passage_is_pasted_into_a_second_file.py:105` | open | Executed: 0 of 767 words read; a 30-word paste inside the region named nothing, the same paste into `templates/sdd-spec.md` was named. Docstring, spec D5, ledger O3 and the changelog fragment say only `CLAUDE.md`'s copy is dropped |
| 🟡 2 | A fifth citation names `CLAUDE.md` as the identifiers rule's place, and `LINKED` does not hold it | `agents/warden.md:404` | open | Spec Scope 2 and S5. The enumerating grep `real identifier` cannot match `no-real-identifiers`. Executed: the fix passes 117 cases, and `unlinked` names the target's sentence |
| ⬜ 3 | A comment cites `CLAUDE.md:39` verbatim for a sentence this branch removed | `tests/test_chain_hooks_hardening.py:917` | open | Read: line 39 at the base was the batch sentence, and at the target it is the link paragraph. The case does not depend on it |
| ⬜ 4 | The records call 2,091 *distinct runs* when it is the sum of per-pair counts; 1,197 distinct windows are shared | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:10` | open | Executed. A correction to the run's paperwork, which `Needs a fix` does not count. The same wording is in `phases/phase-2.md`, `questions.md` Q1 and `overview.md` |
| 🟢 | The four `CLAUDE.md` link rows carry path and section, trigger and act with its values, and no table, incident or reasoning | `CLAUDE.md:40` | confirmed | Read against spec D2 and the four homes; the merge act matches all four pull-request rows of the home's table |
| 🟢 | Each home holds everything its removed copy said, and the identifiers home gained the history-rewrite reason | `CONTRIBUTING.md:265` | confirmed | Read: the merge home, §*House rules*, and steps 1 and 2 of `skills/implement/SKILL.md` |
| 🟢 | The ratchet names a paste and passes the measured debt: `BASELINE` equals the module's own counts in both directions | `tests/test_no_passage_is_pasted_into_a_second_file.py:193` | confirmed | Executed in the scratch clone: 68 files, 188,585 words, 103 pairs; a planted paste into `templates/sdd-spec.md` was named |
| 🟢 | #757's E5 row re-stamped in place in #757's fragment is the documented repair, and its claim holds | `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md:79` | confirmed | `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: re-stamp a fragment's row in place. Executed: `evidence-check --strict` does not name E5 |
| 🟢 | The census classifies the ratchet's `corpus` as a positive sweep that skips the missing half | `tests/test_a_shrunken_corpus_declines_to_judge.py:174` | confirmed | Read against the `on_disk` docstring; executed: the census module passed |
| ❓ | Whether the claims of three of the five `Re-read ·` rows still hold against §*House rules* | `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md:13` | ❓ out of verified scope | Two rows were read against the current sections (the conflict-rule correction and C5). The two other `Corrected ·` rows and the 0.4.0 row were not. The smith's reading is the record; the orchestrator answers whether a second reading is wanted |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

In `tests/test_no_passage_is_pasted_into_a_second_file.py`, delete the first
statement of `words`, the line that applies `GENERATED.sub` to `text`. Then
replace `tree` with these two functions:

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

Add to `BASELINE`, after the `("agents/smith.md", "skills/implement/orchestration.md")` entry:

```python
    ("agents/smith.md", "templates/claude-md-block.md"): 13,
```

In `test_the_generated_block_fences_and_headings_are_not_read`, replace the
`for skipped in …` loop with:

```python
    for skipped in (fenced, readable("CLAUDE.md", block), heading):
        assert not shared_counts({"a.md": skipped, "b.md": run}), skipped
    # The template the region is generated from is read: its markers are
    # not a licence anywhere but in `CLAUDE.md`.
    template = readable("templates/claude-md-block.md", block)
    assert shared_counts({"a.md": template, "b.md": run}) == {("a.md", "b.md"): 1}
```

And add the case:

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

### 🟡 2

In `agents/warden.md`, the paragraph under *Once the orchestrator commits it
the report is tracked content*:

```markdown
The no-real-identifiers rule (`CONTRIBUTING.md` §*House rules*) is enforced
over every tracked file, and §8 of the contract is what told you to write your
clone's absolute path out. So the probe row that records the command you ran
is the row that turns `tests/test_no_real_identifiers.py` red at the pull
request, after your round has ended and where nobody can ask you what you
meant. Name paths relative to the repository root, and spell a user path
`/Users/x/`.
```

In `tests/test_the_rules_claude_md_names_have_one_home.py`, add as the last
entry of `LINKED`:

```python
    # The fifth citation, spelled `no-real-identifiers`, which the
    # enumerating grep's `real identifier` did not match (round 1).
    "agents/warden.md": ("identifiers",),
```

and as the last entry of `CARRIERS`:

```python
    "agents/warden.md",
```

Needs a fix: yes — 🟡 1, the ratchet reads none of `templates/claude-md-block.md`; 🟡 2, `agents/warden.md` still cites `CLAUDE.md` for the identifiers rule
Loses a record or crashes: no

## Proof block

Files opened: `CLAUDE.md`, `CONTRIBUTING.md` (§*House rules*, §*Running the
checks*), `docs/branch-and-release.md` (§*Work accumulates on a release
branch*), `docs/the-record-layout.md` (diff), `docs/the-evidence-ledger.md`
(§*A released row is read again in the branch's fragment*),
`skills/implement/SKILL.md` (steps 1 and 2), `agents/warden.md` (lines
398–412), `agents/smith.md` (lines 403–416),
`tests/test_no_passage_is_pasted_into_a_second_file.py`,
`tests/test_the_rules_claude_md_names_have_one_home.py`,
`tests/test_a_shrunken_corpus_declines_to_judge.py` (lines 140–175),
`tests/conftest.py` (`git_listing`, `on_disk`),
`tests/test_chain_hooks_hardening.py` (lines 895–960),
`tests/test_the_reviewers_report_reaches_the_record.py` (lines 305–345),
the four repointed comments (diff), both ledger fragments (diff), and
`seal/releases/0.18.0.md` and `seal/releases/0.4.0.md` (the cited rows);
the work item's `spec.md`, `questions.md`, `survivors.md`, `overview.md`,
`changelog.md` and `phases/phase-2.md`.
