# Round 1 report — the contract is settled against the agents that exist

Target SHA `5aa83af`, base `release/v0.10.0` (`d35c874`), branch
`docs/120-the-contract-is-settled-against-the-agents-that-exist`, draft pull
request #338. No earlier round record exists; nothing was inherited.

Reviewed in a `git clone --no-local` at the target SHA. No file in the user's
checkout was written except this report.

## What the account claimed, and what the code says

The orchestrator handed over three labelled facts and one enumeration claim.
Each was checked rather than adopted.

**The ten-module run is confirmed.** Re-run in the clone at `5aa83af`, exit 0.
My set added `tests/test_a_moved_rule_leaves_its_definition.py` and dropped
three modules the handoff named; 343 passed. Nothing red.

**The enumeration claim is false, and that is the round's headline.** The
account says a hand sweep for the sentence rather than the vocabulary found
four places still speaking in the present tense, and asks whether four was all
of it. It was not. `skills/code-review/SKILL.md:141` states §7 as a rule about
one file, and it is the procedure document the reviewer in §7's own story was
following. Finding 1 is that place. A second miss, `agents/warden.md:157`,
is a sentence about §2 in a file this branch did edit.

**The ratified answers hold.** `questions.md`'s four owner answers rank above
the code and none of my findings asks for any of them to be reopened. Q2's
one-file decision is honoured — sixteen sections, none added, retired or
renumbered, so no `§N` citation in any existing round record changed meaning.
Q3's widened §7 is the sentence I question in finding 7, but I question its
boundary, not the decision to widen. Q4's deferral of `smith`'s sections is
honoured; finding 4 is about §6's grant surface, which Q4 did not defer.

## Findings

Findings from reading are marked (read); findings from execution are marked
(executed). Every 🔴 and 🟡 has a paste-ready fix below.

### 🔴 1 — `skills/code-review/SKILL.md:141`: §7's file-only half survives in the procedure the reviewer actually follows (read)

The contract's new §7 carries the story that justifies the widening: a
reviewer *"did follow [the file half], to the letter, during #30's review
chain — and the probe still left a git worktree behind."* The document that
reviewer follows is the `code-review` skill, which every warden loads on every
spawn. Its Probes row still reads:

    | Probe | Temporary test to settle what reading can't | You write it,
      run it, **delete it** (name `test_tmp_*`). The verified fact goes into
      the report |

Deleting the named file is stated as the whole of the obligation, which is
exactly the reading §7 was rewritten to end. Nothing in that skill mentions a
worktree, a clone or a venv, and no case pins the row.

Why it matters: a reviewer who reads the skill's summary table and acts on it
reproduces the #30 leaving. The contract now says otherwise, but the skill is
the closer document to the act, and the branch's own §7 story is evidence that
a reviewer follows the procedure rather than reconciling two documents.

This is the instance-versus-class failure §12 names, applied to the branch's
own headline fix: §7's text was corrected at the coordinate and the class —
every place that states the probe rule — was not closed. `agents/scribe.md:44`
shows the shape that survives a widening: it points at §7 instead of restating
it.

### 🟡 2 — `agents/warden.md:157`: a temporal release from a rule that has none (read)

> §2 keeps the suite out of your hands until the rounds settle, and the part
> of it that is yours is the audit.

*Until the rounds settle* says the suite becomes the warden's afterwards. The
new §2 has no such release for anyone: the gate belongs to whichever
definition assigns it, `agents/warden.md` assigns none of the three, and
`agents/sealer.md:110` says its file is the only one in the plugin that does.

This is the fifth place in the class the account asked me to enumerate, and it
is in a file the branch edited — `841ef4a` re-pointed `:187` and `:199` in the
same file and left `:157` alone. It also sits against a live hazard:
`agents/warden.md:60` puts a warden in exactly the moment the sentence appears
to release, telling it that its own unchecked box is what holds the gate.

### 🟡 3 — `agents/warden.md:238`: a third write, against a sentence this branch wrote saying there is no third (read)

The branch changed `:199` to read *"the two writes this file names, which
under §6 is the whole of what you may write; both are yours alone, and there
is no third."* Forty lines later the same file says:

> **Carry the broad-gate state into `round-N.md`** the way you carry probe
> results.

Two problems, and the qualifier fixes only part of the first. *The way you
carry probe results* means via the report, which the generator copies — so it
is recoverable. But the warden's report format has no field for it: the three
tables are `## Verdicts`, `## Executed probes` and `## Deferred`, plus the two
terminal lines. `agents/warden.md:130` is the sentence that names this exact
failure — *"An answer the report format has no field for is a decision that
lives in a transcript."*

Second, and newer: the `Broad gate` cell now has an owner.
`agents/sealer.md:92` names it as the sealer's one write, and
`round_record.py`'s `seal` subcommand is the only thing that makes it. Two
definitions naming one cell is the state §6's rewrite exists to make
impossible.

### 🟡 4 — `agents/smith.md:22`: §6's new default turns a persona line into an unbounded grant (read)

> You forge the work — building and reforging alike — and stamp it with your
> mark. You implement against written specs and leave durable evidence.

Old §6 was a blanket prohibition plus a pointer to deliberate, marked
exceptions, so this sentence was decorative — a reader looking for permission
was looking for a carve-out and this is not one. New §6 asks a weaker
question: *is this write named in your own definition*. This sentence names
two things §6 itself lists as durable records — *a mark on the tree* and
durable evidence generally — and nothing in the file bounds them to the
specific files named further down.

`agents/sealer.md:88` shows the closing form the change requires and the
sealer got: *"This paragraph is that naming, and it is the whole of it — a
write not below is a write you do not make."* `agents/smith.md` has no such
sentence, so its named writes read as examples rather than as the list.

Q4 deferred `smith`'s §-by-§ scoping. It did not defer §6's grant surface, and
this is a widening the rewrite caused in a file the rewrite did not open.

### 🟡 5 — `seal/ledger.md`: six rows were re-anchored and none had `Checked` moved (executed)

`templates/ledger.md:48` states the rule: *"The **Checked** column carries the
date somebody read the code. Re-verifying a row is re-reading it and then
running `evidence-check --reverify`."*

Six rows in the shared file got new anchor hashes on this branch and all six
kept their old dates:

| Row | Checked, before and after |
|---|---|
| L7 (contract §7) | 2026-09-03 → 2026-09-03 |
| L8 (contract §3) | 2026-09-03 → 2026-09-03 |
| the fix-pass row | 2026-09-08 → 2026-09-08 |
| the orchestrator-is-bound row | 2026-09-08 → 2026-09-08 |
| the seam row | 2026-09-10 → 2026-09-10 |
| W1 (the survivor step) | 2026-09-08 → 2026-09-08 |

L7 is the sharpest: its anchor is §7's heading, and the hash moved because
§7's body was widened by this branch. The ledger now records a claim about §7
as last read on 2026-09-03, pointing at content rewritten on 2026-09-10.

The branch knows the convention — its own fragment rows R1, R2 and R3 all
carry `2026-09-10` — so this is the shared file being held to a lower standard
than the fragment. Nothing enforces it: `--reverify` recomputes the hash and
never touches `Checked`, which is why the miss is silent. It is also the risk
`tests/test_the_handoff_names_the_form_it_ran.py:86` names in one phrase —
*"`--reverify` re-stamps a false claim."*

### 🟡 6 — `skills/agent-contract/SKILL.md`: §2 asserts a count nothing checks (read)

> One definition in this plugin does hand them over — the sealer's, whose
> whole procedure is that run — and that assignment lives there rather than
> here, which is where the next one will live too.

*One* is an aggregate, and §5 of this very file says an aggregate is not a
coordinate: the number can be checked while the claim it stands for cannot.
`tests/test_broad_gate_rule.py:248` pins the phrase *present*; nothing counts
`agents/*.md` to confirm the number is still one.

`questions.md` Q2 names the framer as arriving in 0.11.0 and argues the line
is redrawn then. If the framer's definition assigns any of the three, §2 says
*One* and is false with nothing red. The machinery already exists — both
`tests/test_a_moved_rule_leaves_its_definition.py:152` and
`tests/test_every_agent_reads_the_contract.py:126` glob `agents/*.md` and
assert on the result — so the check is cheap and the class is enumerable by
construction rather than by reading.

### 🟡 7 — `skills/agent-contract/SKILL.md:174`: the widened §7 names a virtual environment, and this repository reuses one on purpose (executed)

§7 now reads *"A probe leaves nothing behind, whatever kind of thing it made —
a worktree, a branch, a checkout, a scratch clone, a virtual environment — and
it is not over until every one of them is gone."*

`bin/test` exists to build `.venv` once and reuse it. Its own header states
the cost of not doing so: *"Issue #156: the form `CONTRIBUTING.md` named paid
55-58 seconds of setup per call, on all seventeen test calls of one measured
segment."* I reproduced the build: my first `bin/test` call in a fresh clone
created `.venv`, resolved and installed five packages, and every call after it
reused them.

So an agent that writes a probe, runs it through `bin/test` in a fresh clone,
and then follows §7 to the letter deletes the venv its probe's run created —
and #156's saving is destroyed for every remaining call of the segment. §7
names the venv explicitly and draws no line between what the probe made for
itself and what the repository's tooling builds to be reused.

Q3 ratified the general form over an enumeration, and I am not asking to
reopen that. The general form still needs the clause that says whose leaving
it is.

### 🟡 8 — `templates/sdd-routing.md:29`: a three-way criterion for a two-valued row (read)

The added guidance asks *"whether this work is FINDING OUT or WRITING DOWN"*
and routes finding-out to `scribe`. The row it explains accepts exactly two
values — `hooks/routing.py`'s `IMPLEMENTATION_ANSWERS` is `smith` and
`the session` — and line 27 of the same comment says *"Delete the row rather
than inventing a third answer."*

A session whose work is finding-out is told where the work goes and never told
what to write. The two available readings diverge: answer `the session` and
spawn `scribe` for the discovery step, or take line 27 literally and delete
the row. The second is wrong and the comment permits it.

The row is the one axis nothing contradicts — the comment says so itself at
line 46 — so a session that reads the criterion and guesses gets no correction
from anywhere. The criterion is faithful to `questions.md` Q4; the gap is that
Q4 was answering how to think about the axis, and the template has to answer
what to type.

Executed: the parser is unaffected. `hooks/routing.py`'s `table_rows` reads
only lines beginning with `|`, every added line sits inside the `<!-- -->`
block, and the shipped row still parses to `implementation is None`.
`tests/test_waiver_decided_at_start.py` is green.

### ⬜ 9 — `agents/warden.md:180` and `:283`: old-§6 vocabulary the re-point missed (read)

`841ef4a` changed `:187` from *the second exception* to *the second of them*
and `:199` from *§6's two exceptions* to *the two writes this file names*, and
left the bullet's own title at `:180` reading **§6's instances are yours by
name** and its closing at `:283` reading *"§Role above says why that is one
exception and not a general permission."* The second is a back-reference to a
section that no longer contains the word. Same class as findings 1 and 2:
the coordinates were corrected, the instances around them were not.

### ⬜ 10 — `agents/sealer.md:104` recites §6's withheld acts and gets the list wrong (read)

> Everything else §6 withholds stays withheld: no pull request, no push, no
> commit, no agent spawned.

§6's four are *post, push, pull request, spawn*. This drops `post` and adds
`commit`, which §6 withholds from nobody. No defect ships — §6 now says the
four bind *whatever its file says*, so the sealer cannot grant itself posting
either way — but the branch made §6's list explicit and countable, which is
what turns a loose recitation into a checkable one that does not match.

### ⬜ 11 — `tests/test_a_moved_rule_leaves_its_definition.py:206`: the canary is silent at its own boundary (executed)

    assert widest[0] <= LONGEST_KEPT_APPLICATION

`LONGEST_KEPT_APPLICATION` is 10 and the assertion is `<=`, so it fires only
at 11. The docstring says the case exists because *"a kept application grows
until it shares more than `WINDOW` words with a section"* and the message says
*"the margin under the window is shrinking."* At exactly 10 it says nothing —
which is what the account reports happening to the first draft of the sealer's
new section.

Measured at both ends: the widest pair is 10 at `5aa83af` and 10 at `d35c874`,
`agents/smith.md` against §8 in both. This branch moved no number, so leaving
the assertion is defensible and I am not asking for it to change.

The gap worth writing down is a different one from the account's. The
assertion is on the maximum, not per pair. The docstring records the 10 as one
named pair — `agents/smith.md`'s *a bare word is a pathspec and git rejects
it* — so a **different** definition newly reaching 10 leaves the maximum at 10
and the case silent, and a new near-copy has appeared with nothing saying so.
The primary guard at `WINDOW` 15 is intact, so no defect ships; this is a
canary one word less sensitive than its own docstring claims.

### ⬜ 12 — `spec.md:44` and `plan.md:152` keep the uncorrected framing (read)

Both say `git switch` refused *"a branch it still held"*; the contract at
`:183` says *"a branch a worktree already held"*, following #120's comment.
The two agree in substance — the antecedent of *it* is the leftover worktree —
so nothing downstream is wrong. The contract's wording is the clearer one and
is the one that ships. Recorded as a correction, not a fix: both files are
under `seal/specs/`.

## ❓ Out of verified scope

**The full suite, the repository-wide lint and the typecheck.** Not run. §2 as
this branch rewrites it assigns them to whichever definition names them, and
`agents/warden.md` names none. Answered by **the sealer**, spawned once the
rounds settle.

**`bin/evidence-check`, scoped or unscoped.** The prompt offered it; I declined
and ran nothing. `skills/verify/scripts/broad_gate.py:128` bundles
`evidence_check.py` into the single broad act, and §2's three are named
narrowly enough that I could not settle whether the bundled reading governs.
§3 says to run nothing extra and disclose rather than refuse outright, so that
is what this line is. It would not have changed finding 5 in either direction:
the six hashes were bumped, so they resolve — what is stale is the `Checked`
date beside them, which no checker reads. Answered by **the orchestrator**,
before the sealer's spawn.

**Whether §2 naming the sealer is a per-role exception** (the account's axis 1).
Judged, not deferred: it is a pointer, not an exception. The rule in the
section is universal — *Whether it is yours is what your own definition says* —
and applies unchanged to an agent that does not exist yet. Ledger row R2 makes
the same argument and I reached it independently before reading the row. What
the naming does carry is an unchecked count, which is finding 6.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `smith`'s §-by-§ scoping | Already deferred by `questions.md` Q4, with the criterion landing in `templates/sdd-routing.md` instead | The owner, at the release that retires or re-scopes `smith` |
| Whether §2's naming survives the framer | Finding 6 asks for a check, not a decision. The decision is `questions.md` Q2's — the line is redrawn in 0.11.0 | The owner, at 0.11.0 |

## Paste-ready fixes

Finding 1 — `skills/code-review/SKILL.md:141`, the Probes row and the
paragraph under it:

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

Finding 2 — `agents/warden.md:157`:

```
  §2 never puts the suite in your hands, before the rounds or after them:
  the broad gate goes to whichever definition assigns it and this file
  assigns none of the three. The part of it that is yours is the audit. The
  smith hands over with the suite labeled `unverified` on purpose, so what
  you check is whether that label is honest — not whether the number is
  green.
```

Finding 3 — `agents/warden.md:238`, redirecting the destination to the report:

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

Finding 4 — `agents/smith.md:22`, adding the bounding sentence the sealer has:

```
You forge the work — building and reforging alike — and stamp it with your
mark. You implement against written specs and leave durable evidence — and
what that comes to is the files this file names below, which under §6 is the
whole of what you write: a write not named here is a write you do not make.
The
```

Finding 5 — `seal/ledger.md`, the six re-anchored rows. Set the `Checked`
cell of each to `2026-09-10` and append one sentence to its `Notes`. For the
three rows whose `Notes` already carry the re-read convention, the appended
sentence takes the same shape they already use:

```
**Re-read 2026-09-10 in work item 1789034970 (#120), phase 3.** The anchor's
content changed — §7's body widened / §2's sentence in `orchestration.md`
reworded — so the hash was recomputed. The claim itself is untouched and it
holds.
```

For L7, whose anchor is the section this branch actually rewrote, the
sentence has to say what was re-read rather than only that it was:

```
**Re-read 2026-09-10 in work item 1789034970 (#120), phase 3.** §7's body
gained the leavings paragraph and the #30 story; its heading, which is this
row's anchor, is untouched by design (see R3 of that item's fragment). The
claim — that the definitions point at §7 and §8 rather than restating them —
was re-checked against all four definitions and holds.
```

Finding 6 — a case in `tests/test_broad_gate_rule.py`, next to
`test_the_prohibition_itself_has_one_home_and_it_is_the_contract`. The name
below does not exist in the tree yet:

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

Finding 7 — `skills/agent-contract/SKILL.md:174`, bounding the leaving to
what the probe made for itself:

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

Finding 8 — `templates/sdd-routing.md:29`, saying what to type:

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

## Proof

Files opened, in the clone at `5aa83af` unless noted:
`skills/agent-contract/SKILL.md`, `agents/smith.md`, `agents/warden.md`,
`agents/scribe.md`, `agents/sealer.md`, `skills/code-review/SKILL.md`,
`skills/code-review/orchestration.md`,
`skills/code-review/scripts/survivor_check.py`,
`skills/code-review/scripts/round_record.py`,
`skills/verify/scripts/broad_gate.py`, `templates/sdd-routing.md`,
`templates/ledger.md`, `hooks/routing.py`, `bin/test`,
`.github/workflows/hygiene.yml`, `docs/flow.md`, `seal/ledger.md`,
`seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md`,
`seal/ledger/1789034970-the-contract-is-settled-against-the-agents-that-exist.md`,
`tests/test_broad_gate_rule.py`,
`tests/test_the_agent_contract_holds_the_universal_rules.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_waiver_decided_at_start.py`,
`tests/test_a_moved_rule_leaves_its_definition.py`,
`tests/test_docs_line_wrap.py`, and in the work item directory
`spec.md`, `plan.md`, `questions.md`, `survivors.md`,
`phases/phase-3.md`, `phases/phase-4.md`.

Needs a fix: yes — findings 1 through 8. Finding 1 is the one that reopens the
defect this work item was filed against.
Loses a record or crashes: no
