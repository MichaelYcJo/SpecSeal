# 1789034970-the-contract-is-settled-against-the-agents-that-exist — review round 1

| Field | Value |
|---|---|
| Target SHA | 5aa83af |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 338 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1 through 8. Finding 1 is the one that reopens the |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of #120 at `5aa83af`, the whole branch `docs/120-the-contract-is-settled-against-the-agents-that-exist` against `release/v0.10.0` (`d35c874`, 29 files, +1,302 / −74), draft pull request #338. Three sections of `skills/agent-contract/SKILL.md` rewritten in place — §2, §6, §7, none added, retired or renumbered — plus `agents/sealer.md`'s expiring paragraph deleted and replaced, `agents/warden.md` and `skills/code-review/orchestration.md` re-pointed, `templates/sdd-routing.md` given the criterion that decides its `Implementation` row, six test modules, a ledger fragment and one anchor removed from another work item's. `questions.md`'s four owner answers are ratified and rank above the code: one file rather than a split, §7 widened rather than enumerated, the `Implementation` criterion in place of freezing `smith`'s scope, and the routing. One class to enumerate for this change, and it is not the coordinates the diff touched: every place in the tree that states what §2, §6 or §7 says, or that describes an agent's durable write as an exception — the implementer reported that `survivor-check` exits 0 over the range while a hand sweep for the sentence rather than the vocabulary found four more places still speaking in the present tense, and the question is whether four was all of it. Six shapes offered as candidates rather than findings: a per-role conditional hiding in the rewritten §2 or §6, against the contract's own opening; §6's new default as a widening, since any loose sentence in the four definitions that mentions writing may now read as a grant the old blanket prohibition refused; the widened §7 against `broad_gate.py`, which creates and removes a worktree of its own; the two renamed cases and the ledger anchors they moved, against `CLAUDE.md`'s REMOVED rule; `test_the_window_sits_between_what_was_measured`, whose `<=` bound the implementer reported staying silent at exactly 10 words; and whether `templates/sdd-routing.md` still parses as unanswered with the criterion added. Facts handed over as executed by the orchestrator at `5aa83af`: ten modules, 367 passed, exit 0. Handed over as read: the implementer's own 19 modules at 614 passed, `evidence-check` 1,111 ok, `survivor-check` and `unverified-check` exit 0, ruff clean on changed files, one unit added and mutated. Handed over as unverified: the full suite, the repository-wide lint and the typecheck, answered by the sealer once the rounds settle — §2 as rewritten is what says so, and it is not the reviewer's to take. One correction handed over: `spec.md` and `plan.md` say the stray worktree surfaced when `git switch` refused *a branch it still held* where #120's comment says *a branch another worktree already held*, and the two frame documents were not corrected. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Runner: `bin/test tests/<module> -q`; `bin/evidence-check` has two forms and the unscoped read is the one a pull request runs.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | §7's file-only half survives in the procedure a reviewer follows | `skills/code-review/SKILL.md:141` | open | The row states deleting one named file as the whole obligation. §7's own story is a reviewer who followed exactly that and left a worktree. No case pins the row; the branch's records never name the file |
| 2 | *until the rounds settle* releases the suite to the warden | `agents/warden.md:157` | open | New §2 has no temporal release. This file assigns none of the three; `agents/sealer.md:110` says it is the only one that does. `841ef4a` re-pointed `:187` and `:199` in this file and missed `:157` |
| 3 | A third write against the *no third* this branch wrote | `agents/warden.md:238` | open | The report format has no field for broad-gate state, and `agents/sealer.md:92` now owns the `Broad gate` cell. Two definitions naming one cell |
| 4 | §6's new default makes a persona line an unbounded grant | `agents/smith.md:22` | open | *stamp it with your mark* and *leave durable evidence* name two things §6 lists as durable records. No closing sentence bounds them, where `agents/sealer.md:88` has one |
| 5 | Six rows re-anchored, none had `Checked` moved | `seal/ledger.md` (L7, L8, W1 and three orchestration rows) | open | `templates/ledger.md:48` states the rule. The branch's own fragment rows all carry 2026-09-10; the shared file's six carry dates from before the content moved. `--reverify` never writes `Checked`, so nothing catches it |
| 6 | §2 asserts *One definition* and nothing counts | `skills/agent-contract/SKILL.md:64` | open | §5 of the same file says an aggregate is not a coordinate. `tests/test_broad_gate_rule.py:248` pins the phrase present, not the number true. The framer arrives in 0.11.0 per `questions.md` Q2 |
| 7 | The widened §7 names a venv this repository reuses on purpose | `skills/agent-contract/SKILL.md:174` | open | `bin/test` builds `.venv` once for #156's 55-58 seconds per call. A probe's run creates it; §7 says every leaving goes. No clause separates the probe's own leavings from the tooling's |
| 8 | A three-way criterion for a two-valued row | `templates/sdd-routing.md:29` | open | `IMPLEMENTATION_ANSWERS` is `smith` and `the session`; the criterion routes finding-out to `scribe` and never says what to type. Line 27 permits deleting the row, which is the wrong recovery |
| 9 | Old-§6 vocabulary the re-point missed | `agents/warden.md:180`, `:283` | open | `:283` back-references a section that no longer contains *exception* |
| 10 | §6's withheld four recited as a different four | `agents/sealer.md:104` | open | Drops `post`, adds `commit`. §6 binds regardless, so nothing ships broken |
| 11 | The canary is silent at its own boundary | `tests/test_a_moved_rule_leaves_its_definition.py:206` | open | `<=` against a maximum, not per pair. Measured 10 at both `d35c874` and `5aa83af`; this branch moved nothing |
| 12 | *a branch it still held* was not corrected | `spec.md:44`, `plan.md:152` | open | Agrees in substance with the contract at `:183`; the contract's wording is the one that ships |

## Paste-ready fixes

```
| Probe | Temporary test to settle what reading can't | You write it, run it, **delete it** (name `test_tmp_*`) — and everything else it made goes with it. The verified fact goes into the report |
| Regression test | Test that should exist but doesn't | **You don't write it.** Hand it over as a list with the target file per row |

Batch probe cases into one file and run once. Never probe what reading answers
— schema constraints, enums, defaults settle "can this state even exist"
claims without running anything. Don't touch `test_tmp_*` files another
session created.

**The file is not the whole of it.** Contract §7 is about leavings, not
files: a worktree, a branch, a checkout, a scratch clone or a virtual
environment your probe made is a leaving too, and the probe is not over until
every one of them is gone. Deleting the named file and stopping there is what
left a git worktree behind through #30's whole review chain, with the report
saying the probe files were deleted and nothing wrong with that sentence.
```
```
  §2 never puts the suite in your hands, before the rounds or after them:
  the broad gate goes to whichever definition assigns it and this file
  assigns none of the three. The part of it that is yours is the audit. The
  smith hands over with the suite labeled `unverified` on purpose, so what
  you check is whether that label is honest — not whether the number is
  green.
```
```
- **Carry the broad-gate state into your report** the way you carry probe
  results, under `## Executed probes` where it has a row to sit in. Whether
  the one full-suite run has happened — `not yet`, or the SHA it ran at and
  the base it was compared against — is invisible in the code, and the next
  session either repeats a sealed run or ships assuming someone else made it.
  The `Broad gate` cell itself is the sealer's one write
  (`agents/sealer.md`), so what you produce is the sentence it and the
  orchestrator read, never the cell. You are also what can say the gate has
  come due: when your
```
```
You forge the work — building and reforging alike — and stamp it with your
mark. You implement against written specs and leave durable evidence — and
what that comes to is the files this file names below, which under §6 is the
whole of what you write: a write not named here is a write you do not make.
The
```
```
**Re-read 2026-09-10 in work item 1789034970 (#120), phase 3.** The anchor's
content changed — §7's body widened / §2's sentence in `orchestration.md`
reworded — so the hash was recomputed. The claim itself is untouched and it
holds.
```
```
**Re-read 2026-09-10 in work item 1789034970 (#120), phase 3.** §7's body
gained the leavings paragraph and the #30 story; its heading, which is this
row's anchor, is untouched by design (see R3 of that item's fragment). The
claim — that the definitions point at §7 and §8 rather than restating them —
was re-checked against all four definitions and holds.
```
```python
def test_only_one_definition_assigns_the_broad_gate():
    """§2 says `One definition in this plugin does hand them over`. That is a
    COUNT, and §5 of the same file says an aggregate is not a coordinate --
    the number can be checked while the claim it stands for cannot.

    So it is checked here, from the glob rather than from a list. #120 left
    the assignment in the definitions on purpose, and `questions.md` Q2 names
    the framer as arriving in 0.11.0; if its file assigns any of the three,
    the contract says `One` and is false with nothing red."""
    import glob

    agents = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))
    assert len(agents) >= 4, f"agents/*.md matched {len(agents)} files"
    assigning = [
        os.path.basename(p)
        for p in agents
        if "spawned for exactly that" in " ".join(read_path(p).split())
    ]
    assert assigning == ["sealer.md"], (
        f"{len(assigning)} definitions assign the broad gate ({assigning}), "
        "and §2 says `One definition in this plugin does hand them over`. "
        "Either that sentence needs the new count, or a definition took the "
        "gate without the contract's sentence following it"
    )
```
```
**The rule is about leavings, not about files.** A probe leaves nothing
behind, whatever kind of thing it made — a worktree, a branch, a checkout, a
scratch clone, a virtual environment — and it is not over until every one of
them is gone. Those are examples and not the list: the shapes are deliberately
not enumerated, because every enumeration in this repository has rotted, and
the next leaving is a kind nobody here has met. A list that predates it reads
as permission.

What the probe made for ITSELF is what goes. A thing the repository's own
tooling builds to be reused is not your probe's leaving even when your probe's
run is what created it — `bin/test` builds `.venv` once and every later call
reuses it, and deleting it because a probe ran first is #156's 55-58 seconds
per call paid again by whoever comes next. The question is whose the thing is,
not who happened to trigger it.
```
```
     HOW TO ANSWER IT — the criterion, so the row is not answered by habit.
     Ask whether this work is FINDING OUT or WRITING DOWN. Finding out — what
     an unfamiliar codebase does, where a behaviour lives, what an original
     actually did — is a step to send to `scribe`: a large input and a small
     output is what a subagent boundary is for. That is a step, NOT an answer
     to this row, which has two values and no third: the session that reads
     the facts back and writes the code still answers `the session`. Writing
     down stays with the session too, because a delegate re-buys the context
     the session already holds. The one case `smith` answers is a diff large
     enough to threaten what the orchestrator still has to hold.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_agent_contract_holds_the_universal_rules.py tests/test_broad_gate_rule.py tests/test_a_moved_rule_leaves_its_definition.py tests/test_every_agent_reads_the_contract.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_waiver_decided_at_start.py tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_the_reviewers_report_reaches_the_record.py -q` in the clone at `5aa83af` | exit 0, 343 passed in 56.59s. Confirms the account's ten-module claim on the eight modules that overlap, plus one module the account did not name |
| The same `bin/test` call was the first in a fresh clone | It built `.venv` with `uv` — five packages resolved and installed — and every later call reused it. This is the leaving finding 7 is about |
| Longest shared phrase between every `agents/*.md` and every contract section, computed from the module's own `longest_shared` and `SECTIONS`, at `5aa83af` | 10 (`agents/smith.md`, §8), then 9 (`agents/warden.md`, §6), then 8 (`agents/smith.md`, §3). `agents/sealer.md` does not reach the top eight |
| The same computation against a `git archive` of the base `d35c874` | Identical: 10 / 9 / 8, same pairs. This branch moved no number, which is what finding 11 rests on |
| `hooks/routing.py` loaded against the shipped `templates/sdd-routing.md` | Every added line sits inside the `<!-- -->` block and none begins with `\|`, so `table_rows` never sees them; the row still parses to `implementation is None`. `tests/test_waiver_decided_at_start.py` green |
| `Checked` column extracted from every changed row of `seal/ledger.md` across `d35c874...5aa83af` | Six rows changed hash, zero changed date. The table in finding 5 is that output |
| `git show --stat` per commit over `23ca89c..5aa83af` | `2821f6d` re-anchored five rows, `5aa83af` one. Neither commit's message claims a `Checked` bump |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `smith`'s §-by-§ scoping | Already deferred by `questions.md` Q4, with the criterion landing in `templates/sdd-routing.md` instead | The owner, at the release that retires or re-scopes `smith` |
| Whether §2's naming survives the framer | Finding 6 asks for a check, not a decision. The decision is `questions.md` Q2's — the line is redrawn in 0.11.0 | The owner, at 0.11.0 |
