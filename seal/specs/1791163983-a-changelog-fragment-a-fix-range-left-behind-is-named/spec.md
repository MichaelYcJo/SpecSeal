# Feature Specification: a changelog fragment a fix range left behind is named (#797)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

A work item's `changelog.md` fragment is written by the build's last phase.
Every commit after the build — a fix pass, a fix written after the last round,
a commit integrating a sibling's squash — can change what the work item ships,
and nothing asks whether the fragment still says so. The release gathers the
fragment verbatim, so a fragment left behind ships as a false release note.
0.18.2 shipped three such fragments until #795 corrected them by hand
(`git show b4cb22e1`). This work item adds one notice that names the commits a
fragment was left behind by, and one rule, with one home, that says a commit
changing what ships brings the fragment along.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | a check that stops a run on an honest state costs the unattended run a stop; the measurement below decides notice versus refusal against that goal |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | a test seen red, a stated failure direction, a prompt budget. This arm prints and never refuses, so its failure direction is *allow more* and its prompt budget is zero |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | the fragment's path is `seal/specs/<work-item-id>/changelog.md`; the release gathers it into `changelog/<X.Y.Z>.md` |
| `docs/the-record-layout.md` (the file as a whole) | the home of the new rule: it already owns which file a change writes, and it sits far under the `Document line ceiling` (245 of 1000 lines) where `docs/round-record-spec.md` sits at 945 |
| `docs/round-record-spec.md` §*The fix range — `Fix range`* | a fix range is `` `<a>..<b>`, N commits `` written by `round-record close`; ends this repository cannot see are the ordinary state after a squash and print, never fail |
| `skills/implement/SKILL.md` §3 | an agent's or a skill's instructions are observable behaviour — so `agents/` and `skills/**/*.md` count as behaviour paths here |
| `skills/implement/SKILL.md` §5 and `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | a fix pass adds no mechanism, so the rule this item adds has to be stated once by this item, not by a fix pass that meets the problem later |
| `docs/the-record-layout.md` and `tests/test_no_passage_is_pasted_into_a_second_file.py` | a rule has one home; every other carrier links to it in fewer than 25 shared words |
| `tests/test_the_rules_have_one_owner.py` | the shape that pins "one owner, several links" — the new rule takes a row there |
| `skills/code-review/scripts/chain_check.py#pact_notices` | the precedent for an arm whose every finding is a notice and whose exit status is the one the tree has without it |
| `skills/code-review/scripts/round_record.py#run_check`, `skills/verify/scripts/broad_gate.py` arm 4 | `close` and `seal` both run `chain_check` and print its output, so an arm in `chain_check` is read at every close, at the seal, and in CI |

## The measurement — notice, not refusal

Executed on 2026-10-05 over this clone's whole object store (every ref,
including `refs/backup/*`), by two scratch scripts kept outside the tree. Two
readings: the one the ticket asked for (per fix range), and the one the chosen
design actually makes (per work item, at its branch tip).

### Per fix range

Every round record any ref ever carried, its `Fix range` row read and both
ends resolved.

| Count | What |
|---|---|
| 242 | committed round records carrying a `Fix range` range, over 101 work items |
| 6 | ends this clone cannot see (squashed and never backed up) |
| 236 | resolved, over 99 work items |
| 153 | of those changed a behaviour path (`hooks/`, `bin/`, `templates/`, `docs/`, `skills/*/scripts/`, `agents/`, `skills/**/*.md`) |
| 86 | of those 153 also changed the item's `changelog.md` in the same range |
| 67 | changed a behaviour path and left the fragment untouched — 66 distinct, since one stray `round-2-report.md` repeats `round-1.md`'s range |

The 66, split by what happened next. The first two rows are executed; the last
three are **read** — judged from the range's commit subjects and a keyword
search of the fragment as it shipped, never against the full diff, so their
answerer for a finer split is a measurement nobody has taken (it would not
change the decision below).

| Count | What happened | Label |
|---|---|---|
| 6 | lagging, corrected by hand at the 0.18.2 release by #795 (`1791119071` r1; `1791119072` r1–r2; `1791128260` r1–r3) | executed |
| 11 | the fragment changed later on the branch, before the squash (`1790039346`, `1790076070`, `1790260564`, `1790260566`, `1790550712`, `1791076831`) — lagging when the range closed, caught in the run | executed |
| 21 | honest: record paperwork, a docstring, a comment, wording inside a document, a portability fix — nothing a release-note reader would see | read |
| 14 | likely lagging: a new refusal, a new exception, a changed printed line that the shipped fragment does not state | read |
| 14 | unclear from the subjects | read |

### Per work item, at its branch tip — what the chosen arm would print

The arm below asks one question per work item rather than per range: did a
commit after the build change a behaviour path after the fragment's last
change? Simulated at every backed-up branch tip whose `routing.md` names that
branch, with a round 1 and a fragment: 42 work items, 0.15.6 to 0.18.2.

| Count | What |
|---|---|
| 18 | silent — the fragment changed after the last behaviour commit |
| 24 | the notice would print |
| 3 | of the 24: the three #795 corrected — **all three lagging items of 0.18.2 print, and none of the three honest ones does** (`1791119068`, `1791119069`, `1791119070` are silent) |
| 1 | of the 24: `1790550712`, whose backed-up tip is older than its squash, and the squash `6329af1d` did change the fragment — lagging, caught before the merge |
| 6 | of the 24, read: likely lagging — `1790993137`, `1791019474`, `1790993140`, `1790635414`, `1790635412`, `1790993138` (new refusals, new exceptions, a changed line end). `1791019474`'s branch never reached `main` under its own id — its work shipped inside `1791076833`'s squash `d671a439` — so five of the six fragments shipped: two in 0.16.0, three in 0.18.0 |
| 9 | of the 24, read: honest — `1791019477`, `1791076836`, `1790993139`, `1791076834`, `1791076835`, `1790655302`, `1790690762`, `1791089603`, `1791090130` (documents, comments, a refactor, a compatibility fix) |
| 5 | of the 24, read: unclear — `1790645290`, `1790550714`, `1791076833`, `1791076832`, `1790635415` |

### What decides it

**A refusal would have stopped 24 of 42 runs, and at least 9 of those — up to
14 — for a fragment that needed no change.** Per range the honest share is at
least 21 of 66. Each of those is a stop in a run that was meant to go to its
pull request unattended, and the honest answer has no spelling a refusal could
accept without a new record field. So the arm **prints and never refuses**,
which is also the issue's stated tolerance: *a notice where an unchanged
fragment is honest is acceptable*.

What the notice buys: the three fragments #795 corrected by hand would each
have been named at their own close, at their seal and in CI, before the
release. What it does not buy: a release that ships anyway. Five of the six
likely lagging fragments above shipped, in 0.16.0 and 0.18.0, with nothing
naming them.

## Scope

### In — the check (box 1)

- **One arm in `skills/code-review/scripts/chain_check.py`**, run for every
  work item declared `through the review chain` that the check already
  judges. Notices only; the exit status is the one the tree has without it.
- **Why `chain_check` and neither of the other two named homes.** It is the one
  reader every relevant moment already runs: `round_record.py close` runs it
  after writing a record (`run_check`), `round_record.py seal` runs it after
  writing the `Broad gate` cell and `broad-gate` prints that output, and CI
  runs it on every push. An arm in `close` alone never sees a commit made after
  the last close — a post-review fix, an integration commit. An arm in
  `broad-gate --preflight` is printed nowhere on a passing preflight (its arms'
  output goes to `--keep-output` files), would not run at a close, and would
  share `skills/verify/scripts/broad_gate.py` with sibling C (#789).
- **How each kind of range is found**, all from the tree and the records:

  | Kind | Found by |
  |---|---|
  | post-build, the whole question | first-parent, non-merge commits in `<round 1's Target SHA>..HEAD`. Round 1 reviewed the build's end, so the build's own commits are never read |
  | a fix range | each record's `Fix range` row `<a>..<b>`, when both ends resolve — used to say which round a named commit belongs to |
  | after the last round (a post-review fix, a post-seal fix) | the post-build commits no record's `Fix range` holds and that come after the last record's range end (its `Target SHA` where its `Fix range` reads `none`) |
  | an integration after a sibling's squash | the merge of the base is skipped (`--no-merges`, and `--first-parent` keeps the sibling's own commits out of the walk); the item's own commits after the merge are post-build commits like any other |

- **A behaviour path is any path outside the `seal/` root and outside a
  directory named `tests`.** Not a list of this repository's directories:
  `chain_check` ships to every opted-in repository, whose layout is not this
  one's, and the issue's own list had already missed `bin/` and `agents/`,
  which is an enumeration rotting before it shipped (contract §12). On this
  repository the negative definition flags 69 ranges where the positive list
  flags 67 (the extra paths are `.github/`, `README*.md`, `CONTRIBUTING.md`
  and `CLAUDE.md`). `agents/` and `skills/**/SKILL.md` count, by
  `skills/implement/SKILL.md` §3.
- **The notice names each late commit** — short SHA, which round's fix range
  holds it or that it came after the last round, and its behaviour paths — and
  says the fragment still stands as the release will gather it, that nothing
  is owed where it still says what ships, and which section owns the rule.
- **Silent**, with the reason in the arm's docstring, where: the declaration is
  `straight to the PR` (no rounds, so no post-build boundary); there is no
  `round-1.md` yet; round 1's `Target SHA` does not resolve (squashed); no
  `changelog.md` is tracked at HEAD (local mode commits none, and whether an
  item owes a fragment is not this question).
- **No cutoff.** It refuses nothing, so there is no history for it to fail.
- **The module docstring's *What it reads* table gains the row**, and
  `docs/the-record-layout.md` gains the section that owns the rule and ends
  `Enforced by:` the arm and its cases.

### In — the instructions (box 2)

- **The rule, stated once**, in a new section of `docs/the-record-layout.md`:
  a commit after the build that changes what the work item ships updates its
  `changelog.md` in the same range, whoever writes it — the smith's fix pass,
  a fix written after the last round, an integration commit after a sibling's
  squash — and `chain-check` names the commits a fragment was left behind by.
- **Three carriers link to it, never restate it**: `agents/smith.md`'s
  paragraph *A fix pass is not a phase, and its record is the round record*,
  `skills/implement/SKILL.md` §5, and `skills/code-review/orchestration.md`
  §*Orchestrator: a fix pass resumes the implementer* — the last one naming the
  orchestrator's own two acts (a fix written after the last round, an
  integration commit) since no smith writes those.
- **A row in `tests/test_the_rules_have_one_owner.py`'s `RULES`** pins the
  owner's sentence and each carrier's link.

### Out, and why

| Left out | Why |
|---|---|
| a refusal, or an acknowledgment row in the round record that would silence an honest notice | the measurement above; an acknowledgment is a new record field, and a notice that only prints needs none. Revisit only if a later measurement shows the notice ignored |
| `broad-gate --preflight` printing the notice | a passing preflight prints one line by design (`broad_gate.py` §*`--preflight` runs arms 2 to 7 alone*), and the seal right after it prints `chain_check`'s output. Changing that is sibling C's file |
| the release's gather reading the fragments | at the release the feature branches are squashed and their commits do not resolve, so nothing there can name a commit |
| correcting the five likely-lagging released notes of 0.16.0 and 0.18.0 | amending a released `changelog/<X.Y.Z>.md` is the owner's open decision in `seal/follow-up.md` (the two rows on `changelog/0.12.2.md`); `questions.md` Q1 records the default |
| a work item declared `straight to the PR` | it has no round, so no line separates the build from what came after it |
| a merge commit's own conflict resolution | `--no-merges` skips it, so a behaviour change written only inside a merge is not named. Written beside the arm, not left to be found |
| test paths other than a `tests` directory (`__tests__/`, `*_test.go`, `*.spec.ts`) | a test-only commit there prints a notice it did not need to. One notice line, no stop; the predicate is the one `round_record.py#under_tests` already uses |
| `README.md`, `README.ko.md` | neither describes what `chain-check` reads or prints (searched: no match for `chain-check` or `chain_check`), so neither has a sentence this change makes false |
| `docs/round-record-spec.md` | the arm reads the `Fix range` row and writes nothing into it; the row's own table there stays true |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a fix range leaves the fragment behind | Given a chain item with round 1 at the build's end and a fix range whose commit changes `hooks/x.py`, the fragment untouched / When `chain_check` runs / Then a notice names that commit, `round 1's fix range`, `hooks/x.py`, the fragment's path and the owning section, and the exit status is unchanged | a case in a new test module, seen red against the tree before the arm exists |
| S2 the fragment is brought along | Given S1 plus a commit in the same or a later range that changes `changelog.md` / When `chain_check` runs / Then this arm prints nothing | a case, seen red by making the arm ignore the fragment's touch |
| S3 non-behaviour paths | Given a fix range changing only `tests/…` and `seal/…` paths / When it runs / Then nothing is printed | a case |
| S4 instructions count | Given a fix range changing only `agents/smith.md` or a `skills/x/SKILL.md` / When it runs / Then the notice prints | a case |
| S5 after the last round | Given a commit after the last record's fix range changing `bin/x` / When it runs / Then the notice attributes it to *after the last round* | a case |
| S6 an integration | Given a merge of the base bringing a sibling's commit that changes `hooks/y.py`, and no own commit after it / When it runs / Then nothing is printed; Given one own commit after the merge changing `hooks/y.py` / Then that commit alone is named | two cases |
| S7 silent states | Given no `round-1.md`; or round 1's `Target SHA` unresolvable; or no `changelog.md` at HEAD; or `straight to the PR` / When it runs / Then this arm prints nothing and the rest of the check is unchanged | one case per state |
| S8 never a refusal | Given every case above / Then `chain_check`'s exit status equals the one the same tree has with the arm removed | asserted in each case, and S1 seen red with a deliberate `errors.append` |
| S9 the rule has one home | Given `docs/the-record-layout.md`'s new section / Then `tests/test_the_rules_have_one_owner.py` holds its sentence and the three links, and `tests/test_no_passage_is_pasted_into_a_second_file.py` passes with no new `BASELINE` entry | the two modules run; the owner's sentence deleted to see the first red |
| S10 the notice text is pinned | contract §14 | the case asserts the sentence's load-bearing words, seen red with them changed |

## Data & interfaces

- New: one function in `chain_check.py` returning `([], notices)` like
  `pact_notices`, called once per declared chain work item from `main`, after
  the record walk. No new CLI flag, no new record field, no template change.
- Read: `seal/specs/<id>/rounds/round-1.md` `Target SHA`; every record's
  `Fix range`; `git log --first-parent --no-merges --name-only` over
  `<target>..HEAD` — one `git` call per work item.
- Ledger: rows for the arm and the rule go in
  `seal/ledger/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named.md`.

## What this changes for the three sibling items

Nothing they must do. The arm prints only, and none of them runs it until it
is merged *and* reaches them: CI reads the chain check in each pull request's
own tree, and `round-record` on the PATH is the installed plugin (0.18.2) —
so a sibling sees the notice only after it merges the release branch in
behind this item, and then only as a printed line. The rule in box 2 is worth
following in their fix passes now anyway, since it is the 0.18.2 incident;
that is the orchestrator's call, not a requirement. This item touches neither
`broad_gate.py` (C) nor `hooks/` (B) nor `evidence_check.py` (A).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-05 by framer, before the build.
