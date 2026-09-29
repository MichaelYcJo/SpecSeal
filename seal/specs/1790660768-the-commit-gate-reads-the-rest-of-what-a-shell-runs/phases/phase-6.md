# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 6

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-6.md -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 5c721568 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 6, proof and records:

- the differential corpus of S7 (b), and Q2's prompt budget;
- the #670 paragraph of `docs/commit-review-gate-spec.md`: the positions, the
  redirection rule, the merged view, the hosts, the bound, and its `Enforced
  by:` line;
- `docs/worktree-guard-spec.md`, if it names a word a redirection now
  reaches;
- the ledger fragment, and the rows Q5 names, re-read in their own files with
  a dated note and corrected where an edit made them false;
- the changelog fragment naming #674.

Verified by: zero rows silent at head where `86256492` stops, with the corpus
size and the new-stop count on its non-commit half; Q2's counts;
`evidence-check` exit 0 on every file touched; `rider_check.py`; the survivor
sweep over the corrected sentences.

## What this phase found

**S7 (b), the corpus.** A generator crossed these (a deleted probe):

- the positions P1–P13, 29 spellings among them;
- nineteen redirection spellings, each placed before the program word and
  after it;
- the four readers;
- a commit, an expanding word and nothing, as the payload.

It adds P11's line continuation and W1's four relocating words behind every
redirection. That is 11,393 commands. Each was judged at `86256492` and at
head, in an opted-in undeclared directory and in a declared one: 22,786
judgements. The judgement is the gate's own partition of `commit_invocations`'
output: in the undeclared directory anything found stops, and in the declared
one a target that is unresolved or elsewhere stops. That model was checked
against `main()` itself on 200 of the commands, in both directories and at
both SHAs, and all 800 verdicts agreed.

- **Silent at head where `86256492` stops: 0.**
- **Stop at head where `86256492` was silent: 4,543**, all on the commit and
  expanding-word halves, which is the fix.
- **On the 4,527 commands that commit nothing (9,054 judgements): 0 new
  stops.** The first run found 38. Each was a redirection holding `{` or `$`,
  such as `{fd}>f` or `>"$LOG"`, counted by one of phase 2's readings as a
  word that expands: behind a runner, behind a header, or in the stand-in. A
  redirection's target is never a command, so those three readings now leave
  redirections out (`_without_redirections`), and the reading as written
  keeps its base answer. A mutant then showed that base answer was pinned
  nowhere: `sh -c '>"$LOG" echo hi'` stops at `86256492`, and it is planted
  now. Three controls were red at `8a45d1fe`, and five mutants were killed.

**Q2, the prompt budget: zero.** A deleted probe read every Bash command in
sessions `8cadfa28`, `30ac0e06` and `ab2760f5`: the three main transcripts and
99 subagent transcripts, 6,033 distinct pairs of command and directory. Both
gates' readers ran on them. None changed its verdict under either directory
model, so every one of `spec.md`'s classes (a)–(e) is zero. The probe was
reading real commits: 495 of the commands hold one, at both SHAs, and 16 have
an unresolved target, at both.

**Q5, the drifted rows.** Beyond `spec.md`'s list, `evidence-check` named
E7, E9, E12 and E16, which anchor on the policy section and the corpus, and
one row in `seal/releases/0.4.0.md`. That row anchors on a statement inside
`understood`, and phase 1 had moved the statement into a helper. `understood`
was restructured so its base body stands where it stood, with the W1 check as
its first line, and the row resolves again without an edit. The other 15 rows
were re-read in their own files, four in `seal/ledger.md` and eleven in
`1790644505`'s fragment. Each check `seal/ledger.md`'s rows carry was
executed again at head, and gave the answer they record. Two claims had
become false and carry a `Corrected` note:

- E7: `commit_invocations` is no longer the release branch's;
- E18: the nesting is answered at the bound, not at the depth that
  overflowed.

After the re-stamp the whole ledger reads 3,014 ok, 0 drifted, 0 broken.

**The policy.** The #670 statement names `flock -c` and `parallel`, and its
recursion sentence gets the bound. A new statement follows it with the
positions, the redirection rule, the merged view, the headers, the hosts,
`sudo`'s exclusion, the argument that only stops are gained, and the corpus
and budget figures. Its `Enforced by:` line had to fit the wrap limit, because
the paragraph stands under a heading outside any folded statement. So it names
the wrapper module, and the sentence before it names the invariant module.

The guard's policy gains one sentence. Checking its examples through
`cmdline.adds_a_worktree` found that the first draft's second example, `git
2>&1 worktree add`, is not read by the guard. The merged view is the commit
gate's alone. The sentence now says so, and the overview's *Not done* names
it.

**One rule met.** `tests/test_no_real_identifiers.py` refused the domain of
the online flock(1) page in three records. The allowlist was not extended,
and the records now name the page without the domain.

**Verification.** Executed:

- At `5c721568`: `bin/evidence-check`, 3,014 ok and 0 drifted, lenient exit
  0. `rider_check.py`, 18 ok, exit 0. `survivor-check --range
  86256492..5c721568`, 39 removed sentences checked against 530 files, "no
  removed wording is still standing", exit 0.
- The record and document checks this phase touches, 17 modules: the wrap
  and fold rules, the one-word check, the ledger, changelog, question and
  phase-record shapes, the identifier check and the correction checker. 823
  passed after the two fixes above.
- The 26 modules that load the reader, either gate, the consent writer or the
  notice, plus `tests/test_the_reader_agrees_with_bash.py`: 1481 passed and 1
  skipped, exit 0.

**Mutants of this phase's units.** Each ran alone under
`PYTHONDONTWRITEBYTECODE=1` and was restored from saved bytes. The tree was
clean after each run.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | the header reading asks as written | the `$LOG` in a function body control |
| 2 | the as-written reading dropped at the top level | `sh -c >$LOG echo, the base's own stop`, once planted |
| 3 | P4 counts redirections | the `$LOG` behind a runner's options control |
| 4 | the stand-in counts redirections | the unplaceable-header pin |
| 5 | `_without_redirections` keeps them | the same |
| 6–10 | `understood`'s restructure: no redirection check, a refusal not taken, a `cd` fine, a pass with none passed, prefixes not kept | W1 and the wrapped-commit cases |

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*,** gathered from the six phase records:

- *A test seen red.* Every case was run red before it was planted: 61 at
  `4e5335b3`, 25 at `b1ad717a`, 24 at `f614f89c`, 38 at `b94054ae`, the
  depth count at 249 against 32, and three controls at `8a45d1fe`. A pin on a
  base answer or a control was seen red by the mutant named in its phase's
  table. Every changed branch has a mutant a case kills, 85 in all, and each
  survivor either gained a case or its branch was removed.
- *Failure direction: it blocks more, never allows more.* Every reader asks
  what it asked at `86256492` first, and adds. `understood` only adds a
  refusal. The merged view adds only a kind no segment found. The corpus
  found none of 22,786 judgements silent where the base stops.
- *Prompt budget.* In an attended session a stop is one refusal and then a
  prompt per re-issue. Under `automation` it is a refusal, and no person is
  asked. On commands that commit nothing, the new stops are `spec.md`'s
  (a)–(e), each measured at zero over 6,033 recorded commands. The corpus's
  non-commit half has zero new stops after phase 6's fix.
- *Why nothing cheaper reaches the same guarantee.* Leaving the shapes unread
  is a commit nobody judges, and bash landed every one it was given. The
  stand-in everywhere stops `grep -n watch *.py` in a function body.
  Changing the splitter reads `cd W 2>&1 && git commit` silent where the base
  stops.
- *An outage is excluded.* Every added stop needs a program, a string or a
  redirection where a shell runs one. `git -C <absolute path> commit`, in a
  command of its own, has none of them.
- *Platform honesty.* String reading only, with no process inspection. bash
  3.2.57 and zsh 5.9 ran the redirection shapes on macOS. bash 4.1's `{fd}>`
  was read, not run. `flock`, `parallel` and `sudo` were read from their
  manuals. Windows is CI's `windows-latest` leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `_understood_as_written`, the helper phase 1 moved `understood`'s body into | `understood` itself, where the body stood at `86256492`; the W1 check is `_unreadable_past_leading_redirections` |
| the merged view's per-token `origin` list | none: the directory an addition takes became the last part's, `overview.md`'s divergence row |
