# Feature Specification: reading is charged to a `read` family (#642)

<!-- seal/specs/1790562541-reading-is-charged-to-a-read-family/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/measuring-a-run.md` §*What a measurement must survive, and what it must not invent*, the clause *A reading that was published is still wrong after it is published* | the work item that changes a family says which published numbers move. Its `Enforced by` is *nothing — a session's act*, so this spec, the changelog fragment and the `SKILL.md` paragraph carry it out (Data & interfaces, last bullet) |
| `skills/verify/scripts/session_cost.py#analyse`, its docstring: *Changing what the plain reading prints would make every reading this repository has already published incomparable with the next one, with nothing on the page saying so*, and its account *Two rules moved after readings were published* | a new family is a third move of what a family row means. The account is extended in the same commit, and the `--segments` comparability line names #642 |
| `seal/releases/0.9.4.md` S1 and S2 (#200), and #642's own *What must not break* | *wrong in both directions*: a write is never `read`. `cat > f <<'EOF'`, `sed -i` and a redirection into a file stay out. The four existing families keep precedence, so `read` is judged last |
| `seal/releases/0.15.6.md` N1–N4 (#377's segmentation) | `read` is judged by command word through the same walk `runs_git` uses, not by a second tokeniser, so "what is a command" has one answer in this file |
| the owner's answer of 2026-09-28, given in the pre-edit batch (`routing.md` §*Why this way*; `questions.md` Q1) | a `read` family only. A `python3 - <<'EOF'` script is not given a family and stays in `other` |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | the rule covers the class (every shape of a read-only call), every sentence a person reads that changes is pinned in the same commit, and every new case is seen red before it is planted |
| `CLAUDE.md` *a change writes fragments, never the shared file* | changelog in `seal/specs/1790562541-reading-is-charged-to-a-read-family/changelog.md`, new ledger rows in `seal/ledger/1790562541-reading-is-charged-to-a-read-family.md`. A row an edit drifts is re-read in the file it lives in; a row that is false is corrected in place with a `Corrected <date>` note |

## Scope

### What the ticket measured, and what this frame takes from it

#642's table (executed by its author, 2026-09-28, at 2037cf0, which is
before #377; read here, not re-run): 22,822 Bash calls over 343 transcripts,
17,574 charged to `other`, 8,328 of those with a read command as the first
thing run after any `cd`. The ticket calls 8,328 an upper bound, and it is
one for a second reason: "first after `cd`" charges `ls && rm -rf x` and
`grep x f; python3 build.py` to reading. The rule below is stricter, so it
moves fewer calls than 8,328, and the ticket's *toward about 40%* is not an
acceptance criterion here. Phase 3 measures what the rule actually moves
(`questions.md` Q2).

### In

1. **A call is `read` when every command it runs only reads.** Through the
   walk `command_words` already does (the command word is the first word of
   the line, or the first after `&&`, `||`, `;`, `|`, `&`, a newline or a
   subshell's `(`, skipping leading assignments and `RESERVED`), a call is
   `read` when all of the following hold:
   - at least one command word is a **read word**: `sed`, `grep`, `rg`,
     `cat`, `head`, `tail`, `ls`, `find`, `wc`, `awk`, `nl`, `sort`, `diff`,
     which is #642's measured list, by basename;
   - every other command word is a read word or a **neutral word**, one that
     neither touches a file nor writes one: `cd`, `pushd`, `popd`, `pwd`,
     `echo`, `printf`, `true`, `:`, `test`, `[`, `[[`, the `read` builtin,
     and the grammar words the walk yields in command position (`for`,
     `case`, `select`, `done`, `fi`, `esac`, `}`). An assignment-only command
     (`W=/w;`) yields no command word and does not disqualify;
   - no command on the line writes (In §2);
   - nothing on the line is hidden from the walk (In §3).

   `cd /x && sed -n 1,5p f`, `grep -n x f | head -5`,
   `for f in a b; do wc -l $f; done` and `[ -f x ] && cat x` are `read`.
   `./bin/deploy --wait | tail -3`, `cat f | python3 -c …`, `ls; rm x`,
   `sleep 5; tail log`, `cd /x` alone and `echo hi` are not.
2. **A write is never `read`** (#200's second direction). The line is not
   `read` when any command on it:
   - redirects output into anything but `/dev/null` (`>`, `>>`, `>|`, `&>`,
     `N>`), or duplicates onto anything but a descriptor number or `-`
     (`2>&1` and `>&2` are fine);
   - is `sed` with `--in-place`, or with a single-dash option word containing
     `i` (`-i`, `-i.bak`, `-ni`, `-Ei`);
   - is `sort` with `--output` or a single-dash option word containing `o`;
   - is `find` with `-delete`, `-exec`, `-execdir`, `-ok`, `-okdir`,
     `-fprint`, `-fprint0`, `-fprintf` or `-fls`;
   - is `awk` with an option word beginning `-i` or `--include`
     (`awk -i inplace`).

   A single-dash cluster is read wholesale, so `sed -es/a/i/ f` is not
   `read` either. That direction, a read charged to `other`, is the smaller
   error, and it is the one every funnel in this file already takes.
3. **What the walk cannot see is not `read`.** The line is not `read` when
   it holds a heredoc or here-string operator (any `<<` token, so
   `cat > f <<'EOF'` is out twice over and `cat <<'EOF'⏎text⏎EOF` is out
   too, since it prints a document rather than reading a file), a command or
   process substitution (`$(`, `` ` ``, `<(`, `>(`, and `$((` with them), or
   when the tokeniser refuses it. `runs_git`'s bound is *a substitution is
   not a command position*; for `read` the same blindness would let
   `x=$(rm y); ls` read as reading, so here it disqualifies instead.
   There is no anchored fallback for a refused line: `read` is new, so there
   is no older answer to fall back to, and `other` is the answer.
4. **`read` is judged after the four existing families.** First match in
   `FAMILIES` order still decides, and `read` is last, so `ls && git status`
   is `git`, `grep -rn pytest docs/` stays `test` and
   `cat tests/x/test.sh` stays `test`. Those last two are the mirror #377
   recorded as out, and #642 names keeping them as *what must not break*.
5. **#635's four deferred findings, all in.** They sit on #642 because this
   item reuses #377's segmentation (the comment on #642, read). All four are
   in, for three reasons: `read` reads through the same heredoc pass and the
   same bounds, the units they edit are ones this item re-stamps anyway, and
   the round that found them left paste-ready text
   (`seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/rounds/round-3-report.md`
   §*Paste-ready fixes*, read):
   1. `without_heredoc_bodies` removes `\⏎` from an unquoted heredoc's body
      before it compares a line with the delimiter, as bash does, so
      `cat <<EOF⏎body \⏎EOF⏎git push` is `other`. The `HEREDOC` comment
      states the operator-line continuation (`cat <<EOF \⏎&& git push⏎…`)
      as a bound.
   2. `without_comments`' and `runs_git`'s docstrings say in which direction
      each bound can fail, instead of *never worse than the rule before
      #377*. `x="$(echo "; git log")"` and `echo $(ls)#'⏎git push'` read a
      `git` that bash does not run. The same sentences say the bounds apply
      to `read` too.
   3. `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/overview.md`
      §*Not done*: the same claim, corrected in place with a dated note.
   4. Ledger row N2, which lives in `seal/releases/0.15.6.md`, not in the
      fragment the round cited: the 0.15.6 fold moved it (read: there is no
      `seal/ledger/` directory at 1fa25931). The clause is narrowed to a
      quote the shell itself leaves unmatched, with a `Corrected <date>`
      note naming `echo $(ls)#'⏎git push'`.
6. **The statements that change, each in the commit that makes it true**,
   listed below.

### Every statement about the families, enumerated

Found by searching `skills/`, `docs/`, `tests/`, both READMEs and the ledger
for `famil`, `by_family`, `FAMILIES`, `family(`, `` `other` ``, `lint/type`,
*other three*, *four famil*, and by counting every ledger anchor on the
units below (read 2026-09-28 at 1fa25931 plus the routing commit).

| Coordinate | What it says | Verdict |
|---|---|---|
| `session_cost.py#FAMILIES`, the comment | families in priority order; `git` is the one family read by command word | **edit**: `read` is the fifth, judged last and by command words; state the admission criterion for a read word (its only output is standard output, or the option that writes is in In §2), so the next word is added by the rule rather than by taste |
| `session_cost.py#HEREDOC`, the comment | the bounds of the operator | **edit**: finding 1's operator-line continuation bound |
| `session_cost.py#without_heredoc_bodies` | body to the first line equal to the delimiter | **edit**: finding 1 |
| `session_cost.py#without_comments`, docstring | *Two bounds, neither worse than the rule before #377* | **edit**: finding 2 |
| `session_cost.py#command_words` | the walk | **edit or leave**: see Data & interfaces. Its contract and every existing case are unchanged |
| `session_cost.py#runs_git`, docstring | *an unmatched quote never answers worse than the old rule did* | **edit**: finding 2 |
| `session_cost.py#family`, docstring | *`git` is judged by `runs_git`, by command word, and the other three by their patterns* | **edit**: `read` and its rule |
| `session_cost.py#analyse`, docstring | *Two rules moved after readings were published*; the #377 paragraph | **edit**: a third move, #642: `by_family` and `unnamed` move, the repeats figures do not |
| `session_cost.py#analyse`, the `unnamed` comment | `other` is the family with no meaning of its own | true; no edit |
| `session_cost.py#report`, the `other`-leads note | *`other` is the largest family and names nothing* | true; **no wording change**. It fires less often, which is the point |
| `session_cost.py#report_segments`, the #377 comparability line and its comment | family rows comparable only since #377 | **edit**: they are comparable only with readings on a release that carries #642, and the line says what moved. Names the issue, not the version (`tests/test_release_hygiene.py`'s timer check) |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, beside the #377 paragraph | nothing about reading | **add** one paragraph, #377's shape: what moved, and what a reader comparing across it must know |
| `tests/test_session_cost.py#test_a_git_call_after_cd_is_charged_to_git` | `W=/w; cd $W; for f in a b; do grep -c x $f; done` → `other`, as the control | **edit**: that arm becomes `read`, which is #642's shape. The `python3 -` heredoc arm stays `other` (the owner's answer), and the docstring says so |
| `tests/test_session_cost.py#test_a_line_running_two_families_is_charged_by_their_order`, docstring | *`git` is last* | **edit**: `read` is last |
| `tests/test_session_cost.py#test_the_report_names_the_command_the_table_could_not` | `./bin/deploy --wait \| tail -3` in `other`, `other 4 calls` | true under In §1; **must pass unchanged**. It is the fixture that kills the *any read word* mutant |
| `tests/test_session_cost.py`, the heredoc, refusal, comment and substitution cases | not `git`, or `other` | each must pass unchanged. Every `== "other"` arm is a write, a heredoc, a refusal or neither family |
| `docs/measuring-a-run.md` | the policy clause above | true; no edit |
| `README.md`, `README.ko.md` | describe the reading without naming a family | no edit |

`evidence-check` at the tip is the authority for which ledger rows drift.
The expected set, counted at 1fa25931: `#analyse` in 10 rows over
`seal/ledger.md`, `0.9.4.md`, `0.9.5.md`, `0.11.3.md` and `0.15.6.md`;
`#family`, `#command_words`, `#runs_git`, `#without_comments`,
`#without_heredoc_bodies`, `#HEREDOC` and `#report_segments` in 0.15.6 N1–N6;
`#FAMILIES`, `#family` and `#HEREDOC` in 0.9.4 S1 and S2; the `SKILL.md`
section anchor in 11 rows over six release files; and every
`tests/test_session_cost.py#…` anchor on an edited case.

### Decided from the tree (the judgments the ticket left open)

- **Every command word, not the first after `cd`, and not any one of them.**
  "Any read word" charges `./bin/deploy --wait | tail -3` to reading, and a
  pipe into `head` or `tail` sits behind nearly every kind of command. "First
  after `cd`" charges `ls && rm -rf x`. The ticket's own words are
  "read-only file and listing commands", and In §1 is that phrase taken
  literally. `plan.md`'s Alternatives table carries the failure of each.
- **The word list is #642's thirteen.** They are what the ticket measured, so
  the phase-3 numbers can be set beside the ticket's. A filter that would
  qualify under the criterion (`cut`, `tr`, `jq`, `uniq` without an output
  operand) is left for a later change with numbers: `questions.md` Q3 has
  phase 3 count which command words keep an otherwise-read line in `other`.
- **Ambiguity falls to `other`.** A write charged to `read` is #200's error;
  a read charged to `other` is the state of every reading published so far.
- **The heredoc rule is the owner's answer made mechanical.** Any `<<` on
  the line keeps it out of `read`, so a heredoc stays in `other` whatever
  follows it, and `read` does not move when an agent switches between the
  `Edit` tool and a shell edit.
- **The name is `read`, the owner's.** It meets the `verify` skill's label
  `read` (executed, read, unverified) in a flow-log comment. The family is
  always printed as a row name and written in backticks, and
  `tests/test_one_word_one_meaning.py` pins no sense of the word (read), so
  the frame keeps the owner's name.
- **#640 is not foreclosed.** #640 as filed grades tools per turn against a
  segment's kind, and reads no family (read, the issue body). The caller's
  prompt said its grade "reads the families". The body does not say that,
  and the frame follows the body. What a later grade could use is kept
  intact: every `read` call has no side effect, so a run of `read` calls in
  single-call turns is batchable by construction. That holds only because
  In §1–§3 keep writes, heredocs and vehicles out.
- **#635's finding 2 is not counted.** How many corpus calls its four shapes
  reach was left unverified by its round. The sentences are wrong whatever
  the count is, so nothing here needs it.

### Out

| Item | Why it is out | Who answers it |
|---|---|---|
| A `python3 -` heredoc family | the owner's answer, 2026-09-28: a heredoc row counts a vehicle, it moves whenever agents switch between `Edit` and shell edits, and that confounds 0.17.0's #640 | answered (`questions.md` Q1) |
| More read words (`cut`, `tr`, `jq`, `uniq`, `stat`, `xargs` …) | #642 measured thirteen. Adding words is a later change, with the phase-3 count in hand | the owner, from Q3's numbers |
| The mirror: a read charged to `test`, `lint/type`, `build` or `git` because a name sits in its arguments (`grep -rn pytest`, `cat Makefile \| grep make`) | those families match anywhere on purpose (0.9.4 S1), #377 recorded the mirror as out, and #642 lists keeping it as *what must not break* | as #377 recorded it: the owner, when a release plans it |
| A wrapper looked through (`timeout 60 grep`, `xargs grep`) | `runs_git`'s stated bound, which `read` inherits: the wrapper is the command word | nobody needs to; the docstring states it |
| `read` in the repeats figures | the repeats figures count *a check re-run for a result already produced*, and they keep `test`, `lint/type` and `build`. A re-read file is a different question | not deferred: noted so the build does not widen into it |
| Rewording the `other`-leads note | it stays true, and it has a pinned needle | not deferred |
| #637's slicing (`resume_cuts`, `segment_slices`, `report_segments`' empty branch, `main`) and #640's grade | item A of this milestone, and 0.17.0 | their own chains |
| Re-deriving published readings | the policy asks which numbers move, not a recomputation | this spec, the changelog fragment and the `SKILL.md` paragraph |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the ticket's instance | `cd /x && sed -n 1,5p f` → `read` | a `family` case, red before the family exists |
| S2 read-only shapes | `grep -n x f \| head -5`, `ls -la /x 2>/dev/null \|\| echo none`, `for f in a b; do wc -l $f; done`, `[ -f x ] && cat x`, `if grep -q x f; then echo y; fi`, `(cd /x && ls)`, `FOO=1 rg x`, `W=/w; cd $W; for f in a b; do grep -c x $f; done` → `read` | the same case |
| S3 writes are not reading (#200) | `sed -i s/a/b/ f`, `sed -i.bak …`, `sed -ni …`, `sed --in-place …`, `cat f > g`, `grep x f >> g`, `sort -o g f`, `find . -delete`, `find . -exec rm {} +`, `awk -i inplace …`, `cat > f <<'EOF'⏎x⏎EOF` → not `read` | a case. A mutant that drops the redirection check turns it red, and so does one that drops the `sed -i` check |
| S4 a line that does more than read | `./bin/deploy --wait \| tail -3`, `cat f \| python3 -c 'x'`, `ls; rm x`, `sleep 5; tail log`, `timeout 9 grep x f` → not `read` | a case. The *any read word* mutant turns it red |
| S5 hidden from the walk | `python3 - <<'EOF'⏎x⏎EOF`, `cat <<'EOF'⏎text⏎EOF`, `x=$(rm y); ls`, `cat $(ls)`, `diff <(ls a) <(ls b)`, `cat 'x` → not `read` | a case |
| S6 nothing but neutral words | `cd /x`, `echo hi`, `W=1` → `other` | the same case |
| S7 precedence | `ls && git status` → `git`; `grep -rn pytest docs/` → `test`; `cat f && ruff check .` → `lint/type` | a case. A mutant that judges `read` first turns it red |
| S8 through a transcript | a transcript whose Bash calls are `cd /x⏎sed -n 1p f` and `cat > f <<'EOF'⏎x⏎EOF` / `--json` → `by_family` holds `read` with one call and `other` with one | a transcript case; pins the wiring through `load`'s `ran` |
| S9 finding 1 | `cat <<EOF⏎body \⏎EOF⏎git push` and `…⏎git push⏎EOF` → not `git`; `cat <<'EOF'⏎body \⏎EOF⏎git push` → `git` | a case, red at the rebased base |
| S10 what the reader is told | `--segments` prints a comparability line naming #642 for the family rows, beside the #377 and 0.9.4 lines | a case asserting the sentence. Deleting it turns the case red |
| S11 unchanged cases | every existing `family`, heredoc, refusal, comment, substitution, `other`-note and comparability case passes, the two edited arms aside | the module, run at each phase |
| S12 the ledger stays true | `evidence-check` names no DRIFTED row this work left un-re-read; N2 carries `Corrected <date>` | `evidence-check`'s exit code, read directly |
| S13 the numbers | a transitions table over the corpus: base family → tip family, in calls and seconds | phase 3's probe, deleted after, table in `phases/phase-3.md` |

## Data & interfaces

- **`family(command)` keeps its signature** and gains one return value,
  `read`. `FAMILIES` either gains a fifth entry with no pattern or keeps
  four with `read` checked after the loop. The builder chooses; the order
  is fixed either way.
- **One walk.** `read` needs each command's arguments and redirections,
  where `command_words` yields only the first word. The builder factors the
  walk so both come from one pass: a generator of simple commands from which
  `command_words` is derived with its contract unchanged, or an equivalent.
  A second tokeniser pass is refused, for the reason #377's plan refused
  reading two texts under one docstring.
- **`--json`**: `by_family` may carry a `read` key; `unnamed` may name a
  different command. No key is added or removed elsewhere.
- **The printed reading**: the `by family` block may print a `read` row. Its
  width fits the existing `{name:<12}` column.
- **Dependencies:** none new.
- **Published readings affected** (the policy clause's act): every
  `session-cost` reading taken on a release before the one carrying #642,
  whether posted to a `flow-measurement` or `flow-baseline` log, pasted into
  a seal's `cost` row, or kept in a round record. In each, the `other` row
  holds the calls a `read` row would now hold, there is no `read` row, and
  the `other`-leads note may fire where it would not now and may name a
  read command. The `git`, `test`, `lint/type` and `build` rows, the two
  repeats figures, span, command, model, idle, tokens, tools per turn,
  `slowest`, and every `--spawns` and `--segments` span do not move under
  the `read` rule. Finding 1's heredoc fix moved 0 corpus calls when its
  round measured it (executed by that round; read here).

## Open questions → questions.md

No row needs a person. Q1 is the owner's answer, recorded. Q2 and Q3 are
measurements phase 3 takes, and Q4 and Q5 are the work's.

Framed 2026-09-28 by framer, before the build.
