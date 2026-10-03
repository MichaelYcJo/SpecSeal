# Feature Specification: a gate decides at the moment of the action, not from the text (#692)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person is the more expensive, and the difference has to be argued. The comparison table in §*The three candidates, measured* is that argument, cell by cell |
| `routing.md` §*Why this way*, and the owner's decision of 2026-09-30 recorded in `seal/specs/1790745049-…/spec.md` §*Grounding* | The static reading of shell text is the stopped class. A design that adds one more rule to it is refused here before it is proposed, and `plan.md`'s Alternatives table says so in its own row |
| `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read* | "The repository judged is the one the command commits *into*, not the one the shell sits in." The policy already names the right question. This work changes who answers it: git, at the commit, instead of a reader of the command's text |
| `docs/commit-review-gate-spec.md` §*Why a deny, and why only once* and §*The declaration, and where the check went instead* | The two ways a stop is put (a `deny` to the model, an `ask` to the person), the automation press, the routing declaration and the two arms all stay. What goes is the `ask`: a git hook cannot render two buttons, so every stop becomes a refusal whose text names the ways on, which is the shape the press already produces |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | Its last paragraph names this work: "#692, the redesign of how the gates learn where a command acts, decides the guard's reading again, and deletes the frozen copy." The frozen copy is deleted wherever git can decide, and §*Scope* says where it cannot |
| `docs/worktree-guard-spec.md` §*Creation consent* and §*Unknowns resolve conservatively* | The consent record is "written **after** the answer rather than before the question" — the one thing a command text cannot forge. A `post-checkout` hook is that same fact one step closer to the action. A wrong deny costs a prompt and a wrong allow breaks another session's tree, so a refusal is the fail direction where the two differ |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget and platform honesty. §*What a change to a gate must carry* below states them for this work, and phase 1 of `plan.md` is where the budget is counted rather than hoped |
| `skills/agent-contract/SKILL.md` §13 | A defence resting on a platform guarantee is not verified. The session id reaches a git hook through an environment variable the harness sets (§*What the tree answered*, 4). That is a platform guarantee, so the design carries a second route (the lease's pid) and S9 removes the variable and checks the gate still decides |
| `skills/agent-contract/SKILL.md` §9 and §17, `agents/smith.md`, the user's `CLAUDE.md` *Routing* paragraph | Each describes what the text gate reads. They were written to steer agents around a reader; once no reader exists, the sentences that steer around it are false and go. §*Scope* lists them |
| `hooks/optin.py` module docstring; `docs/one-root-by-lifetime.md` | The opt-in is the `seal/` root, read one way, and `specseal-scratch` takes it back. A git hook stub reads the same answer at run time, so an installed stub in a repository that later opts out is silent |

## What the tree answered, so nobody reopens it

Everything in this section is **read**, from the coordinates named, or
**executed** where marked, by the framer on 2026-10-01 in the worktree at
`cd24f516`. Nothing was built and no probe left anything.

1. **Why no further patch to the text reading is proposed.** The ticket says
   it, the owner's memory of 2026-09-30 says it, and the record shows it:
   #674's three rounds, Q7's cap, #689's round 1 (`seal/specs/1790745049-…/
   rounds/round-1-report.md`: "the guard judges another tree in 78 commands at
   `542f920b`, 36 at the target and 19 under the flag" over 4,380 generated
   commands) and the abandoned branch `fix/689-past-the-cap-…` (its
   `plan.md`'s four alternatives, each an ordering rule) each found one more
   shape. `plan.md` Alternatives row *P* is the refusal.
2. **The invariant moves from text to actions.** Work items 1790644505 and
   1790660768 built under "no command shape may read silent where `86256492`
   stopped it". The ticket names that invariant as the thing that forces the
   old model to be carried beside the new one. This frame replaces it with:
   **no commit, branch switch or worktree creation that reaches an opted-in
   repository goes unjudged, and a command that performs none of the three
   is nobody's business.** Every stop the base made on a real action in an
   opted-in repository is kept by construction (git runs the hook on every
   such action); every stop it made on a command that performs no action is
   lost on purpose. The count of each over the corpora is phase 1's
   measurement (`questions.md` M6), not a hope.
3. **Which hooks git offers for which action** — executed, from
   `git help githooks` of the git on this machine (2.50.1, Apple Git-155):
   `pre-commit` and `commit-msg` run before a commit and abort it on a
   non-zero exit, and both are bypassed by `--no-verify`;
   `reference-transaction` "is invoked by any Git command that performs
   reference updates", in the states `prepared`, `committed`, `aborted`,
   "also supports symbolic reference updates", receives `<old> <new> <ref>`
   lines on stdin, and is not named by `--no-verify`; `post-checkout` runs
   after `git switch`/`checkout` and after `git worktree add` (unless
   `--no-checkout`), "cannot affect the outcome", and receives the previous
   and new HEAD and a branch flag. Hooks run with the working directory at
   the root of the working tree and `GIT_DIR` exported. What the manual does
   not say — whether the working tree is already updated when
   `reference-transaction prepared` fires for a switch, whether a worktree
   creation's new `HEAD` goes through a transaction at all, and the first
   git version at which the symref support holds — is `questions.md` M1–M3.
4. **How a git hook knows the session, and whether a Claude session is
   running at all** — executed in this framer's own Bash tool: the harness
   exports `CLAUDECODE=1`, `CLAUDE_CODE_SESSION_ID` (equal to this session's
   lease file name under `<git-common-dir>/specseal-leases/`),
   `CLAUDE_PID` (equal to the `pid` that lease records and to the parent
   `claude` process), `CLAUDE_CODE_CHILD_SESSION=1` for a subagent,
   `CLAUDE_CODE_SESSION_ATTENDED=1`, `CLAUDE_CODE_ENTRYPOINT=cli` and
   `AI_AGENT=claude-code_2-1-286_agent`. `CLAUDE_PLUGIN_ROOT` is **not** in
   that environment. A child git inherits it, and so does the hook git
   spawns. So the hook has the session id without reading any text, and the
   second route — the parent `claude` pid matched against the lease records
   `hooks/session-lease.py` already writes — exists for a harness that sets
   none of these (§13). What `CLAUDE_CODE_SESSION_ATTENDED` means is M4.
5. **The automation press is readable from a git hook.**
   `hooks/worktree_consent.py#automation_answered(top, session, "")` resolves
   the transcript by session id through `transcript_for` (the glob
   `~/.claude/projects/*/<session>.jsonl`) and needs no command line. The
   commit gate already imports it that way (`hooks/commit-review-gate.py:127`).
6. **The routing declaration needs no text either.** `hooks/routing.py#declared(cwd, root)`
   reads the branch with `current_branch(cwd)`; in a hook `cwd` is the
   worktree git acts on, so the branch is the one git commits to. The
   measured 0.16.0 failure — 13 of the run's 14 commit-gate `ask`s named the
   main checkout because an agent's `cd <worktree> && …; git commit` carried
   a failure branch into the session's directory (`seal/specs/1790644505-…/
   spec.md` §*Where the four prompts came from*; count below) — cannot occur,
   because the hook runs where the commit lands.
7. **What the recorded run cost, counted** — executed as a read of the
   transcripts on this machine (`~/.claude/projects/-Users-michael-Documents-
   GitHub-SpecSeal/ab2760f5-….jsonl` and its 67 `subagents/*.jsonl`), distinct
   hook decisions by timestamp and reason text: **13 `ask`s** reading *No
   review is recorded for this cycle in <main checkout>* (1 in the main
   transcript, 12 in subagents), **1 `ask`** and at least **3 `deny`s**
   reading *This command contains something the gate cannot read as a plain
   command*, **2 `ask`s** from the guard's tracked-changes row, **5 `allow`s**
   from creation consent, and 11 `AskUserQuestion` calls in the main
   transcript. The memory note's "15 gate asks and 102 minutes" is the
   owner's recollection; the 15 matches 13 + 1 + a construct stop within
   rounding, and the minutes are M7. The two earlier milestone sessions
   (`8cadfa28…`, `30ac0e06…`) show no commit-gate decision to the same
   regex; that is **unverified** (the 0.15.x gate's output shape may differ)
   and M7 reads them by hand.
8. **The ticket's "PreToolUse becomes an advisory fast path" is refused.**
   An advisory reader is the same reader with its deny removed. It would keep
   `hooks/cmdline.py` alive, give the model two messages for one commit, and
   its misreadings would still be read by the model as facts. The git hook's
   stderr reaches the model through the Bash tool's result, which is the
   advisory. `plan.md` Alternatives row *A′*.
9. **Hooks run from the installed plugin copy, never from the tree**
   (executed: `~/.claude/plugins/cache/specseal/specseal/` holds twelve
   versions including `0.16.0`, and `hooks/hooks.json` names
   `${CLAUDE_PLUGIN_ROOT}`). So a git hook stub cannot read
   `CLAUDE_PLUGIN_ROOT` at commit time (4) and must carry the installed
   version's absolute path, rewritten by the installer whenever the running
   version differs. §*Migration* holds the consequence.
10. **One hooks directory per clone.** `git rev-parse --git-path hooks` from
    this linked worktree answers the main checkout's `.git/hooks` (executed),
    and `core.hooksPath` is unset here locally and globally (executed). One
    install covers every worktree of a clone, which is where the milestone's
    agents committed.
11. **What stays a text read, and why that is safe.** The consent tokens
    (`[no-review]`, `[no-parity]`, `[worktree-ok]`, `[shared-tree-ok]`) are
    bare words of a command, and git never sees a shell's `: '[no-review]';`
    no-op. A read that only ever widens a consent fails toward one more
    refusal, never toward a silent pass — `hooks/worktree-guard.py#has_token`
    and `docs/worktree-guard-spec.md` §*Choice sites* state that asymmetry.
    So a token translator may keep reading the command, and nothing else
    may. Whether the old spellings are kept at all is `questions.md` P3.
12. **#678 is refused by the design and #686 is answered by it**, in
    §*The two open issues*.
13. **The two whites round 3 of #689 deferred here** (the ticket's comment):
    ⬜ 1, the comment at `hooks/commit-review-gate.py:93` saying both gates
    import `cmdline`, goes with the file's text reader; ⬜ 2, the zsh word
    list at `docs/commit-review-gate-spec.md:392` omitting `foreach`, goes
    with the paragraph that lists what a reader reads past. Both close by
    deletion in phase 6; neither is fixed in place first.

## Scope

**In:**

1. **A git-side gate set**, installed per opted-in clone, each hook a stub
   that `exec`s the installed plugin's `hooks/git/<hook>.py`:
   - `pre-commit`: the commit gate's judgment — both arms, the routing
     declaration from the real branch, the marks, the automation press, the
     waiver — in the repository and worktree git commits into.
   - `reference-transaction` (`prepared`): the backstop for a commit that
     bypassed `pre-commit` with `--no-verify`, and, where M1/M3 say git
     refuses there cleanly, the switch and creation refusals.
   - `post-checkout`: the worktree-creation consent record, written in the
     clone the creation ran in, keyed by the session id; and the post-hoc
     half of the switch and creation arms where M1/M3 say refusal before the
     action is not clean on the supported git.
   - `post-commit`: the implementer notice (`hooks/implementer-notice.py`'s
     one line), which needs "a commit happened" and nothing else.
2. **An installer**, `hooks/hook-install.py`, in `dispatch.py`'s
   `session-start` group and, as one `stat` per call, in `pre-bash` for the
   payload's `cwd` repository: writes the stubs into
   `git rev-parse --git-path hooks` of an opted-in clone, rewrites them when
   the installed version moved, and refuses a slot it does not own (P1).
3. **Session identity in a hook**: `CLAUDE_CODE_SESSION_ID` first, the
   ancestor `claude` pid matched against `specseal-leases/` second, and
   *not a Claude session* otherwise (P2).
4. **A git-native waiver and answer spelling**, `git -c specseal.waive=<arm>`
   and `git -c specseal.answer=<token>`, read through `git config` inside the
   hook; and a PreToolUse **token translator** that keeps the four
   bare-word spellings working by writing a one-shot answer the hook consumes
   (P3 decides whether the translator ships, and for how long).
5. **The refusal texts**, one per stop, each pinned (§14): the automation
   text and the attended text, both naming the git-native way on and, where
   the translator ships, the old one.
6. **Deletion of the text readers for judgment**: `hooks/cmdline.py`'s
   walk, readers and the commit gate's PreToolUse decision path; the guard's
   Bash walk; `hooks/worktree_consent.py#creation_directory`;
   `hooks/cmdline_base.py` wherever git decides (P4 says what stays below the
   git floor). What remains of `cmdline.py` is a bare-word tokenizer for the
   translator, and nothing that names a directory.
7. **The two policy documents rewritten** around the action rather than the
   reading: `docs/commit-review-gate-spec.md` (the decision table, §*Which
   repository*, §*A `cd` the gate cannot read*, the #669/#670/#674
   paragraphs, §*Why a deny, and why only once*, the waiver table) and
   `docs/worktree-guard-spec.md` (§*Which tree*, §*Creation consent*'s record
   paragraphs, §*Choice sites*' token rows, §*Known limits*). The sentences
   in `skills/agent-contract/SKILL.md` §9 and §17, `agents/smith.md`,
   `skills/implement/SKILL.md` §1, `templates/`, `README.md`, `README.ko.md`
   and the repository's `CLAUDE.md` that steer a session around the text
   reader (the `cd … &&` shape, `git -C <abs> commit … in a command of its
   own`, "the gate reads a heredoc body as shell") go or are rewritten to
   what is now true. The ledger rows anchored on removed units are REMOVED
   in their files and the new claims written to
   `seal/ledger/1790815613-….md` (`CLAUDE.md` §*a change writes fragments*).
8. **The migration**, §*Migration*: what a repository on 0.16.0's hooks
   meets while this is built, at the first session on 0.17.0, and below the
   git floor.
9. **The measurements the ticket's acceptance asks for**, taken in phase 1
   and written into `phases/phase-1.md`, with the comparison table below
   re-stated with numbers.

**Out, each with its reason and who answers it:**

- **A global `init.templateDir` or a user-level `core.hooksPath`** so that a
  clone no session ever started in carries the stubs. Both are writes to a
  person's git configuration outside any repository, which this plugin has
  never made; the known limit is stated in §*Data & interfaces* and M8
  measures how often the recorded runs committed into such a clone. The
  owner can reopen it with that number.
- **Reading the command text to refuse `--no-verify`.** It is the stopped
  class; the `reference-transaction` backstop is the answer.
- **The Agent/Task `isolation: "worktree"` PreToolUse arm.** It reads
  `tool_input.isolation`, not text, and stays as it is; M5 decides whether
  `post-checkout` or the PostToolUse arm records its consent.
- **The review-skill gate, the mode gate, the lease, the evidence advisor,
  the review-history guard.** None reads a command for where it acts.
  `review-history-guard.py` reads `gh` commands for *what* they post, which
  no git hook sees, and it is a reminder with no decision.
- **The release and CI scripts** (`chain_check.py`, the hygiene workflow).
  They read the tree at the pull request, not a command.
- **A timeout on git hooks, Windows CI for the stubs beyond what M9 can
  show, and husky/pre-commit chaining beyond P1's answer.**

## The three candidates, measured

Each cell is `read` from the coordinate it names, or names the measurement
(`questions.md` M-rows) that fills it in phase 1. "The recorded run" is
session `ab2760f5` under 0.15.7's installed gate, counted in §*What the tree
answered*, 7.

| | **A. git-native** | **B. static, fail-closed** | **C. hybrid: A where git decides, the frozen 0.16.0 reading where it cannot** |
|---|---|---|---|
| What judges | git's own hooks, in the repository and worktree the action reaches | the text reader, with every segment `understood` refuses and every unresolved directory turned into a stop for every consumer | A's hooks; `hooks/cmdline_base.py` byte-for-byte, only below the git floor (P4) and in a clone whose hooks slot is foreign (P1) |
| Stops lost against `86256492` | every stop on a command that performs no commit, switch or creation in an opted-in repository — the construct and unparsed partitions (`docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read*), and every stop whose target never opted in (the policy's own silence row). Count over the corpora: **M6**. In the recorded run: the 1 `ask` + ≥3 `deny`s on heredoc patches of test files, which committed nothing (read, `seal/specs/1790644505-…/spec.md` §*Where the four prompts came from*, rows 1 and 4) | 0 by construction: it only adds | A's where git decides; 0 where the frozen reading stays |
| Stops added | every real action the base missed: #686's seven `cd` spellings and the 8 of 9 redirected-`cd` spellings `seal/specs/1790660768-…/rounds/round-2-report.md` measured silent at all three SHAs while bash committed; a `git -C "$VAR" commit` whose `$VAR` is an opted-in repository (judged there instead of stopped as unreadable). Each added stop is a commit, switch or creation nothing judged before. Count: **M6** | every segment the reader does not understand, on every consumer: the guard's 36–78 disagreements per 4,380 commands (`seal/specs/1790745049-…/rounds/round-1-report.md`), the 38-against-20 tail shapes of round 2 of 1790660768, and every `cd W && …; …` whose `W` is unresolved. In the recorded run none of the 14 commit-gate asks is removed, because each was a correct reading of the text (read, 1790644505's spec: "The gate's reading was right each time") | A's where git decides |
| Prompts per session, the recorded run | **0 to the person.** The 13 review `ask`s named the main checkout because of a failure branch the shell never took; the hook runs in the declared worktree and is silent. The heredoc accident whose body became a real `git commit` line (row 3 of that spec's table) is a real commit into the undeclared main checkout: one refusal to the model under the press, which is the correct stop kept. The guard's 2 tracked-changes `ask`s become 2 refusals naming the way on. Attended sessions: one `AskUserQuestion` per refusal where today they pay one `deny` and then `ask`s | **14 commit-gate stops stay** (0.16.0's E1 turns them into denies to the model under the press, `seal/releases/0.16.0.md` row E1), plus the added ones. An attended session pays each as a prompt | A's |
| Converges | yes — §*The convergence argument* | yes, at the cost above, and the cost grows with every construct a future shell adds, because "not understood" is the default | yes where git decides; the frozen part never changes, so it has nothing to converge to |
| #678 | refused: no reader exists to teach the three shapes to | built: three more rules | refused |
| #686 | answered: there is no unresolved `cd` | answered: ask | answered where git decides; the frozen fallback keeps the base's silence below the floor |
| What breaks in six months | a git release changes a hook's contract (M1's table is pinned per version and CI runs the floor and the newest) · a harness release renames the session variable (the lease route stands, S9) · a project adopts a hook manager (P1's answer, said once per session, never silent) | the next construct · the next ordering of two readers · the next cap (the record of milestone 49) | A's, plus one: somebody adds "one more rule" to the frozen fallback. S11 pins the file to `86256492`'s bytes so that rule has to delete a test first |

The ticket's acceptance box one asks for each candidate "against the
milestone-49 corpora and the recorded sessions". The corpora exist as
generators in the tree (`tests/test_no_shape_the_base_stops_reads_silent.py`,
`tests/test_guard_resolves_the_tree_it_judges.py`,
`tests/test_the_reader_agrees_with_bash.py`) and as deleted probes whose
sizes the round reports record (W1 8,640; 1790660768 round 3: 1,013 commands
and 572 base stops; #689 round 1: 4,380; #689's build: 43,544 and 3,648
through `main()`; round 3: 784). A candidate that reads no text has to be
measured by what bash and git **do** with each command, which is the oracle
`tests/test_the_reader_agrees_with_bash.py` already uses for the reader.
Phase 1 replays the generators through real bash in sandbox repositories
carrying the stubs and counts (M6); until then the cells above are the
arguments, labelled as such.

## The convergence argument

A decision is made by a program git runs inside the action: `pre-commit`
runs in the process that is making the commit, in the working tree whose
index becomes the commit, on the branch `HEAD` names there;
`reference-transaction` runs with the ref update locked on disk;
`post-checkout` runs in the worktree that was just created or switched. The
model's command text is never an input to any of them. So no shell
construct, present or future — a redirection, a subshell, an `eval`, a
loop variable, a `pushd`, a zsh word, a construct no shell has yet — can
route a commit, a switch or a creation around the decision, because a
command that performs the action reaches git, and one that does not needs
no decision. That is the criterion the text reading never had: the set of
things to read is the empty set.

What **can** step around a git hook is a list git itself maintains, and it
is short: `--no-verify` (bypasses `pre-commit` and `commit-msg`, and nothing
else — the `reference-transaction` backstop is the answer, M2);
`core.hooksPath` pointing elsewhere, a stub deleted or made non-executable
(the installer re-checks at every session start and every Bash call in the
repository, and a slot it cannot own is said once per session through the
dispatcher's failure channel, never silence — P1); and a git whose version
lacks a hook or its symref support (the floor, M1, pinned per version and
run in CI). Each item is finite, documented by git, and changes only with a
git release, which is a thing a version-keyed test can pin. The design is
complete when each item on that list has an answer, and the list is git's,
not the shell's.

What still reads a command is the token translator, and its failure
direction is the whole argument for letting it: a token it cannot read
costs one refusal naming the git-native spelling, and a token the model
wrote has exactly the standing tokens always had (`docs/worktree-guard-spec.md`
§*Choice sites*: "an audit trail, not an authorization"). Nothing it reads
decides where an action lands.

## The two open issues

**#678 — refused with grounds.** Its three shapes (a top-level expanded
command word, `parallel`'s command word, the guard's merged view) are each a
rule for a reader of text. Under this design no reader of text decides
anything: `"$CMD"` that expands to a commit commits in a repository whose
`pre-commit` runs; `parallel git commit …` runs `git commit`, which runs the
hook; `git 2>&1 worktree add` creates a worktree whose `post-checkout`
runs. The issue's acceptance — "each shape measured against the recorded
runs for the stops it would add" — is answered by M6 at zero, because the
shapes add nothing a hook does not already see. Closed by the pull request
that ships phase 3 and 4, with this paragraph as the comment.

**#686 — answered.** The guard asked whether to *ask* on a directory it
cannot resolve or keep judging the session's tree. Under this design there
is no unresolved directory: the switch runs in a worktree, and the hook
runs in that worktree. The seven spellings (`builtin cd w`, `command cd w`,
`time cd w`, `pushd w`, `noglob cd w`, `cd "$W"` with `W` unset, `2>&1 cd
w`) and the comment's `eval true; 2>/dev/null cd O || git worktree add` each
land where bash lands, and the hook judges there. What the issue's trade-off
weighed — a question per unreadable construct against silence — is not
paid either way. Below the git floor (P4) the frozen reading keeps
`86256492`'s silence on these, and the issue stays open for that floor only,
with that sentence as its comment.

## Migration

Three states, each with what a session meets.

| State | What runs | What a session meets |
|---|---|---|
| **While 0.17.0 is built** (the tree carries this work; `~/.claude/plugins/cache/specseal/specseal/0.16.0/` is installed — executed) | 0.16.0's PreToolUse gates, on every command, from the cache | Exactly 0.16.0: the commit gate reads text with #674's reading, the guard and consent through the frozen copy, every stop under the press a deny to the model. Nothing this branch writes under `hooks/` protects its own run (the memory note `the-installed-gate-is-not-the-tree` is the measured instance). The spawn-prompt rule — `git -C <abs> commit …` alone, edits through `Edit` — stays in force for this build and is dropped from the contract in phase 6, which ships after the build is over |
| **First session on 0.17.0 in a repository that was on 0.16.0** | `session-start` runs `hook-install.py`; `pre-bash` runs it again for the first Bash call's `cwd` | The stubs land in `<common-dir>/hooks/` of that clone, said once as a `systemMessage` naming the four files. From that call on, a commit is judged by `pre-commit`, a switch and a creation by `reference-transaction`/`post-checkout`, and the PreToolUse `pre-bash` group no longer carries `commit-review-gate.py` or the guard's Bash walk. Marker directories under the git dir (`specseal-reviewed`, `specseal-parity`, `specseal-leases`, `specseal-worktree-consent`, `specseal-worktree-choice`, `specseal-commit-choice`) keep their names and readers; `specseal-commit-choice` is read by nothing once no `ask` exists and is pruned by the installer |
| **A clone the installer never saw** (cloned by a command, never a session's `cwd`) | nothing | Silent, as a repository that never opted in is silent today. The stub arrives at the first session or Bash call whose `cwd` is inside it. M8 counts the recorded runs' commits into such clones; the out-of-scope `init.templateDir` is the lever if the number is not zero |
| **Below the git floor** (M1 names it) | A's `pre-commit`, `post-checkout` record and `post-commit` — these need no symref transaction — plus P4's answer for the switch and creation refusals | P4's default: the frozen `cmdline_base.py` reading in `pre-bash`, for the switch and creation arms alone, byte-identical to `86256492` and pinned so (S11); the commit gate never falls back |
| **A clone whose hooks slot is foreign** (`core.hooksPath` set, or a hook file the installer did not write) | P1's answer | P1's default: nothing installed, said once per session, and the frozen reading for every arm in that clone |
| **A repository that opts out later** (`seal/` removed, or `specseal-scratch` written) | the stubs stay on disk | Each stub reads `optin.home_at` at run time and exits 0 where the answer is empty; the installer removes stubs it wrote from a clone that no longer opts in |

What a person on 0.16.0 who never upgrades meets: 0.16.0, unchanged.

## User scenarios & acceptance *(mandatory)*

Phases that must run against a real git say so in `plan.md`; the rows below
name the test file each lands in.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a commit is judged where it lands, whatever the command said | Given a session in an undeclared main checkout and a declared worktree `W` of the same clone with the stubs installed; when any of the 0.16.0 run's four recorded commands (`seal/specs/1790644505-…/spec.md` §*Where the four prompts came from*) is run through real bash with `W` in place of `<W>`; then the two commits into `W` go through silently, the heredoc patch that commits nothing produces no stop, and the heredoc whose body became a real `git commit` in the main checkout is refused by `pre-commit` with the review arm's text naming the main checkout | `tests/test_the_commit_gate_decides_at_the_commit.py`, real git and bash, the four commands verbatim; seen red with the stub's judgment replaced by `exit 0` |
| S2 · every shape the base stopped on a real commit is still stopped | Given the corpora of `tests/test_no_shape_the_base_stops_reads_silent.py` and `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`; when each command is run through real bash in a sandbox whose opted-in, undeclared repository carries the stubs; then every command in which bash made a commit meets a refusal, and the count of commands in which bash made no commit and the base stopped is the number M6 records | the two modules retargeted: the oracle is whether a commit object appeared (`git rev-parse HEAD` before and after), not what a reader said; the retired reader-based assertions are deleted with a note naming this row |
| S3 · `--no-verify` does not pass a commit the gate would refuse | Given S1's undeclared checkout; when `git commit --no-verify -m x` runs; then the ref update is refused at `reference-transaction prepared`, `HEAD` is unmoved, the working tree and index are as before the command, and the refusal text is the same arm's text with one sentence saying the bypass was met at the ref | `tests/test_the_commit_gate_decides_at_the_commit.py`, real git; the "as before" clause is asserted on `git status --porcelain` and `git write-tree`; M2 decides the mechanism and this row pins whatever it is |
| S4 · the press is read in the hook and every stop is a refusal to the model | Given a transcript fixture with the `automation` press (the one `tests/test_the_guard_asks_once_per_session.py` builds) and `CLAUDE_CODE_SESSION_ID` set to its session; when a commit the review arm stops runs; then the hook exits non-zero with `AUTOMATION_WAYS`'s successor text, which names the git-native waiver, names no question tool, and says re-issuing unchanged meets the same refusal | `tests/test_an_automation_run_meets_no_commit_prompt.py` retargeted from PreToolUse payloads to real commits; each sentence pinned, deleting any one turns it red (§14) |
| S5 · an attended session gets the choice, once, through the model | Given no press; when the same commit runs; then the refusal instructs the model to put the arm's options up with `AskUserQuestion`, every option names a command that runs (the git-native spelling first, the old one second where P3 keeps it), and the second attempt meets the same refusal rather than two buttons | the same module; the "runs" clause is `tests/test_the_waiver_can_be_typed.py` extended to the `-c specseal.waive=` form against real git in every shell present |
| S6 · the git-native waiver is read, and inside a message it is prose | Given S1's checkout; when `git -c specseal.waive=review commit -m x` runs; then it commits, and `git commit -m "specseal.waive=review later"` is refused | `tests/test_the_waiver_can_be_typed.py`; M11 shows the hook sees `-c` through `GIT_CONFIG_PARAMETERS` first |
| S7 · a worktree creation that ran is consent for the session, recorded by git | Given no consent record; when `git worktree add <path> -b <branch>` runs from any directory, with any `cd`, redirection or wrapper in front of it that bash accepts; then `<common-dir>/specseal-worktree-consent/<session>` exists in the clone the worktree belongs to, and a creation written so that bash never runs it leaves no record | `tests/test_the_guard_asks_once_per_session.py`'s writer half retargeted to `post-checkout`, real git; the #686 and round-2 spellings as parameters, bash as the oracle for "ran" |
| S8 · the first creation of an attended session is still one confirmation, and an automation run pays none | As `docs/worktree-guard-spec.md` §*Creation consent* states, with the refusal in place of the `ask` where M3 says git refuses before the action, and the post-hoc answer P4/M3 settle where it does not | `tests/test_the_guard_asks_once_per_session.py`'s reader half; the six-creations sequence re-measured as **refuse, allow, allow, allow, allow, allow** or its post-hoc equivalent |
| S9 · the session is known without the environment variable | Given `CLAUDE_CODE_SESSION_ID` and `CLAUDECODE` unset in the hook's environment, a lease under `specseal-leases/` recording this process's ancestor pid, and the press in that session's transcript; when a stopped commit runs; then the hook decides as under S4. Given no lease either; then the hook treats the commit as P2's answer says | `tests/test_the_commit_gate_decides_at_the_commit.py`; §13: the guarantee removed and the gate still deciding |
| S10 · a switch is judged in the tree git switches, before it happens where git allows that, and undone where it does not | Given a clean session tree `S` and a dirty nested clone `w` with another session's fresh lease, the shapes of #686 and of `tests/test_guard_resolves_the_tree_it_judges.py`; when each runs through real bash; then the switch in `w` is refused (or reverted, with `w`'s `HEAD` and tree as before) with the ACTIVE-session text, and the switch in `S` is allowed | `tests/test_the_switch_is_judged_where_git_switches.py`, real git, version-keyed on M1's floor; `tests/test_guard_resolves_the_tree_it_judges.py`'s frozen-reader rows kept only under P4's fallback marker |
| S11 · the fallback never grows | Given P4 keeps `hooks/cmdline_base.py`; then its bytes below the rider equal `86256492:hooks/cmdline.py`, and no module outside the fallback arm imports it | `tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer` retargeted to a byte comparison against `git show 86256492:hooks/cmdline.py`; an import grep |
| S12 · the installer owns only what it wrote | Given a clone with `core.hooksPath` set, or a `pre-commit` file not carrying the stub's marker line; when a session starts there; then nothing is written, one `systemMessage` says which slot is foreign and what the session falls back to (P1), and a clone whose slot is free or already ours gets the stubs with the running version's path | `tests/test_the_hooks_are_installed_where_git_runs_them.py`, real git; the message text pinned (§14) |
| S13 · a stub in a repository that opted out is silent | Given the stubs and then `specseal-scratch` written, or `seal/` removed; when a commit runs; then the hook exits 0 and prints nothing | the same module |
| S14 · the two policies say what the code does | Every `Enforced by:` line in the two documents names a case that exists; the paragraphs listed in §*Scope* 7 are gone or rewritten; the #689 whites are closed by deletion | `tests/test_the_hooks_hide_what_a_renderer_hides.py`'s existing enforced-by walk; `bin/survivor-check` over the removed sentences |
| S15 · the ledger stays true | Rows anchored on removed units are REMOVED in `seal/ledger.md` and `seal/releases/*.md` with the new claims in this item's fragment; `bin/evidence-check --strict .` exits 0 | executed by phase 6 and the sealer |

## What a change to a gate must carry

- **Failure direction.** The commit gate blocks more on real commits (every
  base miss that is a real commit becomes a stop) and allows more on text
  (every stop on a command that commits nothing is gone). The guard moves
  the same way. Where a hook cannot run — a foreign slot, a clone never
  visited, a git below the floor — the design falls to a known earlier
  behaviour and says so once, never to silence nobody was told about.
- **Prompt budget.** Automation: zero to the person, by the same press
  reading 0.16.0 ships. Attended: one `AskUserQuestion` per stop, where
  0.16.0 pays one `deny` and then `ask`s; the recorded run's 14 commit-gate
  stops become 1. The number phase 1 counts replaces this sentence.
- **Platform honesty.** Hooks on Windows run through git's bundled `sh`; the
  stub is `#!/bin/sh` and tries `python3` then `py -3` as `hooks.json` does.
  Nothing here was run on Windows (M9); the CI leg that exists for the
  hooks' tests is where it is first run.
- **A test seen red.** Every S-row names how.

## Data & interfaces

- **New files**: `hooks/git/pre-commit.py`, `hooks/git/reference-transaction.py`,
  `hooks/git/post-checkout.py`, `hooks/git/post-commit.py`,
  `hooks/hook-install.py`, `hooks/gate.py` (the judgment the commit gate's
  `judge`, `changed_paths`, `touches_code`, `read_mark`, the arm texts and
  the press reading move into, imported by the git-side hooks and nothing
  PreToolUse), `hooks/tokens.py` (the bare-word tokenizer, from
  `has_marker`/`has_token`).
- **Removed**: `hooks/commit-review-gate.py` from `GROUPS["pre-bash"]` and
  from the tree; `hooks/cmdline.py`'s walk and readers;
  `hooks/worktree-guard.py`'s Bash walk and switch/creation ladders where git
  decides; `hooks/worktree_consent.py#creation_directory`;
  `hooks/cmdline_base.py` where P4 does not keep it.
- **Stub shape**: `#!/bin/sh`, a marker line `# specseal <version>`, then
  `exec python3 "<installed plugin>/hooks/git/<hook>.py" "$@" || exec py -3 …`.
  The installer compares the marker line to decide ownership and version.
- **Environment read by a hook**: `CLAUDECODE`, `CLAUDE_CODE_SESSION_ID`,
  `CLAUDE_PID`, `GIT_DIR`, `GIT_CONFIG_PARAMETERS` (for `-c`), and git's own
  hook arguments. Written by nobody here.
- **Markers**: unchanged names under the git dir; `specseal-commit-choice`
  retired; one new one-shot answer file for the translator,
  `<common-dir>/specseal-answer/<session>/<token>`, written by PreToolUse
  and consumed by the hook or removed by `post-bash` after the call, so it
  lives for one Bash call at most.
- **Known limit**: a clone no session's `cwd` ever entered carries no stub
  until one does. Stated in the policy, counted by M8.
- **Ledger**: `seal/releases/0.16.0.md` carries 32 rows anchored on the
  five reader and gate files, `seal/ledger.md` 4, and eight earlier release
  files 48 more (counted by grep, executed). Phase 6 removes those whose
  unit goes and writes this item's fragment; rows whose unit survives (the
  dispatcher, the press reader, the tokens) are re-read in place.

## Open questions → questions.md

Four for a person (P1–P4), eleven measurements (M1–M11), six for the work
(W1–W6), and the head of that file lists what this section already decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened. -->

Framed 2026-10-01 by framer, before the build.
