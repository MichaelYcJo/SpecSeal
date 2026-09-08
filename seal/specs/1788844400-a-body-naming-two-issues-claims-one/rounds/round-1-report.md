# Round 1 review — a body naming two issues claims one

| Field | Value |
|---|---|
| Target SHA | `38cea82b2fa15ff98f4e984d49fffbd821639fca` |
| Base | `release/v0.9.2` (= `origin/main` at `bcf48b8`) |
| Branch | `feat/167-a-body-naming-two-issues-claims-one` |
| Pull request | #261 (draft) |
| Reviewed in | a `git clone --no-local` of the repository at the target SHA |

## How to read this report

Every closing keyword written next to a number below is inside a fenced block
or a code span, on purpose. This file becomes part of the work item and its
fixes may reach a pull request body, where `close_issues_on_release.py` would
read one as a claim.

## What holds

The design is the right one and the acceptance case reproduces exactly. Run
against PR #162's live body in the clone, the check names `#153` as claimed,
lists `#150, #163, #159, #161, #160, #158` as mentioned, prints one warning
quoting the sentence, and exits 0 — the account's numbers, in the account's
order.

Four things the round was asked to attack came back clean, and each was
executed rather than read:

- **The claimed/mentioned split agrees with the release closer.** Over all 33
  shapes the probe drove, `CLOSING` applied to this module's blanked copy and
  `keywords_in` applied to the raw body returned the same list every time — no
  divergence in either direction. The identity case is real: it takes the
  sibling from `sys.modules` rather than loading it again, and the tuple is
  what asks the question.
- **The removed position guard was genuinely dead.** The pre-`6b81d10`
  implementation was restored beside the current one and both were driven over
  250,000 random bodies built from the atoms that can reach the guard, plus
  every combination of eight atoms up to length five. Zero bodies where the
  answer differed. A separate probe looked for the input the account could not
  name — an `ISSUE_REF` match landing on a claimed digit position while
  carrying a different number — and found none in 50,000 bodies, which is what
  the account's reasoning predicts: both patterns capture a maximal digit run
  starting one character after the hash, so they cannot disagree.
- **The marker class asks for the space where CommonMark asks for one.**
  `#22`, `*bold*`, `0.9.2`, `####### x` and `-x` at the start of a line are all
  correctly *not* boundaries; `- `, `1. `, `1) `, `>` and `|` all are. The
  repair the implementer made after its own case went red is sound.
- **Nothing in the workflow step can be made to inject a workflow command.**
  A body carrying `::error::` and `%0A::error::` produces one annotation line
  with both mid-line, because the sentence is whitespace-collapsed before it is
  quoted. Newlines, carriage returns, NEL and `U+2028` are all collapsed by
  `str.split()`.

The inputs a runner delivers were driven too: an empty body, a whitespace-only
body, CRLF line endings, a null byte, and a 200,000-character body all exit 0
with no exception, and the largest of those takes 0.8 s.

## 🟡 1 — a horizontal rule is not a boundary, and that invents a warning

`.github/scripts/issue_claims_check.py:107`

`BLOCK_START` requires the space CommonMark requires after a bullet, which is
the repair that stopped `#22` at the start of a line reading as a heading. The
same requirement takes a **thematic break** and a **setext heading underline**
out of the class, because neither has a space after its first character:

| Body | Reported |
|---|---|
| a claim, then `---`, then an unrelated `#22` | warning |
| a claim, then `***`, then an unrelated `#22` | warning |
| a claim, then `___`, then an unrelated `#22` | warning |
| a claim, then `===`, then an unrelated `#22` | warning |

In each of those the two numbers sit in different markdown blocks — the first
line is a setext heading or the block above a thematic break, the last is a new
paragraph. Rule 3 as the module docstring states it says the segment ends;
`BLOCK_START` says it does not.

**Why it matters.** The plan spends its whole budget on one direction:
*"splitting early can only put two numbers in different segments, so the check
under-reports rather than inventing a warning."* This is the inversion. A
false positive is the failure the design names as the one that would make
people scroll past the annotation.

**How reachable it is here.** No pull request body among #162, #225, #239,
#245, #251, #252 and #254 carries a line of that shape, and no file under
`docs/`, `CONTRIBUTING.md` or `README.md` does either. So this is not costing
the repository a warning today. It is one regex line to close, the fix keeps
all 28 cases green, and a horizontal rule between sections is ordinary in a
pull request body written by anyone who has not read this module.

## 🟡 2 — the section teaching the rule writes the failing shape in bare prose

`docs/issues-and-milestones.md:117`

The new section closes by saying that a body quoting the failing shape *inside
a fence or a code span, the way this section does,* is not an instance of it.
The section does not do that throughout. Line 117 writes the shape unquoted,
and this branch's own check reads it as one:

```
$ python3 .github/scripts/issue_claims_check.py --body-file docs/issues-and-milestones.md
claimed (closed when the release reaches `main`): #153
mentioned only (nothing closes these): #179, #155, #162, #150, #136, #30
::warning::this sentence claims #153 and NOT #150: "PR #162 wrote that
sentence, the 0.8.0 release closed #153, and #150 was closed by hand
afterwards." …
```

A past-tense narrative keyword is still a keyword: `KEYWORDS` carries the past
tense of all three verbs.

**Why it matters.** Documents are not pull request bodies, so nothing closes
anything today. But this repository's own reasoning is that *its bodies quote
its documents routinely* — that sentence is why the fence masking exists at
all. A body that quotes this paragraph carries a claim its author did not
intend, and it earns the warning from the paragraph that told them the section
was safe to quote.

## 🟡 3 — nothing pins what the check prints

`.github/scripts/issue_claims_check.py:208`

`report()` writes four distinct strings a person reads, and one of them —
`::warning::` — is what turns the third into a job annotation rather than a
line in a log nobody opens. No case in `tests/test_a_body_naming_two_issues_claims_one.py`
asserts any of them. `test_a_body_is_never_a_failure` calls `main` and throws
the output away with `capsys.readouterr()`; every other case goes through
`read()`, which returns tuples. Grepping the whole `tests/` tree for
`::warning`, `claimed (closed`, `mentioned only` and `no sentence claims`
returns nothing from this module's cases.

**Why it matters.** `skills/agent-contract/SKILL.md` §14: a change to a
rendered line is a change someone reads and acts on, and the test that pins the
new text is what keeps the next edit from quietly taking it back. Rewriting
`::warning::` to `WARNING:` — or dropping the prefix while tidying the
f-string — leaves all 28 cases green and silently converts the only output
anybody sees into log noise. The mutation log has no row for it either, which
is consistent: there was no case to go red.

## 🟡 4 — the two facts the record hands to CI are not the ones CI answered

`seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md:27`

The *Not verified* table names **CI, on this pull request** as the answerer for
two facts: that `github.event.pull_request.body` arrives as an empty string
rather than absent for a description-less pull request, and that `::warning::`
renders as an annotation on the job. Neither is answered by the run on #261,
and neither can be:

- #261 **has** a description, so the empty-body path was never taken. The
  step's log shows `PR_BODY` carrying the full body.
- #261's body claims one number and mentions none, so the check printed *"no
  sentence claims one number and names another beside it"* and emitted no
  `::warning::` at all. `gh api repos/.../check-runs/101954866402/annotations`
  returns three annotations — a Node 20 deprecation, the chain-check failure,
  and its `Process completed with exit code 1` — and none from this step.

So the annotation-rendering fact is unobserved and the record points at a run
that structurally cannot observe it. The answerer named will not answer.

What CI **did** answer, and what the record should say instead: the step runs
first in the job, reads the body out of `env:`, prints the two lists, and exits
0 — measured on the run for `38cea82`, where the job went red four steps later
at `chain_check` for the missing round record, which is this round.

## ⬜ 5 — the masking gaps the plan does not enumerate

`.github/scripts/issue_claims_check.py:123`

The plan names one thing the masking gives up — an unclosed fence — and calls
the body that reaches it malformed markdown. Four more shapes are well-formed
CommonMark and reach it too. Each was driven; each reports a claim and a
warning where GitHub would render code and create no reference at all:

| Shape | Result |
|---|---|
| a tilde fence (`~~~`) around the failing shape | claim + warning |
| a four-space indented code block | claim + warning |
| a fence indented inside a list item | claim + warning |
| an HTML comment | claim + warning |
| a double-backtick code span | claim + warning |

This is **⬜ rather than 🟡** for two reasons. `FENCE` and `SPAN` are imported
from `close_issues_on_release.py`, so the check agrees with what the release
closer will actually do in every one of those cases — the split it reports is
true about this repository even where it is false about GitHub. And the shapes
are absent here: no `~~~` fence in any `.md` file in the tree, and one HTML
comment in `docs/`, in a sentence with no issue number near it.

What is worth recording is that §12's class is wider than the instance the plan
named. Closing it means widening `FENCE` in the release closer, which changes
what a release closes, and that is a decision rather than a fix.

## ⬜ 6 — the same annotation twice

`.github/scripts/issue_claims_check.py:199`

A segment that names the same unclaimed number twice earns one warning per
occurrence, with identical text. Driven: a body claiming `#11` and naming `#22`
twice in one sentence prints the warning twice.

## ⬜ 7 — a numeric URL fragment beside a claim earns a warning

`.github/scripts/issue_claims_check.py:199`

The plan says a hex colour or a URL fragment *"would read as issue `#123456` in
the mention list"*, and adds that the warning arm needs a closing keyword in the
same segment before it says anything. That is true and reads as a reassurance,
but the condition is easy to meet: a claim and a link ending `#22` in one
sentence produces a warning naming `#22`. It belongs in the same paragraph as
the mention-list caveat rather than being left to be found.

## Regression tests to plant

| Case | Destination |
|---|---|
| A claim, a `---` line, and an unrelated `#N` produce no warning — one case per break shape (`---`, `***`, `___`, `===`) | `tests/test_a_body_naming_two_issues_claims_one.py` |
| The three report lines and the `::warning::` prefix, asserted against `capsys` for one claiming body and one clean body | `tests/test_a_body_naming_two_issues_claims_one.py` |
| `read()` over `docs/issues-and-milestones.md` warns about nothing — the document that teaches the rule does not carry an unquoted instance of it | `tests/test_a_body_naming_two_issues_claims_one.py` |

The first was shown red before the fix and green after, in the clone: the four
shapes warned at `38cea82` and stopped warning with the regex below, with all 28
existing cases still passing.

## Facts for the evidence ledger

- The removed `claimed_at` position guard is dead by construction, not only by
  the mutation that found it: `CLOSING` and `ISSUE_REF` both capture a maximal
  digit run beginning one character after the hash, so a match at a claimed
  digit position always carries the claimed number. Measured over 250,000
  random bodies and every combination of eight atoms up to length five, with no
  difference in the answer.
- The masking substitution and the sibling's collapse produce the same
  `CLOSING` result on all 33 shapes driven, including a fence between a keyword
  and its number.
- `evidence_check.py --strict --ledger seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md .`
  → 9 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0, at the
  target SHA.

## Broad-gate state

`not yet` — the full suite, the repository-wide lint and the typecheck have not
been run for this branch by anybody, and `skills/agent-contract/SKILL.md` §2
keeps them out of this round. CI on #261 ran `pytest` on three platforms and
`lint`, all passing at `38cea82`; that is the workflow's own broad run and not
the orchestrator's gate. The gate is not due yet: findings 1 to 4 are open.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A thematic break or a setext underline is not a segment boundary, so a claim above one and an unrelated `#N` below it earn a warning — the false-positive direction the design forbids itself | `.github/scripts/issue_claims_check.py:107` | open | Executed: four break shapes each produced a warning at the target SHA; the module docstring's rule 3 says the segment ends there. Not reachable from any body or document in the tree today |
| 2 | The section that teaches the rule writes the failing shape in bare prose, in the paragraph claiming it only quotes the shape inside a fence or a span | `docs/issues-and-milestones.md:117` | open | Executed: the branch's own check over that file names `#153` claimed and warns on the sentence. `KEYWORDS` carries the past tense, so a narrative keyword is a keyword |
| 3 | Nothing pins the four strings the check prints, `::warning::` included — the prefix that makes the third an annotation | `.github/scripts/issue_claims_check.py:208` | open | Read: no case asserts any of them; `test_a_body_is_never_a_failure` discards the output. Executed: grepping `tests/` for the four strings returns nothing from this module. §14 |
| 4 | Two facts the record hands to CI on #261 are not answered by that run and cannot be | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md:27` | open | Executed: the step's log shows a non-empty `PR_BODY` and no warning printed; the check-run annotations API returns three annotations, none from this step |
| 5 | The masking gives up four well-formed shapes the plan does not enumerate, beyond the unclosed fence it does | `.github/scripts/issue_claims_check.py:123` | open | Executed: tilde fence, indented code block, fence inside a list, HTML comment and double-backtick span each report a claim and a warning. Consistent with the release closer, and absent from the tree |
| 6 | A repeated unclaimed number in one segment prints the identical annotation twice | `.github/scripts/issue_claims_check.py:199` | open | Executed |
| 7 | A numeric URL fragment in the same segment as a claim earns a warning; the plan's caveat names only the mention list | `.github/scripts/issue_claims_check.py:199` | open | Executed |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_a_body_naming_two_issues_claims_one.py -q` in the clone at `38cea82` | 28 passed |
| The check against PR #162's live body (`gh pr view 162 --json body`) | claimed `#153`; mentioned `#150, #163, #159, #161, #160, #158`; one warning; exit 0 — the account reproduced |
| 33 attack shapes through `read()`: thematic breaks, setext underlines, HTML comment and block, indented code, tilde fence, fence in a list, unclosed fence, fence opened in an HTML comment, double-backtick span, numeric URL fragment, ordered/blockquote/pipe/nested markers, `e.g.` `i.e.` `vs.` and an ellipsis, CRLF, seven-hash heading, null byte, empty and whitespace-only bodies | four false warnings (finding 1), five masking gaps (finding 5), one duplicate (finding 6), one URL fragment (finding 7); everything else as documented; no exception on any input |
| Differential: `CLOSING` over this module's blanked copy vs `keywords_in` over the raw body, on all 33 shapes | 0 divergences |
| Differential: the pre-`6b81d10` `read()` with the position guard vs the current one, over 250,000 random bodies and every combination of eight atoms up to length five | 0 bodies where the answer differed |
| Invariant probe: an `ISSUE_REF` match landing on a claimed digit position while carrying a different number, over 50,000 random bodies | 0 occurrences — the guard is dead by construction, not only by the mutation |
| Annotation injection: a body carrying `::error::`, `%0A::error::` and `::set-output` inside the claiming sentence | one annotation line, every command mid-line; the sentence is whitespace-collapsed first |
| Scale: 204,000-character body / 20,000 characters of unclosed fences / a single 200,000-character line | 0.83 s / 0.002 s / 0.006 s, no exception |
| `evidence_check.py --strict --ledger seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md .` | 9 ok · 0 drifted · 0 broken, exit 0 |
| The proposed `BLOCK_START` widening applied in the clone, both `__pycache__` directories cleared, module re-run, PR #162 re-read | 28 passed; the four false warnings gone; `#162` still reproduces exactly |
| `gh pr checks 261` and the check-run annotations API for the hygiene run at `38cea82` | the step ran first, printed `claimed … #167` / `mentioned only … none` / no warning, exit 0; the job went red at `chain_check` for the missing round record; no `::warning::` annotation on the run |
| `git diff bcf48b8..HEAD -- tests/test_no_real_identifiers.py` | empty — the fixture allowlist was not extended, and PR #162's body is not committed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `FENCE` and `SPAN` in `close_issues_on_release.py` should cover tilde fences, four-space indented blocks, fences indented inside a list item, HTML comments and double-backtick spans — which changes what a release closes, not only what this check reports | finding 5 above, as a ⬜ | the repository owner |
| Q1 (ship the check to user repositories), Q2 (`edited` on the `pull_request` trigger), Q3 (a closing keyword before a full issue URL) | `questions.md`, already deferred there with the reasoning and a case pinning Q1's absence | the repository owner |
| Whether earlier releases lost issues this way | `overview.md` §*Not verified*, already deferred there | the repository owner |

## Paste-ready fixes

Finding 1 — `.github/scripts/issue_claims_check.py`, replacing the single-line
`BLOCK_START`. Verified in the clone: all 28 cases stay green, the four false
warnings stop, and `#22`, `*bold*`, `0.9.2`, `-x`, `--`, `####### x`, `= x` and
`a --- b` are all still correctly *not* boundaries.

```python
# Rule 3. A line that opens a new markdown block ends the segment before it,
# even with no blank line between them -- consecutive list items are the case
# that matters, and they are written without one.
#
# Every marker that CommonMark requires a space after asks for one here. A
# bare `[-*+>|#]` class reads `#22` at the start of a line as a heading, and
# `#22` at the start of a line is this defect hard-wrapped -- which is the one
# thing this module exists to see. `*bold*` opening a line is the same trap
# one marker over. `>` and `|` take no space in the markdown either.
#
# The space requirement takes the run-of-three markers OUT of the class, and
# they have to come back separately: a thematic break and a setext underline
# are blocks in their own right, and without these four alternatives a claim
# above a horizontal rule and an unrelated `#N` below it land in one segment
# and earn a warning -- the false positive this whole design is spending to
# avoid. They match a WHOLE line only, so `a --- b`, `--` and `= x` are prose.
BLOCK_START = re.compile(
    r"^[ \t]*(?:"
    r"[-*+](?=\s)"
    r"|\#{1,6}(?=\s|$)"
    r"|\d+[.)](?=\s)"
    r"|[>|]"
    r"|(?:-[ \t]*){3,}\r*$"
    r"|(?:\*[ \t]*){3,}\r*$"
    r"|(?:_[ \t]*){3,}\r*$"
    r"|=+[ \t]*\r*$"
    r")"
)
```

Finding 1 — the cases, for `tests/test_a_body_naming_two_issues_claims_one.py`.
Shown red against `38cea82` before the regex above and green after.

```python
@pytest.mark.parametrize("rule", ["---", "***", "___", "==="])
def test_a_horizontal_rule_ends_the_segment(rule):
    """A thematic break and a setext underline are blocks of their own, and
    the space every other marker requires takes all four out of the class. A
    claim above one and an unrelated number below it are not one sentence, and
    warning about them is the false positive this check spends everything to
    avoid."""
    assert warned(f"Closes #11\n{rule}\n#22 is unrelated.") == []
```

Finding 2 — `docs/issues-and-milestones.md`, replacing the sentence that spans
lines 116-118. No keyword now stands immediately before a number, so a body
quoting the paragraph carries no claim.

```markdown
`Closes #153 and #150` claims #153. The second number carries no keyword of
its own, so nothing reads it as a claim — not GitHub, and not the script
above, whose own comment says `Closes #1, #2` is not read as two either. PR
#162 wrote that sentence; the 0.8.0 release acted on #153 alone, and #150
stayed open until somebody dealt with it by hand.
```

Finding 2 — the case that keeps it from coming back, for
`tests/test_a_body_naming_two_issues_claims_one.py`.

```python
def test_the_document_that_teaches_the_rule_carries_no_instance_of_it():
    """`docs/issues-and-milestones.md` says a body quoting the failing shape
    inside a fence or a code span is not an instance of it. This repository's
    bodies quote its documents routinely, so the section has to hold to that
    everywhere -- a narrative past-tense keyword is still a keyword, and
    `KEYWORDS` carries the past tense of all three verbs."""
    with open(
        os.path.join(ROOT, "docs", "issues-and-milestones.md"), encoding="utf-8"
    ) as f:
        claimed, _, warnings = read(f.read())
    assert warnings == [], warnings[0][2] if warnings else ""
```

Finding 3 — the cases that pin what a person sees, for
`tests/test_a_body_naming_two_issues_claims_one.py`. The `::warning::` prefix
is the whole difference between a job annotation and a line in a log nobody
opens, and nothing asserts it today.

```python
def test_the_warning_is_written_as_a_job_annotation():
    """`::warning::` at the start of the line is what makes GitHub render this
    on the job rather than bury it in the log. Dropping the prefix while
    tidying the f-string leaves every other case green."""
    lines = []
    check.report(*read("Closes #11 and #22"), out=lines.append)
    ((warning,),) = ([line for line in lines if line.startswith("::warning::")],)
    assert "#11" in warning and "#22" in warning


def test_the_two_lists_say_what_closes_and_what_does_not():
    """The author acts on these two lines. A rename that leaves `read()` alone
    changes what they are told and no case notices."""
    lines = []
    check.report(*read("Closes #11 and #22"), out=lines.append)
    assert lines[0] == (
        "claimed (closed when the release reaches `main`): #11"
    )
    assert lines[1] == "mentioned only (nothing closes these): #22"


def test_a_clean_body_says_so_rather_than_saying_nothing():
    """Silence reads as a check that did not run."""
    lines = []
    check.report(*read("Closes #11"), out=lines.append)
    assert lines[-1] == (
        "no sentence claims one number and names another beside it"
    )
```

Finding 4 — `seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md`,
replacing the row at line 27 of the *Not verified* table with two rows: one for
what the run at `38cea82` actually settled, one for what is still open and how
it could be settled.

```markdown
| Whether `::warning::` renders as an annotation on the job. The run on #261 at
`38cea82` cannot answer it — that body claims one number and mentions none, so
the check printed *no sentence claims…* and emitted no `::warning::` at all,
and the check-run annotations API returns three annotations, none from this
step. Settling it needs a pull request whose body carries the shape, or a
throwaway body edit before merge | the repository owner |
| Whether `github.event.pull_request.body` arrives as an empty string rather
than absent for a description-less pull request. #261 has a description, so
that path was not taken either. Read from GitHub's documentation | the
repository owner |
```

Findings 6 and 7 — one edit closes the duplicate and one comment closes the
caveat, both in `.github/scripts/issue_claims_check.py#read`. The `seen` set is
per segment, so a number named in two different sentences still earns two
warnings, which is right — each sentence is a separate thing to fix.

```python
        sentence = " ".join(body[start:end].split())
        # One warning per unclaimed NUMBER in this segment, not one per
        # occurrence: `Closes #1 and #2 and #2` is one thing to fix, and the
        # same annotation printed twice reads as two. Per segment, so the same
        # number named in two sentences still earns one warning each.
        #
        # The candidate is any `#N`, which is what the mention list already
        # says: a hex colour or a link ending `#22` reads as an issue number
        # here too, and beside a claim in the same sentence that is a warning
        # rather than a mention. The alternative -- excluding a `#N` preceded
        # by a URL character -- is a second syntax to be wrong about.
        seen = set()
        for m in ISSUE_REF.finditer(text, start, end):
            if m.group(1) in claimed or m.group(1) in seen:
                continue
            before = [c for c in here if c[1] < m.start(1)]
            if before:
                seen.add(m.group(1))
                warnings.append((before[-1][0], m.group(1), sentence))
```

Needs a fix: yes — findings 1, 2 and 3; finding 4 is a record correction the orchestrator makes without touching the tool
Loses a record or crashes: no
