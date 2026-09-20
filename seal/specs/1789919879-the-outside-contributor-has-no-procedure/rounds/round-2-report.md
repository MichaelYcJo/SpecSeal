# 1789919879-the-outside-contributor-has-no-procedure — round 2 report

| Field | Value |
|---|---|
| Round | 2 — the verifying round |
| Target SHA | `dc81224f` |
| Reviewed range | `c8e7a9d0..dc81224f`, four commits — the fix diff, not the branch |
| Base | `origin/release/v0.12.1` |
| Reviewed in | a `git clone --no-local` of the repository at the target SHA |
| Reviewed by | warden on claude-opus-5[1m] |

This round verifies round 1's seven verdicts and judges the surface the fix
pass created. Round 1's coordinates were carried; none of its conclusions
were. Every verdict below is re-derived — six of the seven by reverting the
fix and watching the symptom return.

## What the account claimed, and what the code said

| Claimed | Found |
|---|---|
| `evidence_check.py .` exit 0, `0 refused`, anchors `1368 ok · 0 drifted · 0 broken` | **Executed at `dc81224f` in a clone: exit 0**, `0 refused · 0 drifted · 0 external`. Confirmed |
| `chain_check.py --baseline origin/release/v0.12.1` exit **0**, its only remaining notices being `Broad gate: not yet` and the `Pass`-beside-`nobody` pair | **Executed: exit 1**, not 0. The two messages are exactly the ones described and nothing else prints. `chain_check.py` returns `1 if errors else 0`, so at least one of the two is an error rather than a notice; unchecking `Pass` in the record leaves it at 1, so the error is the broad-gate one. See correction 10 — this is the expected state of the branch, not a defect |
| 8 narrow modules, 300 passed | Not re-run. Round 1 executed the same set at `c0b00d08` and the fix diff touches one of them; that one was re-run below |
| `test_the_contributor_has_a_procedure` 17 passed | **Executed: 17 passed.** Confirmed |
| `test_the_release_check_watches_what_ships` 35 unchanged | **Executed** with four modules together: 139 passed, no failures. Confirmed |
| `survivor-check` exit 0 over both ranges | **Executed at `dc81224f`: exit 0** over `c8e7a9d0..HEAD` and exit 0 over `origin/release/v0.12.1...HEAD`. Confirmed, with one observation in correction 9 |
| `unverified-check` exit 0 with 3 open rows | **Executed: exit 0.** Confirmed |
| A backticked name inside a single-line HTML comment that opens part-way along a table row is refused, at exit 2 | **Executed, confirmed, and narrowed** — finding D below. The open half of the follow-up row's question is settled: the cause is the mid-line opening, not the table cell |

## Round 1's seven rows — is each actually closed

### 1 · 🔴 the three refused lines — **closed**

**Executed.** In a clone at `dc81224f`, the three `NAME NOT IN TREE` markers
were stripped by pattern from `overview.md` (one) and `phases/phase-5.md`
(two), the checker re-run, and the files restored from kept bytes:

```
[baseline]         exit 0   705 names read · 0 refused
[markers stripped] exit 2   712 names read · 3 refused
                   NOT-IN-TREE  …/overview.md:19       read_body
                   NOT-IN-TREE  …/phases/phase-5.md:69  read_body
                   NOT-IN-TREE  …/phases/phase-5.md:114 read_body
[restored]         exit 0   705 names read · 0 refused, porcelain empty
```

Exactly three refusals return, all of the one retired name, at exactly the
three coordinates round 1 found. The markers are on the right lines.

**What each marker costs, measured rather than read.** The marker exempts the
LINE, so 712 − 705 = **seven** compound names stop being read, not three. The
four extra are `issue_claims_check.py`, `PR_BODY` and `body_from` twice. Every
one of them is claimed unmarked elsewhere in the same work item —
`spec.md:66`, `overview.md:59`, `phases/phase-5.md:71`–`74` — so no true
absence is hidden anywhere, which is the property the checker's own docstring
states: the marker exempts the line rather than the name, and the same name
still has to exist everywhere else it is claimed.

Choosing the marker over stripping the backticks was right. These three lines
are records OF a name the tree does not have, which is the case the marker
exists for, and a line that passes only through an invisible absence of
backticks goes red again at the next reformat — phase 5 paid that once
already.

### 2 · 🟡 A1 and the missing divergence row — **closed**

`spec.md` A1 now states what the message ships, with an HTML comment at the
row holding what the frame asked for and why it was not followed.
`overview.md` gained the fourth divergence row. The pin is untouched and green
(139 passed, `test_the_refusal_still_serves_the_release_and_puts_it_first`
among them).

One consequence worth stating, because it is invisible: the A1 comment opens
part-way along the table row, so by finding D below **every backticked name
inside it is read as a claim**. They all resolve today. One of them is
`test_the_refusal_still_serves_the_release_and_puts_it_first`; rename that
case without touching `spec.md` and the record arm goes exit 2 on a line
inside a comment that `skills/evidence-check/SKILL.md` says is not read.

### 3 · 🟡 "each one exits early on any other base" — **closed**, with correction 8

Re-derived against `.github/workflows/hygiene.yml` rather than against the
record. The three steps the new sentence names as release-only do carry the
guard — the version step at line 66, the changelog step at 116, the
ledger-fold step at 134 — and the three it names as always-on carry none: the
issue-claim step at 52, the unverified tally at 158, the round-record check at
199. Every clause of the replacement is true.

### 4 · 🟡 the ledger job is a second refusing check — **closed**

The heading now reads *The two checks that can ask you for something you do
not have*, the `seal/ledger/` row stops implying drift is the whole story and
points below, and a paragraph states the repair. Round 1's executed grounds
were carried, not re-run: a renamed anchor gives `1 broken` at exit 2. What I
re-read is the coordinate behind it — `.github/workflows/test.yml`'s
`if [ "$code" -ge 2 ]; then exit "$code"; fi` — and the new paragraph against
`CLAUDE.md` §*a change writes fragments, never the shared file*, whose
sentence about a removal it matches: the row is removed from `seal/ledger.md`
and the new claim written into a work item's fragment.

### 5 · 🟡 the staleness guard, and whether widening the budget was right — **closed, and the right call**

**Executed, six mutations, each alone and restored from kept bytes.** For each
of the three surfaces, both directions of the case:

```
[unmutated]                                     3 passed
README.md               concrete branch         1 failed, 2 passed
README.md               convention gone         1 failed, 2 passed
README.ko.md            concrete branch         1 failed, 2 passed
README.ko.md            convention gone         1 failed, 2 passed
PULL_REQUEST_TEMPLATE   concrete branch         1 failed, 2 passed
PULL_REQUEST_TEMPLATE   convention gone         1 failed, 2 passed
[restored]                                      3 passed, porcelain empty
```

So the case binds all three surfaces, and in both directions — it goes red
when a concrete branch appears and red again when the convention disappears
altogether. That is confirmed rather than inherited from `phase-*.md`.

**The judgment.** Widening the budget by one parametrized case was right, and
deferring would have been the worse answer. `agent-contract` §12 binds every
agent and names this shape exactly: the branch wrote the release-branch rule
onto three surfaces and guarded none of them, so a fix at the coordinate it
was found on leaves the class open. The three surfaces are ones this branch
created, the pull request template is the one a maintainer reads on every
pull request, the case went into the module phase 1 already wrote rather than
a third module, and the widening is recorded as a divergence instead of being
presented as compliance. Correction 8 is about the wording of those grounds,
not about the decision.

### 6 · 🟡 "CI will refuse a contribution aimed at `main`" — **closed**

Re-derived by reading **every** step of `.github/workflows/hygiene.yml`
against the case the new sentence describes: a contribution based on `main`
that touches nothing under a shipping root.

| Step | What it does on that pull request |
|---|---|
| a change to what ships must move the version | `-z "$ships"` early return, line 78 — exit 0 |
| every changelog fragment reached the released file | runs (base is `main`); a tree branched from `main` carries no ungathered fragment |
| every ledger fragment folded | runs; same reason |
| the milestone this release claims | runs, and returns 0 at `release_completeness_check.py:255`–`261`: `version_of(head)` is `None` for a branch that is not `release/vX.Y.Z`, so it prints *nothing to judge* |
| wording this branch removed is not still standing | exits 0 when the base is `main`, line 243 |
| round record · unverified tally · issue claims · mode row · CLAUDE.md block | always-on, and ask nothing of a branch that declared nothing |

So "nothing catches the wrong base at all" is true, and I could find no step
that falsifies it. The instruction above the rationale is unconditional and
stays unconditional; only the rationale moved.

### 7 · ⬜ the `fi` matcher — **the refusal stands; two of its three premises do not**

`answered` is a legitimate verdict and a round is not a list of orders, so the
decision is the right one. The reasoning recorded beside it does not hold as
written.

- **"Loosening a pin on a workflow guard is a gate change under
  `CONTRIBUTING.md` §*What a change to a gate must carry*."** That section's
  own scope sentence, at `CONTRIBUTING.md:36`–`38`, says the higher bar
  "covers anything under `hooks/` or `.github/workflows/`".
  `tests/test_the_release_check_watches_what_ships.py` is under neither. The
  rule cited does not reach the file the fix would have edited.
- **"With no red behind it."** A red is two lines away: put a trailing comment
  on the step's closing `fi`, watch the pin report an unclosed guard on a
  guard that closes, apply the widening, watch it pass, then re-run round 1's
  three mutations to confirm it still catches them.
- **What does hold, and is the honest ground.** A careless widening is
  genuinely unsafe. `first(lambda line: line == "fi")` widened to
  `line.startswith("fi")` also matches a line opening `file=`, which reads the
  guard as closing before it does — a false GREEN on the exact mutation the
  case exists to catch. Only an anchored form is safe, and choosing between
  the forms is a judgment a fix pass working from a ⬜ the reviewer marked
  *noted, not asked for* should not make unasked. Grepped
  `.github/workflows/` and `hooks/`: no `fi` in the tree carries a trailing
  comment today.

This is a correction to the grounds in a record, not a request to reopen the
finding.

## The surface round 1 never reviewed

### D · the follow-up's measured claim — **confirmed, and its open question settled**

`seal/follow-up.md`'s new row is right, and it can be narrowed before the
owner reads it. **Executed** — six shapes appended in turn to one record file
in the clone, each run alone, the file restored from kept bytes:

| The shape | Result |
|---|---|
| table row, comment opens MID-LINE, name backticked inside it | **exit 2, REFUSED** |
| table row, the same name bare | exit 0, not read |
| PROSE line, comment opens MID-LINE, name backticked inside it | **exit 2, REFUSED** |
| prose line, comment OPENS the line | exit 0, not read |
| table row, comment OPENS the line | exit 0, not read |
| the same name inside a fenced block | exit 0, not read |

So the row's claim reproduces, and the disjunction it leaves open — "the aside
rule either does not reach a comment that opens mid-line, or does not reach
one inside a table cell" — **loses its second half**: a comment that opens a
line is an aside even inside a table row, and a mid-line comment is read even
in plain prose. The whole of it is `claim_lines`'s
`stripped.startswith("<!" "--")` in `skills/evidence-check/scripts/evidence_check.py`,  <!-- the literal this line quotes opens an aside the record reader never closes, so quoting it whole swallowed every heading below — split, per this round's own correction 3. -->
which asks whether the comment opens the line. The fence half of the skill's
sentence holds.

This is not a finding — the row is honest, names the owner, and says the
question is outside this work item either way. It is a fact the row can
absorb, and it matters beyond this branch for the reason the row gives:
moving a name into an explaining comment is the repair a session reaches for.

### The new cases, judged as code

The parametrized case is correct. Two assertions, opposite directions, and
each message names the surface and the offending strings rather than the
expression that failed. `CONVENTION_SURFACES` builds the template path with
`os.path.join`, which is right for the windows leg of the suite. The pattern
`release/v\d+\.\d+\.\d+` matches the three-component convention
`docs/branch-and-release.md` writes, and a release-candidate suffix is caught
by the same prefix.

The corrected docstring and assertion message on
`test_the_section_warns_about_the_check_that_can_still_refuse` are right: the
case still pins only the survivor check's `survivors.md`, which is the one
whose own refusal names a file to create, and the docstring now says why.

## Findings

Nothing in the fix diff needs a fix. What follows is eight corrections, five
of them in records and three in prose the branch ships, plus one deferred
candidate. None of them is counted in `Needs a fix`.

### ⬜ 8 · the divergence row claims an intent `spec.md` S5 does not state

**Location** — `seal/specs/1789919879-…/overview.md:22`.

The row's grounds close with "No new module — a third module is what S5 was
really rationing". `spec.md` S5 reads "`tests/` | **Two pins**, each seen red
before the thing it pins exists", and names them. It rations pins, not
modules. The row is labelled a divergence and says the budget was widened, so
nothing is smuggled past a reader — but the last clause asserts an intent the
document it cites does not carry, and a later reader weighing a fourth pin
would take it as settled that the budget was only ever about modules.

The repair is to drop the reinterpretation and let the divergence stand on
§12, which is what actually carries it.

### ⬜ 9 · "The others run on every pull request and pass" is false read alone

**Location** — `CONTRIBUTING.md:49`.

Read as a standalone sentence it is wrong in the same direction round 1's 🟡 3
was: the `ledger` job and the survivor check are also others that run on every
pull request, and neither always passes. The heading 24 lines below says so in
as many words.

What keeps this off the fix list is that the sentence does not stand alone.
The apposition immediately after it names the three steps meant — the
round-record check, the unverified tally, the issue-claim report — and the
sentence after that sends a maintainer to the row rather than to the summary.
A contributor who reads to the end of the section meets both refusing checks
under a heading that counts them. It is a residue of the shape, not the shape.

### ⬜ 10 · the handed-over `chain-check` exit code does not reproduce

**Location** — the round-2 spawn prompt, against `skills/code-review/scripts/chain_check.py`.

**Executed at `dc81224f` in a clone, exit code read directly:** `chain_check.py
--baseline origin/release/v0.12.1` exits **1**, not 0. Its output is exactly
the two messages the prompt describes and nothing else. `main()` returns
`1 if errors else 0`, so at least one of the two is an error; unchecking the
record's `Pass` box leaves the exit at 1, which puts the error on the
broad-gate side.

This is the expected state of the branch rather than a defect. Both messages
clear by the two acts that are already scheduled: this round's record names
the fixes it checked, and the sealer's one run fills the `Broad gate` cell.
It is worth correcting because a session reading `exit 0` would take the chain
as green apart from advisory notices, and decide the branch was closer to
ready than it is.

### ⬜ 11 · a blank line splits the divergence table into two

**Location** — `seal/specs/1789919879-…/overview.md:20`.

Line 20 is empty, between the first two rows and the last three. A blank line
ends a markdown table, so rows 21 to 23 form a second table with no header and
no separator, and GitHub renders them as a paragraph of literal pipe
characters. The three rows this fix pass cared most about are the ones that
stop rendering.

Nothing goes red: `unverified_check.py` reads only the `## Not verified`
section, and the record arm reads lines rather than tables. The repair is to
delete line 20.

### ⬜ 12 · the approval line is true, and it silences the notice whose subject is that truth

**Location** — `seal/specs/1789919879-…/plan.md:7`.

The line states what is true. It reads *Approved 2026-09-20 by the routing
batch and by no reader of this plan, when `smith` was spawned.*, it matches
`routing.md` — the `automation` preset, answered 2026-09-20 by the owner,
before the first edit — and it claims no signature. The paragraph below it
says in as many words that nobody read the plan clause by clause. On the
question this round was asked, the answer is that it states what is true
rather than a signature nobody gave.

What it costs is the machine-readable half. `chain_check.py`'s `APPROVED_RE`
matches any filled line, and the notice it suppresses says the approval line
"is the only durable trace that a person read the plan". After this edit the
checker prints nothing for a plan nobody read, and the disclaimer lives only
in prose no checker reads. The placeholder is the state 61 of 71 `plan.md`
files in this tree are in, and that measurement is the checker's own reason
for reporting rather than refusing — which makes the placeholder the honest
state here, not an omission to be filled.

**Deferred candidate, not a fix for this round.** The general question is
whether `chain_check.py` should be able to tell a filled-but-negative approval
from an approval, or whether the rule should be that an unread plan keeps its
placeholder. That is a change to what a gate reads and belongs in an issue of
its own — `seal/follow-up.md` is where this repository files exactly this
shape, and the owner answers it. Naming it here so the precedent is not set
silently: this is the first plan in the tree to answer the notice by filling
the line with its own negation.

### ⬜ 13 · the two survivor exemptions currently match nothing

**Location** — `seal/specs/1789919879-…/survivors.md`.

The file is honest about the run it describes, and I confirmed that run.
**Executed at `57f1dacd`**, which is the tree the fix pass was standing on:
`survivor_check.py --range c8e7a9d0..HEAD` reports exactly the three places
the file claims, the two `phases/phase-5.md` quotes matching verbatim with
their shared-phrase scores, and the test module's docstring as the third. That
third one was the real survivor and was corrected at `88809c29`; grepped, and
no contributor-facing surface still calls the survivor check "the one check".

At `dc81224f` the same range reports nothing at all, with or without
`--exempt`, because `88809c29` rewrote `overview.md:19` a second time and the
shared phrases dissolved with it. So both exemption rows are inert today. That
is harmless — the file parses, the run exits 0, and an exemption that stops
applying degrades to *reported again* rather than to silence — but a later
reader should not conclude the file is holding anything back right now.

### ⬜ 14 · a docstring that names a case by its position

**Location** — `tests/test_the_contributor_has_a_procedure.py:18`.

"**The last case in this file reaches past `CONTRIBUTING.md`**" is true today
and becomes false, silently, the moment anyone appends a case below it. Naming
the case instead costs one phrase.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The three refused record lines | `seal/specs/1789919879-…/overview.md:19`, `…/phases/phase-5.md:69`, `…/phases/phase-5.md:114` | answered | **Actually closed.** Executed: markers stripped → exit 2 with exactly 3 refusals of the one retired name at exactly those 3 coordinates; restored → exit 0, `0 refused`, porcelain empty. The markers silence 7 compound names, not 3 — the other 4 are all claimed unmarked elsewhere in the same work item, so nothing true is hidden |
| 2 | 🟡 A1 and the unrecorded divergence | `seal/specs/1789919879-…/spec.md` A1; `…/overview.md` | answered | **Actually closed.** A1 states what the message does, the divergence row exists, the pin is untouched and green. The A1 comment opens mid-line, so its names are read as claims — all resolve today; see finding D |
| 3 | 🟡 The exemption list's reason | `CONTRIBUTING.md` §*What a contribution is not asked for* | answered | **Actually closed.** Re-derived against `.github/workflows/hygiene.yml`: guards at lines 66, 116, 134; none at 52, 158, 199. Every clause true. Residual wording is correction 9 |
| 4 | 🟡 The ledger job is a second refusing check | `CONTRIBUTING.md` §*The two checks that can ask you for something you do not have* | answered | **Actually closed.** Heading, row and new paragraph all changed. Round 1's executed grounds carried; re-read `.github/workflows/test.yml`'s `-ge 2` exit and checked the repair sentence against `CLAUDE.md` §*a change writes fragments* |
| 5 | 🟡 The staleness guard covers two of four surfaces | `README.md`, `README.ko.md`, `.github/PULL_REQUEST_TEMPLATE.md` | answered | **Actually closed, and widening the budget was the right call.** Executed 6 mutations, 3 surfaces × 2 directions, each red alone, restored byte-identical. §12 names this shape, the surfaces are this branch's own, no new module, recorded as a divergence. The grounds wording is correction 8 |
| 6 | 🟡 The rationale promises an unconditional refusal | `.github/PULL_REQUEST_TEMPLATE.md`, `README.md`, `README.ko.md` | answered | **Actually closed.** Re-derived by reading every hygiene step for a `main`-based contribution touching nothing shipped, including the milestone step, which returns 0 for a non-release head branch. No step falsifies the new sentence |
| 7 | ⬜ The guard pin reads `fi` by exact equality | `tests/test_the_release_check_watches_what_ships.py:271` | answered | **The refusal stands; the recorded reasoning does not.** The gate bar's own scope at `CONTRIBUTING.md:36`–`38` is `hooks/` and `.github/workflows/`, which does not reach a file under `tests/`; and a red is constructible in two lines. What holds is that a careless widening matches a line opening `file=` and would be a false green — a judgment a fix pass should not make unasked. Correction 7 above |
| 8 | ⬜ The divergence row claims an intent S5 does not state | `seal/specs/1789919879-…/overview.md:22` | open | Read `spec.md` S5: "Two pins", naming both. The row's "a third module is what S5 was really rationing" asserts more than the cited document says |
| 9 | ⬜ "The others run on every pull request and pass" is false read alone | `CONTRIBUTING.md:49` | open | Read: the `ledger` job and the survivor check are also always-on and can refuse. The apposition after it names the three meant and the heading 24 lines below counts both refusing checks, which is why this is residue rather than the shape |
| 10 | ⬜ The handed-over `chain-check` exit code does not reproduce | `skills/code-review/scripts/chain_check.py`, against the spawn prompt | open | Executed at `dc81224f`, exit code read directly: **1**, not 0, with exactly the two described messages. Unchecking `Pass` leaves it at 1, so the error is the broad-gate one. Expected state, cleared by this round's record and the sealer's run |
| 11 | ⬜ A blank line splits the divergence table into two | `seal/specs/1789919879-…/overview.md:20` | open | Read: line 20 is empty, so rows 21–23 are a headerless table and render as literal pipes. No checker reads that section. Delete line 20 |
| 12 | ⬜ The approval line is true and silences the notice about that truth | `seal/specs/1789919879-…/plan.md:7` | open | Read against `routing.md` — the date, the preset and the owner all match, and no signature is claimed. `APPROVED_RE` matches any filled line, so the notice that calls the line "the only durable trace that a person read the plan" now prints nothing for a plan nobody read. Deferred candidate, not a fix here |
| 13 | ⬜ The two survivor exemptions currently match nothing | `seal/specs/1789919879-…/survivors.md` | open | Executed at `57f1dacd`: the range reports exactly the three places the file claims, quotes matching verbatim. At `dc81224f` it reports nothing, with or without `--exempt`, because the carrier text was rewritten again. Harmless; the record is honest about the run it describes |
| 14 | ⬜ A docstring names a case by its position | `tests/test_the_contributor_has_a_procedure.py:18` | open | Read: "the last case in this file" becomes false silently when a case is appended below it |

## Executed probes

Every row ran in a `git clone --no-local` of the repository at `dc81224f`,
never in the working tree. Probe scripts were named test_tmp_marker_exactness,
test_tmp_surface_pin and test_tmp_aside_region — written without backticks,
since they are not in the tree — and the clone, its virtualenv and all three
are deleted.

| What was run | Result |
|---|---|
| `bin/test tests/test_the_contributor_has_a_procedure.py tests/test_the_release_check_watches_what_ships.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_a_record_states_what_the_tree_has.py -q` | **139 passed** |
| `bin/test tests/test_the_contributor_has_a_procedure.py -q` | **17 passed** — the count the fix pass claims |
| `evidence_check.py .`, exit code read directly | **exit 0** — `705 names read · 0 refused · 0 drifted · 0 external` |
| The same with all three `NAME NOT IN TREE` markers stripped | **exit 2** — `712 names read · 3 refused`, one retired name at each of the 3 coordinates round 1 found |
| The same after restoring the three files from kept bytes | **exit 0**, `0 refused`; `git status --porcelain` empty |
| The new parametrized case, unmutated | 3 passed |
| The same, a concrete `release/v0.12.1` written into `README.md` alone | **1 failed**, 2 passed |
| The same into `README.ko.md` alone | **1 failed**, 2 passed |
| The same into `.github/PULL_REQUEST_TEMPLATE.md` alone | **1 failed**, 2 passed |
| The convention removed entirely from `README.md` alone | **1 failed**, 2 passed |
| The same from `README.ko.md` alone | **1 failed**, 2 passed |
| The same from `.github/PULL_REQUEST_TEMPLATE.md` alone | **1 failed**, 2 passed |
| All six restored from kept bytes, case re-run | 3 passed; porcelain empty |
| Aside probe — a compound backticked name in a mid-line HTML comment, inside a table row | **exit 2, REFUSED** |
| The same name bare on the same table row | exit 0, not read |
| The same mid-line comment on a PROSE line | **exit 2, REFUSED** |
| A comment OPENING the line, prose | exit 0, not read |
| A comment OPENING the line, inside a table row | exit 0, not read |
| The same name inside a fenced block | exit 0, not read |
| `chain_check.py --baseline origin/release/v0.12.1`, exit code read directly | **exit 1** — the two described messages and nothing else. Finding 10 |
| The same with the record's `Pass` box unchecked, then restored | exit 1 both times; the error is the broad-gate one |
| `unverified_check.py --baseline origin/release/v0.12.1 seal/specs/` | **exit 0** |
| `survivor_check.py --range origin/release/v0.12.1...HEAD` | **exit 0** |
| `survivor_check.py --range c8e7a9d0..HEAD` at `dc81224f`, with and without `--exempt` | **exit 0** both ways — 1107 files against 17 removed sentences, nothing standing, nothing exempt |
| The same at `57f1dacd` | **3 places still standing** — the two `phases/phase-5.md` quotes `survivors.md` exempts, and the test docstring that was corrected. Finding 13 |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** `agent-contract` §2 leaves all three to the sealer, and this round ran none of them. The rounds settle here, so what comes due is the sealer's spawn |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `chain_check.py` should tell a filled-but-negative approval line from an approval, or whether the rule should be that an unread plan keeps its placeholder — finding 12 | a `seal/follow-up.md` row or an issue of its own; it is a change to what a gate reads and carries `CONTRIBUTING.md`'s higher bar | the repository owner |
| The aside region's mid-line blindness — already filed at `3323e433`, and finding D narrows it | `seal/follow-up.md`, the row this branch added | the repository owner |

## Paste-ready fixes

Nothing here is asked for. These are the three corrections whose repair is a
single substitution, offered so a later pass does not have to reconstruct
them.

### 11 — the blank line inside the divergence table

Delete line 20 of `seal/specs/1789919879-the-outside-contributor-has-no-procedure/overview.md`.
It is an empty line between the row ending `Round 1 🔴 1. -->` and the row
beginning `| The order of the two causes in the refusal |`. Nothing else
changes.

### 8 — the divergence row stops claiming an intent S5 does not state

```
# seal/specs/1789919879-the-outside-contributor-has-no-procedure/overview.md,
# the S5 row, final clause
old: No new module — a third module is what S5 was really rationing
new: No new module: the case went into the module phase 1 already wrote. S5
     budgets two pins and this is a third, which is the divergence this row
     records
```

### 14 — the docstring names the case instead of its position

```
# tests/test_the_contributor_has_a_procedure.py, module docstring
old: **The last case in this file reaches past `CONTRIBUTING.md`.**
new: **`test_no_contributor_facing_surface_names_a_concrete_release_branch`
     reaches past `CONTRIBUTING.md`.**
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

📋 code-review applied
· read: `seal/specs/1789919879-…/rounds/{round-1.md,round-1-report.md}`,
  `…/{overview,spec,plan,routing,changelog,survivors}.md`,
  `…/phases/phase-5.md`; `seal/ledger/1789919879-….md`; `seal/follow-up.md`;
  `CONTRIBUTING.md`, `README.md`, `README.ko.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`; `.github/workflows/hygiene.yml` in full,
  `.github/workflows/test.yml`; `.github/scripts/release_completeness_check.py`;
  `skills/evidence-check/scripts/evidence_check.py` §`claim_lines` and its
  corpus walk, `skills/evidence-check/SKILL.md` §*What counts as a claim*;
  `skills/code-review/scripts/chain_check.py` §`APPROVED_RE` and `main`,
  `skills/code-review/scripts/survivor_check.py` §*the exemptions*;
  `skills/verify/scripts/unverified_check.py`;
  `tests/test_the_contributor_has_a_procedure.py`,
  `tests/test_the_release_check_watches_what_ships.py`,
  `tests/test_docs_line_wrap.py`; `bin/test`
· executed: the 26 rows of §*Executed probes*, all in a `git clone --no-local`
  at `dc81224f`; nothing was written in the working tree
· unverified: the full suite, the repository-wide lint and the typecheck — the
  sealer answers, and this round leaves nothing open in front of it. Whether
  the repaired refusal reads well in GitHub's rendered error panel, which
  `overview.md` already books to whoever next opens such a pull request
