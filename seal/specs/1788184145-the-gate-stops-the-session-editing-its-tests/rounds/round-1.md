# 1788184145-the-gate-stops-the-session-editing-its-tests — review round 1

| Field | Value |
|---|---|
| Target SHA | `4a48eee67ec75a27a972d54f9816cfe41e15ff17` |
| PR | not open yet — it lands on `release/v0.0.2` after the rounds settle |
| Broad gate | not yet |
| Fixes checked by | round-2 |

<!-- The row was added later, by
`specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody`. Round 2 read
the fixes at `8b6c6ff` and opened seven findings inside them, which is what
this row records. Nothing else about this record changed. -->

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The prose diagnoses the wrong mechanism. It says the fixtures trip the gate *because they are shell command strings*; what the reader counts is a body segment whose command word is `git` with the `commit` subcommand. A whole fixture file delivered as a body is clean, and the documents' own waiver examples are not clean | `agents/smith.md:91-95` · `agents/warden.md:156-158` · `CHANGELOG.md:13-16` · `plan.md:23-25` · `overview.md:14` | **fixed** `8b6c6ff` | Re-ran `verify_round1_finding.py` independently rather than adopting either account, and both halves reproduce: issue #34's partial-patch body TRIPS, whole fixture files are clean, `agents/smith.md` and `README.md` trip only at their own waiver examples. All five coordinates now state the command-word rule and name both kinds of edit that produce such a segment. The reviewer's conclusion is **not** written anywhere: it would have put a false sentence in a shipped agent file |
| 🟡 2 | A shipped agent file asserts a fact about this repository. `This repository's are, the gate's own tests are where they cluster` reads, inside a consuming repository, as a claim about that repository — which is false there | `agents/smith.md:93` · `agents/warden.md:157` | **fixed** `8b6c6ff` | Both sentences are gone. The replacement prose states the rule as a property of any repository whose documents or tests carry commit commands as text, and names no repository at all. Pinned by `test_neither_agent_file_claims_a_fact_about_the_reader_repository`, which refuses all three spellings |
| 🟡 3 | Nothing pins the new prose. `grep -rn "nothing to read\|two reasons that point\|Edit files with the" tests/` returns 0; deleting both new paragraphs leaves the suite green | `agents/smith.md:83` · `agents/warden.md:145` | **fixed** `8b6c6ff` | `tests/test_edits_go_through_the_edit_tool.py` planted, five cases, each asserting the pinned phrasing AND the absence of the loose one per `test_one_word_one_meaning.py:6`. Every case was shown to go red under a mutation before any was called passing; one mutation was a silent no-op on the first attempt because the needle wrapped across a line, which is the same defect this work item is about |
| 🟡 4 | `plan.md` phase 3's Status names one commit for four deliverables, and `questions.md` arrived two commits earlier | `plan.md:64` | **fixed** `8b6c6ff` | `questions.md` moved out of phase 3's Delivers — it was written with the rest of the SDD set before implementing, so it never belonged to that phase — and its commit `13ab33a` is named beside `f805088`. A phase 4 row was added for this round, since round 1's fixes are work the plan did not contain |
| 🟡 5 | `What the prompt costs from there is what the probe table below records` points at the wrong place. The table records probe SHAPES; the cost is the bullet above it — *#36 is what that cost: two prompts inside five minutes* | `agents/warden.md:158` | **fixed** `8b6c6ff` | Now reads *what that costs is what the next bullet measures*, which is the `#36` bullet. Confirmed the bullet order did not change: the probe bullet still immediately follows |
| 🟢 6 | The ledger row's claim is correct, and can be upgraded from `Read, not run` to executed | `.specseal/map.md:50` | **fixed** | Row upgraded to **Executed**, and two rows added to `.specseal/map.md` for what this round measured: the command-word rule with the probe results that establish it, and the fact that prose carrying an odd number of apostrophes flips the reader's quote state for the rest of a document. Stamped `f1cd65d`, an ancestor of the base |
| 🟢 7 | `agents/smith.md` was extended at the existing coordinate rather than duplicating reason 1; `agents/warden.md` places the statement where a warden reaching for a probe meets it first; the SDD set has the shapes it owes, including `## Not verified` in the machine-read form | `agents/smith.md:79-96` · `agents/warden.md:145-160` · `overview.md:28` | answered | Read. Reason 1's restatement in `agents/warden.md` is not a restatement for its reader: the warden does not load the `implement` skill, so it is the only statement it gets |
| 🟢 8 | Line width, ledger stamp and release hygiene hold | — | answered | Executed: 179 passed across the ten prose and hygiene files. New lines measure 76-77 display columns against a limit of 88. `f1cd65d` is an ancestor of the base and is not a commit this branch made |

## Executed probes

| What was run | Result |
|---|---|
| `verify_round1_finding.py` — issue #34's exact eight-line reproduction body through `_hides_a_commit` | **TRIPS.** The ticket's premise holds: patching a fixture file by heredoc does stop the session |
| the same, whole fixture files as the body | `tests/test_gate_judges_the_repo_it_commits_to.py` clean · `tests/test_what_the_reader_understands.py` clean |
| the same, whole documents as the body | `agents/smith.md` TRIPS at line 43 · `README.md` TRIPS at lines 160, 238, 239 — every one a waiver example |
| the same, three hand-built partial patch bodies with balanced quotes | all clean — so it is not "any fragment", it is a fragment whose quoting leaves `git commit` in command position |
| `git log --oneline --diff-filter=A -- …/questions.md` | `13ab33a` |
| `grep -rn "nothing to read\|two reasons that point\|Edit files with the" tests/` | 0 lines |
| ten prose and hygiene test files | 179 passed |
| `evidence_check.py` · `unverified_check.py` | 5 ok · 0 drifted · 0 broken · 0 external · 2 open |

## Inherited coordinates

Round 1 inherits nothing. What this round establishes, for round 2:

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| finding 1 | `hooks/commit-review-gate.py:144-147` | The segment scan — a segment counts only when its command word is `git`. This is the rule the prose has to state, and `:151` alone does not reach it |
| finding 1 | `hooks/commit-review-gate.py:262-286` | `commit_invocations`, where the judgment is actually assembled |
| finding 1 | `agents/smith.md:43` · `README.md:160` | The lines that actually trip a whole-document patch, both waiver examples |
| finding 1 | issue #34's eight-line body, reproduced in `scratchpad/verify_round1_finding.py` | The measured case the corrected prose must stay true to |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the gate should skip a heredoc body being written to a file (issue #34's second checkbox) | `questions.md` Q1 — out of scope for this work item, and round 1 did not judge it | the repository owner |
| The command string that actually triggered issue #34 in the original session, which would close whether that incident was a fixture patch or a document patch | this round record, and the memo's `## Not verified` | the session that opened issue #34 / the repository owner |
