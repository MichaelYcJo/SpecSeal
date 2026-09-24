# Round 1 report — a release writes the gathered text back

Target SHA: `bf7ba905` · base `61f0d0d8` · whole branch, first round, no
earlier rounds to carry. Read in a `git clone --no-local` at the target;
nothing was written in the main checkout except this file.

## Summary

The fix does what #557 and #555 ask. All seven release shapes step A's round 3
listed, plus P6d, report at the target. H1k, H1, H2k and H2 were silent at the
base. The smith's five mutations each reproduce exactly as handed over. What
this round opened:

1. The filter withholds more than the text the fragment's branch wrote. It also
   withholds a gathered **rewording of a sentence `CHANGELOG.md` itself lost**,
   so the lost sentence's runs merge into one and its verbatim copy elsewhere
   goes unreported. That shape reported at the base and is silent at the
   target, which is a regression in the silence direction (🟡 1).
2. The plan and the ledger row state the failure direction as *reports more,
   and only there*. Finding 1 shows that is not true (⬜ 2, a correction).
3. The work item's own records still say step A's `plan.md` gate row was
   corrected, but the overview says it was deliberately left alone (⬜ 3, a
   correction).
4. Four more members of the class *text at the tip that this range did not
   write, reaching `written`*. All four are silent at both the base and the
   target, and none of them is reachable by this repository's own releases
   except the move (⬜ 4–⬜ 7).

## Spec compliance

- **#557's filter** (`skills/code-review/scripts/survivor_check.py:1011-1021`,
  `:1043-1047`): read. The held set is read at `a` over
  `seal/specs/<id>/changelog.md` for each id `gathered_fragments` reads at
  `b`. It is applied after the `lost` guard. `counted` is built before the
  filter, so the held count is untouched. This matches `spec.md` §*Data &
  interfaces* and plan phase 1.
- **Phase 2's marker blank** (`survivor_check.py:566-573`): read. The blank
  sits inside `newly_released`'s `released` closure and runs after
  `only_released`, on both ends of the range. `BLOCK` is untouched. This
  matches the plan.
- **The three docstring sentences** (`:169-175`, `:826-832`, the comment at
  `:986-992`): read against `.github/scripts/gather_changelog.py`. `fragments`
  globs `seal/specs/*/changelog.md`, and nothing in the file deletes one. The
  new sentences are true of both a gatherer that leaves the fragment and one
  that deletes it.
- **Cases G1–G6**: planted where `spec.md` says. The five mutations and the
  base probe below confirm each one is red against the state it names.
  `agent-contract` §15 holds.
- **The gate table** (`plan.md` §*Operational impact*): all four columns are
  present. The phase 1 *Failure direction* cell is the one finding 2
  corrects.
- **Step A's `plan.md` gate row**: not edited. The overview records this as a
  divergence on the orchestrator's instruction. Finding 3 is about the
  records that still say otherwise.

## Findings

### 🟡 1 — a gathered rewording of a lost live entry no longer splits it, and its copy goes silent

`skills/code-review/scripts/survivor_check.py:1047`. The filter drops every
moved sentence whose key is in `shipped`. That includes a gathered sentence
that is the **rewording of a sentence this same file lost**.

Take a repository that keeps `## Unreleased` and also gathers fragments,
which is the repository class #557 is about. At the release, the live entry
`FOUND` is replaced by a gathered fragment whose text is `REPAIRED`, and
`docs/b.md` quotes `FOUND`. At the base, `REPAIRED` is written. `FOUND` is
split into the two runs it no longer shares, and `docs/b.md` is reported
(exit 1). At the target, `REPAIRED` is withheld, the whole of `FOUND` is one
run, capped at 1.0 and under the floor, and the sweep exits 0. This is the
mechanism `test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy`
exists to prevent (step A's round 2 🟡 1). It comes back from the other side
here, which `plan.md` §*Alternatives* names for n-gram containment and not
for the key match that was chosen.

The same holds for a gathered fragment of an **older** release that still
stands at `a`: `shipped` reads every marker at the tip. So a release entry
reworded to match an older fragment's sentence goes silent too. `spec.md`
§*Out* calls this over-holding "the noise direction".

Why it matters: the sweep is a gate. The prompt names silence as the failure
direction to hunt, and this is a new silence against the base in a release
shape the work item's own repository class produces.

The fix below is **executed** in the clone and restored byte-identical. It
lets withheld gathered text still split what `CHANGELOG.md` itself lost, and
nothing else. With it: the module 102 passed, the X5 shape exit 1, and P6,
P6d, H1k, H1, H1c, H2k and H2 all still exit 1. The alternative is to justify
the silence as the sweep's rule for a deletion, since the range did not write
the rewording, and restate the failure direction (finding 2). Either answer
needs the case under *Regression tests to plant*, pinning whichever behaviour
is chosen.

### ⬜ 2 — the stated failure direction says "reports more, and only there", and finding 1 is a report less

`seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144`
(phase 1, *Failure direction*), the same claim at `plan.md:88` and
`spec.md:66` (*over-holding … is noise*), and the note of row H1 in
`seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md:1`
(*that only drops from `written` sentences nobody in this range wrote*). This
is the run's paperwork, so it is a correction and outside `Needs a fix`. Each
of these sentences assumes that withholding from `written` can only add
reports. The scoring is not monotonic in `written`: a withheld rewording
merges runs (finding 1). Whichever way 🟡 1 is answered, these sentences
should name the report-less shape, or say it was closed.

### ⬜ 3 — the work item's records still say step A's gate row was corrected

`spec.md:181` (judgment 7), `questions.md:23` (item 7) and `plan.md:103`
(the phase 4 row, whose Status names `a5630f93`) all state that step A's
`plan.md` §*Operational impact* row gains #557's clause. `overview.md`
records that the row was left alone on the orchestrator's instruction. The
records disagree with each other, and step A's row still says *where the file
lost a sentence the released wording is written as any file's is*, which is
now false for gathered wording, with nothing on the row pointing at the
correction. That pointer exists only in the F1 ledger note. The overview's
grounds also call step A *a shipped work item*, but `CHANGELOG.md` at the
target carries no marker for `1790206435`. This is a correction: a one-line
dated `Corrected` pointer on step A's row, or a note beside item 7 in
`questions.md`, resolves it.

### ⬜ 4 — a file moved whole in the range still writes the corrected wording it quotes

`survivor_check.py:1050-1054`, the per-file `written.update`. This is not
introduced by this branch: the base and the target both give exit 0. A range
moves `docs/c.md`, which quotes `FOUND`, to `docs/d.md`, and corrects
`docs/a.md`. The move writes `FOUND` at `docs/d.md`, `wanted` subtracts it,
and the survivor in `docs/b.md` (and in `docs/d.md`) is not reported. This is
the same class under the ground this work item gives, *the fragment's own
branch wrote it, not this range*: a moved file's text was not written by the
range either. The module's docstring calls a pure move "silent for the right
reason" (#551), and that holds only while the moved text quotes nothing the
range corrected. #551 is about a moved and reworded file, not this. It is
reachable in this repository by any split of a document that also corrects a
sentence another part of it quotes. Deferred candidate below.

### ⬜ 5 — the gathered fragment's path is spelled two ways

`survivor_check.py:842` (`a_gathered_fragment`) accepts
`<anything>/specs/<id>/changelog.md`. `survivor_check.py:1016` reads only
`seal/specs/<id>/changelog.md`. A fragment at `specs/<id>/changelog.md` is
left out of the range and never held, and the X2 probe gives exit 0 at both
ends. It is unreachable here, because the gatherer globs `seal/specs/`. It is
still two predicates for one path, and `a_gathered_fragment`'s docstring
already names `seal/specs/<id>/changelog.md`.

### ⬜ 6 — a fragment carrying its own `## ` heading ends the released section

`survivor_check.py:554` (`only_released`), with `:538` (`blank_released`).
The gatherer pastes a fragment's body verbatim under the version heading. A
`## ` line inside the body is a `SECTION_HEADING` that is not a version, so
everything after it reads as live at the tip. It goes into `now`, is fresh,
and is written. The X3 probe gives exit 0 at both ends. No fragment in the
tree has a `## ` line (`grep` executed), and nothing refuses one. The plan's
failure scenario does not name this shape.

### ⬜ 7 — a CRLF changelog has no gathered ids

`survivor_check.py:810`. With `re.M`, `MARKER`'s `$` matches before `\n` and
not before `\r`. A `CHANGELOG.md` committed with CRLF line endings therefore
yields no ids from `gathered_fragments`. There is then no held set, phase 2's
blank is inert, and the fragment stays in the pool. The X4 probe gives exit 0
at both ends. This is pre-existing in `gathered_fragments` and inherited by
both new uses. It is unreachable here (`.gitattributes` is `eol=lf`). The
plan's failure scenario names a differently spelled marker, and line endings
are a spelling nobody chose.

## Executed separately from read

- **Executed**: the module; ruff check and format over the two edited files;
  thirteen shapes (P6, P6d, H1k, H1, H1c, H2k, H2, X1–X6) at each end; the smith's five
  mutations; the 🟡 1 fix trial; `evidence-check --strict` on this report's
  copy in the clone.
- **Read**: the spec-compliance section above, the ledger corrections F1, C2
  and C3, the re-read notes S3, S1, G5, E1, R1 and U2, and the changelog
  fragment. Each was checked against the code at the target, and no false
  claim was found other than findings 2 and 3.
- **Not re-run, claimed by the handoff**: the six other modules that load the
  sweep and the four neighbouring modules (`570 passed, 7 skipped`), and the
  branch's own sweep with every `survivors.md`. See the ❓ row.

## Regression tests to plant

Destination: `tests/test_a_corrected_sentence_survives_elsewhere.py`, after
`test_a_gathered_release_that_loses_nothing_reports`. As written, it asserts
the behaviour the 🟡 1 fix restores. It is red at the target (the X5 probe:
exit 0) and green with the fix (the X5 probe: exit 1). If 🟡 1 is answered by
justification instead, invert the assertion and say so in its docstring.

## Facts for the evidence ledger

- The sweep's score is not monotonic in `written`. Withholding a sentence
  that shares runs with a removed one merges those runs, and a merged run is
  capped at 1.0 (row S1 of `seal/ledger.md`). Any claim of the form
  *withholding only adds reports* is false. This fact belongs in H1's note
  with whichever answer 🟡 1 gets.
- Executed at the base: H1k, H1, H2k and H2 exit 0 with `against 2
  sentence(s)`, and P6, P6d and H1c exit 1. This round confirms the
  smith's red-at-base figures independently.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the gathered-text filter also withholds a gathered rewording of a sentence `CHANGELOG.md` itself lost, merging its runs; a verbatim copy that reported at the base is silent at the target | `skills/code-review/scripts/survivor_check.py:1047` | open | X5 probe: exit 1 at `61f0d0d8`, exit 0 at `bf7ba905`; the fix below trialled green (module 102 passed, X5 exit 1, the seven shapes still exit 1) |
| ⬜ 2 | the failure direction is stated as *reports more, and only there*, and over-holding as noise; finding 1 is a report less | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | open | paperwork correction; the same claim at `plan.md:88`, `spec.md:66` and ledger row H1's note |
| ⬜ 3 | the work item's spec, questions and plan say step A's gate row was corrected, and the overview says it was left; the row itself carries a now-false clause with no pointer | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | open | paperwork correction; also `spec.md:181`, `plan.md:103`; step A has no marker in `CHANGELOG.md`, so *shipped* in the overview's grounds is not true of the release |
| ⬜ 4 | a file moved whole in the range writes the corrected wording it quotes, and the survivor goes silent | `skills/code-review/scripts/survivor_check.py:1054` | deferred new issue | X1 probe: exit 0 at both ends; pre-existing; same class as this work item's ground; not #551 |
| ⬜ 5 | `a_gathered_fragment` and the held set spell the fragment's path two ways | `skills/code-review/scripts/survivor_check.py:1016` | open | X2 probe: exit 0 at both ends; unreachable here, because the gatherer globs `seal/specs/` |
| ⬜ 6 | a fragment's own `## ` heading ends the released section, and its text after it is written | `skills/code-review/scripts/survivor_check.py:554` | open | X3 probe: exit 0 at both ends; no fragment in the tree has one |
| ⬜ 7 | a CRLF `CHANGELOG.md` yields no gathered ids, so neither the held set nor the marker blank applies | `skills/code-review/scripts/survivor_check.py:810` | open | X4 probe: exit 0 at both ends; pre-existing; unreachable here (`eol=lf`) |
| 🟢 | #557's shapes report at the target: P6, P6d, H1k, H1, H1c, H2k, H2 | `skills/code-review/scripts/survivor_check.py:1047` | confirmed | executed at `bf7ba905`, each exit 1 naming `docs/b.md`; H1k, H1, H2k and H2 exit 0 at `61f0d0d8` |
| 🟢 | the guard and the filter are pinned apart, as the handoff says | `tests/test_a_corrected_sentence_survives_elsewhere.py` | confirmed | executed: guard off → G5 alone red; filter off → G1–G4 red; both off → G1–G6 red; marker blank off → G4 alone red; held set read at `b` → G2 alone red; the file restored byte-identical |
| ❓ | the six other modules that load the sweep, the four neighbouring modules, and the branch's own sweep were not re-run this round | `tests/` | ❓ out of verified scope | the handoff and the orchestrator report them green at `bf7ba905`; this round ran the module alone. Who answers it: the sealer, whose full suite covers them |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `bf7ba905` | 102 passed, exit 0 |
| `uvx ruff check` and `uvx ruff format --check` over `survivor_check.py` and the test module | exit 0 and exit 0 |
| Eleven shapes at `bf7ba905` (a Python probe driving git per contract §8, deleted) | P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 naming `docs/b.md`; X1 move, X2 `specs/` root, X3 `## ` fragment, X4 CRLF exit 0 |
| The same shapes at `61f0d0d8` (the base's script copied beside the target's, deleted) | P6, P6d, H1c exit 1; H1k, H1, H2k, H2 exit 0 `against 2 sentence(s)`; X1–X4 exit 0 |
| X5 (gathered rewording of a lost live entry) and X6 (the range's own rewording) at both ends | X5: base exit 1, target exit 0. X6: exit 1 at both |
| Five mutations of `survivor_check.py` over the module, restored byte-identical and asserted | guard off: 1 failed (G5). Filter off: 4 failed (G1–G4). Both off: 6 failed (G1–G6). Marker blank off: 1 failed (G4). Held set at `b`: 1 failed (G2) |
| The 🟡 1 fix applied in the clone, restored byte-identical | module 102 passed; X5 exit 1; P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 |
| `bin/evidence-check --strict .` over this report's copy in the clone | exit 0; total 1777 ok, 0 drifted, 0 broken; no NOT-IN-TREE line |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it on this branch; it is the sealer's |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 4, a file moved whole in a range writes the corrected wording it quotes (pre-existing, not introduced here) | a new issue, candidate | the repository owner, who decides whether a moved text counts as written by the range |

## Paste-ready fixes

### 🟡 1 — let withheld gathered text still split what `CHANGELOG.md` lost

In `corrected`, replace the filter line at
`skills/code-review/scripts/survivor_check.py:1047`:

```python
        held = [sentence for sentence in moved if sentence.key in shipped]
        moved = [sentence for sentence in moved if sentence.key not in shipped]
        # ...except against what THIS file lost: a live entry the release
        # replaced with a gathered fragment rewording it is still split by
        # that rewording, as a reworded release is (step A's round 2 🟡 1).
        # Only the grams the lost sentences carry are written, so gathered
        # text still cannot subtract another file's corrected wording.
        lost_here = {gram for sentence in gone[lost:] for gram in sentence.grams()}
        for sentence in held:
            written.update(gram for gram in sentence.grams() if gram in lost_here)
```

The case to plant with it, after
`test_a_gathered_release_that_loses_nothing_reports`:

```python
def test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports(
    tmp_path,
):
    """The gathered-text filter's other side. The release replaces the live
    entry `FOUND` with a gathered fragment whose text rewords it, and
    `docs/b.md` quotes `FOUND`. The fragment's rewording is withheld from
    `written`, but it must still split the sentence `CHANGELOG.md` itself
    lost into the runs it no longer shares, as a reworded release does;
    withheld whole, `FOUND` is one run under the floor and its copy goes
    silent. Red at bf7ba905: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": "# a\n\nUnrelated.\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {REPAIRED}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {FOUND}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry, a fragment rewording it, a document quoting the entry",
    )
    head = build(
        repo,
        {
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED, marker=True)
            + f"\n{older}",
        },
        "release: the live entry replaced by the gathered rewording",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered rewording was withheld whole, so the lost entry never "
        f"split and its copy in docs/b.md went silent; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
```

Needs a fix: yes — 🟡 1, the gathered-text filter withholds a gathered rewording of a sentence `CHANGELOG.md` itself lost, a new silence against the base
Loses a record or crashes: no


## Proof block

Files opened this round, all in the clone at `bf7ba905` unless marked:
`skills/code-review/scripts/survivor_check.py` (the diff, the helper block
`read_blobs`–`only_released`, `newly_released`, `segments`, `Sentence`,
`sentences`, the record and fragment predicates, `corrected` in full);
`tests/test_a_corrected_sentence_survives_elsewhere.py` (the diff, the
helpers `run`, `build`, `FOUND`, `REPAIRED`, `FILLER`, `RELEASED_HEADINGS`,
`changelog`); `.github/scripts/gather_changelog.py` (the full file to
`main`); `.github/scripts/run_tests.py` (a grep); `bin/test`;
`.gitattributes`; `CONTRIBUTING.md` §*What a change to a gate must carry*;
this work item's `spec.md`, `plan.md`, `questions.md`, `routing.md`,
`overview.md` and `changelog.md`;
`seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md`; rows F1
and C2 of
`seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md`
and the word diff of that file and of `seal/ledger.md`; step A's `plan.md`
row at line 170. The work item's `phases/phase-*.md` were not opened.
Issue titles were read with `gh issue list`. Nothing was posted.
