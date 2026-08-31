# 1788184145-the-gate-stops-the-session-editing-its-tests — review round 1

| Field | Value |
|---|---|
| Target SHA | `4a48eee67ec75a27a972d54f9816cfe41e15ff17` |
| PR | not open yet — it lands on `release/v0.0.2` after the rounds settle |
| Broad gate | not yet |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The prose diagnoses the wrong mechanism. It says the fixtures trip the gate *because they are shell command strings*; what the reader counts is a body segment whose command word is `git` with the `commit` subcommand. A whole fixture file delivered as a body is clean, and the documents' own waiver examples are not clean | `agents/smith.md:91-95` · `agents/warden.md:156-158` · `CHANGELOG.md:13-16` · `plan.md:23-25` · `overview.md:14` | open | Executed by the orchestrator, `scratchpad/verify_round1_finding.py`. The round-1 reviewer raised this as 🔴 with the conclusion *"the test fixtures are not what trips it, the documents are"*, and **that conclusion is refuted**: the eight-line body issue #34 delta-debugged to — a PARTIAL patch of a fixture file — TRIPS. The reviewer delivered whole files, which is not what an edit is. Both halves are true at once and the prose has to carry the rule rather than either example |
| 🟡 2 | A shipped agent file asserts a fact about this repository. `This repository's are, the gate's own tests are where they cluster` reads, inside a consuming repository, as a claim about that repository — which is false there | `agents/smith.md:93` · `agents/warden.md:157` | open | Read. It contradicts the divergence the memo already recorded, whose grounds are that these files are read where `hooks/commit-review-gate.py` does not exist (`overview.md:23`). The same reasoning refuses the sentence that replaced the coordinate |
| 🟡 3 | Nothing pins the new prose. `grep -rn "nothing to read\|two reasons that point\|Edit files with the" tests/` returns 0; deleting both new paragraphs leaves the suite green | `agents/smith.md:83` · `agents/warden.md:145` | open | Executed. `tests/test_one_word_one_meaning.py:6` states the repository's own norm — *asserting the pinned phrasing AND the absence of the loose one* — and this change sits outside it |
| 🟡 4 | `plan.md` phase 3's Status names one commit for four deliverables, and `questions.md` arrived two commits earlier | `plan.md:64` | open | Executed: `git log --diff-filter=A -- …/questions.md` returns `13ab33a`, which precedes `a15ef3b`. The Status column holds the commit that closed the phase, and one of the four was already there |
| 🟡 5 | `What the prompt costs from there is what the probe table below records` points at the wrong place. The table records probe SHAPES; the cost is the bullet above it — *#36 is what that cost: two prompts inside five minutes* | `agents/warden.md:158` | open | Read, then confirmed against `agents/warden.md:164-165` |
| 🟢 6 | The ledger row's claim is correct, and can be upgraded from `Read, not run` to executed | `.specseal/map.md:50` | fixed by round 2 | Executed twice, independently: a body carrying `git commit` on its own line returns True under both `cat > f <<'EOF'` and `python3 - <<'PY'`, and False for a body carrying none |
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
