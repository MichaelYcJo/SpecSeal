# 1790260566-a-row-inside-a-fence-reads-as-live — review round 1

| Field | Value |
|---|---|
| Target SHA | f754eafbb0da142f3f8a4c6b733b05fb63a4a75e |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 593 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the record generator's fence walk), 🟡 2 (the migration writer rewrites a fenced example), 🟡 3 (three sentences claim a completeness the tree does not have) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790260566 reviews the build at f754eafb against spec.md and plan.md (frame c142ecb6): one fence-delimiter rule (#491), the ledger walk skipping a closed fence (#444), one open-rows reader (#487), and a closer resuming mid-line (#220). The classes are every reader with fence or comment state, every path where the vendored twin and the shared rule could disagree, every caller of the old open_rows copy, and every closer that still ends a whole line.

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

## Paste-ready fixes

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
```text
    The checker's own `ANCHOR_RE` finds the coordinates over the text the
    check reads, `unquoted`, so the rewrite reads exactly what the check
    reads, nothing in prose and nothing in a fenced example that closes.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
