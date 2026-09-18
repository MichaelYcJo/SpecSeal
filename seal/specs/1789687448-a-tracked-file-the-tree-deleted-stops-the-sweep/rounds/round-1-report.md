# Round 1 — a tracked file the tree deleted stops the sweep

| Field | Value |
|---|---|
| Target SHA | `539d32df` |
| Base | `release/v0.12.1` at `5bf22ddb` |
| Reviewed in | a `git clone --no-local` at the target SHA; nothing was written in the working checkout but this report |

## How the findings relate

The branch decides one rule and applies it well in five places. Two findings
are that rule not reaching a sixth place, and both were reachable by running
something:

1. **The rule.** A sweep judges what remains; a check whose verdict needs the
   whole corpus declines and names the missing paths. Five modules follow it.
2. **The module written to close the class does not follow it.** Phase 4's
   reader holds two assertions that need the whole corpus, and neither
   declines. On a mid-edit tree it turns red and tells the reader to delete a
   live classification row.
3. **The record written about the one survivor silenced the check that
   reported it.** That is issue #365's class, one file over, and the tree
   still carries the work item that closed it for round records.
4. Beside those, one helper declines over one missing path and carries a real
   finding away with it, and the frame gained a paragraph whose author is the
   builder although the template gives that paragraph a home.

Everything else I opened held. The re-stamp of the shared ledger is correct
and I confirmed it by running the checker.

---

## 🔴 1 · The reader that closes the class goes red on the tree this work exists to survive

**Location** — `tests/test_a_shrunken_corpus_declines_to_judge.py:296`
(`suite_modules`), consumed at `:345`
(`test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`) and `:391`
(`test_the_reader_finds_the_helpers_this_work_guarded`).

`suite_modules` applies `on_disk` and throws the missing half away:

```python
    present, _ = on_disk(ROOT, out)
    return present
```

Both cases that consume it then assert that every scope in `PATH_LIST_CALLS`
is still found. That is a liveness assertion over a corpus built from a git
listing — the exact shape `spec.md` §*Is a skip a weakening* names, and the
exact shape `keep_entries_not_in_use` and `classifications_of_nothing` decline
for. Here nothing declines, so a module that is tracked and gone from disk
reads as a scope somebody removed.

**Executed.** With `tests/test_release_hygiene.py` removed from disk and the
removal unstaged, the module goes from `14 passed` at exit 0 to `2 failed, 12
passed` at exit 1, and the refusal reads:

```
the suite derives a path list from git in [] that this case does not account
for, and accounts for ['tests/test_release_hygiene.py#tracked'] that no longer
derives one. Classify the difference: it either applies `on_disk`, or it
belongs in one of the five tables above with the grounds a reader can weigh
```

**What it costs.** Two things, and the second is the worse one.

- **The check fails on ordinary work.** `plan.md` §*Alternatives considered*
  rejects exactly this: *a deleted-unstaged file is a normal state mid-edit,
  so the case fails on ordinary work and gets deleted or worked around.* The
  branch ships that shape in the module it wrote last.
- **The refusal instructs a destructive edit.** *Classify the difference* means
  go and change `PATH_LIST_CALLS`, and the honest edit for a scope that "no
  longer derives one" is to delete its row. That is a live classification
  deleted on evidence about a working tree —
  `classifications_of_nothing`'s own docstring calls out the same instruction
  one module over and declines rather than give it.

**Why it was missed.** Q3 asked the work to read *every case in the five
modules* for a verdict that depends on the corpus being whole. This module is
the sixth and was written in phase 4, after that reading.

**Reach.** Any `tests/*.py` in any of the six tables. At a release the missing
paths are under `seal/ledger/`, so step 3 is not where this fires; an unstaged
`git mv` or `git rm --cached` of a test module is.

---

## 🔴 2 · The record written about the one survivor is what stopped it being reported

**Location** — `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md:8`,
the Grounds cell.

The Grounds cell quotes, verbatim, the two shared phrases the check named when
it reported the survivor. `survivor_check.py` measures the wording a range
removed against the whole tree, so a file added to the tree carrying that
wording counts as wording the fix wrote.

**Executed, and the commit isolates the cause.** Commit `114b78f1` changes one
file and only one file, `survivors.md`.

| Range | Exemption passed | Result |
|---|---|---|
| `f8cf32e5..5ffa5dfb` — the commit before `survivors.md` | none | exit 1, one survivor named at `tests/test_the_payload_meter_says_what_it_measured.py:835` |
| `f8cf32e5..539d32df` | none | exit 0, `no removed wording is still standing` |
| `f8cf32e5..539d32df` | `--exempt …/survivors.md` | exit 0, and nothing printed under `exempt` |

`survivor_check.py`'s own docstring states the contract the last row breaks:
*an exempted survivor is still printed, under `exempt`, with its grounds*. No
`exempt` line appears, because there is no longer a survivor to exempt. The
row silences nothing; the file's mere existence does.

**What it costs.** The gate reports success having measured nothing, on
exactly the branches that record a survivor — which is issue #365 restated.
`seal/specs/1789211172-a-round-record-disarms-survivor-check/spec.md` is in
this tree and says it in those words: *a round record quotes the defective
wording verbatim, because that is what a review report is for, so the record
counts as wording the fix wrote … and the gate reports success having measured
nothing.* That work item filtered `rounds/` records out of the pool. A
`survivors.md` sits in the same work item directory and is not filtered, so
the one file the tool tells you to write is the one that disarms it.

**Two repairs, and only the first is this branch's.** The branch can stop
reproducing the phrases in prose. The class — every file under
`seal/specs/<id>/` that a reviewer is instructed to write about removed
wording — belongs to `survivor_check.py`'s pool filter, and §12 says the fix is
owed to the class rather than the coordinate.

---

## 🟡 3 · The coverage check declines over one path and takes the other finding with it

**Location** — `tests/test_no_document_names_the_old_roots.py:139` (`uncovered`).

```python
    absent = [rel for rel in COVERED if rel not in files]
    if absent:
        decline_if_shrunken(sorted(set(absent) & set(missing)), DECLINES_COVERAGE)
    return absent
```

The decline fires when *any* named path is merely off disk, and it swallows
the named paths that are absent for some other reason.

**Executed.** With one of the two `COVERED` paths missing from disk and the
other genuinely out of the corpus, the helper declines and the reason names
only the first:

```
1 tracked path(s) are listed by git and not on disk, so the named-coverage
half of test_the_scan_covers_something cannot tell a file this run skipped
from an entry that is really gone, and is not judging.
Missing: skills/implement/SKILL.md
```

The workflow file's genuine departure from the scan's coverage is reported
nowhere, in the case whose whole job is to prove the scan still reaches both
ends of its prefix list.

**What it costs.** A real coverage loss stays invisible for as long as an
unrelated file is mid-edit. The two sibling call sites do not have this
problem for the same reason in reverse: they decline only over a finding they
computed, and each finding is a single entry.

**Grounds it could be answered with, if the smith disagrees** — that declining
is always the safe direction. It is not here: the direction that costs
something is the one where a check that exists to notice a loss reports
nothing about the loss it noticed.

---

## 🟡 4 · The frame gained a paragraph whose author is the builder, and the template already had a place for it

**Location** — `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md:238-245`.

Two halves, and they judge differently.

- **The three re-stamped hashes are forced and correct.** The records arm of
  `evidence-check` resolves a stamp in a live work item exactly as a ledger
  row's, and a stamp naming content that moved goes to NOT SEALED under
  `--strict`. A stamp is a coordinate, not a judgment, so refreshing one is
  bookkeeping rather than authorship. Executed: `evidence_check.py --strict .`
  exits 0 at the tip, with `3 stamps read · 0 drifted`.
- **The added paragraph is a build verdict inside the contract.** Its last
  clause — *All nine claims were re-read and hold* — is an assertion about the
  build's own diligence, written into the document the build's spec compliance
  is judged against. `agents/framer.md` §*Why the frame is not the builder's to
  draw* is precisely about that: *a `spec.md` written by the agent that then
  builds to it stops being a contract and becomes an account of what got
  built … `warden` reads spec compliance before quality, and that ordering only
  means something when a different party wrote the document.*

**The paragraph has a designated home and the branch is already using it.**
`agents/framer.md` says a builder who finds the frame does not hold comes back
*as a written record and a hand-back*. `templates/sdd-overview.md:58` gives
that record a heading, `## Fed back into the spec`, and
`skills/code-review/SKILL.md:71` says what it holds. This work item's
`overview.md` already carries the same correction twice — in its divergence
table (*How many shared ledger rows drift*) and in `phases/phase-5.md`, which
lists all nine anchors with their grounds one by one. So the spec.md paragraph
is a third copy, in the one document whose author it is not.

**What it costs.** Nothing about the tree is wrong — I verified the count
myself and it is nine. What it costs is the anchor: the next reviewer of this
work item compares the build against a spec.md that the build partly wrote,
and the precedent says a builder may argue a correction inside the frame
rather than hand it back.

**What I am not saying.** Silence was not the alternative. Leaving the table
re-stamped with no sentence would make three post-work hashes read as a
complete list of what drifted. A coordinate-only note fixes that without
moving a verdict into the contract.

---

## ⬜ Corrections

**`overview.md` §*Not done* describes a survivor report the tip does not
produce.** It says the check *names* the payload-meter file and that *with it,
the check exits 0 over 1082 files*. Executed at `539d32df`: the check exits 0
over 1082 files **without** the exemption as well, and names nothing either
way. The sentence is true of `5ffa5dfb` and not of the SHA under review. It
follows from 🔴 2 and should be rewritten with it.

**`docs/release-checklist.md` step 3's new preamble is incomplete in the
direction that matters.** It tells the reader a skipped case appears *when the
tree is also mid-edit somewhere the liveness checks look, under `docs/`,
`skills/`, `templates/` or a shipped `.py`*. A mid-edit `tests/*.py` produces
a **red build**, not a skipped case — 🔴 1 is that, executed. Either the
sentence names it or 🔴 1's fix makes the sentence true; the second is better.

**`timer_offenders` takes its running version from `ROOT` rather than from its
own `root`.** `tests/test_release_hygiene.py:477` — `running = running or
version()`, and `version()` reads `ROOT`. A future caller that passes a
fixture root and no `running` silently compares fixture prose against this
repository's real version. The one present caller passes `running` explicitly,
so nothing is wrong today. The same line also makes
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` read the
version file twice where it read it once.

**The git-listing call is copied six times.** Six helpers now carry the same
`subprocess.run(["git", "ls-files", …], cwd=root, capture_output=True,
encoding="utf-8", errors="replace")` block, differing only in the pathspec.
The predicate was correctly lifted into `tests/conftest.py#on_disk`; the
listing beside it was not. Phase 4's reader counts call sites precisely
because copies multiply, and a seventh helper copying a seventh block is what
it exists to catch.

**Confirmed, not a finding — the re-stamp of the shared ledger.** The claim is
eight rows and nine anchors, and it is exact. Executed: 11 anchor cells
changed across 8 changed rows of `seal/ledger.md`, of which 9 are distinct
anchors (two units are cited from two rows each), and
`evidence_check.py --strict .` exits 0 with `1353 ok · 0 drifted · 0 broken`.
Whether each claim was genuinely re-read is not checkable from the tree;
`phases/phase-5.md` gives per-anchor grounds and the ones I opened hold.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The class reader's two liveness assertions do not decline on a shrunken corpus, so a tracked test module the tree deleted turns the module red and the refusal tells the reader to delete a live classification row | `tests/test_a_shrunken_corpus_declines_to_judge.py:296`, consumed at `:345` and `:391` | open | Executed in the clone: clean tree `14 passed` exit 0; with `tests/test_release_hygiene.py` off disk and the removal unstaged, `2 failed, 12 passed` exit 1. `plan.md` §*Alternatives considered* rejects failing on a shrunken corpus in its own words |
| 🔴 2 | `survivors.md`'s Grounds cell reproduces the two shared phrases the check matched, and adding that file is what stopped the survivor being reported at all — issue #365's class, one file over | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md:8` | open | Executed: exit 1 with one survivor at `f8cf32e5..5ffa5dfb`; exit 0 and nothing under `exempt` at `f8cf32e5..539d32df` with the exemption passed. `114b78f1` changes that one file only. `seal/specs/1789211172-a-round-record-disarms-survivor-check/spec.md` states the same mechanism for `rounds/` records |
| 🟡 3 | `uncovered` declines whenever any named path is merely off disk, so a named path that genuinely left the corpus is reported nowhere | `tests/test_no_document_names_the_old_roots.py:139` | open | Executed: with one `COVERED` path missing and the other genuinely absent, the helper declines and the reason names only the missing one |
| 🟡 4 | The paragraph added to the frame asserts the build's own diligence inside the document its spec compliance is judged against, and `templates/sdd-overview.md:58` gives that paragraph a home the branch is already using | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md:238` | open | `agents/framer.md` §*Why the frame is not the builder's to draw*, and its *comes back as a written record and a hand-back*. The same correction is already in `overview.md`'s divergence table and in `phases/phase-5.md`. The three re-stamped hashes are forced and are not part of this finding |
| ⬜ 5 | `overview.md` §*Not done* states the check names the payload-meter file and exits 0 because of the exemption; at the reviewed SHA it names nothing with or without it | `seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/overview.md` §*Not done* | open | Executed, and it follows from 🔴 2 |
| ⬜ 6 | Step 3's new preamble says a mid-edit tree produces a skipped case; under `tests/` it produces a red build | `docs/release-checklist.md` step 3 preamble | open | Follows from 🔴 1, executed |
| ⬜ 7 | `timer_offenders` resolves the running version from `ROOT` rather than its own `root`, and the version file is now read twice per run | `tests/test_release_hygiene.py:477` | open | Read. No present caller is affected |
| ⬜ 8 | The git-listing `subprocess.run` block is copied into six helpers; only the predicate was shared | `tests/conftest.py`, and the six helpers | open | Read |
| ⬜ | Confirmed: the shared-ledger re-stamp is 9 distinct anchors across 8 rows, and the checker is clean | `seal/ledger.md` | verified | Executed: 11 changed anchor cells over 8 changed rows, 9 distinct; `evidence_check.py --strict .` exit 0, `1353 ok · 0 drifted · 0 broken` |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer`, spawned by the orchestrator once the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository, checked out at `539d32df` | clean tree, tip confirmed `539d32d` |
| `bin/test -q` over the seven modules the diff touches | exit 0, `158 passed` |
| `bin/test -q tests/test_a_shrunken_corpus_declines_to_judge.py`, clean tree | exit 0, `14 passed` |
| the same module with `tests/test_release_hygiene.py` removed from disk, removal unstaged, then restored | exit 1, `2 failed, 12 passed`; both failures are the two liveness assertions |
| a temporary probe calling `uncovered` with one named path missing from disk and one genuinely absent | declined; the reason names only the missing path and never the other |
| `bin/test -q tests/test_one_word_one_meaning.py` | exit 0, `18 passed` |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0, `1353 ok · 0 drifted · 0 broken`, records arm `3 stamps read · 0 drifted` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..5ffa5dfb` | exit 1, one survivor at `tests/test_the_payload_meter_says_what_it_measured.py:835` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..HEAD` | exit 0, `no removed wording is still standing` |
| `python3 skills/code-review/scripts/survivor_check.py --range f8cf32e5..HEAD --exempt <this work item>/survivors.md` | exit 0, and no `exempt` line printed |
| `git show --stat 114b78f1` | one file changed, `survivors.md`, 9 insertions |
| a script comparing the anchor cells of every changed row of `seal/ledger.md` | 11 changed cells over 8 rows, 9 distinct anchors |
| `git ls-files -s` filtered to mode `120000` | no tracked symlinks, so `os.path.isfile` misclassifies nothing in this tree |
| grep for the two new fixture literals in `tests/test_no_real_identifiers.py` across the tree | both confined to that module, which excludes itself from its own corpus |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; it is the sealer's one act, and it comes due once these findings are answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | `overview.md` §*Not done*, which names no ticket and no durable home for it — it says only that it belongs to whoever opens that file next | the repository owner, if it is to have a home |
| Q1 — whether a path missing from disk should have its index content swept | `questions.md` Q1, default `Skip it`, a person's row | the repository owner |
| Whether a skip reason renders in full in the release runner's quiet output | `overview.md` §*Not verified* | the repository owner, at the next release |

## Paste-ready fixes

**🔴 1** — in `tests/test_a_shrunken_corpus_declines_to_judge.py`, return the
missing half and decline on it. Replace `suite_modules` and add the helper the
two cases call:

```python
DECLINES_CLASS = "the suite-wide enumeration of scopes that list paths from git"


def suite_modules():
    """`(every `tests/*.py` on disk, the tracked ones that are not)`."""
    out = subprocess.run(
        ["git", "ls-files", "tests/*.py"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return on_disk(ROOT, out)


def classified_scopes(present, missing, root=ROOT):
    """What the reader found over `present`, or `pytest.skip` when every scope
    that vanished is in a module the working tree deleted.

    The inverse direction the three call sites in the other modules answer,
    in the module that enumerates the class. To this half a module the tree
    deleted and a scope somebody removed are the same evidence -- and the
    refusal below tells the reader to classify the difference, which on a
    mid-edit tree means editing a live row out of a table on evidence about
    the working tree. Conditional on EVERY vanished scope being explained, so
    a genuine removal is still reported beside a skipped one.

    The pair is a parameter rather than fetched here, so the case below can
    hand it a tree it chose without deleting a file the suite is running from.
    """
    found = derivers(present, root=root)
    vanished = set(PATH_LIST_CALLS) - set(found)
    if vanished:
        gone = {key.split("#", 1)[0] for key in vanished}
        if gone <= set(missing):
            decline_if_shrunken(sorted(gone), DECLINES_CLASS)
    return found
```

Both consumers then take it, and neither reaches `_tree_of` on a module that
is not there:

```python
def test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard():
    found = classified_scopes(*suite_modules())
```

```python
def test_the_reader_finds_the_helpers_this_work_guarded():
    found = classified_scopes(*suite_modules())
```

And the case §15 owes, pinning the decline and its reason:

```python
def test_a_test_module_the_tree_deleted_is_not_a_scope_somebody_removed():
    """The inverse direction in the module that enumerates the class.

    An unstaged `git mv` of a test module would otherwise report its scope as
    no longer deriving a path list, and the instruction that comes with that
    report is to classify the difference -- a live row edited out of a table
    on evidence about a working tree.
    """
    key = sorted(APPLIES_THE_SHARED_GUARD)[0]
    rel = key.split("#", 1)[0]
    present, _ = suite_modules()
    with pytest.raises(pytest.skip.Exception) as declined:
        classified_scopes([p for p in present if p != rel], [rel])
    reason = str(declined.value)
    assert rel in reason, reason
    assert DECLINES_CLASS in reason, reason
    assert "not judging" in reason, reason

    # A scope that vanished for any other reason is still a finding.
    assert classified_scopes(present, [rel]) == derivers(present)
```

**🔴 2** — in
`seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md`,
stop reproducing the matched phrases. Replace the Grounds cell with:

```
| `tests/test_the_payload_meter_says_what_it_measured.py` | `skills: [alpha, beta]` | The range rewrote `test_the_scan_covers_something`, whose two named-path assertions became a `COVERED` tuple and a declining helper. The two phrases the check matched are not quoted here, because a `survivors.md` is in the pool the check searches and quoting them is what silenced the report (#365's class, one file over). They fall across a seam between an assertion and a skill path on one side, and a YAML flow-form frontmatter fixture on the other. The standing line is about a meter reading an inline list; it is not a copy of any sentence this work removed, and nothing about it would become false if the rewritten case were reverted |
```

Then confirm the row is doing work rather than being inert, exit read
directly:

```bash
python3 skills/code-review/scripts/survivor_check.py --range 5bf22ddb..HEAD \
  --exempt seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/survivors.md \
  > /tmp/survivor.txt 2>&1; echo $?
grep -c '^  exempt' /tmp/survivor.txt
```

An `exempt` line is what says the exemption matched something. No line means
the row still silences nothing, and the repair is in `survivor_check.py`'s
pool filter rather than in the row.

**🟡 3** — in `tests/test_no_document_names_the_old_roots.py`, decline only
when every named path that is absent is explained by the skip:

```python
def uncovered(files, missing):
    """The named paths the scan no longer covers, or `pytest.skip` when every
    one of them is a file the working tree deleted.

    Q3's third case, found by reading the five modules rather than by either
    ticket. `skills/implement/SKILL.md` leaving the corpus through a `git mv`
    that has not been staged is exactly the state this work is about, and
    without this the case reports the scan as no longer covering a file that
    is merely somewhere else -- a verdict about coverage taken from evidence
    about the working tree.

    **Conditional on every absent path being explained.** A named path absent
    for another reason is a real loss of coverage, and declining over a
    neighbour that is merely mid-edit would report it nowhere.
    """
    absent = [rel for rel in COVERED if rel not in files]
    unexplained = [rel for rel in absent if rel not in missing]
    if absent and not unexplained:
        decline_if_shrunken(sorted(set(absent) & set(missing)), DECLINES_COVERAGE)
    return unexplained
```

Both existing assertions in
`test_a_skipped_file_does_not_read_as_lost_coverage` still hold under this,
and one case is owed for the mixed tree:

```python
def test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit():
    """The decline must not carry a finding away with it."""
    assert uncovered(files=[], missing=[COVERED[0]]) == [COVERED[1]]
```

**🟡 4** — in
`seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md`,
replace the added paragraph with a coordinate-only note that carries no
verdict:

```
**The three stamps above are refreshed to what those units hold after the
work,** because the records arm of `evidence-check` resolves a stamp in a live
work item as it resolves a ledger row, and a stamp naming content that moved
takes `--strict` to NOT SEALED. The refresh is bookkeeping and nothing else.
What actually drifted, how far, and on what grounds is the build's to state:
`overview.md` §*Where spec and implementation diverged* and
`phases/phase-5.md` carry it.
```

Nothing is lost by the move — `overview.md`'s divergence table and
`phases/phase-5.md` already say the count was nine and why, and
`phases/phase-5.md` lists all nine anchors with per-anchor grounds.

---

Needs a fix: yes — 🔴 1 the class reader does not decline on a shrunken corpus; 🔴 2 the survivors record silences the check that reported it; 🟡 3 the coverage decline carries a real finding away; 🟡 4 the build's verdict sits in the frame rather than in the record the template gives it

Loses a record or crashes: no

---

## Proof block

**Executed** — `bin/test -q` over the seven touched modules (exit 0, 158
passed); `bin/test -q tests/test_a_shrunken_corpus_declines_to_judge.py` clean
(exit 0, 14 passed) and against a mid-edit tree (exit 1, 2 failed);
`bin/test -q tests/test_one_word_one_meaning.py` (exit 0, 18 passed); a
temporary probe against `uncovered`, deleted after the run;
`evidence_check.py --strict .` (exit 0); `survivor_check.py` at three ranges,
exits read from `$?` without a pipe; `git show --stat 114b78f1`;
`git ls-files -s` for symlinks; a script diffing the anchor cells of
`seal/ledger.md`.

**Read** — `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
`survivors.md`, `changelog.md`, `phases/phase-4.md`, `phases/phase-5.md`, the
ledger fragment; the full diff of `tests/conftest.py`,
`tests/test_no_real_identifiers.py`, `tests/test_a_finding_id_is_a_bare_integer.py`,
`tests/test_no_document_names_the_old_roots.py`, `tests/test_release_hygiene.py`,
`tests/test_a_release_is_sized_by_a_criterion.py`,
`tests/test_a_script_says_which_interpreter_it_needs.py`,
`docs/release-checklist.md`, and all of
`tests/test_a_shrunken_corpus_declines_to_judge.py`; `agents/framer.md`,
`CONTRIBUTING.md` §*What a change to a gate must carry*, `CLAUDE.md`,
`bin/test`, `skills/code-review/scripts/round_record.py#finding_number`, the
exemption path of `skills/code-review/scripts/survivor_check.py`,
`seal/specs/1789211172-a-round-record-disarms-survivor-check/spec.md`, and the
pull request body of #440.

**Unverified** — every figure in the build's own hand-back that I did not
re-run: 785 passed over 24 modules, 284 over nine, 84 over six, and the
per-phase red demonstrations. Answered by `specseal:sealer` for the totals and
by the phase records for the demonstrations. The full suite, the
repository-wide lint and the typecheck are out of this agent's scope under
`agent-contract` §2 and are the sealer's one act.
