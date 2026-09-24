# Implementation Plan: a release writes the gathered text back

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned.

## Summary

Four phases, in the order the harm is met. Phase 1 lands #557's paste-ready
fix. A gathered fragment's sentences, read at `a` by the gatherer's path, are
held and never written, and the module's three sentences about a gather
deleting its fragments are made true. Phase 2 closes the one way gathered text
escapes that filter: a prose-first fragment fused with its marker line. It is
conditional on a red case. Phase 3 pins the `lost` guard and the filter
apart (#555). Phase 4 is the records.

Nothing in the arithmetic moves. `wanted`, `carriers`, `runs`, `weights`,
`weigh`, `score`, `FLOOR`, the readers and the exemption code are not
edited. The held count, meaning what `counted` holds, is not changed either.
Only what `written` receives from a release is narrowed.

## Technical context

- `skills/code-review/scripts/survivor_check.py#corrected`. `gathered` is
  read at `b` by `gathered_fragments`. `paths` drops records, gathered
  fragments and retired directories, and `before`/`after` come from
  `read_blobs`. Per path: `was`, `now`, and for `CHANGELOG.md`
  `moved = newly_released(...)`. `counted` is `now + moved`, and `gone`
  takes what `was` holds beyond `counted`. The `lost` guard empties `moved`
  when this file added nothing to `gone`. Then `written` takes the grams of
  every sentence in `now + moved` beyond `old`. #557's filter goes between
  the guard and `old`, so it cannot touch `counted`.
- `#newly_released` reads `segments(blank_struck(only_released(text)))` at
  both ends and returns the released sentences at `b` beyond those at `a`,
  per key. Phase 2's marker blank goes in its `released` closure. There it
  holds on both ends by construction, and `only_released`'s docstring
  (*every line of a released section kept*) stays true.
- `#segments` and `BLOCK`: a block ends at a blank line or at a line that
  starts a block (`-`, `*`, `+`, `#`–`######`, `>`, an ordered-list number,
  a thematic break). `<!-- ... -->` is none of these. `BLOCK` is spelled
  alike in two other scripts on purpose, which is why phase 2 blanks the
  marker in `newly_released` and never widens `BLOCK`.
- `#MARKER` is `^<!-- specs/(\S+) -->$`, with `re.M`. It is the shape
  `gather_changelog.py#marker` writes and `unverified_check.py#FOLD_MARKER`
  spells for `docs/`.
- `.github/scripts/gather_changelog.py#section` writes `## <version> — <date>`,
  a blank line, then for each fragment the marker line, the body
  (`read().strip()`) and a blank line. `#insert` appends to an existing
  section the same way. Nothing in the file deletes a fragment.
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: `build`, `run`,
  `FOUND`, `REPAIRED`, `FILLER`, `SHIPPED`, `FRAGMENT`, `RELEASED_HEADINGS`
  and `changelog(heading, body, marker=None)`, which puts the marker on the
  line after the heading and a blank line after it. That is not the
  gatherer's layout, which matters for G4 only. `two_sections` is used by
  round 2's older-release case. The round-2 cases sit at
  `test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy` and
  `test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one`.
- The module stood at 96 passed at `0c335744`, and at 97 with #557's fix and
  case applied (round 3 of step A, executed in its clone). Every count below
  is relative to what the smith reads at the branch tip, not to these.

**Failure scenario of the chosen approach, six months out.** Gathered text
reaches `written` through a key the filter does not know. There are three
ways this can happen, and each is named rather than prevented. First, a
gatherer that rewrites what it gathers: it reflows lines, demotes headings,
or joins bullets. Second, a fragment edited in the release commit as it is
gathered. Round 3 of step A called that wording the range wrote, and it is
written deliberately. Third, a marker in a shape `MARKER` does not match, if
some repository's gatherer spells it differently. Then phase 2's blank does
not apply, and a prose-first fragment's first sentence is written as it is
today. Each is silence in one release commit, and only where that commit
also corrects the wording the fragment quotes. This repository's own
releases reach none of them: they have no `## Unreleased`, and every
fragment here opens with a block start.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Hold a gathered fragment's sentences and never write them, read at `a` by the gatherer's path** (#557's fix) | The three shapes in the failure scenario above | **Chosen.** It matches the class by who wrote the text, which is what `written` is about |
| Read the fragments at `b` | A gatherer that deletes the fragment leaves nothing at `b`, so H1 stays silent. G2 is the case that goes red | Refused |
| Read them through the range's path list | In this repository's release commit the fragment is unchanged and so not in the diff at all. The list is also filtered by `a_gathered_fragment` by design | Refused |
| Refine the guard: count only a lost sentence that has n-grams, so a renamed `## Unreleased` (one word, no grams, never a source) does not trip it | It closes H1 and not H2. A reworded entry loses a real sentence, so the gathered text is still written, and it changes the unit #555 is about to pin. It would also close H1d. The inconsistency with P6d is real, but H1d is wording the range wrote, which the sweep subtracts everywhere else too | Refused for this work item; named in `spec.md` §*Out* for the owner |
| Drop the `lost` guard once the filter exists | P6d goes silent: a release note the range writes directly, quoting corrected wording, subtracts the survivor | Refused. `spec.md` judgment 5 |
| Plant P6 alone for #555, as its body asks | After phase 1, P6 is protected by the guard and the filter each alone. It is green with either removed, so it pins neither. That is the §15 failure, a case that passes against the defect it names | Refused. P6d pins the guard, H1k and H2k pin the filter, and P6 stays as the pair's case |
| Hold only the fragments newly gathered in this range (markers at `b` not at `a`) | A second `CHANGELOG.md` read per run to avoid over-holding. Over-holding drops from `written` only sentences nobody in this range wrote, which is noise, the direction the sweep tolerates | Refused |
| Match a moved sentence to fragment text by n-gram containment rather than by key | It would hold a genuinely reworded entry that shares a run with a fragment. That is round 2's 🟡 1 silence again, from the other side | Refused |
| Prepend the marker line to each fragment's text when building the held set | Couples the key to the gatherer's exact layout, marker then body with no blank line. A gatherer that puts a blank line between them breaks it the other way | Refused. Blanking the marker in `newly_released` holds for either layout |
| Widen `BLOCK` so an HTML comment starts a block | `BLOCK` is kept spelled alike in `issue_claims_check.py` and `round_record.py` on purpose, and it would change segmentation in every file the sweep reads | Refused |
| Import `gather_changelog.py` to find the fragments | A shipped script depending on this repository's release automation. Step A refused this for the same reason | Refused. The path is spelled from `MARKER`'s ids |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A gathered fragment's text is held and never written** (#557). #557's diff to `corrected`: the held set read at `a` over `seal/specs/<id>/changelog.md` for each gathered `<id>`, and the filter on `moved` after the guard. `corrected`'s docstring says why. The three *deletes / retires* sentences (module docstring, the `#307` comment, `a_gathered_fragment`'s docstring) are made true of a gatherer that leaves the fragment and one that deletes it. Cases G1 (#557's verbatim), G2 and G3, each seen red at the branch tip first | `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q`, with the pass count read directly. G2 also red under a mutation reading the held set at `b`. G7 and G8 green | `1d177b26` |
| 2 | **A marker line is a block boundary in `newly_released`** (§12's member, conditional on Q1). First, G4 in the gatherer's layout, seen red with phase 1 in place. Only then is a `MARKER` line blanked in `newly_released`'s `released` closure, with a comment saying why. If G4 is green with phase 1 alone, nothing is changed or planted, and `phases/phase-2.md` records the measurement | The same module. G4 red before, green after. G1–G3 and G7 green. The marker blank removed by mutation turns G4 red and nothing else | |
| 3 | **The guard and the filter each pinned** (#555). G5 (P6d) seen red with `if len(gone) == lost:` replaced by `if False:` and the filter present. G6 (P6) seen red with both removed. G6 run with each removed alone and the two results recorded (Q2) | The same module. Four mutations from Python, the file restored byte-identical after each: guard off (G5 red, and H1k/H2k still green), filter off (G1, G2, G3 red; G5 and G6 green), both off (G6 red), phase 2's blank off (G4 red) | |
| 4 | **The records.** F1 and C2 in step A's ledger fragment corrected with a dated note. Step A's `plan.md` §*Operational impact* row *round 1 fix, 🟡 1 · round 2 fix, 🟡 1 and 🟡 2* gains #557's clause under a dated `Corrected` note. The drifted rows of `spec.md` §*Data & interfaces* re-read, then `--reverify`. New rows in `seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md`: the filter, the guard's pin, and the marker if phase 2 landed. Then `changelog.md`, `overview.md` with its `## Not verified` table, and the branch's own sweep | `bin/evidence-check --strict .` exit 0. `bin/survivor-check --range origin/release/v0.15.1...HEAD` with every `seal/specs/*/survivors.md`: exit 0, or every report corrected or exempted with grounds. `bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/`. `uvx ruff check` and `uvx ruff format --check` over the edited files. The other modules that load `survivor_check.py` (`tests/test_the_contributor_has_a_procedure.py`, `tests/test_the_gate_asks_the_range_ci_will_ask.py`, `tests/test_unverified_rows_close.py`) | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

No migration, no new dependency, no environment variable, no interface
change. The sweep is a gate. It can refuse a pull request into a release
branch, and it is one arm of the seal. So each phase carries
`CONTRIBUTING.md` §*What a change to a gate must carry*:

| Phase | Test seen red | Failure direction | Prompt budget | Platform |
|---|---|---|---|---|
| 1 | G1 at the tip: exit 0, `against 2 sentence(s)` (round 3's figure at `0c335744`). G2 at the tip, and under the read-at-`b` mutation. G3 at the tip | Today the gate is **silent** in two release shapes: a release that renames `## Unreleased`, and one that rewords an entry, in each case where a gathered fragment quotes wording a correction in the same commit removed. After the fix, gathered text is held and never written, so the gate **reports more**, and only there. The wrong direction after is a survivor reported that a gathered fragment's rewording would have split. That is noise, and it needs a fragment rewording the corrected sentence inside the release commit itself. This repository's releases have no `## Unreleased`, so they reach neither shape today and see no change | zero | text handling and git only. One more `git cat-file --batch` per run, one path per marker in `CHANGELOG.md` at `b` |
| 2 | G4 with phase 1 in place (conditional: no red, no change) | The gate **reports more**, and only for a prose-first fragment's first sentence in the same two shapes. The wrong direction after is that the marker's own words no longer reach `written`. They are an id and a slug that no document states as a claim | zero | text handling only |
| 3 | G5 with the guard removed. G6 with the guard and the filter removed | None. These are pins, and the gate's behaviour does not change | zero | text handling and git only |
| 4 | none — records | none | zero | none |

**Parallel chains.** Step E (#526, `wt-526`) and the chain in `wt-547` run
while this one does. This work edits no file under `docs/`. Phase 4 edits
`seal/ledger.md`, but only the `Checked` cell and the note of four rows
under four older work items. If another branch edits the same rows first,
the merge is resolved hunk by hunk as `CLAUDE.md` requires, never with
`--ours` or `--theirs`. Step A's fragment, `seal/ledger/1790206435-…md`, is
not expected to be touched by either sibling. If it is, the same rule
applies.
