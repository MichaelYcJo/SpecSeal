# 1788844127-the-reviewers-report-reaches-the-record-retyped — review round 3 (verifying)

Target SHA `89772db`, PR #258, fix range `eef8610..35ad9cd`. This round reads
the diff of round 2's fixes and asks, for each verdict round 2 left standing,
whether it is actually closed. It did not re-read the branch.

Round 2 left two findings open and two record corrections standing. Both open
findings are closed on my own measurements, digit for digit. Both corrections
hold. The pin the branch's own broad run found red is moved correctly and
fails on a mutation of the sentence it names, and the class that pin belongs
to has exactly the one member already found — enumerated by construction, with
the enumeration itself seen finding that member at the commit before the fix.

What the fix pass created is where this round found something. **The whole of
the text written to answer round 2's 🟡 7 is pinned by nothing.** Delete both
new paragraphs from `agents/warden.md` §Report and the six modules that read
that file — including the case whose only job is to pin that block — pass 186
of 186 at exit 0. One commit earlier the branch planted a pin for this same
block in the same commit as the text; this fix did not.

**This record ends the run, so that finding leaves as an issue and not as a
fix.** Round 2 is the one reopening this run is allowed, and I measured what
a round 3 closing on a fix would do to the gate. §*The cap* below carries it.
Nothing here loses a record or crashes.

---

## Check 1 — round 2's 🟡 7: the replacement block sends the marker to the right place

### The measurement, reproduced from the other side

I did not take round 2's numbers. I wrote a probe markdown file under this
live work item, twice, and ran the narrowed checker over it.

**[executed]** An invented underscored name, backticked on a prose line, is
refused at `NOT-IN-TREE`, exit 2, and the refusal itself names the way
through — *write NAME NOT IN TREE on the line where the record means a name
the tree does not have*. The records arm reported `77 names read · 1 refused`.

**[executed]** The same invented name, backticked inside a fenced block and
again in a docstring inside that fence, is read by nothing: `76 names read ·
0 refused`. The run still exits 2, and the cause is the four drifted ledger
rows that are the orchestrator's, not the probe.

So the asymmetry the block is written about is real and it is the way round 2
stated it. The mechanism is `compound` in
`skills/evidence-check/scripts/evidence_check.py`, which reads a backticked
token only when it carries an underscore, and `claim_lines` above it, whose
docstring gives the reason a fence is a quotation and adds that *a marker
inside a fence changes the fix somebody pastes.*

### Does the new text stop the failure it names

Yes. Read as instructions — which is how I read it, being the first reviewer
to work under this version — it does three things the old paragraph did not.
It scopes the scan to prose in the sentence that introduces it. It says a
fence is already exempt and that marking one up corrupts it, with the reason.
And it says where the marker does go instead: on the prose line where the
same proposed unit is named, and nowhere else.

The old worked example is gone entirely rather than corrected in place, which
is the right repair — the example was the whole defect, and a reviewer
following the new text puts the marker on a prose line and never inside a
paste-ready fix. I followed it in writing this report.

### The third paragraph — the claim is true, the placement is not

**[executed as reading of the module]** The claim holds.
`tests/test_no_real_identifiers.py` carries `test_only_neutral_domains`
beside `test_only_fixture_user_paths`, so it is literally *the same module*,
and its own assertion message opens *"Real-looking domain outside the
allowlist"*. `ALLOWED_DOMAINS` has four entries and the sentence's advice —
quote only from a host the allowlist already carries — is the right advice.

Two things about it are wrong, and neither touches the claim.

**It sits in the wrong paragraph.** The block opens by saying two readers
reach the report and that the contract walks you into the first. What follows
is the first reader, then the second, then the second's fence detail, then —
at `agents/warden.md:295` — the first reader's second half. *The same module*
has to reach back across two paragraphs about a different tool to find the
module it names, and the nearest thing a reader has just been told about is
the evidence checker.

**"Quote a URL" is narrower than the check.** `DOMAIN_RE` matches any
lowercase host-shaped token ending in one of six suffixes, with no scheme and
no URL required. A report that names a bare host in passing — a package
index, an upstream project's site — fails the module while obeying the
sentence to the letter. The general half of the sentence is right, so a
reviewer who reads the whole of it is safe; the actionable half is what
under-covers.

That is ⬜ 10, with a fix that moves the sentence and widens it. **Verdict on
🟡 7: fixed.**

## Check 2 — round 2's ⬜ 8: the corrected ground is true, and the gate is a real gate

**[executed]** Round 1's unconditional gate, inserted after `close`'s target
check at `b76ce68` in a clone of its own: **36 failed, 5 passed of 41**, exit
1. The fixer's and round 2's figure, exactly.

**[executed]** The same refusal wrapped in a file test at the conventional
report path, same commit, same module: **41 passed**, exit 0, read from `$?`
directly rather than through a pipe. The corrected sentence reproduces.

The reason it reproduces is the one the record gives. The suite's `generate`
helper writes the report outside the repository and passes `--report` on
purpose — its docstring says so — so the conventional path holds nothing and
the guard is false on every one of the 41 runs.

**Which raises the question the record does not ask, so I asked it.** A gate
that never fires also passes 41 of 41, and that is the shape a sibling branch
of this release was caught on. **[executed]** A probe pair, deleted after the
run: with the record generated and an uncommitted report left at the
conventional path, `close` refuses and the message names the missing file;
with the same report committed beside the record, the refusal does not
appear. 2 passed. The narrow gate fires, and it fires on exactly the failure
round 1 named.

So the corrected ground is true in both directions: the narrow gate needs no
new record field, no template section and no checker, and it is not green by
being inert. What it gives up is what the record now says it gives up.
**Verdict on ⬜ 8: fixed** in `plan.md` and in `overview.md`, which carried
the same sentence.

One thing I would not have written into the record, offered as reading rather
than as a defect: the narrow gate also refuses a run that passed `--report`
while a stale uncommitted file happens to sit at the convention. It is a
property of the deferred design and not of anything shipped here, so it goes
in the deferred row rather than into a finding.

## Check 3 — the pin, and every pin a moved sentence could have left behind

### Both halves of the instance

**[executed]** `tests/test_the_rules_have_one_owner.py` at the target SHA:
**42 passed**, exit 0. The module is green.

**[executed]** With `once` changed to `after` in the one sentence
`GENERATOR_NAMED` names for the warden — a single word, in `agents/warden.md`
§6 — the module is **1 failed, 41 passed**, exit 1, and the failure is
`test_the_linking_carrier_names_the_generator` on the warden carrier alone.
The pin genuinely fails when the sentence it names is changed. Restored
byte-for-byte against `git show` afterwards.

### The wider question, enumerated by construction

The prompt asked for a grep of distinguishing terms. I built the enumeration
instead, because a grep of terms I choose can only find the sentences I
thought of.

The construction: a pin is a string literal in `tests/` that names a phrase
in a carrier. A pin is **left behind** when the phrase existed at the
baseline and does not exist at the target — the case is red and nobody has
run the suite. So take every file the branch changed outside `seal/` and
`tests/` — `agents/warden.md`, `docs/review-handoff-protocol.md`,
`skills/code-review/SKILL.md` and
`skills/code-review/scripts/round_record.py`, which is what the branch diff
returns — read each at both ends, flatten whitespace so a needle spanning
lines still matches, then walk every string constant in every module under
`tests/` and keep the ones present at the baseline and gone at the target.

**[executed]** At `89772db`: **0 literals**. There is no second instance.

**[executed] The enumeration seen finding the known one.** The same walk at
`eef8610`, the commit before the fix, returns **exactly 1** — the sentence
the warden pin used to name, at `tests/test_the_rules_have_one_owner.py:451`,
reported as gone from the whole tree rather than merely moved. The method
finds the defect where the defect was, and finds nothing where it was fixed.
That is the enumeration, not the instance.

The same walk covers the quieter direction as well: a negative pin — an
`assert … not in` — goes *vacuously green* when the forbidden phrase is
removed rather than red. A zero result means no changed-carrier phrase left
`tests/` at all, so there is no vacuous negative pin either.

Two things the walk cannot see, so I ran them. It reads plain literals, not
f-strings or patterns assembled at runtime, and it cannot see a pin that
counts occurrences or measures a whole document rather than naming a phrase.

**[executed]** Every module under `tests/` that reads one of the four changed
carriers as document data — 28 of them, including the line-wrap limit, the
one-word-one-meaning corpus, the moved-rule check, the contract module, the
review-axes module, the identifier module and the report module: **857
passed**, exit 0.

**[executed]** The three modules whose corpus is the committed round records,
which `89772db` itself changes: **122 passed, 1 skipped**, exit 0.

`agents/warden.md`'s prose maxima stay inside the 88-column limit the
line-wrap module holds it to — the only lines over it are table rows, which
that module exempts and which the fix did not touch.

**Verdict: the pin is correctly moved, it is seen red, and the class it
belongs to has one member.**

## Check 4 — the two corrections round 2 left standing

**Nine readers, and there is no tenth.** Confirmed by construction rather
than carried. I took every site in the tree that *lists* the round-record
directory or globs its names — the selection sites, since a site handed a
name selects nothing — and the count is nine: `_ordered` in
`hooks/routing.py`, `earlier_records` in `round_record.py`, `round_records`
and `stray_records` in `chain_check.py`, `record_files` in
`evidence_check.py`, and four in `tests/`.

Two candidates I opened that are *not* members, offered because the next
person to enumerate this class will meet them:

- `checked_by` in `chain_check.py:1608` calls `round_number` twice and looks
  like a third reader there. It lists nothing — it is handed `rel` and a cell
  value, and its `siblings` come from `round_records`. A consumer of a name,
  not a selector.
- `stray_rounds` in `hooks/routing.py:368` reaches the same `_ordered` that
  `rounds` does, so it is a second caller of one selector rather than a
  second selector. Round 2's table names `_ordered` "reached through
  `routing.rounds`"; it is reached through both, and the count is unaffected.
  `hooks/review-history-guard.py` calls three of these and selects nothing
  itself, as round 2 said.

**`record_files` is outside the class.** Confirmed: it is a module-level
function in `skills/evidence-check/scripts/evidence_check.py:1837`, not
inside any class, and it makes no record / non-record distinction to get
wrong — it walks every `.md` under a work item on purpose, which is the
reason the reviewer warning of check 1 exists at all. Both readings of round
2's sentence are true of the tree as it now stands.

## 🟡 9 — the text written to answer 🟡 7 is pinned by nothing

`agents/warden.md:289-297`. Contract §14: *a fix that changes what a person
sees documents it and pins it, in the same commit.*

`test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file` in
`tests/test_the_reviewers_report_reaches_the_record.py:263` is the case whose
whole job is to pin this block. It walks four needles — `tracked content`,
the identifier module's filename, the fixture user path, and the exemption
marker — and every one of them predates this fix. Nothing in it reaches
either paragraph the fix wrote.

**[executed]** I deleted both new paragraphs from §Report — one substitution,
asserted to have matched exactly once — and ran the six modules that read
that file, that case among them: **186 passed**, exit 0. Restored
byte-for-byte afterwards. The entire content of the 🟡 7 fix can be removed
without a single case noticing, which puts the tree one edit away from the
state round 2 found defective.

Two things make this more than a missing nicety. The branch's own commit
`b76ce68` planted this very case in the same commit as the text it pins, so
the practice being skipped is one the branch established a commit earlier.
And the thing at risk is not a style choice: the block's previous worked
example was *wrong*, in the direction of instructing a reviewer to corrupt a
paste-ready fix, and it read plausibly enough to survive its own review round.

The fix is two entries in a list that already exists and is already walked.
It is written out under §Paste-ready fixes so the issue carries it rather
than a description of it.

## ⬜ 10 — the identifier rule's second half is stated two paragraphs from the rule

`agents/warden.md:295`. Covered in check 1. The claim is true; the paragraph
is in the wrong place and its actionable half is narrower than the check it
describes.

## ⬜ 11 — one line of the pasted correction was not re-wrapped

`seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/overview.md:60`
is 90 columns in a paragraph whose other lines run 74 to 78. Round 2's
paste-ready block was joined to the tail of the preceding sentence without
re-wrapping the join. `plan.md`'s copy of the same correction wraps
correctly. No checker covers `seal/` for width, so nothing says it out loud.
A record location, so it is a correction and not `Needs a fix`.

## The cap — this record ends the run, and 🟡 9 leaves as an issue

Round 2 reported `Needs a fix: no` and the orchestrator wrote fixes over it
anyway, at `35ad9cd`. That is the reopening, and this run is allowed one.

**[executed]** Called against the tree at `89772db`: `wrote_fixes` is `True`
for `round-2.md` and `run_reopened` is `False` for it — the exact sequence
`wrote_fixes` exists to catch. `item_began` is `1788844127`, above both
`FLOOR_FROM` and `REOPEN_FROM`, so the bound is enforced here rather than
grandfathered, and `stopping_floor` from round 1's floor row returns no
errors and no notices as the records stand.

**[executed]** A probe built a scratch repository carrying round 1 and round
2 verbatim plus a synthetic round 3, and asked `stopping_floor` from round
1's floor row twice — git driven from Python so no command line carried a
commit (contract §8):

- round 3 closing 🟡 9 on a fix: `wrote_fixes` `True`, and **1 error** —
  *round-3.md is the second later record whose verdicts closed on a fix,
  after round-2.md … at most one later record may close on a fix.*
- round 3 closing it as `deferred #999`: `wrote_fixes` `False`, **0 errors,
  0 notices.**

So commissioning a fix for 🟡 9 turns the pull-request check red at
`round-1.md`. The exit the cap names is the one to take: 🟡 9 becomes an
issue, its verdict cell reads `deferred #N`, this record's `Fixes checked by`
reads `no fixes to check`, and the pull request says `chain: capped`.
`round_record.py new` should print `this record ends the run` as it writes
this record; if it prints anything else, that disagreement is worth more than
my reading of it.

`Needs a fix` therefore reads `yes` — an edit is genuinely owed on
`agents/warden.md` — and the answer to *what happens next* is the issue and
not a round 4.

## The broad gate

`not yet`, and this round can say more about it than the last two could.

A full-suite run **did** happen between `eef8610` and `35ad9cd` — it is how
the warden pin was found red, and the fix commit message records it as the
first time the suite ran on this branch. It was red, and it has been edited
since. A broad run with an edit after it was spent and not banked, so the one
that counts is still owed at `89772db`, and it is the orchestrator's.

What I did not run, and who answers it: the full suite (88 modules; I ran 32
of them, chosen as the modules that read a file this branch changed), the
unscoped `evidence_check.py --strict` with no `--ledger`, the
repository-wide lint and the typecheck, `unverified_check` and `chain_check`
— all the orchestrator's under contract §2. I did not run `--reverify` on
anything.

What I saw without acting on it: the narrowed records arm is `0 refused` at
`89772db` with my probe removed, and the ledger arm is `10 ok · 4 drifted · 0
broken · 0 external · 0 old-format`, exit 2. The four drifted rows are the
same four round 2 reported, and one of them —
`agents/warden.md#"## Report"` — is drifted again by this very fix range.
They are the orchestrator's at the closing commit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 7 | the reviewer warning's one worked example sent the exemption marker into a fenced paste-ready fix | `agents/warden.md:289` | answered | closed at `35ad9cd`. Executed — the asymmetry reproduces on my own probe: an invented underscored name in prose is refused at `NOT-IN-TREE`, exit 2, 1 refused; the same name inside a fence is 0 refused. The replacement scopes the scan to prose, says a fence is already exempt, forbids the marker there with the reason, and names the prose line as where it goes instead. The old example is gone rather than patched |
| ⬜ 8 | the recorded ground for deferring the report gate named a cost the narrow gate does not have | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md:69` | answered | corrected at `35ad9cd` in `plan.md` and `overview.md`. Executed at `b76ce68` — the unconditional gate is 36 failed / 5 passed of 41, and the same refusal guarded on the conventional path is 41 passed, exit 0. Also executed: the narrow gate is not inert — it refuses an uncommitted report at the convention and stays silent once it is committed |
| 🟡 9 | the whole of the text written to answer 🟡 7 is pinned by no case, one commit after the branch planted a pin for the same block | `agents/warden.md:289` | open | executed — both new paragraphs deleted, the six modules that read that file pass 186 of 186 at exit 0, `test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file` among them; its four needles all predate the fix. Contract §14. The run is capped, so this leaves as an issue: executed — a synthetic round 3 closing it on a fix makes `stopping_floor` return 1 error at `round-1.md`, and closing it `deferred #N` returns none |
| ⬜ 10 | the identifier rule's second half sits two paragraphs from the rule, so *the same module* reaches back across a different tool, and *quote a URL* is narrower than `DOMAIN_RE`, which matches any bare host-shaped token | `agents/warden.md:295` | open | read — the claim is true of `tests/test_no_real_identifiers.py`, whose `test_only_neutral_domains` is literally the same module and whose message opens *"Real-looking domain outside the allowlist"*. What is wrong is the placement and the narrowed advice |
| ⬜ 11 | one line of the pasted correction was not re-wrapped: 90 columns in a paragraph otherwise at 74–78 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/overview.md:60` | open | read — `plan.md`'s copy of the same text wraps correctly; no checker covers `seal/` for width |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_rules_have_one_owner.py -q`, in a clone at `89772db` | 42 passed, exit 0 |
| the same module with `once` changed to `after` in the §6 sentence the warden pin names | 1 failed, 41 passed, exit 1 — `test_the_linking_carrier_names_the_generator` on the warden carrier alone |
| a probe markdown file under this work item naming an invented underscored name in prose, through `evidence_check.py --strict --ledger` | exit 2 — `NOT-IN-TREE` at that line, 77 names read · 1 refused, and the refusal names the marker |
| the same invented name backticked inside a fence and in a docstring inside that fence, same command | 76 names read · **0 refused**; exit 2 from the four drifted ledger rows, not the probe |
| round 1's unconditional `close` gate inserted after the target check at `b76ce68`, `bin/test` over the close module in a second clone | **36 failed, 5 passed** of 41, exit 1 |
| the same gate wrapped in a file test at the conventional report path, same commit, same module | **41 passed**, exit 0 (`$?` read directly) |
| a probe pair at `b76ce68`: `close` with an uncommitted report at the conventional path, then with the same report committed | 2 passed — refuses in the first, silent in the second. The narrow gate is not inert |
| both new paragraphs deleted from `agents/warden.md` §Report, `bin/test` over the six modules that read that file | **186 passed, exit 0** — nothing pins either paragraph |
| the left-behind-pin walk over every changed carrier read at `origin/release/v0.9.2` and at `89772db`, against every string constant under `tests/` | **0 literals** present at the baseline and gone at the target |
| the same walk with the target at `eef8610` | **exactly 1** — `tests/test_the_rules_have_one_owner.py:451`, gone from the whole tree. The enumeration seen finding the known instance |
| `bin/test` over the 28 modules that read one of the four changed carriers as document data | **857 passed**, exit 0 |
| `bin/test` over the three modules whose corpus is the committed round records | **122 passed, 1 skipped**, exit 0 |
| `wrote_fixes` and `run_reopened` called on round 1 and round 2 at `89772db`, and `stopping_floor` from round 1's floor row | round 2 is `wrote_fixes` `True` / `run_reopened` `False`; `stopping_floor` returns 0 errors, 0 notices as the records stand |
| a scratch repository carrying rounds 1 and 2 verbatim plus a synthetic round 3, `stopping_floor` from round 1's floor row, git driven from Python | round 3 closing on a fix: **1 error** naming it the second fix-closing record; round 3 closing `deferred #999`: **0 errors, 0 notices** |
| `evidence_check.py --strict --ledger seal/ledger/<this item>.md .` at `89772db`, probe removed | 10 ok · 4 drifted · 0 broken · 0 external · 0 old-format; records arm 0 refused. The drift is the orchestrator's |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 9 — the two paragraphs of `agents/warden.md` §Report written to answer round 2's 🟡 7 are pinned by no case (contract §14). The run is capped, so an issue rather than a fix; the paste-ready needles are in this record | a new issue, verdict `deferred #N` | the orchestrator, at the closing commit |
| ⬜ 10 — the identifier rule's second half is two paragraphs from the rule and its advice is narrower than the check. Same file and same block as 🟡 9, so the same issue carries it | the 🟡 9 issue | the orchestrator |
| ⬜ 11 — the un-re-wrapped line in `overview.md` | the closing commit, as a record correction | the orchestrator |
| a gate in `close` that survives the flag, in either form — and the narrow form also refuses a run that passed `--report` while a stale uncommitted file sits at the convention, which the record does not say | `overview.md` §*Not done*, unchanged by this round | the orchestrator |
| the four drifted ledger rows in this work item's fragment, one of them re-drifted by this fix range, and the unscoped ledger read | `seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md` | the orchestrator, at the closing commit |
| `--asked` carrying the same defect `--report` had, and the two sibling files named in no shipped document | `questions.md` Q2 and Q3, opened by round 1 | the orchestrator |
| `docs/flow.md`'s `#228` box | `overview.md` §*Not verified* | the orchestrator |

## Paste-ready fixes

🟡 9 — two entries in the needle list of
`test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file`,
`tests/test_the_reviewers_report_reaches_the_record.py`, added inside the
existing tuple after the marker entry:

```python
        (
            "marking one up corrupts it",
            "the fence rule is gone, and the block is back to the state "
            "round 2 found: an exemption marker illustrated inside the one "
            "region the checker reads as a quotation, where nothing reads it "
            "and the smith pastes it into the fix",
        ),
        (
            "a real-looking domain outside",
            "the identifier rule's second half is unstated, so a reviewer "
            "quoting a host meets the domain arm of the same module with no "
            "warning and no way through",
        ),
```

And one line in that case's docstring, replacing *"Both escapes are pinned
for that reason: the fixture user path, and the evidence checker's own
per-line exemption marker."*:

```
    pinned for that reason: the fixture user path, the evidence checker's own
    per-line exemption marker, the rule that the marker never goes inside a
    fence (round 2, 🟡 7 -- the block's first version illustrated it there,
    which is the one region the checker never reads), and the identifier
    rule's second half, the domain arm.
```

⬜ 10 — fold the domain sentence into the paragraph that owns the rule, and
widen it past URLs. Replace the two sentences ending *"spell a user path
`/Users/x/`."* in `agents/warden.md` §Report with:

```markdown
turns `tests/test_no_real_identifiers.py` red at the pull request, after your
round has ended and where nobody can ask you what you meant. Name paths
relative to the repository root, and spell a user path `/Users/x/`. That
module has a second arm: any host-shaped token outside its allowlist fails
it, scheme or no scheme, so name a host only when the allowlist already
carries it and reach for `example.com` otherwise.
```

and delete the standalone paragraph at `agents/warden.md:295`:

```markdown
The identifier rule has a second half as well: a real-looking domain outside
its allowlist fails the same module, so quote a URL only from a host that
allowlist already carries.
```

⬜ 11 — re-wrap the join in
`seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/overview.md`,
replacing the 90-column line and the one after it:

```markdown
measurement. **A gate that reaches every run needs `new` to record the path
it read, which is a new record field, a template section and a checker.**
That is a mechanism nobody has decided to build. **A narrower gate needs
none of it** — guarded on
```

Needs a fix: yes — 🟡 9, an edit is owed on agents/warden.md; but the run is capped, so it goes out as an issue rather than as a round 4
Loses a record or crashes: no

---

## Proof

Files opened: `agents/warden.md`, `docs/review-handoff-protocol.md`,
`docs/review-chain-spec.md`, `skills/code-review/SKILL.md`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`, `hooks/routing.py`,
`hooks/review-history-guard.py`,
`skills/evidence-check/scripts/evidence_check.py`, `bin/test`,
`bin/evidence-check`, `CONTRIBUTING.md`, `CLAUDE.md`,
`tests/test_no_real_identifiers.py`, `tests/test_the_rules_have_one_owner.py`,
`tests/test_the_reviewers_report_reaches_the_record.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_record_is_generated.py`, `tests/test_docs_line_wrap.py`,
and this work item's `routing.md`, `spec.md`, `plan.md`, `overview.md`,
`changelog.md`, `rounds/round-1.md`, `rounds/round-1-report.md`,
`rounds/round-2.md` and `rounds/round-2-report.md`.

Every probe above ran in a `git clone --no-local` of this repository — one at
`89772db` and a second at `b76ce68` — or in a scratch repository built from
scratch, never in the branch's own work tree. `git rev-parse HEAD` was read
before and after every mutation and never moved. Each mutated file was
restored and verified byte-for-byte against `git show`; both clones' working
trees are clean of my edits, and every probe file was deleted. The full
suite, the unscoped ledger read, the repository-wide lint, the typecheck,
`unverified_check` and `chain_check` were not run, and nothing was
re-verified — they are the orchestrator's, once, after the rounds settle.
