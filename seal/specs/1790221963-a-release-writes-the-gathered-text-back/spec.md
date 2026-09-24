# Feature Specification: a release writes the gathered text back

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

The survivor sweep (`survivor-check`,
`skills/code-review/scripts/survivor_check.py`) has a held count for
`CHANGELOG.md` that step A (`seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/`,
#550) added and could not finish, because its run ended at the reopening
bound. Two tickets are left, and they are one unit:

- **A release that loses a live sentence writes the gathered text back**
  (#557). `corrected` writes every sentence the range put under a version
  heading into `written` whenever `CHANGELOG.md` lost a sentence
  (`if len(gone) == lost:`). `newly_released` returns the gathered
  fragments' text too, and the fragment's own branch wrote that text, not
  this range. Two ordinary release shapes lose a sentence: renaming
  `## Unreleased` to a version (the heading line is a lost one-word
  sentence), and rewording a live entry as it is released. In both, a
  fragment quoting wording that a correction in the same commit removed
  subtracts the survivor standing in another file, and the sweep exits 0.
- **The `lost` guard is load-bearing and no case pins it** (#555). With the
  guard replaced by `if False:` the module stayed at 96 passed (executed by
  round 3 of step A). Once #557's filter exists, the shape #555 names (P6)
  is protected twice, so a case of that shape alone no longer pins the
  guard.

This work holds a gathered fragment's text and never writes it, closes the
one way the gathered text escapes that filter, and pins the guard and the
filter each with a case that goes red when that one alone is removed. The
scoring, the floor, the exemption mechanism and every reader outside
`corrected` and `newly_released` are not touched.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else*, first clause: *reports every place in the tree still carrying wording the range removed* | The sweep's subject is **the range's** writing. A gathered fragment's text is not the range's writing, so subtracting it from what the range removed is measuring the wrong party |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | A fragment is written on its work item's own branch and concatenated at the release. That is the ground for *the fragment's own branch wrote it, not this range* |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The sweep can refuse a pull request into a release branch, so every phase states a test seen red, a failure direction, a prompt budget and platform honesty. `plan.md` §*Operational impact* carries the table |
| `skills/agent-contract/SKILL.md` §12 — a defect belongs to a class | The class is *text under a version heading at `b` that this range did not write*. The ticket's filter matches that text by sentence key, and one member escapes the match (§*Judgments the tree answered* 3). The frame names it and phase 2 owns it |
| `skills/agent-contract/SKILL.md` §15 — a case is not planted until seen red | #555's own case would not be red against the one mutation it exists for once #557 lands. Each case below names what it is red against |
| `skills/implement/SKILL.md` §1 — a ticket is a request, not an authority | #555 asks for P6 as the guard's pin. Judgment 4 says why P6 alone cannot pin it after #557 and which case does |
| Step A's `spec.md` judgment 4 and its `plan.md` §*Operational impact*, row *round 1 fix, 🟡 1 · round 2 fix, 🟡 1 and 🟡 2* | The held count and its guard are step A's design, and argued through three rounds. This work does not reopen them. It narrows what the write-back writes and leaves what is held as it is |

## Scope

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #557 | In `corrected`, a gathered fragment's sentences are **held and never written**. The fragments are read **at `a`** by the path the gatherer globs, `seal/specs/<id>/changelog.md`, for every `<id>` whose marker stands in `CHANGELOG.md` at `b`. Their sentence keys are dropped from `moved` after the `lost` guard and before `written` is built. `counted` is built before the filter, so the text is still held. This is the paste-ready fix in #557's body. It applies to the code as it landed in `61f0d0d8`: `git diff 0c335744 61f0d0d8` over `survivor_check.py` and the test module changes one comment in `VERSION_HEADING` and nothing in `corrected` (executed) | Phase 1 |
| #557, the docstrings | `corrected`'s docstring says a gathered fragment's text is held and never written, and why. Three sentences in the module say the gathering release **deletes** or retires each fragment: the module docstring's released-changelog paragraph (*a release's gathering commit deletes each fragment*), the comment above `gathered` in `corrected` (*the range that gathers it deletes it*), and `a_gathered_fragment`'s docstring (*the release that gathered it is what retires the file*). `.github/scripts/gather_changelog.py` removes nothing (read: no `remove`, `unlink` or `rmtree` in the file), and its docstring says `settle` retires the fragments later. The new comment says *which the release does not delete*. So the old sentences are made true of both kinds of gatherer, one that leaves the fragment and one that deletes it, because reading at `a` serves both | Phase 1 |
| §12's member: a fragment that opens with prose | The gatherer writes the marker line and then the fragment body directly under it, with no blank line (`gather_changelog.py#section`). `segments` joins a line that is not a block start onto the line above. So when a fragment's first line is plain prose, the marker's words and the fragment's first sentence become one sentence at `b`. Its key then matches nothing in the fragment, the filter misses it, and that one sentence is written. Every fragment in this tree opens with `###` or `- `, and no template fixes the shape. `newly_released` reads a marker line as a block boundary, so the first sentence keeps its own key. **Conditional on Q1**: the case is planted, and the change made, only if the case is red with phase 1's filter in place | Phase 2 |
| #555 | Two cases. **P6d** pins the guard by itself: a release writes an entry directly under a new version heading, with no fragment and no `## Unreleased`, the same commit corrects `docs/a.md`, and `docs/b.md` quotes the old wording. It is red with the guard removed and the filter present. **P6** is #555's own shape, a gather with nothing lost. It pins the pair: red with both the guard and the filter removed, and green with either one removed (recorded, Q2) | Phase 3 |
| The records | Ledger rows F1 and C2 corrected in place with a dated note. They say the `lost` guard is what keeps a gathered release's text out of `written`, which H1 and H2 show false. *Corrected 2026-09-24 in round 1's fix pass:* this cell said step A's `plan.md` gate row gains the clause #557 supplies; it was left as written on the orchestrator's instruction, and the gate row lives in this work item's `plan.md` §*Operational impact*. Every row the design drifts is re-read and re-stamped, new rows go in this item's own fragment, and the changelog fragment, `overview.md` and the branch's own sweep are done | Phase 4 |

### Out

| Left out | Why, and who answers |
|---|---|
| Any edit to `docs/review-chain-spec.md` | Step E (#526) is splitting it in parallel. Its §*The survivor sweep* describes nothing at the altitude this work changes: it never mentions the held count, the release shape or the guard. So no sentence there goes false and none is owed. Judgment 6 |
| **H1c** (`## Unreleased` kept, the version inserted below) and **H2** (a reworded entry with the fragment deleted) as cases | H1c loses nothing, so the guard and the filter both protect it, and it adds nothing P6 does not pin. H2 is H1 × H2k: reading at `a` is pinned by H1 and the reword by H2k. The two were executed by round 3 of step A and stay in #557's table |
| A released entry the range writes directly, in a release that also loses a live sentence (**H1d**: `## Unreleased` renamed, a new entry quoting the corrected wording) | The range wrote that text, so it is written, as any file's added wording is. `wanted` subtracts what a range writes everywhere else in the tree too. It stays silent by the module's own rule, not by this defect. The inconsistency with P6d, which reports, comes from the guard reading a one-word heading as a lost sentence. `plan.md` §*Alternatives* row 3 holds the refinement that would close it and why it is not taken here. The repository owner decides whether it is ever worth an issue |
| A fragment copy-edited as it is gathered, or created and gathered inside the same range | Round 3 of step A named both as deliberate. The first no longer matches its fragment's keys and is wording the range did write. The second is absent at `a` and was written by this range. Both are written, which is correct |
| Restricting the held set to fragments newly gathered in this range | Every marker at `b` is read, including earlier releases'. That only drops from `written` sentences nobody in this range wrote. *Corrected 2026-09-24 in round 1's fix pass:* this cell called that the noise direction. It is not on its own, because withholding a rewording merges the runs of the sentence it rewords (round 1's 🟡 1); since that fix a held sentence's n-grams shared with a sentence `CHANGELOG.md` itself lost still split that sentence, subtracted from `CHANGELOG.md`'s removed sentences alone since round 2's fix pass (corrected 2026-09-24: round 1's fix wrote them for every file), and `plan.md` §*Operational impact* phase 1 names the one shape that still reports less. It costs nothing measurable and saves a second `CHANGELOG.md` read (`plan.md` §*Alternatives*) |
| Local-mode `OWNER_DIR` (#554), a `#` comment block read as one paragraph, code in non-`.py` files | Step A's *Not done*, each already homed. Untouched here |

## User scenarios & acceptance *(mandatory)*

Each row is a case in `tests/test_a_corrected_sentence_survives_elsewhere.py`,
planted beside the round-2 release cases after
`test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one`. Each
is seen red against the named state before it is planted (`agent-contract`
§15), and the hand-back says how. Every fixture is #557's: `FOUND`,
`REPAIRED`, `FRAGMENT`, `FILLER`, `docs/a.md` corrected and `docs/b.md`
quoting, with one commit as the range.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| G1 · **H1k**: a release renames `## Unreleased` and gathers a fragment that is left in place | `## Unreleased` holds an unrelated entry and becomes `## 1.0.0` with the fragment's text gathered under a marker. The fragment stays, as the gatherer leaves it. When the same commit corrects `docs/a.md`, then exit 1 naming `docs/b.md` | #557's case verbatim, `test_a_release_that_renames_unreleased_and_gathers_still_reports`. Red at the branch tip (exit 0, `against 2 sentence(s)`, as round 3 executed at `0c335744`) |
| G2 · **H1**: the same, and the release deletes the fragment | As G1, with the fragment deleted in the release commit. Then exit 1 naming `docs/b.md` | Case, red at the tip. Also red with the held set read at `b` rather than at `a`, which is the mutation this case exists for |
| G3 · **H2k**: a release keeps `## Unreleased`, rewords its entry as it is released, and gathers a fragment left in place | Then exit 1 naming `docs/b.md`, and the reworded entry still splits as round 2's case requires (that case stays green) | Case, red at the tip (round 3: exit 0, `against 2`) |
| G4 · a gathered fragment whose first line is prose *(conditional, Q1)* | As G1, with the fragment's body a plain paragraph whose first sentence is `FOUND`, laid down the way `gather_changelog.py#section` writes it: the marker line, then the body with no blank line. Then exit 1 naming `docs/b.md` | Case, red with phase 1's filter in place and the marker read as prose. If it is green there, it is not planted, phase 2 makes no change, and `phases/phase-2.md` records the measurement |
| G5 · **P6d**: a released entry written directly, nothing lost | `CHANGELOG.md` holds only an older release. The commit writes a new `## 1.0.0` section whose entry is `FOUND`, with no marker and no fragment, and corrects `docs/a.md`. Then exit 1 naming `docs/b.md` | Case, red with `if len(gone) == lost:` replaced by `if False:` and the filter present. This is #555's pin |
| G6 · **P6**: a gather, nothing lost | No `## Unreleased`. The commit gathers a fragment quoting `FOUND` under `## 1.0.0` and corrects `docs/a.md`. Then exit 1 naming `docs/b.md` | Case, #555's shape. Red with the guard **and** the filter both removed. Green with either one removed, which is recorded rather than asserted (Q2) |
| G7 · the release cases already in the module | Round 1's pure-release case, round 2's reworded-release and older-release cases, S7–S10, S17, S18 | Unchanged and green after every phase |
| G8 · the four real ranges | `test_the_four_real_ranges_report_their_prose_and_none_of_their_code` | Unchanged. None of the four squash ranges releases, so none reaches the write-back |
| G9 · the ledger still anchors | `evidence-check --strict .` after `--reverify` over the rows §*Data & interfaces* names | Phase 4, and the sealer's `ledger` arm |
| G10 · the branch's own sweep | `bin/survivor-check --range origin/release/v0.15.1...HEAD` with every `seal/specs/*/survivors.md` | Phase 4: exit 0, with every report corrected or under `exempt` |

## Data & interfaces

No interface changes. `--range`, `--root`, `--exempt` and `--floor` stay as
they are, and so does every line the report prints. What moves:

- **`corrected`**: one `read_blobs` call at `a` over
  `seal/specs/<id>/changelog.md` for each `<id>` in `gathered`, building a
  set of sentence keys through `sentences`. After the `lost` guard, `moved`
  loses every sentence whose key is in that set. The docstring's closing
  paragraph and the `#307` comment above `gathered` change as §*Scope*
  says. The new list is built from markers, not from a git path-listing
  call, so `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
  does not count it. Round 3 ran that module green with the fix (97 passed).
- **`newly_released`** *(phase 2, conditional)*: a line matching `MARKER`
  is blanked before `segments` reads the released text, so a marker is a
  block boundary there. Both ends of the range are read the same way, so
  the held count cannot change for any sentence except a prose-first
  fragment's first one.
- **The module docstring** §*What is excluded, by construction rather than
  by list*, the released-changelog paragraph: its sentence saying the
  gathering commit deletes each fragment. And **`a_gathered_fragment`'s
  docstring**, its sentence saying the release retires the file. The
  predicate's body is not touched.

Ledger rows whose anchors this work drifts, each to be re-read and
re-stamped in phase 4 with a dated `Re-read` note, or corrected where the
claim changes:

| Row | File | Anchor touched | What happens to it |
|---|---|---|---|
| F1 | `seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md` | `corrected`; `newly_released` if phase 2 lands | **Corrected**: its note's last two sentences say the `lost` guard keeps a gathered release's text out of `written`, and the claim gains #557's clause |
| C2 | the same fragment | `corrected`, `a_gathered_fragment` (docstring only) | **Corrected**: its last `Re-read` note says the same thing about the guard |
| R1, U2 | the same fragment | `corrected` | Re-read: the rename reading is unchanged |
| S3 of `1788873640`, S1 of `1789211172`, G5 of `1790138190`, E1 of `1790174139` | `seal/ledger.md` | `corrected` | Re-read: the counting, the round-record, retired-directory and `survivors.md` exclusions are unchanged |

Whether the docstring heading anchor `#"## What is excluded, by construction
rather than by list"` (three rows of `seal/ledger.md`) drifts when one
sentence under it is reworded is Q3's. Step A measured that adding a
paragraph under it did not drift it.

Rows anchored on `wanted`, `carriers`, `runs`, `weights`, `weigh`, `score`,
`FLOOR`, `blank_released`, `only_released`, `gathered_fragments`, `MARKER`, `corpus` and `whole_range` are not touched
by this design. A phase that finds itself editing one of those units has
left the frame. New rows go in
`seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md`.

## Judgments the tree answered

Listed so nobody reopens them. Each can be overturned by opening what is
cited.

1. **The paste-ready fix applies as written.** `survivor_check.py` differs
   from round 3's target `0c335744` by one comment line in
   `VERSION_HEADING`, and the test module not at all (`git diff`, executed).
   Every hunk's context in #557 matches `61f0d0d8` (read).
2. **Read at `a`, never through the range's path list.** The gatherer
   leaves the fragment in place (`gather_changelog.py`, read), so in this
   repository's release commit the fragment is not in the diff at all. A
   gatherer that deletes it leaves nothing at `b`. `a` is the one end that
   holds the fragment in both, and G2 pins the choice.
3. **The key match has one known miss, and it is the marker.** `segments`
   ends a block only at a blank line or a block start (`BLOCK`). The marker
   line `<!-- specs/<id> -->` is neither, and the gatherer puts the body
   directly under it. A fragment opening with `###` or `- ` is safe because
   that line is a block start. A fragment opening with prose has its first
   sentence fused with the marker's words. Read, not executed. G4 is the
   measurement, and phase 2 is conditional on it.
4. **#555's case is P6d, and P6 stays as the pair's.** P6 loses nothing, so
   the guard empties `moved` before the filter is reached, and the filter
   would drop the gathered text anyway. Each protects it alone, so removing
   either leaves P6 green, and P6 is red only with both removed (read, Q2
   measures it). What the guard alone still protects after #557 is released
   text that is new to the file, not moved there and not gathered, in a
   release that loses nothing. P6d is that shape. The comment on #555 says
   the case should be *shown red with the filter removed*. That holds for
   H1k and H2k, which lose a sentence and so reach the filter. It does not
   hold for P6. Round 3 of step A labelled the sentence itself *read from
   the code, not executed* (`rounds/round-3-report.md` §*#555 (already
   deferred), checked*).
5. **The guard stays.** Removing it once the filter exists would turn P6d
   silent: a release note the range writes directly, quoting corrected
   wording, would subtract the survivor. The guard's own comment says what
   it is for: nothing of this file was removed, so there is nothing the
   moved wording could split.
6. **Nothing for step E.** `docs/review-chain-spec.md` §*The survivor sweep*
   has three bold clauses: reports every place, one row per range, and round
   records outside the corpus. None of them states the held count, the
   release shape or what is written. No clause goes false and none is
   owed, so E needs no row.
7. **Step A's records are corrected in place, not left.** F1 and C2 are live
   claims in a fragment not yet folded, and each says the guard keeps a
   gathered release's text out of `written`. The fix makes that false in a
   new way, and the ledger convention is a dated `Corrected` note on the row,
   which `correction-check` reads. Step A's `plan.md` gate row is left as
   written, on the orchestrator's instruction: it is a record of what step A
   planned, and the gate row #557 supplies lives in this work item's
   `plan.md` §*Operational impact* (corrected 2026-09-24 in round 1's fix
   pass; this judgment first said step A's row is corrected the same way).
   Round records are not edited: they are records of a past state.
8. **Nothing in `seal/follow-up.md` waits on this work.** Its survivor-sweep
   row concerns `phases/` records, which this design does not touch (read).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is four
rows and none of them is a person's: two measurements (Q1, Q2) and two for
the work (Q3, Q4).

Framed 2026-09-24 by framer, before the build.
