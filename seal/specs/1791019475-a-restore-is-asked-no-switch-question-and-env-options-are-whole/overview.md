# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

0.18.0 should not ship a switch question about a restore that the base never
asked. It should also not miss a commit behind an `env` spelling that one of
`env`'s two grammars runs. Both are #733's deferred round-3 findings (#737).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S5's criterion (a) | `plan.md` §*The generated comparison for C*: "No shape that bash ran as neither a switch nor a creation is asked by the build unless `233f0455` asked it … A shape failing (a) is a defect of the build, not a limit." The build fails it on 468 shapes bash 3.2 can judge, plus 358 it cannot. 414 of the 468 are a checkout of a file behind a redirection the frozen reader cannot see past (`2>/dev/null git checkout README.md`). 54 are a descriptor glued into an option word (`git checkout --2>&1 README.md`) | the build as framed, recorded rather than built around | `2b1dcb1f` asks every one of the 468, so none is new. C reads no tree by #689, and `spec.md` §*Out* keeps "a tree-aware C" out, so `README.md` and `feature/x` are one word to it. `switch_kind` is not changed (`spec.md` §*Data & interfaces*). The criterion and the frame's §*Out* cannot both hold over a verb list holding `checkout README.md`, and choosing between them is the framer's (`phases/phase-1.md`) |
| S4's generator | `spec.md` S4: every operator "glued to the word before it and spaced". Built: a numbered or `{fd}` operator is spaced only | the operator bash reads | bash takes a number as a descriptor only as a word of its own, so `--2>&1` hands git the option `--2`. That is another verb, not a restore with a redirection. The bash comparison still generates the glued forms and counts them |
| `_env_option`'s BSD condition | Phase 2 first read a `--` word as a BSD cluster only among env's own options and not for `--` alone | `grammar != "bsd"` alone | breaking either clause left every case green, and each is equivalent under the union of the two walks (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| GNU's half of the env grammar runs as modelled. The model was written from `src/env.c` at `f799b2f48a61` and gnulib's getopt rules, and never run against a GNU `env`, because none is installed here and no CI leg runs one | the reviewer, on a machine with GNU coreutils 9.12 or later, if a GNU run is wanted; the planted cases test the reader and run no `env` |
| The 358 generated guard shapes holding `&>>` or `{fd}`, which `/bin/bash` 3.2.57 cannot run (they need bash 4.0 and 4.1). Read as bash 4.1 or later reads them, the 24 the build adds over `2b1dcb1f` are creations | the reviewer, with bash 4.1 or later, if the 358 are to be run rather than read |

## Not done

**The 414 tree-blind shapes and the 54 glued-descriptor shapes stay asked.**
Closing them needs a tree inside C or git's option table inside
`switch_kind`. The frame keeps both out, and they are listed under
*Where spec and implementation diverged* for the session that spawned this
build.

**#738** stays where Q2 put it. Its S5 count is 226 shapes, 113 core shapes
under the two prefixes that enter `w`, silent at `233f0455`, `2b1dcb1f` and
the build (`phases/phase-1.md`).

## Fed back into the spec

none
