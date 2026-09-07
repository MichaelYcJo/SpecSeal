# Round 2 — the verifying round, review report

| Field | Value |
|---|---|
| Work item | `1788789330-the-update-notice-names-the-expensive-move` (#134) |
| Branch | `docs/134-the-update-notice-names-the-expensive-move` |
| Target SHA | `279628beaf6759a61320ea79148cfdabe5ac6f1f` — unmoved, tree clean at report time |
| Diff reviewed | `d36735e..279628b` — round 1's three fix commits |
| Prior rounds | round 1 at `d36735e`; its fix pass at `round-1-fixes.md` |
| Broad gate | not yet. Full suite, repository-wide lint and typecheck are the orchestrator's, `agent-contract` §2 |

## What this round was asked

Verify round 1's fixes rather than re-read the branch. Three attacks were named:
whether the fix pass's own re-enumeration closed its class, whether the Korean
paragraph whose scope arrived one sentence late has siblings, and whether the
notice now names the cheap move against what this repository actually measured.

## The shape of what follows

Round 1 found that a claim was held up by the presence of a word rather than by
what the sentence said. The fix pass answered all seven findings and then went
looking for the same property elsewhere, which is the right move and is where
four of its five extra surfaces came from. Two things survived it.

1. Rewriting the two by-hand code comments left both of them pointing the wrong
   way. The instruction they now defer to is above them, and they say *below*.
2. Rewriting the case moved the word-presence problem down one level rather than
   removing it. Two mutations carry every word the new assertions look for and
   still tell a user the reload picks up the new install. Both are green.

The third item is a leftover: one of round 1's three counts under finding 3 was
never answered, and the fix record calls that finding fixed without saying so.

## Round 1's seven, and where they stand

| # | Round 1's finding | This round |
|---|---|---|
| 1 | The notice sells the reload as the way to load the new release | **closed.** [executed] The scope qualifier now sits inside the claim's own sentence at `hooks/version-check.py:154-157`, `skills/update/SKILL.md:135-136`, `README.md:314-315` and `README.ko.md:305-306`. `bin/test tests/test_version_check.py …` → `48 passed`, exit 0 |
| 2 | The pinned case passes wording, not meaning | **partly closed** — see finding 2 below. Round 1's own two survivors are dead; two new ones of the same class are alive |
| 3 | The banner grew 391 → 707 characters | **closed on length, one count open.** [executed] `notice((0,7,1),(0,8,0))` → 620 characters, lines `[53, 107, 197, 260]`, matching the fix record exactly. The `README.md:182` count is finding 3 below |
| 4 | `spec.md`'s enumeration arithmetic | **closed.** [executed] Re-derived at `86e140f`: 33 `restart` + 3 `재시작` + 2 `reload` less the one `docs/flow.md:74` overlap = **37**, and the table's 15 in-class coordinates are exactly the 15 lines left after rows 16, 18, 20, 21, 22 and 23 take 1 + 1 + 12 + 1 + 6 + 1 = 22 |
| 5 | `0.5.0` named as run 6's version | **closed.** [read] `seal/specs/1788433011-…/questions.md:15` does name that path as the copy the sentinel was planted in, and `overview.md:19` now states the inference from §*Method* and §*What it established* instead of from the number |
| 6 | `hooks/ledger-migrate.py:4` | **closed as recorded.** Leaving it is what the finding asked for |
| 7 | 하십시오체 in `README.ko.md` | **closed.** [executed] `grep -c '하십시오' README.ko.md` → 0 |

## Findings

### 1 🟡 The by-hand block now tells the reader to look below, and what it points at is above

`README.md:325` and `README.ko.md:317`, both written by `591a801`.

```
321  By hand:
322
323  ```bash
324  claude plugin marketplace update specseal
325  claude plugin update specseal@specseal   # then load it — see below
326  ```
327
328  Both lines, in that order. The first refreshes the marketplace clone; the
329  second installs from it. …
```

The paragraph that says how to load it is at `README.md:314-319`, four lines
above the fenced block. What is below is the paragraph about command order and
`plugin.json` versions, which says nothing about loading. The Korean edition is
identical in shape: `README.ko.md:317` says `아래 참고`, and the paragraph it
means is at `:305-311`.

The fix record knows this. `changelog.md:35` describes the two comments as
*"as much an instruction as the paragraph above them."* The direction word in
the comments is the one thing that did not follow that sentence.

What it costs: the comment used to be `# then /reload-plugins, or restart`,
which was wrong in the way round 1 found but at least self-contained. A reader
who copies the by-hand block now gets a pointer at a paragraph that does not
answer it, so the shorter path through the README ends with the user knowing
they must load it and not knowing how.

### 2 🟡 The rewritten case pins words one level down, and two mutations that hand the third axis back are green

`tests/test_version_check.py:92-131`.

The new assertions do close round 1's two survivors. What they do not close is
the class round 1 named: *a required phrase cannot see a clause that was added.*
Each of the three unmeasured axes is now pinned by its own word appearing
somewhere in the gap sentence, and one negation word anywhere in that same
sentence stands for all three.

I ran the shipped assertion body verbatim against two mutations
(`tests/test_tmp_round2_gap_mutations.py`, deleted). **Both survived.**

- **M6 — the negation is left standing for two axes and an adversative hands
  back the third.** *"Whether it reaches hooks or agent definitions is
  unmeasured, **but the version you just installed is picked up**, so restart
  only for those."* The gap sentence carries `hooks`, `agent definitions`,
  `installed` and `unmeasured`, so every assertion passes.
- **M7 — the reload's own claim keeps its subject and its scope and gains a
  false clause.** *"…out of the copy you are already on **and out of the one
  you just installed**."* `measured`, `skill bodies` and `already on` are all
  present, so the claim passes.

M6 is the sharper one. It is round 1's M2 written as a positive claim instead of
a deletion, and a positive claim is the failure this branch exists to prevent:
`overview.md` §*Where spec and implementation diverged* records the third axis as
the branch's own correction of the ticket, and `skills/update/SKILL.md:96-98`
says a user told the reload covers everything gets a half-loaded plugin with no
way to tell. M6 is that sentence, and the case is green against it.

Controls behaved. Dropping the scope qualifier and deleting the third axis were
both killed.

The new unit `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`
inherits the same shape. Its docstring says a notice selling the reload as the
way to load the new version contradicts the file it lives in, but what it
asserts is that a scope phrase is *present* — never that a new-install claim is
*absent*. M7 passes it too.

### 3 ⬜ The README still calls the banner one line, and the fix record does not say the count is open

`README.md:182` — *"when the running plugin is behind, shows **one line** naming
`/specseal:update`."* The notice is four lines and 620 characters.

Round 1 raised this as one of three counts under finding 3. The fix record's row
for finding 3 answers only the length and reads `fixed`. The line predates the
branch — the notice at `86e140f` was already four lines — so nothing here got
worse, and the Korean edition never carried the claim (`README.ko.md:178` says
only that the hook tells you about `/specseal:update`). What is worth
correcting is the record: a finding closed on two of its three counts is not a
finding closed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The by-hand comment points below at an instruction that is above, in both editions | `README.md:325` | open | Read. The load paragraph is at `README.md:314-319` and `README.ko.md:305-311`, above the fenced block in both; `changelog.md:35` calls it *the paragraph above them*. Sibling: `README.ko.md:317` |
| 2 | The rewritten case pins each axis by word presence, so a positive claim about the third axis and a false clause in the reload's own sentence both stay green | `tests/test_version_check.py:117` | open | Executed. M6 and M7 survived the shipped assertion body; the scope-dropped and axis-deleted controls were killed. The proposed addition kills all four |
| 3 | `README.md:182` still describes the banner as one line; it is four. Round 1's finding 3 is recorded `fixed` on two of its three counts | `README.md:182` | open | Read. `notice((0,7,1),(0,8,0))` returns 4 lines; the same claim is absent from `README.ko.md:178`; pre-existing at `86e140f` |
| 4 | The notice's scope qualifier, in every user-facing surface | `hooks/version-check.py:154` | answered | Executed. Round 1's finding 1 is closed — the qualifier is inside the claim's sentence in all four surfaces, and the two that already had it are unchanged |
| 5 | `spec.md`'s enumeration arithmetic | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | answered | Executed. 37 lines re-derived at `86e140f`; 15 in class and 22 out reconcile row by row against the table as it now stands |
| 6 | The banner's length against `plan.md`'s short form | `hooks/version-check.py:148` | answered | Executed. 620 characters, lines `[53, 107, 197, 260]` — the fix record's figures are exact |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_round2_gap_mutations.py -q` — the shipped case's assertion body verbatim against two new mutations and two controls | exit 1, `2 failed, 3 passed`. **M6 (third axis handed back after an adversative) and M7 (false clause added to the reload's own claim) SURVIVED.** Controls killed: scope qualifier dropped, third axis deleted. Sanity case on the real notice green. Probe deleted |
| `bin/test tests/test_tmp_round2_proposed_pin.py -q` — the same body plus the addition in the paste-ready fix below | exit 1, `4 failed, 1 passed`. All four mutations killed — M6 on the adversative assertion (`:48`), M7 on the unmeasured-pairing assertion (`:41`) — and the shipped notice still passes. Probe deleted |
| `bin/test tests/test_version_check.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | exit 0, `48 passed` |
| `python3 -c` calling `notice((0,7,1),(0,8,0))` on the module at `279628b` | 620 characters, 4 lines, `[53, 107, 197, 260]` |
| `git grep -ciI 'restart' 86e140f` · `git grep -nI '재시작' 86e140f` · `git grep -niI 'reload' 86e140f \| grep -vi preload`, deduplicated by `file:line` | 33 · 3 · 2 → **37 distinct**. All three 재시작 hits are in `README.ko.md`; the experiment's Korean edition is removed by `grep -vi preload`, which is what `spec.md` row 19 claims |
| `bin/evidence-check .` | exit 0. `seal/ledger/1788789330-….md` → `12 ok · 0 drifted · 0 broken`. The fix pass's recomputed anchors are current |
| `uvx ruff check` · `uvx ruff format --check` on `hooks/version-check.py` and `tests/test_version_check.py` | exit 0, `All checks passed!`, `2 files already formatted`. The two changed Python files only — not a repository-wide lint |
| `grep -c '하십시오' README.ko.md` · `git grep -nI 'see below' README.md` · `git grep -nI '아래 참고' README.ko.md` | 0 · `README.md:325` · `README.ko.md:317` |
| `git rev-parse HEAD` · `git status --porcelain` | `279628beaf6759a61320ea79148cfdabe5ac6f1f`, tree clean before and after the probes |

Read, not run: that the four surviving unscoped `/reload-plugins` runs are
correctly out of the class. I re-derived the ten runs at HEAD outside `seal/`,
`tests/` and `CHANGELOG.md` and agree with the fix record's placement of each —
the two editions of the experiment record state the measurement, and
`skills/update/SKILL.md:103` and `:110` describe a run to perform and a command
the procedure will not type.

❓ out of verified scope: the full suite, the repository-wide lint and the
typecheck. `agent-contract` §2 reserves the broad gate to the orchestrator and my
prompt did not order one. **The orchestrator answers it.**

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md` §5 | the repository owner |
| How the four-line `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships |
| The `141 cases` figure in `round-1-fixes.md` — an aggregate rather than a coordinate, so `agent-contract` §5 says it is a claim nobody has opened. The class boundary it rests on (evidential claim against diagnostic output) is a judgment, not a count | round 1's fix record | the orchestrator. Nothing in this round turns on it |

## Paste-ready fixes

**Finding 1 — `README.md:325`.** Two words. The pointer stays; only its
direction changes.

```bash
claude plugin update specseal@specseal   # then load it — see above
```

**Finding 1 — `README.ko.md:317`.** The mirror.

```bash
claude plugin update specseal@specseal   # 그다음 적용 — 위 문단 참고
```

**Finding 2 — `tests/test_version_check.py`.** Append to
`test_the_warning_names_the_cheap_move_before_the_expensive_one`, after the
negation assertion at `:126-129`. Run against M6, M7 and both controls: all four
killed, and the shipped notice still passes.

```python
    # A required phrase cannot see an ADDED clause. Round 2 ran the assertions
    # above against two mutations that carry every word they look for and still
    # tell a user the reload picks up the new install:
    #   the reload's claim + `and out of the one you just installed`
    #   the gap: `hooks or agent definitions is unmeasured, BUT the version you
    #            just installed is picked up`
    # Both were green. So pin the negative too: wherever a sentence puts the
    # reload beside the newly installed version, the negation has to govern the
    # whole sentence rather than the clause before the comma.
    for where, sentence in (("the reload's claim", reload_claim), ("the gap", gap)):
        if "install" not in sentence:
            continue
        assert any(
            negation in sentence
            for negation in ("nobody", "not measured", "unmeasured", "no one")
        ), (
            f"{where} names the newly installed version without saying that "
            "pairing is unmeasured, which is the claim run 6 does not support"
        )
        assert not any(
            adversative in sentence
            for adversative in (" but ", " however", " though ", " except ")
        ), (
            f"{where} carries an adversative after its negation, so the "
            "negation governs only part of the sentence and the clause after "
            "it hands an axis back as a positive claim"
        )
```

**Finding 3 — `README.md:182`.** Replaces `shows one line naming` in the
version-check row.

```
shows a short notice naming `/specseal:update` and the two moves that load a release
```

## Regression tests to plant

None beyond finding 2's addition. It is the case that already exists, extended;
planting a second case for the same message would give two places to edit when
the wording moves.

## Facts for the evidence ledger

The fragment's row for S1 · S2 · S3 records *"Five mutations, five killed."* That
is true of the five the fix pass chose and is not true of the class. Add, in the
Notes column of that row, that a required-phrase assertion cannot detect an added
clause, with M6 and M7 named — otherwise the next reader takes the mutation count
as evidence the claim is pinned.

Needs a fix: yes — findings 1 and 2
Loses a record or crashes: no

Nothing found here leaves a record outside the root and nothing crashes. Finding
1 is a README comment and finding 2 is a test that passes when it should fail;
neither touches the record path.

## Contract changes and new units, for the fixes' diff

**Contract changes: none.** `notice(have, want)` keeps its signature and its
callers. What changed is the string it returns, which is a surface a person
reads — `agent-contract` §14 asks that it be documented and pinned, and it is,
in `changelog.md`, the ledger fragment and two cases.

**New units: one.**
`tests/test_version_check.py::test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`.
Judged as code rather than as a fix, per the verifying round's own rule. It
runs, it is correctly whitespace-normalised against the hand-wrapped docstring,
and its failure messages name the reason. Its weakness is finding 2's: it
asserts a scope phrase is present and never that a new-install claim is absent,
so M7 passes it as well. Nothing in it needs its own fix once finding 2's
addition lands.

`seal/specs/1788789330-…/rounds/round-1-fixes.md` is new but is a record, not a
unit. Two ledger rows were added to the fragment and `bin/evidence-check`
reports all twelve anchors current.

## Proof block

Files opened at `279628b`:

- `git diff d36735e..279628b` in full
- `hooks/version-check.py:1-45`, `:135-170`
- `tests/test_version_check.py:1-40`, `:60-160`
- `skills/update/SKILL.md:1-140`
- `README.md:176-190`, `:300-340`
- `README.ko.md:172-186`, `:292-330`
- `seal/specs/1788789330-…/spec.md:38-115`, `rounds/round-1.md`,
  `rounds/round-1-report.md`, `rounds/round-1-fixes.md` (whole)
- `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` (whole,
  via the diff)
- `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/questions.md:15`
- `bin/test`, `bin/evidence-check`
- `hooks/version-check.py` at `86e140f`, `notice()` only

Written and deleted: `tests/test_tmp_round2_gap_mutations.py`,
`tests/test_tmp_round2_proposed_pin.py`. The `.venv` `bin/test` builds was
removed with them; the tree is clean.
