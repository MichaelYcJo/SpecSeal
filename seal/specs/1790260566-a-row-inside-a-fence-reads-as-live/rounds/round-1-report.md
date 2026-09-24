# 1790260566-a-row-inside-a-fence-reads-as-live — round 1 report

Target SHA `f754eafb`, base `c52e8350` (the branch's fork point). Reviewed in a
`git clone --no-local` of the worktree at the target SHA. First round: there is
no earlier `round-N.md`, so every finding below is new.

## How the pieces relate

The branch does what its spec says for the readers the spec names. The four
fixes hold under execution, and the vendored twin agrees with the shared rule
on every path I could build. What is open is the class boundary:

1. Two readers walk a ledger or a record with fence state, and neither the
   spec's class table nor #584 names them. `round_record.py#fenced_after`
   keeps the old delimiter rule on the record path (🟡 1). `hooks/root-migrate.py#repoint`
   is a third ledger writer that still rewrites inside a closed fence (🟡 2).
2. Because of (1), three sentences this branch wrote are false. They say every
   reader in the plugin or the repository asks the shared rule (🟡 3). The plan
   relies on exactly that docstring to reach the next reader.
3. The rest are loud-only class members, one edge of the new comment walk, one
   split inconsistency and one paperwork correction (⬜ 4 to ⬜ 8).

## Spec compliance — the account checked against the code

| The account claimed | What I found | How |
|---|---|---|
| `fence_opener`, `fence_closes`, `fence_spans`, `closed_fence_lines` implement CommonMark 4.5 | Confirmed. The bound, the backtick-info rule and the empty-closer rule are at `skills/verify/scripts/unverified_check.py:227-324` | read; shapes executed (probe P5) |
| `blank_fences`, `_liveness`, `_paragraph_ends_at`, `todo_open_rows` ask the rule | Confirmed at `:327-341`, `:363-372`, `:448-467`, `:1075-1128` | read |
| The plugin copy of `evidence_check.py` loads the reader; a copy alone uses the vendored twin | Confirmed. A copy put alone in `tools/` of a scratch repository ran at exit 0, skipped the fenced example, and `fence_rule()` returned the vendored pair | executed (P4) |
| `fold_ledger.py#open_rows` is an alias and `DRAINED_RE` left that file | Confirmed at `.github/scripts/fold_ledger.py:671`. The removed copy's separator pattern is byte-identical to `TODO_SEPARATOR_RE`. `SEPARATOR_RE` stays in use at `:503`. The one caller is `open_items` at `:681` | read |
| `gathered_fragments` counts live markers only | Confirmed. Over this tree's `CHANGELOG.md`, 110 markers before and 110 after | executed (P3) |
| `claim_lines` resumes after `-->` | Confirmed: `end --> gone_helper` now yields the name, and `&lt;!-- a --> b_name` yields `b_name` · NAME NOT IN TREE | executed (P1) |
| Q3's premise was false: no fence line in the ledger | Confirmed. No file among `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` has a line opening a fence | executed |
| `readable` moved 10 lines in 3 files (Q2) | Not re-measured. Carried from `phases/phase-1.md` | carried |
| Q5: 1,711 historical record files, one reads differently | Not re-run. Carried as the phase's measurement | carried |
| `survivors.md` answers 19 places | It has 18 data rows. The 19 counts the header. `survivor-check --range d3814875..HEAD --exempt …/survivors.md` exits 0 with "every survivor is excused by a row above (18)". Over `c52e8350..HEAD` it excuses 17, exit 0 | executed |
| Each phase carries `CONTRIBUTING.md`'s four items | All four phases carry a red case, a direction, a prompt budget of 0 and a platform note. Phase 1's direction sentence is incomplete (⬜ 8) | read |
| Q6: the vendored twin diverges from the spec | Recorded in `questions.md` Q6 and in `overview.md`. The default (a) is built and it works (P4) | read, executed |

## The classes the prompt asked me to enumerate

**Every reader with fence or comment state, and which rule it asks now.**

| Reader | Rule it asks at `f754eafb` | Named where |
|---|---|---|
| `unverified_check.py`: `blank_fences` (so `readable`), `_liveness` (so `live_lines`), `_paragraph_ends_at`, `todo_open_rows` | the shared rule | spec, in |
| `evidence_check.py`: `quoted_lines` (so `check_ledger`, `old_format_rows`, `migrate`, `reverify`) and `claim_lines` | `fence_rule()`: shared, or the vendored twin | spec, in |
| `survivor_check.py#gathered_fragments`, `settle.py#coordinates` | `live_lines` | spec, in |
| `hooks/config.py#FENCE` | its own CommonMark copy, held by an agreement case | spec, out on purpose (D8) |
| `skills/code-review/scripts/round_record.py#fenced_after` | **its own `^\s*` rule, closer may carry text** | **nowhere** (🟡 1) |
| `hooks/root-migrate.py#repoint` (a ledger writer) | **no fence state** | **nowhere** (🟡 2) |
| `skills/evidence-check/scripts/correction_check.py#rows` | no fence state | nowhere (⬜ 4) |
| `.github/scripts/fold_ledger.py#demote` | its own three-character rule, with a rider | nowhere (⬜ 5) |
| `payload_meter.py#FENCE`, `rider_check.py#comment_blocks`, `fold_ledger.py#doubled_markers`, `gather_changelog.py` | their own | #584 |
| `close_issues_on_release.py`, `issue_claims_check.py` | any indent, on purpose | spec, out (D6) |

**Every path where the vendored twin and the shared rule could disagree.**
The two regular expressions are identical, and each function has the same
body (read at `evidence_check.py:153-173`). The walk in `quoted_lines` agreed
with `closed_fence_lines` on five shapes, which were CRLF, a tilde info string holding a
tilde, a backtick info string holding a backtick, a four-backtick block quoting three,
and tab indentation (P5). The selection in `fence_rule` picks the twin exactly when this
skill's `SKILL.md` and the reader are not both beside the script (P4, and the
agreement case asserts the plugin copy's selection). The agreement case
`test_the_vendored_fence_rule_agrees_with_the_shared_one` crosses every line of
`FENCE_SHAPES` with every opener. I found no path where they disagree.

**Every caller of the old `open_rows` copy.** One: `fold_ledger.py#open_items`
at `:681`. The fold-at-release tests call `fl.open_rows`, and the S8 case
asserts its identity.

**Every closer that still ends a whole line.** `claim_lines` is now
positional. `comment_scan` (`unverified_check.py:204-212`) and
`round_record.py:784-790` were already positional. `rider_check.py#comment_blocks`
(`:237-246`) still tests `"-->" not in line` and is in #584.
`settle.py#first_cell` (`:450`) is the parallel chain's. None is unaccounted for.

## Findings

### 🟡 1 · The record generator still copies fences by the rule #491 retired

`skills/code-review/scripts/round_record.py:1319` (`fenced_after`) matches an
opener with `^\s*` and closes on any same-character run at least as long,
whatever follows it. It is the walk that copies `## Paste-ready fixes` and
`## Executed probes` into `round-N.md`. It is a fence walk on the record path,
and it is in neither the spec's class table nor #584.

Why it matters: a report whose paste-ready block quotes a fence line with an
info string (a markdown fix that shows ```` ```text ```` inside a ```` ```text ````
block) loses lines of the fix and gains prose. Executed (P6): two such blocks
with prose between them. The record copies "prose that is not a fence", and it
drops the `b` and `c` lines of the two fixes. The artefact then balances under
the new rule, so `write_record`'s `hiders_close` passes it and nothing is
raised. The output is identical at `c52e8350` and at `f754eafb`, so this is not
a regression. But after this branch it is the one fence walk on the record path
that the shared rule does not govern. `readable` and this walk now disagree
about the same report, and this module's own comments count that asymmetry
as the thing it has been bitten by three times (`opens_at`'s docstring).

The fix keeps the opener's indentation generous on purpose. Q2 measured
fenced blocks indented inside list items, and a fix written that way should
still reach the record. It takes the closer rule and the backtick-info rule,
which are the two sub-rules that decide where a block ends. Executed on P6's
input: the prose is no longer copied and `b`/`c` are kept. On a list-indented
block, the block is copied whole.

### 🟡 2 · `root-migrate` still rewrites a fenced example row

`hooks/root-migrate.py:419` (`repoint`) runs `ANCHOR_RE.sub` over the whole
ledger text, and its docstring at `:403` says "the rewrite reads exactly what
the check reads". After phase 2 the check skips a closed fence, so the
sentence is false, and this is a third ledger writer that changes the bytes of
an example. S2 exists to rule that out for `--reverify` and `--migrate`.
Phase 2 enumerated "the four walks the frame named plus that one caller", and
this writer is not among them.

Executed on a scratch text: the current substitution rewrote the fenced
`docs/a.py` example to `seal/a.py`. The fix below left the example byte for
byte and still rewrote the live row, CRLF ending included. If the smith
judges that an example should follow the move, the alternative is to correct
the docstring and say so, which is a 🟡 answered with grounds.

### 🟡 3 · Three sentences say every reader asks the shared rule

- `skills/verify/scripts/unverified_check.py:123-125`: "the one rule every
  reader in this repository that walks a fence asks".
- `skills/verify/scripts/unverified_check.py:237-238` (`fence_opener`):
  "Every reader that walks a fence asks these two functions rather than a
  pattern of its own".
- `skills/evidence-check/SKILL.md:295-296` and `:427-428`: "the one every
  reader in this plugin shares" and "the rule every reader in this plugin
  shares".

Each is false at the target. In the plugin, `fenced_after` (🟡 1) and
`payload_meter.py#FENCE` (#584) keep their own rule, and `hooks/config.py`
keeps a deliberate copy. In the repository, `fold_ledger.py#demote` and
`close_issues_on_release.py` do too. `plan.md` §*What breaks in six months*
names this docstring as the only thing that reaches the next reader. A list
that claims to be complete is the list a reviewer stops checking against.
Even with 🟡 1 fixed, `payload_meter.py` keeps the plugin sentence false until
#584 lands, so the wording needs to change in any case.

### ⬜ 4 · `correction-check` reads a fenced example row as a row

`skills/evidence-check/scripts/correction_check.py:356` (`rows`) takes every
`|` line. If a fenced example row that carries a `Corrected` note is removed,
it is reported as a dropped correction. That is loud and false, and it is in
neither the class table nor #584. The suggested home is #584's table.

### ⬜ 5 · `demote` keeps a rider that this branch made one line to answer

`.github/scripts/fold_ledger.py:276-290` (`demote`) closes a fence on any line
starting with the opener's three characters. Its own `# RIDER:` prescribes
the CommonMark closer. The script now loads the reader (`load_reader`), so
`fence_opener`/`fence_closes` are in hand. It is in neither the class table
nor #584. It is cosmetic, because it demotes a `#` line that is quoted inside a
fence in a release file. The suggested home is #584.

### ⬜ 6 · `&lt;!-->` opens an aside in the records arm

`skills/evidence-check/scripts/evidence_check.py:2242-2247` searches for `-->`
from after the four opener characters. So `&lt;!-->`, which CommonMark 0.31
defines as a complete comment, opens an aside instead. Every claim up to the
next `-->` is then dropped in silence. Executed (P1): `c52e8350` read the next
line's name, and the target reads nothing. `comment_scan` behaves the same, so
the two walks agree. `git grep` finds no `&lt;!-->` or `&lt;!--->` in the tree.
Nothing needs fixing now. It is named so that a Q1 (b) scanner does not
inherit it.

### ⬜ 7 · The ledger walks split with `splitlines`, and this repository's rule is `\n` alone

`evidence_check.py:229` (`unquoted`) and `:1605` (`migrate`) find fences over
`splitlines`, which also breaks at U+2028, U+0085 and a form feed. The
`todo_open_rows` docstring and `demote` both record why this repository splits
on `\n` alone. A fence opener could therefore be read after a U+2028 inside a
cell. Hiding rows would take a second such cell to close it, so the case is
contrived. The two walks agree with each other, so offsets hold.

### ⬜ 8 · Phase 1's failure direction names one direction only (correction)

`seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md`,
§*What `CONTRIBUTING.md` … asks*, says "`readable` blanks fewer lines". The
closer rule makes it blank MORE: a ```` ```python ```` line inside an open block
no longer ends the blanking. The format-correct reading is right in both
directions. The sentence should name the second one. This is paperwork, so it
is a correction and not a fix.

## Regression tests to plant

- `tests/test_the_record_is_generated.py`: a report whose `## Paste-ready fixes`
  holds two ```` ```text ```` blocks, each quoting a ```` ```text ```` line, with
  prose between them. Assert the record carries every fix line and no prose
  (🟡 1). It should be red at `f754eafb`, as P6 shows.
- A `hooks/root-migrate.py` case: a ledger with a fenced `docs/…` example
  above a live `docs/…` row. Assert the fenced block is byte-identical after
  `repoint` and the live row moved (🟡 2).

## Facts for the evidence ledger

- `round_record.py#fenced_after` copies verbatim fences by its own delimiter
  rule. Anchor it once 🟡 1 is answered.
- The vendored twin and the shared rule agree over `FENCE_SHAPES` crossed with
  every opener. Already P2-2. Nothing new.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The record generator's verbatim-fence walk keeps the old delimiter rule (any indent, a closer may carry text); it is named in neither the class table nor #584, and a nested info-closer drops fix lines and copies prose into the record | `skills/code-review/scripts/round_record.py:1319` | open | executed P6: same output at base and target, and after this branch the only unshared fence walk on the record path |
| 🟡 2 | `repoint` rewrites anchors inside a closed fence, and its docstring says it reads exactly what the check reads | `hooks/root-migrate.py:419` | open | read; executed on a scratch text, where the fenced example was rewritten |
| 🟡 3 | Three sentences claim every reader asks the shared fence rule, and at least four readers do not | `skills/verify/scripts/unverified_check.py:123`, `skills/verify/scripts/unverified_check.py:237`, `skills/evidence-check/SKILL.md:295`, `skills/evidence-check/SKILL.md:427` | open | read; the class table above lists the readers |
| ⬜ 4 | The correction check reads a fenced example row as a row, which is loud only | `skills/evidence-check/scripts/correction_check.py:356` | open | read; suggested home #584 |
| ⬜ 5 | The release fold's demote walk keeps its three-character fence rule while the script now loads the shared one | `.github/scripts/fold_ledger.py:276` | open | read; suggested home #584 |
| ⬜ 6 | The empty comment `&lt;!-->` opens an aside in the records arm and drops claims to the next closer | `skills/evidence-check/scripts/evidence_check.py:2242` | open | executed P1; no instance in the tree |
| ⬜ 7 | The ledger fence walks split with splitlines, not on the newline alone | `skills/evidence-check/scripts/evidence_check.py:229` | open | read; contrived |
| ⬜ 8 | Phase 1's failure direction omits that the closer rule makes the gate reader blank more | `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md` | open | read; a correction to paperwork |
| ❓ | Behaviour on Linux and Windows | the whole diff | ❓ out of verified scope | macOS only here; CI's matrix answers it at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six touched modules (`test_unverified_rows_close`, `test_evidence_check`, `test_a_record_states_what_the_tree_has`, `test_the_ledger_fragments_fold_at_release`, `test_settle_reads_before_it_removes`, `test_a_corrected_sentence_survives_elsewhere`) | 539 passed, exit 0 |
| P1: `claim_lines` at base and target over six shapes | the target reads after a closer, drops a name after `&lt;!-->`, reads the lines of a four-space fence, and does not close on a closer carrying an info string |
| P2: `todo_open_rows` at base and target over every tracked `evidence-todo.md` | no such file is tracked (0), so nothing moves |
| P3: `gathered_fragments`' rule at base and target over `CHANGELOG.md` | 110 and 110, none lost |
| P4: `evidence_check.py` copied alone into a scratch repository's `tools/` with a fenced example row | exit 0, 0 broken; `fence_rule()` is the vendored pair |
| P5: `quoted_lines` against `closed_fence_lines` over CRLF, tilde, backtick-info, nested-length and tab shapes | agree on all five |
| P6: `fenced_after` at base and target over a report with two nested info-closer blocks | identical at both, and prose is copied while fix lines are lost |
| The paste-ready fixes for 🟡 1 and 🟡 2, run on P6's input and on a scratch ledger | 🟡 1: prose no longer copied and fix lines kept; 🟡 2: fenced example byte for byte, live row moved |
| `bin/evidence-check .` at the target | exit 0; 2,097 ok, 0 drifted, 0 broken; records arm 193 names, 0 refused |
| `bin/survivor-check --range d3814875..HEAD --exempt …/survivors.md` | exit 0, 18 excused |
| a grep over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` for a line opening a fence | 0 files |
| The broad gate (full suite, lint, typecheck) | not yet: nobody has run it; it is the sealer's, after the rounds settle |

### 🟡 1

```python
    out, marker = [], None
    for i, _ in found[1]:
        line = raw[i].rstrip()
        # The opener keeps any indentation on purpose: a fix written as a
        # fenced block inside a list item is still a fix, and copying it is
        # the direction to be wrong in. Where a block ENDS is the shared
        # rule's (#491): a closer carries nothing after its run, and a
        # backtick opener's info string holds no backtick.
        opener = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker is None:
            if opener and not (opener.group(1)[0] == "`" and "`" in opener.group(2)):
                marker = opener.group(1)
                out.append(line)
            continue
        out.append(line)
        if (
            opener
            and opener.group(1)[0] == marker[0]
            and len(opener.group(1)) >= len(marker)
            and not opener.group(2).strip()
        ):
            marker = None
```

### 🟡 2

```python
        # A row inside a fenced block that closes is an example, and the
        # check skips it (#444), so the rewrite leaves it byte for byte.
        # Matched in the unquoted text and spliced from the original: the
        # two have the same offsets, as in `reverify`.
        view = ec.unquoted(text)
        pieces, at = [], 0
        for m in ec.ANCHOR_RE.finditer(view):
            path = m.group("path")
            new = repoint_path(path)
            if new != path:
                pieces += [text[at : m.start()], new, text[m.start() + len(path) : m.end()]]
                at = m.end()
        new_text = "".join(pieces) + text[at:]
```

## Paste-ready fixes

### 🟡 1 — `round_record.py#fenced_after`, the loop body

```python
    out, marker = [], None
    for i, _ in found[1]:
        line = raw[i].rstrip()
        # The opener keeps any indentation on purpose: a fix written as a
        # fenced block inside a list item is still a fix, and copying it is
        # the direction to be wrong in. Where a block ENDS is the shared
        # rule's (#491): a closer carries nothing after its run, and a
        # backtick opener's info string holds no backtick.
        opener = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker is None:
            if opener and not (opener.group(1)[0] == "`" and "`" in opener.group(2)):
                marker = opener.group(1)
                out.append(line)
            continue
        out.append(line)
        if (
            opener
            and opener.group(1)[0] == marker[0]
            and len(opener.group(1)) >= len(marker)
            and not opener.group(2).strip()
        ):
            marker = None
```

### 🟡 2 — `hooks/root-migrate.py#repoint`, replacing the `follow` closure and the `sub` call

```python
        # A row inside a fenced block that closes is an example, and the
        # check skips it (#444), so the rewrite leaves it byte for byte.
        # Matched in the unquoted text and spliced from the original: the
        # two have the same offsets, as in `reverify`.
        view = ec.unquoted(text)
        pieces, at = [], 0
        for m in ec.ANCHOR_RE.finditer(view):
            path = m.group("path")
            new = repoint_path(path)
            if new != path:
                pieces += [text[at : m.start()], new, text[m.start() + len(path) : m.end()]]
                at = m.end()
        new_text = "".join(pieces) + text[at:]
```

and the docstring's second sentence:

```text
    The checker's own `ANCHOR_RE` finds the coordinates over the text the
    check reads, `unquoted`, so the rewrite reads exactly what the check
    reads, nothing in prose and nothing in a fenced example that closes.
```

### 🟡 3 — the three sentences

```text
unverified_check.py, above FENCE_RE:
# then the info string. `fence_opener` and `fence_closes` below are the rule
# the readers listed in `fence_opener`'s docstring ask, and this pattern is
# only their first half.

unverified_check.py, fence_opener's docstring:
    The readers below ask these two functions rather than a pattern of their
    own, because five spellings of this rule is what five readers had. It is
    not every fence walk in the repository: `hooks/config.py#FENCE` is a
    deliberate copy, and the readers #584 names still keep their own.

skills/evidence-check/SKILL.md, both places:
What counts as a fence is CommonMark's rule, and the one the ledger and record
readers share:
... least as long as the opener and carries nothing after it, the rule the
ledger and record readers share.
```

Needs a fix: yes — 🟡 1 (the record generator's fence walk), 🟡 2 (the
migration writer rewrites a fenced example), 🟡 3 (three sentences claim a
completeness the tree does not have)

Loses a record or crashes: no

The broad gate has not come due: this round leaves three 🟡 open.

## Proof

Files opened for this round, all at `f754eafb` in the round's clone unless
marked:
`seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/{spec.md, plan.md, questions.md, overview.md, routing.md, survivors.md, changelog.md}`,
`…/phases/phase-2.md`, `…/phases/phase-4.md`, and the direction sections of
`…/phases/phase-1.md` and `…/phases/phase-3.md`;
`skills/verify/scripts/unverified_check.py` (diff, and `:180-225`, `:340-420`,
`:540-600`, `:1060-1130`);
`skills/evidence-check/scripts/evidence_check.py` (diff, and `:1000-1030`,
`:2240-2500`);
`.github/scripts/fold_ledger.py` (diff, and `:250-310`);
`skills/code-review/scripts/survivor_check.py` (diff);
`skills/settle/scripts/settle.py` (diff);
`skills/code-review/scripts/round_record.py` (`:625-700`, `:1290-1375`);
`hooks/root-migrate.py` (`:385-440`);
`skills/evidence-check/scripts/correction_check.py` (`:340-375`);
`tests/test_evidence_check.py` (`:515-545`);
`tests/test_unverified_rows_close.py` (`:1609-1634`);
the diffs of `CONTRIBUTING.md`, `docs/`, `skills/evidence-check/SKILL.md`,
`skills/settle/SKILL.md`, `seal/follow-up.md` and the ledger fragment; issue
#584's body (read with `gh`).
