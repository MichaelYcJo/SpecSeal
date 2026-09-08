# 1788789330-the-update-notice-names-the-expensive-move — review round 4 report

| Field | Value |
|---|---|
| Target SHA | 73ab600aeb354d61ec22c08066a53bdb0a7bbd8a |
| Base for the corrections | 89333dd (round 3's target) |
| Ran by | warden on claude-opus-5 |
| PR | 233 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1 |
| Loses a record or crashes | no |

## What this round was asked

A verifying round over two prose corrections, and nothing else. Round 3 opened
one 🟡: the exact pin's docstring and ledger row S1·S2·S3 both claimed the two
cases hold together against a careless golden-string update, and round 3
measured that they do not. The orchestrator applied round 3's paste-ready
corrections itself rather than commissioning a fix pass, so those two sentences
are text nobody has read. This round reads them.

The question the round was pointed at is narrow: **is what the two sentences now
say true?** Verified by measurement rather than by reading — every shape the new
text claims passes was run with the notice and the golden string mutated
together, which is what an author rewording the notice does.

The prompt also asked whether the new text's word *exactly one* holds, whether
the row's re-anchored hash is over the file as it now stands, and whether the
`NAME NOT IN TREE` markers exempt only their own lines.

## What the round found

The corrections are true about the six shapes they list. Every one of them
passes with the golden brought along, at `18 passed`, exit 0 — measured, not
read. On that axis round 3's finding is closed.

They are wrong about one word. Both sentences say the second case holds
**exactly one** property across a rewording. It holds two, and round 3's own
report had already written the second one down.

### Finding 1 — 🟡 the second case holds two properties across a rewording, not one

`tests/test_version_check.py:108` reads:

> The one property the pair still holds across a rewording is the scope
> qualifier, because
> `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`
> looks for it independently. Everything else is carried by the message
> below, which is an instruction to a person rather than a check.

`seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3`, row
S1·S2·S3, says the same thing in its own words: *"The second case holds exactly
one property across a rewording, the scope qualifier, and the rest is carried by
the assertion message."*

That case holds a second property, at `tests/test_version_check.py:163`:

```python
claim = next((s for s in msg.replace("\n", " ").split(". ") if "/reload" in s), "")
assert claim, "the notice names no reload for the docstring to disagree with"
```

A rewording that stops naming `/reload` anywhere fires it. Executed: the notice
changed from `/reload-plugins costs no session` to `A plugin reload costs no
session`, the golden string in the exact pin updated in the same edit, whole
module → exit 1, `1 failed, 17 passed`, and the failure is
`test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` raising
`the notice names no reload for the docstring to disagree with`. That is the
same class of change as the five the sentence lists as passing — the `measured`
label dropped and the `skill bodies` subject dropped are word-level drops too,
and both do pass.

**Round 3 recorded this property itself.** `round-3-report.md:67` carries the row
`` `"/reload-plugins" in msg` | yes — the docstring case raises if no sentence
names a reload ``, in the table headed *Still held after a rewording*. The
correction was written from that report and contradicts its table.

Why it matters: the sentence exists to tell the next editor what survives a
careless golden-string update. It understates the guard by one, so an editor
reading it believes renaming `/reload-plugins` in the notice is unguarded when
it is not. The direction is the safe one — an understatement makes somebody add
a check that already exists, where an overstatement makes them trust one that
does not — which is why this is 🟡 and not 🔴.

The same sentence stands a third time in the run's paperwork, at
`round-3.md:35`: *"Both sentences now say what the pair actually holds — the
scope qualifier, and nothing else."* One defect, one row; the record site is
named here rather than given a row of its own.

A smaller nuance, not a finding: the flipped-gap shape the docstring lists
passes only while the reworded notice keeps the word `restart`. Dropping `so
restart for those` along with the flip fires
`test_the_warning_names_both_commands_in_order` instead. That case is outside
the pair, so it does not touch the *"exactly one"* claim, but it does mean the
module catches more of a rewording than the paragraph accounts for.

### Finding 2 — ⬜ an empty backtick pair where the fix note's summary should be

`round-3.md:35` and `:36` both open their Grounds cell with ``fixed at 8a31d08
— `` `` — a backtick pair with nothing inside it, where `round_record.py`
expects the fix's one-line summary. The sentence reads as though a quotation
was dropped.

This is inherited rather than new: `round-2.md` carries the same empty pair at
three places, written by the same generator. Location is under `seal/specs/`, so
it is a correction to the run's paperwork and `Needs a fix` does not count it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 Both corrected sentences say the second case holds *exactly one* property across a rewording; it holds two — the notice must name `/reload` in some sentence, and that same sentence must carry the scope qualifier | `tests/test_version_check.py:108` | open | Executed in a `--no-local` clone at `73ab600`. `/reload-plugins` replaced with `a plugin reload`, golden updated in the same edit, whole module → exit 1, `1 failed, 17 passed`, `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` raising at `tests/test_version_check.py:163`. Sibling sites, same sentence: `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3` row S1·S2·S3, and `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:35`. Round 3 had already recorded the property at `round-3-report.md:67` |
| 2 | ⬜ The fix note's Grounds cell opens with an empty backtick pair where the one-line summary belongs | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:35` | open | Read. Same at `:36`, and three times in `round-2.md`, so it is the generator's shape rather than this commit's. A record location, so `Needs a fix` does not count it |
| 3 | ✅ Round 3's finding 1 — the six shapes the corrected docstring and ledger row list as passing all do pass | `tests/test_version_check.py:101` | answered | Executed, each with the notice and the golden mutated together, whole module: overclaim appended to the reload's claim, gap flipped to `unmeasured, yet it is picked up`, restart named before the reload, `measured` label dropped, `skill bodies` subject dropped, two of the three axes dropped — `18 passed`, exit 0, every one. A rewrite-only control that changes no meaning also stays at `18 passed` |
| 4 | ✅ The scope qualifier does hold across a rewording, as claimed | `tests/test_version_check.py:164` | answered | Executed. Qualifier dropped with the golden updated → exit 1, `1 failed, 17 passed`; qualifier moved into a sentence of its own, so it no longer sits in the reload's sentence → exit 1, `1 failed, 17 passed`. Both fire the second case |
| 5 | ✅ The row's re-anchored hash is over the file as it now stands | `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3` | answered | Executed. `bin/evidence-check .` → exit 0, the fragment `12 ok · 0 drifted · 0 broken`; `bin/evidence-check . --reverify` → exit 0 and `git status --porcelain` empty afterwards, so `d2062fee` is what the current content hashes to |
| 6 | ✅ The `NAME NOT IN TREE` markers exempt only their own lines | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:70` | answered | Executed. Baseline exit 0, `0 refused`. Marker stripped off `round-3.md:70` → exit 2, that line named. An unmarked new line naming the two absent names appended to `round-3.md` → exit 2, both named at the new line. The same appended to `round-3-report.md` → exit 2, named there. Records restored byte-identical |
| 7 | ❓ out of verified scope — the `Broad gate` cell's `2561 passed, 2 skipped` and the two `ruff` exits | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:8` | unverified | §2 keeps the full suite, the repository-wide lint and the typecheck out of a round's hands, so this round ran neither. The cell names the SHA it ran at, which is auditable. What the orchestrator answers: the gate ran at `e82ef31` plus the marker commit, and `73ab600` — a one-character record change — landed after it, so the stamp is one record-only commit behind HEAD and will be further behind once round 4's own record lands |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_version_check.py -q`, `--no-local` clone at `73ab600` | exit 0, `18 passed`. Baseline |
| Control — the notice and golden rewritten with no change of meaning | exit 0, `18 passed`. The rewrite mechanism itself changes no verdict |
| Overclaim appended to the reload's claim, golden updated in the same edit | exit 0, `18 passed`. Not caught |
| Gap flipped to `unmeasured, yet it is picked up`, `restart` kept, golden updated | exit 0, `18 passed`. Not caught |
| Gap flipped, `so restart for those` dropped with it, golden updated | exit 1, `1 failed, 17 passed`; `test_the_warning_names_both_commands_in_order` fires. Outside the pair — the mutation's own artifact, recorded so the row above is not read as a clean pass |
| Restart named before the reload, golden updated | exit 0, `18 passed`. Not caught |
| `measured` label dropped, golden updated | exit 0, `18 passed`. Not caught |
| `skill bodies` subject dropped, golden updated | exit 0, `18 passed`. Not caught |
| Two of the three axes dropped, golden updated | exit 0, `18 passed`. Not caught |
| Scope qualifier dropped, golden updated | exit 1, `1 failed, 17 passed`; `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads` fires. Caught, as claimed |
| Scope qualifier moved into a sentence of its own, golden updated | exit 1, `1 failed, 17 passed`; the same case fires. Caught |
| **`/reload-plugins` replaced with `a plugin reload`, golden updated** | **exit 1, `1 failed, 17 passed`; the same case fires at `tests/test_version_check.py:163`, `the notice names no reload for the docstring to disagree with`. Finding 1** |
| `bin/evidence-check .` on the clean clone | exit 0. `seal/ledger.md` 762 ok, the fragment `12 ok · 0 drifted · 0 broken`, records arm `0 refused` |
| `bin/evidence-check . --reverify` on the clean clone | exit 0, `git status --porcelain` empty afterwards. No anchor moved |
| `bin/evidence-check .` with the marker stripped off `round-3.md:70` | exit 2, `NOT-IN-TREE … round-3.md:70`, `1 refused` |
| `bin/evidence-check .` with an unmarked new line naming the two absent names appended to `round-3.md` | exit 2, both named at the new line, `2 refused` |
| `bin/evidence-check .` with an unmarked new line appended to `round-3-report.md` | exit 2, named at the new line, `1 refused` |
| `git diff 89333dd..73ab600 -- tests/test_version_check.py hooks/version-check.py`, `^def` lines | no line added or removed. No unit added, none renamed |
| `git status --porcelain` in the clone after every probe | clean. Both mutated files asserted byte-identical against their originals at the end of each script |

Every mutation above rewrote `hooks/version-check.py` and
`tests/test_version_check.py` in one edit, because the message tail is
byte-identical in both files. That is the point of the class: an author who
rewords the notice and pastes the new text into the exact pin makes exactly this
edit.

## Inherited coordinates

Carried from earlier rounds rather than re-derived, per the coordinate rule.
Nothing here is an inherited verdict.

| Fact | Where it came from |
|---|---|
| The exact pin and the docstring case are the pair under discussion, at `tests/test_version_check.py:72` and `:137` | `round-3.md:35` |
| Round 3 measured the six shapes and found them all passing with the golden brought along | `round-3-report.md`, its probes table |
| `"/reload-plugins" in msg` is still held after a rewording | `round-3-report.md:67` — re-derived here by execution, because it is the fact finding 1 turns on |
| Round 2's findings 1–3 are closed | `round-3.md:37-39` |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | | |

## Paste-ready fixes

Finding 1, site 1 — `tests/test_version_check.py`, replacing the paragraph at
lines 108–112:

```python
    Two properties survive a rewording, and both are in
    `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`:
    some sentence of the notice names `/reload`, and that same sentence
    carries the scope qualifier. Measured with the golden brought along —
    `/reload-plugins` swapped for `a plugin reload` fires the first, and the
    qualifier moved into a sentence of its own fires the second, `1 failed,
    17 passed`, exit 1 each time. Everything else is carried by the message
    below, which is an instruction to a person rather than a check.
```

This edit changes the anchored unit's content, so the row's `d2062fee` drifts.
Run `bin/evidence-check . --reverify` in the same commit.

Finding 1, site 2 — `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md:3`,
replacing the one sentence that reads *"The second case holds exactly one
property across a rewording, the scope qualifier, and the rest is carried by the
assertion message, which a person reads rather than a checker."*:

```markdown
The second case holds two properties across a rewording: some sentence of the notice names `/reload`, and that same sentence carries the scope qualifier. Measured with the golden brought along — `/reload-plugins` swapped for `a plugin reload` fires the first, the qualifier moved into a sentence of its own fires the second, `1 failed, 17 passed`, exit 1 each time. The rest is carried by the assertion message, which a person reads rather than a checker.
```

Finding 1, site 3 — `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md:35`,
replacing *"Both sentences now say what the pair actually holds — the scope
qualifier, and nothing else — and name the message as an instruction to a person
rather than a check."*:

```markdown
Both sentences now say what the pair actually holds and name the message as an instruction to a person rather than a check. Round 4 measured that they understate it by one: the second case also fires when no sentence of the notice names `/reload`, which `round-3-report.md:67` had already recorded.
```

Finding 2 — `round-3.md:35` and `:36`, replacing each ``fixed at 8a31d08 — `` ``
with `fixed at 8a31d08 — ` and no backtick pair. The generator writes the pair
around a summary it did not get; with nothing to quote, the pair is noise.

## What was not verified, and who answers it

- The `Broad gate` row's `2561 passed, 2 skipped` and the two `ruff` exits.
  §2 keeps the full suite, the repository-wide lint and the typecheck out of a
  round's hands. **The orchestrator answers this**, including whether the stamp
  needs to move now that `73ab600` and this round's record land after it.
- Rounds 1–3's subject matter. Their verdicts are inherited and settled, and
  this round did not reopen them.

Needs a fix: yes — finding 1
Loses a record or crashes: no

## Proof block

Files opened:

- `tests/test_version_check.py`
- `hooks/version-check.py`
- `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md`
- `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3.md`
- `seal/specs/1788789330-the-update-notice-names-the-expensive-move/rounds/round-3-report.md`
- `CONTRIBUTING.md` (for the test runner's narrow form)
- `~/.claude/skills/writing-style/SKILL.md`

Commands run, all in a `git clone --no-local` of this worktree at `73ab600`:
`bin/test tests/test_version_check.py -q` (twenty-two times, once per mutation
plus baselines), `bin/evidence-check .`, `bin/evidence-check . --reverify`,
`git status --porcelain`, `git diff`, `git show`. Nothing was written in the
worktree except this report. The clone's tree is clean and both mutated files
were asserted byte-identical against their originals at the end of every probe
script; the probe scripts live in the session scratchpad, not in the tree.
