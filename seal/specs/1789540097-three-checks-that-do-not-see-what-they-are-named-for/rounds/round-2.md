# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — review round 2

| Field | Value |
|---|---|
| Target SHA | 9087705b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 425 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 6, the whitespace flattening that no case exercises, which the module stays green without; finding 7, the sweep's own read and call, which the smith may instead answer with grounds |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round. Its target is the diff of round 1's fixes —
`15dcad12..9087705b` — and its job is the answers: are round 1's one 🔴 and
four 🟡 actually closed.

The two units that fix pass added are exempt from that rule and were read as a
finding surface, together with the constants and blocks it changed.

The 🔴 was pressed hardest, and one layer further out than it was found: the
repair makes a case call the sweep's own function over text the case writes,
and the tree still holds zero occurrences of the phrase. So the round was
asked whether anything now connects the guard to what the corpus actually
contains, because a case that plants and asserts is not a guard that fires on
a committed file.

It was also asked to judge the reasoning behind leaving `plan.md` and
`spec.md` standing — a fix pass rewriting the framer's documents would make
the frame say the work was framed as it was finally built — since that decides
what a record means rather than only what this branch does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — all five of round 1's mutations are red, each on the case that calls the same function the sweep calls | `tests/test_chain_hooks_hardening.py:856` | confirmed | Executed: five mutations of `batch_instructions`, constants untouched, each exit 1 · 1 failed, 50 passed, each failing `test_the_sweep_refuses_a_planted_instruction_in_every_spelling`; baseline restored to exit 0 · 51 passed after each |
| 🟡 6 | The whitespace flattening is the one piece of the composition no case exercises, and it is the piece only real files need | `tests/test_chain_hooks_hardening.py:876` | **fixed** `64f36eee` | fixed at 64f36eee — a hard-wrapped spelling joins the tuple the case already walks, which is the shape every file the sweep reads actually has. Re-measured after the fix pass stalled: dropping the flattening from `batch_instructions` is **1 failed, 50 passed** where round 2 measured exit 0, 51 passed; Executed: with `flat_body = EMPHASIS.sub("", body)` the module is exit 0 · 51 passed. Every case input is single-line; no case writes a newline at all. A phrase straddling a line break — the ordinary shape in files hard-wrapped like `agents/framer.md`, 249 non-blank lines — is found only by the flattening: refused with it, returns nothing without it. Fix measured: 52 passed at exit 0, and exit 1 on this case under the mutation |
| 🟡 7 | The sweep's own read and call are held by nothing, so the guard can be disconnected from the tree in silence | `tests/test_chain_hooks_hardening.py:1100-1104` | answered | `64f36eee` for the half that closes, and grounds for the half that does not. The sweep now reports what it read — the definition names and their sizes — and asserts both, so the read and the loop are held: truncating the read to ten bytes is **1 failed** and emptying the loop's iterable is **1 failed**, each where round 2 measured exit 0. What stays open is the **call**: `batch_instructions("")` passes something other than what was read, and observing that needs a walk driven by a planted definition file. That is mechanism a fix pass may not add, and `CONTRIBUTING.md` asks a separate argument for a change to what the suite guards. Recorded in `overview.md` §*Not verified* with an answerer; Executed, three mutations with the function and the constants untouched: the body replaced by `""`, the read truncated to ten bytes, and the loop's iterable replaced by `()` — each exit 0 · 51 passed. `agents/*.md` still holds zero batch phrases, measured at this SHA in all five definitions, so nothing in the corpus reaches the walk. The only guard over this half is `assert len(definitions) >= 3`. Fix measured: 52 passed at exit 0, and exit 1 under each of the three |
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_chain_hooks_hardening.py:1000-1013` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py:843`; compare `skills/code-review/scripts/chain_check.py:419` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py:866` | round 1's 🟡 3 — fixed |
| round-1 | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | round 1's 🟡 4 — fixed |
| round-1 | `plan.md:130`, `spec.md:126-128` | round 1's 🟡 5 — answered |
| round-1 | `questions.md:35`, `spec.md:148`, `tests/test_one_word_one_meaning.py:482`, `tests/test_one_word_one_meaning.py:193` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:242-266` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_one_word_one_meaning.py:253`, `:388`, `:459-503` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1789445605-…/rounds/round-2.md:39-40` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_docs_line_wrap.py:20-24`, `:59` | round 1's 🟢 — confirmed |
| round-1 | the whole tree at this SHA | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py` counts a coordinate matching neither `ANCHOR_RE` nor `OLD_COORD_RE` as nothing rather than refusing it | already deferred in round 1 to a new issue — it is the checker rather than this branch | the repository owner |
| Whether `agents/scribe.md` joins `SEAL_SWEPT` | already deferred in round 1; the fix pass wrote it into `overview.md` §*Not verified* beside the neighbouring question about `chain_check.py` | the repository owner |
