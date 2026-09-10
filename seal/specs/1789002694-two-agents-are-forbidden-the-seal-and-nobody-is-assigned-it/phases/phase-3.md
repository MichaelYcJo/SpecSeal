# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `d515213` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build `plan.md`'s row 3 and nothing past it. `agents/sealer.md` — opening with
the contract paragraph every definition carries, `skills:` listing
`agent-contract` alone, stating the four conditions in its own words rather
than preloading `verify` (Q5), naming its one write and #120 as the ticket
that settles §2. `agents/smith.md` and `agents/warden.md`: *the full suite is
the orchestrator's, once, after the rounds* becomes the sealer's, both gain
the coverage-probe sentence, the warden's *carry the broad-gate state* bullet
gains that what comes due is the sealer's spawn, and the smith's *Then the
broad gate runs once* gains who runs it. The documents that name the owner —
`skills/code-review/orchestration.md`, `skills/verify/SKILL.md`,
`docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`,
`CONTRIBUTING.md`, `bin/test`'s comment, `templates/sdd-round.md`'s `Broad
gate` row comment. Both READMEs' agent tables and the chain diagram's `broad
gate` line, which move together. The pinned sentences re-pointed and each seen
red against the file it left. Tests part 3 in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`: S6 and S7, every case
seen red first. And name in this record the paragraph #120 deletes, so #120's
frame finds it.

Facts came labelled. `executed`: phase 2's verification re-run at `52f6bd3` —
seven modules, 280 passed, ruff clean, the gate's two exit-2 refusals.
`read`: phase 2's handback (the sealer's command, `--record`'s refusal as exit
2, the non-uniform exit codes the gate handles); the four conditions; the
three test modules that read `agents/*.md` and the fourth that derives the
preloaded-skill counts; the sentences that change, with their coordinates.
`unverified`, this phase the answerer: whether `payload-meter --agent sealer`
reports what the handoff expected.

## What this phase found

**`payload-meter` does not exist in this tree, so the phase's one unverified
fact cannot be answered by running it.** `command -v payload-meter` and
`ls bin/ | grep payload` both return nothing, and `find . -name
'payload_meter*'` finds no file. It is #292's, which `docs/flow.md` orders
**fourth** in this release — after #30 — so the fact as handed over asked for
a command that ships two work items later. Phase 1 reported the same absence
from the other side: it was named as one of two sibling scripts carrying the
interpreter-floor guard, and only a stale `.pyc` was there.

What the meter would have reported was measured by hand instead, from the
definition and the skill bodies its `skills:` list injects:

| Agent | Definition | Preloaded | Payload |
|---|---|---|---|
| `sealer` | 6,279 B | `agent-contract` | **20,044 B** |
| `scribe` | 3,469 B | `agent-contract` · `legacy-parity` | 22,598 B |
| `warden` | 21,778 B | `agent-contract` · `code-review` · `writing-style` | 78,520 B |
| `smith` | 19,013 B | `agent-contract` · `implement` · `writing-style` | 98,789 B |

The sealer is the smallest payload of the four, and Q5's answer is what makes
it so: `skills/verify/SKILL.md` is 35 KB, which would have trebled it for four
conditions the definition states in twelve lines. The number is a byte count
of what is written into the spawn, not the meter's `cache_creation` reading;
those are different measurements and only the second answers #292's question.

**The spec's list of pinned sentences is one short, and the missing one is the
same class.** `spec.md` §Scope 6 names *three sentences two test modules pin
(`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:153, :764`)* — the
count is three and the coordinates are two. The third is `:733`,
`test_the_section_says_the_full_run_is_the_orchestrators`, which reads <!-- NAME NOT IN TREE: phase 4 renamed it to `..._the_sealers`, which is what this paragraph hands over; the old name is what phase 3 actually read -->
`CONTRIBUTING.md` §*Running the checks* the way `:153` reads `bin/test`. All
three were seen red against the file each left, in one run, before any of them
was re-pointed.

**Two of the three cases keep their names, and one of them now says why.**
`test_the_section_says_the_full_run_is_the_orchestrators` is cited as a <!-- NAME NOT IN TREE: the name as it stood when phase 3 read it; phase 4 carried out the rename this paragraph asks for -->
coordinate by `seal/ledger.md`'s R4 row. Renaming it removes an anchor rather
than drifting one, and a removed anchor is BROKEN where a changed body is
DRIFTED — so the rename belongs to the phase that touches the ledger, beside
the row it forces. The docstring carries that reason so the next reader does
not read the stale name as an oversight. **For phase 4**: rename it to
`..._the_sealers`, remove that coordinate from R4 in `seal/ledger.md`, and
write the new case name into `seal/ledger/<id>.md`.

**The survivor check found two real survivors, and both were the check's own
failure messages.** `chain_check.py` told a reader, at the moment a pull
request is refused, to *run it once now that the rounds have settled* and to
write the cell with `round_record.py close --broad-gate` — the exact
instruction this phase moved to a spawn, in the one place a person actually
reads it. `spec.md` §Scope 6 lists seven documents and not this file, because
it is a script rather than a document; the class is *what names the owner*,
and a printed message is in it. Both messages now name the `sealer` and
`broad-gate --record`, the second keeping `close --broad-gate` as the
fixes-and-gate-in-one-pass route, and both are pinned on the printed output
(§14) with three mutation arms shown red. The third survivor, `README.md:71`,
is exempted in `survivors.md`: it says the comparison happens *at the gate*
and names no actor, which is still true.

**`chain_check.py:2885` and `:2946` still say `close --broad-gate` is the only
thing that changes the cell.** They are comments explaining why an unparseable
cell above the cutoff is a cell somebody chose, and the reasoning survives
`seal` joining `close` — both are subcommands, neither is free text. The
docstring of the case that pins that arm was corrected to name both; the two
code comments were left, and the survivor check does not reach them because
the sentence they share was not removed by this range.

**Adding a fourth definition moves none of the README's derived counts, which
was confirmed rather than assumed.** `test_chain_hooks_hardening.py` derives
the preloaded-skill set from `agents/*.md` and the three group counts from the
skills tree; `agent-contract` was already preloaded by three agents, so the
set, the counts and the agent-table names are unchanged. All 190 of that
module's cases pass except the one below.

**`agents/sealer.md` joins `tests/test_docs_line_wrap.py`'s covered list.** It
was written wrapped, and that module's own docstring says to add a file once
its prose fits rather than raising the limit. It is the only `agents/*.md`
file with no sweep behind it — `smith.md` and `scribe.md` sit at 148 and 160
columns, which is why the docstring lists them instead of the list holding
them.

**The one failure in the phase's own module list is phase 4's.**
`test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
fails on this work item, which has `spec.md` and `plan.md` and no
`overview.md`. `plan.md` row 4 writes it. This is the same failure phase 2's
one real `broad-gate` run reported and labelled `new`.

**The paragraph #120 deletes** is `agents/sealer.md` §*§2 as it stands, and
#120* — the whole section, heading included. It states that §2 forbids the
sealer's one act, that #120 settles §2 and §6 against the whole set of agents
before this release ships, and that until then the definition is the narrower
document and the contract the wider one. Its last line says so in the file:
*When #120 lands, this section is the paragraph it deletes.* `#120` and
`narrower document` are both pinned by
`test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it`, so
#120's frame has to remove the case in the same commit as the section.

**Seen red, then mutated.** All 16 part-3 cases ran with `agents/sealer.md`
absent and the two definitions unedited: 16 red. Twelve mutation arms then
each broke one thing and ran its case — a 15-word run of §2 pasted into the
sealer's definition, the subcommand dropped from the one-write paragraph,
`#120` dropped, the tree-state condition dropped, `verify` added to the
`skills:` list, the command dropped, the smith saying `orchestrator` again,
the owner sentence stated twice, each definition's probe sentence deleted, the
warden no longer naming what comes due, and the smith's closing paragraph
unassigned again. Every arm red. Three further arms on `chain_check.py`'s two
messages — the agent unnamed in each, and the one-pass route dropped from the
second — all red. Every file restored from bytes the script held and
sha256-compared after each arm; `tests/__pycache__` cleared between arms.

**Two arms were wrong before they were right, and both were the arm's fault.**
The §2 paste sliced the section from `split("## §2 ")[1]`, which keeps the
heading text, so the 15 words straddled the heading/body boundary and matched
nothing the test reads; and the probe-sentence arms used a regex with no
whitespace tolerance where the file wraps *never as a\n   seal*. An arm that
does not apply is reported as `ARM DID NOT APPLY` rather than passing, which
is what caught both.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/smith.md`'s *When the broad gate returns a failure, first ask whether it fails on the base commit as well* — an act the smith performed | the gate. `broad_gate.py` re-runs the failing files at the base and hands back `new` or `failing on base too`; the smith's paragraph now reads that word instead of asking the question |
| `skills/code-review/orchestration.md`'s instruction to run the pass and write the cell with `close --broad-gate` | the same paragraph, as a spawn: `sealer` with the base and the item. `close --broad-gate` is kept in it, named for the one case `seal` refuses — fixes and the gate landing in one pass |
| `chain_check.py`'s two failure messages telling a reader to run the pass and use `close --broad-gate` | the same two messages, naming the sealer's spawn and `broad-gate --record`; pinned by two assertions in `tests/test_chain_check_at_the_pull_request.py` |
