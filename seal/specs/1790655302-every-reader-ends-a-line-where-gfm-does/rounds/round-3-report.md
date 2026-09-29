# 1790655302-every-reader-ends-a-line-where-gfm-does — round 3 report

| Field | Value |
|---|---|
| Round | 3, a verifying round, and the last before the cap |
| Target | round 2's fix diff `81a770bb..0fd554dd` (4 commits), read at branch HEAD `c7fef45f` |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the branch at `c7fef45f`, with `rider_check.py` at `7c339169` loaded beside it for base comparisons |
| Earlier rounds | rounds 1 and 2, read for their coordinates and their verdicts |

## What this round found, in the order one causes the next

1. All three of round 2's verdicts are closed for what they named (executed).
   Round 2's new cases fail against `rider_check.py` at `7c339169`, and the
   byte case would also catch the write half on a CRLF platform.
2. Round 2's fix answers *is the marker piece read* with the hasher's
   answer. It does not answer *which block does the reader run on from that
   piece*. The reader still runs the block over its own pieces, with its own
   test for a closing `-->` and its own test for the comment kind. Where a
   break sits inside a line the hasher cuts, the two blocks part. The rider's
   stamp then lands on a GFM line the hasher does not cut, and the stamp is
   hashed into the region it names. `--reverify` rewrites it on every run and
   the check never reads ok (🟡 1). At `7c339169` these riders were not read
   at all. This is the F round 3 symptom the changelog fragment says is
   gone, in a new shape.
3. Ledger row G13 states the invariant 🟡 1 breaks (⬜ 2).

The two carried questions have answers with no finding. `gather_changelog.py`
reading and writing in the default newline mode is outside this item's class,
and it changes nothing that reaches the repository. The raw U+2028 in
`rounds/round-1.md` is what spec S1 asks a record to keep, and no gate reads
it differently from its escape. Both answers are executed.

## The three asks

### 1. Is each of round 2's verdicts closed?

**🟡 1, a rider behind a comment on its GFM line.** Closed for the three
shapes it named. The case's three parameters fail with `rider_check.py` at
`7c339169`, and pass at HEAD (executed).

*The recursion terminates on every input.* This is by reading, and a fuzz run
agrees. `comment_blocks` recurses only inside `if text is not None`. The inner
call passes GFM lines and no text, so it cannot recurse again, and the depth
is one. A fuzz over 13,237 generated `.py`, `.yml` and `.md` texts holding
the marker raised no `RecursionError` and no other exception (executed).

*No verdict moved for a file with no mid-line marker.* Four probes, all
executed:

- The fuzz texts holding none of the eight characters: 0 differ in their
  riders (start, end, body) between `7c339169` and HEAD.
- The 576-prefix differential (six whitespace prefixes, eight breaks, six
  whitespace suffixes, in `.yml` and `.md`): 0 riders read but not cut at
  HEAD, and 0 differ from `7c339169`.
- The three controls (code or prose before the break, in `.yml`, `.md` and
  `.py`): stepped over at both, cut by neither.
- The 25 files under the rider roots that carry the marker: identical riders
  at both. `check()` on the tree reads `19 ok, 0 drifted, 0 problems`.

The class is still open one step further on. See 🟡 1.

**🟡 2, `write_block` and CRLF.** Closed. `reverify` on six byte shapes comes
back byte for byte apart from the stamp, and `check()` reads 1 ok afterwards
(executed). The shapes are LF, CRLF, lone CR, CRLF with a form feed inside
the rider, lone CR with a U+2028 inside the rider, and one file mixing CRLF,
LF and CR. I also checked the write half, which round 2's fix pass could not
see on macOS. I simulated a CRLF platform by giving every default-mode write
`newline="\r\n"`, as the text layer does there. With the write's `newline=""`
removed, a CRLF file and an LF file both stop coming back byte for byte, and
a lone-CR file stays byte-exact. So the CRLF parameter of the byte case is
red on such a platform, as G15's re-read note says (executed, simulated).

The rider's numbering is safe with the raw read. `Rider` is built from the
default-mode text, and that translation replaces one line end with one line
end. A `\r` followed by one of the eight is still two pieces both ways. The
mixed-ending shape went through `strict=True` without raising (executed).

**⬜ 3, G15 and the fragment.** Closed. G15's claim is true at HEAD by the
six shapes above. The last changelog bullet ("a file with CRLF or lone-CR
line ends came back with LF throughout") describes the old behaviour, and
the shapes show it is gone. `evidence_check.py .` exits 0 at HEAD (executed).
G13 is true as to where a rider is read, and false as to what the reader then
cuts (⬜ 2).

### 2. `gather_changelog.py`'s default newline mode, carried from the fix pass

Not a defect in this item's class, and the orchestrator's reading holds. I
ran it rather than taking it (executed, in temporary roots holding the
tree's `CHANGELOG.md` and all 29 fragments):

| Input line ends | `--check` | `--dry-run` | the file `--version 0.16.0` writes | the `## ` refusal |
|---|---|---|---|---|
| LF | exit 1, the baseline | exit 0 | 0 CR bytes | exit 1, names `changelog.md:69` |
| CRLF, every file | stdout identical to LF | stdout identical | byte-identical to LF | stdout identical, same line number |
| lone CR, every file | stdout identical to LF | stdout identical | byte-identical to LF | stdout identical, same line number |

The read cannot change the output. Universal-newline reading ends a line at
LF, CR and CRLF, which is the set GFM ends a line at. So `gfm_lines` sees the
same lines either way, and the line number the refusal prints is the file's
own.

The write is a platform question, not a line-reading one. On a simulated
CRLF platform the write produced 8,022 CRLF, and with each one read as LF the
file equals the LF output. In a scratch repository carrying this tree's
`.gitattributes` (`* text=auto eol=lf`), that file shows ` M` in `git status`
before staging, and `git diff` is empty. Staging it leaves `git diff --cached`
empty, and its blob equals the LF write's (executed). Nothing different
reaches the repository.

The spec's class is a reader that splits with `str.splitlines`, and the
character turned into a line break where it writes the text back. This
script does neither. It also makes no claim about CRLF, unlike `write_block`,
where the item's own fragment did (round 2's 🟡 2).

### 3. The raw U+2028 in `rounds/round-1.md`

Not a defect by ⬜ 5's rule, and no check reaches it.

The line holds a raw U+2029 as well. Both sit at
`rounds/round-1.md:78`, and at `rounds/round-1-report.md:278` in the report
it was generated from. They are inside a fenced paste-ready fix, as two
members of a Python string constant commented "Every character
`str.splitlines` ends a piece at". Round 1's ⬜ 5 was a sentence made false
by its character. The sentence said "six ASCII characters" and held the raw
one. Here nothing says escape, and the constant holds exactly the characters
it lists. The record keeps the report's character rather than a line break,
which is spec S1 working as written. The spec's grounding also keeps closed
records as they are.

Neither file existed when round 1 scanned the tree at `260c86ac`. They
arrived at `7bfea5f4`, and round 2 checked only `phases/phase-4.md`, so no
round had looked at them before this one.

Whether anything reads them differently from their escapes, I ran each gate
the hygiene workflow runs over the records, and six test modules that walk
the committed records, once with the characters raw and once with both files
rewritten to ` ` and ` ` and committed. The six modules are
`test_no_real_identifiers.py`, `test_a_finding_id_is_a_bare_integer.py`,
`test_a_record_says_what_ran_it.py`, `test_a_record_states_what_the_tree_has.py`,
`test_chain_check_at_the_pull_request.py` and
`test_a_corrected_sentence_survives_elsewhere.py`. Every gate gave the same
exit code and the same output. The only differences were the commit
abbreviation the range gates print and the test run's timing (executed). The
gates were `evidence_check.py .`, `unverified_check.py --baseline`,
`chain_check.py --baseline`, `survivor_check.py --range`,
`correction_check.py --range`, `gather_changelog.py --check`,
`fold_ledger.py --check` and `payload_meter.py --sections`.

## Findings from execution

### 🟡 1 — A rider read on a line the hasher cuts runs on past it, so its stamp is hashed and `--reverify` never settles it

`.github/scripts/rider_check.py:339` (the `cut` set round 2 added) with
`riders_in` at `:408` and the HTML branch at `:372`–`:375`.

Round 2's fix makes the reader read a mid-line marker piece wherever
`comment_blocks` over the GFM lines cuts that line. Once the piece is read,
the reader runs the block on over `str.splitlines` pieces by its own rules.
The hasher runs its block over GFM lines by the same rules applied to whole
lines. Two rules part:

- **Where the block ends.** The HTML branch ends a block at a line holding a
  closing `-->` anywhere. A GFM line that opens with a closed HTML comment,
  then a U+2028, then the rider's own opener, holds a `-->` before the marker.
  So the hasher ends its block on that line. The reader's piece starts after
  the break and holds no `-->`, so the reader runs on to the next line. That
  next line is where the tree's own markdown riders put the stamp.
- **Which comment kind the line is.** In a `.py` file, a GFM line
  `# note`, U+2028, then an HTML opener with the marker is a `#` block to the
  hasher. The reader reads the piece as an HTML block and leaves the comment
  state open behind it. The next line, `b = 2  # …` with a marker, is then
  read as a second rider that the hasher does not cut at all.

Executed on a markdown file under `templates/`, heading `## Heading`, with a
rider whose stamp is on the line after its opener:

| | `7c339169` | `c7fef45f` |
|---|---|---|
| closed comment, U+2028, then the rider | 0 riders read, `check` 0 drifted | 1 read. `check` 1 drifted. `--reverify` wrote 1, `check` 1 drifted. `--reverify` wrote 1 again, `check` 1 drifted |
| the same rider with no prefix (control) | 1 drifted, then 1 ok after `--reverify` | the same |

The fuzz above states the class. Among 13,237 generated texts, the texts in
which a rider read has its marker piece or its stamp piece on a GFM line the
hasher does not cut number 0 at `7c339169` and 4 at `c7fef45f`. All 4 are
one of the two shapes above.

No file in the tree has either shape, so the defect is latent. It is on the
loud side, but it is an alarm no action clears short of rewriting the rider.
It is also the symptom the changelog fragment names as gone: "its own stamp
was hashed and `--reverify` could not make it read ok". At `7c339169` these
riders were silent. `ee6215be` made them read.

**The fix derives the reader's blocks from the hasher's.** `riders_in` takes
`comment_blocks` over the GFM lines, which is exactly what `region_lines`
cuts. It gathers the pieces that start inside each block and splits them at
every piece carrying the marker. Every piece of every rider read is then on a
cut line by construction. Two riders on one GFM line stay two riders. A
piece before the first marker (`# note`, a closed comment) is in none. With
it, all of the following were executed:

- The three modules touching the rider check (the item's module,
  `test_a_rider_reaches_its_file.py`, `test_the_hooks_hide_what_a_renderer_hides.py`)
  pass, 193 cases with the new case.
- The fuzz reads 0 riders out of the cut, and 0 texts without the eight
  characters differ from `7c339169`.
- The 576-prefix differential agrees with the hasher and with `7c339169`.
- The 25 tree files read the same riders. `rider_check.py --root .` prints
  `19 ok · 0 drifted · 0 broken` and exits 0.
- `ruff check` and `ruff format --check` pass on both files.
- The new case fails for both of its shapes against `rider_check.py` at
  `c7fef45f`, and passes with the fix.

What the fix leaves, and why it is right to leave it. With the fix, the
markdown shape reads BROKEN "no verification stamp", because the hasher's
`-->` test ends the block before the stamp. The same rider with a space
where the U+2028 is reads the same BROKEN at every version (executed). So
the break no longer changes the verdict, which is this item's whole claim.
The `-->` test's own crudeness is older than this item and outside its
class.

After the fix, `comment_blocks`' TEXT path (the `gfm_places` step-over and
round 2's `cut` set) has no caller in shipped code. No test passes it a
text either. Removing it is a simplification that moves G13's, P5-1's and
S3's `comment_blocks` anchors, so I left it out of the paste-ready fix.

## Paperwork

### ⬜ 2 — G13 says every rider the reader reads is one `region_lines` cuts

`seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:21` (G13),
the clause "so every rider the reader reads is one `region_lines` cuts before
the hash".

It is false at `c7fef45f` for 🟡 1's two shapes: the markdown rider's stamp
line and the `.py` second rider are read and not cut (executed). It becomes
true by construction with 🟡 1's fix, and G13 is then re-read against the
new `riders_in`. The phase 6 note on S2 in `seal/releases/0.9.1.md` says the
same thing ("no rider is read that `region_lines` does not cut"). It is a
dated reading, and the re-read after 🟡 1's fix is where it gets its next
note. This is a correction to the run's paperwork. It is not a fix.

## Round 2's verdicts, checked

| Round 2 | Is it closed? | Grounds |
|---|---|---|
| 🟡 1, a rider behind a comment on its GFM line goes unread | Yes, as to reading it | The three parameters fail at `7c339169` and pass at HEAD. No texts without the eight characters differ (executed). What the reader then runs on from that piece is this round's 🟡 1 |
| 🟡 2, `write_block` writes a CRLF file back as LF | Yes | Six byte shapes byte-exact. The write half is caught on a simulated CRLF platform (executed) |
| ⬜ 3, G15 and the fragment's CRLF sentences | Yes | True at HEAD by the same shapes. `evidence_check.py .` exits 0 (executed) |
| ❓, the CRLF-platform write and CI's Linux and Windows legs | Still out of verified scope | The simulation above is not a Windows run. The pull request's CI run answers it |

I carried round 2's coordinates (`comment_blocks`' `cut` set, `write_block`'s
two opens, G13 and G15) and re-opened each at `c7fef45f`. I carried none of
its conclusions.

## The account, checked

| The fix pass or the orchestrator claimed | What I found |
|---|---|
| `comment_blocks` steps over a mid-line marker piece only where `comment_blocks` over the GFM lines does not cut that line | True by reading at `:339`–`:348`. Recursion depth one |
| The docstring: where the GFM line opens a comment, `region_lines` cuts it whole, "so the reader reads every marker piece on it" | True for the marker piece. Not true for the block the reader runs on from it (🟡 1) |
| `write_block` opens with `newline=""` both ways, and CRLF and CR come back byte for byte | True for six shapes, mixed endings included |
| G15's note: the write reverted is equivalent on macOS, and only a CRLF platform sees it | True. Simulated, the CRLF parameter would fail there |
| The three shapes of the round 2 case fail at `7c339169`, and so do CRLF and CR | True: 5 failed |
| The orchestrator: `gather_changelog.py`'s default-mode read cannot change the output, and `.gitattributes` handles the CRLF write | True for both. See ask 2 |

## Regression tests to plant

One case, into `tests/test_every_reader_ends_a_line_where_gfm_does.py` below
round 2's cases. It is the second fence under *Paste-ready fixes*. It failed
for both shapes against `rider_check.py` at `c7fef45f` (executed) and passes
with the fix.

## Facts for the evidence ledger

- At `c7fef45f`, `rider_check.py#riders_in` runs a rider's block over
  `str.splitlines` pieces with `comment_blocks`' own `-->` and comment-kind
  tests, and `region_lines` runs them over GFM lines. A break inside a line
  the hasher cuts parts the two blocks. Executed through `check()` and
  `reverify()`.
- `gather_changelog.py` writes byte-identical output from LF, CRLF and
  lone-CR inputs. Under `* text=auto eol=lf`, a CRLF-platform write stages
  the same blob as an LF one. Executed, with the platform simulated.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A rider whose marker piece round 2's fix now reads, on a line the hasher cuts, runs on past that line by the reader's own `-->` and comment-kind tests, so its stamp is hashed into the region it names and `--reverify` never makes it read ok | `.github/scripts/rider_check.py:339` | deferred #682 | Markdown rider behind a closed comment and U+2028: at `7c339169` 0 read. At `c7fef45f` 1 drifted after every `--reverify`. Fuzz over 13,237 texts: a read rider's marker or stamp off the cut in 0 texts at `7c339169` and 4 at `c7fef45f`. Deriving `riders_in` from the hasher's blocks brings it to 0, changes no text without the eight characters, and passes 193 cases |
| ⬜ 2 | G13 says every rider the reader reads is one `region_lines` cuts before the hash, which 🟡 1's two shapes make false | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:21` | deferred #682 | Executed under 🟡 1. True by construction once 🟡 1's fix lands and G13 is re-read. A correction to the run's paperwork, not a fix |
| 🟢 | round 2's finding 1 is closed — a rider behind a comment on its GFM line, or behind a second rider on it, is read | `.github/scripts/rider_check.py:339` | confirmed | The three parameters fail at `7c339169` and pass at HEAD. Recursion depth one, no error over 13,237 texts. No text without the eight characters, none of the 576 prefixes and none of 25 tree files changes riders. What the reader runs on from the piece is this round's finding 1 |
| 🟢 | round 2's finding 2 is closed — `write_block` keeps CRLF and lone-CR files byte for byte | `.github/scripts/rider_check.py:604` | confirmed | Six shapes byte-exact, mixed endings included. The write reverted fails the CRLF shape on a simulated CRLF platform |
| 🟢 | round 2's finding 3 is closed — G15 and the fragment's CRLF sentences are true | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:23` | confirmed | True at HEAD by the six shapes. `evidence_check.py .` exits 0 |
| 🟢 | The fix pass's question: `gather_changelog.py` reading and writing in the default newline mode is outside this item's class | `.github/scripts/gather_changelog.py:413` | confirmed | LF, CRLF and lone-CR inputs give byte-identical output and identical `--check`, dry-run and refusal stdout. A simulated CRLF-platform write stages the LF blob under `* text=auto eol=lf` |
| 🟢 | The raw U+2028 and U+2029 in round 1's record are what spec S1 keeps, not ⬜ 5's defect, and no check reaches them | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-1.md:78` | confirmed | Inside a fenced string constant that lists them, copied from the report. Eight gates and six record-walking test modules give the same output raw and escaped |
| ❓ | `write_block`'s write and the new cases on CI's Linux and Windows legs | `.github/scripts/rider_check.py:604` | ❓ out of verified scope | Only macOS ran here, with the CRLF platform simulated. The pull request's CI run answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the item's module and `tests/test_a_rider_reaches_its_file.py`, in the clone at `c7fef45f` | 130 passed |
| Round 2's two new cases with `rider_check.py` at `7c339169` | 5 failed: the three shapes, CRLF and CR |
| Fuzz, 13,237 generated texts holding the marker, `.py`, `.yml` and `.md`, head against `7c339169` | no exception. A read rider's marker or stamp off the hasher's cut: 0 texts at `7c339169`, 4 at HEAD. Texts without the eight characters whose riders differ: 0 |
| 576-prefix differential, reader against hasher and head against `7c339169` | 0 read but not cut. 0 differ |
| Three controls, code or prose before the break | 0 riders at both, 0 cut |
| The 25 files under the rider roots that carry the marker | same riders at both. `check()`: 19 ok, 0 drifted, 0 problems |
| Markdown rider behind a closed comment and U+2028, `check` and `--reverify` twice | `7c339169`: 0 read. HEAD: 1 drifted after each `--reverify`. The control settles to 1 ok at both |
| The same shape with a second rider in the one comment | HEAD reads the second rider off the cut |
| `reverify` on six byte shapes | all byte-exact apart from the stamp. `check()` 1 ok after each |
| `write_block`'s write reverted to the default mode, on a simulated CRLF platform | CRLF and LF files no longer byte-exact. Lone CR still byte-exact |
| `gather_changelog.py` over the tree's changelog and 29 fragments, in LF, CRLF and lone CR | `--check`, `--dry-run` and the refusal: identical stdout. The written file: byte-identical |
| `gather_changelog.py` write on a simulated CRLF platform, staged in a scratch repository under `* text=auto eol=lf` | ` M` before staging, `git diff` empty, `git diff --cached` empty after, same blob as the LF write |
| Eight hygiene gates and six record-walking test modules, round 1's record and report raw and escaped | same exit codes and output. Only the printed commit abbreviation and the run time differ. The modules: 528 passed both times |
| 🟡 1's fix and case applied | 193 passed over the item's module, `test_a_rider_reaches_its_file.py` and `test_the_hooks_hide_what_a_renderer_hides.py`. The fuzz: 0 off the cut, 0 changed without the eight. 576 prefixes agree. 25 tree files unchanged. `rider_check.py --root .`: `19 ok · 0 drifted · 0 broken`, exit 0. `ruff check` and `ruff format --check` clean on both files |
| 🟡 1's case against `rider_check.py` at `c7fef45f` | 2 failed, both shapes |
| `evidence_check.py .` at `c7fef45f` | exit 0 |
| The broad gate: full suite, repository-wide lint, typecheck | not yet. That is the sealer's run, once the rounds settle |

## Paste-ready fixes

### 🟡 1 — `riders_in` reads the hasher's blocks

In `.github/scripts/rider_check.py`, replace `riders_in`:

```python
def riders_in(rel, text):
    """Every rider in TEXT, numbered on its `str.splitlines` lines.

    The blocks are the hasher's: `comment_blocks` over GFM lines, which is
    what `region_lines` cuts. Each block's pieces -- the `str.splitlines`
    lines that start inside it -- are split at every piece carrying the
    marker, so two riders on one GFM line are two riders, and a piece before
    the first marker (`# note`, a closed HTML comment) is in none. A second
    rule over the pieces is what let the reader and the hasher disagree in
    rounds 1, 2 and 3 of #664: on a line's head, on its cut, and then on a
    block's extent and its comment kind.
    """
    global _blocks
    if MARKER not in text:
        return []
    if _blocks is None:
        _blocks = load_blocks()
    pieces = text.splitlines()
    by_line = {}
    for k, (number, _head) in enumerate(gfm_places(_blocks.gfm_lines, text)):
        by_line.setdefault(number, []).append(k)
    out = []
    for a, b in comment_blocks(_blocks.gfm_lines(text), rel):
        inside = [k for number in range(a, b + 1) for k in by_line.get(number, [])]
        starts = [k for k in inside if MARKER in pieces[k]]
        for s, e in zip(starts, [*starts[1:], inside[-1] + 1], strict=True):
            out.append(Rider(rel, s + 1, e, text))
    return out
```

The case, below round 2's in `tests/test_every_reader_ends_a_line_where_gfm_does.py`:

```python
@pytest.mark.parametrize(
    "rel, text",
    [
        (
            "doc.md",
            f"x\n{RIDER_MARK[:5]}a -->{LS}{RIDER_MARK} about a.\n{STAMP} -->\ny\n",
        ),
        (
            "mod.py",
            f"a = 1\n# note{LS}{RIDER_MARK} about a.\n"
            f"b = 2  # {'RIDER:'} about b. {STAMP} -->\n",
        ),
    ],
    ids=["closed-comment-then-break", "hash-line-read-as-html"],
)
def test_every_piece_of_a_rider_read_is_on_a_line_the_hasher_cuts(rel, text):
    """Round 3. Reading a marker piece on a line the hasher cuts is half of
    agreeing with it: the block the reader runs on from that piece has to be
    the hasher's too, or its stamp is hashed into the region it names and no
    `--reverify` makes it read ok. The characters are built from their code
    points."""
    riders = _load("specseal_riders_extent", RIDERS)
    blocks = riders.load_blocks()
    places = riders.gfm_places(blocks.gfm_lines, text)
    cut = {
        n
        for a, b in riders.comment_blocks(blocks.gfm_lines(text), rel)
        for n in range(a, b + 1)
    }
    read = riders.riders_in(rel, text)
    assert read
    for rider in read:
        lines = {places[k][0] for k in range(rider.start - 1, rider.end)}
        assert lines <= cut, (rider.start, rider.end, sorted(lines), sorted(cut))
```

G13's clause stays as written once the fix lands, and becomes true by
construction. Its re-read note names this case.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a rider read on a line the hasher cuts runs on past it | #682, milestone `release: 0.16.0` | the work item #682 opens, in 0.16.0 |
| ⬜ 2 — G13 false for 🟡 1's two shapes | #682 | the same work item, re-reading G13 against its fix |

Needs a fix: yes — 🟡 1 (a rider read on a line the hasher cuts runs on past it by the reader's own tests, so its stamp is hashed and `--reverify` never settles it)
Loses a record or crashes: no

The broad gate is not due yet: this round leaves 🟡 1 open. The run is
capped after this round, so whether 🟡 1's fix lands before the sealer runs
is the orchestrator's call, under `docs/review-chain-spec.md` §*The cap
bounds rounds, and not the fixes of the round it stopped*. The finding sits
in code round 2's fix commit `ee6215be` changed. At `7c339169` the same
shapes were read by nobody.

## Proof block

Files opened this round, in the clone at `c7fef45f` unless named:

- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-2.md` and `round-2-report.md`, whole
- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-1.md`, lines 1–140, and `round-1-report.md`, ⬜ 5's section and verdict table
- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/spec.md`, lines 1–60 and its CRLF and write clauses
- the diff `81a770bb..c7fef45f` of `.github/scripts/rider_check.py`, `tests/test_every_reader_ends_a_line_where_gfm_does.py`, both ledger fragments it touches, `seal/releases/0.9.1.md`, the changelog fragment and `overview.md`
- `.github/scripts/rider_check.py`, lines 138–200 by grep, 230–640
- `.github/scripts/gather_changelog.py`, lines 90–200 and 236–420
- `tests/test_every_reader_ends_a_line_where_gfm_does.py`, lines 50–60 and 733–736; `tests/test_a_rider_reaches_its_file.py`, lines 425–450
- `.gitattributes`, `bin/test`, `bin/evidence-check`, the command lines of `.github/workflows/hygiene.yml`
- `rider_check.py` at `7c339169`, loaded whole for the comparisons
- commit `5edae0fe`
