# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | ddb580d1 |
| Ran by | specseal:smith on Claude Opus 5.5 (1M context) — the agent as the spawn prompt's first line names it, the model as the commit trailer it prescribes names it |

## What this phase was asked

Five sentences and one verification: #55 (one sentence in `agents/smith.md`
beside the waiver example, pinned as a kept application, the rider re-read
and re-stamped), #316 (one paragraph in `skills/verify/SKILL.md`'s
`arm-check` section, taking W4's default), #474 items 2 and 3, #222 (one
paragraph in `depth_two`'s docstring, with its rows re-read and re-stamped),
and #268 confirmed by grep. And #556, added to this phase at the spawn: the
two comments above the `kept_broad_gate` call in `round_record.py`'s `close`
and `seal` take the issue's two paste-ready blocks, `agents/sealer.md`
takes its sentence, `plan.md`'s phase-4 row and `spec.md` §Scope name
#556, and `changelog.md` gets an entry.

## What this phase found

**#55** (executed). The sentence follows the waiver paragraph in
`agents/smith.md`'s design gate: *That token is the last way past the gate
and never the first one to reach for. On a probe it records something
untrue … Contract §8 names the two shapes to reach for before it.*
`tests/test_a_moved_rule_leaves_its_definition.py#test_a_citation_is_not_a_copy`
keeps the last clause as a phrase. It was seen red with the sentence deleted
(bytes kept, `-k citation`, exit 1:
*agents/smith.md lost its own application: 'Contract §8 names the two shapes
to reach for before it'*), and green once restored. The window case still
reads 10 as the longest kept application (the module, `166 passed`).

**The rider was read before it was re-stamped, and its numbers re-measured**
(executed). It says the waiver example is in command position,
`_hides_a_commit` is True for the file as a whole, and the example line
gives one invocation in a heredoc body both alone and with everything above
it. Loaded from `hooks/commit-review-gate.py` over the edited file:
`_hides_a_commit` True, one invocation alone, one with everything above. The
same numbers, so the rider stands.
`rider_check.py --reverify --only agents/smith.md` re-stamped it
(`"## Phases"@ccacfcc7`), and `rider_check.py` exits 0.

**#316** (read, then written). The paragraph follows the section's *in the
rest of the tree* paragraph. It says the bound is on the wait, names 900
seconds, `--timeout 0` and *twice that*, says only the command's own process
is killed and why the wrapper form is the one that leaks, and says to name
the pytest command directly. Every fact comes from
`arm_check.py#run_arms`'s docstring and `main`'s `--timeout` handling (read).
**W4 takes its default, no case.** `tests/test_arm_check.py` pins the
timeout by running the script (`timeout=0.3`, `--timeout -1`) and reads no
document, so it has no document pin to mirror, and #310 is the standing
warning against pinning a clause by substring.

**#474 item 2** (executed, a whitespace-collapsed search for *this
repository* over the file). The two sentences are
`skills/verify/SKILL.md` §*What the count does not say*, now *the one live
instance in the repository this plugin is developed in … SpecSeal's own
workflow*, and §*The arms the plugin ships*, now *SpecSeal's own `release`
job*. The first was wrapped across two lines, so a line `grep` never found
it. Two uses of *this repository* remain, *this repository's two
measurement logs* and *this repository simply has no durable ledger*, both in
§*Measure the segment*. S13 puts them out of the class as addressed to the
reader's own repository, and they stay.

**#474 item 3** (read, then written). The module docstring of
`tests/test_the_gate_names_every_step_ci_runs.py` no longer says *the half
#423's finding 4 was about*. It says the finding was a narrow reader, three
of four base spellings, and named both directions. **The class has a fourth
carrier the ticket did not list**, found by grep: `seal/ledger.md` row G1
of `1789985781`, whose Notes cell opens *Half a pin is #423's finding 4*.
That is a ledger correction beside G6 and G7, so it goes to phase 6, which
is written against D's ledger.

**#222** (read, then written). The paragraph follows the #333 paragraph in
`round_record.py#depth_two`. It says candidates are the units the range added
in the file the finding's Location resolves in, that a case in another file
is never a candidate, that this is what keeps the rule consistent with
`skills/agent-contract/SKILL.md` §15, and that it is not an exemption for
tests. The walk still reads `[n for r, n in added if r == f]` (read), which
is judgment 11.

**#268** (executed, `grep -rn` over `agents`, `skills`, `templates`, `docs`,
`hooks`, both READMEs, `CONTRIBUTING.md`, `CLAUDE.md`, `.github` and
`seal/follow-up.md`). *a warning rather than a mention*: no hit. *four
shapes*: one hit, `broad_gate.py:823`, about the four lines-stopped shapes of
the gate's reader, not the issue-claim shapes. *only on pull requests into* /
*only those into `main`* / *only on those into*: no hit. The one statement
the ticket corrected still stands correctly in `docs/issues-and-milestones.md`
§*A keyword claims the one number after it* (*The hygiene workflow reports
the split on every pull request*). `close_issues_on_release.py:101` names
#266. No edit, and #268 closes on this report.

**#556** (read, then written). The two comments are the issue's blocks
verbatim. The sealer's sentence moved from `:189-190` to `:212-213` when B
landed, and it reads *every earlier comparison kept behind it*.
`tests/test_the_broad_gate_cell_keeps_every_run.py` holds the sealer on
*earlier run*, which still stands at `:164`. **The class, enumerated** by grep
over shipped files for *kept behind*, *every earlier run*, *never erases*,
*stays behind it* and *second run never*. `agents/warden.md:341` says *an
earlier run kept behind the newest*, which describes the shape and claims no
*every*, so it is left. `round_record.py#kept_broad_gate`'s *a second run
never erases the first* is scoped to a run against another base in the
sentence it closes, so it is left too. The template and the handoff protocol
already state the replace. **One more carrier is in the ledger, not the
tree**: `seal/ledger.md` row A5's Clause says `seal` *keeps that run behind
it* and does not name the replace. The row is noted to that effect and its
correction is left to phase 6.

**Verified** (executed): `bin/test` over the moved-rule, arm-check,
gate-steps, floor-and-depth, one-word, line-wrap, broad-gate-cell and seal
modules, `513 passed`. `rider_check.py` exit 0. `uvx ruff check` and
`uvx ruff format --check` over `round_record.py` and the two edited test
modules, exit 0 each. The ledger: rows on `agents/smith.md#"## Phases"` (3),
`round_record.py#close` (8), `#seal` (9) and `#depth_two` (4, D1 among them)
were re-read and noted, and `evidence-check --reverify .` re-stamped 24 rows.
Then `evidence-check --strict .` exit 0, `1767 ok · 0 drifted · 0 broken`.

**For the fragment, drafted and written at phase 6**: #55's sentence on
`agents/smith.md#"## Phases"` with the kept-phrase case, #316's paragraph on
the `arm-check` heading, #222's paragraph on `depth_two`, and #556's two
comments on `close` and `seal`.

**What `CLAUDE.md` needs: nothing from this phase.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the *half #423's finding 4 was about* characterisation in the gate-steps module's docstring | the same docstring, as a narrow reader naming both directions; the ledger's G1 copy goes to phase 6 |
| *every earlier run kept behind it* in `agents/sealer.md`, and the two always-kept comments in `round_record.py` | the same places, naming the same-run replace |
