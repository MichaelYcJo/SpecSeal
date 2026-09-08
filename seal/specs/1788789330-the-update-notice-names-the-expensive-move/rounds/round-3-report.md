# round 3 — the verifying round, and the last one this work item gets

Target `89333dd`, base `86e140f`, PR 233. The surface is `git diff 279628b..89333dd`,
whose substance is `db5b9cd` and `760ac3e`. Rounds 1 and 2 both closed on fixes, so
this record ends the run whatever it finds — `docs/review-chain-spec.md`
§*The reopening — one, and then the run is capped*.

Every probe ran in a `git clone --no-local` of this worktree at `89333dd`, at
`/private/tmp/claude-501/…/scratchpad/wi134-clone`. Nothing was written in the
worktree except this file.

## How the one finding relates to what came before

This work item produced three fixes of one bug, and each fix was defeated by a
mutation one word outside what it pinned. `760ac3e` broke that pattern by changing
shape: it deleted the predicates and pinned `notice()`'s whole output as an exact
string. That decision holds — the mutation that defeated the fourth predicate now
fails.

What does not hold is the sentence the fix wrote about its own reach. Both
`tests/test_version_check.py:101-103` and the ledger row say the guarantee is
carried by a PAIR of cases, so that an editor who updates the golden string
carelessly still has to contradict the module docstring to overclaim. Measured, an
editor who does exactly that leaves the module at `18 passed`.

That is the same failure this work item kept making, one level up: the pin was
measured against six mutations, none of which updated the golden, and the record
generalised the count to the class. `agent-contract` §5 is the rule, and the ledger
row itself states the lesson twice about earlier rounds.

## 1 · 🟡 The pair of cases is described as a net against a careless golden update, and it is not one

`tests/test_version_check.py:101-103`, and the same sentence in
`seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` row S1·S2·S3.

The exact pin's docstring says: *"The case below is what catches a careless paste.
The module docstring independently scopes the reload, so an editor who overclaims
while updating this string still has to contradict the file to do it."*

Executed. Four mutations of the notice with the golden string brought along in the
same edit, run against both cases:

| The notice now says | Result |
|---|---|
| the reload re-reads the copy you are on **and the one you just installed** | `2 passed`, exit 0 |
| the third axis `is unmeasured, **yet it is picked up**` | `2 passed`, exit 0 |
| the reload re-reads the copy **you just installed** (scope replaced) | `1 failed`, exit 1 — the docstring case fires |
| — baseline, no mutation | `18 passed`, exit 0 |

So the docstring case is a net against ONE thing: the scope qualifier being removed
from the reload's sentence. It is not a net against an overclaim being added, which
is the shape that defeated all four predicates and the shape the sentence claims it
covers. `tests/test_version_check.py:135-140` — the other case's own docstring —
says this correctly and names the exact mutation it leaves standing. The two
docstrings in the same file contradict each other.

### What the four deleted predicates covered, and what covers it now

The prompt asked whether deleting them was a loss. Against the notice as it stands,
no: `msg == <exact string>` implies every property the deleted assertions checked,
and it kills mutations they missed. Against a **rewording where the author updates
the golden**, five of the seven assertions' properties are no longer checked by
anything. Executed — each of these leaves the whole module at `18 passed`, exit 0:

| The deleted assertion | Still held after a rewording |
|---|---|
| `"/reload-plugins" in msg` | yes — the docstring case raises if no sentence names a reload |
| scope in `reload_claim` (`already on` / `in force` / `already running`) | yes — the docstring case asserts the same three |  <!-- NAME NOT IN TREE -->
| `index("/reload-plugins") < index("restart")` | **no** — the restart can be named first |
| `"measured" in reload_claim` | **no** — the source label can be dropped |
| `"skill bodies" in reload_claim` | **no** — the claim's subject can be dropped |
| `"agent definitions" in gap`, `"installed" in gap` | **no** — two of the three axes can be dropped |
| negation in `gap` | **no** — the gap can be stated as a fact |

The first of those unheld rows is clause S1 of this work item's own ledger row —
*"names `/reload-plugins` before the restart"*. Nothing pins it any more once the
golden moves.

### The trade-off the docstring does state, and the half it does not

- **Stated** — a legitimate rewording fails the case (`:95-99`). That is the false
  positive, and it is stated honestly and deliberately.
- **Not stated** — a wrong rewording passes it once the golden is updated. That is
  the false negative, and it is the one the pair was built to close.
- **What actually carries it** — the assertion message at `:121-124`, which tells a
  person to check the new text against run 6. That is an instruction to a reader,
  not a check that runs unattended.

The last line matters against `CLAUDE.md`'s first goal, which prefers the design
that does not stop to ask a person. Naming it in the docstring is the minimum; making
it run again is the deferred candidate below.

### Why this is 🟡 rather than ⬜

The notice's text is correct, the suite passes, and nothing crashes. What ships wrong
is a line a person reads that nothing pins: the next editor of this file is told a
second net exists, and it does not. One of the two sites is in `seal/ledger/`, which
`docs/review-chain-spec.md` counts as a correction; the other is in `tests/`, which
it does not.

## 2 · ⬜ `round-2.md` still says nobody has read its fixes, and this round just did

`seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-2.md:9`
reads `| Fixes checked by | nobody — the fixes are not yet written |`.

That is the correct value at the moment a record lands —
`docs/review-chain-spec.md:680` says so explicitly, and refusing it would refuse
every correctly written record. It is stale now: `db5b9cd` and `760ac3e` are
committed ancestors of `89333dd`, round 2's verdict cells already cite them, and
this round read them. The field is set by the session that closes, so it belongs in
the closing commit rather than in a fix pass.

## What round 2 recorded as closed, checked here

| Round 2's verdict | Actually closed |
|---|---|
| 1 — the by-hand comment pointed the wrong way | yes. `README.md:314` opens the load paragraph and `README.md:325` is the fenced block, so *see above* is right; `README.ko.md:305` and `:317` the same |
| 2 — the case pins by word | yes for the current text. The `yet` mutation now fails, `1 failed`, exit 1. Finding 1 is about the sentence describing the pin's reach, not about the pin |
| 3 — `README.md:182` described the banner as one line | yes. The count is gone; the sentence now names the two moves |
| 4, 5, 6 — answered, no fix | outside this diff, nothing to re-verify |

The two record lines marked `NAME NOT IN TREE` were checked by construction rather
than by reading. Both are load-bearing and both exempt only their own line: stripping
the marker off `round-1-report.md:162` takes `bin/evidence-check .` to exit 2 naming
that line, and adding a third unmarked prose mention of `reload_claim` to  <!-- NAME NOT IN TREE -->
`round-2-fixes.md` is refused the same way. The clean tree is `0 refused`.

The `130 lines` figure survives only in `round-1-report.md:51` and `:112` and in
`round-2-fixes.md:154`, which quotes it as the thing being removed. All three are
records pinned to their own Target SHA, where the number was true. Nothing in the
live tree carries a distance or a count about this pair.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The exact pin's docstring and the ledger row say the docstring case is a second net against a careless golden-string update; measured, an added overclaim and a `yet`-flipped gap both pass both cases with the golden brought along | `tests/test_version_check.py:101` | open | Executed in a `--no-local` clone at `89333dd`. Overclaim added to the reload's claim with the golden updated → `2 passed`, exit 0; `unmeasured, yet it is picked up` with the golden updated → `2 passed`, exit 0; scope phrase replaced with the golden updated → `1 failed`, exit 1, so the docstring case's net is removal only. Five of the seven deleted assertions' properties, including clause S1's ordering, leave the whole module at `18 passed` once the golden moves. Sibling site: `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` row S1·S2·S3, same sentence. `tests/test_version_check.py:135-140` states the opposite and is correct |
| 2 | ⬜ `round-2.md`'s `Fixes checked by` reads `nobody — the fixes are not yet written`; `db5b9cd` and `760ac3e` are ancestors of `89333dd` and this round read them | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-2.md:9` | open | Read. `docs/review-chain-spec.md:680` makes that value correct at landing and stale afterwards. A record location, so `Needs a fix` does not count it |
| 3 | ✅ Round 2's finding 1 — the by-hand comments now point at the load paragraph | `README.md:325` | answered | Read. `README.md:314` is the load paragraph and `:325` the fenced block; `README.ko.md:305` and `:317` the same. Both say *above* |
| 4 | ✅ Round 2's finding 2 — the exact pin refuses the mutation the fourth predicate let through | `tests/test_version_check.py:109` | answered | Executed. `yet`-flipped gap without a golden update → `1 failed`, exit 1. Baseline `18 passed`, exit 0 |
| 5 | ✅ Round 2's finding 3 — `README.md:182` no longer counts the banner's lines | `README.md:182` | answered | Read. The sentence now names the two moves and carries no count |
| 6 | ✅ Both `NAME NOT IN TREE` markers exempt their own line and nothing wider, and no third site names the deleted local | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-1-report.md:162` | answered | Executed. `bin/evidence-check .` exit 0, `0 refused`, on the clean tree; exit 2 naming `round-1-report.md:162` with the marker stripped; exit 2 naming a third unmarked prose mention added to `round-2-fixes.md` |

## Paste-ready fixes

Finding 1, the test docstring. Replace `tests/test_version_check.py:101-103`:

```python
    What this does NOT do is check a REWORDING. An author who changes the
    notice and pastes the new text in here passes both cases — measured, with
    the golden brought along each time: an overclaim added to the reload's
    claim, the gap flipped to `unmeasured, yet it is picked up`, the restart
    named before the reload, and the `measured` and `skill bodies` labels
    dropped. Every one left the module at `18 passed`.

    The one property the pair still holds across a rewording is the scope
    qualifier, because
    `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`
    looks for it independently. Everything else is carried by the message
    below, which is an instruction to a person rather than a check.
```

Finding 1, the ledger row. In
`seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md`, row
S1·S2·S3, replace the sentence beginning *"So `notice()`'s whole output is pinned"*
through *"the one both cases kill"*:

```
So `notice()`'s whole output is pinned as an exact string at `760ac3e`. **What that pin holds is the text as it stands, not any future text.** Measured against six mutations that leave the golden alone, it kills six. Measured again with the golden updated in the same edit — which is what an author rewording the notice does — an added overclaim and `unmeasured, yet it is picked up` both pass, and so do the restart named first, the `measured` label dropped, the `skill bodies` subject dropped, and two of the three axes dropped: `18 passed`, exit 0, each time. The second case holds exactly one property across a rewording, the scope qualifier, and the rest is carried by the assertion message, which a person reads rather than a checker.
```

The row's second and third code grounds are hashes over that case and that file, so
the docstring edit drifts them. Re-anchor in the same commit:

```
bin/evidence-check . --reverify
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_version_check.py -q` at `89333dd`, `--no-local` clone | exit 0, `18 passed`. Baseline |
| `test_tmp` probe — `yet`-flipped gap, golden NOT updated, both cases | exit 1, `1 failed, 1 passed`; `test_the_warning_names_the_cheap_move_before_the_expensive_one` fails. The orchestrator's M9 finding re-derived |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — overclaim ADDED to the reload's claim, golden updated in the same edit, both cases | **exit 0, `2 passed`.** The notice then tells a user the reload re-reads the copy just installed |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — `unmeasured, yet it is picked up`, golden updated in the same edit, both cases | **exit 0, `2 passed`** |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — scope phrase replaced with `you just installed`, golden updated, both cases | exit 1, `1 failed, 1 passed`; the docstring case fires. Control |  <!-- NAME NOT IN TREE -->
| `test_tmp` probe — five reWORDINGS with the golden updated, whole module: restart named first · `measured` dropped · `skill bodies` dropped · gap negation dropped · two axes dropped | **exit 0, `18 passed` on all five** |  <!-- NAME NOT IN TREE -->
| `bin/evidence-check .` on the clean clone | exit 0. `seal/ledger.md` 764 ok, the fragment `12 ok · 0 drifted · 0 broken`; records arm `9 names read · 0 refused` |
| `bin/evidence-check .` with the marker stripped from `round-1-report.md:162` | exit 2, `NOT-IN-TREE … round-1-report.md:162  \`reload_claim\`` |
| `bin/evidence-check .` with a third unmarked prose mention of `reload_claim` appended to `round-2-fixes.md` | exit 2, naming that new line. The markers exempt their own line only |  <!-- NAME NOT IN TREE -->
| `git show 279628b:hooks/version-check.py \| md5` vs `89333dd` | identical, `cfa60c3f9db6b018076e2927c962cb65`. The notice text did not move in round 2's fixes |
| `diff` of `^def ` lines in `tests/test_version_check.py` across `279628b..89333dd` | same fifteen names, line numbers only. No unit added or removed |
| `git status --porcelain` in the clone after every probe | clean; both mutated files restored byte-identical, verified by digest |

Probes deleted. Nothing was written in the worktree except this report.

## Inherited coordinates

| From | Coordinate | Why it was worth opening |
|---|---|---|
| round-2 | `tests/test_version_check.py:117` | round 2's finding 2, the fix this round exists to read |
| round-2 | `README.md:325`, `README.ko.md:317` | round 2's finding 1 |
| round-2 | `README.md:182` | round 2's finding 3 |
| round-1 | `hooks/version-check.py:154` | round 1's finding 1, closed by round 2 and unchanged since |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the presence-and-order assertions should be restored BESIDE the exact pin, so a rewording is checked rather than only trusted. They were collateral in `760ac3e`, not defeated: what defeated the four predicates was blindness to an ADDED clause, and a presence check's blindness is in that same direction, which the exact pin already covers for the current text | an issue at the cap, and `seal/follow-up.md` named in the PR body | the repository owner |
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md` §5 | the repository owner. Carried from rounds 1 and 2 |
| How the four-line `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships. Carried from rounds 1 and 2 |
| The `141 cases` figure in `round-1-fixes.md` | round 1's fix record | the orchestrator. Carried from round 2; nothing in this round turns on it |

## Out of verified scope

The full suite, the repository-wide lint and the typecheck were not run —
`agent-contract` §2 makes the broad gate the orchestrator's, once, after the rounds
settle. Nothing in this branch is otherwise open, so the broad run is the next step.
Answerer: the orchestrator.

## For the record the orchestrator writes

Needs a fix: yes — finding 1
Loses a record or crashes: no
Contract changes: none — `hooks/version-check.py` is byte-identical across `279628b..89333dd`, so `notice()` keeps both its signature and its output
New units: none

Finding 1 is a line a person reads that nothing pins. It removes no record and
crashes nothing, which is why the floor row is `no` while the row above it is `yes`.
The run is capped, so nothing here commissions a fix pass: finding 1 closes as
`deferred #N` once the orchestrator opens the issue, and finding 2 is a record
correction for the closing commit.

## Proof

Opened: `tests/test_version_check.py`, `hooks/version-check.py`, `README.md`,
`README.ko.md`, `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md`,
`seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-1.md`,
`round-2.md`, `round-1-report.md`, `round-2-report.md`, `round-2-fixes.md`,
`docs/review-chain-spec.md`, `seal/config.md`, `bin/test`,
`~/.claude/skills/writing-style/SKILL.md`.
