# Contributing to SpecSeal

## Opening a pull request

**Base your branch on the open release branch, not on `main`.** GitHub offers
`main` by default, and for everything except a release that default is the
wrong one here. Work collects on one release branch and `main` moves once per
release; `docs/branch-and-release.md` §*Work accumulates on a release branch*
holds the reasoning, and this section is the part a contributor needs.

**How to find it.** Exactly one branch named `release/vX.Y.Z` is open at a
time. On GitHub it is the only entry beginning `release/` in the branch
dropdown on the code page. In a clone:

```bash
git branch -r --list 'origin/release/*'   # the one to base on, and nothing else
```

Set it as the base when you open the pull request — the base is the left-hand
dropdown on the compare page. If one is already open against `main`, the
**Edit** button beside its title changes the base without closing anything.

**Why a wrong base is refused with a message about a version.** A pull request
into `main` is a release here, so the checks that run there are a release's
checks, and one of them asks for `.claude-plugin/plugin.json` to move. A
contribution is not a release and must not touch that file. Change the base
instead, and the refusal goes with it.

### What a contribution is asked for

- A branch cut from the open release branch, and a pull request based on it.
- `bin/test tests/<file> -q` on the module you touched. CI runs the rest, on
  three platforms.
- **A change to a gate carries a higher bar**: a test seen failing before the
  fix, a stated failure direction, a prompt budget, and honesty about the
  platforms you could not test. §*What a change to a gate must carry* below is
  the whole of it, and it covers anything under `hooks/` or
  `.github/workflows/`.
- The house rules below. Two of them catch most changes: both READMEs move
  together, and examples use `example.com` and `/Users/x/` rather than any
  real domain, path or handle.

### What a contribution is not asked for

This repository runs a spec-driven workflow on itself — work items under
`seal/specs/`, review rounds, an evidence ledger, a version that moves once
per release. **A contribution is asked for none of it.** The version, changelog
and ledger-fold steps belong to a release and exit early on any base but
`main`. The others run on every pull request. Three of them pass for a different
reason — they ask nothing of a branch that declared nothing: the round-record
check, the unverified-record tally and the issue-claim report. The remaining
two, the ledger and the survivor sweep, are always-on and CAN refuse a
contribution; the heading below counts both and says what each asks.
Each row below gives its own reason, and a maintainer adding a CI step should
read the row rather than this sentence.

Established by reading every step of `.github/workflows/hygiene.yml` and
`.github/workflows/test.yml` against a live contribution that carried none of
the following and came back green.

| You do not write | Why no check asks for it |
|---|---|
| a `routing.md`, `spec.md` or `plan.md` under `seal/specs/` | Nothing in CI reads them. They route a maintainer's own session |
| a review round record | *a declared review chain has the round record it claimed* passes with a notice when no declaration names your branch |
| a row under `seal/ledger/` | the `ledger` job runs the lenient reader: content drifting under an anchor is a warning. An anchor that stops resolving is not — see below |
| a `changelog.md` fragment | *every changelog fragment reached the released file* exits 0 unless the base is `main` |
| an `overview.md`, or a row inside one | *the unverified record is readable* counts the rows already in the tree, so adding none passes |
| a new version in `.claude-plugin/plugin.json` | *a change to what ships must move the version* exits 0 unless the base is `main` |
| an issue number in the description | the issue-claim step reports what it finds and never fails; an empty description is a description |

You also have no commit gate and no worktree guard. Those are this plugin's
own hooks, installed on a maintainer's machine. Nothing runs them on yours,
and nothing in CI stands in for them.

### The two checks that can ask you for something you do not have

*wording this branch removed is not still standing elsewhere* runs on every
pull request into a release branch, and a documentation change can trip it. It
reports each place still carrying wording your change removed, and its refusal
tells the author to record the exemption in a `survivors.md` under
`seal/specs/` — a file belonging to a work item, which a contribution does not
have.

**Do not create one.** Say so on the pull request instead: quote what the
check reported, and say why the text it found is correct where it stands. A
maintainer then either corrects those places or records the exemption on their
side.

**The evidence ledger is the other one.** `seal/ledger.md` and the release
files under `seal/releases/` pin claims to units of code and prose by name,
and the `ledger` job fails when one of those names stops resolving — a
heading you renamed, a function you removed. Drift under a name that still
resolves is only a warning; a name that is gone is exit 2. The repair is a
maintainer's, for the same reason: the row is removed from the file it
stands in and the new claim written into a work item's fragment,
which is a convention a contribution does not have. Say on the pull request
which name your change moved, and leave the ledger alone.

## Running the checks

The suite needs only `pytest`; the gates themselves are stdlib-only Python.
`bin/test` acquires it once: it builds a virtualenv at `.venv` on the first
call and reuses it afterwards, so only the first call pays for an environment.
It works from any directory in the repository or a worktree of it, and it
prints the interpreter it used.

```bash
bin/test tests/test_session_cost.py -q   # one module — the form to type
bin/test                                 # everything, in parallel — the sealer's run
uvx ruff check . && uvx ruff format .    # the linter this plugin runs on your code
python3 skills/evidence-check/scripts/evidence_check.py .
```

Both forms run under `-n auto` unless you pass your own `-n`, `-p no:xdist`
or `--pdb`, and the runner installs `pytest-xdist` into a `.venv` that lacks
it (#337). What the whole run costs is a figure with a date and a machine,
recorded in the work item that measured it, not here.

**The last of those is the lenient reader.** `broad-gate` runs the same script
with `--strict`, where drift is exit 2 and the branch comes back `NOT SEALED`;
CI's `ledger` job runs it without the flag and renders drift as a warning.
Three readers of the exit code, one tree, and the disagreement is deliberate —
a branch mid-flight drifts legitimately, and the gate runs once at the end over
a tree nobody is still editing. A check run that comes back exit 1 prints which
reading you took, so this is not a fact anyone has to remember.

**Name a module.** The full suite is the sealer's, run once after the review
rounds settle — `skills/agent-contract/SKILL.md` §2 forbids it to smith and
warden, and `agents/sealer.md` is the agent it is assigned to. A cheap runner
does not widen that rule. What it makes cheap is `bin/test tests/<file> -q`,
and that is the form a segment types.

**Python 3.12 is the supported floor**, held as `FLOOR` in
`.github/scripts/run_tests.py` so this sentence and the code state one number.
`bin/test` builds its virtualenv with an interpreter at that floor or newer,
refuses a `.venv` it finds below it, and where it finds neither `uv` nor such
an interpreter it says which to install.

The fallback runs the suite without writing a `.venv` into the tree. It is the
form this section used to name first, and it resolves and installs its
environment on every call — 55–58 seconds each, paid on all seventeen test
calls of one measured segment (#133, #156). Check `python3 -V` before using
it, since nothing here holds the floor for you: macOS ships 3.9 under that
name, and a version manager points it wherever it was last told.

```bash
uvx --with pytest python3 -m pytest tests/ -q   # or: pip install pytest && python3 -m pytest tests/
```

CI runs four jobs: lint (`ruff check` + `ruff format --check`), the suite on
ubuntu, macOS and Windows at the floor stated above, the evidence ledger
against this repository, and the hygiene workflow that guards releases. A change to any
hook needs a test that fails without it — see the counterfeit rule below.

**The suite runs with `gh` logged out, on your machine as on CI.** CI's
pytest job has no token, so `tests/conftest.py` makes the same true locally
when it is imported: it points `GH_CONFIG_DIR` at an empty directory and
removes `GH_TOKEN`, `GITHUB_TOKEN`, `GH_ENTERPRISE_TOKEN` and
`GITHUB_ENTERPRISE_TOKEN`. A case that falls through its stubs onto a live
`gh` then fails where you run it, instead of passing because you happen to be
logged in and failing only on CI after the branch was sealed (#510). A case
that needs `gh` stubs it.

Two steps of the hygiene workflow ship to user repositories as well, as
`templates/hygiene.yml`: the unverified-rows tally and the chain check, run
from a clone of this repository at the release the user installed. The
`implement` skill writes it at a shared-mode first setup, so a change to
either step here reaches a user at their next first setup, and the template
has to keep telling the same story as the workflow.

Run the broad ones once, at the end. The `verify` skill's Scope rule applies
to work on this repo too: narrow runs while you are still editing, everything
after the review rounds settle, and nothing edited between that run and the PR.

## What a change to a gate must carry

The gates decide whether someone's commit or branch switch proceeds, so a
change to one is judged by what it does when it is wrong:

- **A test seen red.** Write the test against the unfixed code and watch it
  fail before you fix anything. A test that has never failed proves nothing
  (this repo's own `verify` skill calls that a counterfeit seal).
- **A stated failure direction.** Say whether the change makes the gate
  block more or allow more, and why that direction is the cheaper mistake
  here. A wrong deny costs a prompt; a wrong allow can break another
  session's tree — but a deny that fires on *every* invocation in some
  environment is an outage, not a cost.
- **A prompt budget.** Say how many times the change puts a question in
  front of a person, per session, and what each one costs when nobody is at
  the keyboard. **Verification through an automated workflow is this
  project's first goal**, so an interruption is a price paid against it
  rather than a neutral design choice. A change that adds one says why
  nothing cheaper reaches the same guarantee — a value read from a file, a
  default assumed in writing, a refusal the agent makes on its own. Where a
  question really is the only answer, it belongs in the batch asked before
  the first edit, never at minute thirty.
- **Platform honesty.** Process inspection (`ps`, `lsof`, `/proc`) behaves
  differently across macOS, Linux, and Windows. If you cannot test a
  platform, say so in the PR rather than assuming.

The prompt budget is the one of these four a passing suite cannot report on,
because nothing counts interruptions. It is answered in the pull request body
or it is not answered. `skills/implement/SKILL.md` §1 holds the reasoning the
budget is drawn against: the cost of a question is not its difficulty, it is
when it arrives.

## House rules

- **A change writes a fragment, never a shared registry.** Its changelog
  entry goes in `seal/specs/<work-item-id>/changelog.md` and its evidence rows in
  `seal/ledger/<work-item-id>.md`. A feature branch **appends** to neither
  `CHANGELOG.md` nor a ledger file — `seal/ledger.md` or a release's
  `seal/releases/<X.Y.Z>.md`. Three branches running in parallel
  shared exactly one file between them and it was the changelog; the conflict
  is three lines, and it arrives after the broad gate has run, where nothing
  may be edited. Both kinds of fragment are gathered at the release
  (`docs/branch-and-release.md`): the changelog fragments into the released
  section, the ledger fragments into that release's own file,
  `seal/releases/<X.Y.Z>.md`, where the rows stay. `seal/ledger.md` keeps
  the notation and the rows from before the fragments existed, and stops
  growing.

  **Changing cited code is the case the rule has to answer, and it is not an
  append.** Change what an existing ledger row cites — in `seal/ledger.md`
  or a `seal/releases/` file — and the checker reports DRIFTED, which needs
  that row touched in the file this rule covers. Three answers, and which one
  applies is about the claim rather than the code:

  - the claim still holds and you have re-read it — run
    `evidence-check --reverify .`, which recomputes the hash and names what it
    changed;
  - the code still stands and your edit made the claim false — correct the
    claim in place first, with a `Corrected <date>` note, then run
    `--reverify`;
  - the claim went with the code — **remove the row and write the new claim
    into your own fragment.** A row is not re-pointed at whatever now sits
    nearest to where it used to look.

  All three are writes to the file the row is in, and none is an append. A
  branch that removes or edits code an existing row cites is keeping an
  existing claim true, which can only happen where the row stands; adding a
  claim is what goes in your fragment, and always did.

  So a claim leaves the ledger when the code it was about does, and comes
  back at the release, folded in from the fragment that replaced it.

  **When a ledger file conflicts — `seal/ledger.md`, a
  `seal/releases/<X.Y.Z>.md`, or a fragment two stacked branches both edited —
  resolve it hunk by hunk and read both sides.** The split into release files
  made the files smaller, not the conflict rarer: two branches that re-stamp
  one row still meet on it. Never `--ours` and never `--theirs`. A whole-file
  choice is wrong by construction once both branches have been correcting, and
  the measured instance is the argument: in #424 the two hunks resolved in
  opposite directions, because each side was the superset in one of them.
  Taking a side reverted three corrections that had each turned a false claim
  true.

  **Nothing downstream can see that, which is why the reading is yours.** A
  row reverted to a superseded state is byte-identical to a row nobody
  touched — there is no marker on it, and the hash `evidence-check` reads is
  correct for the restored text. `correction-check --range
  origin/<base>...HEAD` reads the `Corrected <date>` and `Re-read <date>`
  markers instead and names what a merge dropped from a row that still
  stands; the hygiene workflow runs it on every pull request into a release
  branch. It reports the loss after the fact and cannot prevent it.

  **Hunk by hunk has two halves, and only the notes are a union.** A row's
  `Re-read` and `Corrected` notes are both sides', because each records a
  reading somebody performed; the anchor's hash belongs to the side that
  edited the anchored unit, and to neither side where both did.
  `correction-check` cannot see a union that kept a stale hash, because no
  marker was dropped, so run `evidence-check` after the resolution: a drifted
  anchor is the tool naming the row, which is re-read against every edit the
  merged unit carries. `docs/the-evidence-ledger.md` §*A correction a merge
  dropped* owns the rule.

  `CLAUDE.md` carries both paragraphs and the halves rule, and
  `tests/test_a_merge_cannot_silently_drop_a_correction.py` holds the two
  against each other.

  **Renamed a cited symbol or file?** `bin/evidence-check --reverify .`
  re-anchors every row whose content provably moved intact and prints BROKEN
  with the destination for anything it cannot prove. The command is the rule;
  remembering it is not — forgetting costs one line at the very next commit,
  printed by the post-commit advisory in the terminal where the rename just
  happened, and CI prints the same line at the pull request.

  **One branch does edit `CHANGELOG.md`, and it is the one based on `main`.**
  A pull request into `main` is a release, so the entries are due there and
  the hygiene workflow fails it while a fragment is still ungathered. Run:

  ```bash
  python3 .github/scripts/gather_changelog.py --version X.Y.Z   # --dry-run first
  python3 .github/scripts/fold_ledger.py --split                # once; checklist §2
  python3 .github/scripts/fold_ledger.py --version X.Y.Z        # --dry-run first
  python3 .github/scripts/gather_changelog.py --check           # what the workflow runs
  python3 .github/scripts/fold_ledger.py --check                # and this
  ```

  This is the rule above being satisfied rather than broken: the branch is not
  adding an entry to a shared region, it is collecting the fragments that
  already exist. A hotfix taken straight to `main` is the case that meets this
  without expecting to.

  The fold refuses, naming the file, while any `seal/specs/<id>/evidence-todo.md`
  in the tree still has an open row: a row in a file with no `drained` line,
  whose first cell does not begin with ✅. Merge the fact into the fragment
  and drain the file; that is one commit on the release branch.
- **No real identifiers.** Examples, fixtures, and docs use `example.com`
  and `/Users/x/` only. `tests/test_no_real_identifiers.py` enforces it in
  CI — extend its allowlist deliberately, never to make a test pass.
- **Functional files are English-only.** Skills, agents, hooks, and commands
  load into model context, where a translated mirror would drift. Korean
  belongs in human-facing docs (`README.ko.md`). The `writing-style` skill
  is the deliberate exception: its per-language sections are independent
  norms, not mirrors.
- **Both READMEs move together, and so does every document with a `.ko.md`
  edition.** They need not be literal translations, but they must tell the
  same story about what exists. Under `docs/` the outline is checked:
  `tests/test_both_editions_carry_the_same_folds.py` reads every top-level
  `docs/X.ko.md` beside a `docs/X.md` and requires the same sequence of
  heading levels and, under each heading position, the same fold markers. A
  fold into one edition is a fold into both.
- **Hooks stay local and quiet.** No writing outside the repo being worked
  on, and failure must never block a tool call. A gate that crashes should
  let the work through, not wedge the session.

  Two hooks reach the network, and both are named in the README's privacy
  section because a rule with undisclosed exceptions is not a rule.
  `lint-python` fetches ruff through `uvx` when no local copy exists.
  `version-check` asks the plugin's own repository for its newest release tag.
  A third needs the same three limits the second carries — an opt-in condition
  so unrelated repos are untouched, a throttle so it is not per-session, and
  silence on every failure — plus a line in the README saying what leaves the
  machine. Anything that would send repository contents, paths, or prompts is
  not on the table.
- **Hooks are Python invoked as `python3 <script>`, with `py -3 <script>`
  behind it.** Shebangs and exec bits do not exist on Windows, and `python3`
  is the one name its official installer does not create — so the registered
  command names both, in that order, and the packaging test enforces the
  form. The fallback is safe because `dispatch.py` exits 0 for every decision
  it makes, deny included: `||` is reached only when the first interpreter
  could not start, never as a second run of a gate that already decided.

## Cutting a release

`docs/branch-and-release.md` holds it: where a branch is cut from, **which
merge method each direction takes** — they are not interchangeable — the two
things that carry the version, how the changelog fragments are gathered, and
which issues a release closes. Read it before merging anything, not after.

## Proposing a new gate or skill

Open an issue first describing the failure it prevents and what a false
positive would cost. The plugin's value is that its always-on surface stays
small — a new always-loaded rule has to earn its place against
[the context-file study](https://arxiv.org/abs/2602.11988) the README cites.
Skills that load on demand are a much easier case to make than anything
added to the CLAUDE.md block.
