# 1790076080-every-orchestrator-rule-is-a-sentence — round 2 report

| Field | Value |
|---|---|
| Round | 2 — the verifying round |
| Target SHA | `73e71c1a7a86b3b1139a6311a29d7173b08955e6` |
| Fix range read | `238dbeafea0dd8b3105bf9ab045371bfcd10fa6b..da35172fc5deaff640f89989fad447788ac90e04`, 4 commits |
| Base | `origin/release/v0.13.1` at `6d41002398bfeeb55db08cca9b441b68e0267049` |
| Branch | `docs/330-every-orchestrator-rule-is-a-sentence` |
| Inherited | round 1's four verdicts and two corrections, read before the diff |

Read and executed in a `git clone --no-local` of the worktree at the target
SHA, with a `uv` virtual environment inside it. The clone and the one probe
file are deleted; the worktree is clean and no other worktree was touched.

Scope held to the fix diff and to the five units round 1's record names under
`New units`. The branch was not re-read.

## What round 1 asked and what the fixes answer

All four of round 1's findings are closed, and each was checked against the
code rather than against the fix pass's account of it. The two contract
changes reach every call site. The four claims the fix pass made are
three-and-a-half true: the enumeration behind the red finding holds, the floor
case is clean for the right reason, Q3's two option cells are both corrected,
and the aggregates are corrected in the sense that a wrong number was replaced
— but the replacements are a count of something narrower than the sentence
says, and two statements of the corrected denominator were left standing.

### 🟢 Finding 1 is closed, and the enumeration behind it holds

`skills/verify/scripts/session_cost.py`, `emit` and its three call sites.

The repair is a rule at the seam rather than a patch at the two coordinates
round 1 named: the captured body has the transcript's path replaced by its
basename, and the printed report is untouched. I checked the enumeration the
docstring claims rather than taking it.

Every line that can put a path into the captured body prints the one `path`
argument. There are exactly two — `report_segments`' empty branch at line 1859
and `report_spawns`' empty branch at line 1561 — and `--latest`'s `# {path}`
line is printed by `main` before `emit` captures, so it never enters the
buffer. The one remaining place a filesystem name reaches the printed table is
a segment row's label: `segment_label` falls back to `row["transcript"]` for a
row nobody named, and `measure_segments` stores that field as
`os.path.relpath(transcript, beside)` where `beside` is the parent
transcript's own directory. Every row label is therefore already relative, and
the subagent search root is built under that same directory, so the relative
form cannot climb out of it. The claim checks out.

The residual the docstring states — a future report line printing some other
absolute path is not covered — is the honest one, and it is stated where the
next editor of `emit` will read it.

**Executed**: with `session_cost.py` restored to `238dbeaf` and the two new
cases kept, both go red. Green at the target SHA.

### 🟢 Finding 2 is closed, and the refusal moved earlier than the fix round 1 proposed

An empty or whitespace-only `--says` now exits 1 with a message and posts
nothing. The fix pass put the `read_says` call **before** the render rather
than after it, which round 1's paste-ready fix did not, and said why in a
comment: a refusal that renders first spends the work to throw it away. Read
against the non-post path, which returns before either, and against `--says -`,
which answers at EOF in both orders. No behaviour is lost by the move.

The second of the two cases checks the refusal at the `gh` seam rather than by
reading the message, so the refusal does not depend on the tracker answering.

**Executed**: both cases red against `238dbeaf`, green at the target SHA.

### 🟢 Finding 3 is closed, and the floor case is clean for the right reason

`tests/test_every_orchestrator_act_names_its_delivery.py`, `findings`,
`_delivery` and `_tree`.

Two changes were needed and both landed: `_delivery` resolves a named path
against the root `findings` was given, and `_tree` now writes the file its own
`SELF` row names into the planted tree. The second is what the question *is it
clean, or clean by a second leak* turns on, so I checked it by taking it away.

**Executed**, three ways:

- Repair undone both ways, the new case kept — the new case fails on
  `assert 0 == 1`, which is the leak reproducing.
- Resolution repaired, the planted file taken back out — **nine** cases go
  red, the floor case among them, naming the file the planted tree no longer
  carries. So the floor is now actually asking the planted tree.
- Both in place — 51 passed over the three affected modules.

The new case separates the two readings with `bin/round-record`, a path the
repository has and a planted tree does not, and it guards itself with an
assertion that names what to do if the repository ever loses that path. A3 was
left as it stood and `phases/phase-1.md` now records what each of the four
directions demonstrates, which is the right shape: A3's red was never wrong,
only narrower than its name.

### 🟢 Finding 4 is closed, and I counted the table rather than reading the correction

`skills/implement/orchestration.md`, the acts table. Counted mechanically: 20
rows — 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's
act`. Thirteen delivered rows, and twelve of them carry a sentence naming the
part their delivery does not reach. The one that does not is `Then say who
checked them, in the record`, which is the row round 1 already judged
defensible. The corrected number is right.

### 🟢 Both contract changes reach every call site

`emit(args, render, path=None)` has three callers, all in `main`, and all
three pass `path`. `_delivery(root, …)` has one caller, updated. Neither
symbol is read from outside its own module — checked across every tracked
Python file, not just the two the diff touches.

### 🟢 Q3's two option cells now describe the list by what it is a list of

Opened `CONTRIBUTING.md` lines 277–289. The bullet is **Hooks stay local and
quiet**, its sentence is *"Two hooks reach the network"*, and the three limits
it sets for a third are an opt-in condition, a throttle, and silence on every
failure. Option (a) now says the list keeps being the list of hooks that reach
the network; option (b) says a list written for hooks would become a list of
every network touch whatever fires it, and names those three limits as
hook-shaped. Both cells describe the list by what it is a list of. The
survivor the sweep found one column over is genuinely corrected rather than
exempted.

## Stage 2 — what this round opened

### 🟡 1 · The module's own docstring enumerates four red directions where five stand, and names a case no file carries

`tests/test_every_orchestrator_act_names_its_delivery.py`, lines 38–46 — the
module docstring's §*Red-first* block.

Two things are wrong in one paragraph, and one of them is the fix diff's own
consequence.

**The list is one short.** The block opens *"Red-first, per the contract's
§15, four ways"* and then lists four planted directions by name. The fix pass
added a fifth planted red direction,
`test_a_named_path_is_resolved_against_the_tree_under_check`, and did not add
it to the list. A reader who takes the docstring's enumeration as the
enumeration now misses the one direction that separates *absent from the tree
under check* from *absent from the repository* — which is the distinction the
whole of round 1's finding 3 was about.

**And the sentence in the middle names a case that is in no file.** It reads
*"… is the case that asserts the real-tree check can fail at all"*, and the
name it gives is
`test_the_four_red_directions_are_all_red` · NAME NOT IN TREE
That name — written across a line break, so a single-line search does not
find it — exists nowhere in the tree. Searched every tracked file. The case
that asserts the real-tree check can fail is
`test_every_orchestrator_act_names_its_delivery`, and the planted cases are
what make it able to fail. This half is pre-existing at `238dbeaf` and round 1
did not catch it.

<!-- Corrected in round 2's fix pass, 2026-09-22, and this note was itself
corrected after round 3, which found it declaring less than the edit had done.
THREE things changed in the paragraph above and all three are named here,
because an edit to a committed reviewer's record that its own note does not
cover is the same defect the record is about.

1. THE MARKER MOVED onto the name's own line. It sat at the end of this
   paragraph, three lines below the name, and `evidence_check.py`'s records
   arm exempts the LINE rather than the name — so the moment the fix pass took
   the name out of the module docstring, the arm refused at the line the name
   is on. Nothing had exercised the placement before, because until then the
   name resolved against the docstring that carried it. Round 3 showed the
   placement is load-bearing by putting it back: exit 2 naming
   `round-2-report.md:148` with `1 refused`, against exit 0 as it stands.

2. THE QUOTATION WAS RE-CAST so the name could sit alone on its own line. It
   read *"`<the name>` is the case that asserts the real-tree check can fail
   at all"* and now reads *"… is the case that asserts the real-tree check can
   fail at all"* with the name lifted out beneath it. This is what the marker
   rule required, and the original wording is recoverable from this note.

3. THE WORD *FOUR* WAS REMOVED from the reviewer's own sentence. It read *"and
   the four planted cases are what make it able to fail"*; it now reads *"and
   the planted cases"*. The direction is right — the module has eight planted
   trees carrying a defect, which is what round 2's own 🟡 was about — but
   round 2's report and its record then differed in one of round 2's own
   miscounts with only the report moved, and nothing said so. The edit stands
   and this is what declares it.

Round 3 also found three blank lines left below this note where markdown wants
one, and a ragged wrap the same edit introduced two lines above it. Both are
repaired here. -->

**Why it matters here rather than anywhere else.** This is the module whose
entire subject is that an enumeration nobody reads is worthless — its own
table's paragraph says *"A row that reads closed over a tree that is not is
worse than no row at all, because the next work item picks its subject from
this table."* A docstring that enumerates four of five directions and points
at a case that does not exist is that failure in the file that names it.
Nothing catches it: `evidence-check`'s not-in-tree arm reads `.md` under a
live work item, not a Python docstring, so this ships silently.

One docstring block repairs both halves. The paste-ready fix is below.

### ⬜ · The corrected citation count is a count of something narrower than the sentence says, and it understates

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`
(§*Where spec and implementation diverged*, the row *The row phase 3 was to
flip*) and `phases/phase-3.md`.

Both now say **thirty-three files** name the heading
`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, and
that **nine** of them sit outside `CHANGELOG.md` and the work-item records.
The correction was made because *eight documents* was a number nobody had
taken. The replacement is closer, and it is not reproducible from the sentence
either.

- A single-line search of the tracked tree at the commit that wrote the
  sentence gives **39** files, and **37** at the commit round 1 reviewed.
  Thirty-three is what comes out only if the work item's own six files under
  `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/` are dropped
  as well, which the sentence does not say and which a rename would not spare.
- This repository wraps its prose, and the heading is cited across line
  breaks in nine more files. Tolerating the wrap, the count is **48**.
- Two of those nine are live files outside `CHANGELOG.md` and the work-item
  records, so *nine sit outside* is **eleven** at best:
  `.github/scripts/roll_flow_measurement_issue.py`, which names the section
  twice — once in its module docstring and once inside a message a person
  reads on the tracker — and `skills/commit-pr-convention/SKILL.md`, which
  names that section as the one owner of the segment rows.

The conclusion the number supports — that renaming the heading is expensive,
so the repair belongs in an issue — is unchanged and gets stronger. What is
worth correcting is that the sentence states a bare file count while the
number behind it was taken with two exclusions nobody can recover from the
record. A count in a record outlives the round that wrote it, which is the
reason the first correction was made.

Located in the work item's records, so it owes no fix pass.

### ⬜ · Two statements of the corrected denominator survived the correction

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`
line 23, and `phases/phase-1.md` line 63.

The fix pass corrected the limit-sentence count to *twelve of the thirteen
delivered rows* in the ledger row and in both phase records. The same
denominator is stated twice more in the same two documents, and both still
say fourteen:

- `overview.md` line 23 — *"what fourteen have is something that refuses when
  the act did not happen."*
- `phases/phase-1.md` line 63 — *"What fourteen of them now have is something
  that refuses, or says so, when the act did not happen."*

A command or a check is what refuses, and there are thirteen of those. In
`phases/phase-1.md` the tally table two lines above line 63 reads 8 and 5, and
the corrected passage at line 82 of the same file says thirteen, so the file
now contradicts itself across nineteen lines.

`survivor-check` cannot see this. It reports wording a change removed that is
still standing elsewhere, and nothing removed the word *fourteen* — the
correction was written as a new passage beside the old sentences rather than
over them. Reported here because the sweep that is supposed to catch this
class structurally cannot.

Located in the work item's records, so it owes no fix pass.

### ⬜ · The new ledger row is written between O5 and O6

`seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md`.

The rows now run O1, O2, O3, O4, O5, **O7**, O6, while the header comment
above the table says *"O4 to O6 are the posting command, and O7 is round 1's
repair to it"*. Nothing reads the order — `evidence-check` reads each row's
own anchor — so this is cosmetic, and it is the kind of thing that costs a
reader a second look at release time when `fold_ledger.py` moves the fragment
into `seal/ledger.md` under a release heading. Moving O7 below O6 is the whole
repair.

## What was confirmed rather than opened

**The five new units were judged as code, not as fixes.** All five are
red-first-verified by me rather than on the fix pass's word, all five name
what they pin in their own docstring, and each of the two pairs closes its
subject from two sides — the posted body under `--segments` and under
`--spawns`, and the empty reading by its message and by nothing reaching `gh`.
`test_the_spawns_report_leaks_no_path_either` asserts only that the directory
part is absent where its sibling asserts three things; that is enough to catch
the leak, because the leaking line prints the whole path, and the sibling
carries the basename-survives assertion. Not a finding.

**The refusal's reordering introduces no regression.** `read_says` raising on
a `--says` file that does not exist now raises before the render instead of
after it. Same exception, same exit, earlier. The non-post path returns before
either call.

**The `--json` path cannot reach `post`.** `main` rejects `--post` with
`--json` at the parser, so the body substitution is not needed there.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's 🔴 1 — the posted body carried the transcript's absolute path | `skills/verify/scripts/session_cost.py#emit`, `#report_segments`, `#report_spawns` | **answered** | Closed by a rule at the seam rather than two patched lines. Enumeration checked independently: the only two body lines that can carry a path print the one `path` argument, `--latest`'s line is printed outside the buffer, and `segment_label` falls back to a field `measure_segments` stores through `os.path.relpath`. Executed: both new cases red against `238dbeaf`, green at the target SHA |
| 🟢 | Round 1's 🟡 2 — an empty `--says` posted a comment with no judgment | `skills/verify/scripts/session_cost.py#emit` | **answered** | Exit 1, nothing posted, and the refusal moved ahead of the render — further than round 1's paste-ready fix went, with the reason in a comment. Executed: both cases red against `238dbeaf`. The second pins the refusal at the `gh` seam, so it does not depend on the tracker answering |
| 🟢 | Round 1's 🟡 3 — `_delivery` resolved against `ROOT`, so the floor case was green by leak | `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery`, `#_tree` | **answered** | Clean for the right reason, checked by taking the repair away: resolution repaired with the planted file removed turns nine cases red including the floor; both undone reproduces the leak on `assert 0 == 1`. The new case separates the two readings with a path the repository has and the tree does not |
| 🟢 | Round 1's 🟡 4 — row 14's grounds named no part its delivery does not reach | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself"` | **answered** | The row now names the surface `New units` cannot reach. Counted the table myself rather than reading the correction: 20 rows, 8 checks and 5 commands, twelve of the thirteen delivered rows carry a limit sentence |
| 🟢 | Both contract changes reach every call site | `skills/verify/scripts/session_cost.py#emit`, `tests/test_every_orchestrator_act_names_its_delivery.py#_delivery` | confirmed | `emit` has three callers, all in `main`, all passing `path`; `_delivery` has one, updated. Neither is read from outside its own module, checked across every tracked Python file |
| 🟢 | Q3's two option cells now describe the list by what it is a list of | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/questions.md` Q3 | confirmed | Opened `CONTRIBUTING.md` 277–289: *"Two hooks reach the network"* and three hook-shaped limits. Both cells now scope the list to hooks; the survivor the sweep found is corrected rather than exempted |
| 🟡 1 | The module docstring enumerates four red directions where five stand, and names a case that is in no file | `tests/test_every_orchestrator_act_names_its_delivery.py`, the docstring's §*Red-first* block, lines 38–46 | open | The fix pass added a fifth planted direction and left the four-way list alone. The block also points at a case whose name exists nowhere in the tree — pre-existing at `238dbeaf`, written across a line break so a single-line search misses it. Nothing catches either: the not-in-tree arm reads `.md` under a live work item, not a Python docstring |
| ⬜ | *Thirty-three files* and *nine outside the records* are a count of something narrower than the sentence says, and both understate | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `phases/phase-3.md` | correction | A single-line search gives 39 at the commit that wrote it and 37 at the reviewed commit; 33 needs the work item's own six files dropped. Tolerating the line wraps this repository's prose uses, the count is 48, and two of the extras are live files — `.github/scripts/roll_flow_measurement_issue.py` and `skills/commit-pr-convention/SKILL.md`. The conclusion is unchanged and gets stronger |
| ⬜ | Two statements of the corrected denominator survived the correction | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 23, `phases/phase-1.md` line 63 | correction | Both still read *fourteen* where the delivered rows are thirteen. `phases/phase-1.md` now contradicts itself: its tally table reads 8 and 5, and its corrected passage at line 82 says thirteen. `survivor-check` cannot see it, because nothing removed the word |
| ⬜ | The new ledger row O7 is written between O5 and O6 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` | correction | The header comment says O7 is the last row and it is written sixth. Nothing reads the order, so this costs a reader a second look when `fold_ledger.py` moves the fragment at the release |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle. This round did not run it |

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_every_orchestrator_act_names_its_delivery.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py tests/test_session_cost_post.py`, in a clone at the target SHA | 51 passed — matches the orchestrating session's reading |
| §15 probe A — `skills/verify/scripts/session_cost.py` restored to `238dbeaf`, the four new cases kept | 4 failed. All four of round 1's new posting cases are red against the reviewed commit |
| §15 probe B — `_delivery`'s root threading and `_tree`'s planted `SELF` file both undone, the new case kept | `test_a_named_path_is_resolved_against_the_tree_under_check` fails on `assert 0 == 1`. The leak reproduces |
| §15 probe C — resolution repaired, the planted `SELF` file left out | 9 failed, 5 passed. The floor case is among the nine, naming the file the tree does not carry, so it is clean for the right reason rather than by a second leak |
| The acts table counted mechanically off `skills/implement/orchestration.md` | 20 rows: 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`. Thirteen delivered |
| Every call site of `emit` and `_delivery`, searched across all tracked Python files | 3 and 1, all updated; no caller outside either module |
| Files naming the flow-log heading, counted at `238dbeaf`, `ef010857`, `da35172f` and the target SHA, single-line and wrap-tolerant | 37 / 39 / 39 / 39 single-line, 48 wrap-tolerant. Ten outside `CHANGELOG.md` and the work-item spec directories single-line, twelve wrap-tolerant |
| A search of every tracked file for the case the module docstring names | No match anywhere in the tree. Finding 1 |
| The broad gate — full suite, repository-wide lint, typecheck | not yet, and not run here. It is the sealer's, once, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is | `overview.md` §*Not done*, already deferred in round 1, named for an issue rather than built here | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so a twenty-first act written without the prefix is counted by nobody | `overview.md` §*Not done*, already deferred in round 1 | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a), already deferred in round 1. This round confirmed the corrected grounds against the section | the repository owner, who owns that list |

## Paste-ready fixes

**Finding 1** — `tests/test_every_orchestrator_act_names_its_delivery.py`.
Replace the docstring's `Red-first` block. Two repairs: the list gains the
fifth direction the fix pass added, and the sentence pointing at a case that
does not exist is replaced by one naming the case that does.

```python
Red-first, per the contract's §15, five ways. Each planted tree below builds
a temp root with one defect in it, and `test_a_clean_planted_tree_is_clean`
is the floor beneath them -- the same tree without the defect, which has to
be clean for any of the five to mean anything. The case that asserts the
check can fail against the REAL tree is
`test_every_orchestrator_act_names_its_delivery` itself, which the five
below are what make able to fail:

  a marked heading with no row               `test_an_act_with_no_row_is_named`
  a row naming a heading no file carries     `test_a_row_naming_no_heading_is_named`
  a row naming a command that does not exist `test_a_named_command_must_exist`
  a row naming a path the tree under check
  lacks and the repository has               `test_a_named_path_is_resolved_against_the_tree_under_check`
  `still a sentence` with empty grounds      `test_a_sentence_row_carries_grounds`
```

Needs a fix: yes — finding 1, the docstring block of `tests/test_every_orchestrator_act_names_its_delivery.py`. The three corrections are records and commission nothing.
Loses a record or crashes: no


## Proof block

📋 code-review applied

· read: `rounds/round-1.md` and `rounds/round-1-report.md` of this work item ·
  the fix diff `238dbeaf..da35172f` in full, and the closure commit
  `da35172f..73e71c1a` · all four commit messages ·
  `skills/verify/scripts/session_cost.py` (`emit`, `main`, `report_segments`,
  `report_spawns`, `segment_label`, `measure_segments`, `read_says`,
  `comment_body`, `post`, `newest`) ·
  `tests/test_every_orchestrator_act_names_its_delivery.py` in full ·
  the four new cases in `tests/test_session_cost_post.py` ·
  `skills/implement/orchestration.md`'s twenty rows ·
  `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` ·
  `overview.md`, `phases/phase-1.md`, `phases/phase-3.md`, `questions.md` of
  this work item · `CONTRIBUTING.md` §*Hooks stay local and quiet* ·
  `.github/scripts/roll_flow_measurement_issue.py` and
  `skills/commit-pr-convention/SKILL.md` at their citations
· executed: the nine rows of §*Executed probes* above, in a
  `git clone --no-local` at the target SHA with its own `uv` virtual
  environment. Clone and probe deleted; the worktree is clean and no sibling
  worktree was opened
· unverified: the full suite, the repository-wide lint and the typecheck —
  the sealer's, once, after the rounds settle
