# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — review round 1

| Field | Value |
|---|---|
| Target SHA | 07a3dc7f0344b3fe4bb55fbd180f84638da095f1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 733 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `25e5b01ac4a3c368b60659f5a1f21e89bbe8af23..2f4e993325fb68b5b4e25f8ed162008e59a60bd7`, 10 commits |
| Contract changes | reparsed_texts → command_strings, reparsed_texts, _string_hides_a_commit, round-1-report.md, round-1.md, round-3-report.md, round-3.md, plan.md, spec.md, pytest; wider_only_kinds → main, round-1-report.md, round-1.md, pytest |
| New units | ENV_VALUED (depth 1); ENV_VALUED_LONG (depth 1); _env_takes_next (depth 1); _env_split_at (depth 1); test_a_restore_before_a_hidden_switch_does_not_silence_the_question (depth 1); test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it (depth 1); test_a_hidden_switch_behind_a_judged_one_adds_no_question (depth 1); test_a_hidden_creation_behind_a_judged_one_adds_no_question (depth 1); test_a_wider_reader_that_exits_at_load_costs_only_the_question (depth 1) |
| Needs a fix | yes — 🟡 1 (env's own words stop no-commit `env -S` commands), 🟡 2 (the `env -S` class misses clusters and abbreviations), 🟡 3 (a restore before a hidden switch silences candidate C) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `07a3dc7f`, over the build's diff `233f0455..07a3dc7f`. It was asked to check the build against `spec.md` and the approved plan (D1–D10), then quality. Six things were named for close checking:
- whether phase 3's count, which decided #686 (A=9) and #678's guard half (C=0) by the owner's rule of 2026-10-03, was honestly produced: same functions, the issues' own shapes firing, this run's probes cut out, and nothing from the corpus but counts and rewritten shapes committed;
- whether candidate C, as wired, keeps the frozen reading's tree and first slot and checks consent first;
- whether the try-wrapped import keeps ACTIVE deny when `cmdline.py` breaks;
- #716's two readings, and whether any shape the gate stopped went silent;
- the frozen gate document's line count and the frozen reader's bytes;
- the ledger corrections and re-reads made in place in `seal/releases/`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `env`'s own words are asked the expansion question and joined unquoted, so `env -S` commands holding no commit now deny, in a declared repository too | `hooks/cmdline.py:1740` | **fixed** `5d2a58f7` | fixed at 5d2a58f7 — `a8dfb388`; executed: five shapes deny at `07a3dc7f`, silent at `233f0455`; the PR's prompt-budget sentence promises otherwise |
| 🟡 2 | the `env -S` class misses a cluster ending in `S` and GNU's `--split-string` prefixes; `env -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1726` | **fixed** `ea53c0a3` | fixed at ea53c0a3; executed: macOS `env -iS` and `-vS` run the string; three commit shapes found by nothing at target and base |
| 🟡 3 | candidate C subtracts the frozen words' kinds, not the loop's verdicts, so a restore before a hidden switch silences the question | `hooks/worktree-guard.py:336` | **fixed** `139bf5e6` | fixed at 139bf5e6 — `cdc05d99`; executed: two shapes silent where the bare hidden switch asks; the per-view fix fires on 0 of 27,351 corpus pairs |
| ⬜ 4 | a hidden creation reads the session clone's consent, not the creation's | `hooks/worktree-guard.py:359` | deferred #734 | #734 — Predates the work item: the base was silent for the same shape; filed as #734; executed: silent into another clone where the plain spelling denies; asks from a non-repo cwd where the plain spelling allows; base silent for both |
| ⬜ 5 | the guarded import catches `Exception` but not `SystemExit` | `hooks/worktree-guard.py:143` | **fixed** `1bbc534b` | fixed at 1bbc534b; read: `hooks/dispatch.py` catches both; no such module body exists today |
| ⬜ 6 | W10's re-read does not test its claim; the new reason is a third exception | `seal/releases/0.15.6.md:17` | answered | corrected at `b32aa5ce`; read; ledger correction, outside `Needs a fix` |
| ⬜ 7 | M1's correction says the verdict kinds are still `86256492`'s | `seal/releases/0.16.0.md:247` | answered | corrected at `b59030bd`; read; ledger correction, outside `Needs a fix` |
| 🟢 | phase 3's count was honestly produced: the built functions reproduce A = 9, C = 0 and every denominator | `phases/phase-3.md` | confirmed | executed re-count with `c7f84438`'s A and the target's C over D1's cut |
| 🟢 | the probe fired on the issues' own shapes before a zero was trusted | `phases/phase-3.md` | confirmed | executed: 7 of 7 for A, 9 of 9 for C |
| 🟢 | D1's cut excludes this run's own commands, and the corpus is complete for the machine | `questions.md` D1 | confirmed | executed: cut equals `5c8a49f7`'s time; the other SpecSeal project directory holds 0 transcripts |
| 🟢 | nothing from the corpus but counts and rewritten shapes reached a committed file | `233f0455..07a3dc7f` | confirmed | executed grep over the added lines |
| 🟢 | phase 4 followed the count: A removed and named a limit, C wired | `docs/worktree-guard-spec.md` | confirmed | read; the `UNPLACED` pins and the `WIDER_ONLY` cases passed (executed) |
| 🟢 | candidate C takes no tree or first slot, and `WIDER_FIRST` still denies | `hooks/worktree-guard.py` main | confirmed | read; the guard module passed at the target (executed) |
| 🟢 | a broken `hooks/cmdline.py` that raises leaves the ACTIVE deny in force | `hooks/worktree-guard.py:141` | confirmed | read; the broken-shared-module case passed (executed) |
| 🟢 | `env -S` is read both ways with redirections, and no added option is one git does not separate | `hooks/cmdline.py` | confirmed | executed on git 2.54.0 and through the reader |
| 🟢 | no shape the commit gate stopped goes silent | `hooks/cmdline.py` | confirmed | executed: the three swallowed-subcommand shapes commit nothing in git |
| 🟢 | the frozen policy file has no net growth, and the frozen reader is byte-identical | `docs/commit-review-gate-spec.md` | confirmed | executed: 1047 lines, 19 markers identical; `hooks/cmdline_base.py` no diff |
| 🟢 | the I9, M2, M3 and M4 corrections and 16 of the 17 re-reads hold against the edit | `seal/releases/0.16.0.md` | confirmed | read row by row; W10 and M1 are ⬜ 6 and ⬜ 7 |

## Paste-ready fixes

```python
# hooks/cmdline.py

def reparsed_texts(tokens, env_words=True):
    # (body as now; the env arm is replaced by 🟡 2's fence, which carries
    # the `if env_words:` guard on every `_env_words` call)
    ...


def _env_words(word, before, after):
    # (docstring as now)
    after = _without_redirections(after)
    if not after:
        return []
    # Only the string is split again; every other word reached `env` as ONE
    # argument, so it is quoted back into one (`env -S echo 'a && b'` runs
    # `echo` with one operand, not a list).
    head = [shlex.quote(w) for w in _without_redirections(before)]
    tail = [shlex.quote(w) for w in after[1:]]
    return [" ".join([word, *head, after[0], *tail])]


# in command_strings, the env arm:
        elif word in ("env", "genv"):
            # The split string alone: `env`'s own words carry its options'
            # values and the operands after the string, which `env` runs as
            # arguments and never as a command word (round 1 of 1790993140).
            out += reparsed_texts([tok, *rest], env_words=False)
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, CONTROLS
    # Round 1 of 1790993140: env's own words are arguments to `env`, so a
    # variable among them names no command, and a quoted operand stays one
    # word. Each was a deny in a declared repository at `07a3dc7f`.
    "env -S behind an option's variable value": "env -u \"$V\" -S 'echo hi'",
    "env -S behind a variable directory": "env -C \"$D\" -S 'echo hi'",
    "env -S with a variable operand": "env -S 'echo' \"$X\"",
    "env -S with a quoted operand holding a list": "env -S 'echo' 'a && git commit -m y'",
```
```python
# hooks/cmdline.py, the env arm of reparsed_texts
        elif word in ("env", "genv"):
            # OWN: still among env's own options, where a cluster or an
            # abbreviation can spell the split string. The base spellings are
            # read anywhere, as they always were.
            own, value = True, False
            for j, t in enumerate(rest):
                at = _env_split_at(t, own and not value)
                if value:
                    value = False
                elif own and not t.startswith("-"):
                    own = False
                elif own:
                    value = _env_takes_next(t) or (at is not None and at[0] == "next")
                if at is None:
                    continue
                kind, string = at
                if kind == "next" and j + 1 < len(rest):
                    texts += _string_at(rest, j + 1)
                    after = rest[j + 1 :]
                elif kind == "here":
                    texts.append(string)
                    after = [string, *rest[j + 1 :]]
                else:
                    continue
                if env_words:
                    texts += _env_words(word, rest[:j], after)
    return texts


# `env`'s options other than `-S` that take a value, in GNU coreutils and
# BSD/macOS: the rest of the cluster, or the next word where none is left.
ENV_VALUED = frozenset("uCPLa")
ENV_VALUED_LONG = frozenset({"--unset", "--chdir", "--argv0"})


def _env_takes_next(t):
    """True where T is one of `env`'s options whose value is the next word."""
    if t.startswith("--"):
        return t in ENV_VALUED_LONG
    middle = t[1:-1]
    return (
        len(t) > 1
        and t[-1] in ENV_VALUED
        and all(c.isalnum() and c not in ENV_VALUED for c in middle)
    )


def _env_split_at(t, own):
    """Where T spells `env`'s split string (#716), or None.

    ("next", None) where the string is the next word, ("here", s) where T
    carries it. `-S`, `-S<s>` and `--split-string[=<s>]` anywhere, as the
    base read them. Among env's own options (OWN) also a cluster ending in it
    (`-iS`, `-vS<s>`, which macOS `env` and GNU's getopt both accept) and
    every prefix of `--split-string` GNU's getopt takes, from `--s`: no other
    long option of GNU `env` starts with `s`.
    """
    if t in ("-S", "--split-string"):
        return ("next", None)
    if t.startswith("--split-string="):
        return ("here", t.split("=", 1)[1])
    if t.startswith("-S") and len(t) > 2:
        return ("here", t[2:])
    if not own:
        return None
    if t.startswith("--"):
        name, eq, value = t.partition("=")
        if name.startswith("--s") and "--split-string".startswith(name):
            return ("here", value) if eq else ("next", None)
        return None
    if not t.startswith("-") or len(t) < 2:
        return None
    for i, ch in enumerate(t[1:], 1):
        if ch == "S":
            string = t[i + 1 :]
            return ("here", string) if string else ("next", None)
        if ch in ENV_VALUED or not ch.isalnum():
            return None
    return None
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, HANDED
    # Round 1 of 1790993140: a cluster ending in `S`, which macOS `env`
    # accepts, and GNU's abbreviation of `--split-string`. Each found nothing
    # at `07a3dc7f`.
    "env -iS, a cluster": f"env -iS '{C}'",
    "env -vS, a cluster carrying env's own words": f"env -vS '-i {C}'",
    "env -iS glued": f"env -iS'{C}'",
    "env --split, abbreviated": f"env --split '-i {C}'",
    "env --split=, abbreviated": f"env --split='-i {C}'",
    "env -iS behind an option's value": f"env -u FOO -iS '{C}'",

# ... and in CONTROLS:
    # A cluster ending in `S` after the program is the program's (`ls -lS`).
    "a program's own cluster ending in S": "env ls -lS \"$DIR\"",
```
```python
# hooks/worktree-guard.py
def wider_only_kinds(command: str, cwd: str, judged=None) -> set:
    # (docstring as now; replace its last sentence of the first paragraph with:
    # "A kind the frozen loop judged keeps its slot and its verdict, and a
    # view the frozen parser reads as the same kind is not hidden from it,
    # so neither is reported." JUDGED defaults to the kinds the frozen
    # segments' words hold, which is what the unit cases ask.)
    if wide is None:
        return set()
    if judged is None:
        judged = {
            switch_kind(parse_git(tokens))
            for tokens, _wheres in walk_command(command, cwd)
        }
    text = wide.drop_heredoc_bodies(wide.drop_comments(command))
    segments, _clean = wide.split_segments(text)
    views = [*segments, *wide.merged_segments(text)]
    wider = set()
    for tokens in [*views, *filter(None, map(wide.unglued, views))]:
        kind = switch_kind(wide.parse_git(tokens))
        # A view the frozen reader reads as the same kind is not hidden from
        # it: `git checkout README.md` is a restore to `classify`, and must
        # not silence a switch written behind a redirection after it.
        if kind and switch_kind(parse_git(tokens)) != kind:
            wider.add(kind)
    return wider - set(judged)


# in main, quiet():
    def quiet():
        judged = {"switch"} if switch_reason is not None else set()
        if creation_at is not None:
            judged.add("creation")
        hidden = wider_only_kinds(command, cwd, judged)
        ask_what_only_the_wider_reading_finds(hidden, cwd, session_id, transcript_path)
        sys.exit(0)
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py
def test_a_restore_before_a_hidden_switch_does_not_silence_the_question(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of 1790993140. `classify` reads `git checkout README.md` as a
    restore, so the frozen loop judged no switch, and the switch behind the
    redirection is still put to the person. Silent at `07a3dc7f`, where the
    restore's words alone took the switch kind out."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command = f"git checkout README.md && cd w && 2>/dev/null {SWITCH}"
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (decision, reason)
    assert "switches a branch" in reason, reason
    assert top is None, top
```
```markdown
The consent read is the session clone's: the guard cannot place a creation
only the wider reading finds, so a hidden creation into another clone is
silent under this clone's consent, and one reached through `git -C` from a
directory in no repository is asked although its clone has consent.
```
```python
# hooks/worktree-guard.py
try:
    import cmdline as wide
except (Exception, SystemExit):
    wide = None
```
```markdown
**Corrected 2026-10-03** by work item 1790993140 (#678): a third command names
no tree. The question about a switch or creation only the commit gate's
reading finds tells the person to re-issue it as `git switch …` or
`git worktree add …`, with `git -C <dir>` as a placeholder, because the guard
could not place it.
```
```markdown
**Corrected 2026-10-03** by work item 1790993140 (#678): *never through
`hooks/cmdline.py`* no longer holds for the guard. It imports that module as
`wide`, guarded, and at an exit where it was about to say nothing it reads that
module's segments with that module's `parse_git` (`wider_only_kinds`) and asks
about a switch or creation only that reading finds. The tree it judges, each
segment's directories, every verdict the frozen reading earns and the clone
consent is filed under are still `86256492`'s, and the consent writer still
imports only the frozen copy.
```

## Executed probes

| What was run | Result |
|---|---|
| Re-count of phase 3: `c7f84438`'s candidate A and the target's candidate C over D1's corpus and cut | 27,551 uses, 27,351 pairs, 395 switch, 51 creation, A = 9, C = 0, none raised; self-check 7 of 7 and 9 of 9 |
| The per-view subtraction of 🟡 3 over the same 27,351 pairs | fires on 0; 2.6 ms per pair against 6.1 ms for the wired version |
| `git <option> <value> status` on git 2.54.0 for `--attr-source`, `--shallow-file`, `--config-env`, `--namespace`, `--exec-path` | the first four ran `status`; `--exec-path` printed its path and exited |
| `git <new option> commit --allow-empty -m x` for the three added options | exit 129, 129, 128; no commit |
| macOS `env -iS`, `env -vS`, `env --split-string=` | the two clusters ran the string; `--split-string` is GNU's alone (`illegal option`) |
| `env -S` shapes through `commit_invocations` at target and base | redirection shapes found at the target only; clusters and the abbreviation found at neither |
| Five `env -S` controls through `main()` in a declared repository, target and base | deny at the target, silent at the base |
| Guard probe: a restore or a no-ref checkout before a hidden switch | silent; the bare hidden switch asks |
| Guard probe: consent for the session's clone with a hidden creation elsewhere | silent into another clone (plain spelling denies); ask from a non-repo cwd (plain spelling allows) |
| Corpus count of `env` split strings and spaced added options | 0 of 27,351 |
| Narrow run at the target: the guard module, the wrapper module, the frozen-reading module, the broken-shared-module case, the commit-gate-decides module | 955 passed, 72 skipped |
| The three 🟡 fences applied in the clone, then the guard, wrapper and frozen-reading modules and the broken-shared-module case | 706 passed; ruff check and format clean on the four files |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet: the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
