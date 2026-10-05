# Feature Specification: the worktree guard asks about a message search and reads no body token (#790, #780)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issues #790 and #780, milestone `release: 0.18.3`. Both are places where the
worktree guard reads a command differently from the program that runs it, and
both fail in the quiet direction: the guard says nothing where it should ask.

- **#790.** `git checkout :/<message>` detaches HEAD at the newest commit
  whose message matches, so the tree moves. `hooks/worktree-guard.py#is_ref`
  asks git about `<name>^{commit}`, and a `:/` message search reads that
  suffix as part of its pattern, so no commit matches, `classify` reads a
  restore, and the guard is silent. `switch_kind` reads the same words as a
  switch, so candidate C (`wider_only_kinds`) counts the switch as one the
  frozen loop already holds and subtracts it. The issue asks for the class:
  every revision syntax git accepts for a `checkout`, checked against the
  guard's readers by construction. Its second box is the stale comment above
  the `KINDS` rows in `tests/test_guard_resolves_the_tree_it_judges.py`,
  deferred to it by round 2 of work item
  `1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection`
  (`rounds/round-2.md` ⬜ 3; the paste-ready words are in that round's
  `rounds/round-2-report.md` §*Paste-ready fixes*).
- **#780.** `hooks/worktree-guard.py#has_token` reads the guard's two
  consent tokens out of the command as written, here-document bodies
  included. A `[shared-tree-ok]` a command only carries as data, inside a
  body, passes a switch silently at the two cannot-tell rows of §A, and a
  `[worktree-ok]` there lowers the single-stream creation deny to an ask.
  #773 closed the same class at the commit gate in 0.18.2 and left this read
  out of scope (work item `1791119070-a-waiver-inside-a-here-document-body-is-data`,
  `questions.md` Q1, answered (b), filed as #780).

Every record of this work item names the mechanism and the code coordinate.
Shapes are described in words; the test cases hold the strings.

## The frozen reading, and what this work does not reopen

`hooks/cmdline_base.py` is byte-pinned below its rider to
`86256492:hooks/cmdline.py` by
`tests/test_the_frozen_reading_never_grows.py#test_the_bytes_below_the_rider_are_86256492s`,
and `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/questions.md`
P4 is the owner's answer that keeps it so. **This work does not edit that
file or that test.** Nothing in either defect lives there:

- `is_ref` and `classify` are in `hooks/worktree-guard.py`. `classify`'s
  `checkout` and `switch` arms were reopened by the owner on 2026-10-04 for
  #764 and #738 (work item 1791119071, `spec.md` §*The frozen reading, and
  what the owner reopened*, and its `questions.md` P1). The name lookup is
  inside the `checkout` arm, and #790's own fix text asks for exactly this
  ("a word starting with `:/` is resolved the way git resolves it for
  `checkout`"). The owner placed #790 in milestone `release: 0.18.3`. That
  placement, read the way 1791119071 read the placement of #764, is the
  owner's agreement to this rule; `routing.md` records the batch.
- `has_token` is in `hooks/worktree-guard.py`, and the body reader it gains
  is `hooks/tokens.py#without_bodies`, which #773 wrote for every consent
  read. Its module docstring says so: "A new consent read starts here".

What does change is the sentence of policy that lists what the guard reads
past the base. `docs/worktree-guard-spec.md` §*Which tree, when the command
walks to it*, first paragraph, says "One rule is read past the base, since
#764 and #738". After this work a second is: a `checkout`'s name is looked up
the way `git checkout` resolves it. The paragraph is amended to say so, on
whose act and when (Scope, In 2). Segments, `-C` values and `cd` landings stay
the base's.

One part of #790's class goes beyond the ticket's words: the remote-tracking
guess (C3 below), which `is_ref` reads for `origin` alone. It is the same
cause, the guard resolving a checkout's name differently from git, so §12
puts it in. Whether the owner's act covers it is the one question only a
person can settle; `questions.md` P1 carries it with the default the build
uses.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*A. Branch switch* | A switch over a tree with another session or uncommitted changes is denied, offered as a choice or asked. The defect is that these shapes never reach the table. The table does not change |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*, first paragraph | The list of what is read past the frozen base. This work adds the name lookup to it (Scope, In 2) |
| `docs/worktree-guard-spec.md` §*Choice sites*, the paragraphs from **Retry tokens, one per direction** to the token table | Where the tokens are read from: "The command, and only the command". This work adds that a token inside a here-document body is not read (Scope, In 5) |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | A wrong deny costs one prompt, a wrong allow can break another session's tree. It is why both changes are built to move only towards a question |
| `docs/worktree-guard-spec.md` §*Known limits* | Where what this work still does not read is named (Scope, Out) |
| `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read*, the paragraph **Only what the shell would EXECUTE is read as commands** | #773's rule for the commit gate's consent reads: a waiver is typed in front of a command, so a body is skipped and comments are kept. #780 applies the same rule at the guard; this clause is not edited |
| `seal/specs/1790815613-…/questions.md` P4; `tests/test_the_frozen_reading_never_grows.py` | `hooks/cmdline_base.py` stays byte-pinned; this work reads it as it is |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. Each is an acceptance row below |
| `CONTRIBUTING.md` §*House rules*, both READMEs move together | `README.md` and `README.ko.md` describe the two tokens as bare words; both gain the body sentence (Scope, In 5) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is enumerated by construction (below); each changed sentence is pinned in the same commit as the behaviour; each new case is seen red against the base |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | The changelog entry goes in this directory's `changelog.md`, the ledger rows in `seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md` |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from` | A released row whose anchor this work moves is re-read by a citing row in the fragment, never re-stamped in place |

## The class, enumerated by construction (§12)

### #790: how git resolves a checkout's name, against how the guard does

`git checkout <name>` with no creating option, and with no `--` or a bare
`--` after the name, resolves `<name>` by three routes, in this order (`git
help checkout`, git 2.54.0, *DESCRIPTION* and the `<branch>`/`<start-point>`
entries, read 2026-10-05):

| Route | What git accepts | What the guard does today |
|---|---|---|
| C1 a single-revision expression naming a commit | every single-revision form of `gitrevisions(7)` §*SPECIFYING REVISIONS*: `<sha1>`, `<describeOutput>`, `<refname>`, `@`, `[<ref>]@{<date>}`, `<ref>@{<n>}`, `@{<n>}`, `@{-<n>}`, `[<branch>]@{upstream}`/`@{u}`, `[<branch>]@{push}`, `<rev>^[<n>]`, `<rev>~[<n>]`, `<rev>^{<type>}`, `<rev>^{}`, `<rev>^{/<text>}`, `:/<text>` (with its `:/!-` and `:/!!` modifiers), `<rev>:<path>`, `:[<n>:]<path>`; git switches or detaches only where the object peels to a commit | `is_ref` asks `<name>^{commit}`. Correct wherever the suffix peels the named object; wrong wherever the suffix changes what the name parses as. Read: the `:/<text>` forms absorb it into the pattern (#790). Every other form is measured (M1) |
| C2 the merge-base shorthand `<a>...<b>` | the single merge base of `<a>` and `<b>`, either side omitted meaning `HEAD`, only where there is exactly one | `rev-parse --verify` takes one revision, so `<a>...<b>^{commit}` resolves nothing: silent wherever git detaches (read; M1 confirms) |
| C3 the remote-tracking guess (`--guess`, the default) | a name that is no local branch and matches a remote-tracking branch in exactly one remote, or in `checkout.defaultRemote`: git creates the branch and switches to it | `is_ref("origin/<name>")` only: silent for a remote by any other name |

The range forms of §*SPECIFYING RANGES* (`^<rev>`, `<a>..<b>`, `<rev>^@`,
`<rev>^!`, `<rev>^-<n>`) name no single commit, and git does not switch on
them; M1 confirms each is refused and stays outside the class.

The carriers, the words that make a segment read a name this way:
`checkout <name>`, `checkout <name> --`, `checkout --detach <name>`,
`checkout --detach <name> --`. `switch` and `switch --detach` read any word as
a switch already (`classify`'s `switch` arm reads no ref), so they carry no
lookup; they are generated beside the others to show it. A creating option
makes the segment `create+switch` before any lookup, so its start point
carries no lookup either.

The guard's readers, each of which a shape crosses: `classify` with its tree
(the path test, `is_ref`, the `origin/` guess, the `)` peel), `switch_kind`
without one, and candidate C, which compares the two. `switch_kind` already
reads every name but `.` as a switch, so a form `classify` misses is always
subtracted by C. The fix is therefore owed in `classify`'s lookup alone, and
the generated check runs every shape through all three.

### #780: where the guard's consent tokens are read

Enumerated from where the two literals are read in `hooks/` (searched
2026-10-05), not from where the finding pointed:

| Read | Token | Reads a body today | In this work |
|---|---|---|---|
| `hooks/worktree-guard.py#has_token`, called by `guard_worktree_creation` | `[worktree-ok]` | yes: `_tokenize` over the command as written | **in** |
| `hooks/worktree-guard.py#has_token`, called by `main`'s switch ladder | `[shared-tree-ok]` | yes, the same read | **in** |
| `hooks/tokens.py#given` (`hooks/answer-write.py`) | lists both in `KNOWN` | no, since #773 | already body-free; `hooks/answers.py` carries neither guard token to a hook |
| the Agent/Task path | none | — | reads no token (§B) |
| `hooks/worktree-guard.py#parses_cleanly` | none | — | not a consent read: it decides whether the unbalanced-quote note is added. Unchanged |

What a body token did, by consumer, and which way the change moves it:

| Body | Base | Now | Direction |
|---|---|---|---|
| any body a program other than a shell consumes (a file's text, a Python program, a sink with any delimiter) | the token was read as typed | not read | silent pass → choice (`[shared-tree-ok]`), ask → deny (`[worktree-ok]`) |
| a body fed to a shell that runs a switch or a creation inside it | read | not read | the same. The way on is the token typed outside the body, which every documented form already does |
| text the reader takes for a body and the shell does not | read | not read | the same, rarely |
| a body the reader does not see | read | read | unchanged; the base's residual, named so nobody reads it as closed |

## Scope

### In

1. **`is_ref` resolves a name the way `git checkout` does (C1, C2)**,
   OR-ed with today's lookup, so it can only turn a "no" into a "yes":
   - today's `rev-parse --verify --quiet <name>^{commit}` first, unchanged,
     so every name the base resolved answers with the same one call;
   - where that fails: resolve `<name>` with no suffix, then peel the object
     it named to a commit by its object name, which no suffix can be absorbed
     into (this reaches every C1 form, `:/<text>` included);
   - where `<name>` holds `...`: split it at the first `...` the way git
     does, read an empty side as `HEAD`, resolve each side as above, and
     count it a commit where `git merge-base --all` gives exactly one.
2. **The guess reads every remote (C3)**, OR-ed with today's `origin/<name>`
   lookup: a remote-tracking branch `refs/remotes/<remote>/<name>` in any
   remote counts. Where two remotes hold it, git refuses unless
   `checkout.defaultRemote` names one, and the guard asks anyway — a refused
   command asked about costs one prompt, the louder direction. The `)` peel
   reads through the same lookups. This item rides P1's default.
3. **The policy text, in the same commit as the behaviour (§14)**: §*Which
   tree*'s first paragraph names the second rule read past the base, on
   whose act and when; §*Known limits* names what stays out (below); the pin
   `test_the_guard_policy_says_what_it_reads_past_the_base` moves with it.
   `README.md` and `README.ko.md` say nothing about how a checkout's name is
   resolved, and stay as they are for #790.
4. **The `KINDS` comment** in `tests/test_guard_resolves_the_tree_it_judges.py`
   takes round 2's paste-ready words: a `--` with a word after it takes every
   name out of a checkout.
5. **`has_token` reads no body (#780)**: a token counts only where the base
   read finds it AND the same read over `tokens.without_bodies(command)`
   finds it, through the same `_tokenize`, parenthesis stripping and Windows
   doubling. Where `tokens.without_bodies` cannot load or raises (it imports
   `hooks/cmdline.py`, which the guard already survives failing to load), the
   second read runs over the frozen reader's `cmdline_base.drop_heredoc_bodies`
   instead, the body reader `_judgment_text` already uses, so a broken wider
   reader neither honours a body token nor takes the typed token away
   (`plan.md` *Alternatives considered*, rows F–H). The words that say what
   the read reads change in the same commit: `has_token`'s and
   `_judgment_text`'s docstrings, the module docstring's retry-token
   paragraph, `hooks/tokens.py`'s rule list ("the commit gate's `has_marker`
   already does" names the guard's read too), the token paragraphs of
   `docs/worktree-guard-spec.md` §*Choice sites*, and the two token rows of
   both READMEs (`README.md`'s *[worktree-ok] in a worktree command* and
   *[shared-tree-ok] in a switch command*, and `README.ko.md`'s two rows that
   carry the same tokens).
6. **The checks**, each seen red at `a3aa139a` before it is committed (§15):
   the C1–C3 cases with a real git, the generated never-quieter properties
   (A4, A9), the body cases and the implication case for `has_token`.
7. **The records**: `changelog.md`, the ledger fragment with its rows and
   `Re-read ·` rows, `overview.md` (the builder's), `phases/phase-N.md`.

### Out, and why

- **`hooks/cmdline_base.py` and its pin.** Nothing here needs it (above).
- **A `checkout <tree-ish> <path>` with no `--`** (`git checkout HEAD~1
  README.md`). git restores the file, and `classify` reads the first name as
  a ref and asks. That is the louder direction on a shape nobody reported,
  and the base's answer; §*Unknowns resolve conservatively* keeps it.
- **`git checkout --detach` and `git switch --detach` with no name.** They
  detach HEAD at the commit it is on, so no file moves; `KINDS` pins both as
  `None` (`"switch with no target"`), which is a decision already made, not
  this class.
- **A name git refuses but the guard resolves** (a `<rev>:<path>` that names a
  blob, a range form). With the OR in In 1 a "yes" never becomes a "no", so a
  shape the base asked stays asked. M1 lists any such shape, and §*Known
  limits* names it only where M1 finds one git refuses and the guard asks.
- **Reading `checkout.guess`, `checkout.defaultRemote` or `--no-guess`.** The
  guard reads no git config today, and ignoring them asks more, never less.
- **A timeout on `is_ref`'s git calls.** `repo_paths` carries one and
  `is_ref` never has. A timeout read as "no ref" would be a new quiet
  direction, which is a decision of its own, not this class. The calls In 1
  adds take `is_ref`'s existing form.
- **A note when a token is found only inside a body.** The deny and the
  choice already name the token and where to type it. #773 added no such note
  at the commit gate, and nothing documents a body as a place a token goes.
- **`parses_cleanly`.** It is not a consent read.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1. git moves on every constructed form | Given a scratch repository with two commits, a branch, a tag, a reflog, a second remote with a branch only it holds and two branches with one merge base, when each C1–C3 form runs under each carrier, then git switches, detaches or refuses, and which one is recorded | Executed in phase 1 against the installed git (2.54.0), outside the tree, probe deleted; the table goes in `phases/phase-1.md` (M1) |
| A2. `classify` reads every form git moves on | Given that repository, when `classify` reads each carrier × form git switched or detached on in A1, then `switch` (or `create+switch` for C3 where the name is new); each form git refused keeps the base's verdict | Executed: parametrized cases in `tests/test_guard_resolves_the_tree_it_judges.py` with a real git, red at `a3aa139a` for every `:/`, `...` and non-`origin` guess shape |
| A3. #790's own shape through `main()` | Given a dirty tree under a clean session, when `git checkout ':/<message>'` matching a commit is judged, then the dirty-tree row asks; the same command whose pattern matches nothing stays silent | Executed: one case through `main()`, red at `a3aa139a` |
| A4. Nothing the base asked goes quiet (#790) | Given the generated carrier × form shapes, when the build's `classify` verdict is compared with `a3aa139a`'s on the same repository, then every shape the base read as a switch the build reads as one | Executed: a generated case comparing the two lookups shape by shape; it holds by the OR in In 1, and the case shows it rather than assuming it |
| A5. A restore stays a restore | Given `checkout :/<message> -- README.md`, `checkout <a>...<b> -- README.md` and `checkout -- README.md`, when read, then `None`, as at the base | Executed: cases beside A2 |
| A6. A consent token in a body is not read | Given a command that carries `[shared-tree-ok]` only inside a here-document body (once in the one shape `hooks/one_heredoc.py` matches, once with an unquoted delimiter) and a switch after the terminator, at a cannot-tell row, then the choice is put, where the base was silent; the same for `[worktree-ok]` in a body at the single-stream creation row, which denies where the base asked | Executed: cases through `main()`, red at `a3aa139a` |
| A7. The documented forms still carry consent | Given the token typed as a trailing comment, as a bare word before or after the command, and inside `( … )`, each beside a heredoc in the same command, then it is read, as at the base. `test_the_retry_token_survives_a_closing_parenthesis` and `tests/test_worktree_guard.py`'s token cases stay green unchanged | Executed |
| A8. A broken wider reader keeps both halves | Given `wide` unloadable (the way `test_a_broken_wider_reader_costs_only_the_question` makes it), then a body token is still not read and a typed token still is | Executed: a case beside that test, red at `a3aa139a` for the body half |
| A9. `has_token` never reads more than the base | Given every command of A6–A8 and the existing token cases, for both tokens, then the build's `has_token` is True only where `a3aa139a`'s is | Executed: a parametrized implication case; holds by the AND in In 5 |
| A10. The policy says what the guard reads | §*Which tree*'s first paragraph names the name lookup as read past the base since #790; §*Choice sites* and both READMEs say a token inside a here-document body is not read; each sentence is pinned | Executed: each pin red against the current text; read: the sentences against the code clause by clause |
| A11. The frozen file did not move | `tests/test_the_frozen_reading_never_grows.py` passes with no case deleted | Executed |
| A12. The prompt budget is counted over the recorded runs | Given the transcript corpus 0.18.2 counted (Bash uses before 2026-10-03T11:06:22+09:00, 25,741 distinct command and directory pairs on 2026-10-04) and, beside it, every pair recorded up to the build day, when base and build are replayed, then the pairs whose answer changes are listed for each reader, each is a shape of this class, and none is quieter | Executed in phase 1 (before) and phase 4 (after), probe deleted; counts in the phase records and in the pull request's prompt budget (M3) |
| A13. The records hold | `bin/evidence-check --strict .` exits 0 after the `Re-read ·` rows; `bin/survivor-check` over the range reports none or rows with grounds; `tests/test_no_real_identifiers.py` passes | Executed |

**Failure direction**, stated once for both: each change is built so it can
only make the guard stricter. #790 ORs a lookup onto the base's, so a
"switch" never becomes "no switch". #780 ANDs a read onto the base's, so a
token is never read where the base did not read it. A9 and A4 check that the
construction holds.

**Prompt budget**: a new question arises only on a `checkout` naming a
`:/`, `...` or non-`origin` guessed name that git moves the tree on (#790),
or on a command whose only consent token sits in a body (#780). A12 counts
both over the recorded runs.

**Platform honesty**: the new lookups are `git rev-parse` and `git
merge-base`, which read no process table. The real-git cases run wherever
the module runs, Windows CI included; the `:/` forms are quoted in the cases
so no shell splits them.

## Data & interfaces

- `hooks/worktree-guard.py`: `is_ref` keeps its signature
  `(name, cwd) -> bool`; what it answers widens (In 1). The `origin/` guess
  in `classify` reads every remote (In 2); the helper's name is the
  builder's. `has_token` keeps its signature `(command, token) -> bool`.
- `hooks/tokens.py`: no new function. `without_bodies` is called, not
  edited; its module docstring's rule list gains the guard's read.
- No change to `hooks/cmdline_base.py`, `hooks/cmdline.py`,
  `hooks/one_heredoc.py`, `hooks/worktree_consent.py`, or §A's rows and
  messages. What a person reads when asked is unchanged; which commands reach
  a question changes.
- Ledger: the units this work changes are cited by released rows in
  `seal/releases/0.18.2.md` (at least D1, D4 and W1), `0.18.0.md` (K6, K7)
  and `0.16.0.md` (M2); `bin/evidence-check --strict .` names the full set
  (`questions.md` W1).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-05 by framer, before the build.
