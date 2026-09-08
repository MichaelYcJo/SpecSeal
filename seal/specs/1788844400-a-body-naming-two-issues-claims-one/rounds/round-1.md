# 1788844400-a-body-naming-two-issues-claims-one — review round 1

| Field | Value |
|---|---|
| Target SHA | 38cea82b2fa15ff98f4e984d49fffbd821639fca |
| Ran by | warden on claude-opus-5 |
| PR | 261 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1, 2 and 3; finding 4 is a record correction the orchestrator makes without touching the tool |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Seven targets, in the order the prompt set them.

1. **Sentence segmentation, named as where this check will be wrong if it is
   wrong**, attacked with shapes this repository actually writes: a version
   number mid-sentence, a trailing `#150.`, `e.g.`, `i.e.`, `vs.`, an
   ellipsis, a numbered list, a table row, a nested list, a blockquote, a
   setext heading, an HTML comment, and a URL containing a fragment. The
   stated failure direction is that it under-reports rather than inventing a
   warning, and the round was told to find a shape that inverts it.
2. **Fence and code-span blanking, character for character** — an unclosed
   fence, a fence inside a list, a tilde fence, a four-space indented block,
   nested backticks, a code span containing a backtick, and a fence opened
   inside an HTML comment. Carried: a sibling branch of this release has a
   ticket about a fence under a table closing after a later heading, so
   unbalanced hiders are a live class here.
3. **The claimed/mentioned split against what the release closer and GitHub
   actually do**, in both directions.
4. **The markdown marker class, which a case already caught once** — the bare
   class read a number at the start of a line as a heading, and a number at
   the start of a line is this defect hard-wrapped.
5. **The mutation that survived and was answered by removing the code.**
   Whether the removed guard was genuinely dead, with the distinction drawn
   between an unreachable branch and one reachable only by an input nobody
   tried.
6. **The acceptance run, reproduced rather than read**, against the real body
   of the pull request that produced the ticket.
7. **The inputs a workflow actually delivers** — an empty body, whitespace
   only, Windows line endings, a very long body, a null byte, invalid UTF-8 —
   and whether CI has answered the two facts the records handed to it.

Facts carried as executed by the orchestrator at the target SHA: the module at
28 passed exit 0, and ruff check and format at exit 0 over both changed `.py`
files.

Two hazards were named. The round was told not to write a closing keyword
followed by a number outside a fence anywhere in its report or paste-ready
fixes, and told that a checker's fixtures are where a real identifier gets
inlined.

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

## Paste-ready fixes

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
```markdown
`Closes #153 and #150` claims #153. The second number carries no keyword of
its own, so nothing reads it as a claim — not GitHub, and not the script
above, whose own comment says `Closes #1, #2` is not read as two either. PR
#162 wrote that sentence; the 0.8.0 release acted on #153 alone, and #150
stayed open until somebody dealt with it by hand.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `FENCE` and `SPAN` in `close_issues_on_release.py` should cover tilde fences, four-space indented blocks, fences indented inside a list item, HTML comments and double-backtick spans — which changes what a release closes, not only what this check reports | finding 5 above, as a ⬜ | the repository owner |
| Q1 (ship the check to user repositories), Q2 (`edited` on the `pull_request` trigger), Q3 (a closing keyword before a full issue URL) | `questions.md`, already deferred there with the reasoning and a case pinning Q1's absence | the repository owner |
| Whether earlier releases lost issues this way | `overview.md` §*Not verified*, already deferred there | the repository owner |
