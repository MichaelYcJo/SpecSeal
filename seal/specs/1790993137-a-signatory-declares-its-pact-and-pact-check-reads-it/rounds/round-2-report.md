# Round 2 report — #647 steps A and B (PR #735), verifying round 1's fixes

| Field | Value |
|---|---|
| Round | 2 (verifying) |
| Target SHA | 2a0243b2 |
| Fix range read | `0487fb5b..62726cb9`, then the close commit `2a0243b2` |
| Ran by | specseal:warden on claude-opus-5-5 |

The round ran in a scratch clone (`git clone --no-local`) checked out at the
target SHA, under the session scratchpad. Nothing in the worktree was written
but this file. The clone, its probe files and its outputs were removed before
hand-over.

## What this round was asked, and how the account was read

The target is round 1's fix diff, not the branch. The account is the prompt,
`rounds/round-1.md`, `rounds/round-1-report.md`, the fix commits' messages,
the orchestrator's fixes table, and the corrected ledger rows. Each claim was
checked against the code at `2a0243b2`.

- **Claimed** (prompt): "The fix table lists every reader in
  `evidence_check.py` with the reason it needs no blanking." **Found**: no
  such list exists at the target. The fixes table holds `bf035a2f; ledger
  notes f299c650` for 🟡 3, and `round-1.md` carries nothing more. The only
  account is one sentence, in commit `bf035a2f` and in P5's `Corrected` note:
  every other reader "either cannot match inside one or already reads
  blanked text". So the list was derived here from scratch, by what each
  reader reads (below). It holds, with one documented exception the
  sentence leaves out.
- **Claimed** (commit `bf0333e2`, P8's note): "Both of the table's refusals
  now read after the words *the pact*." **Found**: two of the five sentences
  printed after *the pact* were changed. Three others, from
  `remote_entries`, still print as *the pact the `Signatory` table holds an
  empty row* and *the pact `<url>` holds a space* (⬜ 14, executed).
- **Claimed** (commit `bf0333e2`, P8's note): the stray-row refusal means
  "the signatories below it cannot go unread in silence". **Found**: true
  for a row the walk stops at. **Not** true for a row below a blank line
  inside the table, which the walk never reaches (🟡 12, executed).
- **Claimed** (commit `532554f1`, P9's note): "anything starting
  `pact:<name>` for this pact that does not parse is `REFUSED`". **Found**:
  true, and wider than it should be. Prose that names the pact, which is no
  citation at all, is refused at exit 2 (🟡 13, executed).
- **Claimed** (commit `9a277382`): each of the four new branch cases was seen
  red by breaking it. **Found**: the cases exist and pin the printed
  sentences. I broke `declared_pacts`' unreadable answer myself and the
  config case went red. The other three reds are the smith's account, not
  re-run here.

## Round 1's findings at their fix commits

Every fix was broken once in the clone, one at a time, and the planted case
was run. Each went red, and the tree was restored after each.

| Round 1 finding | Fix | Broken how | Case run | Result |
|---|---|---|---|---|
| 🟡 1 | `2ba6a896` | `--full-history` dropped | the merge case | 1 failed |
| 🟡 2 | `bf0333e2` | the stray row not recorded | both stray cases, 3 ids | 3 failed |
| 🟡 3 | `bf035a2f` | `stated_names` reads the raw line | the two new anchor cases | 2 failed |
| 🟡 3 | `bf035a2f` | `stated_coordinates` reads the raw line | the two new anchor cases | 1 failed |
| 🟡 4 | `532554f1` | the mention loop never refuses | the three malformed ids | 3 failed |
| ⬜ 5 | `1e1bb977` | an unreadable config answered as no row | the config case and the reader's case | 2 failed |
| ⬜ 9 | `6fa9cb60` | the self-listed check disabled | the self-listed case | 1 failed |

### 🟡 1 holds

`skills/evidence-check/scripts/pact_check.py:254`. `History.commits` passes
`--full-history` to both lists. `other()` still says `--not HEAD`, and HEAD's
list is read first, so the NOT TAKEN branch is unchanged. A merge listed this
way holds one parent's text, so no verdict moves. One consequence is
cosmetic: the SUPERSEDED sentence names the first matching commit in HEAD's
list, which may now be a merge that kept the clause rather than the commit
that wrote it. Its text is that version, so the sentence stays true.

### 🟡 2 holds for the shape it names, and the class has one more (🟡 12)

### 🟡 3 holds, and the reader list is re-derived here

Every regular-expression read in `evidence_check.py` (60 call sites, found by
searching for `finditer`, `findall`, `search`, `match`, `fullmatch`, `sub`
and `split`) was sorted by what it reads:

| Reader | What it reads | Pact anchor |
|---|---|---|
| `old_format_rows`, `malformed_rows`, `migrate` | ledger rows with `OLD_COORD_RE` after `ANCHOR_RE` | blanked first (P5) |
| `stated_names`, `stated_coordinates` | records with `RECORD_NAME_RE`, `RECORD_COORD_RE` | blanked first (this fix) |
| `refused_coordinate` | what `malformed_rows` left of a cell | reads blanked text |
| `check_text`, `reverify`, `stated_stamps` | `ANCHOR_RE` matches only | cannot match inside one, except a heading that holds a whole `path#name@hash` |
| `ledger_table_rows`, `overflow_rows` | unescaped `\|` positions | a locator writes `\|` escaped |
| `claim_lines` | the marker and comment positions | reads no coordinate |
| `heading_slugs`, `tree_names`, `coordinate_misses`' token read | the tree's files, not the records | not a reader of records |
| the date readers (`Checked`) | date cells | not a reader of anchors |

No reader was missed. The exception in the fourth row is the one
`PACT_ANCHOR_RE`'s own comment already names as a known limit: a pact
heading whose text holds a whole stamped coordinate is read by `check_text`
as one. The fix's account says every other reader "cannot match inside one",
which is the claim without that limit. That is a sentence and not a defect,
so it is not a finding. A clause heading carrying a ledger stamp is not a
shape anyone writes.

### 🟡 4 holds for the three malformed shapes, and it now refuses prose (🟡 13)

### ⬜ 5, ⬜ 6, ⬜ 8, ⬜ 9 and ⬜ 11 hold

- ⬜ 5: `declared_pacts` answers no file as no row, and a file that is there
  and will not read as None. `pact_check.py:429` is now its one production
  caller and prints `UNREADABLE` for None. The old in-line read and its
  `lexists` check are gone, and nothing else lost them: no file still reaches
  `ONE-SIDED` through an empty row list, as before.
- ⬜ 6: `seal/releases/0.15.4.md`'s claim cell names all three patterns, under
  a dated `Corrected` note that says the code is unchanged.
- ⬜ 8: four cases pin the four sentences (`9a277382`).
- ⬜ 9: a pact listing its own repository is `REFUSED` in the table's own
  words.
- ⬜ 11: the word case now reads `templates/config.md` §*Pact*, the pact lines
  of both READMEs and the config skill, every string constant of
  `pact_check.py`, and `pact_notices` and `PACT_NOT_HERE` of `chain_check.py`.
  The refusals `pact-check` prints from `hooks/config.py` are still unheld
  (⬜ 15).

### ⬜ 7 and ⬜ 10 stand as answered

Both were answered by the orchestrator with no change. I read both answers
and they hold. For ⬜ 7, round 1's identity probe showed `seal.py`'s name is
the same function object, so the re-pointed coordinate names the unit the
claim is about. For ⬜ 10, the cost named is small and local.

### The ledger

- `seal/releases/0.15.4.md` MALFORMED: corrected in place, dated.
- `seal/releases/0.9.0.md` R1 and `seal/releases/0.16.0.md` P1: each re-read
  under a dated note, its `Checked` cell extended with 2026-10-03, and the
  hashes moved to the new `stated_names` and `stated_coordinates`.
  `evidence-check --strict` reads them `OK` (executed).
- Fragment P1: the claim is corrected in place and the new case is cited.
- Fragment P5: a `Corrected` note names the two readers the `.sub`
  enumeration missed and cites both new cases. The claim cell names only the
  three `.sub` readers, but what it says about them is true, and its
  consequence ("reports its local coordinate alone") is true now.
- Fragment P8: a `Corrected` note. It repeats the *both refusals* sentence
  that ⬜ 14 finds incomplete, so it moves with that fix.
- Fragment P9: a `Corrected` note covering 🟡 1, 🟡 4, ⬜ 5, ⬜ 9 and ⬜ 8.
  Its Code grounds cite one of the three `UNREADABLE` cases and not the
  pact-level stray case (⬜ 16).

## Findings from execution

### 🟡 12 — A blank line inside the `Signatory` table drops every signatory below it, and `pact-check` exits 0

`hooks/config.py:851` (`pact_signatories`). The fix refuses a table line the
walk stops at, but only when that line itself starts with `|`. A blank line
also ends the walk, and nothing looks past it. So a row written below a
blank line is never read, and nothing is refused.

Executed: the pact's table listed the signatory, then a blank line, then
`| https://example.com/org/orders-mobile |`. `pact-check` printed `1 of 1
signatory read` and exited 0. The same pact with the row above the blank line
reads that signatory as `NOT FOUND`, exit 1.

Why it matters: this is the silence 🟡 2 was opened for, reached by a
different line. P8's note now says the signatories below a stray line
"cannot go unread in silence", and for this line they do. A blank line
between rows is an ordinary slip when a table is edited by hand. Under GFM
the table does end at the blank line, so the row is a paragraph. That is a
reason to refuse it, not to read it: the person who wrote it meant a
signatory, and the refusal is where they learn the table stopped.

The fix keeps walking after the line that ends the table, up to the first
heading, and refuses a row it finds there with its own sentence. The
template's shape, a blank line and then the first clause heading, still
reads clean.

### 🟡 13 — `pact-check` refuses prose that names the pact, which is no citation

`skills/evidence-check/scripts/pact_check.py:104` (`PACT_MENTION_RE`). The
pattern takes `pact:<name>` followed by anything. So every mention of the
pact by that spelling, in any ledger file or `spec.md` of a signatory, is a
"pact anchor that does not parse".

Executed, each in a signatory's `spec.md`, beside one valid citation:

| Text | Exit | Printed |
|---|---|---|
| `This work item signs pact:orders-api, the order contract.` | 2 | `` `pact:orders-api,` does not parse `` |
| ``This work item signs `pact:orders-api`.`` | 2 | the same, for the code span |
| ``Cite each clause as `pact:orders-api/"<heading path>"@<hash>`.`` | 2 | the same, for the placeholder form |
| `See pact:orders-api.` | 0 | nothing: the name group swallows the `.` |
| a malformed anchor naming another pact | 0 | nothing, correctly |
| a malformed anchor in a closed fence | 0 | nothing, correctly |

Why it matters: the first three are correct input refused at exit 2, and the
message tells the person to "quote the heading path and give it a hash",
which is advice for text that was never meant as an anchor. No marker exempts
a line, so the only remedy is to reword or fence the prose. The third row is
the form this plugin itself prints in that refusal, so a signatory that
documents how it cites clauses is refused for doing so. The fourth row shows
the cut falling by accident, not by rule. Its local counterpart,
`malformed_rows`, reads only `Code grounds` cells and needs glued marks. This
net reads every line of every file.

The fix keeps exactly the attempts: a name followed by what opens a locator
or a hash (`/`, `#`, a quote, `@`), read whole, and not the placeholder form.
The three malformed shapes round 1 named are still refused. The fix also
skips a mention that starts inside a graded anchor's span, not only at its
start. That half is reasoned from the code, not seen fail: a heading that
spells another `pact:` is not a shape anyone writes.

### ⬜ 14 — Three refusals print as *the pact the `Signatory` table holds an empty row*

`hooks/config.py:856`. Both callers print each refusal from
`pact_signatories` after the words *the pact* (`pact_check.py:393`,
`chain_check.py:4092`). `bf0333e2` changed the two sentences that function
writes itself. The ones it passes through from `remote_entries` were left.

Executed: an empty row printed `REFUSED seal/pact.md — the pact the
`Signatory` table holds an empty row`; a row with a space printed `the pact
`https://example.com/org/orders web` holds a space`; and a duplicate printed
`the pact `…orders-web.git` and `…orders-web` are one repository`.

The behaviour is right and every one exits 2. The sentences read badly, and
the fix commit says this class was done. The fix gives each entry refusal a
lead-in at the one call site, so `remote_entries` and the `Pact` row's
sentences stay as they are. The existing *holds a space* case still passes.

### ⬜ 15 — The word case does not read the refusals `pact-check` prints from `hooks/config.py`

`tests/test_one_word_one_meaning.py:588` (`PACT_PRINTED`). Round 1's ⬜ 11
named "the sentences `pact-check` and `chain-check` print". The case reads
`pact_check.py`'s string constants and two units of `chain_check.py`. Every
refusal about a `Pact` row, a notify value or a `Signatory` entry is written
in `hooks/config.py` (`pact_declaration`, `remote_entries`,
`pact_signatories`) and printed by both commands. None of them is held.
They are clean today, which I searched. ⬜ 14's fix adds sentences there,
which is when holding them starts to matter.

## Findings from reading

### ⬜ 16 — P9's Code grounds cite one of the three `UNREADABLE` cases (paperwork)

`seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:9`.
P9's `Corrected` note says the three `UNREADABLE` branches each have a case.
Its Code grounds cite the pact one and not
`test_a_signatory_config_that_will_not_read_is_unreadable` or
`test_an_anchor_file_that_will_not_read_is_unreadable`, and not
`test_a_signatory_row_the_table_walk_cannot_read_is_exit_2`, the pact-level
half of 🟡 2. This is a correction to the run's paperwork, so it is not
counted in `Needs a fix`.

### ⬜ 17 — `round-1.md`'s Grounds read `fixed at bf035a2f — ;` (paperwork)

`seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1.md:36`.
The close spliced the fixes-table cell `` `bf035a2f`; ledger notes
`f299c650` `` as *fixed at bf035a2f — ; ledger notes*, and ⬜ 5's two SHAs as
*fixed at 1e1bb977 — `62726cb9`*. It reads as a join that keeps the cell's
own leading separator. It is the generator's behaviour, not this branch's.
This is a correction to the run's paperwork, and it is not counted in
`Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 12 | A blank line inside the pact's `Signatory` table ends the walk, and a signatory written below it is never read: `pact-check` prints `1 of 1 signatory read`, exit 0 | `hooks/config.py:851` | open | executed: a row below a blank line was unread at exit 0; above it, the same row read `NOT FOUND`, exit 1; the stray-line fix covers only a line that starts with `\|` |
| 🟡 13 | `PACT_MENTION_RE` takes `pact:<name>` followed by anything, so prose naming the pact, a code span holding it, and the placeholder form are each refused at exit 2 as a pact anchor that does not parse | `skills/evidence-check/scripts/pact_check.py:104` | open | executed: three prose shapes beside a valid citation each exit 2; `pact:orders-api.` ending a sentence exits 0; the three malformed shapes stay refused under the fix |
| ⬜ 14 | Three refusals from `remote_entries` print after *the pact* as *the pact the `Signatory` table holds an empty row*, *the pact `<url>` holds a space*, *the pact `<a>` and `<b>` are one repository*, in `pact-check` and `chain-check` | `hooks/config.py:856` | open | executed: each printed as quoted; the fix commit says both of the table's refusals read after *the pact*, and it changed two of five |
| ⬜ 15 | The word case's printed texts leave out the refusal sentences `pact-check` and `chain-check` print from `hooks/config.py` | `tests/test_one_word_one_meaning.py:588` | open | read: `PACT_PRINTED` names `pact_check.py` and two `chain_check.py` units; the three config units are clean today |
| ⬜ 16 | P9's Code grounds cite one of three `UNREADABLE` cases and not the pact-level stray case, while its note says each branch has a case | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:9` | open | read: a correction to the run's paperwork, not a fix |
| ⬜ 17 | `round-1.md`'s 🟡 3 and ⬜ 5 Grounds read *fixed at bf035a2f — ;* and *fixed at 1e1bb977 — `62726cb9`*, the close's splice of the fixes table | `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1.md:36` | open | read: a correction to the run's paperwork; the generator's join, not this branch's code; the orchestrator answers it |
| 🟢 | round 1's finding 1, re-read: HEAD's history is read with `--full-history`, so a clause a merge did not keep is `SUPERSEDED` | `skills/evidence-check/scripts/pact_check.py:254` | verified | executed: flag dropped, the merge case red; read: `other()` unchanged in shape, a merge listed carries one parent's text |
| 🟢 | round 1's finding 2, re-read: a `Signatory` line with no closing pipe or a second cell is refused | `hooks/config.py:849` | verified | executed: recording dropped, three ids red; the class has one more line, 🟡 12 |
| 🟢 | round 1's finding 3, re-read: `stated_names` and `stated_coordinates` blank pact anchors first | `skills/evidence-check/scripts/evidence_check.py:2940` | verified | executed: each blanking dropped alone, a case red each time; read: every regex read in the file sorted by what it reads, none missed beyond the limit `PACT_ANCHOR_RE`'s comment names |
| 🟢 | round 1's finding 4, re-read: a malformed anchor naming this pact is refused at exit 2 | `skills/evidence-check/scripts/pact_check.py:476` | verified | executed: the loop disabled, three ids red; the net is wider than an attempt, 🟡 13 |
| 🟢 | round 1's finding 5, re-read: `declared_pacts` is `pact-check`'s reader and answers an unreadable config as None | `hooks/config.py:799` | verified | executed: the old answer restored, two cases red; read: no file still reaches `ONE-SIDED` as before |
| 🟢 | round 1's finding 6, re-read: 0.15.4's MALFORMED claim names three patterns | `seal/releases/0.15.4.md:54` | verified | read: claim corrected in place under a dated note |
| 🟢 | round 1's finding 7, re-read: the re-pointed coordinates | `seal/releases/0.5.0.md:212` | answered | carried the orchestrator's answer; read: round 1's identity probe makes the alias the same unit, so the claim names what it is about |
| 🟢 | round 1's finding 8, re-read: the four branches each have a case pinning the sentence | `tests/test_pact_check.py:446` | verified | read: four cases, sentences pinned; executed: the config case red when broken; the other three reds are the smith's account |
| 🟢 | round 1's finding 9, re-read: a pact listing its own repository is refused in the table's words | `skills/evidence-check/scripts/pact_check.py:402` | verified | executed: the check disabled, the case red |
| 🟢 | round 1's finding 10, re-read: the repeated git calls | `skills/evidence-check/scripts/pact_check.py:195` | answered | carried the orchestrator's answer; read: the cost is local and small |
| 🟢 | round 1's finding 11, re-read: the word case reads five more texts | `tests/test_one_word_one_meaning.py:581` | verified | executed: the module green; read: the five texts are read; `hooks/config.py`'s sentences are not, ⬜ 15 |
| 🟢 | the ledger corrections round 1's fixes owed | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:5` | verified | read: 0.15.4 corrected; 0.9.0 R1 and 0.16.0 P1 re-read and re-hashed; fragment P1, P5, P8 and P9 carry dated notes; executed: `evidence-check --strict` exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on six modules: `test_pact_check`, `test_a_signatory_declares_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory`, `test_one_word_one_meaning`, `test_a_signatorys_ci_prints_its_pact`, `test_a_record_states_what_the_tree_has` | 179 passed, exit 0 |
| `bin/evidence-check --strict .` at the target | exit 0; 3678 ok; records arm 0 refused |
| `bin/fold-check` at the target | exit 0, 158 statements in 15 documents |
| Seven breaks of round 1's fixes, one at a time, each case run (the table above) | every one red; tree restored after each |
| `pact-check` over a signatory `spec.md` holding each prose shape of 🟡 13 | three exit 2, `See pact:orders-api.` exit 0, other pact and fenced exit 0 |
| `pact-check` over a pact with a blank line inside the `Signatory` table (🟡 12) | `1 of 1 signatory read`, exit 0 |
| `pact-check` over an empty row, a row with a space, and a duplicate row (⬜ 14) | each `REFUSED`, exit 2, with the sentences quoted in ⬜ 14 |
| The paste-ready fixes for 🟡 12, 🟡 13 and ⬜ 14 applied in the clone, with the proposed cases | 6 proposed cases red before the fixes and green after; with the five pact modules, 72 passed, exit 0; clone restored |
| The full suite, the repository-wide lint and the typecheck | not yet — not run in this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🟡 12 (and ⬜ 14, which edits the same lines)

`hooks/config.py`, `pact_signatories`, from the walk to the end:

```python
    values, seen_header, stray, ended = [], False, None, False
    for _index, line in unfenced(text.splitlines(), text):
        if not seen_header:
            seen_header = bool(SIGNATORY_HEADER.match(line))
            continue
        if ended:
            # Past the line that ended the table -- a blank one, say -- and
            # before the first clause: a row written here is a signatory the
            # walk never reaches, the same silence as the stray row below
            # (round 2 of #647).
            if line.lstrip().startswith("#"):
                break
            if line.lstrip().startswith("|"):
                stray = (
                    f"has a `Signatory` table that ends above `{line.strip()}`, "
                    "a row the walk never reaches — it and every signatory "
                    "below it would go unread"
                )
                break
            continue
        if CONFIG_SEPARATOR.match(line.strip()) and not values:
            continue
        match = SIGNATORY_ROW.match(line)
        if not match:
            # A table line the walk cannot read -- no closing pipe, or a
            # second cell -- ends the walk, and every signatory written below
            # it would go unread in silence. So it is refused (round 1 of
            # #647, yellow 2).
            if line.lstrip().startswith("|"):
                stray = (
                    f"has a `Signatory` table that stops at `{line.strip()}`, "
                    "which is not a one-cell row closed by `|` — every "
                    "signatory below it would go unread"
                )
                break
            ended = True
            continue
        values.append(unescaped(match.group("value").strip()))
    if not seen_header:
        return [], ["holds no `| Signatory |` table, so it names no signatory"]
    # Each sentence is printed after "the pact " by both callers, so an
    # entry's refusal gets a lead-in that reads after those words.
    signatories, entry_refusals = remote_entries(values, "an empty row", named=False)
    refusals = [
        f"has a `Signatory` entry that will not read: {r}" for r in entry_refusals
    ]
    if stray is not None:
        refusals.append(stray)
    if not values:
        refusals.append("has a `Signatory` table that lists nobody")
    return signatories, refusals
```

### 🟡 13

`skills/evidence-check/scripts/pact_check.py`, the constant, replacing its
last line and keeping the comment above it:

```python
#
# **An attempt, not a mention**: the name must be followed by what opens a
# locator or a hash -- `/`, `#`, a quote or `@` -- so prose naming the pact
# (`pact:orders-api,`, a code span holding `pact:orders-api`) is not refused,
# and neither is the form written with its placeholders, `/"<heading path>"`.
# The name is read whole, so `pact:orders-api.` ending a sentence is prose
# and not a near miss.
PACT_MENTION_RE = re.compile(
    r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]*[A-Za-z0-9_-])"
    r"(?![A-Za-z0-9_.-]*[A-Za-z0-9_-])(?!/\"<)(?=[/#\"'@])[^\s`|]*"
)
```

and in `check`, the two lines that skip a graded anchor:

```python
            graded = [m.span() for m in checker.PACT_ANCHOR_RE.finditer(view)]
            for near in PACT_MENTION_RE.finditer(view):
                inside = any(s <= near.start() < e for s, e in graded)
                if near.group("name").lower() != name or inside:
                    continue
```

### ⬜ 14

Carried by the 🟡 12 block above, which is the same function. The change on
its own:

```python
    # Each sentence is printed after "the pact " by both callers, so an
    # entry's refusal gets a lead-in that reads after those words.
    signatories, entry_refusals = remote_entries(values, "an empty row", named=False)
    refusals = [
        f"has a `Signatory` entry that will not read: {r}" for r in entry_refusals
    ]
```

### ⬜ 15

`tests/test_one_word_one_meaning.py`, three more entries in `PACT_PRINTED`:

```python
    (("hooks", "config.py"), "pact_declaration"),
    (("hooks", "config.py"), "remote_entries"),
    (("hooks", "config.py"), "pact_signatories"),
```

### ⬜ 16

The fragment's P9 Code grounds cell, three more coordinates, each stamped
`@00000000` and then `evidence-check --reverify --checked 2026-10-03`:

```markdown
`tests/test_pact_check.py#test_a_signatory_config_that_will_not_read_is_unreadable@00000000`, `tests/test_pact_check.py#test_an_anchor_file_that_will_not_read_is_unreadable@00000000`, `tests/test_pact_check.py#test_a_signatory_row_the_table_walk_cannot_read_is_exit_2@00000000`
```

## Regression tests to plant

Each was run red against the target and green with the fixes above.

| Finding | Destination | Case |
|---|---|---|
| 🟡 12 | `tests/test_pact_check.py` | a row below a blank line inside the table is `REFUSED`, exit 2, with its sentence pinned |
| 🟡 13 | `tests/test_pact_check.py` | prose, a code span, and the placeholder form naming the pact each leave `pact-check` at exit 0 |
| ⬜ 14 | `tests/test_pact_check.py` | an empty row and a row with a space each print after *the pact has a `Signatory` entry that will not read:* |

```python
# tests/test_pact_check.py — 🟡 12
def test_a_signatory_row_below_a_blank_line_is_refused(world):
    """A blank line ends the table's walk; a row written below it is a
    signatory nobody reads, so it is refused rather than passed over."""
    text = pact(V2).replace(
        f"| {SIGNATORY_URL} |\n",
        f"| {SIGNATORY_URL} |\n\n| https://example.com/org/orders-mobile |\n",
    )
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a blank line inside the table")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert (
        "REFUSED seal/pact.md — the pact has a `Signatory` table that ends above "
        "`| https://example.com/org/orders-mobile |`, a row the walk never "
        "reaches — it and every signatory below it would go unread"
    ) in out, out


# tests/test_pact_check.py — 🟡 13
@pytest.mark.parametrize(
    "body",
    [
        "This work item signs pact:orders-api, the order contract.",
        "This work item signs `pact:orders-api`.",
        'Cite each clause as `pact:orders-api/"<heading path>"@<hash>`.',
    ],
    ids=["prose", "code span", "the form with its placeholders"],
)
def test_prose_naming_the_pact_is_not_a_citation(world, body):
    cite(world, clause(V2))
    write(world["web"], "seal/specs/1790000001-y/spec.md", f"# spec\n\n{body}\n")
    code, out = run(world)
    assert code == 0, out


# tests/test_pact_check.py — ⬜ 14
@pytest.mark.parametrize(
    "row, said",
    [
        ("|  |", "an empty row"),
        ("| https://example.com/org/orders web |", "holds a space"),
    ],
)
def test_an_entry_refusal_reads_after_the_pact(world, row, said):
    text = pact(V2).replace(f"| {SIGNATORY_URL} |\n", f"| {SIGNATORY_URL} |\n{row}\n")
    write(world["api"], "seal/pact.md", text)
    commit(world["api"], "a bad entry")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 2, out
    assert "the pact has a `Signatory` entry that will not read: " in out, out
    assert said in out, out
```

## Facts for the evidence ledger

| Claim | Where it is grounded | How it was established |
|---|---|---|
| Every regular-expression read in `evidence_check.py` either blanks pact anchors first, reads only `ANCHOR_RE` matches, reads the tree rather than a record, or reads no coordinate; the one shape still read is a heading that holds a whole stamped coordinate | `skills/evidence-check/scripts/evidence_check.py#blank_pact_anchors` | read, re-derived over all 60 call sites |

This belongs in P5's note when 🟡 13 and 🟡 12 are fixed and P5 is next
re-read. It needs no row of its own.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 12 (a blank line inside the `Signatory` table drops the signatories below it, exit 0), 🟡 13 (`pact-check` refuses prose naming the pact at exit 2)
Loses a record or crashes: no

The broad gate has not come due: two findings need a fix, so the sealer's
spawn waits for the round that verifies them. The broad gate's state is `not
yet` — no full-suite run has happened on this branch.

## Proof block

Files opened in this round, at `2a0243b2`: `rounds/round-1.md`,
`rounds/round-1-report.md`, the orchestrator's fixes table for round 1;
`skills/evidence-check/scripts/pact_check.py` (whole);
`skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE` to
`OLD_COORD_RE`, `unquoted`, `check_text`'s head, `old_format_rows`,
`refused_coordinate`'s tail, `grounds_cells`, `malformed_remedy`,
`malformed_rows`, `migrate`'s blanking, `reverify`'s anchor loop,
`RECORD_NAME_RE` to `RECORDS_HEADING`, `claim_lines`' tail,
`stated_names`, `stated_coordinates`, `heading_slugs`,
`coordinate_misses`, `stated_stamps`, and every regex call site by search);
`hooks/config.py` (`normalise_remote`, `pact_name`, `remote_entries`,
`pact_declaration`, `declared_pacts`, `SIGNATORY_ROW`, `pact_signatories`,
`unfenced`'s docstring); `skills/code-review/scripts/chain_check.py`
(`CLOSED_WORDS`, `FIX_WORDS`, `closed_with_a_fix`, the pact refusal print);
`skills/code-review/scripts/round_record.py` (`IDENTIFIER_RE` and its
neighbours); `templates/pact.md`; `docs/round-record-spec.md` (the
confirmation-row section); the fix range's diff over `hooks`, `skills` and
`tests`; the commit messages of `0487fb5b..2a0243b2`; the word diff of
`seal/ledger` and `seal/releases` over the range, and the P5 and P9 rows,
the 0.9.0 R1 row and the 0.15.4 MALFORMED row in full;
`tests/test_pact_check.py` (fixtures and the new cases);
`tests/test_one_word_one_meaning.py` (the pact case).
