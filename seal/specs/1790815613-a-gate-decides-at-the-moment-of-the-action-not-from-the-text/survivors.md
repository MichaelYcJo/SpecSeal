# Survivors — a gate decides at the moment of the action, not from the text

`survivor-check --range cd24f516..HEAD`, run at `c5f650c` by `smith`, reported six
places. The range corrected two comments and one paragraph that described the
text reading as the only reading: the commit gate's comment on the routing
declaration (moved into `hooks/gate.py#arms_missing` and reworded), the rider in
`hooks/cmdline_base.py` (which said #692 would delete the file), and the guard
policy's *the commit gate still reads both*. Each place below shares phrasing with
one of those and states something still true, or is an earlier work item's record
of its own moment.

| Path | Quote | Grounds |
|---|---|---|
| `docs/commit-review-gate-spec.md` | **The gate reads `seal/specs/<work-item-id>/routing.md` before it | the declaration still silences the review arm, now read in `hooks/gate.py#arms_missing` for both the git hooks and the fallback; the statement is true |
| `docs/commit-review-gate-spec.md` | silent — the routing question was answered before the first edit, and CI checks the answer at the pull request. | the decision table's declared row, true for both readings |
| `skills/code-review/scripts/chain_check.py` | It runs on the pull request, where nobody has to be sitting. | the chain check's own docstring, about CI; this range does not touch it |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/overview.md` | the rider in `hooks/cmdline_base.py` says those comments describe `542f920b` and that #692 reconciles them | work item 1790745049's closing memo, a record of what the rider said then |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/overview.md` | several of its comments name the worktree guard or the consent writer as a reader | the same memo's divergence row, a record of its own build |
| `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/spec.md` | the commit gate still reads both. | work item 1790745049's frame, true of the commit gate on the day it was written; the policy now says which reading |
| `seal/specs/1790381327-an-automation-run-creates-its-worktrees-without-asking/overview.md` | six rows of `seal/releases/0.9.1.md` and S3, S4 | work item 1790381327's closing memo, a record of its own moment; it shares only the guard's and the consent writer's names with the `hooks/cmdline_base.py` rider this branch rewrote. Reported by `broad-gate --preflight` over the whole branch after the merge of `release/v0.17.0` |

## Round 1's fix pass

`survivor-check --range 12c09ec3..e3ecb7d7`, run by `smith`, reported 62 places
(61 after one heading in `tests/test_the_frozen_reading_never_grows.py` was
corrected). The range withdrew phase 4's design on the owner's answer to P6:
it deleted `hooks/creationgate.py`, `hooks/git/post-checkout.py`, their test
module and the guard policy's *Where git decides* section, and it took this
branch's own notes back out of eight release rows whose code returned to the
release base's bytes. Nothing it removed was corrected into something else,
so each place below shares phrasing with a copy that went, not with a claim
that changed. The kinds, named in the grounds: the guard's own ladder texts,
which `creationgate.py` had copied (**guard text**); sentences that share
only test or anchor names with a removed `Enforced by:` line (**names**); the
framer's drawing of the design before P6, whose divergence `overview.md`
records (**frame**); another work item's record of its own moment
(**record**); and text of this branch that is still true for commits
(**true**).

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/plan.md` | switch is judged where git switches | frame |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/plan.md` | The commit gate, the worktree guard's two arms and the consent writer | frame |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/spec.md` | switch is judged where git switches | frame |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/spec.md` | the first creation of an attended session is still one | frame |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/spec.md` | a commit is judged where it lands, whatever the command | frame; S1 is still true |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/spec.md` | A decision is made by a program git runs inside the action | frame; true for commits, and `overview.md`'s convergence row says so |
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/spec.md` | What stays a text read, and why that is safe. | frame |
| `hooks/worktree-guard.py` | if they are forgotten tabs this is effectively single | guard text |
| `hooks/worktree-guard.py` | A command that also creates a worktree is judged by these rows | guard text |
| `hooks/worktree-guard.py` | single-stream work, don't create a worktree | guard text |
| `hooks/worktree-guard.py` | Declining cancels this — use the worktree already | guard text |
| `hooks/worktree-guard.py` | If this genuinely is concurrent work needing | guard text |
| `hooks/worktree-guard.py` | The Agent tool was called with isolation | guard text |
| `tests/test_worktree_guard.py` | The Agent tool was called with isolation | guard text, pinned by the guard's own case |
| `docs/worktree-guard-spec.md` | use the worktree that session opened, or wait for | guard text |
| `docs/worktree-guard-spec.md` | six creations in one session on a | guard text; the budget the PostToolUse writer keeps again |
| `docs/worktree-guard-spec.md` | stream work uses plain `git switch` on the shared tree. | guard text |
| `docs/review-handoff-protocol.md` | test_a_record_says_what_ran_it.py | names |
| `docs/round-record-spec.md` | test_a_document_that_names_a_script_says_how_to_reach_it.py | names |
| `docs/the-evidence-ledger.md` | skills/settle/scripts/fold_check.py::bound | names |
| `seal/releases/0.15.3.md` | fold_check.py#numbered_statements | names |
| `seal/releases/0.15.3.md` | fold_check.py#main | names |
| `seal/releases/0.15.3.md` | test_a_document_has_room_for_the_next_fold.py#prose_disagreements | names |
| `seal/releases/0.15.3.md` | Settle what the release leaves behind | names |
| `seal/releases/0.15.3.md` | fold_check.py#located | names |
| `seal/releases/0.8.0.md` | chain_check.py#runner_problem | names |
| `seal/releases/0.8.0.md` | chain_check.py#ON_RE | names |
| `seal/releases/0.8.0.md` | test_a_record_says_what_ran_it.py#INSTRUCTORS | names |
| `seal/releases/0.8.0.md` | templates/sdd-phase.md | names |
| `seal/releases/0.15.4.md` | both are now pinned in | names |
| `seal/releases/0.15.5.md` | broad_gate.py#as_cmd_expands | names |
| `seal/releases/0.15.6.md` | hooks/worktree-guard.py#judgeable | names |
| `seal/releases/0.16.0.md` | the enumeration was phase 5's alone | names |
| `seal/releases/0.16.0.md` | noglob git commit` is judged where the shell is | names |
| `seal/releases/0.16.0.md` | a redirection in front of the program word | names |
| `docs/commit-review-gate-spec.md` | stand in front of a command without opening | names |
| `docs/commit-review-gate-spec.md` | A program that runs its operands as a command | names |
| `docs/commit-review-gate-spec.md` | A commit there is judged where the shell is | names |
| `templates/config.md` | The directory is judged where the row starts | names |
| `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` | judged where the shell is | names |
| `seal/specs/1790263216-the-older-statements-name-what-enforces-them/plan.md` | test_a_folded_statement_names_what_enforces_it.py | record |
| `seal/specs/1790263216-the-older-statements-name-what-enforces-them/spec.md` | line names | record |
| `seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/plan.md` | test_a_script_copied_on_its_own_says_which_sibling_it_misses | record |
| `seal/specs/1790381329-the-deferred-sentences-and-pins/plan.md` | The round's case appended to | record |
| `seal/specs/1790381329-the-deferred-sentences-and-pins/spec.md` | the round's case, appended to | record |
| `seal/specs/1790550713-what-the-last-rounds-deferred/spec.md` | docstring, a line holding | record |
| `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/spec.md` | the lead says the token carried the person's | record |
| `seal/releases/0.14.0.md` | The texts are unchanged and the three cases pass | record |
| `seal/releases/0.4.0.md` | none of the answers this claim is about is read differently | record |
| `tests/test_gate_judges_the_repo_it_commits_to.py` | The gate resolved everything from the payload's | record, a case's docstring about #39's gate |
| `seal/releases/0.9.1.md` | Creation consent is observed after the call ran | the release base's row, restored with the code it cites |
| `seal/releases/0.9.1.md` | A session that already created a worktree in this clone is not | the release base's row, restored with the code it cites |
| `seal/releases/0.9.4.md` | The bound on the ALLOW is untouched | the release base's row, restored with the code it cites |
| `tests/test_the_commit_gate_decides_at_the_commit.py` | the entry point says the same thing on its own | true: `commitgate.pre_commit` with no session |
| `tests/test_the_commit_gate_decides_at_the_commit.py` | Every case runs a real shell and real git in fixture repositories | true of the commit hooks |
| `hooks/git/pre-commit.py` | Run by the stub | true; `post-checkout.py` was its sibling |
| `docs/commit-review-gate-spec.md` | In a clone carrying this plugin's git hooks, a | true: the commit statement |
| `docs/commit-review-gate-spec.md` | Where git decides, the PreToolUse reading in the next | true: the commit statement, with round 1's exception added |
| `hooks/commit-review-gate.py` | kept for a clone whose hooks slot | true: the commit reading's stand-aside comment |
| `hooks/implementer-notice.py` | `post-commit` says this line for | true |

## Round 3's fix pass

`survivor-check --range b34b5401..b34272cb`, run by `smith`, reported five
places. The range rewrote the policy's stand-aside paragraph, the gate's
comment and contract §9's parenthesis from a list of words to the positive
rule (`questions.md` P7). The list itself still exists: `steps_around_hooks`
is one of `is_plain`'s conditions, so its own docstring and comments still
describe what it reads (**true**). The release rows carry this branch's
earlier dated notes, each followed by this pass's note of 2026-10-02
(**record**).

| Path | Quote | Grounds |
|---|---|---|
| `hooks/tokens.py` | The kinds, each living in the one command where the installer | true: `steps_around_hooks`' own docstring, about the words it reads |
| `hooks/tokens.py` | `--config-env` or `git config`, and HOME or XDG_CONFIG_HOME | true: the same function's comment on its config-file arm |
| `seal/releases/0.16.0.md` | in a clone without them both decision sites are untouched and the three cases pass unedited | record: E1's note of 2026-10-01 |
| `seal/releases/0.16.0.md` | the unreadable site is untouched and the case passes unedited | record: E2's note of 2026-10-01 |
| `seal/releases/0.16.0.md` | in a clone without them it is unchanged and the case and the corpus pass | record: E17's note of 2026-10-01 |

## The ceiling fix after the chain

`survivor-check --range 28daffc6..2d964e21`, run by `smith`, reported one
place. The range froze `docs/commit-review-gate-spec.md` over the document
line ceiling until MichaelYcJo/SpecSeal#715, and rewrote the fold case's
docstring, which had said the listing stays empty for the next such document.
The place is another work item's rejected alternative, quoting that docstring
as it stood (**record**).

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790260563-the-fold-checks-run-only-as-this-repositorys-tests/plan.md` | the test docstring records the intent to keep the listing for the next document a fold takes past the ceiling before it can be split | record: work item 1790260563's plan, a rejected alternative quoting the docstring of its day; the listing was kept, and this range is that next document arriving |
