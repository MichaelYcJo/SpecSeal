# Round 1 — review report

| Field | Value |
|---|---|
| Work item | `1788789330-the-update-notice-names-the-expensive-move` (#134) |
| Branch | `docs/134-the-update-notice-names-the-expensive-move` |
| Target SHA | `0a9dfc54adb12a2d8157be25d96c25a8f807bb28` — unmoved, tree clean at report time |
| Base | `86e140f` |
| Prior rounds | none |
| Broad gate | not yet. Full suite, repository-wide lint and typecheck are the orchestrator's, `agent-contract` §2 |

## Stage 1 — spec compliance

The four *Done when* conditions, in the order the prompt gave them.

| # | Condition | Verdict |
|---|---|---|
| 1 | The notice and the update skill name `/reload-plugins`, and say what it does that a restart also does | **met, with finding 1.** Both name it. What the notice says it does is wider than what run 6 measured |
| 2 | The hooks / agent-definitions half is stated at whatever confidence it actually has | **met, and correctly widened.** The branch states three unmeasured axes where the ticket implied one measured claim. The divergence is right — see below |
| 3 | `tests/test_version_check.py` pins the new wording and was seen red against the old | **partly met, finding 2.** It was seen red — the old text carries no `/reload-plugins`, so the case's first assertion fails against it. It pins wording, not meaning, on two axes that I killed the case on |
| 4 | Both READMEs move with the text | **met.** All three Korean coordinates and all three English coordinates moved in one commit (`4822a01`), and `tests/test_docs_line_wrap.py` passes |

### The two divergences I was asked to judge

**Run 6 reaches one axis less than the ticket says — the record supports the
claim, and the branch is correcting the ticket.**

I opened `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md`
against its own §*Method* and §*Results*. The method installs no second
version: it edits `writing-style` in place, spawns `specseal:smith`, reads the
answer, and restores the file from a backup. Result 2 names the version cache
as *the copy that loads*, and runs 1–4 are recorded as failures **because they
edited the marketplace clone** rather than that copy. So the directory run 6's
sentinel sat in is, by the record's own account, the directory the running
session was already resolving `$CLAUDE_PLUGIN_ROOT` to.

Nothing in the record touches a newly installed version directory. The ticket's
summary — *"a full restart is not required to get it"* — is therefore broader
than its evidence, and `spec.md`'s added row and `overview.md`'s divergence
entry are correct. This is not a fabricated limitation.

**`hooks/version-check.py:18` belongs in the class, and the edit did not widen
the change.** The old sentence read *"a session simply keeps what it loaded
until a restart."* The experiment's result 3 — *"Preloaded skill bodies are
read at session start and at `/reload-plugins`"* — contradicts it directly: a
reload changes what a spawned agent is handed with no restart. The replacement
(*"a session keeps the version it started with"*) is narrower and survives the
measurement. Pulling it in was right.

That same edit is what produces finding 1, though: the docstring now says the
reload re-reads *"out of that same copy"*, and the notice 130 lines below sells
the reload as the way to load the new one.

## Stage 2 — the class, re-derived

I did not read `spec.md`'s table before grepping. Re-derived at `86e140f` with
`git grep` over tracked files:

```
git grep -ciI 'restart' 86e140f   → 33 lines
git grep -cI  '재시작'   86e140f   →  3 lines
git grep -niI 'reload'  86e140f | grep -vi preload →  2 lines
```

`docs/flow.md:74` carries both `restart` and `reload`, so **37 distinct lines**,
not 38. The third `reload` hit the spec claims does not exist in the tracked
tree — the experiment record's own reload sentence begins *"Preloaded skill
bodies…"* and is removed by the pattern's own `grep -vi preload`. The
worktree carries an untracked `.venv`, which `grep -r` reaches and `git grep`
does not; that is the likely source.

**The membership decision is right.** Every one of the 37 falls in a row of the
table, and the 15 the table places in class are exactly the 15 the branch
edited — `hooks/version-check.py` ×2, `skills/update/SKILL.md` ×6,
`README.md` ×3, `README.ko.md` ×3, `tests/test_version_check.py` ×1. I checked
the two fenced code comments the prompt flagged (`# then restart`,
`# 그다음 재시작`) and both moved. The arithmetic is off by one in two places;
that is finding 4.

I also went after the shape a word-grep cannot reach — a place that tells a
user what to do after an update without using any of the three words. Two
candidates, both correctly out of class:

- `skills/implement/SKILL.md:158` — *"start a new session and the plugin moves
  it into `<repo>/seal/`"*. About the 0.3.x layout migration, a different act.
- `hooks/ledger-migrate.py:4` — *"`claude plugin update` is the whole of what a
  user does."* This one is close. It is the same claim one level up that the
  branch used to justify pulling `version-check.py:18` in, and it elides the
  load step entirely — a `SessionStart` hook fires on the next session, which
  is exactly the thing the branch now says is unmeasured for a reload. It is a
  module docstring no user reads and the sentence predates this branch, so it
  ships no user-visible defect. Recorded as ⬜ 6 rather than fixed here.

`README.md:446` (*"The hooks need no restart"*, `seal mode`) is correctly out —
it is about a hook re-reading a folder per invocation, not about loading a
version.

## Findings

### 1 🟡 The notice sells `/reload-plugins` as the way to load the new release, and the same file's docstring says it re-reads the old one

`hooks/version-check.py:154-158` — with the same defect at
`skills/update/SKILL.md:135-137`, `README.md:314-319`, `README.ko.md:305-310`.

The notice fires because a newer release exists. It then says:

> Either way it still has to be loaded. /reload-plugins is the cheap move: a
> reload was measured to refresh the skill bodies a spawned agent is handed,
> and it costs you no session.

*The cheap move* — for loading the release that just arrived. But the module
docstring 130 lines above, in this same branch's own words at `:19-21`, says:

> the previous version stays in the plugin cache and `$CLAUDE_PLUGIN_ROOT`
> keeps resolving to it, so a session keeps the version it started with.
> `/reload-plugins` re-reads preloaded skill bodies **out of that same copy**

On the branch's own reading, then, a reload after an update re-reads the *old*
version's skill bodies. Whether it reaches the new install at all is the third
unmeasured axis this branch itself discovered. So the notice recommends, as the
cheap way to get the update, a move whose only measured effect is on the
version the user already has.

`skills/update/SKILL.md:88` gets this exactly right — its table row reads
*"re-reads preloaded skill bodies **out of the copy in force**"*. That
qualifier is the whole difference, and it is missing from all three of the
surfaces a user actually reads: the banner, the output template the model
prints, and both READMEs.

Two of those go further and presuppose partial coverage:

- `README.md:318` — *"so restart when you want **all of it**"*. *All of it*
  says the reload gives you some of it.
- `README.ko.md:310` — *"**전부** 확실하게 적용하려면 재시작하십시오"*. Same
  presupposition, same word.

Why it matters, in the branch's own terms: `skills/update/SKILL.md:95-98` says
the point of the distinction is that *"a user told it covers everything gets a
half-loaded plugin with no way to tell."* A user who reads the banner, types
`/reload-plugins`, and is told that was the cheap move is in that exact
position — except the evidence says they may have loaded nothing at all.

The gap sentence that follows does disclose the third axis, so a reader who
finishes the paragraph is not lied to. A reader who stops at *"the cheap
move"* is.

### 2 🟡 The pinned case still passes wording rather than meaning, and leaves the branch's own divergence unpinned

`tests/test_version_check.py:73-105`.

The case's docstring says the first draft's whole-message substring assertion
let a mutation through, and that splitting on sentences fixed it. Splitting
narrowed the scope; it did not change what is asserted. Each claim is still
pinned by *the presence of the word `measured` in its sentence*, never by what
the sentence says was measured.

I ran the case's assertion body verbatim against five mutations
(`tests/test_tmp_notice_mutations.py`, deleted). **Two survived.**

- **M1 — the reload's claim replaced with a false one, vocabulary intact.**
  *"a reload was measured to install the new version into this session"*.
  `reload_claim` contains `/reload-plugins` and `measured`, so the assertion <!-- NAME NOT IN TREE — the local was deleted at 760ac3e, where the four substring predicates gave way to an exact pin on the notice. The sentence is left as round 1 wrote it because it records what was true then. -->
  passes. This is finding 1 written as a flat falsehood, and the case is green.
- **M2 — the third unmeasured axis deleted.** *"Nobody has measured what it
  does for hooks or for agent definitions"* — the clause about *moving a
  running session onto the new version* removed. The `gap` sentence still
  carries `hooks`, `agent definitions`, `measured` and `Nobody`, so the
  assertion passes.

M2 is the sharper of the two. `overview.md` §*Where spec and implementation
diverged* names that third axis as the branch's own correction of the ticket,
`plan.md` rejects two alternatives on it, and `changelog.md` calls it *"the
part the ticket itself assumed"*. It is the most contested sentence in the
change and nothing holds it. `agent-contract` §14: what a person sees is
documented and pinned.

Controls behaved: M3 (reload's subject changed to hooks), M4 (gap flipped to a
positive claim) and M5 (order inverted) were all killed.

### 3 🟡 The banner grew 81% and carries the long form the plan chose against

`hooks/version-check.py:148-159`.

Measured by calling `notice((0,7,1),(0,8,0))`: **707 characters**, against 391
for the text it replaces. The fourth line alone is 316 characters in one
unbroken run.

The prompt asked whether the multi-sentence `systemMessage` is a rendering
finding. **The wrapping itself is not** — the previous message was already
four lines and its third line was already 197 characters, so the terminal was
already wrapping this banner. What is a finding is the growth, on three counts:

- The module's own failure-direction paragraph (`:39-41`) says *"a wrong notice
  at every session start is the kind of noise people disable a plugin over."*
  Length is not wrongness, but it is the same budget.
- `plan.md`'s chosen alternative reads *"The notice carries the short form and
  the skill carries the boundary in full."* The notice shipped the boundary in
  full: all three axes, both halves of the gap, and the evidence label. What
  the skill carries that the notice does not is only the settling method.
- `README.md:182` still describes this hook as showing *"one line naming
  `/specseal:update`"*. That was already loose; it is now four lines and 707
  characters.

Fix or justify. The paste-ready trim below keeps the cheap move first and every
claim finding 1 needs, at roughly 240 characters for the closing clause.

### 4 ⬜ `spec.md`'s enumeration arithmetic is off by one in two places

`seal/specs/1788789330-.../spec.md:38-49` and row 20.

- The `reload` grep is recorded as **3 hits**; `git grep` over tracked files at
  `86e140f` gives **2**. The corpus total is therefore **37 distinct lines**,
  not 38.
- Row 20 says *"Thirteen lines"* and lists twelve coordinates
  (`CHANGELOG.md` ×2, `docs/review-chain-spec.md` ×2, `seal/ledger.md` ×2,
  `chain_check.py` ×3, `round_record.py` ×1, `test_the_record_is_generated.py`
  ×1, `test_the_reopening_is_one.py` ×1).
- Row 22 names the three past work items as `17885…`, `17886…`, `17887…`. They
  are `1788354065`, `1788597030`, `1788761915` — no item begins `17886`.

With twelve in row 20 the table reconciles exactly against my re-derivation:
15 in class + (1 + 1 + 12 + 1 + 6 + 1) out = 37. **Nothing is missing from the
class**; only the count is wrong. A record, so not a fix — a correction.

### 5 ⬜ `0.5.0` is named as run 6's version and the experiment record does not carry it

`overview.md:21` (*"`…/specseal/specseal/0.5.0/…` while 0.5.0 was the running
version"*) and `phases/phase-1.md:26`.

The experiment record dates itself 2026-09-03 and pins Claude Code 2.1.259. It
names no plugin version anywhere. The reading is plausible from the release
dates, but it is an inference stated as a quoted path. The claim the divergence
rests on does not need it — result 2 plus the runs 1–4 failure account carry it
on their own. Say *the running version's own cache directory* and drop the
number, or cite where 0.5.0 comes from.

### 6 ⬜ `hooks/ledger-migrate.py:4` is the same shape as the sentence the branch pulled into the class

*"`claude plugin update` is the whole of what a user does."* The migration runs
at `SessionStart`, so a user who updates and neither restarts nor reloads gets
nothing — the load step this branch exists to name is elided here entirely. It
is a docstring no user reads, and it predates this branch, so it ships no
user-visible defect. Named so the decision is on the record rather than the hit
being missed.

### 7 ⬜ `README.ko.md:310` introduces 하십시오체 into a 합니다체 document

`재시작하십시오` is the only 하십시오체 form in the file. Everything around it is
합니다체 (`실행합니다`, `알려 줍니다`, `없습니다`). The paste-ready fix for
finding 1 corrects this in the same edit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The notice sells `/reload-plugins` as the way to load the new release; the same file's docstring says a reload re-reads the copy already in force | `hooks/version-check.py:154` | open | `hooks/version-check.py:19-21` says *out of that same copy*; `skills/update/SKILL.md:88` carries the qualifier and the three user-facing surfaces drop it. Siblings: `skills/update/SKILL.md:135`, `README.md:318`, `README.ko.md:310` |
| 2 | The pinned case passes wording, not meaning: a false reload claim and the deletion of the third unmeasured axis both survive it | `tests/test_version_check.py:96` | open | Executed. M1 and M2 of five mutations survived the case's own assertion body; controls M3/M4/M5 killed |
| 3 | The banner grew 391 → 707 characters and ships the long form `plan.md` chose against | `hooks/version-check.py:148` | open | Measured by calling `notice((0,7,1),(0,8,0))`. `plan.md` §Alternatives: *"The notice carries the short form"* |
| 4 | `spec.md`'s enumeration arithmetic: 2 reload hits not 3, 37 lines not 38, twelve coordinates under *Thirteen lines*, two mistyped work-item ids | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | open | `git grep` at `86e140f` re-derived independently; membership itself is correct |
| 5 | `0.5.0` named as run 6's running version; the experiment record names no plugin version | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/overview.md:21` | open | `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` pins Claude Code 2.1.259 and a date, nothing else |
| 6 | `claude plugin update` named as the whole of what a user does, with no load step — the shape the branch pulled `version-check.py:18` in for | `hooks/ledger-migrate.py:4` | open | Docstring, pre-existing, no user-visible defect. Named rather than fixed |
| 7 | 하십시오체 in a 합니다체 document | `README.ko.md:310` | open | Only such form in the file |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_notice_mutations.py -q` — the pinned case's assertion body verbatim against five mutations of the notice | exit 1, `3 failed, 3 passed`. **M1 (reload claim replaced with *measured to install the new version into this session*) and M2 (third unmeasured axis deleted from the gap) SURVIVED.** Controls M3/M4/M5 killed; sanity case on the real notice green. Probe deleted |
| `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | exit 0, `30 passed` |
| `python3 -c` calling `notice((0,7,1),(0,8,0))` on the module at the target SHA | 707 characters, 4 lines; line 4 is 316 characters. Old text reconstructed at 391 |
| `git grep -ciI 'restart' 86e140f` · `git grep -cI '재시작' 86e140f` · `git grep -niI 'reload' 86e140f \| grep -vi preload` | 33 · 3 · 2 → 37 distinct after the `docs/flow.md:74` overlap |
| `git -C … rev-parse HEAD` · `git status --porcelain` | `0a9dfc54adb12a2d8157be25d96c25a8f807bb28`, tree clean. Target SHA did not move |

Inherited as executed from the orchestrator, not re-run:
`bin/test tests/test_version_check.py -q` → `17 passed`, exit 0; `ruff check`
and `ruff format --check` on both changed Python files → clean.

Read, not run: the claim that the case was seen red against the old text. The
old notice ends *"Either way, restart to load it."* and carries no
`/reload-plugins`, so the case's first assertion cannot pass against it. That
is provable from the text; I did not restore the old tree and run it.

❓ out of verified scope: the full suite, the repository-wide lint and the
typecheck. `agent-contract` §2 reserves the broad gate to the orchestrator, and
my prompt did not order one. **The orchestrator answers it.** With findings 1
and 2 open, the gate has not come due.

❓ out of verified scope: whether `/reload-plugins` reaches hooks, agent
definitions, or a newly installed version. Not settleable from this segment —
`agent-contract` §6 forbids the spawn and no agent types a built-in CLI
command. `overview.md` §*Not verified* names the repository owner and carries
the method. **I confirm that deferral is correctly placed.**

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md:100-104` | the repository owner |
| How the multi-sentence `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships. Finding 3 is about its length, which is measurable and is not deferred |

## Paste-ready fixes

**Finding 1 — `hooks/version-check.py`, the closing clause of `notice()`.**
Replaces lines 154-158. Puts the qualifier the docstring already carries into
the sentence a user reads, and drops *all of it*-style implicature. This
breaks the current case's `gap` negation check (`unmeasured` is not in its
literal list), which finding 2's fix repairs — apply both together.

```python
        "data.\nEither way it still has to be loaded. /reload-plugins costs "
        "no session, and what was measured about it is a re-read of preloaded "
        "skill bodies out of the copy this session is already on. Nobody has "
        "measured whether it reaches hooks, agent definitions, or the version "
        "you just installed, so a restart is the move with no open question."
```

**Finding 1 — `skills/update/SKILL.md`, the output template.** Replaces the
last paragraph of the fenced `## Output` block (lines 135-139).

```
To load it: /reload-plugins re-reads the skill bodies a spawned agent is
handed, out of the copy this session is already on — that is what was
measured and all that was. Nobody has measured whether it reaches hooks,
agent definitions, or <new> itself, so restart for those. Either way this
session keeps running <old> until you do, so nothing is half-applied.
```

**Finding 1 — `README.md`.** Replaces lines 313-319. Wrapped for the 88-column
check; re-run `bin/test tests/test_docs_line_wrap.py -q`.

```
Then load it. `/reload-plugins` re-reads the preloaded skill bodies a spawned
agent is handed, out of the copy your session is already on — that is what
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` measured,
and it is the whole of it. Nobody has measured whether a reload reaches hooks,
agent definitions, or the newly installed version at all, so restart when you
want the update loaded for certain.
```

**Finding 1 and 7 — `README.ko.md`.** Replaces lines 305-310. Also drops the
하십시오체. Korean counts two display columns per codepoint in the wrap check.

```
적용하는 방법은 두 가지이고 드는 값이 다릅니다. `/reload-plugins` 는 세션을
끝내지 않고, 하위 에이전트에게 넘어가는 스킬 본문을 다시 읽습니다. 다만 다시
읽는 대상은 지금 세션이 이미 쓰고 있는 복사본이며, 여기까지가
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` 에
적힌 측정 결과의 전부입니다. 훅과 에이전트 정의는 어떻게 되는지, 그리고 새로
설치된 버전을 집어 오기는 하는지는 아무도 측정한 적이 없습니다. 새 버전이
확실히 적용되게 하려면 재시작합니다.
```

**Finding 2 — `tests/test_version_check.py`.** Replaces the assertion body
from line 92 to the end of the case. Pins the reload claim's *subject* and its
*scope*, and pins all three unmeasured axes rather than two. Accepts either
paste-ready notice above.

```python
    # Per SENTENCE, not over the whole message: a bare `"measured" in msg` is
    # satisfied by the gap sentence alone. And per CLAIM, not per word — the
    # sentence has to name what was measured, or `a reload was measured to
    # install the new version` passes every assertion here.
    sentences = [s.strip() for s in msg.replace("\n", " ").split(". ")]

    reload_claim = next(s for s in sentences if "/reload-plugins" in s)
    assert "measured" in reload_claim, "the reload's reach is asserted, not sourced"
    assert "skill bodies" in reload_claim, (
        "the reload's claim names no subject, so it pins a word and not a fact"
    )
    assert any(
        scope in reload_claim
        for scope in ("already on", "in force", "already running")
    ), (
        "run 6's sentinel sat in the RUNNING version's directory, so what it "
        "measured is a re-read of the copy in force. Without that qualifier "
        "the notice sells the reload as the cheap way to load the new install, "
        "which nothing measured"
    )

    # All THREE unmeasured axes. The third — picking up a newly installed
    # version — is the one run 6's own sentinel placement rules out, and it is
    # the axis the ticket assumed, so it is the one most likely to be dropped.
    gap = next(s for s in sentences if "hooks" in s and "/reload-plugins" not in s)
    for axis in ("agent definitions", "installed"):
        assert axis in gap, f"the gap leaves {axis} to silence"
    assert any(
        negation in gap.lower()
        for negation in ("nobody", "not measured", "unmeasured", "no one")
    ), "the gap is stated as a fact rather than as an absence of measurement"
```

**Finding 3 — the shorter notice, if the smith takes it.** An alternative to
finding 1's first block: same claims, ~240 characters for the closing clause
instead of ~330, and `/reload-plugins` still precedes `restart`. Passes
finding 2's assertions as written.

```python
        "data.\nThen load it. /reload-plugins costs no session; what was "
        "measured is a re-read of preloaded skill bodies out of the copy you "
        "are already on. Hooks, agent definitions, and picking up the new "
        "install are unmeasured — restart for those."
```

## Regression tests to plant

Beyond finding 2's rewrite of the existing case, one new case, in
`tests/test_version_check.py`:

```python
def test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads(hook):
    """The module docstring says a reload re-reads out of the copy already in
    force. A notice that sells the reload as the way to load the NEW version
    contradicts the file it lives in, and the contradiction is silent."""
    doc = hook.__doc__
    assert "out of that same copy" in doc

    msg = hook.notice((0, 7, 1), (0, 8, 0))
    claim = next(s for s in msg.replace("\n", " ").split(". ") if "/reload" in s)
    assert any(q in claim for q in ("already on", "in force", "already running")), (
        "the docstring scopes the reload to the copy in force and the notice "
        "does not; a user reads the notice"
    )
```

Seen red as written: the current notice's reload sentence carries none of the
three scope phrases.

## Facts for the evidence ledger

- **The experiment's own coordinates for the third unmeasured axis.** The
  branch's ledger fragment row 4 cites
  `docs/experiments/2026-09-03-…md#"## Results"@b1d499df` and says run 6's row
  reads `version cache, flag on`. The load-bearing half is elsewhere: §*Method*
  (the run installs no second version, and restores from a backup) and §*What
  it established* item 2 with the runs 1–4 failure account. Add those two
  anchors to the row, so a reader can check the inference rather than the
  results table alone.
- **The corpus figure.** 37 distinct lines at `86e140f`, 15 in class, 22 out —
  re-derived by `git grep` over tracked files. Worth carrying because
  `grep -r` in a worktree reaches an untracked `.venv` and this repository's
  enumerations are graded on the count.

Needs a fix: yes — findings 1 and 2. The notice tells a user the reload is the
cheap way to load a release it may not load at all, and the case that pins the
wording is green against that exact sentence.
Loses a record or crashes: no

## Proof block

Files opened at `0a9dfc5`:

- `hooks/version-check.py` (whole), `hooks/ledger-migrate.py:1-20` and its
  string literals
- `tests/test_version_check.py:1-105`
- `skills/update/SKILL.md:70-139`, `:1-35` via diff
- `README.md:263-330`, `:182`, `:440-450`
- `README.ko.md:254-320`, `:178`
- `docs/flow.md:1-40`, `:55-80`
- `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` (whole)
- `skills/implement/SKILL.md:150-166`
- `seal/specs/1788789330-…/spec.md`, `overview.md`, `routing.md`, `plan.md`,
  `phases/phase-1.md`, `changelog.md` (whole)
- `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` (whole)

Read via grep output only, not opened: `phases/phase-2.md`, `phase-3.md`,
`phase-4.md`.

Written and deleted: `tests/test_tmp_notice_mutations.py`.
