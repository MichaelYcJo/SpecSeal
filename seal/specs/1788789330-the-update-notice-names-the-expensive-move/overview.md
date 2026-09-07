# the update notice names the expensive move — overview

📋 implement applied
· spec:     `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` (results 2 and 3, the results table, §What it did not establish) · `CLAUDE.md` §the goal a design is chosen against, §fragments never the shared file · `CONTRIBUTING.md` §runner · `seal/config.md` (no `Record language` row → English) · `seal/follow-up.md` (no row is a prerequisite of this work) · this item's `routing.md`, `spec.md`, `plan.md`
· evidence: `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md`
· verified: **executed** — `bin/test tests/test_version_check.py -q` red then green, and six mutations of the notice all killed. **read** — the two READMEs and `skills/update/SKILL.md`, whose wording nothing pins. **unverified** — the full suite, and whether a reload reaches hooks or agent definitions; answerers named below

## Why this work exists

The notice and the update skill named a restart, which costs the session you
are in, and never named `/reload-plugins`, which this repository measured and
wrote down eleven months of releases ago. Both now name the cheap move first
and say exactly how far the measurement behind it reaches.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How far run 6's result reaches | The ticket: *"So `/reload-plugins` is what refreshes what an agent will be handed, and a full restart is not required to get it."* The handoff narrowed it to skill bodies for spawned agents and named hooks and agent definitions as the unmeasured half | **Three unmeasured things, not two.** Hooks, agent definitions, **and** moving a running session onto a newly installed version | Run 6's sentinel sat in `~/.claude/plugins/cache/specseal/specseal/0.5.0/…` while 0.5.0 was the running version, so what it measured is a re-read of the copy already in force. A user reading this notice is in the other case — a *new* directory exists — and nothing has measured that. `implement` §1 ranks a ticket above the code and below what was ratified; the experiment record is the ratified half |
| Whether `hooks/version-check.py:18` is in the class | The handoff offered it as an example of a hit that is *"correct as it stands — describes the session's own behaviour rather than instructing anyone"* | **In the class, narrowed** | `agent-contract` §5: a fact arriving in prose is a claim to open. Opened, the sentence reads *"a session simply keeps what it loaded until a restart"*, which the reload result contradicts for preloaded skill bodies. It is the notice's own claim one level up, and leaving it would have left the file disagreeing with itself |

## Not verified

| Item | Who must answer |
|---|---|
| Whether `/reload-plugins` refreshes **hooks** | the repository owner or the orchestrator, by run 6's method one artifact over: a sentinel in a hook under the newly installed version's cache directory, a reload with no restart, then the hook's event triggered. `skills/update/SKILL.md` §5 carries the method |
| Whether `/reload-plugins` refreshes **agent definitions** (`agents/*.md`) | the same run, with a spawn in place of the hook event |
| Whether `/reload-plugins` moves a running session onto a **newly installed version** at all | the same run. This is the axis the ticket assumed and no run has touched |
| The full suite, the repository-wide lint and the typecheck | the orchestrator. `agent-contract` §2 reserves the broad gate to it; this segment ran the six modules its edits touch |
| That the new notice renders as intended in a real session-start banner | the orchestrator, on the first session after this ships. The string is pinned by a case; how a multi-sentence `systemMessage` wraps on screen is not something a test can see |

## Not done

**The unmeasured half was not measured here, and could not be.** Settling it
needs `/reload-plugins` typed by a person and an agent spawned after it.
`agent-contract` §6 forbids this segment the spawn, and a built-in CLI command
is not a skill an agent can invoke — the ticket's own *Not this* draws the same
line for the neighbouring act. What was done instead is to name the run that
would settle it, in the skill, so the person who wants it settled has the
method rather than a note saying somebody should look.

**`README.md:439` was left alone.** *"The hooks need no restart: the next
command reads the folder where it is"* is about `seal mode`, a different act,
and it already names the cheap move for that act. It is row 16 of `spec.md`'s
enumeration table, with the grounds.

**The tracker row at `docs/flow.md:74` was ticked, not rewritten.** It
describes the ticket, and a tracker describing what a ticket said before it was
built is not a defect.

## Fed back into the spec

**One clause, inferred during implementation.** `spec.md`'s *What is measured*
table now carries the row *"A reload moves a running session onto a newly
installed version — unverified"*, which no document in this repository stated
before. It came from reading run 6's own placement rather than its conclusion,
and a planner may overturn it the moment somebody runs the experiment.
