# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 76cce46 |
| Ran by | <the spawning session fills this row> |

## What this phase was asked

Two documents. `CONTRIBUTING.md` §*Running the checks* to name `bin/test`
first, with the slow `uvx --with pytest` form either gone or clearly marked as
the fallback — the judgment left open, with the reason to be stated. The 3.12
floor sentence to stay, but only after opening the runner and confirming it
holds that number as a constant: a document naming a floor the code does not
enforce is a finding rather than a rewrite. The *run the broad ones once* rule
to stay.

And whatever names the runner to a spawned segment, which is #156's *Done
when*: `agents/smith.md` or the handoff protocol stops needing an orchestrator
to type the runner into every spawn prompt. `docs/review-handoff-protocol.md`
§*The handoff before round 1* already requires *"the runner incantation in the
form the round is to run it"*, to be read before deciding. The evidence handed
over: four #170 build segments read repeats of 17 s, 2 s, 0 s and 0 s, the
only difference being whether the orchestrator typed the runner into the
prompt.

One prohibition. `README.md`'s command table is for plugin users, so `bin/test`
must not go in it.

And the §2 problem: `bin/test` runs the full suite, which the contract forbids
to smith and warden, so wherever the runner is named to a segment the text has
to say the narrow form is the segment's and give it — `bin/test tests/<file>
-q` — rather than repeat §2.

## What this phase found

**Phase 1's central fact is false, and it took an `ls -a` to see it.** That
record says **[executed]** the plugin cache ships `tests/` and `skills/`
"while `.github/` is absent from it", and the runner's location rests on it.
**[executed]** `ls -a` on the cached releases: `0.5.0`, `0.7.0`, `0.8.0` and
`0.8.1` each hold `.github/scripts/` and `docs/`. `.claude-plugin/marketplace.json`
declares `"source": "./"` and `.gitattributes` carries no `export-ignore`, so
the plugin ships from the repository root and withholds nothing. A plain `ls`
is what a dotfile disappears from, which is the likeliest way the claim was
taken — and it reached three files and a test docstring before this phase
opened it. §5 is the rule that caught it: the fact arrived in prose, labelled
executed, and opening it was one command.

**The decision stands and the reason is replaced.** `.github/scripts/` is
where this repository's own automation already lives, which is a placement
argument that needs no concealment. What actually keeps a plugin user out is
the other fact phase 1 established: `test` is a shell builtin, so PATH never
offers `bin/test` however many copies sit on it, and reaching the runner means
typing a path into a versioned cache directory on purpose. Corrected in
`.github/scripts/run_tests.py`, `bin/test` and one test docstring;
`test_the_placement_stands_on_what_it_actually_buys` refuses the old sentence
and requires the new one. What phase 2 did not do is add a guard — that is
mechanism on phase 1's surface, and it is question 7 for the owner.

**The prohibition survives its false reason.** `bin/test` stays out of
`README.md`'s command table, but not because a plugin user's copy finds no
runner — it will find one at 0.8.2. It stays out because that table lists
commands a reader types, and `test` is the one command there that PATH cannot
offer. Same outcome, and the case that pins it says the true thing.

**The slow form is kept, demoted, and labelled.** Deleting it was the other
option. It is kept because `bin/test` writes a `.venv` into the working tree
and a reader who does not want that has nowhere else to go, and because the
`pip install pytest` variant beside it is what CI actually does. It is not a
no-clone fallback — it runs `tests/`, so it needs the clone too — it is a
no-write one, and the section says so. It also carries the 55–58 seconds that
demoted it, because a fallback named without its cost gets promoted back by
the next reader.

**The floor claim held.** `FLOOR = (3, 12)` in `.github/scripts/run_tests.py`,
used both to build with `uv venv --python ">=3.12"` and to refuse the standard
library fallback below it, so the document's 3.12 and the code's are one
number. The sentence changed anyway, because its advice no longer fits the
first command: *check `python3 -V`* was the reader's job when every command in
the block ran under whatever `python3` resolved to, and `bin/test` now holds
the floor itself and says what to install when it cannot. The check moved to
where it is still true — the fallback — and the sentence now names `FLOOR`, so
the two places stating a version are traceable to each other. A case pins them
equal by reading the constant out of the runner rather than by repeating 3.12.

**The requirement had to be met by the tree, not by the prompt.** The protocol
already required the runner incantation in a spawn prompt, and that is a
per-prompt act — met until somebody forgets, which is what the 17 s and 2 s
readings are. So the fifth requirement says a shipped runner is *found*, not
typed: the handoff names it once, the segment finds it where the contribution
guide names it first, and a prompt carrying no incantation is not a prompt
missing one. The old requirement survives for the case it was written for, a
repository that ships no runner.

**Two carriers, one owner, because a rule stated twice is two places to
disagree.** The protocol owns it; `agents/smith.md` links it by naming the
section, which is the pattern `test_the_rules_have_one_owner.py` already holds
nine rules to. `agents/smith.md` is the carrier that matters for the cause,
because it reaches a segment at startup with nobody typing anything — which is
exactly what went missing.

**`skills/agent-contract/SKILL.md` was not touched, and neither was
`CLAUDE.md`.** The contract is the wrong home: it holds what is true of any
agent, and *look for a runner* is one role's verification habit rather than a
universal rule. `CLAUDE.md` is the one file a segment reads automatically that
could have carried this repository's own command — and no agent's message can
authorize an agent to edit it, so it is the orchestrator's or the owner's to
change, never a spawned segment's.

**Every case was seen red before it was planted**, including the two that had
nothing to fail against: the prohibition case was shown red by inserting a
`bin/test` row into `README.md`'s table, and the *broad ones once* case by
deleting the sentence it guards. Both were restored and re-run green.

**One module fails and it is phase 3's.**
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` fails
because this work item has `spec.md` and `plan.md` and no `overview.md` yet.
It failed the same way before this phase's first edit; the closing memo is
phase 3's first row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `CONTRIBUTING.md`'s claim that the floor is checked with `python3 -V` for every command in the block | the same section, narrowed to the fallback — `bin/test` holds the floor itself and says what to install |
| the placement argument that `.github/` does not reach a user's machine, in `.github/scripts/run_tests.py`, `bin/test` and one test docstring | replaced in place by what the location actually buys; the correction and its measurement are appended to `phases/phase-1.md` |
