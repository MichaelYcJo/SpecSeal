# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — review round 3

| Field | Value |
|---|---|
| Target SHA | 3287c78 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed — 2605 passed, 2 skipped; `ruff check .` and `ruff format --check .` both exit 0 |
| Fixes checked by | no fixes to check |
| Contract changes | `choose` → `guard_worktree_creation`, `main`; `only_creates_a_worktree` → `judge_creation` |
| New units | none |
| Needs a fix | yes — 1, 2 and 3, all in `docs/worktree-guard-spec.md` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of `1788817291-the-guard-asks-once-per-worktree-not-once-per-session` (ticket #239's sibling in this release, ticket #237), at target `3287c78`, base `origin/release/v0.9.1`. The verifying round over round 2's fixes, whose substance is `bba7dab` and `f4db784`, and the last round this work item gets: rounds 1 and 2 both closed on fixes, so the record after this one ends the run whatever it finds. The change weakens a guard, and the round was told to review it as such without manufacturing a finding about that.

Round 2 had opened two things. The bounded allow's first test was `os.path.basename(tokens[0]) != "git"`, and a basename is not an identity — `./git`, `/tmp/evil/git`, `../git` and `bin/git` all answered `allow`, which covers the whole tool call and speaks over the user's own permission settings, so a session holding one creation approval could run any binary by placing it at a path ending in `git`. And the creation question was skipped whenever the rows kept above it stopped denying: two of those three are `choose` sites, which deny once per session per direction and `ask` afterwards, so a second attempt at `git switch feature/x && git worktree add …` asked about switching branches and approving it created the worktree and recorded session-wide consent — 64 of 288 pairs.

The named targets. The fix pass refused round 2's paste-ready fix and narrowed it, arguing the hoist is right for the `ask` branch and wrong for the `deny` branch, so that argument was to be tested by applying the report's version and watching what moves, then checking the shipped version leaves every `deny` untouched. The boundary sentence — vouched for only when the command word is the separator-free word `git` — with its 32 enumerated shapes to be re-derived and a 33rd looked for. What the boundary deliberately excludes, a shell function or a `git` earlier on `PATH`, neither creatable inside the command being judged. The 1260-combination sweep reported as 230 writer cells and 0 holes, against 64 when the fixes are reverted. The strengthened property, *deny or an `ask` whose text names the creation*, which the old *never silent* could not hold. The prompt budget, claimed unchanged with a new residual for a path-qualified creation. The five invariants. Finding 8's replacement number. And whether finding 2's repair really reduces what rides on the two open questions with the repository owner.

The report was to be a file, finding ids bare integers, one row per finding, no real user path, and `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 "exactly five are vouched for" is a property of one enumeration, not of the boundary — 17 command-word spellings answer `allow`, and the twelve unnamed ones are quoting spellings of the same word | `docs/worktree-guard-spec.md:158` | deferred #243 | **Executed** over 55 shapes with a record present: `g'i't`, `gi"t"`, `"g"it`, `\g\i\t`, `g\it`, `''git`, `""git`, `git""`, `git''`, `"gi"t`, `g''it` and `;git` all answer `allow` alongside the five named. **Read**: each lexes to the word `git`, so the security boundary is intact and the fix is owed to the sentence only. `;git` is a bash syntax error and runs nothing |
| 2 | 🟡 Five of the shapes the paragraph says "falls to `ask`" answer `silent`, and this document draws that distinction on purpose | `docs/worktree-guard-spec.md:160` · `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md:9` | deferred #243 | **Executed**: `gi*`, `$GIT`, `` `which git` ``, `GIT` and `git/` answer `silent`; so do `nice git` and `xargs git`, which "every wrapper" covers. The nine path shapes and the four `WRAPPERS` entries do answer `ask`. None of the fourteen gets an `allow`, so nothing is open in the code |
| 3 | 🟡 The `230` writer cells cannot be a subset of the `1260` combinations — the filter is attempt-independent, so the count must divide by 3, and 230 does not | `docs/worktree-guard-spec.md:207` · `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:98` · `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md:11` | deferred #243 | **Executed**: a 21 × 5 × 2 × 2 × 3 sweep of my own axes walks 1260, and gives 240 writer cells at the (shape, cwd, state, record) grain and 720 including attempts. 230 × 3 = 690 is the figure the sentence needs. **Read**: `creation_directory(command, cwd)` reads no state, record or attempt; the `64` in the same sentence is at the combination grain, so one sentence carries two. The 21 shapes and the record axis are in no artifact in the tree — the committed sweep case has 12 shapes, 4 states and no record axis |
| 4 | ⬜ `spec.md` says *"all deny" was true of two of them* where the ledger, the code comment and its own next sentence say one | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:85` | answered | **Read.** `seal/ledger/…:12` says "true of one of the three"; `hooks/worktree-guard.py:2117` says "Only one of those three denies unconditionally"; `spec.md:91` says "Only the ACTIVE row denies unconditionally". Under `seal/specs/`, so out of `Needs a fix` |
| 5 | ⬜ §4's "two of the three shapes are closed either way" was not updated for round 2's six path shapes, though the claim that finding 2's repair reduces what rides on the `❓` is true | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md:182` | answered | **Read.** Both `❓` rows in `overview.md` §*Not verified* name the repository owner, and §4 still states the fallback. **Executed**: the allow surface at `3287c78` is strictly smaller than at `62b2d2e` — the seven path-qualified shapes now answer `ask`. Under `seal/specs/`, so out of `Needs a fix` |
| 6 | 🟢 Refusing round 2's paste-ready fix for finding 1 was right, and the alternative costs four denies rather than one | `hooks/worktree-guard.py:1450` · `:2033` · `:2076` | answered | **Executed** as a variant, one session id per cell: hoisting `judge_creation` above rows 1-b and 2 turns four cells from `deny` to `ask`. With a record present, attempt 1 in the idle state goes from *"Other Claude sessions may exist in this tree…"* with the two options to *"Attempting to create a worktree… A worktree creation already ran in this repository this session"* — the fix pass's exact claim, measured. Same in the detection-unusable state. Two more at attempt 2 with no record |
| 7 | 🟢 Every `deny` verdict is where it was, and the two verdicts that moved got stronger | `hooks/worktree-guard.py:1392` · `:1450` · `:2138` | answered | **Executed**: 96 cells over 4 commands × 4 tree states × 2 record states × 3 attempts, `62b2d2e` against `3287c78`. Two moved, both `ask` → `deny` (`git switch feature/x && git worktree add ../wt f`, attempt 2, idle and detection-unusable, no record). Denies lost: **0**. **Read**: `before_ask` runs after `respond("deny", …)`, which exits, and is `None` whenever `creation_at` is `None`, so a command with no creation on it cannot reach it |
| 8 | 🟢 Whatever the writer records for, the guard denies it or names the creation in its `ask` — re-derived, not accepted | `hooks/worktree-guard.py:2138` · `tests/test_the_guard_asks_once_per_session.py:525` | answered | **Executed** over my own 21 shapes × 5 tree states × 2 shell directories × 2 record states × 3 attempts: 1260 walked, 720 writer combinations, **0** holes. With both round-2 fixes reverted the same sweep finds 152 holes, all of them attempts 2 and 3 in the idle and detection-unusable states — the same class the fix pass reports at 64 against its own shape list |
| 9 | 🟢 The strengthened property is falsifiable, and fails for the reason it names | `tests/test_the_guard_asks_once_per_session.py:525` · `hooks/worktree-guard.py:1757` | answered | **Executed** as a mutation: with `judge_creation`'s origin line changed to *"A worktree operation is under way."*, attempt 3 in both the idle and the detection-unusable state becomes a hole. Attempts 1 and 2 stay `deny`, so the case fails on exactly the cell the strengthening was written for |
| 10 | 🟢 The prompt budget is unchanged, and the new residual is stated honestly | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/pr-notes.md:88` · `:114` | answered | **Executed**: six `git worktree add ../wt f` in one session on a clean single-stream tree, the record written after the first — `deny, allow, allow, allow, allow, allow`. Six `/usr/bin/git worktree add ../wt f` with a record present — `ask` every time, which is what the fourth residual says. The residual names the trade rather than the shape, and the six calls the release run made carry no path |
| 11 | 🟢 The five invariants hold in the no-record state | `hooks/worktree-guard.py:1684` · `:2012` · `:2033` · `:2076` | answered | **Executed**, no record: single-stream creation `deny` with the `git switch` steer; ACTIVE switch `deny`; idle switch `deny` at attempt 1 then `ask`; detection-unusable switch `deny` at attempt 1 then `ask`; ACTIVE creation `ask`. The pure-switch ladder is byte-identical to `62b2d2e` in all 24 of its cells |
| 12 | 🟢 What the boundary deliberately excludes cannot be created inside a command it vouches for | `hooks/worktree-guard.py:370` · `:461` | answered | **Read**, and the argument holds for a reason the docstring does not state: `only_creates_a_worktree` requires **every** segment to be a `git worktree add`, so a command that plants a `git` on `PATH` or defines a shell function named `git` fails on the planting segment before the running one is reached. A leading `PATH=…` fails test 1, and `$PATH` fails `ELSEWHERE`. **Read** on bash semantics: `'git'`, `"git"` and `\git` suppress alias expansion, so each is at least as narrow as bare `git` — refusing them would buy nothing |
| 13 | 🟢 The two cases round 2's record names as new units are sound as code | `tests/test_the_guard_asks_once_per_session.py:307` · `:470` | answered | **Read.** Both assert on the English reason text, which `tr()` would render in Korean on a machine exporting `LANG=ko`; `tests/conftest.py:38` pins `SPECSEAL_LANG=en` for exactly that reason, and the note there says the author's machine exports `ko` session-wide. `test_a_spent_choose_budget_…` asserts the property rather than a verdict per attempt, which is what lets it survive the ordering the fix chose. **Executed**: the module is 35 passed at `3287c78` |
| 14 | 🟢 Ledger anchors resolve and no real user path is left anywhere under `seal/` | `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md` · `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8` | answered | **Executed**: `bin/evidence-check` exits 0 — 807 ok, 0 drifted, 0 broken, this fragment 10 ok. `bin/test tests/test_no_real_identifiers.py -q` is 2 passed. Round 1's report now reads `/Users/x/orca/…` |

## Paste-ready fixes

```markdown
The boundary the code implements is *a command word carrying no separator, so
the shell resolves it on `PATH`*. Anything with a `/` in it names a file this
hook cannot identify. What is vouched for is the CLASS the lexer reduces to the
word `git`, which is unbounded: `git`, `\git`, `'git'`, `"git"`, `g"i"t`,
`g'i't`, `\g\i\t`, `''git` and every other spelling of the same word all pass,
and every one of them runs exactly what `git` runs. Re-enumerated over 55
command-word shapes, 17 pass and all 17 are that word after lexing.
```
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
```markdown
**And *"the three concurrency rows all deny"* was true of one of them.** Round
```
```markdown
  redesign. Eight of the shapes that made this urgent are closed either way:
  `sudo git worktree add …`, `env LD_PRELOAD=… git worktree add …`, and the six
  path-qualified spellings round 2 closed (`./git`, `../git`, `bin/git`,
  `/usr/bin/git`, `/tmp/evil/git`, `~/git`, `*/git`) no longer get an allow at
  all — so strictly less rides on this answer than did at `62b2d2e`.
  **Answerer: the repository owner**, against the harness.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:342` · `:1746` | round 1's 1 — fixed |
| round-1 | `hooks/worktree-guard.py:1684` · `hooks/worktree_consent.py:138` | round 1's 2 — fixed |
| round-1 | `hooks/worktree-guard.py:342` · `hooks/cmdline.py:37` | round 1's 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1746` | round 1's 4 — deferred |
| round-1 | `pr-notes.md` §4 · `overview.md` §*Not verified* | round 1's 5 — deferred |
| round-1 | `seal/ledger.md:269` · `:337` · `:379` | round 1's 6 — fixed |
| round-2 | `hooks/worktree-guard.py:2049` · `:1368` · `docs/worktree-guard-spec.md:168` | round 2's 1 — fixed |
| round-2 | `hooks/worktree-guard.py:436` · `:401` | round 2's 2 — fixed |
| round-2 | `hooks/worktree-guard.py:1655` · `tests/test_the_guard_asks_once_per_session.py:408` | round 2's 3 — answered |
| round-2 | `hooks/worktree-guard.py:1884` · `:2067` | round 2's 4 — answered |
| round-2 | `hooks/worktree-guard.py:2067` · `tests/test_the_guard_asks_once_per_session.py:434` | round 2's 5 — answered |
| round-2 | `hooks/worktree-guard.py:401` · `hooks/cmdline.py:1282` | round 2's 6 — answered |
| round-2 | `pr-notes.md` §3 | round 2's 7 — answered |
| round-2 | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md:77` · `docs/worktree-guard-spec.md:176` | round 2's 8 — fixed |
| round-2 | `overview.md` §*Not verified* · `pr-notes.md` §4 | round 2's 9 — answered |
| round-2 | `hooks/worktree-guard.py:1655` | round 2's 10 — answered |
| round-2 | `seal/follow-up.md` | round 2's 11 — answered |
| round-2 | `hooks/worktree-guard.py:1760` | round 2's 12 — answered |
| round-2 | `seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-1-report.md:8` | round 2's 13 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a hook `ask` can be auto-answered, and whether a `PostToolUse` payload means the call ran | `overview.md` §*Not verified*, already deferred at round 1 | the repository owner, against the harness |
| Whether a `permissions.deny` rule outranks a hook `allow` | `overview.md` §*Not verified*, already deferred at round 1; `pr-notes.md` §4 carries the fallback | the repository owner, against the harness |
| A shell function or alias named `git`, or a `git` earlier on `PATH` | documented as excluded in `hooks/worktree-guard.py#only_creates_a_worktree`; judged sound at finding 12 | nobody — closed, not deferred |
