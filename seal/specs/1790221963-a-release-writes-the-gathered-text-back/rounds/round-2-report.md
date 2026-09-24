# Round 2 report — a release writes the gathered text back

Target SHA: `e6c85df6` · base `61f0d0d8` · the verifying round. Its target is
round 1's fix range `0b094396..1e2905cc` (79c791fe, 7c419218, 813a55f4,
1e2905cc). Read in a `git clone --no-local` at the target, under this round's
scratch directory. Nothing was written in the main checkout except this file.

## Summary

Round 1's fix does what round 1 asked. X5 is red with bf7ba905's script and
green at the tip, and every earlier shape answers as round 1 recorded. The two
paperwork corrections are in place. Round 1's ⬜ 2 left one question open: the
report-less shape. Measured against two controls, that shape is the sweep's
rule working, not a defect.

The fix also opened one thing:

1. **The split writes into the one set every file is scored against.** A
   gathered sentence's n-grams that a lost changelog entry shares go into
   `written`, and `written` is subtracted for every file's removed sentences,
   not only for `CHANGELOG.md`'s. Take a release that rewords a live entry
   quoting a claim, gathers a fragment quoting the same claim, and corrects
   that claim in `docs/a.md`. The fragment subtracts the claim from
   `docs/a.md`'s corrected sentence, and the survivor in `docs/b.md` goes
   silent. This is #557's defect coming back through the fix, and the fix's
   own comment says it cannot happen (🟡 1).

A per-source fix closes it. The split is applied only when a `CHANGELOG.md`
sentence is scored. It was trialled in the clone with the module green,
104 passed, and every shape of this round answered as it should.

## What the fix range changed, read against the code

- **The split** (`skills/code-review/scripts/survivor_check.py:1055-1064`):
  read. `held` is the gathered subset of `moved`. `lost_here` is the n-grams
  of `gone[lost:]`, which are this file's removed sentences, because `lost`
  is taken before this file's loop. Of each held sentence, the grams in
  `lost_here` are added to `written`. Round 1's paste-ready fix went in as
  written. The trouble is the target set, not which grams are picked:
  `written` is one set for the whole range, and `wanted` subtracts it from
  every source's grams (`:1074-1079`, `score` at `:1180`).
- **The docstring bound** (the module docstring `:174-178`, `corrected`'s
  docstring `:980-990`, the comment at `:1057-1061`): read against the code.
  The mechanism is stated correctly: the gathered grams that a lost
  changelog sentence shares are written. Two claims are false at the tip.
  The module docstring says the gathered text *may not subtract a survivor
  the same commit's correction left*. The comment says *gathered text still
  cannot subtract another file's corrected wording*. Z1 and Z2 below
  contradict both, and so does ledger row H1's clause *does not let a
  fragment quoting wording the same commit corrected subtract the survivor
  in another file*. They are part of 🟡 1. The per-source fix makes all
  three true, so none of them needs a rewording of its own.
- **X5** (`tests/test_a_corrected_sentence_survives_elsewhere.py`, after
  G6): read and executed. Its docstring's *Red at bf7ba905: exit 0* holds.
- **⬜ 2's correction** (`plan.md` §*Operational impact* phase 1,
  `spec.md` §*Out*, `plan.md` §*Alternatives*, ledger H1 and F1, the
  changelog fragment, the overview): read. Each now says that withholding
  can report less, and names the one shape that still reports less than
  the base. That is true of the tip: none of this round's shapes reports
  less than the base except W.
- **⬜ 3's correction** (`spec.md` judgment 7 and §Scope, `questions.md`
  item 7, `plan.md` phase 4, the overview's divergence row): read. All of
  them say step A's gate row was left as written. The overview says step A
  was squashed and not released. `survivors.md` has one row, and running the
  sweep over the fix range with that row applied exits 0 (executed).

## Round 1's ⬜ 2 question: is the report-less shape the rule or a defect?

**The rule.** Shape W: the range deletes `FOUND` from `docs/a.md` and writes
nothing in its place. `docs/b.md` quotes `FOUND`. The only rewording,
`REPAIRED`, is in a fragment that stood at `a`, and a release that renames
`## Unreleased` gathers it. W is exit 1 at the base and exit 0 at bf7ba905
and at the tip. Two controls, executed:

- **Wc**, the same deletion, with `REPAIRED` in an ordinary document that
  stood at `a`. Exit 0 at the base, at bf7ba905 and at the tip.
- **Ww**, the same deletion, with `REPAIRED` written into an ordinary
  document by the range. Exit 1 everywhere.

The tip treats a gathered rewording exactly as it treats wording that stood
before the range (Wc), and never as wording the range wrote (Ww). The sweep
never reports the verbatim copy of a sentence that was deleted with no
rewording anywhere, because a lone run cannot clear the floor
(`test_one_independent_run_can_never_clear_the_floor`). The base's exit 1
came from counting the gathered text as the range's own writing. That is
the same over-count that made #557's shapes silent, pointed the other way.
So W costs something, but it is what the rule says. The records already
name it and leave the owner to decide whether a gathered rewording should
ever count as written.

## Findings

### 🟡 1 — the split's n-grams are written for every file, so a gathered fragment again subtracts another file's survivor

`skills/code-review/scripts/survivor_check.py:1062-1064`. The split adds
gathered grams to `written`, and `wanted` subtracts `written` from every
removed sentence. So when the sentence `CHANGELOG.md` lost shares a claim's
wording, a gathered fragment quoting that claim subtracts it from every other
file where the same commit corrected it.

**Executed** (throwaway repositories; exit codes read directly;
`b` = the report names `docs/b.md`):

| Shape | base `61f0d0d8` | `bf7ba905` | tip `e6c85df6` | per-source fix |
|---|---|---|---|---|
| Z1: the release rewords a live entry *The docs no longer say that* + `FOUND`, gathers a fragment quoting `FOUND`, corrects `docs/a.md` to `REPAIRED`; `docs/b.md` quotes `FOUND` | 0 | 1 b | **0** | 1 b |
| Z2: the live entry is `FOUND` with *afterwards* → *later*, and the release replaces it with the gathered `FOUND`; `docs/a.md` corrected | 0 | 1 b | **0** | 1 b |
| Z1n: Z1 with no fragment at all | 1 b | 1 b | 1 b | 1 b |

Z1n is the control that proves the cause. The same release without the
gathered fragment reports. Adding the fragment silences it. That is the
defect #557 exists to close: *the gathered wording would then subtract the
survivor a correction in the same commit left standing in another file*
(`corrected`'s docstring). The base is silent too, so this is not a new
silence against the base. It is a silence against bf7ba905, and it comes
from the round-1 fix, inside the one unit the fix changed.

**Why it matters.** The sweep is a gate, and silence is the direction this
work item hunts. Z1 needs a repository that keeps `## Unreleased` and also
gathers fragments. That is the repository class #557 and round 1's 🟡 1 are
both about, and this repository is not in it (it has no `## Unreleased`).
Three places state that the shape cannot happen: the comment beside the
code, the module docstring and ledger row H1. A reader relying on any of
them is misled.

**Why a set-level patch is not enough.** An obvious alternative writes the
split grams only where no other file lost them (`written |= split -
elsewhere`). That was trialled too. It closes Z1 and Z2 but silences X5W:
X5 with `FOUND` also deleted from `docs/a.md` in the same commit. X5W is
exit 1 at the base and at the tip, and 0 under that patch. The per-source
fix below keeps X5W at 1. It changes `corrected`'s return shape and one line
of `score`. `examine` is the only caller of either (`grep` executed).

The paste-ready fix and its case are below. **Executed** in the clone, then
restored with `git checkout` and a clean `git status`. Results: the module
104 passed with the case added. The new case is red at the tip, exit 0.
With the fix's `mine -= split` line removed, X5 alone fails among the 19
release, gather and rewording cases. `ruff check` and `ruff format --check`
exit 0 over both files. Every shape in the table under *Executed probes*
answers under the fix as it does at the tip, except Z1 and Z2, which
report.

The fix changes the hash of the `score` and `examine` units as well as
`corrected`. So `evidence-check` will name the ledger rows anchored at those
three units DRIFTED, and they need a re-read and `--reverify` in the fix
pass. Ledger row H1's claim becomes true as written, and its anchors need a
re-stamp.

## Executed separately from read

- **Executed**: the module at the tip; X5 with bf7ba905's script swapped in;
  twenty shapes at four script states (the base, bf7ba905, the tip, the
  per-source fix) plus the set-level patch; the proposed case at the tip and
  under the fix; the fix with its split removed; `ruff` over the fixed
  files; the sweep over the fix range with `survivors.md`;
  `evidence-check --strict` over this report's copy in the clone.
- **Read**: the fix diff, `corrected`, `score`, `examine`, `weigh`, `runs`,
  `Sentence`, `newly_released`, `a_gathered_fragment` and
  `gathered_fragments` in full; the paperwork diff of the fix range; the
  closing-word vocabulary in `chain_check.py`.
- **Not re-run, claimed by the orchestrator**: the hygiene modules
  (`149 passed` at 1e2905cc, module included). The ❓ row carries it.

## Regression tests to plant

Destination: `tests/test_a_corrected_sentence_survives_elsewhere.py`,
directly after
`test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports`.
Seen red at `e6c85df6`: exit 0, the assertion message printed. Green with the
paste-ready fix: module 104 passed.

## Facts for the evidence ledger

- `written` is one set for the whole range, and `wanted` subtracts it from
  every file's removed sentences. Anything added to `written` for one file's
  sake also reaches every other file. A per-file bound has to be applied
  where a source is scored (`score`), never in `written`. Z1 against Z1n
  shows this.
- Round 1's ⬜ 2 shape W is the rule working. At the tip, a gathered
  rewording behaves like wording that stood before the range (Wc: exit 0
  everywhere) and not like wording the range wrote (Ww: exit 1 everywhere).
  This belongs in the open-shape paragraph of `plan.md` phase 1 and ledger
  row H1 as grounds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the round-1 split writes a gathered sentence's n-grams into `written`, which every file's removed sentences are scored against, so where the lost changelog entry shares a claim's wording, a gathered fragment quoting it subtracts the survivor that a correction in another file left, which is #557's defect back through the fix, and the code comment, module docstring and ledger H1 each say it cannot happen | `skills/code-review/scripts/survivor_check.py:1062` | open | executed: Z1 and Z2 exit 1 at `bf7ba905`, exit 0 at `e6c85df6`; Z1n (no fragment) exit 1 at all four states; the per-source fix below trialled: module 104 passed, the new case red at the tip, X5 alone red with the split removed, X5W kept at 1 where the set-level patch loses it |
| 🟢 | round 1's finding 1 is closed: a gathered rewording of a lost live entry splits it again | `skills/code-review/scripts/survivor_check.py:1062` | confirmed | executed: X5 failed (1 failed, 102 deselected) with `bf7ba905`'s script swapped in, restored with `git checkout`; module 103 passed at the tip; X5 exit 1 naming `docs/b.md` at the tip, 0 at `bf7ba905`, 1 at the base |
| 🟢 | round 1's shapes answer as recorded at the tip: P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 naming `docs/b.md`; X1–X4 exit 0; X6 exit 1 | `skills/code-review/scripts/survivor_check.py:1047` | confirmed | executed at four script states; H1k, H1, H2k, H2 exit 0 at `61f0d0d8`; unchanged from round 1's table |
| 🟢 | round 1's finding 2 is closed: the records state the failure direction after the fix, and the one report-less shape they name is the rule working | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | confirmed | read at `plan.md:144`, `spec.md` §Out, ledger H1; executed: W exit 1 at the base, 0 at `bf7ba905` and the tip; controls Wc exit 0 and Ww exit 1 at every state, so the tip treats gathered wording as wording that predates the range |
| 🟢 | round 1's finding 3 is closed: the records say step A's gate row was left as written, and that step A is squashed, not released | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | confirmed | read at `questions.md:23`, `spec.md` judgment 7, `plan.md:103`, the overview's divergence row; executed: the sweep over `0b094396..1e2905cc` with `survivors.md` exit 0, one exempt row |
| carried | round 1's finding 4, a file moved whole writes the corrected wording it quotes | `skills/code-review/scripts/survivor_check.py:1054` | deferred #563 | already deferred in round 1; X1 exit 0 at all four states, unchanged by the fix range |
| carried | round 1's findings 5–7: the fragment path spelled two ways, a fragment's own `## ` heading, a CRLF changelog | `skills/code-review/scripts/survivor_check.py:1016` | deferred #564 | already deferred in round 1; X2, X3, X4 exit 0 at all four states, unchanged by the fix range |
| ❓ | the other modules that load the sweep and the hygiene modules were not re-run this round | `tests/` | ❓ out of verified scope | the orchestrator reports `149 passed` at `1e2905cc`; this round ran the one module. Who answers it: the sealer, whose full suite covers them |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:xdist` in the clone at `e6c85df6` | 103 passed, exit 0 |
| The same module, `-k` X5, with `bf7ba905`'s `survivor_check.py` swapped in, then `git checkout` | exit 1, 1 failed (X5), 102 deselected; `git status` clean after |
| Twenty shapes at the base, `bf7ba905`, the tip, the per-source fix and the set-level patch (a Python probe driving git per contract §8, deleted) | see the table below |
| The proposed case appended to the module, at the tip | exit 1, 1 failed: `exit 0` in the assertion message |
| The per-source fix plus the proposed case, whole module | 104 passed, exit 0 |
| The per-source fix with `mine -= split` removed, over the 19 release, gather and rewording cases | exit 1, 1 failed (X5), 18 passed |
| `uvx ruff check` and `uvx ruff format --check` over the fixed `survivor_check.py` and the module with the case | exit 0 and exit 0 |
| `bin/survivor-check --range 0b094396..1e2905cc` with this work item's `survivors.md` | exit 0; 31 sentences; one exempt row, `spec.md:44` |
| `bin/evidence-check --strict .` over this report's copy in the clone | exit 0; see the proof block |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch, and it is the sealer's |

### The shape table

```
shape   base   bf7   tip  set-level  per-source
P6        1b    1b    1b    1b    1b
P6d       1b    1b    1b    1b    1b
H1k        0    1b    1b    1b    1b
H1         0    1b    1b    1b    1b
H1c       1b    1b    1b    1b    1b
H2k        0    1b    1b    1b    1b
H2         0    1b    1b    1b    1b
X1         0     0     0     0     0
X2         0     0     0     0     0
X3         0     0     0     0     0
X4         0     0     0     0     0
X5        1b     0    1b    1b    1b
X6         1     1     1     1     1
W         1b     0     0     0     0
Wc         0     0     0     0     0
Ww        1b    1b    1b    1b    1b
Z1         0    1b     0    1b    1b
Z2         0    1b     0    1b    1b
Z1n       1b    1b    1b    1b    1b
X5W       1b     0    1b     0    1b
```

X6 has no `docs/b.md` and reports `docs/a.md`. X5W is X5 with `FOUND` also
deleted outright from `docs/a.md` in the release commit.

## Paste-ready fixes

### 🟡 1 — split only the sentences `CHANGELOG.md` lost, where a source is scored

In `corrected`, `skills/code-review/scripts/survivor_check.py:1030`:

```python
    gone, written, split = [], set(), set()
```

The same function, replacing `:1057-1064` (the comment and the three lines
under `moved = [...]`):

```python
        # ...except against what THIS file lost: a live entry the release
        # replaced with a gathered fragment rewording it is still split by
        # that rewording, as a reworded release is (step A's round 2 🟡 1).
        # Those n-grams are kept apart from `written`, which every file's
        # removed sentences are scored against, and `score` subtracts them
        # from this file's alone: written for every file, a fragment quoting
        # wording the same commit corrected elsewhere would subtract that
        # survivor again (round 2's 🟡 1).
        lost_here = {gram for sentence in gone[lost:] for gram in sentence.grams()}
        for sentence in held:
            split.update(gram for gram in sentence.grams() if gram in lost_here)
```

`:1071`:

```python
    return gone, written, split
```

`corrected`'s docstring: its first line, and the text from `🟡 1, #557).`
at `:985` to the closing quotes at `:990`:

```python
    """`[Sentence]` -- what the range removed -- the n-grams it wrote, and
    the gathered n-grams that split `CHANGELOG.md`'s removed sentences alone.
```

```python
    🟡 1, #557). Of a gathered sentence, only the n-grams that also occur in a
    sentence THIS file lost count, and they are the third return rather than
    part of `written`: `score` subtracts them from `CHANGELOG.md`'s removed
    sentences alone, so a live entry the release replaced with a gathered
    fragment rewording it is still split into the runs it no longer shares,
    as a reworded release is, while no gathered text subtracts another
    file's sentence. A release that removes no live sentence writes nothing
    at all."""
```

In `score`, `:1166` and `:1180`:

```python
def score(gone, keep, where, weight_of, floor, split=frozenset()):
```

```python
        mine = set(sequence) & keep
        if source.path == CHANGELOG:
            # What a gathered rewording shares with the entry it replaced
            # splits that entry, and no other file's sentence (`corrected`).
            mine -= split
```

In `examine`, `:1217` and `:1222`:

```python
    gone, written, split = corrected(root, a, b)
```

```python
        score(gone, keep, where, weights(len(pool), files), floor, split),
```

The module docstring, `:174-178`:

```python
at the release and not written as the range's own (#557): the fragment's
own branch wrote it, so it may not subtract a survivor the same commit's
correction left. Only its n-grams that also occur in a sentence
`CHANGELOG.md` itself lost count, and against that file's sentences alone,
so a gathered rewording of a lost entry still splits that entry into runs.
```

The case to plant, directly after
`test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports`:

```python
def test_a_gathered_fragment_cannot_subtract_a_survivor_through_a_lost_entry(
    tmp_path,
):
    """Round 2's 🟡 1. The release rewords a live entry that quotes the claim,
    gathers a fragment quoting it verbatim, and corrects `docs/a.md`. What the
    fragment shares with the lost entry splits that entry and nothing else:
    written for every file, it subtracts the claim from `docs/a.md`'s
    corrected sentence too, and the survivor in `docs/b.md` goes silent. The
    same release without the fragment reports. Red at e6c85df6: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    quoting = f"The docs no longer say that {FOUND[0].lower()}{FOUND[1:]}"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {quoting}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry quoting the claim, a fragment quoting it, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0],
                f"{FOUND}\n\n- The docs now name the generator as its writer.",
                marker=True,
            )
            + f"\n{older}",
        },
        "release 1.0.0: reword the entry, gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered text shared with the lost entry was written for every "
        f"file and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
```

Needs a fix: yes — 🟡 1, the round-1 split writes gathered n-grams for every file, so a gathered fragment again subtracts another file's survivor (Z1, Z2 silent at the tip)
Loses a record or crashes: no

The gate has not come due: 🟡 1 is open, so the sealer's spawn waits on its
fix. This round opened a 🟡, which spends the run's one reopening. Per
`docs/review-chain-spec.md` §*The reopening*, the round after its fix pass
reports its findings as `deferred <home>` candidates.

## Proof block

Files opened this round, all in the clone at `e6c85df6` unless marked:
`skills/code-review/scripts/survivor_check.py` (the fix diff; the module
docstring `:160-180`; `newly_released`; `words`, `segments`, `Sentence`,
`sentences`, `ngrams`; `gathered_fragments`, `a_gathered_fragment`;
`corrected`, `wanted`, `carriers`, `runs`, `weights`, `weigh`, `score`,
`examine` in full); `tests/test_a_corrected_sentence_survives_elsewhere.py`
(the fix diff; `run`, `build`, `FOUND`, `REPAIRED`, `FILLER`,
`RELEASED_HEADINGS`, `FRAGMENT`, `changelog`, `two_sections`; G1–G6, X5,
the round-2 reworded-release case, the first same-file case);
`skills/code-review/scripts/chain_check.py:400-460`; `bin/test`;
this work item's `rounds/round-1.md` and `rounds/round-1-report.md` (main
checkout), `spec.md` §Scope and acceptance, `questions.md:15-30`, the
overview's divergence rows, `survivors.md`, the paperwork diff of the fix
range over `seal/specs/` and `seal/ledger/`;
`seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md` rows
H1–H3; step A's `rounds/round-3-report.md:60-95`. The `phases/phase-*.md`
files were not opened. Nothing was posted, pushed or committed. The probe
files, the swapped scripts and the throwaway repositories were deleted, and
the clone's `git status` was clean after every swap.
