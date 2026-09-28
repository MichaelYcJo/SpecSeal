# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — review round 3

| Field | Value |
|---|---|
| Target SHA | ea6689c6ff539b392e4061938f0ee01d3e04a48e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #650 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of work item 1790562543 (#400), the verifying round and the run's last: round 2's fixes closed on a fix, which spent the one reopening, so the run ends at this record whatever it finds. Its target is the diff of round 2's fixes, 34a029c9..f66eae08 (one commit), with the branch at ea6689c6 and draft PR #650. The job is the answers: are round 2's ⬜ 1 (the "every sealed line names seal-stamp --from" sentence narrowed in every copy), ⬜ 2 (the README side-effects pin able to fail) and ⬜ 3 (the pipe case's quoting asserted on a path with a space) actually closed. Anything still open after this round takes the filing ladder. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The narrowing splice left `nothing` alone on a line in the orchestrator's paragraph and a 92-column line in the hook's docstring | `skills/code-review/orchestration.md:554`, `hooks/sealer-stamp.py:43` | open | read; ruff check and format --check exit 0 on the hook, executed; the wrap check measures width only; deferral candidate, see Deferred |
| ⬜ 2 | Correction: three work-item files keep a line past 88 columns from the same splice | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/changelog.md:14`, `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/overview.md:39`, `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/survivors.md:6` | open | read; paperwork, outside Needs a fix; deferral candidate, see Deferred |
| 🟢 | round 2's note 1 is closed — the recovery is scoped to the lines that name a values file, in every copy | `docs/the-broad-gate.md:136`, `agents/sealer.md:159`, `skills/code-review/orchestration.md:553`, `hooks/sealer-stamp.py:42`, `skills/verify/scripts/broad_gate.py:2417` | confirmed | read, and the tree grepped for the old scope; probe M4 executed: the old sentence restored, the policy case red |
| 🟢 | round 2's note 2 is closed — the README side-effects limb can fail on its own in both editions | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:500` | confirmed | probes M1 and M2 executed: each clause deleted with its count kept, the case red |
| 🟢 | round 2's note 3 is closed — the common line's quoting is asserted on a path holding a space | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2319` | confirmed | probe M3 executed: `command=path`, the case red; the class's other member already spaced |
| carried | round 2's confirmations of round 1's findings 1–8 and the two survivors.md exemptions, and round 1's confirmed verdicts | `hooks/sealer-stamp.py#main`, `skills/verify/scripts/broad_gate.py#signal` | confirmed | carried from round 2; the fix diff touches wording, two assertions and one fixture, none of the code under them; survivor-check over the fix range exits 0, executed |
| ❓ | S17: the stamp on the owner's screen after the orchestrator's text, unfolded, in colour, once; several stamps in one message rendering whole | the harness | ❓ out of verified scope | carried from rounds 1–2; no case can observe a screen; the owner answers on the first real run after merge |

## Paste-ready fixes

```markdown
is drawn. Wherever the `SEALED` line names `seal-stamp --from`, quote it as
it stands: that command is the person's to type, and never yours. Every line
that names a values file names it, because the hook draws nothing and says
nothing where it cannot: a `python3` under 3.12, a working directory outside
the sealed clone, or a plugin older than the hook.
```
```python
macOS — where this draws nothing and the `SEALED` line in the sealer's
report, which names the file and `seal-stamp --from` wherever a values file
was written, is what remains. The same line is what remains where the main
session's working directory is outside the sealed clone, and where its
plugin predates this hook; `docs/the-broad-gate.md` §*Where the stamp is
drawn* states all three.
```
```markdown
  was sealed, and draws nothing at a subagent's end. Every line that names a
  values file names `seal-stamp --from <path>` too, quoted for the shell,
  because the hook draws nothing and says nothing where it cannot: a
  `python3` under 3.12, a session outside the sealed clone, or a plugin older
  than the hook. A run with no session says so; a values file that cannot be
  written leaves the run sealed and says nothing will be drawn. The hook
  builds each stamp whole before it claims the file, so a malformed values
  file is left pending and takes no other file's drawing with it.
```
```markdown
failure, the `SEALED` line in the sealer's report names the file and
`seal-stamp --from` wherever a values file was written — true since round
1's fix pass, which added the command to the common line — and changing the
floor is a decision about every script that copies it. The hook's docstring
states it.
```
```markdown
Round 1's fix pass (`survivor-check --range a3b76a2f..23e75f53`) reported two
places. Both share wording with the orchestrator's old sentence about the
no-session line, which the range widened to every line naming a values
file. Each place is about the no-session line alone, which still says no
Claude Code session was found and still names `seal-stamp --from`, so
neither is a claim the range corrected.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_docs_line_wrap.py`, `-q -p no:xdist`, in a `git clone --no-local` at ea6689c6 | 205 passed, exit 0 |
| `ruff check` and `ruff format --check` on the four changed .py files | exit 0 and exit 0 |
| Probe M1: README.md's side-effects clause deleted with "Four side effects" kept, then `test_both_readmes_list_the_stamp_hook` | 1 failed, exit 1 |
| Probe M2: README.ko.md's clause deleted with "네 가지 부수 효과" kept, then the same case | 1 failed, exit 1 |
| Probe M3: `DRAWN_AT_TURN_END` formatted with `command=path`, then `test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing` | 1 failed, exit 1 |
| Probe M4: the old *every sealed `SEALED` line* sentence restored in `docs/the-broad-gate.md`, then `test_the_policy_names_what_enforces_the_drawing_and_what_nothing_does` | 1 failed, exit 1; the clone clean after all four |
| `bin/survivor-check --range 34a029c9..f66eae08`, bare and with `--exempt` on this work item's survivors.md | exit 0 both; no removed wording is still standing |
| `bin/evidence-check --strict .` at ea6689c6 | exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2413`, `hooks/sealer-stamp.py:40`, `docs/the-broad-gate.md:124` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/sealer-stamp.py:92` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:683` | round 1's 🟡 3 — fixed |
| round-1 | `README.md:107`, `README.md:181`, `README.md:390`, `README.ko.md:102`, `README.ko.md:383` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2409` | round 1's ⬜ 5 — fixed |
| round-1 | `agents/sealer.md:86`, `docs/the-broad-gate.md:88` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/code-review/orchestration.md:539` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md:48` | round 1's ⬜ 8 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:2383` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2341` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py#claim` | round 1's 🟢 — confirmed |
| round-1 | `hooks/sealer-stamp.py#main` | round 1's 🟢 — confirmed |
| round-1 | the harness | round 1's ❓ — out of verified scope |
| round-2 | `docs/the-broad-gate.md:136`, `agents/sealer.md:160`, `skills/code-review/orchestration.md:553`, `hooks/sealer-stamp.py:42` | round 2's ⬜ 1 — fixed |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:488` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2311` | round 2's ⬜ 3 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2418` | round 2's 🟢 — confirmed |
| round-2 | `hooks/sealer-stamp.py#drawings` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:688` | round 2's 🟢 — confirmed |
| round-2 | `README.md:192`, `README.ko.md:188` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2469` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/orchestration.md:543` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/survivors.md:12` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — two unwrapped lines in `skills/code-review/orchestration.md:554` and `hooks/sealer-stamp.py:43` | candidate for rung 1: the branch owns both lines, and the re-wrap is whitespace only (paste-ready above) | the orchestrator of this run, who decides whether it rides the merge with release/v0.15.7 or stays in round-3.md |
| ⬜ 2 — three overlong lines in the work item's changelog.md, overview.md and survivors.md | candidate for rung 1 as a paperwork correction (paste-ready above) | the orchestrator of this run, who writes the work item's paperwork |
