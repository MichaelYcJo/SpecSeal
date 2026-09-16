# Round 2 — the verifying round, on round 1's fix diff

Target: `git diff 15dcad12..HEAD`, four commits. HEAD is `9087705b` on
`test/413-418-422-three-checks-that-do-not-see-what-they-are-named-for`, the
working tree was clean at the start, and the SHA did not move during the
round. Pull request #425, draft.

Everything below was read or run in a `git clone --no-local` of the repository
checked out at that SHA. The only file written outside it is this report.

## The relationship between the findings

Round 1's five verdicts all close. The two new findings are the same class as
round 1's 🔴, one and two layers further out.

```
  🔴 1  the composition was unreachable      CLOSES  all five mutations red,
        on anything committed                       each on the new case
          ↓ and the same shape one piece over
  🟡 6  the whitespace flattening is the one part of that composition
        no case exercises. Drop it and the module is exit 0, 51 passed,
        while the guard stops seeing any instruction whose phrase
        straddles a line break — the normal shape of the files it reads
          ↓ and once more, one layer out
  🟡 7  the sweep's own read and call are held by nothing. Feed the
        function `""`, or the first ten bytes of each file, or cut the
        loop: exit 0, 51 passed, three times

  🟡 2  the marker set                        CLOSES  both halves red
  🟡 3  the agent nouns recorded as residue   CLOSES  comment true
  🟡 4  the ledger row's anchor               CLOSES  all three corruptions
                                                      reported, exit 2/2/1
  🟡 5  the framer documents left standing    SOUND   with two corrections
```

## 🔴 1 closes — I re-ran all five mutations and each is red on the new case

The five mutations round 1 ran against the inline sweep were re-run against
`batch_instructions`, leaving the module-level constants untouched so the two
pattern cases stay green. Each one is exit 1, and each fails on
`test_the_sweep_refuses_a_planted_instruction_in_every_spelling` — the case
that calls the same function the sweep calls.

| Mutation, inside `batch_instructions` only | Before (round 1) | Now |
|---|---|---|
| emphasis strip dropped | exit 0 · 50 passed | exit 1 · 1 failed, 50 passed |
| finder back to the literal `in one batch` | exit 0 · 50 passed | exit 1 · 1 failed, 50 passed |
| stems front-anchored only | exit 0 · 50 passed | exit 1 · 1 failed, 50 passed |
| window widened to 400 | exit 0 · 50 passed | exit 1 · 1 failed, 50 passed |
| window narrowed to 5 | exit 0 · 50 passed | exit 1 · 1 failed, 50 passed |

The baseline restored to exit 0, 51 passed, after each.

## 🟡 6 — the one piece of the composition no case exercises is the one that only real files need

`tests/test_chain_hooks_hardening.py:876`

`batch_instructions` flattens whitespace before it searches:

```python
    flat_body = EMPHASIS.sub("", " ".join(body.split()))
```

Every string the new case hands that function is a single line. So the
flattening is the one part of the composition nothing exercises, and it is the
part that exists solely for the corpus the sweep reads.

**Measured.** With the flattening dropped and the emphasis strip kept —
`flat_body = EMPHASIS.sub("", body)` — the module is exit 0, 51 passed.

**Why it matters.** Every file the sweep reads is hard-wrapped prose;
`agents/framer.md` is 249 non-blank lines. An instruction whose phrase
straddles a line break is the ordinary case, not the exotic one. Run through
the function as it stands, this text is refused and names `answer`, `person`
and `questions`:

```
Questions a person genuinely has to answer go in one
batch before the first edit.
```

Run through it without the flattening, the same text returns nothing. The
guard would go silent on the commonest spelling a real definition can carry,
and the module would stay green.

The fix is one more spelling in the tuple the case already walks. I applied it
and measured: 52 passed at exit 0 with the fix in, exit 1 on this case with the
flattening dropped.

## 🟡 7 — nothing connects the guard to what the tree contains, which is the layer the round was told to reach for

`tests/test_chain_hooks_hardening.py:1100-1104`

Round 1's 🔴 was that the composition was unreachable on anything committed.
Extracting `batch_instructions` fixed that. What the extraction did not reach
is the other half of the sweep — the walk that opens each file and hands its
body to the function. Nothing runs that half, because `agents/*.md` still
holds zero batch phrases (measured again at this SHA: 0 in all five
definitions).

**Measured, three mutations of the sweep with the constants and the function
untouched:**

| Mutation | Result |
|---|---|
| `batch_instructions(body)` → `batch_instructions("")` | exit 0 · 51 passed |
| `body = f.read()` → `body = f.read()[:10]` | exit 0 · 51 passed |
| the loop's iterable replaced by `()` | exit 0 · 51 passed |

The one guard over this half is `assert len(definitions) >= 3`, which pins the
glob and nothing after it.

**Why it matters.** This is the work item's own subject at the next layer: a
check that passes while blind to what it is named for. A later session that
touches those four lines gets no signal, and the guard this whole branch exists
to repair goes quiet without a word.

**What can be answered instead.** Holding this half means running the walk
over a file a case writes, which is a temporary directory and a planted
definition — mechanism `CONTRIBUTING.md` asks a separate argument for, and the
smith may answer with that argument rather than the fix. The paste-ready fix
below is what I measured: green at 52 passed with it in, and red on the new
case under each of the three mutations above.

## 🟡 2 closes — the three spellings are reachable and both halves are pinned

`tests/test_chain_hooks_hardening.py:839`, `:843`

`EMPHASIS` is `[*_`]+` and `BATCH_PHRASE` carries `into`. Both halves are
pinned in the pattern case and in the composition case, so undoing either is
two failures rather than none.

| Mutation | Result |
|---|---|
| `EMPHASIS` back to `\*+` | exit 1 · 2 failed — the pattern case and the composition case |
| `into` removed from `BATCH_PHRASE` | exit 1 · 2 failed — the same two |

The comment's factual claims hold. `skills/code-review/scripts/chain_check.py`
carries a normaliser of the same name over the same three markers, and no stem
in `ASKING` and no word in `BATCH_PHRASE` carries an underscore, so stripping
`_` cannot change what is found.

One asymmetry, not a defect: the pattern case carries all three new spellings
and the composition case carries two of them — `_one batch_` is only in the
pattern case. Both halves are covered between them.

## 🟡 3 closes — the comment is true and nothing asserts the loss as right

`tests/test_chain_hooks_hardening.py:949-962`

`asker`, `answerer` and `questioner` sit in their own block now, under a
comment that calls them residue rather than correctness. The correctness block
above kept `humans` in place of `asker`, which is a population and belongs
there.

The comment's load-bearing claim checks out: `skills/agent-contract/SKILL.md`
§4 writes *answerer* for the party that answers an unverified item, at line
122. The stems themselves are unchanged — `ASKING` back to front-anchored-only
is exit 1 on both this case and the composition case.

One overstatement, which changes nothing the code does: the comment says *This
block used to sit in the one above*, and only `asker` did. `answerer` and
`questioner` are new words this fix added.

## 🟡 4 closes — all three corruptions are reported where all three were silent

`seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6`

Re-run at this SHA, each corruption applied on its own:

| Corruption | Result |
|---|---|
| the documented 109 → 999 | exit 2 · 1 drifted · 1 broken |
| the documented 90 → 999 | exit 2 · 1 drifted · 1 broken |
| the restated 109 inside `COVERED`'s comment → 999 | exit 1 · 2 drifted |

Each number is held by the line that states it: corrupting one takes that
line's own quoted-line anchor BROKEN and drifts the other, because both
anchors hash the same file.

`bin/evidence-check .` is exit 0 at HEAD, 1326 ok, 0 drifted, 0 broken.

One correction to the record's wording: round 1's Grounds cell says *`109→999`
is exit 2 BROKEN, `90→999` is exit 2 DRIFTED*. Each of them is one BROKEN and
one DRIFTED together. The substance — exit 2 where all three were silent —
holds.

## 🟡 5 — the reasoning is sound, and its application left two gaps

The question is whether a fix pass may rewrite `plan.md` and `spec.md` to
correct a reason the review disproved.

**The reasoning holds, and I would apply it the same way.** Those two files
are what the routing gate approved before anything was built. A fix pass that
edits them makes the record say the work was framed as it was finally built,
which is the one thing the frame exists not to say. The distinction the
repository already draws is the right one: a record asserts a past state, so
it can stand beside a contract it contradicts, provided the correction is
findable. `questions.md` was corrected in place and that is consistent — the
edit is confined to the Status cell, which the phases write, not the framer.

Two things the application left open.

- **`spec.md` has no row at all.** The record says *`plan.md` and `spec.md` are
  left standing on purpose … That is a `survivors.md` row with the standing
  text quoted*. There is one row and it quotes `plan.md`. The `spec.md` §*Out*
  bullet that carries the disproved reason is quoted nowhere.
- **The `plan.md` row surfaces to nobody.** Run at this SHA,
  `bin/survivor-check --range 27a2d403..HEAD` reports exactly one place,
  `phases/phase-3.md:36`. The rows for `plan.md` and `overview.md` exempt
  nothing the checker reports, so a reader who opens `plan.md` alone meets the
  disproved reason and nothing in that file points onward.

## The two things the pass reported, checked rather than trusted

**The `survivor-check` correction is true, and the paragraph still reads as
what it was.** The phase-3 paragraph the checker flagged is untouched, and the
correction is a new paragraph after it, opening *And it was still held by
nothing — corrected after round 1's 🔴 1, at the fix pass*. Its claims are the
ones I measured above. The reasoning that produced the defect is intact, which
is what a phase record is for.

**The reworded ledger note carries no `path:line` coordinate.** The Notes cell
names `ANCHOR_RE`, `OLD_COORD_RE` and the shape `#<module>@00000000` in prose,
which the checker does not read as a coordinate. `bin/evidence-check .` is
exit 0 over the whole tree.

## Corrections — measured, and none of them changes what the branch does

- **`phases/phase-3.md:31` still says *four definitions*.** Round 1 reported
  that count wrong at `questions.md:35`; the fix pass corrected that copy and
  left this one. It is stated as a measurement — *measured over the glob, four
  definitions* — and there were five when it was taken. `agent-contract` §12:
  the fix is owed to every instance.
- **`phases/phase-6.md:73` opens *the reason above is not the one that
  holds*.** The reason it corrects was deleted from that file rather than left
  above the correction; what stands above is the `bin/evidence-check`
  paragraph. The old reason is quoted two lines further down, so nothing is
  lost, but the pointer points at the wrong paragraph.
- **`survivors.md`'s preamble overstates two of its three rows.** It says *all
  three now carry the correction beside the standing text rather than instead
  of it*. That is true of `phase-3.md`. The `plan.md` correction lives in two
  other files, and the `overview.md` row argues no correction is owed at all.
- **Round 1's Grounds for 🟡 4 splits BROKEN and DRIFTED between the two
  corruptions.** Each produces both. Measured above.

## What I confirmed and did not re-derive

The folded-member comparison is a set now, which is right for the claim: the
closure argument is about which members the fold reaches, and removing a member
from the expectation is exit 1 on that case. A duplicated entry would be
silent, which changes nothing the claim rests on.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | 🔴 1 is closed — all five of round 1's mutations are red, each on the case that calls the same function the sweep calls | `tests/test_chain_hooks_hardening.py:856` | confirmed | Executed: five mutations of `batch_instructions`, constants untouched, each exit 1 · 1 failed, 50 passed, each failing `test_the_sweep_refuses_a_planted_instruction_in_every_spelling`; baseline restored to exit 0 · 51 passed after each |
| 🟡 6 | The whitespace flattening is the one piece of the composition no case exercises, and it is the piece only real files need | `tests/test_chain_hooks_hardening.py:876` | open | Executed: with `flat_body = EMPHASIS.sub("", body)` the module is exit 0 · 51 passed. Every case input is single-line; no case writes a newline at all. A phrase straddling a line break — the ordinary shape in files hard-wrapped like `agents/framer.md`, 249 non-blank lines — is found only by the flattening: refused with it, returns nothing without it. Fix measured: 52 passed at exit 0, and exit 1 on this case under the mutation |
| 🟡 7 | The sweep's own read and call are held by nothing, so the guard can be disconnected from the tree in silence | `tests/test_chain_hooks_hardening.py:1100-1104` | open | Executed, three mutations with the function and the constants untouched: the body replaced by `""`, the read truncated to ten bytes, and the loop's iterable replaced by `()` — each exit 0 · 51 passed. `agents/*.md` still holds zero batch phrases, measured at this SHA in all five definitions, so nothing in the corpus reaches the walk. The only guard over this half is `assert len(definitions) >= 3`. Fix measured: 52 passed at exit 0, and exit 1 under each of the three |
| 🟢 | 🟡 2 is closed — the three newly reachable spellings are reachable and both halves are pinned in two cases | `tests/test_chain_hooks_hardening.py:839`, `:843` | confirmed | Executed: `EMPHASIS` back to `\*+` is exit 1 · 2 failed; `into` removed from `BATCH_PHRASE` is exit 1 · 2 failed, both on the pattern case and the composition case. Read: `chain_check.py` carries a normaliser of the same name over the same three markers, and no stem in `ASKING` and no word in `BATCH_PHRASE` carries an underscore |
| 🟢 | 🟡 3 is closed — the comment is true and the correctness block no longer asserts the loss as right | `tests/test_chain_hooks_hardening.py:949-962` | confirmed | Read: `skills/agent-contract/SKILL.md:122` is in §4 and writes `answerer` for the party that answers an unverified item, which is the comment's load-bearing claim. `humans` replaced `asker` in the correctness block and is a population, which belongs there. Executed: `ASKING` back to front-anchored-only is exit 1 on this case and on the composition case, so the stems are unchanged and pinned |
| 🟢 | 🟡 4 is closed — all three corruptions are reported where all three were silent | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | confirmed | Executed at this SHA, each corruption alone: 109→999 exit 2 · 1 drifted 1 broken; 90→999 exit 2 · 1 drifted 1 broken; the restatement inside `COVERED`'s comment exit 1 · 2 drifted. `bin/evidence-check .` exit 0 · 1326 ok · 0 drifted · 0 broken at HEAD |
| 🟢 | 🟡 5's reasoning holds — the framer's approved documents are not a fix pass's to rewrite | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/survivors.md` | confirmed | Read: `spec.md` and `plan.md` are what the gate approved, and editing them makes the frame say the work was framed as it was built. The `questions.md` edit is consistent — it is confined to the Status cell, which the phases write. The two gaps in the application are corrections below, not grounds against the reasoning |
| 🟢 | The `survivor-check` correction is true, and the phase-3 paragraph still reads as what it was | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/phases/phase-3.md:36-55` | confirmed | Read: the flagged paragraph is byte-identical and the correction is a new paragraph after it. Executed: `bin/survivor-check --range 27a2d403..HEAD --exempt <survivors.md>` exit 0, the one survivor excused |
| 🟢 | The reworded ledger note carries no `path:line` coordinate | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | confirmed | Read: `ANCHOR_RE`, `OLD_COORD_RE` and `#<module>@00000000` are named in prose, none of which the checker reads as a coordinate. Executed: exit 0 over the whole tree |
| 🟢 | The folded-member comparison over a set is right for the claim it holds | `tests/test_one_word_one_meaning.py:482` | confirmed | Executed: removing a member from the expectation is exit 1 on that case. Read: the closure argument is about which members the fold reaches, so a duplicated entry going silent costs the claim nothing |
| ⬜ | Four corrections that commission nothing: `phase-3.md`'s uncorrected *four definitions*, `phase-6.md`'s dangling *the reason above*, `survivors.md`'s preamble overstating two of its three rows, and round 1's Grounds splitting BROKEN and DRIFTED between the two ledger corruptions | `phases/phase-3.md:31`, `phases/phase-6.md:73`, `survivors.md:9-11`, `rounds/round-1.md` 🟡 4 | correction | See §*Corrections*. Each is measured; none changes what the branch does |
| ⬜ | The `plan.md` and `overview.md` rows of `survivors.md` exempt nothing the checker reports, and `spec.md` has no row at all although the record says it is covered by one | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/survivors.md` | correction | Executed: `bin/survivor-check --range 27a2d403..HEAD` with no exempt file reports exactly one place, `phases/phase-3.md:36`, exit 1. Read: one row quotes `plan.md`; no row quotes `spec.md` |
| ❓ | The full suite, the repository-wide lint and the typecheck | the whole tree at this SHA | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer and `agents/warden.md` hands me none of the three. Not yet run. Answered by the sealer, spawned by the orchestrator after the rounds settle |

## Paste-ready fixes

Finding 6 — one more spelling in the tuple
`test_the_sweep_refuses_a_planted_instruction_in_every_spelling` already
walks, after the backtick spelling:

```python
        "collect in `one batch` what a person answers",
        # Hard-wrapped prose, which is the shape of every file the sweep
        # reads: the phrase itself straddles a line break, and the whitespace
        # flattening in `batch_instructions` is the only thing that finds it.
        # Round 2's 🟡 6 — no case wrote a newline at all, so dropping the
        # flattening left the module at exit 0, 51 passed while the guard went
        # silent on the commonest spelling a real definition can carry.
        "questions a person genuinely has to answer go in one\nbatch "
        "before the first edit",
```

Finding 7 — the corpus half extracted the way the composition half was, with
a case that runs it over a definition the case writes. The function and the
case go above
`test_the_sweep_refuses_a_planted_instruction_in_every_spelling`:

```python
def definitions_with_batch_instructions(paths, root):
    """`batch_instructions` over real files, as `(relative, phrase, window,
    names)`.

    The sweep IS this function over `agents/*.md`, and the case below is this
    function over a file the case writes. Round 2's 🟡 7: extracting
    `batch_instructions` held the composition and left this half unheld —
    nothing in `agents/*.md` contains a batch phrase, so the walk could be made
    to read `""`, to read the first ten bytes of each file, or to iterate
    nothing at all, and the module stayed at exit 0, 51 passed, all three
    times. The one guard over it was `assert len(definitions) >= 3`, which
    pins the glob and nothing after it.
    """
    for path in paths:
        with open(path, encoding="utf-8") as f:
            body = f.read()
        relative = os.path.relpath(path, root)
        for phrase, window, named in batch_instructions(body):
            yield relative, phrase, window, named


def test_the_sweep_reads_the_files_it_is_given(tmp_path):
    """The corpus half, on a definition this case writes, because `agents/*.md`
    holds nothing for the walk to find.

    Red with the body replaced by `""`, red with the read truncated, and red
    with the loop cut — each of which left the module green while the walk sat
    inside the sweep case.
    """
    planted = tmp_path / "planted.md"
    planted.write_text(
        "# A definition\n\n"
        + "filler line\n" * 40
        + "\nCollect in one batch everything a person has to\n"
        "answer, before the first edit.\n",
        encoding="utf-8",
    )
    found = list(definitions_with_batch_instructions([str(planted)], str(tmp_path)))
    assert found, (
        "the sweep does not read the file it is given, so a definition "
        "carrying a batching instruction reaches no window that refuses it"
    )
    relative, phrase, _window, named = found[0]
    assert (relative, phrase, named) == (
        "planted.md",
        "in one batch",
        ["answer", "person"],
    ), (
        f"the sweep reports {(relative, phrase, named)}, so what it hands the "
        "refusal no longer names the file, the spelling and the words found"
    )
```

And the sweep's own loop calls it, replacing the four lines that open each
file inline:

```python
    for relative, phrase, window, named in definitions_with_batch_instructions(
        definitions, ROOT
    ):
        raise AssertionError(
            f"{relative} tells an agent to collect {phrase} something a "
            f"person answers — the window names {named}. No agent this "
            "plugin spawns has `AskUserQuestion`, so collecting a batch "
            "of questions is an instruction nothing can carry out; the "
            "act belongs to the session that spawns the work. Batching "
            "READS is a different thing and is what `agent-contract` §10 "
            f"asks for — that wording is not refused here.\n  …{window}…"
        )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -q` at the target SHA | exit 0 · 51 passed |
| `bin/test tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py -q` | exit 0 · 43 passed |
| `bin/evidence-check .` | exit 0 · 1326 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `bin/survivor-check --range 27a2d403..HEAD --exempt <the work item's survivors.md>` | exit 0 · 1 survivor, excused by a row |
| `bin/survivor-check --range 27a2d403..HEAD` with no exempt file | exit 1 · exactly one place, `phases/phase-3.md:36` |
| 🔴 1 mutation A — the emphasis strip dropped from `batch_instructions` | exit 1 · 1 failed, 50 passed — the composition case |
| 🔴 1 mutation B — the finder back to the literal inside `batch_instructions` | exit 1 · 1 failed, 50 passed — the composition case |
| 🔴 1 mutation C — the stems front-anchored only inside `batch_instructions` | exit 1 · 1 failed, 50 passed — the composition case |
| 🔴 1 mutation D — the window widened to 400 inside `batch_instructions` | exit 1 · 1 failed, 50 passed — the composition case |
| 🔴 1 mutation E — the window narrowed to 5 inside `batch_instructions` | exit 1 · 1 failed, 50 passed — the composition case |
| 🟡 6 mutation — the whitespace flattening dropped, the emphasis strip kept | exit 0 · 51 passed |
| 🟡 7 mutation — the sweep calls the function on `""` instead of the file body | exit 0 · 51 passed |
| 🟡 7 mutation — the sweep reads only the first ten bytes of each definition | exit 0 · 51 passed |
| 🟡 7 mutation — the sweep's loop iterable replaced by `()` | exit 0 · 51 passed |
| Corpus measurement — batch-phrase occurrences across `agents/*.md` at this SHA | 0 in all five definitions |
| A batch phrase straddling a line break, through the function as it stands | refused, window names `answer`, `person`, `questions` |
| The same text with the flattening dropped | nothing found |
| Both paste-ready fixes applied together | exit 0 · 52 passed |
| The fixes, under the 🟡 6 mutation | exit 1 · 1 failed, 51 passed — the composition case |
| The fixes, under each of the three 🟡 7 mutations | exit 1 · 1 failed, 51 passed each — the new corpus case |
| 🟡 2 mutation — `EMPHASIS` back to `\*+` | exit 1 · 2 failed, 49 passed — the pattern case and the composition case |
| 🟡 2 mutation — `into` removed from `BATCH_PHRASE` | exit 1 · 2 failed, 49 passed — the same two |
| 🟡 3 mutation — `ASKING` back to front-anchored only | exit 1 · 2 failed, 49 passed — the stem case and the composition case |
| 🟡 4 — the documented 109 corrupted to 999 | exit 2 · 1 drifted · 1 broken |
| 🟡 4 — the documented 90 corrupted to 999 | exit 2 · 1 drifted · 1 broken |
| 🟡 4 — the restated 109 in `COVERED`'s comment corrupted to 999 | exit 1 · 2 drifted |
| Folded-member set — a member removed from the expectation | exit 1 · 1 failed, 17 passed |
| The full suite, the repository-wide lint, the typecheck | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py` counts a coordinate matching neither `ANCHOR_RE` nor `OLD_COORD_RE` as nothing rather than refusing it | already deferred in round 1 to a new issue — it is the checker rather than this branch | the repository owner |
| Whether `agents/scribe.md` joins `SEAL_SWEPT` | already deferred in round 1; the fix pass wrote it into `overview.md` §*Not verified* beside the neighbouring question about `chain_check.py` | the repository owner |

Needs a fix: yes — finding 6, the whitespace flattening that no case exercises, which the module stays green without; finding 7, the sweep's own read and call, which the smith may instead answer with grounds
Loses a record or crashes: no


## Proof block

Opened in the clone at `9087705b`: `tests/test_chain_hooks_hardening.py`,
`tests/test_one_word_one_meaning.py`, `tests/test_docs_line_wrap.py`,
`bin/test`, `skills/agent-contract/SKILL.md`,
`skills/evidence-check/scripts/evidence_check.py`, `agents/*.md`, and the work item's
`overview.md`, `spec.md`, `plan.md`, `questions.md`, `survivors.md`,
`changelog.md`, `phases/phase-3.md`, `phases/phase-6.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-1-fixes.md`,
`seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md`.
