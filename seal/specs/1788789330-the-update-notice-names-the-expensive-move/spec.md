# Feature Specification: the update notice names the expensive move

<!-- seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` result 3 and run 6 | the only measured fact about `/reload-plugins` — a preloaded skill body handed to a **spawned agent** refreshes at a reload. It is the whole of the positive evidence, and it is narrower than the ticket's summary of it |
| the same file, §*What it did not establish* | the experiment names its own gap, and that gap is not hooks or agent definitions. Silence there is not a claim either way |
| `CLAUDE.md` §*The goal a design is chosen against* | between two texts that carry the same fact, the one that does not send a reader to ask a person is the cheaper. Stating what is unmeasured is what stops the reader asking |
| `skills/verify/SKILL.md` via `agent-contract` §4 | executed, read, unverified are separate labels. A sentence that reads as measured when nothing measured it is the counterfeit this repository names |

## Scope

**In.** Every place this repository tells a user what to do after an update
lands names `/reload-plugins`, says what a reload was measured to do, and says
what nobody has measured about it. Six sentences in `skills/update/SKILL.md`,
two in `hooks/version-check.py`, three in each README, and the case that pins
the notice's wording.

**Out.**

- **Running the reload for the user.** The ticket's *Not this*. A
  `SessionStart` hook writes to a session and cannot type into one, and a
  built-in CLI command is not a skill an agent can invoke.
- **Measuring the unmeasured half.** Settling it needs a `/reload-plugins`
  typed by a person and an agent spawned after it, and neither is an act this
  segment can perform. What the work does instead is state the gap and name
  the run that would close it.
- **The review chain's own use of the word `restart`.** Twenty-three of the
  thirty-eight hits are a walk over review records restarting at a floor
  record. Same word, unrelated subject.

## The class, enumerated by construction

The class is **every place this repository tells a user what to do after an
update lands**. It was enumerated with two greps over the whole tree rather
than from the ticket's list, which was three lines short and omitted the
Korean README entirely.

**Measured over tracked files at `86e140f`, the commit this branch was cut
from**, which is the tree the class has to be enumerated against — the branch's
own commits add hits of their own, and counting those makes the enumeration a
measure of the fix rather than of the defect.

```
git grep -ciI 'restart' 86e140f                        # 33 lines
git grep -cI  '재시작'   86e140f                        #  3 lines
git grep -niI 'reload'  86e140f | grep -vi preload     #  2 lines
```

Deduplicated (`docs/flow.md:74` carries both `restart` and `reload`):
**37 distinct lines**, reconciling as 15 in class and 22 out against the rows
below. A second pass over `plugin update` and `/specseal:update` added two
candidates and no new members.

<!-- Round 1, finding 4. This block first read 33 · 3 · 3 → 38, from `grep -r`
     over the WORKING TREE partway through the branch. The third `reload` hit
     was this work item's own `routing.md:18`, committed at `389ad12` — so the
     count included a line the branch had just written. The reviewer's proposed
     cause, an untracked `.venv`, is not it: `grep -rnI 'reload' .venv` returns
     0. Both numbers were right for their own tree, and neither said which tree
     it measured, which is the whole of the defect. -->

**Every count here is of a line, and a line is not a coordinate.** Two rows
below name a range or a group; their line counts are stated so the table
reconciles to 37, and the rows themselves are what carry the judgment.

| # | Coordinate | What it says | In the class? |
|---|---|---|---|
| 1 | `hooks/version-check.py:151` | `"Either way, restart to load it."` | **yes** — the notice's closing line, the ticket's headline |
| 2 | `hooks/version-check.py:18` | `keeps what it loaded until a restart.` | **yes** — describes the session rather than instructing anyone, but it is the same claim one level up and the measurement makes it too strong. Narrowed, not deleted |
| 3 | `skills/update/SKILL.md:11` | *"which is a number, not a reason to restart"* | **yes** |
| 4 | `skills/update/SKILL.md:32` | *"There is nothing to restart for."* | **yes** |
| 5 | `skills/update/SKILL.md:79` | step 5's heading | **yes** |
| 6 | `skills/update/SKILL.md:83` | *"not loaded until Claude Code restarts"* | **yes** |
| 7 | `skills/update/SKILL.md:87` | *"It does not restart anything."* | **yes** — a scope statement that has to cover the reload too, or naming the reload reads as offering to run it |
| 8 | `skills/update/SKILL.md:111` | the user-facing output template | **yes** — the cheap move goes first here |
| 9 | `README.md:266` | the `/specseal:update` command-table row | **yes** |
| 10 | `README.md:311` | *"Restart to load it; the session you are in…"* | **yes** |
| 11 | `README.md:318` | `# then restart` in the by-hand block | **yes** |
| 12 | `README.ko.md:257` | the command-table row (`적용은 재시작 후`) | **yes** — the mirror of 9; the ticket names none of the three |
| 13 | `README.ko.md:302` | `적용은 재시작 후이고` | **yes** — the mirror of 10 |
| 14 | `README.ko.md:309` | `# 그다음 재시작` | **yes** — the mirror of 11 |
| 15 | `tests/test_version_check.py:69` | `assert "restart" in msg.lower()` | **yes** — the word is pinned, so the case moves with the text |
| 16 | `README.md:439` | *"The hooks need no restart: the next command reads the folder where it is."* | no — about `seal mode`, a different act, and it already names the cheap move for that act |
| 17 | `README.md:182` · `README.ko.md:178` | the version-check row of the hooks table | no — describes what the hook asks and prints, not what a user does with the release |
| 18 | `docs/flow.md:74` | the tracker row for #134 | no — the tracker describing this ticket. Its checkbox is ticked, its text is not rewritten |
| 19 | `docs/experiments/2026-09-03-…md` result 3 and the results table · `.ko.md:32` | the evidence this work cites | no — and **not among the 37 either**: every one of those lines says *preloaded*, so the pattern's own `grep -vi preload` removes them. Listed because it is the document a reader will expect to see judged, and rewriting it would be editing the measurement to match the claim |
| 20 | `CHANGELOG.md:274, 893` · `docs/review-chain-spec.md:858, 906` · `seal/ledger.md:985, 1417` · `skills/code-review/scripts/chain_check.py:218, 591, 2515` · `round_record.py:1068` · `tests/test_the_record_is_generated.py:1971` · `tests/test_the_reopening_is_one.py:6` | the bound walk *restarting* at a floor record | no — same word, unrelated subject. **Twelve lines**, which is the count of the coordinates listed |
| 21 | `tests/test_one_word_one_meaning.py:36` | *"A round does not restart it"* | no — about when a work item starts |
| 22 | six lines under `seal/specs/1788354065-…/spec.md`, `1788597030-…/changelog.md` and `plan.md`, `1788761915-…/changelog.md`, `overview.md` and `phases/phase-5.md` | past work items' records | no — a record asserts a past state and is never rewritten |
| 23 | `seal/specs/1788445862-…/overview.md:61` | an unverified row naming a reload | no — an open row of another work item, whose answerer is already named there |

**15 in the class, 22 out** — 1 + 1 + 12 + 1 + 6 + 1 across rows 16, 18, 20,
21, 22 and 23, which is 22 and reconciles to the 37 above. Rows 17 and 19 are
candidates that carry none of the three words at `86e140f` and so are not
members of the count; they are in the table because a reader looking for them
would otherwise read their absence as a miss.

<!-- Round 1, finding 4. Row 20 read *Thirteen lines* and listed twelve
     coordinates; row 22 named the three work items as `17885…`, `17886…`,
     `17887…` and no item begins `17886` — they are `1788354065`,
     `1788597030` and `1788761915`. A row 24 for this work item's own
     `routing.md:18` is gone with the count that included it. -->

Rows 16 through 23 are here because the table is what shows the decision was
made rather than the hit missed.

## What is measured, and exactly how far it reaches

This is the substance of the change, so it is spelled once here and every
edited sentence is held to it.

| Claim | Label | Evidence |
|---|---|---|
| A preloaded skill body handed to a **spawned agent** is re-read at `/reload-plugins` | **executed** | run 6 of the experiment: sentinel in the version cache, reload, spawn → PRESENT. Run 5 (right file, no reload) → ABSENT |
| The copy that loads is `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` | **executed** | result 2; runs 1–4 edited the marketplace clone and nothing read them |
| A reload also refreshes **hooks** | **unverified** | the experiment measured nothing about hooks. Its own *What it did not establish* names a different gap, so its silence is not a claim either way |
| A reload also refreshes **agent definitions** | **unverified** | the same. `agents/*.md` is a different artifact from a `skills:` body, and no run touched one |
| A reload moves a **running session onto a newly installed version** | **unverified** | run 6's sentinel sat in the *running* version's own directory, so it shows a re-read of the copy in force and nothing about a new one. `hooks/version-check.py:18` states the opposite for the no-reload case |
| A restart loads the new version's skills, hooks and agent definitions | **read** | the pre-existing claim of `version-check.py:18` and both READMEs, unchanged by this work |

The honest discharge of the ticket's second *Done when* is therefore three
sentences and not one: name what a reload was measured to do, name what nobody
measured, and name the run that would settle it. Asserting that a reload is
enough would be labelling an inference as measured, which is the one thing the
handoff forbids outright.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given a session in an opted-in repository behind the newest tag, when the notice prints, then it names `/reload-plugins` before it names a restart | `tests/test_version_check.py::test_the_warning_names_the_cheap_move_before_the_expensive_one` |
| S2 | Given that notice, when a reader looks for the reload's reach, then the text says what was measured and that hooks and agent definitions were not | the same case: `measured` present, `hooks` and `agent definitions` both named |
| S3 | Given the same notice, when the old assertion runs, then `restart` is still in it — the reload is added beside the restart, never in place of it | `test_the_warning_names_both_commands_in_order`, unchanged |
| S4 | Given `skills/update/SKILL.md`, when a user reaches step 5, then the step names both moves, says which was measured for what, and names the run that would settle the rest | read: step 5 and §*What this does not do* |
| S5 | Given the skill's output template, when the model fills it in, then the cheap move is printed first and the restart is what covers the unmeasured half | read: the fenced block at the end of the skill |
| S6 | Given either README, when a reader follows *Updating*, then it names the reload with the same three sentences, in English and in Korean | read, both editions; `tests/test_docs_line_wrap.py` on the pair |
| S7 | Given the skill's *It does not restart anything*, when a user asks whether the command will reload for them, then the text answers no for both moves | read: §*What this does not do* |

## Data & interfaces

No schema, no interface. One string literal in `notice()`
(`hooks/version-check.py#notice`), one module docstring, and prose.

## Open questions → questions.md

None. `routing.md` records that the batch was answered before the first edit
and that this item raised nothing needing a person; the one judgment call —
how far to state the unmeasured half — is settled by the handoff's own
instruction and recorded in the table above rather than asked.
