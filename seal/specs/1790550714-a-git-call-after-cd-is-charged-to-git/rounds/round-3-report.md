# Review round 3 — `fix/377-a-git-call-after-cd-is-charged-to-git`

Target SHA `af1e263e1cb62e44cd9676f27e2afbe6595c2e4d`, base
`origin/release/v0.15.6`. This is the verifying round and the run's last
round: the one reopening was spent at round 2. Its target is round 2's fix
range, `f12b995620c6930be7b5b86957e05ca18cc8e4cd..807e2ccd902aa98040fd3010168d2f6509e2b60a`
(9c0520f, a654a35, 807e2cc), and not the branch. `af1e263` changes only
`round-2.md`, so the code at the target is 807e2cc's.

I reviewed in a `git clone --no-local` at the target under this round's
scratchpad directory, since deleted. I compared three copies of
`skills/verify/scripts/session_cost.py`: 2037cf0's (the base rule, fed the
flattened command as its `load` did), ee72397's (round 2's target) and the
target's. Every shape named below went through all three, and every shape
whose answer was in doubt went through bash itself.

How the findings relate:

```
round 2's fixes
  ├ quoted or escaped operator characters become a letter          closed   (executed)
  ├ an operator token is walked a character at a time              closed   (executed)
  ├ `\⏎` is removed as bash removes it
  │    in the text the walk reads                                  closed   (executed)
  │    ① but not in the heredoc pass, which runs first:
  │      an unquoted heredoc's body line ending in `\` joins
  │      the delimiter line in bash, and here closes the body       (🟡, worse than 2037cf0)
  ├ the HEREDOC here-string sentence, COMMENT_AFTER's pins,
  │  the changelog's long line                                     closed   (executed / read)
  └ the answers to round 2's findings 6 and 7 (bounds)
       the bounds stand, and each answers as stated for its own shape
       ② "neither worse than the rule before #377" is false as a class:
         each bound also reads a `git` that bash does not run       (🟡, worse than 2037cf0)
       ③ overview.md repeats the claim                              (⬜, correction)
       ④ ledger N2 carries the same claim for a refused line        (⬜, correction)
```

Neither 🟡 moves a corpus call. Findings 1 and 2 are about shapes the
branch reads worse than the rule before #377, and about sentences that say
no such shape exists.

## Round 2's verdicts

### Finding 1 (quoted or escaped operators): closed as a class

Executed. Every separator shape the prompt named reads as bash reads it at
the target: `echo "a"; git x`, `'a'&&git x`, `"\""; git x`,
`echo "a\\"; git x`, `echo 'a\'; git x`, `echo \\; git x`,
`echo "a\⏎b"; git x` and `echo 'a\⏎b'; git x` all read `git`, and
`echo "a\⏎; git x"` and `echo 'a\⏎; git x'` read `other`. bash confirms
that `\⏎` is removed inside double quotes and kept inside single quotes, and
`without_comments` does the same.

Read. The neutralising cannot hide a separator the tokeniser saw before it,
because `without_comments` tracks quotes with the same parity as `shlex`: a
backslash escapes the next character outside quotes and inside double
quotes, and is literal inside single quotes, in both. A region the walk
neutralises was already a quoted region to the tokeniser at ee72397.

`$'\''; git x` reads `other` where bash reads `git`. ANSI-C quoting is not
modelled, so the walk sees an unmatched `'` and the tokeniser refuses the
line before its first word. The anchored pattern then answers `other`, as
it does at ee72397 and 2037cf0. This is `runs_git`'s stated refusal bound,
not a new shape.

### Finding 2 (a token that closes and opens): closed as a class

Executed. `&&`, `||`, `|&`, `;;`, `>>`, `2>&1`, `&>` and a `case` arm's `;;`
before a later `git` read `git`. `ls >(git x)`, `ls>(git x)` and
`ls;>(git x)` read `other`. `x=$(ls)||(git x)` reads `other` at ee72397 and
`git` at the target, which is bash's reading. `x=$(ls <(git a))&&git x`
reads `git`, and `x=$(ls <(git a)); ls` reads `other`.

Read. `token[at - 1 : at]` at `at == 0` is the empty string, so the walk
never reads the token's last character as the one before its first. The
counter only decreases while it is above zero, so dropping `max(0, …)`
cannot make it negative. a654a35's pins hold: `echo a;<(git s)` reads
`other` and `diff <(ls a)<(ls b); git s` reads `git`.

### Finding 3 (`\⏎`): closed where `without_comments` reads, open in the heredoc pass

Executed. `ls \⏎# x; git push` reads `other` and `cd /x && \⏎git status`
reads `git`. A comment's `\` does not continue it (`# a \⏎git push` keeps
its second line), and `\\⏎` is an escaped backslash and a real newline. The
code gets both right. The one corpus call round 2 said would move does move,
`other` → `git`. The heredoc half is finding 1 below.

### Finding 4 (the here-string sentence): closed

Executed. `cat <<< "$x"⏎git push` reads `other`. Read: the pattern fails at
the first `<` and matches from the second with `"$x"` as a quoted delimiter,
as the comment says. `cat <<< $x⏎git push` does not match at all and reads
`git`, which is bash's reading. The comment names the quoted shape only, so
it stays true.

### Finding 5 (`COMMENT_AFTER`'s pins): closed

Executed. Removing each of the eight characters in turn from
`COMMENT_AFTER` fails `test_a_comment_runs_nothing_whatever_it_holds`, one
failure per mutant. The file was restored byte for byte, and the clone was
clean afterwards.

### Findings 6 and 7 (answered as bounds): the bounds stand, and the sentence about them does not

Executed. Each shape round 2 answered still answers as its bound says:
`echo $(ls)#x; git s`, `x="$(git log --format="%h # %s")"; git push` and
`ls # see <<EOF⏎git push` read `other` at all three copies. The claim
written beside them is that neither bound is worse than the rule before
#377. It holds for the direction round 2 probed, a `git` lost, and fails for
the other direction. That is finding 2 below.

### Finding 8 (the changelog's long line): closed

Read. Line 12's 107 characters are re-wrapped. Round 2's record says "at
most 77 characters", but line 8 is 79, which is older than the fix, and
line 26 is 78. Both are near the file's wrap, so nothing needs changing.

## Findings

### 🟡 1 — a heredoc body line ending in `\` closes the body where bash does not

`skills/verify/scripts/session_cost.py:237`, in `without_heredoc_bodies`.

bash removes `\⏎` inside an unquoted heredoc's body before it compares a
line with the delimiter. So in `cat <<EOF⏎body \⏎EOF⏎git push`, the first
`EOF` is joined onto `body ` and closes nothing, and `git push` is body. I
confirmed this with bash: the line after the joined `EOF` printed as body,
and only the second `EOF` closed it. `without_heredoc_bodies` compares each
physical line, so it closes at the first `EOF` and reads `git push` as a
command.

| shape | bash | 2037cf0 | ee72397 | target |
|---|---|---|---|---|
| `cat <<EOF⏎body \⏎EOF⏎git push` | not `git` | `other` | `git` | `git` |
| `cat <<EOF⏎body \⏎EOF⏎git push⏎EOF` | not `git` | `other` | `git` | `git` |
| `cat <<'EOF'⏎body \⏎EOF⏎git push` | `git` | `other` | `git` | `git` |
| `cat <<EOF \⏎&& git push⏎body⏎EOF` | `git` | `other` | `other` | `other` |

Why it matters:

- The first two rows answer worse than 2037cf0. That is the one direction
  the spec rules out ("never produces an answer worse than the old one").
- Round 2's fix of finding 3 says `\⏎` is read as bash reads it, and the
  changelog fragment says "A line continuation, `\⏎`, joins its two lines,
  as it does in the shell". The heredoc pass runs before `without_comments`
  and does not, so the class round 2 closed is closed in one of the two
  passes that read newlines.

The last row, a continuation on the operator's own line, answers as
2037cf0 did. The body starts one line early and swallows the `&& git push`.
It is not worse than the base, so the fix below leaves it and the `HEREDOC`
comment states it.

Executed: 0 of 22,872 Bash calls in 334 transcripts move under the fix
below. That count excludes this review session's own transcripts, which
hold these probes. Two calls in the corpus hold an uppercase unquoted
heredoc and a `\⏎`, and neither is this shape.

### 🟡 2 — the bounds are described as never worse than the rule before #377, and each can read a `git` bash does not run

`skills/verify/scripts/session_cost.py:284`, in `without_comments`' docstring
("Two bounds, neither worse than the rule before #377"), and
`skills/verify/scripts/session_cost.py:420`, in `runs_git`'s docstring ("an
unmatched quote never answers worse than the old rule did").

Round 2 answered findings 6 and 7 with shapes that lose a `git`. The rule
before #377 already read `other` for those, so it could not be beaten there.
The same misreadings also create a `git` bash does not run. The rule before
#377 read `other` there, and it was right:

| shape | bash | 2037cf0 | ee72397 | target |
|---|---|---|---|---|
| `x="$(echo "; git log")"` | not `git` | `other` | `git` | `git` |
| `x="$(printf "%s && gh pr list" a)"` | not `git` | `other` | `git` | `git` |
| `echo $(ls)#'⏎git push'` | not `git` | `other` | `git` | `git` |
| `ls # n <<EOF⏎echo 'a⏎EOF⏎git push'` | not `git` | `other` | `git` | `git` |

- The first two are the nested-quote bound. The inner `"` closes the outer
  quote, so `; git log` is read as bare text.
- The third is the `)`-inside-a-word bound. `#'` is read as a comment, which
  removes the `'` that opens the quote hiding `git push`. The tokeniser then
  refuses the line at the closing `'` after it has read `git`, so the answer
  comes from the words before the refusal. That is why `runs_git`'s
  sentence about an unmatched quote is false too.
- The fourth is the heredoc-in-comment bound. The body removal takes the
  line holding the opening `'`, and the rest is the same as the third.

None of these was caused by round 2's fixes: all four read the same at
ee72397. The finding is about the sentences 9c0520f wrote, which state as a
class what was measured on one direction. Keeping the bounds needs no
parser. Keeping the sentences true needs them to say which direction
each bound can fail in. The fix is sentence-only, and nothing the tool
prints changes.

Whether a corpus call falls in these shapes is not measured. Telling one
apart needs bash's reading of every call that reads `git`. Unverified; the
orchestrator answers it if the count is wanted.

### ⬜ 3 — `overview.md` repeats the claim as a correction

`seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/overview.md:39`
says the three bounds are kept "because each answers as the rule before
#377 did". The four shapes above do not. This is paperwork, so it is not
counted in `Needs a fix`.

### ⬜ 4 — ledger N2 carries the same claim for a refused line, as a correction

`seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md:13`, N2:
"a line the tokeniser refuses … never answers worse than the anchored
rule". `echo $(ls)#'⏎git push'` is refused and answers `git`, where the
anchored rule answers `other` and bash runs no `git`. The claim holds for a
quote the shell itself leaves unmatched. It does not hold for one the walk
sees unmatched because a comment bound took the quote that opened it. This
is paperwork, so it is not counted in `Needs a fix`.

## The cap

The run is capped, so no further round is spawned. Both 🟡 are reported at
the severity found. As I read `docs/review-chain-spec.md` §*The cap bounds
rounds, and not the fixes of the round it stopped*, the sentences of
finding 2 were written by 9c0520f, one of this run's fixes. They are in
`without_comments`, a unit round 1's fix pass created, so they are the
branch's to fix. Finding 1 is in `without_heredoc_bodies`, a unit from the
implementation phases. The claim it contradicts was written by round 2's
fix. Where it goes is the orchestrator's test to apply, and I left it off
the Deferred table because nothing has been deferred yet.

## Regression tests to plant

In `tests/test_session_cost.py`, inside
`test_a_command_after_a_heredoc_is_read_and_its_body_is_not`, with finding
1's fix. Executed: the first case reads `git` at the target and `other` on
the patched copy, so it is red before the fix. The other three read the same
on both and pin that the fix does not over-reach: a quoted delimiter keeps
its `\`, `\\` is not a continuation, and a joined body still ends at the next
delimiter.

```python
        ("cat > f <<EOF\nbody \\\nEOF\ngit push", "other"),
        ("cat > f <<EOF\nbody \\\nEOF\ngit push\nEOF\ngit add f", "git"),
        ("cat > f <<'EOF'\nbody \\\nEOF\ngit push", "git"),
        ("cat > f <<EOF\nbody \\\\\nEOF\ngit push", "git"),
```

Finding 2 is sentence-only and has no case to plant. The four shapes
above would pin a wrong answer as a bound, which is a decision for the
owner, not a regression.

## Facts for the evidence ledger

- N3's heredoc rule gains a clause under finding 1's fix: an unquoted
  delimiter's body lines are joined across `\⏎` before each is compared with
  the delimiter, and a quoted one's are not.
- N2's claim is narrowed as finding 4 says.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | an unquoted heredoc's body line ending in `\` closes the body at the next delimiter line, where bash joins the two, so `cat <<EOF⏎body \⏎EOF⏎git push` reads `git`; round 2's "`\⏎` as the shell reads it" is not true of the heredoc pass | `skills/verify/scripts/session_cost.py:237` | open | executed: two shapes read `git` at the target and ee72397, `other` at 2037cf0, not `git` in bash; the paste-ready fix reads them `other`, passes 116 cases, and moves 0 of 22,872 corpus calls |
| 🟡 2 | "neither worse than the rule before #377" (`without_comments`) and "an unmatched quote never answers worse than the old rule did" (`runs_git`) are false: each bound also reads a `git` bash does not run | `skills/verify/scripts/session_cost.py:284` | open | executed: four shapes read `git` at the target and ee72397, `other` at 2037cf0, not `git` in bash; round 2's answers to its findings 6 and 7 probed only the direction that loses a `git` |
| ⬜ 3 | `overview.md` §Not done says each bound "answers as the rule before #377 did" | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/overview.md:39` | open | read against finding 2's executed shapes; a correction, not counted in `Needs a fix` |
| ⬜ 4 | ledger N2 says a refused line "never answers worse than the anchored rule"; `echo $(ls)#'⏎git push'` is refused and answers `git` | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md:13` | open | executed: the shape reads `git` at the target, `other` at 2037cf0; a correction, not counted in `Needs a fix` |
| 🟢 | round 2's finding 1 is closed as a class — a quoted or escaped operator character is a letter | `skills/verify/scripts/session_cost.py:307` | confirmed | executed: ten separator shapes through three copies read as bash does; read: the walk's quote parity equals the tokeniser's, so no separator the tokeniser saw is hidden; `$'\''` falls under `runs_git`'s refusal bound and reads as at ee72397 |
| 🟢 | round 2's finding 2 is closed as a class — an operator token is walked a character at a time | `skills/verify/scripts/session_cost.py:370` | confirmed | executed: every multi-character operator and process-substitution shape the prompt named reads as bash does; `x=$(ls)\|\|(git x)` moves `other` → `git` against ee72397 |
| 🟢 | round 2's finding 3 is closed where `without_comments` reads the command | `skills/verify/scripts/session_cost.py:294` | confirmed | executed: `ls \⏎# x; git push` reads `other` and `cd /x && \⏎git status` reads `git`; the heredoc pass is finding 1 |
| 🟢 | round 2's finding 4 is closed — the here-string sentence states the cut | `skills/verify/scripts/session_cost.py:198` | confirmed | executed: `cat <<< "$x"⏎git push` reads `other`; `cat <<< $x⏎git push` reads `git`, outside the sentence's shape |
| 🟢 | round 2's finding 5 is closed — each of `COMMENT_AFTER`'s eight characters is pinned | `tests/test_session_cost.py:1754` | confirmed | executed: eight mutants, one character removed each, each 1 failed; restored |
| 🟢 | round 2's findings 6 and 7 answer as their bounds state for the shapes named | `skills/verify/scripts/session_cost.py:284` | confirmed | executed: three shapes read `other` at all three copies; the sentence around them is finding 2 |
| 🟢 | round 2's finding 8 is closed — the 107-character line is re-wrapped | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md:12` | confirmed | read: lines 8 and 26 are 79 and 78, against the record's "at most 77" |
| 🟢 | the corpus moves as round 2 recorded, and no call goes from `git` to anything else against 2037cf0 | `skills/verify/scripts/session_cost.py:430` | confirmed | executed: ee72397 → target moves 1 call, `other` → `git`, the `git -C` after `&& \⏎`; refused 16 and 16 |
| 🟢 | the ledger has no drifted or broken row | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | confirmed | executed: `bin/evidence-check --strict`, unscoped, at the target, exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q -p no:xdist` at the target | 116 passed, exit 0 |
| 42 command shapes through 2037cf0's (flattened), ee72397's and the target's `family`, each against bash's reading | separators, operators, process substitutions and `\⏎` in quotes read as bash does; 6 shapes answer worse than 2037cf0 (findings 1 and 2); 5 more are wrong as at 2037cf0 (the stated bounds, `$'\''`, the operator-line continuation) |
| the contested shapes through `bash -c` | an unquoted body's `body \⏎EOF` joins and does not close; `cat <<EOF \⏎&& echo RAN` runs `RAN`; `"a\⏎b"` is `ab`; `x="$(echo "; echo FP")"` is a string; the `#'⏎…'` and heredoc-in-comment shapes run nothing |
| `COMMENT_AFTER` with each of its eight characters removed, `-k comment_runs_nothing`, one at a time | each 1 failed; the file restored and the clone clean |
| every Bash call under `~/.claude/projects/*SpecSeal*/`, through all three copies | 351 transcripts, 23,779 calls; ee72397 → target: 1 call, `other` → `git`; 2037cf0 → target: no call leaves `git` except 10 to `test` (the order `FAMILIES` states); refused 16 at ee72397 and at the target |
| finding 1's fix on a copy of the target: the shapes, the corpus and the module | the two worse shapes read `other`; 0 of 22,872 calls in 334 transcripts (this session's excluded) move against the target; the fix copied into the clone, `bin/test tests/test_session_cost.py -q -p no:xdist` 116 passed, then restored with `git checkout` |
| the four planted cases at the target and on the patched copy | the first reads `git` at the target and `other` patched; the other three read the same on both |
| `bin/evidence-check --strict`, unscoped, at the target | exit 0 |
| the orchestrator's four modules giving 205 passed, and ruff clean, at the target | not re-run here beyond `tests/test_session_cost.py`: unverified by this round, and the orchestrator answers it |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet. Nobody has run it. It is the sealer's, and it comes due when the orchestrator settles findings 1 and 2 under the cap |

## Paste-ready fixes

### 🟡 1

`without_heredoc_bodies`, replacing the lines from `tabs = …` to the end of
the `while` loop:

```python
        tabs = operator.startswith("<<-")
        # An unquoted delimiter's body has `\⏎` removed before a line is
        # compared with it, so a body line ending in `\` joins the next one
        # and that line closes nothing. A quoted delimiter keeps the `\`.
        joins = operator[-1] not in "'\""
        body = command.find("\n", opener.end())
        closed = None
        if body != -1:
            at, carried = body + 1, ""
            while at <= len(command):
                end = command.find("\n", at)
                end = len(command) if end == -1 else end
                line = carried + command[at:end]
                trailing = len(line) - len(line.rstrip("\\"))
                if joins and trailing % 2 and end < len(command):
                    carried, at = line[:-1], end + 1
                    continue
                carried = ""
                if (line.lstrip("\t") if tabs else line) == delimiter:
                    closed = end
                    break
                at = end + 1
```

The `HEREDOC` comment, appended after the paragraph that ends "every
command after it.":

```python
#
# A `\⏎` on the operator's own line is not joined here, so the body starts
# one line early and takes the continued line with it:
# `cat <<EOF \⏎&& git push⏎…⏎EOF` is `other`, as it was before #377.
```

### 🟡 2

`without_comments`' docstring, replacing its last paragraph:

```python
    Two bounds. A `)` inside a word starts a word boundary even when it
    closes a substitution (`echo $(ls)#x` reads `#x` as a comment), and
    quotes nested inside `"$( … )"` are read as closing the outer ones.
    Where they lose a `git`, the rule before #377 lost it too. They can also
    read one bash does not run, which that rule did not:
    `x="$(echo "; git log")"` reads its `git`, and so does
    `echo $(ls)#'⏎git push'`, whose `#'` removes the quote hiding it."""
```

`runs_git`'s docstring, the end of the fourth bound:

```python
      first word, `git'x` from the pattern, and a quote the shell leaves
      unmatched never answers worse than the old rule did, and never ends a
      reading. A quote the walk sees unmatched only because a bound in
      `without_comments` removed its opener can: `echo $(ls)#'⏎git push'`
      is `git`."""
```

### ⬜ 3

```text
overview.md §Not done — replace "because each answers as the rule before
#377 did and fixing it needs a parser this file does not have" with:
because where each loses a `git` the rule before #377 lost it too, and
fixing it needs a parser this file does not have. Each can also read a
`git` bash does not run, which `without_comments`' docstring shows
```

### ⬜ 4

```text
N2's clause — replace "never answers worse than the anchored rule" with:
never answers worse than the anchored rule for a quote the shell itself
leaves unmatched
and add a `Corrected 2026-09-28` note naming `echo $(ls)#'⏎git push'`.
```

Needs a fix: yes — findings 1 and 2: an unquoted heredoc's body line
ending in `\` closes the body where bash does not, and two docstrings say
the bounds are never worse than the rule before #377 when four shapes are

Loses a record or crashes: no

## Proof block

Files opened this round, at the target in the clone unless named:

- `skills/verify/scripts/session_cost.py` (lines 170–470, 611–700; and the
  2037cf0 and ee72397 copies)
- `tests/test_session_cost.py` (lines 1671–1712, and the fix diff's hunks)
- `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/rounds/round-2.md`
- `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/rounds/round-2-report.md` (lines 1–40)
- `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/overview.md`
- `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md` (the diff and line widths)
- `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` (N2, and the grep of N1 and N4)
- `bin/test` (its header)
- the diff `f12b995..807e2cc` in full, and `807e2cc..af1e263`'s stat
