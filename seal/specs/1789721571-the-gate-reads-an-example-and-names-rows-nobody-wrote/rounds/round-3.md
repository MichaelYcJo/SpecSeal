# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — review round 3

| Field | Value |
|---|---|
| Target SHA | 631df127e44e4d4a337898a88f360e77b1e7bca4 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 445 |
| Broad gate | 28fcb28b against origin/main |
| Fixes checked by | no fixes to check |
| Fix range | `95de3cdc7e6ceb81c2681dfbadd7f4ebdddbe470..c06997f1723df1376fff043f412bd133d6e17045`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, `fence_left_open`'s default answering about the file when the question is about a row. |
| Loses a record or crashes | no — nothing I found leaves the root and nothing raises. |

- [x] Pass

## What this round was asked

The last round of the run, and the round was told so. Round 1 met the floor, round 2 was the verifying round and reopened the run, and that is the one reopening this chain allows — so anything this round opens becomes an issue rather than a fix, and the pull request is labelled `chain: capped`. The round was asked to report at the severity it found, not to soften a finding because of where it lands and not to manufacture one because it is the last look: what changes is the destination, not the bar.

It was pointed first at the row that was not `none` for the first time in this run. `close` derived `Contract changes` from the fix range — `fenced_row` changed and reaches two records and pytest, and **`fence_left_open` changed and reaches `missing_row`** — and a contract change whose reach is never revisited is the largest regression class this repository has measured, four findings of ten in issue #57. The `New units` depth claim was handed over to be checked rather than read, because `close` refuses depth 2 before writing any cell, so a miscounted entry is a cell written on a wrong reading.

The fix pass named two things it had judged rather than measured, and both went to the round by name: whether `write_row`'s non-fence arm is reachable and whether its message is honest for whatever reaches it, and whether `fence_left_open`'s remaining default is safe with nothing in the tree exercising it. It was also asked to judge the four new survivor exemptions — an exemption's quote is its anchor, and a row excusing a sentence that is not the same claim is how a survivor goes quiet for the wrong reason — and to verify that the sweep for other identity comparisons over interned strings held.

The orchestrator had executed two things and said so: that round 2's red finding is closed in both directions, verified with `cat -A` over a file whose last line has no ending and no fence, and that `survivor-check` over the fix range exits 0 with two survivors excused. Judging the cases' shape, the new wording and the exemptions was left undone and named as left undone.

The broad gate was out of the round's hands (`agent-contract` §2) and the sealer's spawn is what follows this record. The round wrote no record and no `plan.md` row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `fence_left_open`'s `above=None` default answers the whole-file question round 2's 🟡 2 removed from the refusal — no caller, no case, and a `None` reaching it returns the old answer instead of raising | `skills/verify/scripts/broad_gate.py#fence_left_open` | deferred #446 | Executed: over the fixture round 2 named, `fence_left_open(home)` is `True` and `fence_left_open(home, at)` is `False`. No test in the tree calls the unit at all; its behaviour is pinned only through a substring of `missing_row`'s message. The chain is capped, so this goes to an issue rather than to a fix pass · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| ⬜ | `mine is stopper` is the one identity comparison over `refused` line text the sweep left, and its stated grounds are not the reason it works | `skills/verify/scripts/broad_gate.py#missing_row` | deferred #447 | Executed: over two identical `Broad gate` refused lines `mine == stopper` is `True` and `mine is stopper` is `False`, and the right arm is taken. It is sound because CPython's shared-object cache is one character wide and `names_this_row` guarantees a longer string — a premise nothing states and nothing pins · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| ⬜ | `fenced_row` has no production caller left; one assertion is its whole reach | `skills/verify/scripts/broad_gate.py#fenced_row` | **answered** | Read: `missing_row` calls `fenced_row_at` now, and the only reader is `tests/test_the_seal_is_taken_once_by_the_sealer.py:1887`. Keeping it is grounded — three docstrings, `hooks/config.py:343` and ledger R7 name it — so this is named rather than commissioned |
| ⬜ | `New units` declares `fenced_row_at` and `test_a_fence_opened_below_the_row_is_not_the_fence_above_it` at depth 1; both are at depth 2 | `seal/specs/1789721571-…/rounds/round-2.md` | **correction** | Executed: both were added by `15d4f38`, the fix of finding 2, whose `Location` names `fence_left_open`, which round-1.md's `New units` names. `close` reproduced in a clone prints the same value; `units_named_earlier` returns `fenceleftopen`, the RIDERed emphasis-stripping defect, so `depth_two` reaches no snake_case parent. No consequence for the code — this round read both units |
| ⬜ | Two of the six survivor exemptions excused nothing in this range and stand ready to silence a later one | `seal/specs/1789721571-…/survivors.md` | **correction** | Executed: `survivor-check` exits 0 and names two excused survivors, the case module and `broad_gate.py`. `exempted` matches on path plus a word run with no tie to a range, so the `plan.md` and `hooks/config.py` rows apply to any future range carrying that wording |
| ⬜ | The changelog fragment does not carry the sentence round 2's 🟡 4 added | `seal/specs/1789721571-…/changelog.md` | **correction** | Read: the #430 bullet covers *moves the stopping place down* and not *the rows under THAT line, which arrive today, go with the repair*, which is a different and worse cost |
| 🟢 | Round 2's finding 1 is closed, both acts of it | `skills/implement/scripts/seal.py#with_row`, `#write_row` | **confirmed** | Executed: both touched modules are green in a clean clone at the target SHA, `164 passed, 3 skipped`. Read: `end == len(lines)` is the only state where the insertion point follows a line with no ending, since `splitlines(keepends=True)` terminates every line but the last |
| 🟢 | Round 2's finding 2 is closed, and the fence arithmetic is right at every arrangement | `skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row` | **confirmed** | Executed: `fence_left_open(home, at)` is `False` for a row in a block that closes with an unclosed block below, `True` for a row inside an unclosed block. An unclosed opener above a closed block is unreachable — `fence_map` lets it swallow everything under it |
| 🟢 | Round 2's finding 3 is closed, and the tail is found by position on grounds that hold | `skills/verify/scripts/broad_gate.py#missing_row` | **confirmed** | Read: `refusal` appends `(line, stopper is None)` and never resets `stopper`, so `got` is monotone and `max(position … if got)` is the stopper's own entry. Executed through the two-bare-pipe file, where the clause about further lines now prints |
| 🟢 | Round 2's finding 4 is closed, and the new clause is true exactly where it prints | `skills/verify/scripts/broad_gate.py#missing_row` | **confirmed** | Executed over seven config shapes covering all five arms. In the `stopper is None` arm every refused line precedes every parsed row, so `after_mine` non-empty means every row arriving today sits under the next refused line — which is what the sentence says. It correctly stays silent in the arm where the repair costs nothing |
| 🟢 | `write_row`'s non-fence arm is reachable only through a defective `with_row`, and its message is honest for that state | `skills/implement/scripts/seal.py#write_row` | **confirmed** | Read: the three `with_row` arms and both call sites enumerated — the value is `local` or `shared`, the insert arm now terminates, and the append arm lands outside every closed fence. Executed: the case drives the arm by replacing `with_row`, and the refusal names no fence |
| 🟢 | The four new survivor exemptions' grounds are sound | `seal/specs/1789721571-…/survivors.md` | **confirmed** | Read: the rewritten paragraph was moved rather than withdrawn, and what it claimed is still what the four arms do. The case's sentence is a historical measurement, `plan.md`'s row is a contracted past state, and `hooks/config.py`'s is `refusal`'s own untouched contract |
| 🟢 | Leaving `spec.md` unedited is grounded, and both `overview.md` sections now hold the right things | `seal/specs/1789721571-…/spec.md` §*Data & interfaces*, `…/overview.md` | **confirmed** | Read: §*Data & interfaces* carries its own escape hatch in the paragraph that states the contract, the divergence row quotes both sides, and §*Fed back into the spec* now holds only clauses this work added |
| 🟢 | R7's narrowing, R8, R9 and R10 state what the code does, and every anchor resolves | `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md` | **confirmed** | Executed: `evidence-check` exit 0 — 11 ok, 0 drifted, 0 broken in the fragment; 1364 ok across the tree. Read: R10 anchors the *above it* decision on the unit that makes it, so R7's narrowed claim is covered twice |
| ❓ | The full suite, the repository-wide lint and the typecheck | `tests/`, the repository's `Broad gate` row | **out of verified scope** | `agent-contract` §2 and this round's prompt both place the broad gate with the sealer, after the rounds settle. Two modules were run narrow, `evidence-check` and `survivor-check` were run whole, and nothing broad was run |

## Paste-ready fixes

```python
def fence_left_open(home, above):
    """Whether a fenced code block ABOVE the line at index ABOVE is never
    closed.

    Read off the one fence rule, not a second one. It is the difference
    between a row somebody pasted into an example block and a row that is in
    the live table with a fence swallowing it: the first has to move and the
    second must not, and telling the second person to move a row that is
    already where it belongs is an instruction that changes nothing (#429).

    `hooks/config.py#fence_map` already computes this while it walks; this
    reads the value rather than walking again.

    False for every way of not having an answer: no file, a file that will not
    read, a file with no fence in it at all.

    **Above, because that is what the sentence says.** A file whose row sits
    in an example block that closes and which opens a second block further
    down answered True for the whole file, and the person was told to close a
    fence that has nothing to do with their row while the act they needed --
    move it -- was the sentence they did not get (#429, round 2).

    **ABOVE has no default, and that is the guard rather than an omission.**
    The whole-file answer is the one this refusal must never use, so the
    shorter spelling must not reach it: a caller with no index in hand is a
    caller that has not decided which row it is speaking about, and a `None`
    arriving from one has to stop at the call rather than return the answer
    the line above was written to remove.
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return False
    opened_at = config.fence_map(text.splitlines())[1]
    return opened_at is not None and opened_at < above
```
```python
def test_the_fence_question_is_asked_about_the_row_and_not_the_file(tmp_path):
    """The unit itself, which until now was pinned only through a substring of
    `missing_row`'s message.

    The file has two blocks: the one holding the row closes, and the one below
    it never does. *Is any fence in this file left open* is True for it and
    *is a fence above this row left open* is False, and only the second is a
    question this refusal may ask. Asking the first is what told the person to
    close a fence that has nothing to do with their row (#429, round 2).
    """
    module = gate_module()
    home = tmp_path / "asked_about_the_row" / "seal"
    home.mkdir(parents=True)
    (home / "config.md").write_text(
        "# Repository config\n\nAn example of the format:\n\n"
        "```markdown\n| Item | Value |\n|---|---|\n"
        f"| {ROW} | EXAMPLE |\n```\n"
        "\nAnd a block somebody opened and never closed:\n\n"
        "```markdown\n| Item | Value |\n",
        encoding="utf-8",
    )
    at, line = module.fenced_row_at(str(home))
    assert at is not None and line is not None, (at, line)
    assert module.fence_left_open(str(home), at) is False, (
        "the row is inside a block that closes; the block opened below it is "
        "not a fence above the row"
    )
    with pytest.raises(TypeError):
        module.fence_left_open(str(home))
```
```python
    mine, reached, after_mine, after_stopper = None, False, [], []
    mine_at, stopper_at = None, None
    for position, (line, got) in enumerate(refused):
        if names_this_row(line):
            mine, reached, mine_at = line, got, position
            after_mine = [text for text, _got in refused[position + 1 :]]
            break
    if stopper is not None:
        # **The stopper's POSITION, not its identity.** `refused` holds line
        # text, and CPython hands back one shared object for every
        # one-character string -- so two refused lines that are both `|` are
        # the same object, `line is stopper` matched both, and the tail came
        # from the last of them with the clause about the lines below silently
        # dropped. Every entry appended before the stopper carries `got` True
        # and the stopper's is the last of those, which is a fact about how
        # `refusal` fills the list rather than about the text (#430, round 2).
        #
        # **And the arm below is chosen the same way**, because it was the
        # other half of the same class. `mine is stopper` is sound only while
        # `names_this_row` keeps `mine` too long for that shared cache -- a
        # premise nothing here states and no case pins, three lines under the
        # comment saying what the cache costs (#430, round 3).
        stopper_at = max(
            position for position, (_line, got) in enumerate(refused) if got
        )
        after_stopper = [text for text, _got in refused[stopper_at + 1 :]]
```
```python
        elif mine_at == stopper_at:
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q` in a clean clone at `631df12` | `164 passed, 3 skipped` |
| `evidence-check` over the whole tree at `631df12` | exit 0 · `1364 ok · 0 drifted · 0 broken`; this work item's fragment `11 ok` |
| `survivor-check --range 20eade5..5a1f47e --exempt seal/specs/1789721571-…/survivors.md` | exit 0 · 27 removed sentences · two survivors, both excused; the other four exemption rows matched nothing |
| `fence_left_open` over a config whose row sits in a block that closes with a second block opened and never closed below it | `fence_left_open(home)` is `True`; `fence_left_open(home, at)` is `False`, `at` is 7. The default gives the pre-fix answer |
| A grep of `tests/` for `fence_left_open` | no hit. Nothing in the suite calls the unit, with or without the second argument |
| `refusal` over a config with two identical `Broad gate` refused lines, one above the first parsed row and one as the stopper, then `missing_row` over the same file | `mine == stopper` is `True`, `mine is stopper` is `False`, distinct ids; the refusal takes the *stopped LOWER DOWN* arm. `"\|\n\|\n".splitlines()` gives one shared object; the same two long lines give two |
| `missing_row` over seven config shapes — all five arms of the quoted-line refusal and the hidden-row refusal, each with and without a further refused line below | every sentence true of the file that produced it; the new *There is more than one line to write here* clause prints in the one arm where the repair costs a row and is absent from the arm where it costs nothing |
| `round-record close --item … --round 2 --fixes … --range 20eade5..5a1f47e` re-run in a clone from round-2.md's pre-close state | the same `Fix range`, `Contract changes` and `New units` values byte for byte, including `fenced_row_at (depth 1)`; no depth-2 refusal |
| `units_named_earlier` over round-1.md with the reader `close` uses | `{'fencemap': 1, 'fenceleftopen': 1, …}` — `chain.EMPHASIS` is `[*_`]+` over the whole entry, so `fence_left_open` is unreachable to `depth_two` |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** It is the sealer's, once, after the rounds settle (`agent-contract` §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/implement/scripts/seal.py#table_span`, `#with_row`, `#mode_report` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row`, `#fenced_row` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row`, `spec.md` §*Data & interfaces* | round 1's 3 — fixed |
| round-1 | `seal/specs/1789721571-…/overview.md` §*Not done* | round 1's ⬜ — correction |
| round-1 | `seal/ledger.md` | round 1's ⬜ — correction |
| round-1 | `hooks/config.py#unfenced` | round 1's ⬜ — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#load` | round 1's ⬜ — answered |
| round-1 | `hooks/config.py#unfenced`, `#config_rows` | round 1's ⬜ — answered |
| round-1 | `seal/config.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row` | round 1's 🟢 — confirmed |
| round-1 | `hooks/optin.py#parity_config` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py#config_rows` | round 1's 🟢 — confirmed |
| round-1 | `tests/` | round 1's 🟢 — confirmed |
| round-2 | `skills/implement/scripts/seal.py#with_row`, `#write_row` | round 2's 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row` | round 2's 2 — fixed |
| round-2 | `seal/specs/1789721571-…/spec.md` §*Data & interfaces* | round 2's ⬜ — correction |
| round-2 | `seal/ledger/1789721571-…md` | round 2's ⬜ — correction |
| round-2 | `tests/test_the_mode_question_is_asked_once.py:633`, `:553` | round 2's ⬜ — correction |
| round-2 | `skills/implement/scripts/seal.py#write_row`, `tests/test_the_mode_question_is_asked_once.py` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py#fence_left_open`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1789721571-…/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `2ad0a56`, `94f5a1d`, `87fc32c` | round 2's 🟢 — confirmed |
| round-2 | `tests/`, the repository's `Broad gate` row | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `fence_left_open`'s `above=None` default, and the unit having no case of its own | an issue — the run is capped, so nothing it opens is commissioned as a fix | the repository owner |
| The `mine is stopper` identity comparison and its unstated premise | an issue, for the same reason | the repository owner |
| `units_named_earlier` strips underscores, so `depth_two` reaches no snake_case parent | already RIDERed at `skills/code-review/scripts/round_record.py#units_named_earlier`, with the repair described | the repository owner |
| `round_record.py` and `chain_check.py` were not driven against a fenced example table | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after this record | the sealer |
