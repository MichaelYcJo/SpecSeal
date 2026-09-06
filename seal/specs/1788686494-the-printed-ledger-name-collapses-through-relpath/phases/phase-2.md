# 1788686494-the-printed-ledger-name-collapses-through-relpath — phase 2

<!-- seal/specs/1788686494-the-printed-ledger-name-collapses-through-relpath/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `afcece0` — the five sites routed. `79e00b8` carries the three cases and the module docstring correction they forced; the records ride the commit that closes the phase |
| Ran by | |

## What this phase was asked

Route every site in the class through `display_name`, where the class is the
**property** — *a ledger path turned into a name a person reads* — and not the
line numbers issue #163 listed, all of which phase 1 had moved. Say what method
enumerated the class and how the enumeration is known to be complete rather
than merely larger. Write the integration case in
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` beside
`test_the_path_returned_is_the_one_the_pattern_named`, reusing its symlink
fixture: the printed header names the file that was **read**, POSIX branch
only, seen red first against `relpath` in that position, both runs reported.
Write the source-reading case that refuses a future `relpath` on a ledger path
in the module phase 1 created, because without it the helper is a convention
and a convention is what this defect already was. Write the records — rows into
the ledger fragment and never `seal/ledger.md`, the changelog fragment and
never `CHANGELOG.md`, this record, `plan.md`'s Status cell, and `overview.md`,
whose `## Not verified` section is machine-read and has one shape.

Three facts arrived with labels. **Executed at `885acf8`**: the phase-1 module
at 18 passed, the three evidence-check modules at 148 passed, `uvx ruff` clean
on both changed files, and `.venv` has no `ruff` module. **Read**: the call is
`display_name(ledger, root)`, two arguments. **Read, and named as a trap**: the
scan-suggestion site appends `.replace(os.sep, "/")` after its `relpath` and
`display_name` deliberately does not, so an enumeration reaching it owes a
written judgement rather than a silent skip. **Unverified**: whether any site
in the class renders a path that is not one of `resolve_patterns`' returns —
to be settled by reading.

Issue #163 also asks that round 13's notes in `seal/ledger.md` be extended or
a row of this work item's own be written; the fragment rule settles it as the
fragment, and `seal/ledger.md` is to be touched only for a row this change
falsifies, which would be a removal rather than a re-point.

## What this phase found

**The class has five members, and the issue's four came from a grep.** A grep
for `relpath(ledger` finds `check_ledger` L1131, `migrate` L1389, `reverify`
L1514 and `main`'s per-ledger header. The fifth is `main`'s `--ledger narrowed
this run` loop, whose variable is `path` rather than `ledger`. That is not a
naming accident worth one line of commentary — it is the whole reason the
enumeration had to stop being lexical.

**Enumerated by data flow, and the completeness argument is a closure rather
than a search.** Three steps, each mechanical:

1. **The entry points.** A ledger path is produced by `resolve_patterns` and
   by nothing else in the program. There are exactly three calls: `main`'s
   `--ledger` arm, `main`'s default arm, and `skipped_by_narrowing`'s own
   `resolve_patterns(default_patterns(root))`. Everything downstream is one of
   those lists, an element of one, or something derived from an element.
2. **The closure of names.** From those seeds, four propagation rules taken to
   a fixed point: a name assigned from a seed call; a loop or comprehension
   variable over a carrier; the *i*th parameter of a function called with a
   carrier in position *i*; and the assignment target of a call to a function
   that returns an expression mentioning a carrier. That yields `ledger` in
   `check_ledger`, `migrate` and `reverify`; `ledgers`, `ledger`, `missed` and
   `path` in `main`; `candidates`, `read`, `p` and `path` in
   `skipped_by_narrowing`; and the parameters of `read`, `write_atomic`,
   `file_identity` and `display_name`.
3. **The sink set, which is where the first mechanical pass was wrong.** Asked
   for every `print` and every `append` mentioning a carrier, the analysis
   returned **four** of the five — it missed `check_ledger` L1131, which is a
   `return`. Widening the question from *which calls render* to *every
   statement in which a carrier appears at all* closed it: twenty-four
   statements, classified as opening the file (5), identity and set arithmetic
   (5), rebinding or passing along (7), a false positive on the name `path`
   in `main`'s `--map` loop (2), and **rendering for a person (5)**.

Completeness rests on step 1 and on step 3 being a partition. A ledger path
cannot reach a person without appearing in some statement, and every statement
holding a carrier name was listed and classified — so the argument is *the set
is closed under the ways a value moves*, which is checkable, rather than *I
looked and found no more*, which is not. The near-miss at step 3 is the
evidence that the method has teeth: a plausible sink set returned a strictly
larger answer than the grep and still missed a site.

**The enumeration is kept as a case, not as a paragraph.**
`test_no_ledger_path_reaches_relpath` recomputes the closure against the
checker's source on every run and refuses `relpath` on any carrier. That is
what `plan.md` said breaks in six months — a sixth site added by someone
reaching for what the standard library offers — and it is now caught whatever
the new variable is called. Reverting all five sites at once turns it red
naming each with its function and line.

**The detector over-reaches, and that is the safe direction.** The return rule
marks `main`'s `findings` (tuples whose first element is a coordinate) and
`resolve_patterns`' `key` (an inode pair). Neither is a path, so the check can
raise a false alarm and can never let a real site through. A false alarm costs
a reader a minute; a false pass is #163 again. This is the thing a reviewer
should attack first.

**A green empty list is a counterfeit seal, so it has its own case.**
`test_no_ledger_path_reaches_relpath` passes on an empty offender list and
would pass just as quietly if the analysis had degraded. Changing the seed from
`resolve_patterns` to a name no call uses was run as a mutation: the carrier
set went empty, the refusal case **passed**, and only
`test_the_refusal_above_can_actually_fail` went red. That case asserts the
carrier set still holds the six real names and puts one site back in a copy of
the source to prove the detector fires.

**The unverified fact, settled by reading, has a wrinkle worth keeping.** Every
rendered path is a `resolve_patterns` return — but not all from the same call.
The four `ledger` sites render the list `main` built; the fifth renders
`skipped_by_narrowing`'s own default-discovery list, whose spelling comes from
`seal_home(root)`. In local mode from a linked worktree that sits outside the
worktree root, so those names print absolute — which is exactly the case phase 1
pinned as `test_a_local_mode_home_outside_the_tree_prints_absolute`, now
reachable from a real run rather than only from the unit. The site carries a
comment saying so, because the next reader will otherwise wonder why the
variable is not called `ledger`.

**The scan-suggestion site: judged out, and pinned out both ways.** The data-flow
closure does not reach it at all — `full` and `repo` are not carriers — so the
grep-based worry that a session might route it through the helper is answered
by construction rather than by discipline. Three separate reasons keep it on
`relpath`, any one of which is sufficient: `os.walk` composes the path downward
from the root it was given, so there is no `..` to fold; the result is compared
against `rel`, a path spelled the way a ledger row spells one, so it must be
normalised rather than preserved; and it appends `.replace(os.sep, "/")`, which
`display_name` deliberately does not do, so routing it through the helper would
change what Windows prints for every `(moved?)` hint.
`test_the_scanned_source_path_is_not_a_ledger_and_keeps_its_relpath` holds both
directions — the site still calls `relpath`, and the detector does not classify
it — and each was seen red under its own mutation.

**The integration case asserts by inode before it asserts by spelling.** A
string compare pins today's rendering; joining the printed name back under the
root and stat-ing it is the claim itself. Red against `relpath` it reads
`assert (16777232, 185959477) == (16777232, 185959475)` — the header opening a
different file from the one the run read, which is the whole of #163 as an
assertion. The fixture's premise is asserted rather than assumed: were
`ledger.md` and `x/ledger.md` one inode, every assertion below would pass
against `relpath` too. An earlier draft had that guard stat the *printed* name
rather than the file that was read, which made it fire under the mutation with
a message describing something that had not happened; the red run is what
exposed it.

**Ordering the assertions was a real finding, not a tidy-up.** The first draft
compared spellings first, so under the mutation the spelling assertion fired
and the inode assertion — the one carrying the claim — never ran. A case whose
strongest assertion is unreachable in the failure it was written for is pinning
the weaker thing.

**`seal/ledger.md` was left alone, and the decision is contestable.** Editing
four units moved four anchors, so six rows in the shared ledger read DRIFTED
where the base read two. No row is falsified: they claim things about drift
verdicts, `--reverify` semantics, migration and unreadable ledgers, and a
rendering line moving inside each unit changes none of them. Re-verifying was
attempted and reverted, for two measured reasons. `--reverify` cannot be
scoped to a row — the run re-stamped `templates/config.md` and
`round_record.py#swallowed`, two rows that drifted **before** `885acf8` and
that this work item never opened, and certifying those is the silent re-stamp
the ledger design refuses. And doing it honestly means bumping the `Checked`
date on **thirteen** rows belonging to other work items, in the one file the
fragment rule exists to keep branches out of. DRIFTED is the correct state and
says *go re-read the claim*; it is named in `overview.md`'s Not verified with
an answerer. The alternative — re-stamp the four and hand-revert the two — is
one edit away if a reviewer prefers it.

**The base already fails this gate.** `evidence_check.py .` at `885acf8` exits 1
on `templates/config.md` and `round_record.py#swallowed`. Both are outside this
work item's scope and predate it.

**Phase 1's module docstring had gone stale and was corrected here.** It said
the source-reading case was phase 2's — true when written, false once the case
landed beside it — and it repeated the issue's "four sites". Both now say what
is there.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `os.path.relpath` at the five sites that render a ledger name | `display_name`, which phase 1 added; the rule they carried implicitly is now `test_no_ledger_path_reaches_relpath`, which holds it for sites that do not exist yet |
| phase 1's module docstring sentence assigning the source-reading case to phase 2 | the same docstring, rewritten to describe the two kinds of case now in the module |
