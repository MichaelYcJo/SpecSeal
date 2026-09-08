# Feature Specification: local mode from first setup to the gate

<!-- seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/spec.md -->

Two tickets, one path. #151 is the moment a repository picks a mode; #225 is
what the review chain does with the mode it picked. A repository that reaches
local mode by either route today meets a record tool that refuses its root and
a pull-request check that reports its declaration missing.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §*The opt-in signal is the root itself* | The root's presence is the opt-in and no config key decides it. That is why the third direction #151 lists — making `seal/config.md` the signal — is out of scope: it replaces this clause rather than patching around it |
| `skills/agent-contract/SKILL.md` §16 | Every `seal/…` path means `<repo>/seal/` where that exists and `$(git rev-parse --git-common-dir)/seal/` otherwise. Two scripts in `skills/code-review/scripts/` do not honour it |
| `skills/implement/SKILL.md` §*Bootstrap* | The mode question is asked here and nowhere else. #151 is the route that never reaches here |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. Answered in `pr-notes.md` |
| `CLAUDE.md` §*The goal a design is chosen against* | Verification that runs unattended. The prompt this work adds is a price paid against it and has to be argued, not assumed |

## Scope

**In.**

1. `round_record.py#where` resolves a work item that sits under the common
   git directory, instead of refusing it.
2. `chain_check.py` says which root it searched, so a local-mode repository
   stops reading a false *no declaration*.
3. A root whose mode nobody recorded is a state something names — a gate at
   the commit, and `seal mode` as the way out.
4. The preset block in `CLAUDE.md`, which `install.sh` copies into
   `~/.claude/CLAUDE.md`, points at the bootstrap before it tells a session
   to write `routing.md`.

**Out.**

- **#158** — whether the root should live under `.git` at all. It is a design
  question, and folding it in would settle it inside a bug fix
  (`docs/flow.md` §0.9.1 says so explicitly).
- **Making `seal/config.md` the opt-in signal.** #151's third direction. It
  reopens the clause named in Grounding above.
- **Teaching `chain_check` to read an untracked declaration.** Argued below.

## The sharp question — where an untracked declaration lands

In local mode nothing under the root is committed, so
`chain_check#tracked_declarations` — a `git ls-tree HEAD -- seal/specs/` —
has no file to find. Three answers were available.

| Answer | What it does | Verdict |
|---|---|---|
| **A. Say which root was searched** | The message names the root this repository actually uses and, in local mode, says nothing under it is committed. The verdict does not move: still a pass with a notice | **Taken** |
| B. `--worktree` reads declarations from the working tree | `round_record.py` already passes `--worktree` for the round record it just wrote; extending it to the declaration would make the local run report *declared* | Rejected |
| C. Read an untracked declaration in CI too | — | Rejected outright |

**Why A.** The ticket's complaint is ambiguity, not the verdict: *"a false
'no declaration' is indistinguishable from a genuinely undeclared work
item"*. Naming the root removes exactly that, and it is the one change that
**cannot move a verdict** — a defect in it is a confusing sentence, never a
wrong pass. `CONTRIBUTING.md` asks for a stated failure direction, and a
change with no verdict to get wrong is the cheapest direction available.

The remaining friction is real and it is correct. A local-mode round still
prints *examined nothing*, because CI genuinely cannot check that repository:
`templates/hygiene.yml`'s header and `implement` §*Bootstrap* both say local
mode installs no pull-request checks and gives up CI enforcement. A notice
saying so on every round is that trade surfacing, not a defect hiding.

**Why not B**, which is the tempting one. It is not unsafe on the axis
`read_record`'s docstring warns about — finding a declaration makes the check
demand round records, so reading the working tree there is *stricter* than
reading HEAD, not more permissive. It is rejected on two other grounds. It
makes the local run assert a chain verdict CI can never reproduce, which is a
second guarantee the tree then has to keep true; and the declaration is
committed **before the first edit** by rule, so an uncommitted one is not the
transient state `--worktree` was built for. It stays on the table as a
follow-up with a named answerer rather than being decided here.

**Why not C.** `tracked_declarations`'s own docstring closes this: reading
the working tree is *"more permissive locally than in the place it actually
runs"*. C would reopen it in the file that documents why it was closed.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A local-mode item is a record's home | Given a repository whose root is at `<git-common-dir>/seal/` · When `round_record.py new --item <that item>` runs with no `--root` · Then the record is written and nothing is refused | `tests/test_local_mode_reaches_the_review_chain.py` |
| S2 | The refusal that stays says what it looked at | Given an `--item` that is under no repository at all · When the same command runs · Then it still refuses, and the message names the item and that no repository was found either way | same |
| S3 | A linked worktree resolves too | Given the same repository, and the command run from a linked worktree of it · When the record is written · Then the root resolved is that worktree, not the main tree | same |
| S4 | A shared-mode item is unchanged | Given `<repo>/seal/` · When the record is written · Then the root is the one `reader.repo_root(item)` already returned | existing `tests/test_the_record_is_generated.py` stays green |
| S5 | Local mode reads its own root back | Given a local-mode repository holding a declaration for this branch · When `chain_check.py` runs · Then the notice names the local root, says nothing under it is committed, and does **not** tell the operator to add a file | `tests/test_local_mode_reaches_the_review_chain.py` |
| S6 | Shared mode still says add the file | Given a shared-mode repository with no declaration for this branch · When `chain_check.py` runs · Then the notice still names `seal/specs/<work-item>/routing.md` | `tests/test_chain_check_at_the_pull_request.py` stays green, plus a new case |
| S7 | A root with no recorded mode is named | Given a repository with `seal/` and no `Mode` row · When a commit is issued · Then the gate denies once with both ways on, and asks on the next attempt | `tests/test_the_mode_question_is_asked_once.py` |
| S8 | A recorded mode is silent | Given the same repository with `\| Mode \| shared \|` · When a commit is issued · Then the gate says nothing | same |
| S9 | A repository with no root is silent | Given no `seal/` at either place · When a commit is issued · Then the gate says nothing — a globally installed plugin must not nag | same |
| S10 | One prompt per session per repository | Given the gate denied once · When a second commit is issued in the same session · Then the decision is `ask`, which approving gets past | same |
| S11 | The preset names the question | Given `CLAUDE.md`'s `specseal:start`/`specseal:end` block · When it is read straight through · Then the sentence that tells a session to write `routing.md` says first what to do in a repository that has no root yet | `tests/test_first_setup_asks_once.py` |
| S12 | What `install.sh` copies is what was changed | Given the block above · When `install.sh` extracts it · Then the extracted text carries S11's sentence | same |

## Data & interfaces

**New module `hooks/config.py`.** The repository config table — where it is,
how it parses, and what the `Mode` row says. It exists because two callers
need the row and `seal.py` is a two-thousand-line command a `PreToolUse` hook
must not import. `seal.py` keeps the writer (`with_row`, `table_span`,
`write_row`) and re-exports the reader by name, so there is one parser rather
than a second reader that drifts from it.

It is **not** in `hooks/optin.py`. That module's docstring says there is no
config key and everything in it fails toward *not opted in*; the `Mode` row
decides nothing about opting in, and putting it there would read as the
clause in Grounding being softened.

**New gate `hooks/mode-gate.py`**, in the `pre-bash` group. Its own gate
rather than a third arm of `commit-review-gate.py`: the two arms there are
about whether a *change* was checked and carry a waiver token each, where
this one is about *setup* and has no waiver — `seal mode` takes a second and
always works, so a waiver would only build the standing exemption
`docs/review-chain-spec.md` refuses. It reuses `hooks/cmdline.py` for target
resolution rather than parsing a command line a second time.

## Open questions → questions.md

`questions.md` carries the one decision this work did not take: whether
`--worktree` should read declarations from the working tree (alternative B).
