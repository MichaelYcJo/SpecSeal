# Feature Specification: a here-document body is data to the commit gate (#739)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md` §*Only what the shell would EXECUTE is read as commands* | Bodies are already dropped before the walk. That half is untouched: this work changes only the second, separate question — whether a dropped body is read back as commands to find a commit. |
| `docs/commit-review-gate-spec.md`, the paragraph opening **A file edit goes through the `Edit` tool** (`<!-- specs/1788184145-… -->`) | States the rule this work changes ("whether the command commits at all is asked of every body separately, as shell, on purpose") and gives the decision to the owner: "Skipping a body that is only being written to a file would reopen #75, and that trade is the repository owner's to make." #739 is the owner's own ticket, and it asks for that trade for the shapes it measured. This paragraph is rewritten to state the new boundary. |
| `docs/commit-review-gate-spec.md`, the paragraph opening **Two readings that prompted that run stay as they are** | Records that work item `1790635415` narrowed the body reading to "a body fed to a known interpreter is data", and that rounds 2 and 3 found five silent shapes a real bash ran. The narrowing here is the opposite construction: a closed list of consumers that are data, with everything unlisted read as it is today. Every one of those shapes must still stop (acceptance S9). The paragraph is updated so it no longer says the body reading stands unchanged. |
| `docs/commit-review-gate-spec.md`, the paragraph opening **What stays unread is a program whose operands are a script** | `bash run.sh`, `source` and `make` are unread today. That is why a Python program read from stdin counts as data here: it is the same class as `python3 script.py`. It is also why a file written on the line must not be runnable by anything else on the line (R2f, R2c). |
| `docs/the-commit-gate-inside-git.md` §*The commit gate inside git*, the **plain** paragraph (`hooks/tokens.py#is_plain`) | Owner's answer P7 of 2026-10-02: after three rounds each found words a list missed, plain became a *positive* shape. The line shape in R2c is built the same way and reuses the same sets (`PLAIN_PROGRAMS`, `PLAIN_GIT`, `PLAIN_CONFIG`, `steps_around_hooks`). `is_plain` itself does not change. |
| `hooks/cmdline_base.py`, the RIDER at its head | The frozen reader. The worktree guard's switch and creation arms and the consent writer read through it. NEVER edited (`tests/test_the_frozen_reading_never_grows.py`). |
| `tests/test_no_shape_the_base_stops_reads_silent.py`, module docstring | The owner's constraint for work item `1790644505`: no shape `release/v0.16.0` stops may read silent. Every row of its corpus keeps stopping except ONE, which this work moves on the authority of #739 (acceptance S10, `questions.md` Q1). |
| `tests/test_gate_judges_the_repo_it_commits_to.py::test_an_interpreter_fed_heredoc_body_that_commits_stops`, docstring | Legacy #75 rejected "the interpreter enumeration": a list of shells that run a body, with everything else treated as data. That fails open on any shell the list misses. This work does not enumerate shells. It enumerates the few consumers that are provably data. An unlisted consumer, including every shell, keeps today's reading. |
| `skills/agent-contract/SKILL.md` §9 | Says "The gate reads a heredoc body as shell, on purpose". It is what every agent is told, so it changes with the rule (contract §14). |
| `CLAUDE.md` §*The goal a design is chosen against* | Unattended verification is the first goal. Each of #739's refusals cost an orchestrator the whole Bash call. |

## Scope

**In.**

1. In `hooks/commit-review-gate.py#commit_invocations`, the top-level reading of heredoc bodies (the loop over `heredoc_bodies(drop_comments(command))`) reads a body as commands only when rule R below does not make it data.
2. `hooks/cmdline.py` reports, per body, what R needs: whether its delimiter was quoted, whether its terminator arrived, and which opener it belongs to. `drop_heredoc_bodies` and `heredoc_bodies` keep their exact outputs and signatures. Their other callers are `hooks/tokens.py#is_plain`, `hooks/worktree-guard.py` through `wide`, `hooks/worktree_consent.py` and `hooks/implementer-notice.py`, and none of them changes.
3. The policy text and the contract text named in Grounding are rewritten to state R, each paragraph with an `Enforced by:` line naming the new cases.
4. Tests that pin R in both directions (acceptance below), each seen red first (contract §15).
5. The one corpus row named in S10 moves out of the must-stop corpus.

**Out, and why.**

- **Unquoted delimiters** (`<<EOF`). The outer shell expands `$( … )` and backticks inside the body, so a precise reading needs a body scanner with heredoc quoting rules: quotes are literal there, and `substitution_bodies` treats `'…'` as text, so reusing it would fail open. #739's own checkbox scopes data to the quoted delimiter ("with a quoted delimiter nothing in it expands"). Unquoted bodies keep today's reading whole, so `tests/test_no_shape_the_base_stops_reads_silent.py`'s "r3: control, genuinely data" row (`python3 - <<EOF#x`) keeps stopping. Nobody owns a follow-up for it yet. The orchestrator files one if it wants one.
- **Bodies anywhere but the top level**: inside `$( … )`, backticks, `<( … )`, `>( … )`, an `eval` argument, a host's `-c` string, or a body that is itself read as commands. The value of a substitution goes wherever its enclosing command sends it, and the inner reading cannot see where. Examples: `bash <<<"$(cat <<'EOF' … )"`, `source /dev/stdin <<<"$(cat <<'EOF' … )"`. Each runs the body, and today each stops. Every recursive call (`_reads_a_commit` → `heredoc_bodies(text)`) keeps today's reading. So the `git commit -m "$(cat <<'EOF' … EOF)"` false stop that a message mentioning a commit causes is NOT fixed here.
- **Interpreters other than `python3`/`python`** (`node -`, `perl -`, `ruby -`). Nothing measured them. Each would widen the set reviewers must break.
- **The worktree guard.** It already treats every body as data: `_judgment_text` drops bodies and never reads them back. Its switch and creation arms read through the frozen `cmdline_base.py`. Nothing in it changes. Read but not acted on: the guard therefore never sees a `git switch` inside `bash <<'EOF'`. That is a guard-side gap in the frozen reader, and only the owner may reopen it (`cmdline_base.py`'s RIDER).
- **`hooks/tokens.py#is_plain`.** Its heredoc clause decides whether the reading stands aside where git decides, and it is the owner's P7 rule. Not touched.
- **`hooks/cmdline_base.py`**: frozen, never edited.

## The rule (R)

**R1 — where it applies.** Only the top-level loop in `commit_invocations`, for bodies `_heredoc_split` removed from the command the gate was handed. Every other reading is today's.

**R2 — a body is DATA when all of a–f hold.** Where any fails, the body is read as commands exactly as today.

- **a. Quoted delimiter, and every delimiter on the line quoted.** The delimiter word as written contains `'` or `"`, and contains no `$`, backslash, newline or backtick. `<<'EOF'`, `<<"EOF"`, `<<E'O'F` and `<<-'EOF'` qualify. `<<EOF`, `<<-EOF`, `<<\EOF`, `<<$'EOF'` and `<<$"EOF"` do not. Every other heredoc on the line must qualify too, or no body on the line is data: the outer shell expands a body behind an unquoted delimiter, and that body can run a file another body was written to (round 2, the owner's structural rule). The exclusions are fail-closed: what bash makes of `$'…'` as a delimiter is not settled here, and a backslash-newline is removed before the shell reads the word, so where a backslash stands the reader cannot be sure which parts the shell saw quoted (#763). *Rewritten 2026-10-04 by the build after rounds 2 and 3, to state the rule as built; the frame's version admitted `\` and judged each body alone.*
- **b. Terminated.** The body's delimiter line arrived. An unterminated body keeps today's reading, so `test_a_heredoc_that_never_terminates_swallows_the_rest` stays as it is. A reader whose delimiter differs from bash's shows up as an unterminated body, which is round 3's `#`-glued family, so this clause also closes that family's direction.
- **c. Line shape (positive, `is_plain`'s construction).** This clause reads the command with comments and bodies dropped. It must:
  - split cleanly;
  - hold no `$(`, backtick, `$((`, `$[`, `${`, `<(`, `>(`;
  - hold no `(`, `)`, `{`, `}` outside quotes;
  - hold no `&` except inside `&&` and inside a `>&` or `<&` whose target is a digit or `-`;
  - make `steps_around_hooks` false.

  Every simple command's program is a bare literal word, with no assignment prefix, no wrapper, no path and no quoting, drawn from `PLAIN_PROGRAMS ∪ {tee, gh, python3, python}`. Further:
  - each `git` passes `is_plain`'s git rule: only `-C` and a `-c` of a `PLAIN_CONFIG` key before a `PLAIN_GIT` subcommand;
  - each `gh` has as its next word one of `pr`, `issue`, `release`, `api`;
  - each `python3` or `python` is a consumer that satisfies R2e;
  - plain parameter expansions (`$NAME`, `"$NAME"`) may stand in argument positions and in no program position.
- **d. Ownership is certain.** The scan in (c) sees exactly as many heredoc openers as `_heredoc_split` removed bodies. Every opener is on the default descriptor, with no digit or `{name}` before the `<<`. The k-th opener owns the k-th body. Words after the opener belong to the same simple command (round 2's "words after the `<<` are never read" finding).
- **e. Consumer.** The simple command owning the body is one of:
  - a **sink**, `cat` or `tee`;
  - a **program read from stdin**, `python3` or `python`, where the words after the program name, with redirections skipped, are either none or begin with exactly `-`. Anything else in that first position means the body is input to some other program, which may run it. Examples: `-c`, `-Bc…`, `-m`, a script path, `$X`. That is the shape of round 2's `python3 <<'EOF' -c '…'` finding.
- **f. Nothing on the line can run what a sink wrote.** A sink writes a file when it has an output redirection (`>`, `>>`, `>|`) to anything other than `/dev/null` or a descriptor, or when it is `tee` with an operand. Such a sink's body is data only when the line holds no `python3`/`python` consumer and no `git … commit` segment. A Python program can run that file. A commit runs hooks, and the file may be one. The rule names no file-name pattern, because a list of hook paths is the kind of enumeration that rots. *As built (2026-10-04, after rounds 1–3 and #763): any `git` and any `gh` but `pr ready` and a `pr edit` given a flag count as runners, any stage of the sink's pipeline that writes counts, and so does a written file whose name is a program the line runs from `PATH`, `git` included where `gh` runs it.*

**R3 — what R changes, and nothing more.** A body R makes data is not read by `_hides_a_commit` at all. Every other body is read exactly as now, and so are the segments outside the bodies. A real commit before or after a data body is judged as today (#739's third row).

## Shapes, enumerated by construction

The axes are those of R. A cell is its verdict alone, and "stops" means a commit-bearing body keeps today's reading.

| Axis | Values, each a case | Verdict |
|---|---|---|
| Delimiter | `'D'` · `"D"` · `D'x'` (partly quoted) | can be data |
| | `D` · `\D` · `$'D'` · `$"D"` · a backslash-newline anywhere in the word | today's reading |
| Operator | `<<` · `<<-` (tab-stripped body and terminator) | same verdict for both |
| Terminator | arrives · never arrives | data possible · today's reading |
| Consumer | `cat`, `tee` | data (subject to f) |
| | `python3 -`, `python3`, `python -` with argv after `-` | data |
| | `python3 -c …`, `python3 -Bc…`, `python3 <<'D' -c …`, `python3 x.py`, `python3 $X` | today's reading |
| | `bash`, `sh`, every `SHELLS` word, `source`, `.`, `eval`, `exec`, `perl`, `node`, `ssh`, `at`, `xargs`, any unlisted word | today's reading |
| | `sudo cat`, `env cat`, `command cat`, `/bin/cat`, `\cat`, `'cat'`, `X=1 cat` | today's reading |
| | a loop, `if`, `{ …; }`, `( … )`, a function | today's reading |
| Heredocs per line | one · two on one command (`cat <<'A' <<'B'`) · two on two commands · mixed quoting | each body judged on its own; any count mismatch → all today's |
| Descriptor | default · `0<<`, `3<<`, `{fd}<<` | data possible · today's reading |
| Pipeline | `cat <<'D' \| grep x` (every stage allowed) · `cat <<'D' \| sh` · `\| python3 …` | data · today's · today's |
| Output | none · `>/dev/null` · `>&2` · `> f` | data · data · data · data subject to f |
| | `>(…)` · `>&python3` (round 2) · `exec 3> >(bash)` earlier | today's (c) |
| Same line | `gh pr edit --body-file f` · `git -C /abs add/commit` · `cd` · `echo` | allowed |
| | `bash f` · `./f` · `source f` · `make` · `gh alias import f` · `git -c alias.x=… x` | today's (c) |
| | a sink writing `f`, then `git commit` · then `python3 -` | sink body today's (f) |
| Position | top level · inside `"$(…)"`, `` `…` ``, `<(…)`, `eval '…'`, `sh -c '…'`, a shell-run body | data possible · today's (R1) |

## User scenarios & acceptance *(mandatory)*

Every "silent" scenario is run through the gate's `main()`, in an opted-in repository whose session directory carries no declaration, with no git hooks installed. That puts it in the state where the PreToolUse reading judges. Every "stops" scenario asserts the decision is not silence.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — #739 row 2 | Given `cat > pr.md <<'EOF'` whose body quotes `` `git -C /x commit -m y` `` and a line `git commit -m x`, then `EOF; gh pr edit 1 --body-file pr.md; gh pr ready 1`. When the gate reads it, then it is silent. | new case in the gate's test module; red at `101f9bd0` |
| S2 — #739 row 1 | Given `python3 - <<'EOF'` appending to a file, the body holding `` `git commit` `` in a string and a line `# then git commit -m x`. When read, then silent. | new case; red at `101f9bd0` |
| S3 — #739 row 3 | Given `python3 - "$F" <<'EOF' … EOF && git -C <declared abs> add f && git -C <declared abs> commit -m x`, with the body mentioning a commit. When read, then the one real commit is judged against `<declared abs>` and is silent there. The same command with an undeclared `<abs>` stops for that repository and NOT with the unplaceable-construct text. | new case; `commit_invocations` returns exactly one invocation, based at `<abs>` |
| S4 — `<<-` and the other quotings | Given S1's command with each of `<<-'EOF'` (tab-indented body and terminator), `<<"EOF"`, `<<E'O'F`. Then silent. (`<<\EOF` was here and moved to S5's reading in #763.) | parametrised case |
| S5 — unquoted stays read | Given S1 and S2 with `<<EOF` and `<<$'EOF'`. Then each stops as today. | parametrised case; green at `101f9bd0` and after |
| S6 — a shell consumer stays read | Given each of `bash <<'EOF'`, `sh -s <<'EOF'`, `cat <<'EOF' \| sh`, `cat <<'EOF' \| bash -s`, `source /dev/stdin <<'EOF'`, `sudo bash <<'EOF'`, `env cat <<'EOF'`, `/bin/cat <<'EOF'`, `$SH <<'EOF'`, `perl - <<'EOF'`, each with body `git commit -m x`. Then each stops. | parametrised case; each green before and after |
| S7 — a written file a line could run | Given `cat > f.sh <<'EOF'\ngit commit -m x\nEOF\n` followed by, in turn, `bash f.sh`, `sh f.sh`, `./f.sh`, `source f.sh`, `make`, `python3 - <<'P'\nimport os; os.system('sh f.sh')\nP`, `git commit -m y`. Then each stops. | parametrised case |
| S8 — not top level | Given `bash <<<"$(cat <<'EOF'\ngit commit -m x\nEOF\n)"`, `source <(cat <<'EOF'\ngit commit -m x\nEOF\n)`, `eval "$(cat <<'EOF'\ngit commit -m x\nEOF\n)"`, `bash <<'O'\ncat > f <<'I'\ngit commit -m x\nI\nbash f\nO`. Then each stops. | parametrised case |
| S9 — every row of #665's rounds still stops | `tests/test_no_shape_the_base_stops_reads_silent.py`'s r2 and r3 rows, the `>&python3` row included, stay in the corpus and stay non-silent with and without the press. | that module, run narrow |
| S10 — the one corpus row that moves | "measured: a patch whose body loops over a commit string" (`cd <w> && python3 - <<'EOF'` with a quoted delimiter, Python text only) moves out of the must-stop corpus into a case asserting it is silent. The module docstring says why: #739 is the owner's later, narrower decision for exactly this shape, and the 1790644505 constraint was stated "for the work". | the moved case; the docstring change; `questions.md` Q1 |
| S11 — nothing else moves | `drop_heredoc_bodies` and `heredoc_bodies` return what they returned at `101f9bd0` for every string in the existing reader tests. The worktree guard's, the consent writer's and `is_plain`'s cases are untouched and green. `cmdline_base.py` is byte-identical. | `tests/test_what_the_reader_understands.py`, `tests/test_the_frozen_reading_never_grows.py`, `tests/test_the_commit_gate_decides_at_the_commit.py`, run narrow |
| S12 — the words a person reads | The two `commit-review-gate-spec.md` paragraphs and contract §9 state R in prose a reader can apply without opening code. Each carries an `Enforced by:` line naming S1–S8's cases. | `tests/test_edits_go_through_the_edit_tool.py`, the docs line-wrap and one-word tests, run narrow |

## Data & interfaces

- `hooks/cmdline.py`: one new public function, named by the smith, returning per body `(text, quoted, terminated)` in delimiter order. It comes from the same single pass `_heredoc_split` makes, with `_heredoc_word` reporting whether it met a quoting character. `drop_heredoc_bodies` and `heredoc_bodies` become thin views over it, with byte-identical results.
- The R2c/d/e/f shape check is one function. It sits beside `is_plain` in `hooks/tokens.py` and reuses its sets and its lexer settings, or in `cmdline.py` if the import order forces it. Either way it does not change `is_plain`'s output.
- `hooks/commit-review-gate.py#commit_invocations`: its body loop iterates only the bodies R leaves as commands. `_reads_a_commit`'s own recursion is unchanged (R1).
- No new file I/O in hooks. Any file a new test writes names `encoding="utf-8"` (sibling #741 lands an encoding check first).
- Ledger rows citing `_heredoc_split`, `heredoc_bodies`, `_reads_a_commit` and `commit_invocations` sit in released files, which are frozen from `1790993141` per `seal/config.md`. Their re-reads go into `seal/ledger/1791076831-a-here-document-body-is-data-to-the-commit-gate.md` through `evidence-check --reverify --into`.

## Open questions → questions.md

Q1 (the S10 corpus row) and Q2 (python in scope at all) were decided by the framer from #739 and precedence, and they are listed there with what overturning each costs.

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

Framed 2026-10-04 by framer, before the build.
