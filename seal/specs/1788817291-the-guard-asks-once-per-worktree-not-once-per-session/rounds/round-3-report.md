# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 3, report

| Field | Value |
|---|---|
| Target SHA | `3287c78` |
| Base | `62b2d2e` |
| Branch | `fix/237-the-guard-asks-once-per-worktree-not-once-per-session` |
| Worktree | `/Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-237` |
| Probes ran in | a `git clone --no-local` of that worktree, checked out at `3287c78` |
| PR | not yet |
| Broad gate | not yet — the full suite, the repository-wide lint and the typecheck are the orchestrator's, once, after the rounds settle (`agent-contract` §2) |

## What this round was asked

Round 3 is the verifying round over round 2's fixes, and the last round this
work item gets: the record written after it ends the run whatever it finds.
The surface is `git diff 62b2d2e..3287c78`, whose substance is `bba7dab` and
`f4db784`. Rounds 1 and 2 are recorded and closed, and their verdicts are
inherited.

The round was pointed first at the fix pass's **refusal** of round 2's
paste-ready fix for finding 1, with instructions to apply the report's version
and see what moves rather than to read the argument. Then at the boundary
sentence the second fix draws, with the 32 enumerated command-word shapes to be
re-derived and a 33rd to be looked for; at what the boundary deliberately
excludes; at the 1260-combination sweep and its 230 / 0 / 64; at the
strengthened *never silent* property and whether it can still go red; at the
prompt budget and its new residual; at the five invariants; at finding 8's
replacement figure; and at the two `❓` standing with the repository owner.

The bound was stated: the change weakens a guard and is to be reviewed as such,
an unfounded finding spends the item's last round, and a round that opens
nothing needing a fix does not consume the cap.

## What this round found, in the order the findings cause each other

The code is right. Every claim the fix pass made about behaviour reproduced,
including the two it made against its own instructions, and the three findings
below are all in the prose that describes the code rather than in the code.

- **The refusal was correct, and the executed cost of the alternative is
  larger than the fix pass claimed.** Applying the report's hoist loses four
  denies, not one class of one. The two that matter are the ones the fix pass
  named: in a session that already holds a consent record, attempt 1 in both
  the idle and the detection-unusable state collapses from a `deny` naming the
  idle sessions and offering *split into a worktree* to a bare `ask` reading
  *A worktree creation already ran in this repository this session*.

- **The shipped shape moves nothing it should not.** Across 96 cells of
  (command × tree state × record state × attempt), exactly two verdicts differ
  between `62b2d2e` and `3287c78`, and both moved from `ask` to `deny`. No deny
  was lost anywhere.

- **The boundary holds, and the documents that describe it do not.** Nothing
  outside the word `git` collects an `allow` — that is the whole security
  claim, and it survived 55 command-word shapes. But the paragraph stating it
  gets three things wrong: how many spellings pass, what verdict the refused
  ones get, and what the replacement figure for `576` counts.

Findings 1, 2 and 3 are all in `docs/worktree-guard-spec.md`, which is a
shipped document rather than this work item's paperwork. Findings 4 and 5 are
under `seal/specs/` and are corrections.

---

### 1 · 🟡 The allow surface is a class, and the document states it as a list of five

`docs/worktree-guard-spec.md:158-160`

> Re-enumerated by construction over 32 command-word shapes, exactly five are
> vouched for, and all five are the word `git` after lexing: `git`, `\git`,
> `'git'`, `"git"` and `g"i"t`.

The reason given is exactly right — a command word the lexer hands back as the
word `git` runs what `git` runs — but the reason describes an unbounded family
and the sentence describes five members of it. Executed over 55 shapes with a
consent record present, **17 answer `allow`**, not five. The twelve the
document does not name:

    g'i't   gi"t"   "g"it   \g\i\t   g\it   ''git
    ""git   git""   git''   "gi"t    g''it  ;git

Every one of them lexes to the word `git`, so **the guard's boundary is not
breached** and no fix is owed to the code. `;git worktree add …` is the one
that is not a plain quoting spelling; bash rejects it as a syntax error before
anything runs, so it too costs nothing.

Why it matters: this paragraph is the one a person opens to audit what an
`allow` can cover, and *by construction* claims the 32 shapes were built to
cover the class. They were not — the enumeration contains `g"i"t` and misses
`g'i't`. A reader checking a new spelling against the list of five concludes it
is refused when it is allowed.

### 2 · 🟡 Five of the shapes the document says answer `ask` are ones the guard is silent on

`docs/worktree-guard-spec.md:160-163`

> Every path, every expansion (`~/git`, `*/git`, `gi*`, `$GIT`, `` `which git` ``),
> a different case, a trailing slash, every wrapper and every leading
> assignment falls to `ask`.

Executed, with a record present, `<word> worktree add ../wt f` for each:

| Shape | Documented | Measured |
|---|---|---|
| `./git` · `../git` · `bin/git` · `/usr/bin/git` · `/tmp/evil/git` · `.//git` · `/git` · `~/git` · `*/git` | `ask` | `ask` |
| `gi*` · `$GIT` · `` `which git` `` · `GIT` · `git/` | `ask` | **silent** |
| `sudo git` · `env git` · `command git` · `time git` · `VAR=1 git` · `PATH=/tmp/evil git` | `ask` | `ask` |
| `nice git` · `xargs git` | `ask` (as "every wrapper") | **silent** |

Silent is not a weaker verdict here — none of these gets an `allow`, and the
guard abstaining leaves the harness's own permission settings to decide, which
is its ordinary answer for anything that is not a git invocation. What is wrong
is the sentence. This document draws the `ask`/`silent` distinction on purpose
two paragraphs further down (*"Why the Agent/Task path is silent rather than an
allow"*), so writing `ask` where the guard says nothing is a claim a reader
cannot check against the code.

The same list, with the same five shapes, is in the ledger row at
`seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md:9`.

### 3 · 🟡 `230` is a cell count at a different grain from the `1260` it is presented as a subset of

`docs/worktree-guard-spec.md:207-216`

> Re-derived after the change over 21 command shapes × 5 tree states × 2 shell
> directories × 2 record states × 3 attempts, which is **1260 combinations**:
> 230 of them are cells the writer records for, and **0** of those reach a
> verdict that lets the command run without the creation question. With both
> round-2 fixes reverted the same sweep finds **64**.

The filter that decides a writer cell is `worktree_consent.creation_directory(command, cwd)`
resolving a repository. It reads the command and the shell directory and
nothing else — not the tree state, not the record, and not the attempt. So the
writer-cell subset of the 1260 is closed under the 3-attempt axis, and **any
honest count of it is divisible by 3**. 230 is not. The figure the sentence
needs is 690; 230 is the count one axis up, at (shape × cwd × state × record),
where the grid is 420 rather than 1260.

Reproduced by construction rather than argued. A sweep over the same five axes
with 21 shapes of my own:

    shapes=21 states=5 cwds=2 records=2 attempts=3
    product = 21*5*2*2*3 = 1260;  walked = 1260
    writer cells at (shape,cwd,state,record) grain = 240
    writer cells including attempts                = 720      (= 240 × 3)
    holes = 0

240 × 3 = 720 is the relation the shipped sentence is missing; 230 × 3 = 690.
The `64` in the same sentence *is* at the combination grain — it is described
as "the second and third attempt", which is two of the three — so one sentence
carries two grains and presents both against 1260.

This is round 2's finding 8 one level down. That finding was that `576` did not
reconstruct from the three axes it named; the replacement reconstructs at the
top (21 × 5 × 2 × 2 × 3 = 1260) and stops reconstructing at the subset.

Two things make it harder to catch than it should be, and both belong in the
fix. The 21 shapes and the fifth tree state are not in the tree: the committed
case `test_the_guard_is_never_silent_where_the_writer_records` sweeps 12 shapes
× 4 states × 2 directories × 3 attempts and carries **no record-state axis at
all**, so nothing a reader can run reproduces 230, 64, or the 1260. `agent-contract`
§5 is the rule — an aggregate is a fact whose coordinate cannot be opened.

The same figure is at `seal/specs/…/spec.md:97-101` and in the ledger row at
`seal/ledger/…-the-guard-asks-once-per-worktree-not-once-per-session.md:11`.

### 4 · ⬜ `spec.md` says the claim was true of two rows where every other document says one

`seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:85`

> **And *"the three concurrency rows all deny"* was true of two of them.**

It was true of one. The next sentence but one in the same paragraph says so —
*"Only the ACTIVE row denies unconditionally"* — and so do the ledger row
(`…/1788817291-….md:12`, "was true of one of the three") and the code comment
at `hooks/worktree-guard.py:2117` ("**Only one of those three denies
unconditionally.**"). The "two" reads as a copy of the "two choice sites" in
the following clause.

Under `seal/specs/`, so it is a correction and out of `Needs a fix`. Written up
because a reader who stops at the bolded sentence takes away the opposite of
what the fix established.

### 5 · ⬜ The `❓` paragraph's "closed either way" list was not updated for round 2

`seal/specs/…/pr-notes.md:182` (§4, *Platform honesty*)

> Two of the three shapes that made this urgent are closed either way:
> `sudo git worktree add …` and `env LD_PRELOAD=… git worktree add …` no longer
> get an allow at all.

The claim the round was asked to judge — that finding 2's repair **reduces**
what rides on the two open questions — is **true**. The unfavourable answer to
*does a hook `allow` outrank `permissions.deny`* costs a user who denied
`Bash(git worktree add:*)` an override, and it can only cost that for commands
that reach an `allow`. Round 2 removed six more shapes from that set
(`./git`, `../git`, `bin/git`, `/usr/bin/git`, `/tmp/evil/git`, `~/git`, `*/git`),
so strictly less rides on the answer than did at `62b2d2e`.

What is missing is that §4 still says it in round 1's terms. The sentence names
two shapes closed either way when it is now eight. Both `❓` rows in
`overview.md` §*Not verified* still name the repository owner as answerer, and
§4 still states the fallback (the consented row answers `ask` rather than
`allow`, one word at one site), so nothing is unowned.

Under `seal/specs/`, so it is a correction and out of `Needs a fix`.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 "exactly five are vouched for" is a property of one enumeration, not of the boundary — 17 command-word spellings answer `allow`, and the twelve unnamed ones are quoting spellings of the same word | `docs/worktree-guard-spec.md:158` | open | **Executed** over 55 shapes with a record present: `g'i't`, `gi"t"`, `"g"it`, `\g\i\t`, `g\it`, `''git`, `""git`, `git""`, `git''`, `"gi"t`, `g''it` and `;git` all answer `allow` alongside the five named. **Read**: each lexes to the word `git`, so the security boundary is intact and the fix is owed to the sentence only. `;git` is a bash syntax error and runs nothing |
| 2 | 🟡 Five of the shapes the paragraph says "falls to `ask`" answer `silent`, and this document draws that distinction on purpose | `docs/worktree-guard-spec.md:160` · `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md:9` | open | **Executed**: `gi*`, `$GIT`, `` `which git` ``, `GIT` and `git/` answer `silent`; so do `nice git` and `xargs git`, which "every wrapper" covers. The nine path shapes and the four `WRAPPERS` entries do answer `ask`. None of the fourteen gets an `allow`, so nothing is open in the code |
| 3 | 🟡 The `230` writer cells cannot be a subset of the `1260` combinations — the filter is attempt-independent, so the count must divide by 3, and 230 does not | `docs/worktree-guard-spec.md:207` · `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:98` · `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md:11` | open | **Executed**: a 21 × 5 × 2 × 2 × 3 sweep of my own axes walks 1260, and gives 240 writer cells at the (shape, cwd, state, record) grain and 720 including attempts. 230 × 3 = 690 is the figure the sentence needs. **Read**: `creation_directory(command, cwd)` reads no state, record or attempt; the `64` in the same sentence is at the combination grain, so one sentence carries two. The 21 shapes and the record axis are in no artifact in the tree — the committed sweep case has 12 shapes, 4 states and no record axis |
| 4 | ⬜ `spec.md` says *"all deny" was true of two of them* where the ledger, the code comment and its own next sentence say one | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:85` | open | **Read.** `seal/ledger/…:12` says "true of one of the three"; `hooks/worktree-guard.py:2117` says "Only one of those three denies unconditionally"; `spec.md:91` says "Only the ACTIVE row denies unconditionally". Under `seal/specs/`, so out of `Needs a fix` |
| 5 | ⬜ §4's "two of the three shapes are closed either way" was not updated for round 2's six path shapes, though the claim that finding 2's repair reduces what rides on the `❓` is true | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md:182` | open | **Read.** Both `❓` rows in `overview.md` §*Not verified* name the repository owner, and §4 still states the fallback. **Executed**: the allow surface at `3287c78` is strictly smaller than at `62b2d2e` — the seven path-qualified shapes now answer `ask`. Under `seal/specs/`, so out of `Needs a fix` |
| 6 | 🟢 Refusing round 2's paste-ready fix for finding 1 was right, and the alternative costs four denies rather than one | `hooks/worktree-guard.py:1450` · `:2033` · `:2076` | answered | **Executed** as a variant, one session id per cell: hoisting `judge_creation` above rows 1-b and 2 turns four cells from `deny` to `ask`. With a record present, attempt 1 in the idle state goes from *"Other Claude sessions may exist in this tree…"* with the two options to *"Attempting to create a worktree… A worktree creation already ran in this repository this session"* — the fix pass's exact claim, measured. Same in the detection-unusable state. Two more at attempt 2 with no record |
| 7 | 🟢 Every `deny` verdict is where it was, and the two verdicts that moved got stronger | `hooks/worktree-guard.py:1392` · `:1450` · `:2138` | answered | **Executed**: 96 cells over 4 commands × 4 tree states × 2 record states × 3 attempts, `62b2d2e` against `3287c78`. Two moved, both `ask` → `deny` (`git switch feature/x && git worktree add ../wt f`, attempt 2, idle and detection-unusable, no record). Denies lost: **0**. **Read**: `before_ask` runs after `respond("deny", …)`, which exits, and is `None` whenever `creation_at` is `None`, so a command with no creation on it cannot reach it |
| 8 | 🟢 Whatever the writer records for, the guard denies it or names the creation in its `ask` — re-derived, not accepted | `hooks/worktree-guard.py:2138` · `tests/test_the_guard_asks_once_per_session.py:525` | answered | **Executed** over my own 21 shapes × 5 tree states × 2 shell directories × 2 record states × 3 attempts: 1260 walked, 720 writer combinations, **0** holes. With both round-2 fixes reverted the same sweep finds 152 holes, all of them attempts 2 and 3 in the idle and detection-unusable states — the same class the fix pass reports at 64 against its own shape list |
| 9 | 🟢 The strengthened property is falsifiable, and fails for the reason it names | `tests/test_the_guard_asks_once_per_session.py:525` · `hooks/worktree-guard.py:1757` | answered | **Executed** as a mutation: with `judge_creation`'s origin line changed to *"A worktree operation is under way."*, attempt 3 in both the idle and the detection-unusable state becomes a hole. Attempts 1 and 2 stay `deny`, so the case fails on exactly the cell the strengthening was written for |
| 10 | 🟢 The prompt budget is unchanged, and the new residual is stated honestly | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md:88` · `:114` | answered | **Executed**: six `git worktree add ../wt f` in one session on a clean single-stream tree, the record written after the first — `deny, allow, allow, allow, allow, allow`. Six `/usr/bin/git worktree add ../wt f` with a record present — `ask` every time, which is what the fourth residual says. The residual names the trade rather than the shape, and the six calls the release run made carry no path |
| 11 | 🟢 The five invariants hold in the no-record state | `hooks/worktree-guard.py:1684` · `:2012` · `:2033` · `:2076` | answered | **Executed**, no record: single-stream creation `deny` with the `git switch` steer; ACTIVE switch `deny`; idle switch `deny` at attempt 1 then `ask`; detection-unusable switch `deny` at attempt 1 then `ask`; ACTIVE creation `ask`. The pure-switch ladder is byte-identical to `62b2d2e` in all 24 of its cells |
| 12 | 🟢 What the boundary deliberately excludes cannot be created inside a command it vouches for | `hooks/worktree-guard.py:370` · `:461` | answered | **Read**, and the argument holds for a reason the docstring does not state: `only_creates_a_worktree` requires **every** segment to be a `git worktree add`, so a command that plants a `git` on `PATH` or defines a shell function named `git` fails on the planting segment before the running one is reached. A leading `PATH=…` fails test 1, and `$PATH` fails `ELSEWHERE`. **Read** on bash semantics: `'git'`, `"git"` and `\git` suppress alias expansion, so each is at least as narrow as bare `git` — refusing them would buy nothing |
| 13 | 🟢 The two cases round 2's record names as new units are sound as code | `tests/test_the_guard_asks_once_per_session.py:307` · `:470` | answered | **Read.** Both assert on the English reason text, which `tr()` would render in Korean on a machine exporting `LANG=ko`; `tests/conftest.py:38` pins `SPECSEAL_LANG=en` for exactly that reason, and the note there says the author's machine exports `ko` session-wide. `test_a_spent_choose_budget_…` asserts the property rather than a verdict per attempt, which is what lets it survive the ordering the fix chose. **Executed**: the module is 35 passed at `3287c78` |
| 14 | 🟢 Ledger anchors resolve and no real user path is left anywhere under `seal/` | `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md` · `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8` | answered | **Executed**: `bin/evidence-check` exits 0 — 807 ok, 0 drifted, 0 broken, this fragment 10 ok. `bin/test tests/test_no_real_identifiers.py -q` is 2 passed. Round 1's report now reads `/Users/x/orca/…` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_guard_asks_once_per_session.py -q` at `3287c78` | `35 passed in 9.61s` |
| 55 command-word shapes, `<word> worktree add ../wt f`, record present | 17 `allow` (the five named plus twelve quoting spellings and `;git`), 20 `ask`, 18 `silent` |
| Newline, `$'…'` and trailing-separator forms | `'gi\nt'`, `"git\n"`, `$'git'`, `$'\x67it'` and `git\nworktree add …` all refuse the allow |
| 21 shapes × 5 states × 2 directories × 2 records × 3 attempts at `3287c78` | 1260 walked · 240 writer cells at the grid grain · 720 including attempts · **0 holes** |
| The same sweep with `tokens[0] != "git"` reverted to a basename and both `before_ask=` removed | **152 holes**, every one of them attempt 2 or 3 in the idle or detection-unusable state |
| 96 cells, `62b2d2e` against `3287c78` | 2 verdicts moved, both `ask` → `deny`; **0 denies lost** |
| 96 cells, `3287c78` against round 2's paste-ready hoist | **4 denies lost** by the hoist, two of them attempt 1 with a record present |
| Mutation: `judge_creation`'s origin line no longer names the creation | 2 holes appear; the strengthened case goes red on attempt 3 in both states |
| Six creations in one session, clean single-stream tree | `deny, allow, allow, allow, allow, allow` |
| Six `/usr/bin/git worktree add ../wt f` with a record present | `ask, ask, ask, ask, ask, ask` |
| `bin/evidence-check` | exit 0 · `total: 807 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `bin/test tests/test_no_real_identifiers.py -q` | `2 passed in 0.25s` |

The probe file was `tests/test_tmp_round3.py` and `tests/test_tmp_round3b.py`
in a `git clone --no-local` of the branch, and both are deleted. The three
source variants (basename restored · `before_ask` removed · `judge_creation`
hoisted · the origin line muted) were built as copies of `hooks/` in a
temporary directory, never in the tree under review, which is clean.

## Inherited coordinates

Carried from rounds 1 and 2 and used rather than re-derived. No verdict was
inherited; every one below was re-established this round.

| Coordinate | What it saved |
|---|---|
| `hooks/worktree-guard.py#only_creates_a_worktree` — the two-test bound | where the command-word test lives and why `ELSEWHERE` is separate from it |
| `hooks/worktree-guard.py#choose` — the once-per-session-per-direction marker | that the deny is spent and the ask is not, which is the whole shape of finding 1 |
| `hooks/worktree_consent.py#creation_directory` — the writer's own read | the filter the sweep's writer-cell count is taken over, which is what finding 3 turns on |
| `tests/conftest.py:38` — `SPECSEAL_LANG=en` | that English text assertions are pinned rather than accidental |
| `overview.md` §*Not verified* — the two `❓` and their answerer | that both are already routed to the repository owner |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a hook `ask` can be auto-answered, and whether a `PostToolUse` payload means the call ran | `overview.md` §*Not verified*, already deferred at round 1 | the repository owner, against the harness |
| Whether a `permissions.deny` rule outranks a hook `allow` | `overview.md` §*Not verified*, already deferred at round 1; `pr-notes.md` §4 carries the fallback | the repository owner, against the harness |
| A shell function or alias named `git`, or a `git` earlier on `PATH` | documented as excluded in `hooks/worktree-guard.py#only_creates_a_worktree`; judged sound at finding 12 | nobody — closed, not deferred |

## Paste-ready fixes

Finding 1 — `docs/worktree-guard-spec.md:158-160`, replacing the sentence that
counts the spellings with the class it meant:

```markdown
The boundary the code implements is *a command word carrying no separator, so
the shell resolves it on `PATH`*. Anything with a `/` in it names a file this
hook cannot identify. What is vouched for is the CLASS the lexer reduces to the
word `git`, which is unbounded: `git`, `\git`, `'git'`, `"git"`, `g"i"t`,
`g'i't`, `\g\i\t`, `''git` and every other spelling of the same word all pass,
and every one of them runs exactly what `git` runs. Re-enumerated over 55
command-word shapes, 17 pass and all 17 are that word after lexing.
```

Finding 2 — `docs/worktree-guard-spec.md:160-163`, the same paragraph's second
half, replacing the single verdict with the two the guard actually gives:

```markdown
Nothing else is vouched for. Every path (`./git`, `/usr/bin/git`, `~/git`,
`*/git`), every wrapper `cmdline.WRAPPERS` reads past and every leading
assignment falls to `ask`; a shape `cmdline.parse_git` does not recognise as a
git invocation at all (`gi*`, `$GIT`, `` `which git` ``, `GIT`, `git/`) leaves
the guard silent, which hands the command to the harness's own permission
settings. Neither reaches an `allow`, which is the property that matters. What
that costs is one prompt on `/usr/bin/git worktree add …`, which is the trade
already made for `$` and `>`: a wrong deny spends a prompt, a wrong allow signs
for a binary nobody identified.
```

Finding 3 — `docs/worktree-guard-spec.md:207-216`, with the subset count put at
the grain of the sweep it is a subset of:

```markdown
**The property, measured rather than the shapes.** Whatever the writer would
record for, the guard has either denied it — which stops the whole command
line — or put the creation question in the text of its `ask`. Re-derived after
the change over 21 command shapes × 5 tree states × 2 shell directories × 2
record states × 3 attempts, which is **1260 combinations**. The writer records
for 23 of the 42 (shape, directory) pairs, and those pairs carry **690** of the
1260: **0** of them reach a verdict that lets the command run without the
creation question. With both round-2 fixes reverted the same sweep finds **64**
holes, all of them the second and third attempt at a switch-then-create in the
idle or detection-unusable state.
```

The same sentence is at `seal/specs/…/spec.md:97-101` and in the ledger row at
`seal/ledger/…-the-guard-asks-once-per-worktree-not-once-per-session.md:11`,
and both take the same replacement. The fix is not complete until the sweep
that produced the three numbers is reproducible from the tree: either the
committed case gains the record-state axis and the fifth tree state and the
document cites it, or the document says the sweep was a probe and gives the 21
shapes.

Finding 4 — `seal/specs/…/spec.md:85`, one word:

```markdown
**And *"the three concurrency rows all deny"* was true of one of them.** Round
```

Finding 5 — `seal/specs/…/pr-notes.md:182`, the count and the list:

```markdown
  redesign. Eight of the shapes that made this urgent are closed either way:
  `sudo git worktree add …`, `env LD_PRELOAD=… git worktree add …`, and the six
  path-qualified spellings round 2 closed (`./git`, `../git`, `bin/git`,
  `/usr/bin/git`, `/tmp/evil/git`, `~/git`, `*/git`) no longer get an allow at
  all — so strictly less rides on this answer than did at `62b2d2e`.
  **Answerer: the repository owner**, against the harness.
```

## For the record

Needs a fix: yes — 1, 2 and 3, all in `docs/worktree-guard-spec.md`
Loses a record or crashes: no
Contract changes: choose → guard_worktree_creation, main; only_creates_a_worktree → judge_creation
New units: test_a_path_qualified_git_carries_no_allow (depth 1); test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned (depth 1); judge_the_creation (depth 2)

## Proof

Files opened this round:

- `hooks/worktree-guard.py`
- `tests/test_the_guard_asks_once_per_session.py`
- `tests/conftest.py`
- `docs/worktree-guard-spec.md`
- `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/changelog.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/overview.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-2.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-2-asked.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-2-fixes.md`
- `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-2-report.md`
- `seal/config.md`
- `CONTRIBUTING.md`
- `CLAUDE.md`
