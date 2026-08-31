# Contributing to SpecSeal

## Running the checks

The suite needs only `pytest`; the gates themselves are stdlib-only Python.
**Python 3.12 is the supported floor** — check with `python3 -V` rather than
assuming, since macOS ships 3.9 under that name and a version manager points
it wherever it was last told.

```bash
uvx --with pytest python3 -m pytest tests/ -q   # or: pip install pytest && python3 -m pytest tests/
uvx ruff check . && uvx ruff format .           # the linter this plugin runs on your code
python3 skills/evidence-check/scripts/evidence_check.py .
```

CI runs four jobs: lint (`ruff check` + `ruff format --check`), the suite on
ubuntu, macOS and Windows at the stated floor of 3.12, the evidence ledger
against this repository, and the hygiene workflow that guards releases. A change to any
hook needs a test that fails without it — see the counterfeit rule below.

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

- **No real identifiers.** Examples, fixtures, and docs use `example.com`
  and `/Users/x/` only. `tests/test_no_real_identifiers.py` enforces it in
  CI — extend its allowlist deliberately, never to make a test pass.
- **Functional files are English-only.** Skills, agents, hooks, and commands
  load into model context, where a translated mirror would drift. Korean
  belongs in human-facing docs (`README.ko.md`). The `writing-style` skill
  is the deliberate exception: its per-language sections are independent
  norms, not mirrors.
- **Both READMEs move together.** They need not be literal translations, but
  they must tell the same story about what exists.
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
things that carry the version, and which issues a release closes. Read it
before merging anything, not after.

## Proposing a new gate or skill

Open an issue first describing the failure it prevents and what a false
positive would cost. The plugin's value is that its always-on surface stays
small — a new always-loaded rule has to earn its place against
[the context-file study](https://arxiv.org/abs/2602.11988) the README cites.
Skills that load on demand are a much easier case to make than anything
added to the CLAUDE.md block.
