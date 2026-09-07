# 1788817289-local-mode-from-first-setup-to-the-gate — overview

📋 implement applied
· spec:     `docs/flow.md` §0.9.1 · `docs/one-root-by-lifetime.md` §*The opt-in signal is the root itself* · `CONTRIBUTING.md` §*What a change to a gate must carry* and §*House rules* · `CLAUDE.md` §*The goal a design is chosen against* and §*Repo rule — a change writes fragments* · `skills/agent-contract/SKILL.md` §§1–16 · `skills/implement/SKILL.md` §§1–4 and §*Bootstrap* · `templates/config.md` · `seal/follow-up.md`
· evidence: 6 rows in `seal/ledger/1788817289-local-mode-from-first-setup-to-the-gate.md`, 27 coordinates, all `ok`
· verified: executed — 4 modules of new cases and 12 neighbouring modules (counts in *Not verified*); 19 mutations across 3 phases. read — the two tickets, the four scripts the coordinates named, `hooks/cmdline.py`'s exports. unverified — the full suite, the repository-wide lint, the typecheck, and every platform but macOS

## Why this work exists

A repository that reaches local mode meets a review chain whose record tool
refuses the root it was told to create and a check that reports its routing
declaration missing on every round — and the repository that reaches shared
mode may never have been asked which one it wanted.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the mode question is asked | `plan.md`'s Phases table says the gate fires on a commit, and `spec.md` §*Data & interfaces* says it reuses `hooks/cmdline.py` for target resolution | any Bash call, judging the session's own repository, with no command-line reading at all | `hooks/cmdline.py` does not export `commit_invocations` or `commit_targets` — they live in `commit-review-gate.py`, and both ways of reaching them are refused by this repository's own records (loading a gate from disk is the anti-pattern that file's docstring closed; moving the cluster is a refactor of a 1000-line gate inside a bug fix). Re-weighed rather than worked around: the subject is the workspace a session sits in, `git -C <elsewhere>` does not move that, and the interruption count is identical because the budget is per session. What changes is WHEN it arrives, and `skills/implement/SKILL.md` §1 — *"the cost of a question is not its difficulty, it is when it arrives"* — makes the first Bash call the better placement, not the tolerable one |
| Whether the mode arm joins `commit-review-gate.py` | `plan.md` rejects it because `ask_reason` builds a waiver form from every arm's marker | rejected, on a different ground | The stated one is a five-line change and it undercounted the budget: three arms render into ONE deny. The ground that holds is that `tests/test_gate_judges_the_repo_it_commits_to.py` and `tests/test_chain_hooks_hardening.py` pin a two-arm prompt — `"BOTH questions in ONE call"` — and compare a whole reason against a released version, so a third arm rewrites pinned text across a 1600-line suite this work item has no business rewriting |
| Two stale counts in the READMEs | *Four of the seven gates* and *the four hooks that read it*, both written before `implementer-mark` and `implementer-notice` joined the table | corrected to seven of ten, with the hooks named out rather than counted | Adding a row without touching them makes a wrong number wronger. `hooks/commit-review-gate.py#offer_header` records the same lesson: a written-down count is a second thing to keep in step |
| Whether to re-verify the shared ledger rows this branch drifted | the repo rule says a branch keeps the ledger true | left DRIFTED, and named here | `evidence-check --reverify` rewrites the hash and does NOT move the `Checked` date, so a blanket run would have dated a read on 2026-09-02 at content that exists only now, on nine rows. DRIFTED is the honest state and its own instruction — *widen to the unit and re-read* — and CI treats drift as a warning (`.github/workflows/test.yml` exits only at 2 or above) |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator, in the broad gate after the rounds settle (`agent-contract` §2) |
| every platform but macOS 15.5 — Windows and Linux legs of this branch | the repository's own CI on the pull request; `pr-notes.md` §*Platform honesty* names the three places a difference would show |
| four cases in `tests/test_the_records_can_be_carried_out_and_in.py` fail on this branch AND on its base — reproduced with the branch stashed | the repository owner; they predate this work and are outside the scope it may change |
| whether `--worktree` should read routing declarations from the working tree, so a local-mode round reports *declared* | the repository owner; `questions.md` Q3 and `seal/follow-up.md` |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements `hooks/config.py#config_rows` rather than calling it — a third copy of one parser | the repository owner; the header-gate case this branch added exists because that copy left the real one uncovered |

## Not done

**#158 was kept out**, as `docs/flow.md` §0.9.1 says explicitly: it asks
whether the root should live under `.git` at all, and folding it in would
settle a design question inside a bug fix.

**`chain_check` was not taught to read an untracked declaration**, which is
the change that would remove the residual friction — a local-mode round still
prints *examined nothing*. The argument is in `spec.md` §*The sharp question*
and the option is recorded as Q3 rather than dropped.

**`skills/verify/scripts/unverified_check.py:573` derives a root the same way
`round_record.py` did and was left alone.** It needs one only under
`--baseline`, and a local-mode root has nothing committed for a baseline to
compare against — so its refusal there is correct rather than the same defect.

**The nine drifted rows in `seal/ledger.md` were not re-verified**, for the
reason in the divergence table. Whoever re-reads them should run
`evidence-check --reverify` and move the `Checked` dates in the same edit.

## Fed back into the spec

**`skills/implement/SKILL.md` §Bootstrap gained an instruction and lost one**
— it records the mode with `seal mode` where it previously said in as many
words not to. Inferred during implementation: the old rule was right about
defaults and wrong about traces, and #151's second Done-when is exactly that
an answered question has to leave one. `templates/config.md`'s *There is no
default* is untouched and still governs, because recording an observation the
bootstrap just made is not assuming a default.

**`CLAUDE.md`'s preset routing rule gained a leading condition.** Inferred
during implementation, from #151's own reading: a conditional appended to a
block meant to be read straight through only helps a session that notices it
applies.
