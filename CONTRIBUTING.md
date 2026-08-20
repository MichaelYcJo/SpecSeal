# Contributing to SpecSeal

## Running the tests

The suite needs only `pytest`; the gates themselves are stdlib-only Python.

```bash
uvx --with pytest python3 -m pytest tests/ -q   # or: pip install pytest && python3 -m pytest tests/
```

CI runs the same suite on ubuntu and macOS. A change to any hook needs a
test that fails without it — see the counterfeit rule below.

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
- **Platform honesty.** Process inspection (`ps`, `lsof`, `/proc`) behaves
  differently across macOS, Linux, and Windows. If you cannot test a
  platform, say so in the PR rather than assuming.

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
- **Hooks stay local and quiet.** No network calls, no writing outside the
  repo being worked on, and failure must never block a tool call. A gate
  that crashes should let the work through, not wedge the session.
- **Hooks are Python invoked as `python3 <script>`.** Shebangs and exec bits
  do not exist on Windows; the packaging test enforces this form.

## Proposing a new gate or skill

Open an issue first describing the failure it prevents and what a false
positive would cost. The plugin's value is that its always-on surface stays
small — a new always-loaded rule has to earn its place against
[the context-file study](https://arxiv.org/abs/2602.11988) the README cites.
Skills that load on demand are a much easier case to make than anything
added to the CLAUDE.md block.
