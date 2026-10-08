# Round 1 report — #867, draft PR #882

Target SHA `7e0b11932882ff35d188884b12ae19e854379709`, diff `5623d728...7e0b1193`.
Reviewed in a `--no-local` clone at the target SHA. No earlier round exists,
so nothing was carried.

## How the findings relate

```
the pull request is red twice ........................ 🔴 1, 🔴 2
  (a test that assumes `/`; a sweep the build never ran)
the ledger fragment states a claim holds that this branch broke ... 🟡 3
"every reader goes through one reader" misses one reader ......... 🟡 5
the guards that keep the one rule one are weaker than stated ..... 🟡 4, 🟡 6
wording and cost, nothing that ships wrong ....................... ⬜ 7–11
```

The spec's three formats are built as framed. The two reversed cases are
what `spec.md` §*Scope* 1 asks, the hooks stay silent, a doubled
`routing.md` label behaves as S5 says, and the heading rule holds against
markdown-it on every CommonMark corner I tried except the two the module
already names. What fails is around the build, not inside it.

## The pull request is red, and the build's own checks could not see either cause

### 🔴 1 — the Windows shard fails on a path the test spells with `/`

`tests/test_a_released_row_is_read_again_in_a_fragment.py:859` asserts
`"seal/config.md" in out.stderr`. The checker builds that refusal with
`display_name`, whose docstring keeps the spelling as the OS gives it, so on
Windows the sentence reads `seal\config.md`. Both parametrisations of
`test_a_freeze_row_written_twice_is_refused_and_nothing_is_written` fail
there (CI log of job 113099210318: `2 failed, 2744 passed, 17 skipped`).
The behaviour is right; the assertion is not. The sealer's cases already
spell this assertion with `.replace(os.sep, "/")`
(`tests/test_the_seal_is_taken_once_by_the_sealer.py:1660`).

### 🔴 2 — the release job's survivor sweep names 33 places and the work item has no `survivors.md`

The `release` job fails at the survivor sweep (CI log of job 113099209523):
33 places still carry wording this range removed. I reproduced it in the
clone, exit 1 and the same 33. Read one by one:

- **30 are regex fragments** that share character classes (`a za z0 9`,
  `f 6 12`) with the two removed coordinate copies in
  `skills/settle/scripts/settle.py` and `.github/scripts/rider_check.py`.
  Removed names: `COORDINATE_RE`, `NEW_STAMP` — NAME NOT IN TREE.
  None reads a coordinate, except
  `skills/evidence-check/scripts/evidence_check.py:154`, the grammar itself,
  and the pact anchor built beside it at lines 182–185.
- **2 are released ledger rows**, frozen. `seal/releases/0.9.1.md:119` is
  answered by this item's `Corrected · S7–S10` row. The notes cell of
  `seal/releases/0.15.0.md:56` says a `#120` at column 0 still ends a
  section, which this branch made false; its claim cell still holds and is
  re-read as `Re-read · A1`.
- **1 is `hooks/routing.py:24`**, which is still true: an unreadable
  `routing.md` is no declaration and the gate asks. The removed sentence was
  `hooks/config.py`'s.

The overview lists `evidence-check --strict` and `correction-check` as run
at the build's end, but not this sweep, which is the check CI runs. The
paste-ready `survivors.md` below takes the sweep to exit 0 in the clone
(executed). Its grounds were written by me per kind, so the smith should
read each row before committing it.

## The ledger fragment says a claim holds that this branch made false

### 🟡 3 — two `Re-read ·` rows confirm 0.19.0's `Corrected · C1`, whose vendored-copy clause no longer happens

The fragment's rows at lines 16 and 40 re-read `seal/releases/0.19.0.md`
`Corrected · C1` and say "the cited row's claim holds". That claim says *a
vendored copy names each citing row, and each other moved row where
`seal/config.md` will not read*. Since this branch, `--reverify` reads the
freeze row first. An unreadable `config.md` is refused at exit 2 there,
before any row is planned, by the plugin and by the vendored twin alike. The
case row 40 cites is the one that shows it: it now asserts exit 2 and "is
there and cannot be read"
(`tests/test_a_signer_records_a_pact_change.py:1572`). Before this branch the
same case asserted exit 1 and "may be `always`".

- What stands if this stays: a released ledger carries a re-read that
  vouches for a sentence the code contradicts, and the only case that would
  tell asserts the opposite.
- The repair: replace both rows with one `Corrected · C1` row, the claim
  with that clause rewritten (fenced below).

Of the other 59 re-reads I read nine, and those nine hold: 0.11.0 P3,
0.12.0's two `Mode` rows, 0.12.2 C4, 0.17.0 C1, 0.9.1 Q1, 0.15.0 A1's claim
cell, and 0.19.0 P1 and O1. The other 50 are unread. The 0.12.0 row needs
care. It says *the next `seal mode`
sets the first row and leaves the second*, and that is still true in its own
setting, where the second row sits below a bare-pipe line that neither
reader nor writer reaches. The nine `Corrected ·` rows also read true
against the code, including the two 0.11.4 rows that replaced re-reads.

## One reader of `seal/config.md` is left, and it crashes on the shape this branch is about

### 🟡 5 — `chain_check.py`'s pact notices open the config by their own rule

`skills/code-review/scripts/chain_check.py:4320` reads `seal/config.md`
with `read_record`. At HEAD it reads the file with `git show` decoded
`errors="replace"`, the lenient read that `config_at`'s new docstring in
`skills/evidence-check/scripts/correction_check.py` names as the defect it
removes. Under `--worktree` it reads with `open(…, encoding="utf-8")` and
catches only `OSError` (`chain_check.py:1078–1082`). An undecodable file
raises `UnicodeDecodeError` out of `read_record`; I executed that against a
one-file fixture. `pact_notices` calls it unconditionally from `main`
(`chain_check.py:5098`), and `round_record.py` runs this check with
`--worktree` before it writes a record.

- Read, not executed: that the whole `chain-check --worktree` run ends in a
  traceback. The raise itself is executed.
- The lines predate this branch. They are still in the class
  `spec.md` §*Scope* 1 closes, and the overview says every reader now goes
  through one reader (§12 of the contract: the class, not the coordinate).

## The guards that keep each rule one are weaker than they say

### 🟡 4 — S7's case cannot fail on the property it is named for

`tests/test_settle_reads_before_it_removes.py:1844` asserts that
`coordinate_paths(line)` equals the paths of `ANCHOR_RE` matches. That is
how `coordinate_paths` is written, so the case is red only when the
function is missing. Its docstring says as much: it was red against
5623d728 because `settle.py` there had no `coordinate_paths`. S7 asks that
settle attribute *the paths it attributed through its own copy*, and the
"0 of 8,218 spans changed" fact lives only in a deleted probe. The released
ledgers are frozen, so keeping the 0.20.0 pattern in the test as the oracle
makes the fact a case.

### 🟡 6 — the S12 heading grep lets a `#{2,3}` spelling through, and one stands in the rule's own file

`HEADING_SPELLING` (`tests/test_a_format_has_one_reader.py:75`) matches
`#{1,6}` and `startswith("#`. The payload meter's old `^#{2,3} ` would have
passed it, and
`LOOSE_HEADING = re.compile(r"^#{2,3}\s.*not verified", re.I)` still stands
at `skills/verify/scripts/unverified_check.py:158`. It is asked only of
lines `headings` already took, so the heading decision is the one rule's.
What it adds is a `^` with no indentation allowed, so an indented
`   ### not verified` at a base revision is a heading that the relaxed match
refuses. The module docstring says the next copy is red on arrival, and
that holds only for two spellings.

## Wording and cost — nothing here ships a wrong behaviour

### ⬜ 7 — the vendored config twin and the plugin's reader differ on one more shape than the docstring says

Executed: a row holding a form feed or U+2028 is a row for
`vendored_config_rows`, which reads GFM lines, and no row for
`hooks/config.py`, whose walk splits on `str.splitlines`. The twin's
docstring (`evidence_check.py:3919`) says fences and comments are "the one
way the two differ". The plugin side is a known exemption
(`tests/test_every_reader_ends_a_line_where_gfm_does.py:689`); the sentence
is what is wrong.

### ⬜ 8 — "read where a renderer shows it" is true for fences only

Executed: in the checker, `## B` inside an HTML block (`<details>` with no
blank line) or a multi-line HTML comment is still a heading and opens a
section. markdown-it reads neither. Over every tracked `.md` file, neither
the checker nor `unverified-check` reads a heading that markdown-it does not
(0 and 0), so no row moves today. The property case skips every line the
oracle hides, so it cannot see this. Which lines a reader hides is #872's
family, as `spec.md` §*Scope* says. The correction is to the standing
statement in `spec.md:200`, which is folded into `docs/` at the release:
*outside a closed fence*.

### ⬜ 9 — a doubled `Pact` row lost the sentence that said how to fix it

`spec.md` §*Data & interfaces* ordered `pact_declaration`'s doubled-row
sentences replaced by the generic one, so this is as framed. But `Pact` is
the one list-valued row, and "`Pact` appears 2 times — one value" can be
read as *one pact only*. The old sentence said to list every pact in one
row, separated by `;` (`hooks/config.py:977`).

### ⬜ 10 — a garbled clause in `hooks/routing.py:165`

"since #867 a label it is shown twice has no value", on a line past the
file's wrap.

### ⬜ 11 — `resolve_unit` rebuilds the shown lines once per anchor

`markdown_lines(text)` runs `unquoted` and `gfm_lines` over the whole file
for every quoted `.md` locator (`evidence_check.py:713`), so a file cited by
many rows is blanked once per row. One run each, so noisy: `bin/evidence-check
--strict .` took 13.17 s at 5623d728 and 15.35 s at the target, with about
95 more ledger rows. The commit advisor runs the same checker.

## Confirmed

- **Both reversed cases are what Scope 1 asks.** `seal mode` is named among
  the commands that print a refusal and exit 2, and S2 names two `Mode`
  rows refused with both lines. The folder line is still printed.
- **Hooks stay silent.** `hooks/mode-gate.py:164` reads `refused` as
  silence. `hooks/evidence-advisor.py:225` quotes no refusal and only keeps
  the freeze on. No hook calls `seal mode`, `fold-check`, `broad-gate` or
  `correction-check`. `seal mode --check` in the hygiene workflow exits 0
  on this repository (executed).
- **`routing.md`.** Executed: a doubled `Review` gives no declaration; a
  doubled `Planning` keeps the declaration with `planning: None`; a
  `Review` quoted in a closed fence does not double. A `Review` row in a
  second two-cell table further down the file does double, because
  `table_rows` reads every table. It was last-wins before, and none of the
  86 declarations holds one.
- **CommonMark corners.** Read and executed against markdown-it: four
  spaces, a tab before the run, `#hello`, `#######`, `#120)`, a closing run,
  an empty `#`, `> #` and `- #` all agree. Setext and a heading indented
  under a list item are the module's two stated limits. The twin is the
  same code. The guard modules and the heading-rule module pass in the
  clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The Windows shard fails: the case asserts `seal/config.md` and the refusal names `seal\config.md` | `tests/test_a_released_row_is_read_again_in_a_fragment.py:859` | open | CI log of job 113099210318, 2 failed; `display_name` keeps the OS spelling by design |
| 🔴 2 | The release job fails: the survivor sweep names 33 places and the work item holds no `survivors.md` | `.github/workflows/hygiene.yml:262` | open | reproduced in the clone, exit 1, 33 places; with the paste-ready file, exit 0 |
| 🟡 3 | Two `Re-read ·` rows say 0.19.0 `Corrected · C1` holds; its clause on a vendored copy reading an unreadable config is now an exit-2 refusal | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:16` | open | the case row 40 cites asserts exit 2 since this branch (`tests/test_a_signer_records_a_pact_change.py:1572`) |
| 🟡 4 | S7's case compares `coordinate_paths` with the grammar it is built from, so it is red only when the name is missing | `tests/test_settle_reads_before_it_removes.py:1844` | open | read; the docstring's own red is the missing attribute |
| 🟡 5 | `chain_check.py`'s pact notices read `seal/config.md` by their own rule: lenient at HEAD, and a `UnicodeDecodeError` under `--worktree` | `skills/code-review/scripts/chain_check.py:4320` | open | executed: `read_record` raises on an undecodable file; the call from `main` is read; lines predate the branch |
| 🟡 6 | The S12 heading grep misses a `#{2,3}` spelling, and `LOOSE_HEADING` stands in the rule's own file | `tests/test_a_format_has_one_reader.py:75` | open | read; `skills/verify/scripts/unverified_check.py:158` |
| ⬜ 7 | The config twin and the plugin's reader differ on a form feed or U+2028 in a row; the docstring says fences and comments are the only difference | `skills/evidence-check/scripts/evidence_check.py:3919` | open | executed probe over eight shapes, two differ |
| ⬜ 8 | The standing statement says a heading is read where a renderer shows it; the checker blanks closed fences only, so HTML blocks and comments still open sections | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md:200` | open | executed; the tree holds none (0 and 0); the hiding rule is #872's family |
| ⬜ 9 | A doubled `Pact` row's refusal no longer says to list every pact in one row | `hooks/config.py:977` | open | as `spec.md` §*Data & interfaces* ordered |
| ⬜ 10 | A garbled clause and an over-long line in `table_rows`' docstring | `hooks/routing.py:165` | open | read |
| ⬜ 11 | `resolve_unit` rebuilds `markdown_lines` once per quoted `.md` anchor | `skills/evidence-check/scripts/evidence_check.py:713` | open | executed, one run each: 13.17 s at base, 15.35 s at target |
| 🟢 | The two reversed cases are what `spec.md` §*Scope* 1 and S2 ask | `tests/test_the_mode_is_a_row_and_a_command.py:694` | confirmed | read against the spec; the folder line is still printed |
| 🟢 | Hooks read a refusal as silence and no hook reaches a command that now exits 2 | `hooks/mode-gate.py:164` | confirmed | read; `hooks/evidence-advisor.py:225`; `seal mode --check` exit 0 executed |
| 🟢 | A doubled strict `routing.md` label is no declaration and a doubled optional one is unanswered | `hooks/routing.py:242` | confirmed | executed probe of four shapes |
| 🟢 | The two 0.11.4 rows replaced by `Corrected ·` rows, and the other seven corrections, state the code as it stands | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:89` | confirmed | read against the code; `bin/evidence-check --strict .` exit 0 executed |
| ❓ | The unreadable-config fixtures on Linux and on the three Windows shards that passed | `tests/test_a_released_row_is_read_again_in_a_fragment.py:874` | ❓ out of verified scope | CI shows them green (read); I ran macOS only. The orchestrator answers it from the next CI run after 🔴 1 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named | exit 0, 436 passed |
| `bin/test tests/test_one_heading_rule_holds_to_commonmark.py tests/test_a_format_has_one_reader.py` | exit 0, 21 passed |
| `python3 skills/code-review/scripts/survivor_check.py --range 5623d728...7e0b1193` | exit 1, 33 places |
| the same with the paste-ready `survivors.md` under `--exempt` | exit 0, every survivor excused (33) |
| `bin/evidence-check --strict .` at the target, then at 5623d728 | exit 0 both; 15.35 s and 13.17 s |
| `bin/correction-check --range 5623d728...7e0b1193` | exit 0, no merge commit in the range |
| `python3 skills/implement/scripts/seal.py mode --check` | exit 0, folder and row agree |
| probe: plugin config reader against `vendored_config_rows` over eight shapes | six equal; a form feed and a U+2028 in a row differ |
| probe: lines the checker's and `unverified-check`'s shown lines read as headings where markdown-it reads none, every tracked `.md` | 0 and 0 |
| probe: `## B` inside an HTML block, a multi-line comment, a list item | the checker reads a level-2 heading in the first two; markdown-it reads none in any |
| probe: `routing.parse` over a doubled `Review`, a doubled `Planning`, a fenced `Review`, a `Review` in a second table | None, unanswered `planning`, a declaration, None |
| probe: `chain_check.read_record` with `--worktree` over an undecodable `seal/config.md` | raises `UnicodeDecodeError` |
| read, not executed by me: the CI logs of jobs 113099210318 and 113099209523 | the two failures under 🔴 1 and 🔴 2 |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 8's mechanism: which lines a reader hides (HTML blocks, comments) before it asks the heading rule | #872, which the frame filed for the seven live-line rules | the repository owner, who triages #872 |

## Paste-ready fixes

### 🔴 1

```python
    assert "`Ledger frozen from` appears 2 times — one value" in out.stderr
    assert "seal/config.md" in out.stderr.replace(os.sep, "/"), out.stderr
```

### 🔴 2

`seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md`:

```markdown
# Survivors — config rows, the ledger coordinate and a markdown heading have one reader

`survivor-check --range 5623d728...7e0b1193` named 33 places that still carry
wording this item's range removed. Each was read. Thirty are patterns of their
own that share only character classes with the two removed copies of the
coordinate grammar; two are released ledger rows, frozen by `Ledger frozen
from`, which this item's fragment answers; one is a sentence that is still
true where it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.9.1.md` | **A gate is not a writer.** hooks/config.py#declared_mode folds a file that will not open into *declared nothing*, which is right for seal mode | a released ledger row, frozen by `Ledger frozen from`; this item's fragment carries its `Corrected · S7–S10` row |
| `seal/releases/0.15.0.md` | heading_level keeps the reader's own test for a heading — startswith("#") — and adds only the depth, so a #120 at column 0 still ends a | the notes cell of a released ledger row, frozen by `Ledger frozen from`; its claim cell is re-read in this item's fragment (`Re-read · A1`), and the notes record the reading of their date |
| `hooks/cmdline.py` | \{[A-Za-z_][A-Za-z0-9_]*\})?" r"(?:<<< | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | r"(?:<[A-Za-z][A-Za-z0-9-]*" r"(?:[ \t]+[A-Za-z_:][A-Za-z0-9_.:-]*" r"(?:[ \t]*=[ \t]*(?:[^ \t\"'=<>]+ | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/pact_check.py` | r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]+)" r"(?:(?=[/#])(?!/\"<)" r" | the pact anchor, which reads a pact name and no ledger coordinate; it shares character classes with the removed copy |
| `skills/evidence-check/scripts/evidence_check.py` | \\\")+\")" r"@(?P<hash>[0-9a-f]{6,12})" | the pact anchor beside the coordinate's one grammar, in the checker that owns both; it reads a pact clause |
| `skills/evidence-check/scripts/pact_check.py` | r"(?P<item>[^\s@]+)@(?P<hash>[0-9a-f]{6,12})" | a pact review's record id, `<work-item-id>@<content hash>`, which is no coordinate |
| `docs/round-record-spec.md` | grep -oE '[0-9a-f]{7,40}\.\.[A-Za-z0-9@_/.-]+' | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/answers.py` | r"[^A-Za-z0-9]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | r"[A-Za-z0-9_.-]+" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | </[A-Za-z][A-Za-z0-9-]*[ \t]*>)[ \t]*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/one_heredoc.py` | D is [A-Za-z0-9_]+. | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/one_heredoc.py` | r"[A-Za-z0-9_]+" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/root-migrate.py` | r"^[0-9]{9,10}-[A-Za-z0-9._-]+$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/worktree-guard.py` | r"[^A-Za-z0-9-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | **Item 2, an issue number keeps its sentence.** A # followed by digits that no ASCII word character continues is an issue number, whatever the | another work item's frame, a record of its own time |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/plan.md` | - **The anchor grammar.** skills/evidence-check/scripts/evidence_check.py#ANCHOR_RE needs a path made of [A-Za-z0-9_.@/-], holding a / or a | another work item's plan quoting the coordinate pattern of its time |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/spec.md` | It matches [A-Za-z0-9_.-]+. | another work item's frame quoting a pattern of its time |
| `skills/code-review/scripts/round_record.py` | r"(?<![A-Za-z0-9_])" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/evidence_check.py` | r"[A-Za-z_][A-Za-z0-9_.]*" | the coordinate's one grammar, which the removed copies in `skills/settle/scripts/settle.py` and `.github/scripts/rider_check.py` spelled again |
| `skills/evidence-check/scripts/evidence_check.py` | r"[A-Za-z0-9_.-]+" | the pact anchor built beside the coordinate's one grammar; it reads a pact name |
| `skills/evidence-check/scripts/evidence_check.py` | r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>" | the pact anchor built beside the coordinate's one grammar; it reads a pact name |
| `skills/evidence-check/scripts/evidence_check.py` | # RIDER: the two [A-Za-z0-9_.@/-] repetitions below overlap, so the path | a rider on one of the checker's own path patterns, true as it stands; it shares character classes with the removed copy |
| `skills/evidence-check/scripts/evidence_check.py` | r'[A-Za-z][A-Za-z0-9+.-]*://[^\s"]*' | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/evidence_check.py` | r"\d+(?![A-Za-z0-9_])" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/implement/scripts/seal.py` | r"[^A-Za-z0-9._-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/broad_gate.py` | r"^ ([A-Za-z0-9_-]+):\s*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/session_cost.py` | r"[A-Za-z_][A-Za-z0-9_]*=" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/session_cost.py` | r"[^A-Za-z0-9-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `tests/test_a_row_points_by_content.py` | r"[A-Za-z0-9_./-]+\.(?:py | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `tests/test_ci_gives_the_checks_what_they_need.py` | r"^ ([A-Za-z0-9_-]+):\s*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/routing.py` | A file that cannot be read is not an answer somebody gave, so the gate goes back to asking. | true as it stands: a `routing.md` that cannot be read is no declaration and the commit gate asks; the removed sentence was `hooks/config.py`'s, whose reader now refuses instead |
| `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/spec.md` | A file that cannot be read is not an answer somebody gave", and 1790635413 pinned R2 the same way. | another work item's frame, a record of its own time |
```

### 🟡 3

Delete the fragment's rows at lines 16 and 40 (the two `Re-read · Corrected ·
C1` rows) and add one row. The claim is 0.19.0's with one clause rewritten;
the hashes are the ones the fragment already carries for these units.

```markdown
| Corrected · C1 · `evidence-check --reverify`, in place and under `--into`, plans every ledger write without making one, records the pact changes the plan owes, and writes the plan only after; it appends one row per re-read ledger row citing a clause of a pact the signer's `Pact` row declares, and per such row with a BROKEN coordinate, to `seal/pact-changes/<work-item-id>.md` (created with its header), and prints a `recorded` line; `Pact notify` filters (`always` adds `—` rows, `never` records nothing); the id is `--into`'s fragment, else the branch's declared work item, else a `LEFT` line and exit 1; a coordinate whose last recorded row for the same clause and ledger row says the same move or the same BROKEN is not appended again, so a change re-landed after its revert is; a record that will not read, decode or parse is named and left; a `seal/config.md` that is there and will not read is refused at exit 2 before anything is planned, by the plugin and by a vendored copy alike, and nothing is re-stamped or recorded; a vendored copy names each citing row, and each other moved row where `seal/config.md` holds a plain `Pact` row and a plain `Pact notify` row that both carry a value, or holds a line that names a pact by `PACT_WORD` (as written or `NFKC(html.unescape)`, the plugin's word and predicate, held equal) and is neither a plain `\| Pact \| … \|` nor a plain `\| Pact notify \| … \|` row, reading a two-cell row (`CONFIG_ROW_RE`, on a GFM line no `str.splitlines`-only character cuts) by its item alone unless it stands directly above a line GFM may read as a delimiter row (`UNDER_A_HEADER`: block-quote markers, a vertical tab or form feed, and a one-column row with no pipe included), where it is a table's header and is read whole with no `\|` asked, and asking no `\|` of a line in a file holding an HTML table cell (`HTML_CELL`), and records nothing; a `Pact notify` row written twice has no value, so `always` cannot be ruled out; a row left whole moved nothing and records nothing; the ledger bytes are what they are without a `Pact` row | `seal/releases/0.19.0.md#"### 1791239490-a-repository-that-keeps-a-pact-is-a-signer">"Corrected · C1 ·"@d1aa3380`, `skills/evidence-check/scripts/evidence_check.py#frozen_from@2f3469f9`, `skills/evidence-check/scripts/evidence_check.py#vendored_config_text@228ea1c7`, `tests/test_a_signer_records_a_pact_change.py#test_a_vendored_copy_whose_config_will_not_read_leaves_the_row@0fa961e4`, `tests/test_a_signer_records_a_pact_change.py#test_a_pact_row_that_will_not_read_leaves_the_row@732701e9` | **Read** 2026-10-08: the cited row's claim against `frozen_from`, which `--reverify` reads before it plans. **Executed** 2026-10-08: both cases, green | 2026-10-08 | Corrected 2026-10-08 by work item 1791384156-config-rows-coordinates-and-headings-have-one-reader: the clause on a vendored copy naming moved rows where `seal/config.md` will not read no longer happens, because the freeze row is read first and an unreadable file is refused there (#867) |
```

### 🟡 4

In `tests/test_settle_reads_before_it_removes.py`, add `import re` to the
imports and replace the S7 case:

```python
# The coordinate pattern `settle.py` kept until #867, frozen here as the
# oracle S7 is measured against. The released ledgers do not change, so the
# paths this copy attributed there are the paths `coordinate_paths` must.
SETTLE_COPY_AT_0_20_0 = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r"#(?:\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"(?:>\"(?:[^\"\n]|\\\")+\")?"
    r"@[0-9a-f]{6,12}"
)


def test_settle_attributes_the_paths_its_own_copy_attributed():
    """S7 of #867. `settle` reads `evidence_check.py#ANCHOR_RE` now; over
    this repository's released ledgers every path it attributes is the one
    its own copy attributed, so no segment moved. Red by narrowing the
    checker's locator, which the old copy does not follow."""
    assert not hasattr(settle, "COORDINATE_RE"), "a second grammar is back"
    seen = 0
    for path in real_ledgers():
        with open(path, encoding="utf-8") as f:
            for line in f.read().split("\n"):
                want = [m.group("path") for m in SETTLE_COPY_AT_0_20_0.finditer(line)]
                assert settle.coordinate_paths(line) == want, line
                seen += len(want)
    assert seen > 8000, seen
```

### 🟡 5

`skills/code-review/scripts/chain_check.py`: a decode error under
`--worktree` is a file this run cannot read, as a missing one is.

```python
    if WORKTREE:
        try:
            with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
                return f.read()
        except (OSError, ValueError):
            return None
    return git(root, "show", f"HEAD:{rel}")
```

And in `pact_notices`, read the config the way `correction_check.py#config_at`
reads a blob, and say so when it will not read:

```python
def config_at_head(root, rel):
    """(text, refusal) for REL as HEAD holds it, decoded strictly: the two
    states `hooks/config.py#config_text` tells apart on disk (#867)."""
    if WORKTREE:
        try:
            with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
                return f.read(), None
        except FileNotFoundError:
            return None, None
        except (OSError, ValueError) as exc:
            return None, f"{rel} is there and cannot be read as UTF-8 text ({exc})"
    kind = git(root, "cat-file", "-t", f"HEAD:{rel}")
    if kind is None:
        return None, None
    if kind.strip() != "blob":
        return None, f"{rel} at HEAD is a {kind.strip()}, not a file"
    out = subprocess.run(
        ["git", "-C", root, "cat-file", "blob", f"HEAD:{rel}"], capture_output=True
    )
    try:
        return out.stdout.decode("utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"{rel} at HEAD is not UTF-8 text ({exc.reason})"
```

```python
    config_text, unreadable = config_at_head(root, config_rel)
    ...
    notices = []
    if unreadable:
        notices.append(
            (
                config_rel,
                0,
                f"the pact relationship was not read: {unreadable}. Nothing "
                "about a pact moves this check's exit status, so this is a notice",
            )
        )
    pacts, notify, refusals = config.pact_declaration(config_text or "")
```

### 🟡 6

`tests/test_a_format_has_one_reader.py`: any brace count after a `#`.

```python
HEADING_SPELLING = re.compile(r'#\{\d|startswith\(\(?"#')
```

`skills/verify/scripts/unverified_check.py:158`: the relaxed match allows the
indentation the rule allows, and is named as what it is.

```python
# The heading matcher for a base revision: a TEXT match, asked only of lines
# `headings` already took by `heading_level`, with the indentation that rule
# allows. It decides the wording, never whether the line is a heading.
LOOSE_HEADING = re.compile(r"^ {0,3}#{2,3}[ \t].*not verified", re.I)
```

and its exemption, beside the others in `HEADING_EXEMPT`:

```python
    (
        "skills/verify/scripts/unverified_check.py",
        "LOOSE_HEADING = re.compile",
    ): "a base revision's relaxed wording, asked only of lines heading_level took",
```

Needs a fix: yes — 🔴 1 and 🔴 2 (the pull request is red), 🟡 3 (a
re-read that vouches for a broken claim), 🟡 4, 🟡 5, 🟡 6

Loses a record or crashes: yes — `chain_check.py --worktree` raises
`UnicodeDecodeError` from `read_record` on an undecodable `seal/config.md`
(🟡 5; the raise executed, the path from `main` read; the lines predate
this branch)

## Proof

Opened: `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/`
`spec.md`, `overview.md`, `changelog.md`, `handoff.md`, `routing.md`; the
fragment `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md`;
the diffs of `hooks/config.py`, `hooks/mode-gate.py`, `hooks/evidence-advisor.py`,
`hooks/routing.py`, `templates/config.md`,
`skills/evidence-check/scripts/evidence_check.py`,
`skills/evidence-check/scripts/correction_check.py`,
`skills/evidence-check/scripts/pact_check.py`, `skills/settle/scripts/settle.py`,
`skills/settle/scripts/fold_check.py`, `skills/implement/scripts/seal.py`,
`skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/unverified_check.py`,
`skills/verify/scripts/payload_meter.py`, `skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/survivor_check.py`, `.github/scripts/rider_check.py`,
`skills/evidence-check/SKILL.md`, `tests/commonmark_oracle.py`,
`tests/test_a_signer_declares_its_pact.py`, `tests/test_a_signer_records_a_pact_change.py`,
`tests/test_the_mode_is_a_row_and_a_command.py`, `tests/test_settle_reads_before_it_removes.py`;
whole or in part `tests/test_one_heading_rule_holds_to_commonmark.py`,
`tests/test_a_format_has_one_reader.py`, `tests/test_evidence_check.py` (the
twin cases), `tests/test_a_released_row_is_read_again_in_a_fragment.py`
(830–905), `tests/test_every_reader_ends_a_line_where_gfm_does.py` (599–712),
`.github/workflows/hygiene.yml` (340–400), `seal/releases/0.9.1.md`,
`0.11.4.md`, `0.12.0.md`, `0.15.0.md`, `0.19.0.md` at the cited rows, and
`seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/survivors.md`
for the format. The CI logs of jobs 113099210318 and 113099209523.
