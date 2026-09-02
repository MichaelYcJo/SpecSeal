# 1788305134-the-reader-stops-where-it-need-not — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     this item's `spec.md` and `plan.md` · the original item's
            `spec.md`, `plan.md`, `questions.md`, `overview.md` and
            `rounds/round-2.md` read from `fix/stops-the-reader-need-not-make`
            · `CLAUDE.md` on this branch · `templates/sdd-*.md` ·
            `.specseal/map.md` header · `skills/evidence-check/scripts/evidence_check.py`
            usage
· evidence: 13 rows in `.specseal/map/1788305134-the-reader-stops-where-it-need-not.md`
            (9 at round 0, 4 from round 1's fixes); no row of `.specseal/map.md`
            removed — this change deletes no anchor
· verified: executed — the scope run (round 0: 301 passed across seven files;
            round 1's fix pass: the reader's test files plus the in-tree
            differential), 24 mutations (7 from round 2's 🟡 7 against the code
            as found, 6 red; 7 against round 0's count, 7 red; 10 against
            round 1's stack, call reset and writers, 10 red), differential
            runs with bash 3.2.57 as the oracle (1,790 inputs at round 0;
            2,109 against the reader at `dd7e45e` after round 1 — 0 fail-open
            now, 124 there), `ruff check` and `ruff format --check`,
            `evidence-check --strict`. Read only — the old branch's diff
            against this tree, its round records, the gate and guard call
            sites that take the change without a signature change

## Why this work exists

The reader's two needless stops were fixed and reviewed on a branch the
history rewrite orphaned; re-applying it found the change already in the tree
together with a later, unreviewed aimed reset, and proving that reset against
bash found it had opened a class of confident wrong answers, which is now
closed.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What "re-apply" meant | The handoff expected `git apply --3way` and hand resolution in six files | Nothing was applied. `git diff fix/stops-the-reader-need-not-make -- hooks/cmdline.py agents/warden.md agents/scribe.md tests/…` shows the tree AHEAD of the old branch: the differences are the rewrite's issue-number rewording, a warden section from another item, and the aimed reset with its eight tests | Executed, the diff is quoted in the handback. Applying the old patch would have moved the tree backwards |
| Where round 2's 🟡 3/4/5 close | The handoff asks this item to close them with code or grounds | They were closed in the tree before this item began — `_unseen` (🟡 3), the rewritten `else` comment (🟡 4), the `lastpipe` comment and its test (🟡 5) — by a commit that exists only inside the rewrite's initial commit and was reviewed by nobody | The tests carry a `b76fd99` measurement, the old branch's tip, so the work postdates it. This item's job became proving it, and the proof found S10 |
| The `else` branch's comment on function bodies | *"It is narrower than it sounds, because a body defined in this command string is split on `;` like any other text, so its assignments arrive here as tokens"* | Rewritten. Arriving as tokens was the problem, not the mitigation: the second statement arrived as a top-level assignment and bound | Measured — `f() { echo hi; SB=/three; }; git -C "$SB"` answered `/three` where bash has `/one` |
| How a closer is counted | First version counted `fi`/`done`/`}` wherever they stood | In command position only; `)` last as well | Eight shapes survived the first version, all `echo fi` inside a body; bash reads a closer as a word in argument position, so the count does too |
| An integer or a stack (round 1) | Round 0 kept an integer body count | A stack of open bodies: `)` pops only a `(`, every closer only its own opener, `f(){` opens a `{` | Round 1 🔴 2 and 🔴 3: a multi-line `case` arm pattern `a )` is a `)` last in its segment and brought the count to zero; the glued `f(){` opened nothing. Both bound a body's assignment where bash has `/one`. Cost accepted: a `case` arm that does match prompts too |
| Where an opener counts (round 1) | Round 0 counted openers wherever they stood, as the safe direction | Command position only | `git commit -m "(wip) x"; SB=/two` and `grep -c '(' f; SB=/two` prompted for the rest of the string. Safe because a closer pops only its own opener, so an uncounted opener inside a counted body cannot close the outer one |
| The function-call edge (round 1) | Round 0's comment called a function call the alias open edge | A function this string defines is a name the reader can see; the call empties the environment. What remains open is a function or alias defined outside the string | `f() { SB=/three; }; SB=/one; f; git -C "$SB"` — bash `/three`, reader `/one` |
| `${NAME:=…}` on a set name (round 1) | bash leaves a name that already has a value | Forgotten anyway, with `${NAME=…}` | The value the reader holds can be empty (`SB=`), where `:=` does write; one rule for both spellings costs a prompt on a rare shape and never an answer |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck on this branch after the review rounds settle — the scope here was the seven files that import `hooks/cmdline.py` | the orchestrator's broad gate, once |
| The Windows and Linux legs — every expected path here goes through `os.path.normpath`, but the oracle ran on one platform | CI at the pull request |
| Shapes whose oracle needs bash ≥ 4 — `mapfile`, `readarray`, `shopt -s lastpipe`. Under 3.2.57 each errors and leaves the name; the reader forgets on all of them, so nothing opens either way | whoever has bash 5 at hand; the answer can only widen the prompt count |
| The original item's 26,400-input differential against `2f95d72`. Its generator did not travel with the branch; the differential now in the tree (`tests/test_the_reader_agrees_with_bash.py`) covers the compound-command family it did not, and covers none of the paren-model corpus, which `tests/test_what_the_reader_understands.py` pins case by case | the review chain, if it wants the old corpus rebuilt |
| `declare -n ref=SB; ref=/three` — a nameref writes `SB` through `ref` on bash ≥ 4.3. This machine's 3.2.57 cannot run it, and the reader keeps `SB` (round 1 🟡 8 ③) | a maintainer with bash 5; if it writes, `declare -n` joins the writers `_forget` reads |

## Not done

**The directory half keeps its reading of bodies.** `if false; then :; cd
/two; fi; git commit` reports `/two` and the session's directory both, because
a `cd`'s failure is parked and `;` merges it back. That over-asks and never
passes, so it is recorded (`questions.md` Q5) and left.

**Quote provenance is not carried out of the splitter.** A quoted `"("` opens
a body that never closes and a glued `make)` closes nothing; both cost prompts
(`questions.md` Q4). Closing them closes Q1 with them and touches every
consumer of the splitter.

**Loop and positional variables, and anything from the environment, stay
unresolvable.** The substitution runs in front of the `EXPANDS` test rather
than replacing it, which is the line the original item drew and this one does
not move.

## Fed back into the spec

S10, S11 and S12 in `spec.md`, marked *inferred during implementation*. Each
is a fact the differential run produced rather than a clause the contract
carried, and a planner may overturn the count's two costs by answering Q4.
