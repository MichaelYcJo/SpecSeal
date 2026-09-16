# Round 3 — the verifying round that ends the run

Target confirmed: `6bc9b284` on
`feat/88-399-419-who-asks-the-routing-question-and-what-checks-the-answer`,
working tree clean. HEAD has not moved. The diff read is
`ca058695..6bc9b284`.

## What the round found, in one paragraph

Round 2's 🟡 1 is closed and its sweep reached past the three coordinates it
was aimed at, which is the answer this round was spawned for. The repair that
closed round 2's third ⬜ does what the fix pass reported — but only for the
wording it probed. One word over, the same defect the repair was written to
remove is still standing, and the guard's finder is still a literal spelling,
so the sentence it exists to refuse slips through when written the way this
repository's own `CLAUDE.md` writes it. Separately, the count the same pass
corrected from 28 to 29 is 22 at HEAD, and the correction blamed the exact
mechanism that produced the new wrong number.

## ① 🟡 1 is closed, and the sweep reached the class rather than the three lines

**Executed and read.** All three coordinates are corrected at `ef5c607d`:
`tests/test_waiver_decided_at_start.py:148` and `:885` no longer name the
framer as the party that asks, and
`tests/test_chain_hooks_hardening.py:1010-1014` no longer routes a `no` back to
a framer phase this branch deleted.

I ran my own sweep rather than trusting the pass's six patterns —
`framer` within eighty characters of `ask`/`question`/`multiSelect`/`checkbox`/
`routing batch`, and the reverse direction, over `tests/ agents/ skills/ docs/
templates/ hooks/ .github/ CLAUDE.md CONTRIBUTING.md`. Eleven hits, and every
one is correct:

- The kept hit is `tests/test_the_set_a_work_item_always_has.py:460`, and the
  pass's judgment of it holds. Its *asks for* means *demands* — "A table that
  hands it to the framer asks for a memo written before the work it is about"
  — and the act it names is authorship of `overview.md`, not putting a
  question to a person.
- `templates/sdd-routing.md:28` hands `spec.md`, `plan.md` and the questions
  file to the framer, and eight lines below it says **HOW TO ANSWER IT —
  nobody is asked**. Writing `questions.md` and asking a person are two acts,
  and this file already separates them.
- `skills/implement/orchestration.md:287` reads *It is YOUR question, whether
  or not a framer runs*, which is the reversal itself.

## ② The repair passes the wording it was built for, and refuses that same wording when `persona` sits beside it

**Executed**, on a throwaway clone at the target SHA, five one-paragraph edits
to `agents/smith.md` and the single case run after each.

The two directions the fix pass reported both reproduce. *Open every
coordinate a task names in one batch* passes at exit 0, and *Collect
everything a person has to answer in one batch* is refused at exit 1 naming
`['answer', 'person']`. The `task` defect the pass found and repaired is
genuinely gone.

The repair does not reach the rest of its own class. `ASKING` anchors a word
boundary at the START of each stem and none at the end, so two of its seven
members still match a longer word that is not them:

| Word in the window | Stem that fires | Is it about a person answering? |
|---|---|---|
| `persona` | `person` | no — it is a document's voice |
| `users` | `user` | usually no — this repository's *users* are the people who install the plugin |

Both are live rather than hypothetical. `agents/smith.md:127` already carries
*A two-file wording change to an agent's persona is over it at the first
file*, and `users` is ordinary in every definition.

**Measured, with padding so nothing but my own sentence is in the window**:
*A wording change to an agent's persona is over the rung. Open every
coordinate a task names in one batch.* is refused at exit 1. So is the same
sentence with *The cases a plugin's users already run stay green.* in front of
it. The message both times is *tells an agent to collect in one batch
something a person answers*, which is not what either sentence says.

The same probe showed the window's reach is not a paragraph. My first run of
the contract's own wording went red on `answer` drawn from
`agents/smith.md`'s closing *open issues with who must answer each*, a
different section entirely — the 140-character window is taken over the
flattened file, so it crosses headings. Counted over the whole glob, the share
of positions where a new *in one batch* would pass is 42 % in
`agents/framer.md`, 60 % in `agents/smith.md`, 71 % in `agents/warden.md`.
A definition following `agent-contract` §10 has a better than even chance of
landing in the other half.

This is the defect the case's own comment names — *a substring standing in for
a word* — one member of the class over from where it was repaired (§12).

## ③ And the sentence it exists to refuse still slips through, written the way this repository writes it

**Executed.** The repair moved the REFUSAL to a claim and left the FINDER on a
spelling: `flat_body.find("in one batch")` is a literal substring search, so a
sentence the check would refuse never reaches the window test if it is spelled
any other way.

Two spellings that get through, both probed at exit 0 against a definition
carrying them:

- `Questions a person genuinely has to answer go in **one batch** before the
  first edit.` — the emphasis markers sit inside the phrase, so the literal
  never matches. This is not an invented example. It is `CLAUDE.md:39`, this
  repository's own statement of the rule, copied verbatim.
- `Collect what a person has to answer as a single batch before the first
  edit.` — any synonym.

A guard whose finder is a spelling refuses what it happens to be looking at.
The case is green today because no `agents/*.md` contains the literal at all,
which is also why neither direction of this shows up in a run.

## ④ The count corrected to 29 is 22 at HEAD, and the correction named the mechanism that produced it

**Executed.** `survivor-check --range 6edfb71f..<sha>`, at each commit of the
branch:

| SHA | Reports |
|---|---|
| `5ca4077d` | 29 |
| `ca058695` — round 2's target | 29 |
| `ef5c607d` — the fix commit | 24 |
| `0b292ad0` | 22 |
| `6bc9b284` — HEAD | 22 |

`survivors.md:35` says *29 reports at HEAD* and the range row at `:48` says
*29 survivors at HEAD*. Both are 22. The tool prints the number itself:
`every survivor is excused by a row above (22)`, exit 0 with the work item's
own `--exempt` file.

29 was right for round 2's target and wrong the moment the fixes landed — the
three corrections removed five reports and the record commit removed two more.
The prose that carries the number explains the earlier 28 as *taken before the
last commit of the pass*, which is precisely what happened again to 29.

Nothing rests on it: the range row excuses all 22 either way, and
`evidence-check` is clean. That is why this is a correction rather than a
finding that needs a fix — but it is the third time a count in this work item
reached a record without being opened (§5), and the round-2 record carries it
as an answered ⬜.

## ⑤ The rewrap is right, and the 109-column line was right to leave

**Executed and read.** `agents/smith.md:58-63` now runs 61 to 77 columns,
matching the 75-78 of the paragraph around it, and the sentence is unchanged.

Leaving line 125 was the right call, and for a firmer reason than the fix pass
gave. Measured with `test_docs_line_wrap.py`'s own `prose_lines` and
`display_width`, `agents/smith.md`'s prose maximum is **109 at both
`ca058695` and HEAD** — the rewrap moved that line from 124 to 125 and changed
nothing else. The file is not in that module's `COVERED` list, so no check
moved either way, and bringing a line down that another work item's commit put
there is a sweep rather than this work item.

One thing that fell out of measuring it: the module's docstring lists
`agents/smith.md 148` as the current maximum. It is 109, and has been for
longer than this branch.

## ⑥ `New units: none` is true

**Executed.** `git diff ca058695..HEAD -U0` grepped for added and removed
`def ` and `class ` lines returns nothing in either direction. The fix pass
added `ASKING` and `WINDOW` as locals inside an existing case and rewrote that
case's body in place; no test function, no production unit, and no `.py` file
outside `tests/` is in the diff. `Contract changes: none` holds the same way —
`skills/agent-contract/SKILL.md` is not in the diff.

`tests/test_chain_hooks_hardening.py` is green: 48 passed, exit 0.

## What I did not run, and who answers it

The broad gate has not run. It is the sealer's one act, and `agent-contract`
§2 keeps it out of this round. Nothing in this report leaves it open, so it is
now due — what comes due is the sealer's spawn, and the answerer is the
orchestrator.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | 🟡 1 is closed, and the sweep reached the class rather than the three coordinates | `tests/test_waiver_decided_at_start.py:148`, `tests/test_waiver_decided_at_start.py:885`, `tests/test_chain_hooks_hardening.py:1010` | verified | Read all three corrections, then swept the class independently over eight trees and two root documents: eleven hits, every one correct. The kept hit is about authorship of `overview.md`, not about asking |
| 🟢 | The kept hit is correctly kept | `tests/test_the_set_a_work_item_always_has.py:460` | verified | Read: its *asks for* means *demands*, and the act is `overview.md`'s authorship. `templates/sdd-routing.md:36` says in as many words that nobody is asked |
| 🟡 2 | The repaired window still lets a substring stand in for a word: `\bperson` fires on `persona` and `\buser` on `users`, so a definition following `agent-contract` §10 goes red under a message about a question nobody asked | `tests/test_chain_hooks_hardening.py:844` | deferred #422 | Executed on a throwaway clone: *A wording change to an agent's persona is over the rung. Open every coordinate a task names in one batch.* is refused at exit 1 naming `['person']`, and the same sentence behind *a plugin's users* is refused naming `['user']`. `agents/smith.md:127` already carries `persona`. The contract's own wording passes only when padded, because the 140-character window is taken over the flattened file and crosses headings — 42 % of `agents/framer.md` and 40 % of `agents/smith.md` are positions where it would fire |
| 🟡 3 | The refusal decides by the claim but the FINDER is still a literal substring, so the instruction the case exists to refuse passes when spelled with emphasis inside the phrase or with a synonym | `tests/test_chain_hooks_hardening.py:848` | deferred #422 | Executed, both at exit 0: *Questions a person genuinely has to answer go in `**one batch**` before the first edit* — which is `CLAUDE.md:39` verbatim — and *…as a single batch…*. `find("in one batch")` never sees either, so the window test is never reached |
| ⬜ | The count corrected from 28 to 29 is 22 at HEAD, by the mechanism the correction blamed | `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/survivors.md:35`, `:48` | correction — the closing commit | Executed: `survivor-check --range 6edfb71f..<sha>` gives 29 at `ca058695`, 24 at `ef5c607d`, 22 at `0b292ad0` and at HEAD. The tool prints `every survivor is excused by a row above (22)` at exit 0. Nothing rests on the number, and the range row excuses all 22 either way |
| ⬜ | Round 2's record carries the count as an answered ⬜, and it was not | `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/rounds/round-2.md` | correction — the closing commit | The same measurement. The row should say the number was corrected in the wrong direction rather than that it was answered |
| ⬜ | `test_docs_line_wrap.py`'s docstring lists `agents/smith.md` at 148 columns; measured with the module's own `prose_lines` and `display_width` it is 109, and was 109 before this branch | `tests/test_docs_line_wrap.py:19` | deferred #422 | Executed at `ca058695` and at HEAD: 109 both times, at line 124 then 125. Out of this diff and older than this branch, so it is routed rather than corrected here |
| 🟢 | The rewrapped paragraph is right, and the 109-column line was right to leave | `agents/smith.md:58`, `agents/smith.md:125` | verified | Executed: the rewrapped lines run 61-77 columns against a 75-78 paragraph, the sentence is unchanged, and `agents/smith.md` is not in `test_docs_line_wrap.py`'s `COVERED` list. The file's maximum did not move |
| 🟢 | `New units: none` and `Contract changes: none` are both true | `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/rounds/round-2.md` | verified | Executed: `git diff ca058695..HEAD -U0` grepped for added and removed `def ` and `class ` returns nothing either way, and `skills/agent-contract/SKILL.md` is not in the diff |
| 🟢 | The two `seal/ledger.md` rows citing `agents/smith.md#"## Phases"` state claims the section still carries | `seal/ledger.md:736`, `seal/ledger.md:987` | verified | Read the section rather than the hashes: `agents/smith.md:208` carries *Mutation-test every unit you added, one at a time* for L5, and `:123` and `:126` carry *hands over a fix table under `## Fixes`* and *writes no `phases/phase-N.md`* for R8. A third row in the work item's own fragment cites the same anchor and was updated with them |
| 🟢 | Every anchor in the tree resolves at HEAD | `seal/ledger.md`, `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md` | verified | Executed: `evidence-check .` at exit 0 — 1271 ok, 0 drifted, 0 broken |
| 🟢 | Round 2's record may tick `Pass` while its `Needs a fix` reads `yes` | `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/rounds/round-2.md:18` | verified | Read `docs/review-chain-spec.md:1097` — *a `fixed` cell — whatever its `Needs a fix` says*. The two rows answer different questions |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -q` in a throwaway clone at `6bc9b284` | 48 passed, exit 0 |
| `bin/evidence-check .` in the same clone | exit 0 — 1271 ok, 0 drifted, 0 broken, 0 external |
| `bin/survivor-check --range 6edfb71f..HEAD --exempt <the work item>/survivors.md` | exit 0, `every survivor is excused by a row above (22)` |
| The same, at `5ca4077d`, `ca058695`, `ef5c607d`, `0b292ad0` | 29, 29, 24, 22 |
| Five one-paragraph edits to `agents/smith.md`, each run through `test_the_questions_are_collected_before_the_work_not_during_it` | *…a task names in one batch* refused (exit 1) unpadded, passed (exit 0) padded; *…a person has to answer in one batch* refused naming `['answer', 'person']`; *…persona… in one batch* refused naming `['person']`; *…users… in one batch* refused naming `['user']` |
| The same case against `in **one batch**` and *as a single batch* | exit 0 both — neither reaches the window test |
| `agents/smith.md` prose maximum at `ca058695` and at HEAD, using `test_docs_line_wrap.py`'s `prose_lines` and `display_width` | 109 columns both times, line 124 then line 125 |
| Share of flattened positions in each `agents/*.md` where a new *in one batch* would pass the window | framer 42 %, scribe 76 %, sealer 92 %, smith 60 %, warden 71 % |
| The repository's broad gate — full suite, repository-wide lint, typecheck | not yet. It is the sealer's one act and `agent-contract` §2 keeps it out of this round; this report is what makes it due |

All probe files and the throwaway clone were deleted before this report was
written; the working tree is clean and no worktree was created.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The window still lets a substring stand in for a word (`persona`, `users`), and it is taken over the flattened file so it crosses headings | a new issue the orchestrator opens — the run is capped, so this is a candidate rather than a fix to commission | the repository owner, at the issue |
| The finder is a literal spelling, so `in **one batch**` and any synonym never reach the claim test | the same issue — it is the other half of one class | the repository owner, at the issue |
| `test_docs_line_wrap.py`'s docstring lists `agents/smith.md` at 148 columns; it is 109 | a new issue, or the same one as a second row | the repository owner, at the issue |
| A sweep over `agents/*.md` for every tool an agent cannot reach | already deferred by `overview.md` §*Not done* as the ticket round 2 named | the repository owner, at the ticket |
| The `Checked` column records no re-read, so `--reverify` cannot report the half that was skipped | already deferred by `overview.md` §*Not done*, and #120 round 1 | the repository owner |
| A durable record that a person chose `no work item` | already deferred by `overview.md` §*Not done* | the repository owner |
| Promoting the approval-line notice to a refusal | already deferred by `overview.md` §*Not done* | the repository owner |

## Paste-ready fixes

🟡 2 — anchor both ends of every stem and drop `user`, whose plural is this
repository's ordinary word for the people who install the plugin. Replace the
`ASKING` definition in
`tests/test_chain_hooks_hardening.py`:

```python
    # Anchored at BOTH ends, and the stems spelled out. A leading-only
    # boundary is the same defect one word over: `person` fires on `persona`,
    # which `agents/smith.md` uses for a document's voice, and `user` on
    # `users`, which is this repository's word for whoever installs the
    # plugin. Neither is a person answering anything.
    ASKING = re.compile(
        r"\b(questions?|asks?|asked|asking|answers?|answered|"
        r"persons?|people|humans?)\b",
        re.IGNORECASE,
    )
```

🟡 3 — normalise the emphasis markers out before searching, and look for the
synonyms too. Replace the body of the per-file loop:

```python
    PHRASE = re.compile(r"\bin (?:one|a single|a) batch\b", re.IGNORECASE)
    for path in definitions:
        with open(path, encoding="utf-8") as f:
            flat_body = " ".join(f.read().split())
        # The markers come out before the search, because markdown emphasis
        # inside the phrase breaks a literal one: `CLAUDE.md` states this very
        # rule as `go in **one batch** before the first edit`, and a search for
        # the plain string never sees it. Removing them keeps one string, so
        # the window below is still taken over what the reader reads.
        flat_body = flat_body.replace("**", "").replace("*", "")
        relative = os.path.relpath(path, ROOT)
        for hit in PHRASE.finditer(flat_body):
            at = hit.start()
            window = flat_body[max(0, at - WINDOW) : hit.end() + WINDOW]
            named = sorted({m.group(0).lower() for m in ASKING.finditer(window)})
            assert not named, (
                f"{relative} tells an agent to collect in one batch something "
                f"a person answers — the window names {named}. No agent this "
                "plugin spawns has `AskUserQuestion`, so collecting a batch "
                "of questions is an instruction nothing can carry out; the "
                "act belongs to the session that spawns the work. Batching "
                "READS is a different thing and is what `agent-contract` §10 "
                f"asks for — that wording is not refused here.\n  …{window}…"
            )
```

⬜ — the two survivors corrections, for the closing commit. In
`survivors.md`, the prose:

```
22 reports at HEAD, all correct as reports and none a defect. The number was
written as 28, then corrected to 29, and both were taken before the commits
that changed them — 29 was the count at round 2's target `ca058695`, and the
three corrections at `ef5c607d` plus the record commit at `0b292ad0` took it
to 22. `survivor-check` prints the number itself. The range row excuses all of
them at every one of those counts, which is why nothing turns on it and why it
is corrected rather than re-taken each time.
```

and the range row's opening clause:

```
| `6edfb71f..HEAD` | 22 survivors at HEAD. The fix pass deleted
```

⬜ — the round-2 record's answer on that ⬜, for the same commit:

```
| ⬜ | The survivor count | `seal/specs/…/survivors.md:35` | corrected in the wrong direction | 28 was replaced by 29, which was the count at this round's target and not at HEAD. Round 3 measured 22 |
```

## Proof block

Files opened, all read at `6bc9b284` unless a SHA is named:

- `agents/smith.md` — the rewrap at 58-63, the long line at 125, the `## Phases` section at 114-212, the closing `## Report`
- `tests/test_chain_hooks_hardening.py` — the changed case and its docstring change
- `tests/test_waiver_decided_at_start.py` — the three corrected lines, via the diff
- `tests/test_docs_line_wrap.py` — the docstring, `COVERED`, `prose_lines`, `display_width`, `LIMIT`
- `tests/test_the_set_a_work_item_always_has.py:450-470` — the kept sweep hit
- `templates/sdd-routing.md:18-38` — the `Planning` row and its comment
- `seal/ledger.md:733-740`, `:985-990` — the two rows citing the `## Phases` anchor
- `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md` — the diff, all four changed and added rows
- `seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/` — `overview.md`, `changelog.md`, `survivors.md`, `rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-2-fixes.md`, all via the diff
- `skills/code-review/scripts/survivor_check.py` — the exemption reader, lines 106-151 and 725-860
- `skills/code-review/scripts/chain_check.py`, `skills/code-review/scripts/round_record.py` — grepped for the `Needs a fix` readers
- `docs/review-chain-spec.md:1092-1113` — `Pass` against `Needs a fix`
- `CLAUDE.md:39`, `skills/implement/SKILL.md:184`, `skills/implement/orchestration.md:177` — how the tree spells the phrase
- `skills/writing-style/SKILL.md` (user-level) — read before writing this report
- `bin/test`, `bin/evidence-check`, `bin/survivor-check` — the runners

Needs a fix: no — 🟡 2 and 🟡 3 are real and are one class, but the run is capped and both are routed to an issue rather than commissioned; the three ⬜ corrections are paperwork under seal/ for the closing commit.
Loses a record or crashes: no


