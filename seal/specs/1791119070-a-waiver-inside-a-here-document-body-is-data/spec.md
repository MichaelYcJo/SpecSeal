# Feature Specification: a waiver inside a here-document body is data

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#773, found by round 1 of #769 (work item
`1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data`, shipped in
0.18.1; its records are read on the local backup ref of that branch). The
commit gate's waiver reads take a waiver token out of a here-document body, so
a token the command only carries as data can silence the gate for a commit
into a repository that declares no work item. A waiver is typed in front of a
command; a token inside a body is not that.

Every record in this work item names the mechanism and the code coordinate.
Shapes are described in words; the test cases hold the strings the code needs.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read*, the paragraph **Only what the shell would EXECUTE is read as commands** | Its last sentence says the scan for a waiver token "still sees the command as written". This work amends that sentence. The only reason the tree gives for it is the comment in `hooks/commit-review-gate.py#commit_invocations`: "a waiver token is written inside a comment on purpose". That reason covers comments and not bodies, so comments stay read and bodies stop being read |
| `docs/commit-review-gate-spec.md` §*A file edit goes through the `Edit` tool* | The commit reading reads every body as shell for whether it commits, except the one shape `hooks/one_heredoc.py` matches. This work leaves that reading alone. Only the consent reads change |
| `docs/the-commit-gate-inside-git.md` §*The commit gate inside git*, the paragraph on how a stop is put | "`hooks/answer-write.py` reads the bare word out of the Bash call and `hooks/answers.py` carries it to the hook". That read is `hooks/tokens.py#given`, and it reads bodies too. This work amends the sentence to say the bare word is read outside here-document bodies |
| `skills/implement/SKILL.md` §1, *A waiver is one command's*; `CLAUDE.md` §*Git* | The waiver goes in front of the command, quotes included. That is the spelling every documented form uses, and none of them puts it inside a body |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class: every read that takes a consent token out of command text. §*Scope* enumerates it |
| `skills/agent-contract/SKILL.md` §14, §15 | The verdict a person sees changes, so the docs sentences and the pinning cases go in the same commit as the fix. Each new case is shown red against the base before it is planted |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from` | A released row whose anchor this work moves is re-read through a citing row in `seal/ledger/1791119070-a-waiver-inside-a-here-document-body-is-data.md`. It is never re-stamped in place |
| `CLAUDE.md` §*The goal a design is chosen against* | Of two designs that catch the same defect, the one that stops more has to argue for it. `plan.md` §*Alternatives considered* makes that argument for the one place this work adds a stop |

## Scope

### The class, enumerated by construction

A consent read is any read that takes a waiver token out of a Bash command's
text. The tree has three. The list comes from where the four known tokens are
read (`hooks/tokens.py#KNOWN`, and `gate.TOKENS`), not from where a finding
pointed.

| Read | Tokens | Reads a body today | In this work |
|---|---|---|---|
| `hooks/commit-review-gate.py#has_marker` — the PreToolUse reading. Two call sites: `judge`'s waived arms and `main`'s unreadable-target branch | `[no-review]`, `[no-parity]` | yes: `split_segments` over the raw command, plus a substring fallback over the raw command when the split is not clean | **in** |
| `hooks/tokens.py#given` — called by `hooks/answer-write.py`, whose answer `hooks/answers.py` hands to the git hook. It is the only consent read for a command `hooks/tokens.py#is_plain` leaves to git | the same two (`answers.NAMES`) | yes: `words()` runs `shlex` over the raw command | **in** |
| `hooks/worktree-guard.py#has_token` — the worktree guard | `[worktree-ok]`, `[shared-tree-ok]` | yes: `_tokenize` over the raw command | **out**, see below |

`tokens.given` is in scope because without it the fix covers one path out of
two. Where this plugin's git hooks run, a commit is judged inside git, and the
token the hook honours is the one `given` read.

### In

- Both commit-gate consent reads read the command with its here-document
  bodies taken out, and comments kept. The bodies taken out are exactly the
  bodies the gate already knows about. Where `hooks/one_heredoc.py#reduce`
  matches, the read uses its reduced text. Everywhere else it uses
  `hooks/cmdline.py#drop_heredoc_bodies`. No new tokenizer is written.
- **The new read can only refuse, never newly honour.** A token counts only
  where the base read found it AND the read without bodies finds it. This
  holds by construction rather than by a property of the splitter. Without
  the AND, removing a body can turn an unclean split clean, and a waiver the
  base did not read would then be honoured.
- The comments and the policy text that describe the consent reads say what
  they now read. That is four comments: `has_marker`'s docstring, the comment
  in `commit_invocations`, the comment in `main`, and the rules list in
  `hooks/tokens.py`'s module docstring. It is also the two policy sentences in
  §*Grounding*.
- The re-reads of released ledger rows whose anchors move (`plan.md`
  §*Operational impact* lists them), the work item's own ledger rows, and its
  changelog fragment.

### Out, one line each with the reason

- **`hooks/worktree-guard.py#has_token`.** It is the same class at a different
  gate, and sibling item D edits that file. `questions.md` Q1 asks whether it
  joins this item or gets an issue of its own.
- **The commit reading.** `commit_invocations`, `_hides_a_commit`, the
  `one_heredoc` grammar and the `unparsed` fallback keep what they read. A
  body is still read as shell for whether it commits.
- **`hooks/cmdline.py` and `hooks/cmdline_base.py`.** They are called and not
  edited. That keeps sibling D's edit to `hooks/worktree-guard.py#classify` clear of
  this one.
- **Making `has_marker` and `given` one read.** They disagree on a command
  that does not split cleanly: one falls back to a substring test, the other
  reads nothing. Choosing between those two is a decision about unclean
  commands. It has nothing to do with bodies.
- **A token in a `sh -c` string or inside `$( … )`.** Both readers see such a
  string as one quoted word, so the bare-word comparison does not match unless
  the whole string is the token. That is not a body, and it is not reported
  as a defect.
- **Issue #773's second checkbox.** #769 already corrected that comment, so it
  is not this work's to do: at release head `94d7b2e0`, `main`'s comment says
  which way each raw-text read runs and names this issue as the open half.
  This work rewrites that comment once more, because its last sentence calls
  #773 pending.

### What is excluded, by the consumer of the body, and which way each case moves

"Excluded" means the text the new read drops: the one shape's body, or every
body `cmdline._heredoc_split` returns. Each case below is sorted by what
consumes the body.

| # | Body | What the base did with a token there | Now | Changes what the base read as a waiver typed in front of a command the shell runs? |
|---|---|---|---|---|
| 1 | One shape, sink: the body becomes a file's text | honoured it | not read | no. No shell runs the body |
| 2 | One shape, `python3 -`: the body is a Python program | honoured it, for a commit in the suffix | not read | no. The commit reading reads no commit in that body, so the token could only ever waive a different command, the suffix's. This is #773's case |
| 3 | Any other body a non-shell program consumes, for example a sink with an unquoted delimiter or another interpreter | honoured it | not read | no. Same reason as 1 and 2 |
| 4 | A body fed to a shell, which runs it | honoured a token typed in front of a commit inside the body. The commit reading meets that commit as an unresolved target | not read: the commit stops | **yes.** This is the one case where a waiver a shell would actually run gets refused. It turns a silent pass into a stop, never the reverse. The way on is to type the token in front of the Bash call's own command, which stays outside every body. `plan.md` argues the cost |
| 5 | Text the splitter takes for a body and the shell does not (over-drop) | honoured it | not read | yes, rarely. It also turns a silent pass into a stop. The splitter's own design leans the other way (`_heredoc_split`'s comments treat keeping text as the fail-closed direction for a judgment read) |
| 6 | A body the splitter does not see (under-drop) | honoured it | honoured it | no change. This residual is the base's, named here so nobody reads it as closed |

So the answer to the direction question is this. Cases 4 and 5 change
something the base read as a waiver in front of a command the shell runs. Both
move from a silent pass to a stop. The AND above makes the reverse impossible.

## User scenarios & acceptance *(mandatory)*

Every PreToolUse case runs in an opted-in repository with no git hooks and
no declaration, so the PreToolUse reading is the one judging.
`tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py#make_repo` builds
that repository. "The tokenless verdict" means the verdict the same command
gets with the token taken out of the body. Comparing against it pins the
change without pinning one particular stop wording.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — #769's round-1 probe | Given a command of the one shape with the `python3 -` program, whose body holds the review waiver token inside a Python string literal, and whose suffix commits with `git -C` into the undeclared repository. When the commit gate reads it. Then the verdict is the tokenless verdict (a stop), where the base was silent | A case in `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`, shown red against `94d7b2e0`'s `has_marker` |
| S2 — a body outside the one shape | Given a heredoc the one-shape reader refuses (a sink with an unquoted delimiter), whose body holds the token as a bare word, then a commit after the terminator into the undeclared repository. When read. Then the tokenless verdict | A case in the same module, red first |
| S3 — the documented forms still waive | Given a command that carries a heredoc and a commit, with the token typed (a) as the no-op in front of the command on line 1, and (b) as a trailing comment on a line outside the body. When read. Then silent, as at the base | A case in the same module. Every existing case in `tests/test_the_waiver_can_be_typed.py` stays green |
| S4 — `tokens.given` reads no body | Given the S1 and S2 commands, `given` returns no token. Given the S3 commands, it returns the token. Given a command whose raw text does not split but whose text without bodies does, it returns what the raw read returns, which is nothing | New rows in `tests/test_the_old_spellings_reach_the_hook.py#test_a_token_is_a_bare_word_and_nothing_else`. The body rows are red first |
| S5 — the stated cost, pinned | Given a body fed to a shell, holding the token in front of a commit, with nothing outside the body. When read. Then the unresolved-target stop, where the base was silent. The same command with the token typed in front on line 1 is silent | A case in the same module as S1. Its docstring names `spec.md` case 4 |
| S6 — never newly honoured | Given any command in the cases above, the new read finds a token only where the base read found one | A parametrized case over the S1–S5 commands that asserts the implication for both readers |
| S7 — the words agree | The two policy sentences in §*Grounding* say the consent reads skip here-document bodies and keep comments. Their `Enforced by:` lines name the S1, S4 and S5 cases. The four code comments no longer say the consent read sees the whole command | The checker that reads `Enforced by:` lines resolves the names. Read by the reviewer |

## Data & interfaces

- A new function in `hooks/tokens.py` returns the command with its
  here-document bodies taken out and comments kept: `one_heredoc.reduce`'s
  text where it matches, else `cmdline.drop_heredoc_bodies`. Both consent
  reads use it. `tokens.py` already imports `cmdline` lazily inside
  `is_plain`. `one_heredoc` imports nothing but `re`.
- `has_marker(command, marker)` and `given(command)` keep their signatures.
  Their callers (`judge`, `main`, `hooks/answer-write.py#main`) do not change.
- No new hook, no new config row, no new file outside this work item's
  directory and its ledger fragment.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-10-04 by framer, before the build.
