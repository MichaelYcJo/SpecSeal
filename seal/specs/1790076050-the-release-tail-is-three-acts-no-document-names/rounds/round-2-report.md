# 1790076050-the-release-tail-is-three-acts-no-document-names — review round 2

The verifying round. Target SHA `11f3cde83dc2f617de293c92f959d1c1a95880b2`;
the surface read is
`317a96e0ebcc3b36b927c22ab5f2a81469528748..d2b1e19487e7b656ea016335264ad78582ac5231`,
two commits, plus the six units round 1 recorded under `New units`, which no
round has judged. Round 1's six verdicts are inherited, not re-derived.

Every one of round 1's six findings is closed, and all six of its claims about
how they were closed hold when measured. Three new things need a fix, and all
three are in what the fix pass wrote rather than in what it repaired.

## What round 1's fixes actually did — the six claims, judged

**Finding 2's figures are right, and they were re-derived rather than
pasted.** Executed against the live directory file on 2026-09-22, with the
command `phases/phase-3.md` now carries:

| | claimed | measured |
|---|---|---|
| entries | 310 | 310 |
| `source` an object carrying a `url` | 258 | 258 |
| of those, carrying a `sha` | 258 | 258 |
| of those, carrying a `ref` | 96 | 96 |
| of those refs, naming `main` or `master` | 91 | 91 |
| `source` a plain string, pinning nothing | 52 | 52 |

The five refs that are neither `main` nor `master` are the two version-shaped
strings and the three ordinary branch names `phase-3.md` describes, which is
why dropping *exactly one names a tag* was right: a `ref` in that file carries
nothing that says which it is. The rolled-up table also reconciles with the
four-shape table forty lines above it — 157 + 96 + 5 = 258 objects, and the 52
official strings plus 5 community ones are the 57 entries that section says
`source["sha"]` raises on.

**Finding 1 was fixed as a class and the positive control is a real one.**
`spend_label` is reached from all three call sites and `drop_label` from
nowhere else — executed, the whole tree, including the workflow files. Of the
four new cases, three are red against the pre-fix script and one,
`test_an_already_closed_issue_reports_a_removal_that_worked`, is green by
construction; deleting the success print inside `spend_label` reds it.
That is §15's second route, written into the section as an alternative to the
first, so the case is planted.

**Finding 6's second spelling is bound to the call.** `--add-assignee` beside
`--remove-label` reds it, executed. The first spelling's defect — an argv
written as a list literal and read as call arguments — is fixed, and the
reader now collects both shapes. What it is not is reachable; see finding 1
below.

**Finding 3's probe-instead-of-a-case reasoning holds, with one sentence
missing.** The class is genuinely bigger than the branch, the existing
case is a hand-written spawn under hostile encodings rather than a corpus list,
and adding one script to it is the coordinate fix. See the ⬜ row below for
what is not recorded.

**Finding 5's grounds are correct.** §*House rules* is the section with the
arms, both arms are conditioned on the cited code changing, and neither reaches
a claim falsified by code a branch added. The act stands. The two rows the fix
pass wrote into `seal/follow-up.md` are where the new findings are.

**The anchor count is 14.** Executed: the fragment reports `14 ok`, the corpus
`1453 ok · 0 drifted · 0 broken`, and a mechanical count of backticked
coordinates in the fragment gives 14 total and 14 unique. Both records say 14
and both say why the number moved.

**`Contract changes: none` is correct.** `drop_label` keeps its signature and
has no caller outside its own module; `spend_label` is new and is reached only
from the loop that replaced the three copies. The two test references to either
name are source-text reads, not imports.

**The ⬜ answered as a reading is answered.** Executed: `DOMAIN_RE` over
`.github/scripts/plugin_directory_check.py` matches three times in the whole
file, all of them the API host and all of them in `ALLOWED_DOMAINS`; over lines
81, 82 and 85 it matches nothing. The corpus is every tracked text file, so the
file is scanned and the pattern is what cannot see the values — which is
exactly what `overview.md` §*Not done* now says.

## Findings

### 🟡 1. Finding 6's fix is gated behind the reader whose blindness finding 6 was about

`tests/test_release_hygiene.py:1084` and `:1101`

The new `ast` reader is the whole of finding 6's repair: it parses the script,
finds the one `gh issue edit` argv, and asserts the flags it carries. It runs
under `if edits:`, where `edits` is the old folded-substring count:

```python
edits = folded.count('"gh", "issue", "edit"')
assert edits <= 1, (...)
...
if edits:
    tree = ast.parse(...)
```

`edits <= 1` passes at zero. So any re-spelling of the argv that the folded
substring does not match takes the count to zero, skips the block, and the case
asserts nothing at all about what the script edits — while the `ast` reader,
which does not care about spelling, would have caught it.

**Executed.** With the argv rewritten across lines with one comment between the
words and `"--add-assignee", "someone"` added to it, the folded count is 0 and
`test_the_script_closes_and_takes_off_one_named_label_and_nothing_else` exits
0. The script in that state assigns a person on every label removal and the
case says it is clean.

Why it matters: this is round 1's finding 6 one layer out. That finding was
that two assertions were not bound to the call they judged. The fix bound them
and then made the binding conditional on the unbound reader agreeing first.

### 🟡 2. The new `seal/follow-up.md` row's answerer is the condition that file forbids

`seal/follow-up.md:80`

The header of that file states its own rule:

> **Every row names a person, with no condition attached.** An answerer column
> reading `repository owner, next time X is opened` is a condition wearing a
> person's clothes: nobody agreed to open `X`, so nobody answers.

The row the fix pass added reads *the repository owner, at the next change to
`CONTRIBUTING.md` §*House rules**. Nobody has agreed to change that section,
so nobody answers the row — which is the outcome the header describes, in a
different spelling.

**Executed.** `tests/test_a_rider_reaches_its_file.py` is green, 54 passed with
`tests/test_docs_line_wrap.py`. Its guard is
`test_the_header_stops_the_answerer_that_is_really_a_condition`, and it tests
`"next time" not in " ".join(row)` — one literal. `at the next change to`
passes it.

Two things are owed and only the first is a fix pass's: the row gets an
unconditional answerer. Whether the guard should read the class rather than the
spelling is mechanism and belongs in the `## Deferred` table below.

### 🟡 3. `five of nine` is false on every reading, in the row below it

`seal/follow-up.md:81`

The row opens *so five of nine `.github/scripts/` modules call it and four do
not*. **Executed at `11f3cde8`**: there are 13 `.py` files under
`.github/scripts/`, every one of them carries a `__main__`, 6 call
`console.to_utf8()` and 7 do not. Before the fix the same corpus was 5 and 8.
No counting rule produces a denominator of nine, and the `four` is wrong under
either.

The figure came from round 1's own deferral cell and was copied rather than
re-derived, which is the same act finding 2 was raised for one file over. It
also carries no moment, which is the class the row immediately above it in the
same file enumerates — *a figure about a corpus, stated with no moment*, whose
own text records that every hand enumeration of it has shipped short.

### ⬜ Two occurrences of the renamed case are unmarked

`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:25`
and `spec.md:201`

Finding 4 renamed the case. The fix pass put `NAME NOT IN TREE` beside the two
occurrences written as a bare name and left the two written as
`path#name` — one in `phase-4.md` and one in `spec.md`. Those two name a unit
the tree does not have, and a reader opening the coordinate finds nothing.

**Executed**: `evidence-check` is green (`14 ok`, `total 1453 ok`, `0
refused`), because the `path#name` form is read as a coordinate rather than as
a prose name. So the checker is not what would have caught this, and the class
finding 4 named is *every place the old name is written*, not *every place the
checker complains*. Old name, for the record:
`test_the_label_is_two_states_and_nothing_reads_it` (NAME NOT IN TREE).

A correction to this run's own paperwork, so `Needs a fix` does not count it.

### ⬜ The fix pass left a 103-column line in a shipped document

`docs/branch-and-release.md:100`

The re-join after the figures were replaced left `So the rule above stopped
being only about readers this repository can fix. Breaking it now also breaks`
on one line at 103 columns, in a paragraph whose other lines run 68 to 78.
Nothing catches it: `docs/branch-and-release.md` is not in
`tests/test_docs_line_wrap.py`'s covered list, and that file already carried one
over-88 line at `:247` before this branch. Readability only; the sentence is
correct.

### ⬜ The `console.to_utf8()` call this branch added is pinned by nothing, and no record says so

`.github/scripts/tracker_labels.py:148`

The decision not to add a case is defensible and I would have taken it: the
existing case spawns each gate under four hostile encodings by hand rather than
reading a corpus, so covering one script is the coordinate fix and covering the
directory reds the seven standing non-callers. The `seal/follow-up.md` row
carries the class with the question stated.

What is missing is one sentence in `overview.md` §*Not done* — that a later
session deleting the `console.to_utf8()` line from `tracker_labels.py` gets no
warning from this suite. The same fix pass wrote exactly that sentence, at
exactly that length, for the `DOMAIN_RE` reading three paragraphs earlier. The
disclosure standard was applied to one unpinned thing and not the other.

A correction to this run's own paperwork, so `Needs a fix` does not count it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | finding 6's `ast` reader runs under `if edits:`, so a re-spelling of the argv takes the folded count to zero and the case asserts nothing about what the script edits | `tests/test_release_hygiene.py:1084` | open | Executed in a clone at `11f3cde8`: the argv rewritten with one comment between its words and `--add-assignee` added gives a folded count of 0 and the case exits 0, with the script assigning a person on every removal |
| 🟡 2 | the new §*House rules* row's answerer is *the repository owner, at the next change to `CONTRIBUTING.md` §*House rules**, which is the condition-wearing-a-person's-clothes the file's own header forbids | `seal/follow-up.md:80` | open | Executed: `tests/test_a_rider_reaches_its_file.py` green. Its guard tests one literal, `next time`, so the new spelling passes. §12 — the class is the shape, and the check enumerates a spelling |
| 🟡 3 | *five of nine `.github/scripts/` modules call it and four do not* is false on both numbers, and carries no moment | `seal/follow-up.md:81` | open | Executed at `11f3cde8`: 13 `.py` files, all 13 with a `__main__`, 6 call `console.to_utf8()` and 7 do not; before the fix, 5 and 8. Copied from round 1's deferral cell rather than re-derived |
| ⬜ | two `path#name` occurrences of the case finding 4 renamed are unmarked, so they name a unit the tree does not have | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:25` | answered | ⬜ — this run's own paperwork. Executed: `evidence-check` green (`14 ok`, `1453 ok`, `0 refused`) because the `path#name` form is read as a coordinate, not as a prose name, so the checker was never what would catch it |
| ⬜ | a 103-column line left by the re-join, in a paragraph that otherwise wraps at 68–78 | `docs/branch-and-release.md:100` | answered | ⬜ — readability only; the sentence is correct. Executed: `tests/test_docs_line_wrap.py` green, and this file is not in its covered list |
| ⬜ | the `console.to_utf8()` call this branch added is pinned by nothing and `overview.md` §*Not done* does not say so, while the same fix pass wrote that sentence for the `DOMAIN_RE` reading | `.github/scripts/tracker_labels.py:148` | answered | ⬜ — the decision not to add a case is right: the existing case spawns each gate by hand, so one script is the coordinate fix and the directory reds seven standing non-callers. Only the disclosure is missing |
| 🟢 | finding 2's figures, re-derived rather than pasted, and the command that re-derives them | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-3.md:56-96` | confirmed | Executed live 2026-09-22 against the directory file: 310 / 258 / 258 / 96 / 91 / 52, exact. The five non-`main` refs are the two version-shaped and three branch-shaped strings the record names, which is why dropping the tag claim was right |
| 🟢 | finding 1 fixed as a class — `spend_label` reached from all three sites, `drop_label` from nowhere else | `.github/scripts/close_issues_on_release.py:189` | confirmed | Executed over the whole tree: no caller outside the module, so `Contract changes: none` is right. Three of the four new cases are red against the pre-fix script |
| 🟢 | the positive control, shown red by deleting the line it pins | `tests/test_a_declared_label_reaches_the_tracker.py:336` | confirmed | Executed: green against the pre-fix script, red when the success print inside `spend_label` is deleted. §15's second route, which the section states as an alternative to the first |
| 🟢 | finding 6's second spelling reddens on the escape the round named | `tests/test_release_hygiene.py:1101-1131` | confirmed | Executed: `--add-assignee` beside `--remove-label` reds the case. Both argv shapes are collected, so the first spelling's zero-parse is fixed |
| 🟢 | the 14/13 anchor count, and the corpus figure that follows it | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5` | confirmed | Executed in a clone at `11f3cde8`: the fragment reports `14 ok`, the corpus `1453 ok · 0 drifted · 0 broken`, and a mechanical count gives 14 total, 14 unique |
| 🟢 | the ⬜ answered as a reading — `DOMAIN_RE` returns zero matches over the two lines, and the corpus does include the file | `.github/scripts/plugin_directory_check.py:81-85` | confirmed | Executed: three matches in the whole file, all the API host and all allowlisted; zero on lines 81, 82 and 85. The corpus is every tracked text file, so the pattern is what cannot see them, which is what `overview.md` §*Not done* says |
| ⬜ | round 1's `## Paste-ready fixes` cell reads *no paste-ready fix in the report* while the report carries six | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/rounds/round-1.md:63` | answered | ⬜ — a defect in the record generator, filed as #505 by the orchestrating session. Not this branch's to fix or to work around; carried here so the next reader of that cell knows why it is wrong |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer. The prompt withheld it, so nothing was declined. Answerer: the `sealer`, in its single run |

## Paste-ready fixes

### 🟡 1 — `tests/test_release_hygiene.py`

Make the `ast` reader the authority and stop the folded count gating it. Replace
the `if edits:` line and its block header with an unconditional parse; the body
below it is unchanged except for the dedent.

```python
    edits = folded.count('"gh", "issue", "edit"')
    assert edits <= 1, (
        f"{edits} `issue edit` calls; there is one, and it is the removal of "
        "a spent sizing label"
    )
    # **Bound to the call, and not gated on the reader that cannot see it.**
    # Round 1's finding 6 was that `--remove-label` being present somewhere
    # and `--add-label` being absent everywhere said nothing about the one
    # `issue edit` the folded count above found. Round 2's finding 1 is that
    # the reader which fixed that ran under `if edits:` — and `edits <= 1`
    # passes at zero, so any re-spelling of the argv the folded substring does
    # not match skipped the whole block and asserted nothing. Measured: the
    # argv rewritten across lines with one comment between its words takes the
    # folded count to 0, and an edit carrying `--add-assignee` passed.
    #
    # So the parse runs unconditionally and asserts exactly one edit. The
    # folded count stays as the cheap statement above it and gates nothing.
    #
    # Read through `ast` rather than by counting brackets, because the
    # arguments are wrapped one per line and the folded text gives no
    # reliable end.
    tree = ast.parse(read_text(".github", "scripts", "close_issues_on_release.py"))
    # BOTH argv shapes this file uses: `run("gh", …)` spreads the words as
    # call arguments, and `subprocess.run(["gh", …], …)` passes a list.
    # The one `issue edit` is written the second way, and a reader that
    # knew only the first parsed zero calls and asserted nothing —
    # measured, on the first spelling of this check.
    argvs = [node.elts for node in ast.walk(tree) if isinstance(node, ast.List)]
    argvs += [node.args for node in ast.walk(tree) if isinstance(node, ast.Call)]

    def words(argv):
        return [
            a.value
            for a in argv
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
        ]

    edit_calls = [argv for argv in argvs if words(argv)[:3] == ["gh", "issue", "edit"]]
    assert len(edit_calls) == 1, (
        f"{len(edit_calls)} `gh issue edit` argv lists parsed; there is one, "
        "and it is the removal of a spent sizing label"
    )
    flags = {word for word in words(edit_calls[0]) if word.startswith("--")}
    assert flags == {"--repo", "--remove-label"}, (
        f"the one `gh issue edit` carries {sorted(flags)}. It may carry "
        "`--remove-label` and nothing else that writes: adding a label is "
        "the sibling's act at the squash, and any other write is not the "
        "removal this case says the one edit is"
    )
```

### 🟡 2 — `seal/follow-up.md:80`, the answerer cell only

```
| the repository owner |
```

The row's body already states what has to be decided, so the cell loses
nothing by naming the person alone. Nothing else in the row changes.

### 🟡 3 — `seal/follow-up.md:81`, the row's opening sentence

```
| **`console.to_utf8()` is owed by an entry point and nothing says which files are entry points, so 6 of the 13 `.github/scripts/` modules call it and 7 do not — measured 2026-09-22 at `11f3cde8`, where every one of the 13 carries a `__main__`.**
```

The rest of the row is unchanged. Its later sentence *the four standing ones
predate it* becomes *the seven standing ones predate it*.

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, checked out at `11f3cde8`; every probe below ran there, and the clone and its virtual environment were removed afterwards | the worktree was written to once, for this report |
| the five new and renamed cases at `11f3cde8` | `5 passed` |
| probe: `"--add-assignee"` appended beside `"--remove-label"` in `drop_label`'s argv, then the restated hygiene case | `1 failed` — finding 6's second spelling reddens on the escape the round named |
| probe: the success print deleted from inside `spend_label`, then the three already-closed cases | `1 failed, 2 passed` — the positive control reddens on the line it pins |
| probe: the four new cases against the pre-fix script (`317a96e0`) | three red; `test_an_already_closed_issue_reports_a_removal_that_worked` green, which is the positive control |
| probe: the argv rewritten across lines with one comment between its words and `--add-assignee "someone"` added, then the restated hygiene case | folded count **0**, case **exit 0** — the script assigns a person on every removal and the case says it is clean. Finding 1 |
| `tests/test_a_rider_reaches_its_file.py tests/test_docs_line_wrap.py` — the two modules the `seal/follow-up.md` and `docs/` edits reach and the handoff's five do not | `54 passed` — the answerer guard and the wrap list are both blind to what this fix pass wrote |
| `evidence_check.py .` in the clone at `11f3cde8` | `total: 1453 ok · 0 drifted · 0 broken`; the fragment `14 ok`; `72 names read · 0 refused` |
| mechanical count of backticked coordinates in the ledger fragment | 14 total, 14 unique |
| `gh api repos/<owner>/<directory>/contents/.claude-plugin/marketplace.json`, the command `phases/phase-3.md` now carries | `310 / 258 / 258 / 96 / 91 / 52` and the five non-`main` refs — every figure in the corrected paragraph, exact |
| `DOMAIN_RE` driven over `plugin_directory_check.py` | three matches in the whole file, all the API host and all in `ALLOWED_DOMAINS`; zero on lines 81, 82 and 85 |
| count of `.py` files under `.github/scripts/`, of those carrying `__main__`, and of those calling `console.to_utf8()` | 13 / 13 / 6, against 5 before the fix. Finding 3 |
| `uvx ruff check` and `ruff format --check` over the five files this range changed | exit 0 and exit 0, read directly. `E402` is selected and does not fire: ruff allows an import after a `sys.path` edit, which is the shape both sibling scripts already use |
| `bin/deferral-check .` in the clone | exit 0, read directly |
| the eight modules, the five modules of the fix range, and the repository-wide lint the orchestrating session already ran | not re-run — `agent-contract` §3, the handoff carries them |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |
| the tag-triggered job running on GitHub, and the live label write on the tracker | **not run here and not runnable here** — `agent-contract` §6 withholds both from every agent |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1, finding 1 | `.github/scripts/close_issues_on_release.py:291-321` | the three call sites the class fix collapsed; opening them is how `Contract changes: none` was checked |
| round 1, finding 5 | `CONTRIBUTING.md` §*House rules* | the two arms and what neither reaches; the fix pass's corrected grounds rest on it |
| round 1, deferred | `seal/follow-up.md` header | carried as a coordinate and re-read, which is what produced findings 2 and 3 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `test_the_header_stops_the_answerer_that_is_really_a_condition` tests one literal, `next time`, while the rule it guards is a shape — *at the next change to X*, *when X is next opened*, *whoever gets to X first* all pass it. Widening it is mechanism with its own false-positive argument to make, which a fix pass may not add. Finding 2 fixes the one instance; the class is the check | a candidate row for `seal/follow-up.md`, to be written by the session that acts on finding 2 | the repository owner |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point as a class — **already deferred** by round 1's fix pass, to `seal/follow-up.md:81`. Not re-litigated; finding 3 corrects that row's figure and nothing else about it | `seal/follow-up.md` | whoever owns `hooks/console.py`'s convention |
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries, for a claim falsified by code a branch added — **already deferred** by round 1, to `seal/follow-up.md:80`. Finding 2 is about that row's answerer cell, not about the question in it | `seal/follow-up.md` | the repository owner |
| `round-1.md`'s `## Paste-ready fixes` cell reading *no paste-ready fix in the report* against a report carrying six — **already filed as #505** by the orchestrating session, in the record generator rather than in this work | issue #505 | whoever owns `skills/code-review/scripts/round_record.py` |

Needs a fix: yes — findings 1, 2 and 3. Finding 1 is the one in the tool: the
guard finding 6 built is skipped whenever the script's argv is re-spelled, so
an `issue edit` that also assigns, milestones or writes a body passes it.
Findings 2 and 3 are one row each of `seal/follow-up.md`, a tracked document
this branch writes to — an answerer that is a condition, and a figure about a
corpus that is false on both its numbers.

Loses a record or crashes: no — nothing found leaves the root, nothing crashes,
and no path this release exercises is affected. All three findings are a guard
that can go quiet and two rows that misstate what they point at.

## Proof block

**Executed** — the probes in the table above, each in a `git clone --no-local`
at `11f3cde8`, removed afterwards.

**Read, not executed** — the eight modules and the lint the orchestrating
session ran before round 1; the five modules and `survivor-check` it ran over
this fix range; the tag-triggered workflow's actual run; the reconcile step's
actual write to the tracker.

**Unverified** — the broad gate: the full suite, the repository-wide lint and
the typecheck over the whole tree. Answerer: the `sealer`, in its single run,
after the three findings above are settled.

Files opened: `.github/scripts/close_issues_on_release.py`,
`.github/scripts/tracker_labels.py`, `.github/scripts/plugin_directory_check.py`,
`.github/scripts/publish_release_note.py`, `.github/workflows/`,
`docs/branch-and-release.md`, `ruff.toml`, `seal/follow-up.md`,
`seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`,
`tests/test_release_hygiene.py`, `tests/test_a_declared_label_reaches_the_tracker.py`,
`tests/test_a_release_is_sized_by_a_criterion.py`, `tests/test_a_rider_reaches_its_file.py`,
`tests/test_docs_line_wrap.py`, `tests/test_console_is_not_utf8.py`,
`tests/test_no_real_identifiers.py`, and this work item's `overview.md`,
`questions.md`, `spec.md`, `survivors.md`, `phases/phase-3.md`,
`phases/phase-4.md`, `rounds/round-1.md`, `rounds/round-1-report.md`.
