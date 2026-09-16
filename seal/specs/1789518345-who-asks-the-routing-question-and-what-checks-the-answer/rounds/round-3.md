# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — review round 3

| Field | Value |
|---|---|
| Target SHA | 6bc9b284 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 421 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — 🟡 2 and 🟡 3 are real and are one class, but the run is capped and both are routed to an issue rather than commissioned; the three ⬜ corrections are paperwork under seal/ for the closing commit. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of the run. Round 1 met the floor and round 2 — a verifying
round that opened one finding — closed on a fix, so the one reopening is spent
and this record ends the run whatever it finds
(`docs/review-chain-spec.md` §*The reopening — one, and then the run is
capped*).

Its target is the diff of round 2's fixes, `ca058695..6bc9b284`, and its job is
the answers: is round 2's one verdict actually closed, and are its three ⬜
corrections true. Round 2's record names no new units, and verifying that claim
was part of the round rather than taken from it.

Three claims the fix pass made about its own work were checked by running them:
that the rewritten guard decides by the claim rather than by a spelling, that
leaving one over-long line was right, and that the two ledger rows citing the
rewrapped section state claims the section still carries.

The round was also asked to route rather than only to report, since no round
follows it.

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

## Paste-ready fixes

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
```
22 reports at HEAD, all correct as reports and none a defect. The number was
written as 28, then corrected to 29, and both were taken before the commits
that changed them — 29 was the count at round 2's target `ca058695`, and the
three corrections at `ef5c607d` plus the record commit at `0b292ad0` took it
to 22. `survivor-check` prints the number itself. The range row excuses all of
them at every one of those counts, which is why nothing turns on it and why it
is corrected rather than re-taken each time.
```
```
| `6edfb71f..HEAD` | 22 survivors at HEAD. The fix pass deleted
```
```
| ⬜ | The survivor count | `seal/specs/…/survivors.md:35` | corrected in the wrong direction | 28 was replaced by 29, which was the count at this round's target and not at HEAD. Round 3 measured 22 |
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:3843` | round 1's 🟡 1 — fixed |
| round-1 | `agents/smith.md:113`, `tests/test_a_moved_rule_leaves_its_definition.py:266` | round 1's 🟡 2 — fixed |
| round-1 | `templates/claude-md-block.md:16`, `tests/test_waiver_decided_at_start.py:841` | round 1's 🟡 3 — fixed |
| round-1 | `agents/framer.md:228`, `skills/implement/orchestration.md:286` | round 1's 🟡 4 — fixed |
| round-1 | `seal/ledger.md`, `skills/evidence-check/scripts/evidence_check.py:1577` | round 1's 🟡 5 — fixed |
| round-1 | `tests/test_chain_check_at_the_pull_request.py:658` | round 1's ⬜ — correction |
| round-1 | `spec.md:392`, `plan.md:183` | round 1's ⬜ — correction |
| round-1 | `skills/code-review/scripts/chain_check.py:3270` | round 1's 🟢 — verified |
| round-1 | `hooks/routing.py:164` | round 1's 🟢 — verified |
| round-1 | `templates/claude-md-block.md`, `CLAUDE.md` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/chain_check.py:696` | round 1's 🟢 — verified |
| round-1 | `tests/test_waiver_decided_at_start.py:147`, `:696`, `:815`, `tests/test_chain_hooks_hardening.py:789`, `:969` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/chain_check.py:1638` | round 1's 🟢 — verified |
| round-1 | — | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_waiver_decided_at_start.py:148`, `tests/test_waiver_decided_at_start.py:885`, `tests/test_chain_hooks_hardening.py:967` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:3825`, `hooks/routing.py:51` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/chain_check.py:1135` | round 2's 🟢 — verified |
| round-2 | `tests/test_a_moved_rule_leaves_its_definition.py:278` | round 2's 🟢 — verified |
| round-2 | `tests/test_waiver_decided_at_start.py:905`, `tests/test_review_axes.py:130` | round 2's 🟢 — verified |
| round-2 | `agents/framer.md:209`, `skills/implement/orchestration.md:287`, `skills/implement/SKILL.md:399` | round 2's 🟢 — verified |
| round-2 | `tests/test_waiver_decided_at_start.py:619` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md`, `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md` | round 2's 🟢 — verified |
| round-2 | `rounds/round-1.md:46`, `rounds/round-1-report.md:194`, `:259` | round 2's 🟢 — verified |
| round-2 | `skills/implement/orchestration.md:316`, `hooks/commit-review-gate.py:892` | round 2's 🟢 — verified |
| round-2 | `survivors.md:20` | round 2's ⬜ — correction |
| round-2 | `agents/smith.md:61` | round 2's ⬜ — correction |
| round-2 | `tests/test_chain_hooks_hardening.py:814` | round 2's ⬜ — correction |

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
