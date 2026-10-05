# Post-review check — 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token

| Field | Value |
|---|---|
| What this is | a narrow verifying pass over #811's post-review fix, not a round; the run is capped |
| Target SHA | 001e7e21 |
| Range checked | a8c7ab74..001e7e21: ad134ab1 (the fix, `Closes #811`), 33a18783 (the empty-destination case), 001e7e21 (ledger R5 and `phases/phase-4.md`) |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 001e7e21, and each version's `hooks/` taken by `git archive`, under `<scratchpad>/<id>/post-review/`; all of it removed at hand-over |
| git | 2.54.0 |

## Summary

#811 is closed. Round 3's 26 fetch-config shapes were re-run row for row, beside
53 further shapes: Unicode separators at the end, front and inside of a value
and on an exact destination, empty destinations, and the ASCII whitespace the
removed `.strip()` used to take off. git's own `checkout` was the reference,
under both the `checkout N` and the `checkout N --` carriers. No shape git
switches on reads as no switch at 001e7e21. Every move against a8c7ab74 goes
toward git: a shape git lands on moves from `None` to `switch`, and a shape git
refuses moves from `switch` to `None`.

The empty-word drop in `_refs` cannot drop a real ref. git refuses an empty ref
name and any name holding a newline, so the only empty word the split can make
is the one after the listing's last newline, or the whole of an empty listing.
That second case is why the drop is needed at all. An empty destination maps to
the ref name `""`, `git for-each-ref` lists nothing for it, and the
listing then splits to `[""]`. Without the drop the guard would read a switch
git refuses. With it, every empty-destination shape reads `None`, as git does.

The `phases/phase-4.md` bound and ledger row R5 say what was done. One ⬜
correction is about paperwork. R5 cites "16 fetch-config shapes", which no file
in the tree records. Its conclusion holds over round 3's 26 shapes and 53 more.

The never-quieter recheck through `main()` covered 30 command shapes in 4
session states at three versions. None of the 120 runs is quieter at 001e7e21
than at a3aa139a. 001e7e21 equals a8c7ab74 in every run but one shape, a guess
through a destination ending in U+00A0, which is #811's own shape and the
louder direction.

Nothing here is a regression against a3aa139a. The base reads `None` on every
config shape in this check, because it guessed from `origin` alone.

## What the account claimed, and what was found

- **ad134ab1's message claims** that git's config reader strips only ASCII
  whitespace, and that a destination ending in U+00A0, U+3000, U+0085 or
  U+2028 is fetched into and guessed through. Executed: git lands on all four
  and on five more characters (U+2029, U+1680, U+2000, U+202F, and U+FEFF, which
  `.strip()` never removed). a8c7ab74 reads `None` on every one that `.strip()`
  or `splitlines()` acts on. 001e7e21 reads `switch` on all of them.
- **The `_fetched_as` comment claims** that git's reader has already taken
  the ASCII whitespace off. Executed over five shapes: trailing spaces, a
  trailing tab, spaces before a `;` comment and before a `#` comment, and CRLF
  line endings. git lands on all five and the target reads `switch` on all five,
  so nothing the old `.strip()` did is lost. git's reader does not take a
  trailing vertical tab or form feed off. git refuses that refspec, and the
  target now reads `None` where a8c7ab74 read `switch`, which matches git.
- **R5's new executed sentence** says the case was red at a8c7ab74, 4 of 4,
  and that each change was broken once, red. Executed in the clone:
  - with a8c7ab74's two lines, 4 failed;
  - with only the `.strip()` restored, 4 failed;
  - with only `splitlines()` restored, 2 failed, U+0085 and U+2028;
  - with the empty word kept, the empty-destination case failed (1).

  The new case's docstring ("Red at `a8c7ab74`") and the empty-destination
  case's docstring ("Seen red with the empty word kept") are true.
- **R5's "over 16 fetch-config shapes"** names a set that neither the tree
  nor round 3's report records. The handoff says the smith ran a subset and
  wrote four rows differently from round 3. No file holds those rows, so this
  check could not compare them. It ran round 3's own 26 rows instead (below).
  R5's conclusion holds over them. The count is the ⬜ 1 correction.

## Findings from execution

### #811 closed: round 3's 26 config shapes at three versions

Each shape is a scratch repository holding one bare remote with a branch
`onfork` that nobody has locally. The ref the mapping names was put in place
before the config was written, so a config git cannot parse still has the ref
round 3's rows assume. Both carriers answered alike in every row.

| Fetch config (round 3's row) | git | a3aa139a | a8c7ab74 | 001e7e21 |
|---|---|---|---|---|
| destination outside `refs/remotes/` | lands | None | switch | switch |
| partial glob inside `refs/remotes/` | lands | None | switch | switch |
| a negative refspec excluding the name, beside a mapping one | lands | None | switch | switch |
| two `fetch` lines, the second mapping the name exactly | lands | None | switch | switch |
| `*` in the middle of the destination | lands | None | switch | switch |
| whole-namespace mirror into a private prefix | lands | None | switch | switch |
| no destination, a ref left by an earlier fetch | refused | None | None | None |
| the refspec only in a config reached by `include.path` | lands | None | switch | switch |
| remote name holding a `/` | lands | None | switch | switch |
| a legacy remotes file under the git directory | refused | None | None | None |
| remote name holding a space | lands | None | switch | switch |
| remote name holding two spaces and a tab | lands | None | switch | switch |
| remote name holding a `.` | lands | None | switch | switch |
| remote name holding `.`, `/` and `.fetch` | lands | None | switch | switch |
| mixed-case section and variable, mixed-case subsection | lands | None | switch | switch |
| deprecated `[remote.Name]` section | lands | None | switch | switch |
| three `fetch` keys, the third mapping | lands | None | switch | switch |
| an empty value beside a mapping one | lands | None | switch | switch |
| a key with no value beside a mapping one | refused | None | switch | switch |
| a value holding a newline, beside a mapping one | refused | None | switch | switch |
| the only mapping refspec after a newline inside one value | refused | None | None | None |
| a value ending in an escaped newline | refused | None | switch | **None** |
| a quoted value with surrounding spaces | refused | None | switch | **None** |
| a spaced remote, beside another remote's newline value | refused | None | switch | switch |
| empty subsection, `[remote ""]` | lands | None | switch | switch |
| no subsection, `[remote]` | refused | None | None | None |

The git, a3aa139a and a8c7ab74 columns match round 3's git, a3aa139a and
61e59b42 columns in all 26 rows. The 61e59b42 hooks are byte-identical to
a8c7ab74's (read: `git diff 61e59b42..a8c7ab74 -- hooks` is empty). The
two bold moves are the two round 3 predicted for this fix, and both now match
git.

### #811 closed: the Unicode-separator shapes

| Shape | git | a3aa139a | a8c7ab74 | 001e7e21 |
|---|---|---|---|---|
| destination ends in U+00A0, U+3000, U+0085, U+2028, U+2029, U+1680, U+2000 or U+202F | lands | None | None | switch |
| exact destination ends in any of the same eight | lands | None | None | switch |
| destination holds U+0085, U+2028 or U+2029 inside it | lands | None | None | switch |
| destination holds U+00A0, U+3000, U+1680, U+2000 or U+202F inside it | lands | None | switch | switch |
| any of the eight begins the value (a ref left in place) | refused | None | switch | None |
| U+FEFF at the end, inside, or on an exact destination | lands | None | switch | switch |
| U+FEFF begins the value | refused | None | None | None |
| U+001C anywhere | refused (git will not hold the ref) | None | None or switch | None |
| a remote-tracking ref ending `/onfork` and then U+2028 or U+0085 and more | lands | None | switch | switch |

The third row is the `splitlines()` half of the class, met in the middle of a
name and not only at its end. The listing split the real ref in two, and
neither piece was the name mapped. The fix reads it.

The fifth row differs from round 3's sentence that every version reads `None`
on a leading character. Round 3 ran that shape without the ref in place.
Here the ref was left in place, and a8c7ab74's `.strip()` read past the
leading character. 001e7e21 reads `None`, as git does, so this is not a
finding.

### The empty-word drop

- **It drops no real ref.** Executed: `git update-ref` refuses an empty name,
  a name holding a newline, and a name ending in a carriage return. It accepts
  a name holding U+2028, and `git for-each-ref --format=%(refname)`
  prints it whole on its own line. The listing always ends in a newline, so
  the split's only empty word is the last one, and `if ref` drops that word
  and nothing else. Read: `tracked_in_any_remote`'s first test (`endswith`)
  cannot be satisfied by an empty word, so the drop changes nothing there.
- **An empty destination maps no ref.** Executed: an exact source with an
  empty destination, a glob source with an empty destination, and an exact
  source with an empty destination beside a ref that does exist elsewhere.
  git refuses all three and all three versions read `None`. Kept, the empty word
  would read a switch here. That is the louder direction, and it would make
  the guard ask about a command git refuses. The case at
  `tests/test_guard_resolves_the_tree_it_judges.py:2596` is what pins it.

### The never-quieter recheck through `main()`

The run used the shapes round 3's whole-item pass listed by mechanism, built
afresh: a fresh repository pair for every run, and one process per version.
The shapes:

- P1 to P5;
- R1 to R14, plus #811's shape: a guess through a destination ending in
  U+00A0, alone in a dirty second tree, and again in front of a base-read
  switch in the clean tree;
- N1 to N6;
- T1, T2 and T4.

That makes 30 shapes in the 4 session states (single-session, detection
unusable, an idle session, an active session), at a3aa139a, a8c7ab74 and
001e7e21. Decisions were ranked silent < ask < deny.

- 0 of 120 runs are quieter at 001e7e21 than at a3aa139a.
- 001e7e21 equals a8c7ab74 in 116 of 120. The four that differ are #811's
  shape alone in a dirty tree. It is silent at both earlier versions. At
  001e7e21 it is `ask` in the single-session state and `deny` in the other
  three, about the dirty tree.
- Every row round 3 tabulated for a3aa139a against 61e59b42 reproduces with
  a8c7ab74 and 001e7e21 in the 61e59b42 column. P5, R1 and R7 to R9 are `ask`
  through candidate C at the base, and `ask`, or `deny` about the dirty tree,
  after. R3, R4, R6 and T4 are silent at the base in all four states and
  louder after. R5 is silent at both in the single-session state and louder
  after in the other three.

## Findings from reading

### ⬜ 1 — R5's "16 fetch-config shapes" is a count with no set behind it

`seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md:12`.

R5's #811 sentence ends "over 16 fetch-config shapes, none git lands on reads
as no switch". No file in the tree records which 16 shapes those were. The
handoff says four of them were written differently from round 3's rows, so
the count cannot be taken to mean round 3's set either. The conclusion is
true: this check ran round 3's 26 shapes and 53 more, and no shape git lands
on reads `None`. A reader cannot audit the count as written, though. This is
paperwork, so it is a correction and not counted in `Needs a fix`. One clause
fixes it, given under `## Paste-ready fixes`.

### The `phases/phase-4.md` bound

`phases/phase-4.md:63-66` now says that no recorded command holds a
`checkout` only #790's lookups read, among the pairs whose directory still
exists. 449 of the 972 `checkout` pairs up to the fix pass name a directory
that is gone, counted by round 3's reviewer. That is round 3's ⬜ 2 paste-ready
text, nearly word for word, and it states round 3's executed count.
Re-derived here by execution over the same project transcripts (638 now):
with the cut at the fix pass's last commit (2026-10-05T12:29+09:00), there are
972 distinct `checkout` pairs, and 449 of them have a working directory that
no longer exists. Both figures match. The "none newly read" half was executed
by round 3 at 61e59b42 and is carried, not re-run. The only code change since
then is #811's, and it reads a switch only through a fetch destination
holding a non-ASCII separator.

The edited line runs past the paragraph's wrap width. That is cosmetic, and
it is not a finding.

## Regression tests to plant

None. The two cases this range planted are the ones the mutations above show
red: `test_a_guess_through_a_destination_ending_in_unicode_whitespace` and
`test_a_fetch_refspec_with_an_empty_destination_maps_no_ref`.

## Facts for the evidence ledger

- R5, if ⬜ 1 is taken: the shape count becomes round 3's 26 shapes re-run by
  this check, plus the Unicode and ASCII-whitespace shapes. The executed facts
  are in the tables above.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | R5's #811 sentence counts "16 fetch-config shapes" that no file records, four of them said to differ from round 3's rows; the conclusion holds, the count cannot be audited | `seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md:12` | open | read; the conclusion executed over round 3's 26 shapes and 53 more; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | #811 is closed — a fetch destination ending in, or holding, a Unicode space or line separator maps to the ref git fetched into | `hooks/worktree-guard.py:1201` | confirmed | executed: round 3's 26 shapes row for row and 42 Unicode shapes against git's own `checkout`, at three versions; no shape git lands on reads `None` at 001e7e21; not a regression, a3aa139a reads `None` on every one |
| 🟢 | the empty-word drop drops no real ref, and an empty destination maps none | `hooks/worktree-guard.py:1173` | confirmed | executed: git refuses empty and newline-holding ref names; three empty-destination shapes refused by git, `None` at three versions; the case red with the empty word kept |
| 🟢 | R5's #811 sentence says what was executed | `seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md:12` | confirmed | executed: 4 failed with a8c7ab74's lines, 4 with the strip alone, 2 (U+0085, U+2028) with `splitlines()` alone, 1 with the empty word kept |
| 🟢 | the `phases/phase-4.md` bound states round 3's count | `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:64` | confirmed | executed: 972 `checkout` pairs to the fix pass, 449 with a working directory gone |
| 🟢 | no shape is quieter at 001e7e21 than at a3aa139a — `main()` recheck | `hooks/worktree-guard.py:1134` | confirmed | executed: 30 shapes × 4 states × 3 versions, 0 of 120 quieter; 001e7e21 equals a8c7ab74 except #811's shape, louder |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over the two narrow modules in the clone at 001e7e21 | 508 passed |
| Round 3's 26 fetch-config shapes through `classify`, both carriers, at a3aa139a, a8c7ab74 and 001e7e21, against git's own `checkout` | 17 git lands on: `switch` at a8c7ab74 and 001e7e21, `None` at a3aa139a; 9 git refuses: `None`, or the louder `switch`; two move from `switch` to `None` at 001e7e21, both refused by git |
| 42 Unicode-separator shapes (ten characters, U+001C among them, × end, front, inside and exact destination; two split tracking refs) | every shape git lands on: `switch` at 001e7e21; every move against a8c7ab74 is toward git |
| Three empty-destination shapes and eight ASCII-whitespace or quoting shapes | empty destinations: git refuses, `None` at three versions; whitespace git strips: lands, `switch`; trailing vertical tab and form feed: git refuses, `None` at 001e7e21 |
| The two new cases with a8c7ab74's lines, the strip alone, `splitlines()` alone, the empty word kept | 4 failed; 4 failed; 2 failed (U+0085, U+2028); 1 failed (empty destination). The clone's file restored and compared byte for byte |
| `git update-ref` with an empty name, a newline-holding name, a carriage return, and a U+2028 name | the first three refused; U+2028 accepted and listed whole |
| `main()` over 30 shapes × 4 session states at three versions, a fresh repository pair per run | 0 of 120 quieter than a3aa139a; 116 of 120 equal to a8c7ab74, the other 4 #811's shape, louder |
| The project transcripts, distinct `checkout` pairs to 2026-10-05T12:29+09:00, working directory present or gone | 638 transcripts; 972 pairs, 449 gone |
| `bin/evidence-check --strict .` in the worktree, with this file on disk | exit 0 |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this check ran none of it, and the sealer answers it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

## Paste-ready fixes

### ⬜ 1 (optional, the run's paperwork)

```text
each change broken once, red; over round 3's 26 fetch-config shapes and 53
more (Unicode separators, empty destinations, ASCII whitespace), re-run by
the post-review check, none git lands on reads as no switch
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened: `hooks/worktree-guard.py` (`tracked_in_any_remote`, `_refs`,
`_fetched_as`, the head of `classify`, the `sessions_in_tree` signature),
`tests/test_guard_resolves_the_tree_it_judges.py` (`run`, `_git`, `_commit`,
`CARRIERS`, `_a_repository`, `_where_git_checkout_lands`,
`_a_dirty_clone_beside`, `test_a_newly_read_checkout_in_front_takes_no_question_away`,
the two new cases), `tests/conftest.py` (`_build_repo`, `repo`,
`load_hook_module`), `bin/test`, `docs/worktree-guard-spec.md:785-800`,
`phases/phase-4.md:40-80`, `rounds/round-3-report.md`, `rounds/round-3.md`,
`changelog.md`, the ledger fragment's R5 row, the range's diff, the three
commit messages, and issue #811.
