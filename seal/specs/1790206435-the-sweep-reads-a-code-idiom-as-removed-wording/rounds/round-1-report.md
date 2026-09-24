# Round 1 report — the sweep reads a code idiom as removed wording

Target SHA `6a424d81` on `fix/543-the-sweep-reads-a-code-idiom-as-removed-wording`,
base `release/v0.15.1` (`9f846733`), whole-branch review, no earlier rounds.
Reviewed in a `git clone --no-local` of the main checkout at the target SHA;
the main checkout itself had moved on to `943651b8` by the time this file
was written, which this round did not open. Paths below are relative to the
repository root.

## Spec compliance

The three tickets land where `spec.md` §Scope puts them, and each phase
carries the four rows `CONTRIBUTING.md` §*What a change to a gate must
carry* asks for (`plan.md` §*Operational impact*, the phase records): a case
seen red against the previous phase's script, a failure direction stated as
*reports less* with the wrong allow named, a prompt budget of zero, and the
platform row (the tokenizer is the standard library's; the kinds are read off
it by name, so the 3.14 template-string pair is covered by `hasattr`). The
smith's account of what was seen red and mutated is a claim; what this round
executed is in `## Executed probes`, and what it read is said to be read.

- **#543, `python_prose`** (`skills/code-review/scripts/survivor_check.py:591`).
  Read against `spec.md` §Data & interfaces: COMMENT, STRING and
  FSTRING_MIDDLE kept in place, every other token blanked with a `|` at its
  first character, line numbers intact, `TokenError`/`SyntaxError`/`ValueError`
  falling back to the whole file. `sentences` routes `.py` through it on both
  sides and in the pool by construction. The multi-line assignment
  `out[row - 1 + offset][at : at + len(part)] = part` cannot widen a row: a
  continuation line of a string token starts at column 0 and its part is a
  prefix of that line; executed over CRLF text, the line count and every
  width hold (probe below). The `col < len(out[row - 1])` guard is what keeps
  NL, NEWLINE, DEDENT and ENDMARKER out of the output, as the phase-1 record
  says it measured; a DEDENT that shares a column with a following STRING is
  overwritten by the string because tokens are applied in order.
- **#307, `blank_released` and `a_gathered_fragment`** (`:523`, `:774`).
  The heading pattern matches the three spellings the spec names and not
  `## Unreleased`; the marker is `FOLD_MARKER`'s shape and
  `gather_changelog.py#marker` writes exactly `&lt;!-- specs/<id> -->` (the
  opener is spelled that way here so this file stays readable). The pool and
  the range apply the same predicate beside `records_a_past_state`, and the
  path-list case still counts one call site because `gathered_fragments`
  reads one file rather than listing paths. **One shape is missed, and it is a
  regression against the base rather than a gap the base had** — 🟡 1 below.
- **#439, `whole_range`** (`:1271`–`:1296`). An unresolved declaration now
  takes the same ownership question as a resolved one, from the same lazy
  `changed` list; `foreign` stays in the body, so `NAMED_EXCEPTION`'s grounds
  still hold. Ownerless `--exempt` files keep the hand-run reach (the
  existing G6 case), the owned-and-touched arm prints (S14), the
  owned-and-untouched arm is silent (S13). Executed in this round's clone as
  part of the module run.
- **S6 / S12, the four real ranges.** The module's four real-range cases
  passed here (the commits resolve in the clone), and the B-range divergence
  the smith recorded (9 → 8 at phase 1) reproduces with the base script: the
  base names `seal/ledger.md:2053` at 2.47 on three runs — *no longer the
  first*, *the paragraph does*, *applies to the* — one per assert literal of
  the test whose docstring the old reading had joined to them; the tip reads
  each literal as its own sentence and the row falls under the floor. That is
  the rule the spec asked for, applied on the range side, and the row was one
  the previous frame had already excused in its `survivors.md`. Confirmed,
  not a defect.
- **The rename shape found under Q5 and not taken.** Judged: leaving it out
  is right. The `git diff --name-only` call runs without `--no-renames` at the
  base too, so the silence on an `R096` move is a defect the sweep carried
  before this branch, it belongs to none of the three tickets, and `spec.md`
  judgment 7 explicitly scoped #526's split (two files that both remain) and
  not a whole-file rename. It is already deferred in `overview.md` §*Not
  done*; the Deferred table below names it so nobody re-finds it.

## Findings

### 🟡 1 · a release commit that moves `## Unreleased` under a version heading counts every sentence of the section as removed

`skills/code-review/scripts/survivor_check.py:930` (`corrected`, the
`counted` Counter). The heading-based reading was chosen over excluding the
file by path so that a repository following `agents/smith.md`'s *let the
entry accumulate unreleased* keeps its live prose in the sweep (`plan.md`
§Alternatives, row 5). In that repository the release commit renames
`## Unreleased` to `## 1.0.0 — <date>`. At `a` the section is live and every
line is a sentence; at `b` `blank_released` blanks it, so `counted` holds
none of those keys and every sentence of the section becomes a source, while
`written` gets nothing back because the tip is blanked. Any document that
restates an entry with two disjoint runs of its words is then reported at the
release with nothing anybody may correct — the #307 harm at the one commit
where a released section is created.

The base did not do this: with the section live on both sides, the rename
removed one two-word heading and nothing else. Executed both ways below:
base exit 0 against 1 sentence, tip exit 1 naming `docs/a.md:3` at 2.00. The
gathered-fragment shape one file over — the same event for this
repository's own flow — is handled and is silent (exit 0, against 0), which
is the asymmetry: `corrected`'s own comment says *the range that gathers it
deletes it and writes its text under a version heading, which is blanked, so
left in the list every sentence of the fragment would count as removed*, and
the `## Unreleased` section at a release is that sentence with one noun
changed. In this repository the hygiene job skips a pull request into
`main`, so the CI arm never meets it here; the sealer's arm and every
downstream repository do.

The fix counts a sentence standing under a version heading at `b` as still
held, never as written: a helper that keeps only the released lines, and
`counted` extended from it for the changelog path. It changes what the
range reads, so it takes a row in the gate table with the direction *reports
less, only for a sentence that stands under a version heading at the tip*,
and a case seen red first — the shape below is red against the tip as it
stands (exit 1). Two names below exist nowhere yet, and each is marked on
its own line: the helper `only_released` (NAME NOT IN TREE) and the case
`test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing` (NAME NOT IN TREE).

### ⬜ 2 · `report`'s docstring says every unresolved declaration is printed, and since phase 3 one kind is not

`skills/code-review/scripts/survivor_check.py:1345`: *`unresolved` is the
declarations whose range does not resolve here; they silence nothing and are
printed, because a declaration that quietly stopped applying is the one
failure a rotting anchor must not have.* After #439 a declaration of a work
item the range does not touch is dropped before it reaches `report`, quietly
and by design. The behaviour is the spec's; the sentence now describes the
input `report` receives as if it were the whole set. A sentence that reads
wrong while the behaviour is right, so ⬜: one clause — *the ones this run
could have used, which `whole_range` decides* — makes it true again. Editing
`report` drifts the 12,100-survivors row of `1790076070`, which `spec.md`
§Data & interfaces already lists as *`report` if edited*.

### ⬜ 3 · `phases/phase-3.md` cites a policy sentence the policy does not carry

`seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md:92`
says *`docs/review-chain-spec.md` §The survivor sweep still says a spec that
will not resolve is printed*. That section (`docs/review-chain-spec.md:2027`
onward) states the second anchor and says nothing about printing or
resolving; the sentence quoted lives in `whole_range`'s own docstring
(`survivor_check.py:1246`). A record pointing a reader at a policy clause
that is not there. Paperwork under `seal/specs/`, so a correction and not a
fix: replace the citation with the docstring's coordinate.

### ⬜ 4 · the tip's `CHANGELOG.md` is read twice per run

`skills/code-review/scripts/survivor_check.py:764` (`gathered_fragments`),
called at `:851` from `corpus` and at `:920` from `corrected`, both at `b`.
Two `git cat-file --batch` spawns for one file whose answer cannot differ
between the calls. The cost is one process per run and the smith may answer
with grounds (the two functions are independently callable and each is
anchored). The cheaper form is to read it once in `examine` and hand the set
to both, which widens two signatures already drifted by this branch.

### ⬜ 5 · in local mode no declaration can be *mine*, and phase 3 makes one more line silent there

`skills/code-review/scripts/survivor_check.py:1127` (`OWNER_DIR`) with
`:1293`–`:1308`. Where `seal/` sits under the git directory
(`agent-contract` §16), a `survivors.md` is at `<git-dir>/seal/specs/<id>/`,
`OWNER_DIR` names `seal/specs/<id>` as its owner, and `changed` — a `git
diff --name-only` — can never contain that directory because nothing under it
is tracked. Executed below: a resolved range row from such a path is refused
as `not yours` for its own run, which is the base's behaviour and not this
branch's; an unresolved one printed at the base and prints nothing at the
tip. The wrong allow is empty either way, so nothing is silenced; what is
lost is the line a person reads. Pre-existing in its cause, so deferred
rather than commissioned, with the party named in the Deferred table.

## Regression tests to plant

| Case | Destination | Seen red how |
|---|---|---|
| a release commit that renames `## Unreleased` to a version heading removes nothing a document may be reported against (🟡 1) | `tests/test_a_corrected_sentence_survives_elsewhere.py`, beside `test_a_range_that_edits_only_a_released_section_removes_no_sentence` (`:2628`) | red against the tip as it stands — exit 1 naming `docs/a.md:3` (executed in this round's probe, the same fixture) |

## Facts for the evidence ledger

- The base script over B's range (`cc49ae64^..cc49ae64`, resolved
  `cc49ae6..3dd2407`) names `seal/ledger.md:2053` at 2.47 on the three runs
  *no longer the first*, *the paragraph does*, *applies to the*, each from one
  assert-message literal; the tip names eight places and not that one.
  Executed 2026-09-24 in the clone at `6a424d81` — the fact row P2 states,
  reproduced by a second reader.
- `python_prose` over CRLF text keeps the line count and every line's width
  (executed; the case in row P1 covers LF only).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a release commit that moves `## Unreleased` under a version heading counts every sentence of the section as removed; a document restating an entry is reported at the release with nothing correctable — a regression against the base in the repository shape the heading-based reading was chosen for | `skills/code-review/scripts/survivor_check.py:930` | open | executed: base `9f846733` exit 0 against 1 sentence, tip `6a424d81` exit 1 naming `docs/a.md:3` at 2.00; the gathered-fragment shape of the same event is silent |
| ⬜ 2 | `report`'s docstring says every unresolved declaration is printed; since phase 3 a foreign one is dropped before it arrives | `skills/code-review/scripts/survivor_check.py:1345` | open | read; behaviour right, sentence overstates |
| ⬜ 3 | `phases/phase-3.md` cites `docs/review-chain-spec.md` §The survivor sweep for a sentence that section does not carry | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md:92` | open | read; paperwork under `seal/specs/`, a correction and not a fix |
| ⬜ 4 | the tip's `CHANGELOG.md` is read twice per run, once from `corpus` and once from `corrected` | `skills/code-review/scripts/survivor_check.py:764` | open | read; one process spawn, answerable with grounds |
| ⬜ 5 | in local mode `OWNER_DIR` names an owner `changed` can never contain, so a declaration is `not yours` for its own run (base) and an unresolved one is now silent (tip) | `skills/code-review/scripts/survivor_check.py:1127` | deferred new issue | executed; pre-existing in its cause, wrong allow empty |
| 🟢 | #543 · `python_prose` keeps COMMENT, STRING and FSTRING_MIDDLE, blanks the rest with a `|`, falls back whole on a tokenizer error, and holds line numbers over CRLF | `skills/code-review/scripts/survivor_check.py:591` | confirmed | read against `spec.md` §Data & interfaces; the module's 91 cases and the CRLF probe executed |
| 🟢 | #307 · the released region is read off the heading in the three spellings, `## Unreleased` stays live, the gathered set is read off the marker with no path list | `skills/code-review/scripts/survivor_check.py:523` | confirmed | read; S7–S11 executed in the module run |
| 🟢 | #439 · an unresolved declaration takes the ownership question from the same lazy `changed` list; ownerless and owned-and-touched still print | `skills/code-review/scripts/survivor_check.py:1293` | confirmed | read; S13, S14 and G6 executed in the module run |
| 🟢 | the B-range divergence (9 → 8 at phase 1) is the reader applied on the range side, and the row it drops was already excused by the previous frame | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-1.md` | confirmed | executed: base and tip scripts over `3dd24073^..3dd24073` |
| 🟢 | the gate table's four rows are carried per phase — red-first, direction, zero prompts, platform | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md` | confirmed | read; the smith's red-first runs are its claim, the mutations likewise |
| ❓ | the full suite, `ruff check .` and `ruff format --check .`; S15 and S16 at the seal | the tree at the reviewed HEAD | ❓ out of verified scope | `agent-contract` §2 — the sealer's, after the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `6a424d81` | 91 passed in 44.17 s, exit 0; the four real-range commits resolve in the clone, none skipped |
| release commit renaming `## Unreleased` to `## 1.0.0 — 2026-01-01`, `docs/a.md` restating the entry with two disjoint runs, base script `9f846733` | exit 0, `against 1 sentence(s)`, no removed wording standing |
| the same fixture, tip script `6a424d81` | exit 1, `against 3 sentence(s)`, `docs/a.md:3` at 2.00 against `CHANGELOG.md:7` |
| the same event as a gathered fragment — fragment deleted, its text written under `## 1.0.0` with its marker — tip script | exit 0, `against 0 sentence(s)` |
| the release commit with `docs/a.md` carrying the entry verbatim (one run), tip script | exit 0 — one run scores 1.00, under the floor by the module's own design; the two-run fixture above is the calibrated shape |
| `python_prose` over `x = 1\r\n"""doc one\r\nline two"""\r\ny = "lit"\r\n` | 4 lines in, 4 out; widths `[6, 11, 12, 10, 0]` both ways; sentence keys `doc one line two`, `lit` |
| `--exempt <repo>/.git/seal/specs/<id>/survivors.md` holding `origin/gone..HEAD`, tip script | exit 1, the survivor named, no `unresolved` line |
| the same file holding this run's own resolved range, tip script | exit 1, `not yours … written by seal/specs/<id> and this range touches nothing in it` |
| base script over `3dd24073^..3dd24073` | exit 1, 9 places including `seal/ledger.md:2053` at 2.47 (*no longer the first*, *the paragraph does*, *applies to the*) and `CHANGELOG.md:2090` |
| tip script over the same range | exit 1, 8 places: the two above gone, `skills/code-review/scripts/survivor_check.py:142` joined |
| full suite, `ruff check .`, `ruff format --check .` (the broad gate) | not yet |
| `evidence-check --strict .`, `unverified-check` | not run by this round; the handoff reports 0 and 0 as the orchestrator's re-run, read here and the sealer's `ledger` arm answers it |

Every probe file carried the probe prefix the contract names, ran once and
was deleted; the clone's working tree is clean and the clone itself is the
orchestrator's.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a whole file moved as a rename (`R096`) with one sentence reworded is silent, because `git diff --name-only` runs with rename detection and lists the new path alone; repair `--no-renames` on both calls with a red-first case | already deferred in `overview.md` §*Not done* and ledger row U2; a new issue | the orchestrator, who files it with the repair in `phases/phase-3.md` |
| in local mode `OWNER_DIR` names an owner that `changed` can never contain, so the ownership question refuses every local-mode declaration (⬜ 5) | a new issue, beside the rename one — both are `whole_range`/`corrected` gate changes outside the three tickets | the orchestrator, who files it |

## Paste-ready fixes

### 🟡 1 — `skills/code-review/scripts/survivor_check.py`, beside `blank_released`

```python
def only_released(text):
    """The complement of `blank_released`: every line of a released section
    kept, line numbers intact, every other line blanked.

    Read by `corrected` for the tip's changelog, so a sentence a release
    moved from `## Unreleased` under a version heading is counted as still
    held rather than as removed. Counted, never written back: a released
    section subtracts nothing from what the range is looking for."""
    out, released = [], False
    for line in text.split("\n"):
        if SECTION_HEADING.match(line):
            released = VERSION_HEADING.match(line) is not None
        out.append(line if released else "")
    return "\n".join(out)
```

### 🟡 1 — `skills/code-review/scripts/survivor_check.py`, in `corrected`, replacing the `counted = Counter(s.key for s in now)` line

```python
        counted = Counter(s.key for s in now)
        if path == CHANGELOG and path in after:
            # A release moves `## Unreleased` under a version heading. The
            # section is blanked at `b`, so without this every sentence of
            # it would count as removed and the documents restating an entry
            # would be reported at the release with nothing to correct -- the
            # gathered-fragment shape, one heading over. Held, not written:
            # nothing here reaches `written`.
            counted.update(
                sentence.key
                for line, raw in segments(blank_struck(only_released(after[path])))
                if raw
                for sentence in (Sentence(path, line, raw),)
            )
```

### 🟡 1 — `tests/test_a_corrected_sentence_survives_elsewhere.py`, beside the S9 case; red against the tip as it stands

```python
def test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing(
    tmp_path,
):
    """The release commit of a repository that lets the entry accumulate
    unreleased: `## Unreleased` takes a version heading and nothing else
    changes. The section is live at `a` and blanked at `b`, so without the
    held-count every sentence of it reads as removed and the document
    restating an entry is reported at the release with nothing anybody may
    correct. Two disjoint runs in the restatement, because one run scores
    1.00 and never clears the floor."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    restated = FOUND.replace("itself and the", "itself and, from then on, the")
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{restated}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the entry under Unreleased, and a document restating it",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND)},
        "release 1.0.0: the unreleased section takes a version heading",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "a release that only moved the unreleased section under a version "
        f"heading was read as a correction to chase into docs/a.md; exit {code}\n{text}"
    )
    assert "docs/a.md" not in text.split("examined", 1)[-1], text
```

Needs a fix: yes — 🟡 1, the release commit that moves `## Unreleased` under a version heading
Loses a record or crashes: no

## Proof block

Files opened in the clone at `6a424d81` unless stated:
`skills/code-review/scripts/survivor_check.py` (the branch diff, and the
functions `resolves`, `parse_range`, `tracked`, `read_blobs`, `segments`,
`Sentence`, `sentences`, `records_a_past_round`, `records_a_past_state`,
`retired_directories`, `corpus`, `corrected`, `wanted`, `carriers`, `runs`,
`weights`, `weigh`, `score`, `examine`, `OWNER_DIR`, `whole_range`,
`report`), `tests/test_a_corrected_sentence_survives_elsewhere.py` (the
branch diff, the helpers at `:40`–`:110`, `build`, `FOUND`, `REPAIRED`,
`FILLER`, `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`),
`seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/{spec,plan,questions,overview,changelog}.md`
and `phases/phase-1.md` through `phase-4.md`,
`seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md`,
the `seal/ledger.md` diff head, `CONTRIBUTING.md` §*What a change to a gate
must carry*, `.github/workflows/hygiene.yml` (the survivor step),
`.github/scripts/gather_changelog.py` (the marker), `skills/verify/scripts/unverified_check.py:113`,
`docs/review-chain-spec.md:2027`–`:2062`. Executed: the module run and the
probes in the table above. Not run: the broad gate, `evidence-check`,
`unverified-check`.
