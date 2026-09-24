# Feature Specification: the survivor sweep's moved text, gathered reading, and local ownership (#563, #564, #554)

Three defects in `skills/code-review/scripts/survivor_check.py`. Each one predates the
branch that found it, and each one changes a gate's verdict or the line a
person reads. All three sit in two functions: `corrected`, which decides whose
writing a sentence is, and `whole_range`, which decides whose declaration a
range row is.

| Issue | What goes wrong today | What this work changes |
|---|---|---|
| #563 | A range moves a file, or splits a document, and corrects a claim somewhere else. The moved text counts as wording the range wrote. It subtracts the corrected claim's n-grams, so no survivor is reported, including the survivor inside the moved text | Moved text is held: counted, and never written. A pure move stays silent because nothing was removed |
| #564 | The gathered-text reading assumes three things: one spelling of the fragment path, no `## ` heading inside a fragment, and LF line endings | One predicate spells the path. A released region is not ended by a non-version heading. Text is read with CRLF normalised to LF |
| #554 | In local mode a `survivors.md` sits under the git directory. Its owner is looked for in a tracked-file diff, which cannot contain it, so the work item's own range row prints `not yours` | In local mode, ownership is answered from the work item's `routing.md` `Branch` row instead of from the diff |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*What the sweep reads, and what it counts as written*, the rule sentence **Only wording the range itself wrote is subtracted from what it removed.** and *the question is always whose writing a sentence is* | This decides #563. A move changes no sentence's author, so moved text is not the range's writing. The same statement's grounds sentence *a pure move writes every sentence back and is silent for that reason* is the one sentence that changes (see *Docs sentences this work changes*) |
| same statement: *A fragment's text gathered by a release is held and never written, because the fragment's own branch wrote it* | This is the shape #563's candidate names, and it is already ratified for gathered text. Moved text takes the same shape. #563's comment (its Y1 and W shapes) asks one question of both kinds of text. The docs now answer it for gathered text, and this work answers it for moved text the same way |
| same section, first statement: *The sweep reads only wording that still instructs somebody, and it reads it the same way on both sides of the range and in the pool. What is left out is left out by its shape* | #564. The released region and the gathered fragment are defined by their shape. A second spelling of the path, a heading inside a gathered body, and a line ending are each a way that shape gets misread. None of them is a policy choice |
| `docs/review-chain-spec.md` §*The survivor sweep*, statement **A declaration in `survivors.md` speaks to its own work item's runs and to no other.**, and its last sentence *In local mode the owner is never in the range's diff, which is MichaelYcJo/SpecSeal#554, open.* | #554. The rule stands. What changes is how the owner is found in local mode, and the sentence naming #554 as open is replaced |
| `skills/agent-contract/SKILL.md` §16 | Local mode means the root is `$(git rev-parse --git-common-dir)/seal/` and nothing under it is committed. So nothing under it can ever be in a range's diff |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every phase must show a test seen red, state a failure direction, give a prompt budget, and include a platform note. Each phase in `plan.md` carries all four |
| `agent-contract` §12, §13, §14, §15 | §12: each issue is a class, and the phase enumerates its members. §13: CRLF and path-resolution cases must be shown to hold without the platform guarantee. §14: a changed report line or docstring statement is pinned in the same commit. §15: every new case is seen red first |
| `CLAUDE.md` §*a change writes fragments, never the shared file*, second half | Ledger rows in `seal/releases/*.md` whose anchored units this work edits drift. Each one is re-read. A row whose claim becomes false is corrected in place with a `Corrected <date>` note. New rows go into `seal/ledger/1790260564-a-moved-file-counts-as-written.md` |

## The judgments the tickets left open, decided from the tree

These were decided here. Each one has its grounds, and each can be overturned
by reopening the same sources. None of them is in `questions.md`.

1. **Moved text is held, never written (#563's design question).** A sentence
   is *moved* when the range removed it at one path and added the same
   sentence (same `key`) at a different path in the same range. A moved
   sentence is neither removed nor written. Pairing is done on counts,
   one-for-one. This is the in-file rule applied across files: inside one
   file, `corrected` already counts a reordered sentence as neither removed
   nor fresh. It covers a whole-file move, a rename, and a split of a
   document into two files that both remain. The split is the shape #563
   names as reachable in this repository: the 0.15.1 split of
   `docs/review-chain-spec.md` (#526). A whole-file-only rule, such as git
   rename detection or identical-blob matching, would miss the split. That
   is why this frame rejects it (`plan.md` *Alternatives considered*).
   **Grounds:** the rule sentence quoted in Grounding row 1, and #557's
   reason applied to a move (*this range did not write it*).
2. **What this does to the verdict, and it is not strictly monotone.**
   Pairing takes a sentence out of the removed set only when every one of its
   n-grams was already in `written`. That sentence therefore added nothing to
   `wanted`, and it was never a scoring source. Pairing also takes the
   paired copy out of `written`, so `wanted` can only grow. A bigger `wanted`
   can still *merge* two runs of shared wording into one run, and `weigh`
   scores one run by its rarest n-gram. So one survivor can score lower than
   it did before. This is the same reading the text would get if it had not
   moved. It is the failure scenario in `plan.md`, not a defect to engineer
   away.
3. **A pure move now reports `against 0 sentence(s)`.** Today it reports a
   positive count, because every sentence is removed and then written back.
   S18 (`test_a_file_moved_verbatim_is_silent_because_its_wording_is_written_back`)
   pins the positive count as proof that the old path was read. That proof
   changes hands. S17 (a rename with one reworded sentence is measured) can
   only pass if the old path is read. S18 is rewritten to pin silence at a
   count of 0, and its name and docstring change with it.
4. **#564 ⬜5: one predicate spells the fragment path.** The reader in
   `corrected`, which today builds `seal/specs/<id>/changelog.md` itself,
   will read the paths that `a_gathered_fragment` accepts in the tree at the
   range's left end. The predicate's own acceptance does not change. The
   issue names *two predicates for one path* as the defect, and narrowing
   what the predicate accepts is a separate change that nobody has measured.
   A larger `shipped` set can only move sentences from written to held.
5. **#564 ⬜6: after a version heading, only another version heading or an
   `Unreleased` heading ends the released region.** The pattern is
   `^##\s+\[?unreleased\b`, case-insensitive. A `## ` line of any other kind
   inside a released section stays released. The rule does not depend on the
   marker, so a marker that is misspelled or has a CRLF ending cannot reopen
   the gap. **Grounds:** the only live-prose convention the module names is
   `agents/smith.md`'s *let the entry accumulate unreleased*, and
   `VERSION_HEADING`'s comment puts that prose *above the first version*.
   Also, this repository's gatherer inserts a new release above the first
   `## ` line, so a repository that keeps both a gatherer and
   `## Unreleased` ends up with `## Unreleased` directly after a fragment
   body. A rule bounded by markers alone would blank that live section. The
   `Unreleased` exception is what prevents that. `blank_released` and
   `only_released` stay exact complements because both read one region
   helper.
6. **#564 ⬜7: CRLF is normalised at the read boundary.** `read_blobs`
   returns text with `\r\n` turned into `\n`. That is one place, and every
   reader inherits it: `MARKER` under `re.M`, `blank_released`'s
   `split("\n")`, and any later `$`-anchored pattern. Line counts are
   unchanged. A lone `\r` is left alone (see *Out*). `read_exemptions`
   already opens files in text mode, which applies universal newlines.
7. **#554: in local mode, a declaration is `mine` when the range's right end
   `b` is `refs/heads/<Branch>` or an ancestor of it.** `<Branch>` is the
   `Branch` row of the `routing.md` next to the `survivors.md`, read with
   `hooks/routing.py#parse` (loaded by path, as `chain_check.py` loads it).
   A file is in local mode when its real path is under the real path of
   `<git-common-dir>/seal/specs/`. The ownership test is taken against the
   range's tip rather than the checked-out branch, because it is a question
   about the range. The issue's other candidate, *the range's commits carry
   that id's `routing.md`*, cannot hold in local mode, because that
   `routing.md` is never committed. Shared mode is unchanged. CI checks out a
   detached merge commit with no `refs/heads/<branch>`, so applying the
   branch test there would break the CI run that shared mode exists for.
   A missing `routing.md`, an unreadable one, one with no branch, or a branch
   ref that does not resolve all read as *not mine*. Such a declaration
   excuses nothing and prints under `not yours`, which is the loud direction.
8. **Docs sentences are corrected in place, and no marker is added.** The
   precedent is `00adf8c6` (#558), a fix branch that corrected
   `docs/review-chain-spec.md` sentences in place. Adding this work item's
   `<!-- specs/<id> -->` marker would tell `settle` that the item is already
   folded. The marker is the fold's record. The fold at release reads this
   `spec.md`.

## Scope

**In:**

- `skills/code-review/scripts/survivor_check.py`: the `corrected` pairing
  across files (#563); `read_blobs` normalising CRLF, one region helper
  behind `blank_released` and `only_released`, and the fragment reader in
  `corrected` asking `a_gathered_fragment` (#564); `whole_range` asking
  local-mode ownership through the branch row (#554). Also every docstring and
  comment these changes make false: the module docstring's *A released
  changelog section, and a gathered fragment* paragraph (*up to the next `## `
  heading*), `corrected`'s *A rename is read as a deletion plus an addition*
  paragraph, `whole_range`'s ownership paragraphs, and `OWNER_DIR`'s comment.
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: the new cases
  listed below, and S18 rewritten.
- `docs/review-chain-spec.md`: the two sentences listed under *Docs
  sentences this work changes*.
- Ledger upkeep. The drifted rows in `seal/releases/*.md` are re-read and
  re-stamped. The rows this work makes false are corrected in place:
  `0.15.1.md` R1 (a verbatim move silent *because written back*), C1 (*up to
  the next `## ` heading*), H1 (*read at the range's LEFT end* at the one
  spelled path; the note's *shares nothing* reason, which #563's comment
  names as narrower than the rule). `evidence-check` names the full list, and
  that list decides, not this one.
- The work item's own `changelog.md` and ledger fragment
  `seal/ledger/1790260564-a-moved-file-counts-as-written.md`.

**Out, each with its reason:**

- **The gatherer and the release-note publisher reading a fragment's `## `
  line.** `.github/scripts/gather_changelog.py#insert` and
  `publish_release_note.py#section_body` both end a section at any `## `,
  so a fragment that carries one breaks them too. They belong to the same
  class as #564 ⬜6, but they are this repository's release automation, not
  the sweep, and whether a fragment may carry a `## ` line at all is a
  format decision → `questions.md` Q1.
- **Narrowing `a_gathered_fragment` to an anchored path** (the
  `WORK_ITEM_DIR` shape). The predicate accepts
  `<anything>/specs/<id>/changelog.md`. Nothing has measured a false
  exclusion from that, and #564 names only the two-spellings defect.
- **A lone `\r` line ending.** `splitlines` breaks on it and
  `split("\n")` does not, so line numbers already disagree for such a file.
  No tool in this repository writes one, and it is not the shape #564 ⬜7
  measured.
- **Shared-mode ownership.** It is unchanged. See judgment 7.
- **Correcting survivors that a re-measured historical range turns up.**
  If `questions.md` Q2's measurement finds real survivors in #526's split
  range, they are reported and written to `seal/follow-up.md` with an
  answerer. They are not corrected here.

## User scenarios & acceptance *(mandatory)*

Each case is seen red at `c52e8350` (the base), or against the phase's code
reverted, before it is committed (§15).

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| M1 · a file moved whole, and a correction elsewhere (#563's probe) | Given `a.md` states FOUND, `b.md` quotes it and `c.md` quotes it. When one commit moves `c.md` to `d.md` unchanged and corrects `a.md` to REPAIRED. Then exit 1, and both `b.md` and `d.md` are named | New case. Red at the base with exit 0 |
| M2 · a split, and a correction elsewhere | Given `c.md` has two sections, one quoting FOUND, and `a.md` states FOUND. When one commit moves the quoting section into `d.md` (both files remain) and corrects `a.md`. Then exit 1, naming `d.md` and the untouched quoter | New case. Red at the base |
| M3 · a pure move stays silent (S18, rewritten) | When `a.md` is moved whole to `b.md` with nothing else changed. Then exit 0, `no removed wording is still standing`, and `against 0 sentence(s)` | S18 rewritten. The old assertion (`[1-9]` sentences) goes red under phase 2, and that red is the reason for the rewrite |
| M4 · a rename with one reworded sentence is still measured (S17) | Unchanged | S17 green, with no edit |
| M5 · a sentence moved verbatim is not a source | When one commit moves sentence S from `x.md` to `y.md` and makes no other change. Then S is not counted as removed | Covered by M3's count. No separate case unless the builder finds M3 does not pin it |
| G7 · a fragment at the other spelling is held (#564 ⬜5, X2) | Given a G1-shaped release whose fragment sits at `specs/<id>/changelog.md`. Then the survivor is reported | New case. Red at the base with exit 0 |
| G8 · a fragment carrying `## ` stays released (#564 ⬜6, X3) | Given a G1-shaped release whose fragment has a `## Notes` line before the quoting sentence. Then the text after it is not read as live, not written, and the survivor is reported | New case. Red at the base |
| G9 · `## Unreleased` after a released section stays live | Given a changelog with a version section and then `## Unreleased`, carrying an entry that restates a corrected claim. Then that entry is still a carrier | New case. It pins the half that must not move. It is green at the base, and it must be shown red against a region helper with the `Unreleased` exception deleted |
| G10 · a CRLF changelog has gathered ids (#564 ⬜7, X4) | Given the G1 shape committed with CRLF. The fixture repository sets `core.autocrlf=false` and asserts that the blob of `CHANGELOG.md` holds `\r\n`. Then the survivor is reported | New case. Red at the base. The blob assertion is the §13 half: without it, a Windows runner's autocrlf could turn the fixture into LF and the case would pass while measuring nothing |
| O1 · a local-mode work item owns its own range row (#554) | Given `seal/` under the git common directory, a work item there whose `routing.md` names the checked-out branch, and a range row for `<base>...HEAD`. When survivor-check runs with that `--exempt`. Then the row excuses the range, and no `not yours` line prints | New case. Red at the base, which prints `not yours` |
| O2 · a local-mode declaration does not reach another branch's range | Given O1's declaration, run from a second branch whose `<base>...HEAD` is a different range. Then the survivors are reported and the declaration prints `not yours` | New case. It pins the bound (the wrong-allow direction). It must be shown red against an ownership test reduced to `True` |
| O3 · shared mode unchanged | The existing ownership cases (U1, E4, G5 rows' cases) | Green, with no edit |

## Docs sentences this work changes

In `docs/review-chain-spec.md`. Replacement wording is the builder's, and it
must say this:

1. §*What the sweep reads, and what it counts as written*, second statement.
   Replace *A file moved to another path is read as a deletion plus an
   addition: a pure move writes every sentence back and is silent for that
   reason, and a move that rewords one sentence measures it, where git's
   rename detection hid both.* The replacement says that a sentence the range
   moved verbatim to another path (a file moved whole or a document split) is
   held and never written, because a move changes no sentence's author. A
   pure move removes nothing and is silent for that reason. A move that
   rewords one sentence measures that sentence, where git's rename detection
   hid both. The rule sentence and the gathered-text sentences stay.
   `Enforced by:` still names `corrected`. If the pairing lives in a helper
   of its own, add that helper to the list.
2. §*The survivor sweep*, the statement on declarations. Replace *In local
   mode the owner is never in the range's diff, which is
   MichaelYcJo/SpecSeal#554, open.* The replacement says that in local mode,
   ownership is read from the `Branch` row of the work item's `routing.md`:
   the declaration holds over a range whose tip is on that branch.

## Data & interfaces

No CLI flag, exit code or report line changes shape. The count in
`against N sentence(s)` drops for any range that moves text. That is the
visible change §14 pins, through M3. `whole_range` gains the `root`'s common
git directory as an input it computes lazily. It is asked only of a
declaration that would have matched, so a run with no matching declaration
still runs no extra `git` process.

## Open questions → questions.md

Q1 (a person, non-blocking), Q2–Q3 (a measurement), Q4 (the work).

Framed 2026-09-24 by framer, before the build.
