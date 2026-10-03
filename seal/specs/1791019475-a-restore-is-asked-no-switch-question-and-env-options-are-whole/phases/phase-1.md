# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f9652cdc |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Close 🟡 13 and ⬜ 16. Candidate C reads each view's words with every
redirection taken off, starting from round 3's fence. Plant the S1 case, the
S4 generated case and three `WIDER_ONLY` rows: the two `&>` switches and the
`worktree 2>/dev/null add` creation. Reword `wider_only_kinds`' docstring.
Add one sentence and the re-stated corpus count to
`docs/worktree-guard-spec.md` §*Which tree*'s #678 paragraph, and correct K5
in place. Hold every change to the comparison over generated shapes (S5),
with bash in a scratch repository as the ground truth and `233f0455`,
`f1629706` and `2b1dcb1f` beside the build. Re-count the owner's corpus
(S6, M2); a count above zero stops the work. Write down the S5 count for
#738's shape.

## What this phase found

**The fence went in as written, and the S4 generator found a gap in the
generator, not in the fence.** `_bare_words` is round 3's fence line for line.
The first S4 run failed on 12 shapes, every one a descriptor glued to the
word before it: `git checkout --2>&1 README.md`. bash takes a number as a
descriptor only when it is a word of its own, so that hands git the option
`--2`, which is another verb rather than a restore with a redirection. The
generator now spaces a numbered or `{fd}` operator from the word before it,
and its docstring says why. The bash comparison below still generates the
glued forms, and they are counted there.

**Every new case was seen red.** At `2b1dcb1f`'s hooks, S1 failed on all six,
S3 failed in both the function case and the `main()` case, and S4 failed on
162 shapes. The two `&>` rows pass at `2b1dcb1f` and were red against the
merged-self mutant (below).

**Each unit was broken once with `bin/mutation-check`, over the guard module,
and every break was red:** the glued cut (8 failed), the `&` trim (5), the
removal of redirections (9), the empty-word filter (5) and the merged view's
sources replaced by the view itself (4, the two `&>` rows among them). The
`&` trim is reachable: `merged_view` gives `&>/dev/null` as one word, and
`unglued` cuts that word into `&` and `>/dev/null`.

**S5, the generated comparison.** 4,848 core shapes: 13 verbs, the 12
operators of `_REDIRECTION` that bash takes plus a numbered form of each that
takes one, `>&` with a file, and `{fd}>` once, at every position, glued and
spaced, target glued and spaced. Each ran under `/bin/bash` (3.2.57) in a
fresh copy of a scratch repository: 2,526 ran as nothing, 1,668 as a switch,
406 as a creation and 248 as a detach. Through `main()` over a dirty `w`
under a clean session, with four prefixes, the result is 19,392 shapes.

| | `233f0455` | `f1629706` | `2b1dcb1f` | build |
|---|---|---|---|---|
| `main()` stops | 2,752 | 5,802 | 7,360 | 7,008 |
| of them, the wider reading's question | 0 | 3,050 | 4,608 | 4,256 |
| `wider_only_kinds` non-empty (function level) | — | 2,196 | 3,280 | 3,144 |
| (a) stops on a shape bash ran as neither a switch nor a creation, where `233f0455` was silent | — | 586 | 1,450 | 826 |

(c), the build against `2b1dcb1f`: 648 stops dropped, every one on a shape
bash ran as nothing or as a detach (`checkout -q` 201, `switch --detach` 201,
`checkout .` 114, `checkout -- README.md` 48, and 84 on `checkout -` and
`switch -` with a descriptor glued in, which git refuses). 296 stops added:
272 on `worktree … add` shapes bash ran as a creation, and 24 on
`git worktree &>>/dev/null add …` and `git worktree {fd}>/dev/null add …`.

**S5's criterion (a) does not hold as written, and no part of what fails it
is new in the build.** Of the build's 826:

- **358 are the oracle's limit.** `/bin/bash` here is 3.2, which has neither
  `&>>` (bash 4.0) nor `{fd}` (4.1), so it ran those shapes as a background
  job and a word. 24 of them are the only (a) shapes the build adds over
  `2b1dcb1f`, and under bash 4.1 or later each is the creation S3 names.
- **414 are a checkout of a file behind a redirection the frozen reader
  cannot see past**, such as `2>/dev/null git checkout README.md` and
  `git checkout<<<word README.md`. C reads no tree, so `README.md` and
  `feature/x` are the same word to it. `2b1dcb1f` asks the same 414, and
  `f1629706` asks 336 of them. Telling the two apart needs a tree inside C,
  which `spec.md` §*Out* excludes because #689 forbids it.
- **54 are a descriptor glued into an option word.** Examples are
  `git checkout --2>&1 README.md`, `git checkout -b2>&1 y` and
  `git switch -c0<&0 y`. bash hands git `--2` or `-b2`. `switch_kind` counts
  every argument as a name, or misses `-b` with a value glued to it. Twelve
  of the eighteen distinct shapes switch wherever `y` names a commit, so they
  are tree-dependent too. `2b1dcb1f` asks 210 of this class.
- **0 are 🟡 13's class.** At `2b1dcb1f`, 408 stops were a redirection's word
  read as a name. In the build that number is 0.

So the build removes 564 of `2b1dcb1f`'s 1,032 judged (a) shapes and adds
none. The 468 left are C's tree-blind and option-blind upper bound, which
#733's D3 chose and this frame's §*Out* keeps. The frame's criterion
"no shape that bash ran as neither … is asked by the build unless
`233f0455` asked it" cannot hold for a tree-blind C over a verb list that
holds `checkout README.md`. That is recorded here and in the hand-back
rather than built around (`plan.md` and `spec.md` are the framer's).

**Corrected 2026-10-03 by round 1's fix pass (white 2).** "Adds none" and
"the only (a) shapes the build adds" held over this phase's generator, which
never wrote a numbered `>&` with a file. Round 1's generator did, and found
60 more commands, 16 core shapes: `2>&/dev/null` or `{fd}>&/dev/null`,
target glued or spaced, before `add` or before `-C`'s value, as in
`git worktree 2>&/dev/null add ../wt b`. bash 3.2 and 5.2 refuse each as an
ambiguous redirect and run nothing; zsh 5.9 runs each as the creation. The
guard reads zsh's forms, so asking is right, and only these figures were
wrong.

**(b), the silences, and #738's number.** Over the two prefixes that enter
`w`, where the guard's tree holds `feature/x` as the ground truth's does, 226
shapes ran as a switch under bash with `233f0455` and the build both silent
(113 core shapes, each under two prefixes). `2b1dcb1f` is silent on 362 and
`f1629706` on 810. Every one of the 226 is a checkout: a redirection between
`checkout` and its name (`git checkout <<<word feature/x`, 84), glued to the
name (`git checkout feature/x<<<word`, 44), after `-b` (56) or around `-`
(42). That is #738's class, a checkout whose name carries a redirection or
has one before it, and **226 is the S5 count for #738**.

**S6 and M2, the owner's count.** Over D1's cut, 540 transcripts hold 27,551
Bash tool uses before 2026-10-03T11:06:22+09:00, and those give 27,351
distinct command and directory pairs. `wider_only_kinds` fires on 0 of them
at `2b1dcb1f` and on 0 in the build. In the same run it fired on four shapes
it is meant to find, the `worktree 2>/dev/null add` creation among them,
which `2b1dcb1f` missed. The built C is round 3's fence in logic, so the
count is also the fence's 0. Zero added stops, so the change stands under
the owner's rule.

**The policy sentence.** `docs/worktree-guard-spec.md` §*Which tree*'s #678
paragraph now says that a view is read with every redirection taken off. It
also says that the reading still looks up no tree, so the 414 above stay a
question. It re-states the count as 0 for #737's reading. Q2 keeps §*Known
limits* unchanged.

The probes, the hooks extracted at the three commits, the scratch
repositories and the result files were made under the session scratchpad.
They are deleted before the hand-back. Nothing from the corpus is committed
except the counts above.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `wider_only_kinds`' second reading of each view through `unglued` alone | none: `_bare_words` reads the glued cut and the removal in one pass |
