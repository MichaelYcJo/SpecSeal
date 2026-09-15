# Round 1 — the checker is wrong about itself, and nothing goes red

Target SHA `0ff4e3e`, branch
`fix/142-333-334-335-342-395-the-checker-is-wrong-about-itself-and-nothing-goes-red`,
range `aa3000d..HEAD`. Reviewed in a `git clone --no-local` at that commit,
deleted at the end of the round.

## How the findings relate

Two of the four sit in the same seam, and the second only exists because of
the first. #342's repair reaches forward from `close --round N` into round
N+1's `## Inherited coordinates`, and it assumes that every row that section
carries under `round-N` has a counterpart in round N's **numbered** verdict
rows. `inherited_rows` guarantees neither direction of that. So:

1. it writes a row for a verdict row that commissions nothing, which `close`
   never puts in the map → `close` refuses (🔴 1);
2. it drops a round N coordinate an earlier round already claimed, so the
   section can name nothing from round N at all → `close` refuses (🔴 2).

Both were reproduced against records this generator itself wrote. The third
finding is a separate unit with the same flavour — #333's repair takes the
file-level fallback in a case where it did resolve the adder, and then prints
a sentence saying it did not (🟡 3). The fourth is a citation that does not
resolve (🟡 4).

Spec compliance was checked first and S1–S16 are met; the measurement
disclosures all hold. Those confirmations are at the end.

---

## 🔴 1 — `close` refuses a pair of records the generator itself wrote, whenever the round carries a row that commissions nothing

**Location** `skills/code-review/scripts/round_record.py#reach_forward`, the
coordinate refusal at `:1535`, against `round_record.py#close`'s map at
`:3719-3727`.

`close` builds the map the reach reads from `rows.values()`, and `rows` is
`verdict_rows`' output — `{finding number: (index, cells)}`. A row whose `#`
cell commissions nothing is absent from that mapping by design, which is what
the function's own docstring says it is for. `inherited_rows`, which `new`
runs, writes one row per `Location` cell of **every** verdict row, numbered or
not. So a confirmation row's coordinate reaches round N+1's section and is not
in the map, and `reach_forward` raises.

**Executed** in the clone, on a fixture whose round 1 carries
`| 🔴 1 | … | `mod.py#helper` | open | … |` and
`| 🟢 | … | `README.md` | verified | … |`:

```
INHERITED: {'`mod.py#helper`': "round 1's 🔴 1 — open",
            '`README.md`': "round 1's 🟢 — verified"}
EXIT: 2
OUT: round-record: round-2.md inherits ``README.md`` from round-1, and
     round-1's verdict table holds no row with that `Location`. The
     reach-forward sets a `Why` cell from the row it names and does not guess
     which row that is; correct the coordinate; no cell was written
```

**Why it matters, in the shape this repository writes records.** A row that
commissions nothing is not an edge case here — it is the shape `agents/warden.md`
and `skills/code-review/SKILL.md` instruct a reviewer to use for a
confirmation, for an earlier round's closure carried forward, and for
`❓ out of verified scope`. The committed corpus holds 25 of them. Any round
carrying one, in a run where the verifying round was generated before the fix
pass closed the round below it, cannot be closed at all: `close` exits 2 with
nothing written, and the reader who follows the refusal's instruction —
*correct the coordinate* — will change a coordinate that is already correct.
The likeliest repair a person reaches for is deleting the inherited row, which
throws away the coordinate the section exists to carry.

Nothing is lost and nothing crashes; the run stops.

---

## 🔴 2 — `close` refuses when the round's coordinates were all claimed by an earlier round

**Location** `skills/code-review/scripts/round_record.py#reach_forward`, the
empty-fill refusal at `:1552`, against `round_record.py#inherited_rows`.

`inherited_rows` is first-seen-wins across rounds: it walks earlier records
lowest round first and skips a `Location` it has already emitted. A round N
finding at a coordinate round N-1 already used is therefore written into round
N+1's section under `round-{N-1}`, and nothing under `round-N`. `reach_forward`
reads that as *the table names no row from round N* and refuses.

**Executed** in the clone, round 1 finding at `mod.py#helper`, round 2 finding
at the same coordinate, round 3 generated:

```
INHERITED(3): {'`mod.py#helper`': "round 1's 🔴 1 — fixed"}
EXIT: 2
OUT: round-record: round-3.md's `## Inherited coordinates` names no row from
     round-2, and `new` writes one per `Location` cell of every earlier
     record. A table with nothing from round-2 in it is one this round's
     verdicts cannot be carried into, so the reach is declined rather than a
     row invented; no cell was written
```

**The refusal's grounds are stated as a fact about `new` that is not true.**
`new` writes one row per `Location` cell **that no earlier round already
claimed** — that is `inherited_rows`' `seen` set, and `phase-6.md` reads the
rule without the qualifier. A re-review round looking again at the coordinate
the round before it opened is the ordinary case, not an exotic one, so this
fires on the shape the section is most useful for.

---

## 🟡 3 — the file-level fallback fires where the range did resolve the adder, and says it did not

**Location** `skills/code-review/scripts/round_record.py#depth_two`, `:3487`.

`candidates` is keyed only by findings whose `Location` sits inside a unit an
earlier record names. `unit_adders` resolves every `fixed` commit's added
units, including units added by findings that are **not** candidates. When the
adder is one of those, the intersection is empty, `len(owners) != 1`, and the
walk takes the fallback — refusing the unit and printing *the range does not
resolve which fix added it*, which `unit_adders` just did.

**Executed** in the clone. Round 1 names only `alpha`; round 2 opens finding 1
inside `alpha` and finding 2 inside `beta`, which no earlier record names; the
fix range is two commits and it is **finding 2's** commit that adds the new
unit:

```
EXIT: 2
OUT: round-record: `betaguard` in pair.py would be at depth 2, and the
     attribution is FILE-LEVEL: the range does not resolve which fix added
     it, so every fix inside an earlier unit in pair.py is a candidate —
     🔴 1 (inside `alpha`, round-1.md). …
```

`betaguard` was added by the fix of finding 2, and finding 2 sits inside no
unit an earlier record names, so the unit is at **depth 1** and the rule has
nothing to say about it. This is #333's own *quiet direction*, which the
ticket names and says nobody had measured. It is not a regression — the
file-level walk refused the same thing — but the repair now holds the
information that would answer it and does not use it.

**It also contradicts the sentence this branch ratified in the same commit.**
`docs/review-chain-spec.md:1274` reads *Where the range cannot resolve one — a
single commit answering two findings resolves to nothing at any cost — it
still refuses*. Here the range resolves one, and the code behaves as though it
had not. §14's pinned text is false in a reachable case.

---

## 🟡 4 — a case comment sends the reader to a file that holds nothing about it

**Location** `tests/test_the_fixes_close_the_record.py:1252-1253`.

The comment above the depth-2 pair fixture says the emphasis defect "is
written up in `seal/follow-up.md` rather than repaired here". **Measured:**
`seal/follow-up.md` carries no occurrence of `EMPHASIS`, of the stripped
spelling, or of the enclosing unit's name, and `git log aa3000d..HEAD --
seal/follow-up.md` is empty — the branch never touched that file.

Where it is actually written up is the stamped `# RIDER:` inside
`skills/code-review/scripts/round_record.py#units_named_earlier`, which is
what `phases/phase-5.md` and `overview.md` both say. So the one carrier a
reader is likeliest to open — the comment beside the fixture constraint — is
the one pointing at the wrong home.

This is the class the round was told to watch for, and it is the third
mis-citation this work item has met (`plan.md` records two of the tickets'
own).

---

## ⬜ 5 — `unit_adders` runs on every `close`, including the rounds where the walk returns immediately

**Location** `skills/code-review/scripts/round_record.py`, `:3622`.

`unit_adders(reader, root, fixes)` is evaluated at the call site, so its second
`measure` pass runs before `depth_two` can take its own
`if not named or not added: return`. Round 1 has no earlier records at all, so
every round-1 `close` pays it for nothing — `phases/phase-5.md` measured that
pass at 127.8 ms against 36.4 ms for the range pass.

Not a defect, and small; it is here because the guard it should sit behind is
four lines away. **It carries an id** because the one-line move below is a
change to the tool that a fix pass can make — `⬜` means *fixed in passing or
not at all*, and this is the passing. It stays out of `Needs a fix`, which
counts 🔴 and 🟡 only.

---

## ⬜ — two frame documents still carry the corpus figure the branch corrected, and this one is for the memo

**Location** `seal/specs/1789425391-…/plan.md:21` and the same directory's
`spec.md:143` (S16).

Both read *this repository's own 176 records*. The measured figure is 211 of
212, and `overview.md`'s divergence table records the correction with its
grounds.

**This row commissions nothing, and that is deliberate rather than a severity
call.** `plan.md` and `spec.md` are the framer's artifacts, and a fix pass may
not rewrite the frame — so there is no row a fix table could be asked to close
here, and numbering it would ask for one. It takes no id for the same reason a
confirmation does.

What I mean by it is **a line for the closing memo**: the work item corrected
the figure everywhere it is load-bearing and left it standing in the two
sentences a next reader opens first, and the memo is where that residue is
stated. If the owner would rather the frame be corrected in place, that is the
framer's edit and a decision above this round.

---

## What was checked and held

Spec compliance first. Each row read as the state it names, against the code
and against the mutation that would put the state back.

| Row | Verdict |
|---|---|
| S1 six shapes | **Held, executed.** `test_a_row_that_commissions_nothing_cannot_read_open` carries all six; three (`carried`, `A`, `—`) have no severity marker. Arm disabled → all six red. |
| S2 short row, both subcommands | Held, read. Cases on `new` and on `close`, both asserting no traceback. |
| S3 four-cell row | Held, read. `assert code == 0`, one answer. |
| S4 / S5 boundary | **Held, executed.** `OPEN_BOUNDARY` borrowed from `chain.SEPARATORS` → both boundary cases red. |
| S6 the figure | **Held, executed.** Re-derived independently; see below. |
| S7 the comment | Held, read. `OPEN_WORD`'s comment says *one WORD rather than a vocabulary test*; the word *exact* is gone, and two cases in `tests/test_the_rules_have_one_owner.py` pin it. |
| S8 two records agreeing | Held for the numbered case, executed — and **🔴 1 and 🔴 2 are the two shapes it does not reach.** |
| S9 `seal` refuses `round-N` | **Held, executed.** Predicate back to shape-only → the refusal cases red. |
| S10 the gate's literal | Held; the orchestrator's mutation, not re-run. The route is asserted inside the case, which is what keeps it from quietly missing the state. |
| S11 / S12 depth-2 | Held, executed — with 🟡 3 against the fallback arm. |
| S13 / S14 / S15 #142 | **Held, executed.** `failures.extend(errors)` → `pass` turns the control red; all three readers list from HEAD; the third is repaired and its residual stated in its own docstring. |
| S16 own records | **Held, executed.** Both walkers green in the 249-case run below. |

**The three disclosures, verified rather than taken.**

- **The corpus figure.** Re-derived at `0ff4e3e` through `table_body` under
  `VERDICT_HEADER`, `chain.verdict_of` and `says_open`, in one pass:
  212 carried, **211 parse**, 2,044 verdict rows, **0 short**, **123** cells
  the arm reads as open, **9** wider than the bare word (so equality reaches
  **114**), **0** of the 123 in `CLOSED_WORDS`, **51** no-digit `#` cells of
  which **25** admitted, **15** of those carrying a verdict outside
  `CLOSED_WORDS`, **0** newly refused. Every figure in the shipped docstring
  matches. All four conditions `plan.md` §*#331's trap* sets are met —
  population named exactly, date, readers by name, and the whole triple taken
  together — and round 4's `95 / 7 / 88` was not carried.
- **The name `spec.md` S11 cites** occurs nowhere outside work item
  `1789002694`'s own round records, each of which carries the marker on the
  line. `git log --all -S` over the name finds it in no commit that touches
  `skills/verify/scripts/broad_gate.py`. The marking is honest and S11's claim
  — which is about the *shape*, two findings in one file inside two different
  earlier units — is what the cases build.
- **176 → 211** is real and corrected everywhere it is load-bearing; ⬜ 6 is
  the residue.

**Nothing else.** Both ledgers are clean, the work item's prose states no name
the tree lacks, and every refusal this branch adds or rewrites names an exit.

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py tests/test_chain_check_at_the_pull_request.py tests/test_the_reopening_is_one.py tests/test_the_rules_have_one_owner.py -q` in the clone at `0ff4e3e` | 249 passed, 1 skipped, exit 0 |
| Mutation: `OPEN_BOUNDARY` borrowed from `chain.SEPARATORS` | exit 1 — the boundary and the coupling cases red; restored, tree clean |
| Mutation: the verdict-column arm disabled | exit 1 — 10 failed / 58 passed; all six no-commission shapes and all four spellings red |
| Mutation: `seal` back to shape-only on `Fixes checked by` | exit 1 — the `round-N` refusal cases red |
| Mutation: `depth_two` attribution back to the first candidate row | exit 1 — the naming case red |
| Mutation: both `failures.extend(errors)` in `tests/test_chain_check_at_the_pull_request.py` replaced with `pass` | exit 1 — the positive control red |
| Mutation: `reach_forward` returns `None` unconditionally | exit 1 — the two-records case red |
| Control: the same six selections unmutated | 5 / 4 / 5 / 1 / 1 / 1 passed, exit 0 each |
| Corpus re-measurement through the module's own readers (probe, deleted) | every shipped figure reproduced; see above |
| Probe: round 1 carrying one numbered row and one confirmation row, `new --round 2`, then `close --round 1` (deleted) | exit 2, refused — 🔴 1 |
| Probe: round 2's only finding at round 1's coordinate, `new --round 3`, then `close --round 2` (deleted) | exit 2, refused — 🔴 2 |
| Probe: one finding inside an earlier unit, the other outside, the outside one's commit adding the unit (deleted) | exit 2, refused a depth-1 unit — 🟡 3 |
| Ledger drift over `seal/ledger.md` and this work item's fragment, through the checker's own reader | 1214 rows and 40 rows, 0 not OK |
| Name scan over the work item's twelve documents and its ledger fragment, through the checker's own reader | 0 names the tree does not carry |
| The broad gate — full suite, repository-wide lint, typecheck | **not yet** — `skills/agent-contract/SKILL.md` §2 assigns all three to `agents/sealer.md`, spawned after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `chain.EMPHASIS` strip reaching no snake_case parent, so the depth-2 walk reaches no Python unit whose name carries an underscore | already deferred in the build — a stamped `# RIDER:` at `round_record.py#units_named_earlier`, named in `overview.md` §*Not verified* | the repository owner |
| Whether `no fixes to check` beside a fix-surface row reading *none — the fixes are not yet written* should be refused | already deferred — Q1, answered **(a) leave it open** by the owner before the build | the repository owner, in 0.12.0 beside #174 |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `close` refuses a generated pair whenever the round carries a row that commissions nothing | `skills/code-review/scripts/round_record.py#reach_forward` `:1535` | open | Executed: exit 2, nothing written, on records `new` itself wrote. The shape is the one `agents/warden.md` instructs reviewers to use, and the corpus holds 25 of them |
| 2 | 🔴 `close` refuses when an earlier round already claimed every coordinate this round opened | `skills/code-review/scripts/round_record.py#reach_forward` `:1552` | open | Executed: exit 2, nothing written. `inherited_rows` is first-seen-wins across rounds, and the refusal states a rule about `new` without that qualifier |
| 3 | 🟡 the file-level fallback fires where the adder resolved, and the message says it did not | `skills/code-review/scripts/round_record.py#depth_two` `:3487` | open | Executed: a depth-1 unit refused. Contradicts `docs/review-chain-spec.md:1274`, written in this branch |
| 4 | 🟡 a case comment names `seal/follow-up.md` as the home of a defect that file does not carry | `tests/test_the_fixes_close_the_record.py:1252-1253` | open | Read: no occurrence in that file, and the branch never touched it. The real home is the `# RIDER:` at `units_named_earlier` |
| ⬜ 5 | `unit_adders` runs before the guard that would skip it | `skills/code-review/scripts/round_record.py:3622` | open | Read: 127.8 ms paid on every round-1 `close`, where `depth_two` returns at once. Numbered because it does commission the one-line move under `## Paste-ready fixes` — fixed in passing or not at all, and ⬜ is never counted by `Needs a fix` |
| ⬜ | two frame documents keep the corrected corpus figure | `seal/specs/1789425391-…/plan.md:21`, `spec.md:143` | answered | Read: both say 176; measured 211 of 212. **No id, because it commissions nothing a fix pass may do** — `plan.md` and `spec.md` are the framer's files. It is a line for the closing memo, and `overview.md`'s divergence table already carries the correction with its grounds |
| 🟢 | S1–S7 and S9–S16 confirmed | the modules named in `plan.md`'s Verified-by column | answered | Executed — the narrow run and seven mutations above. A confirmation this round verified and did not open, so it takes no id |
| 🟢 | the three build disclosures confirmed | `round_record.py#says_open`'s docstring; `spec.md:138`; `overview.md:19` | answered | Executed — the corpus re-measured in one pass, and the name searched over every branch. A confirmation, so it takes no id |

## Paste-ready fixes

**Finding 1 and finding 2 together.** Both come from the same mismatch, and
one change answers both: build the map from every verdict row rather than the
numbered ones, and let a section that names nothing from this round be silence
rather than a refusal.

In `close`, replace the map construction (`round_record.py:3719-3727`):

```python
    # Every verdict row, not only the numbered ones. `inherited_rows` writes
    # one row per `Location` cell of every row -- a confirmation, an earlier
    # round's closure carried forward, a `?` out of verified scope -- and
    # `rows` holds only what `finding_number` keyed. Reading the map from
    # `rows` refused a pair of records this generator itself wrote.
    location = VERDICT_HEADER.index("Location")
    number = VERDICT_HEADER.index("#")
    now = {}
    for i, cells in table_body(reader, reader.readable("\n".join(raw)),
                               VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) > VERDICT_COL and seen[location]:
            now[seen[location]] = (
                seen[number],
                chain.verdict_of(seen, VERDICT_COL),
            )
    forward = reach_forward(reader, rounds, args.round, now)
```

In `reach_forward`, replace the empty-fill refusal (`round_record.py:1552`):

```python
    if not filled:
        # NOT a refusal. `inherited_rows` is first-seen-wins across rounds,
        # so a round whose every coordinate an earlier round already claimed
        # is written into this section under that earlier round and under no
        # other. A re-review round looking again where the round before it
        # looked is the ordinary case, and refusing it stops the run this
        # reach exists to keep truthful.
        return None
```

The case for each, in `tests/test_the_fixes_close_the_record.py`:

```python
CONFIRMATION = "| 🟢 | round 0's finding, re-read | `README.md` | verified | read |\n"


def test_a_row_that_commissions_nothing_does_not_stop_the_reach(repo):
    """Finding 1. `inherited_rows` writes a row per `Location` cell of EVERY
    verdict row; `close` keyed its map from the numbered ones. A round
    carrying a confirmation -- the shape `agents/warden.md` asks for, and 25
    of the committed corpus -- then could not be closed at all."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1 + CONFIRMATION))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    a = commit(repo, "round 2")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, _ = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    why = inherited(repo)
    assert why["`mod.py#helper`"] == f"round 1's 🔴 1 {chr(0x2014)} fixed", why
    assert why["`README.md`"] == f"round 1's 🟢 {chr(0x2014)} verified", why


def test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused(repo):
    """Finding 2. Round 2 opens a finding where round 1 opened one, so round
    3's section carries the coordinate under `round-1` and nothing under
    `round-2`. That is silence, not a malformed record."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    a1 = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b1 = commit(repo, "round 1's fix")
    close(repo, 1, fix_table(f"| 1 | fixed | {b1[:7]} |\n"), f"{a1}..{b1}")
    commit(repo, "round 1 closed")
    code, out, _ = generate(
        repo, n=2,
        report_text=report(
            verdicts="| 🟡 1 | helper still drops b | `mod.py#helper` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    commit(repo, "round 2")
    code, out, _ = generate(
        repo, n=3,
        report_text=report(verdicts="| 🟡 1 | a third look | `mod.py:5` | open | read |\n"),
    )
    assert code in (0, 1), out
    a = commit(repo, "round 3")
    write(repo, "mod.py", MOD_CHANGED + "\n\ndef extra():\n    return 1\n")
    b = commit(repo, "round 2's fix")
    code, out, _ = close(
        repo, 2, fix_table("| 1 | answered | grounds |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "Inherited coordinates" not in out, out
```

**Finding 3.** A unit whose adder the range resolved to a row that is not a
candidate is at depth 1, and the rule has nothing to say about it. Replace the
per-unit decision in `depth_two` (`round_record.py:3487`):

```python
    for (f, name), rows_for in candidates.items():
        resolved = set(adders.get((f, name), ()))
        owners = sorted(resolved & set(rows_for))
        if len(owners) == 1:
            unit, record_n, cell_text, location = rows_for[owners[0]]
            lines.append(
                f"`{name}` in {f} would be at depth 2: added by the fix of "
                f"{cell_text}, whose Location `{location}` is inside `{unit}`, "
                f"a unit round-{record_n}.md's `{chain.NEW_UNITS}` names."
            )
            continue
        if resolved:
            # The range DID resolve the adder, to a row that sits inside no
            # unit an earlier record names. The unit is at depth 1 and this
            # rule has nothing to say about it -- #333's quiet direction,
            # where the file-level walk named every unit in the file against
            # whichever candidate it reached. Only an UNRESOLVED unit takes
            # the file-level sentence below.
            continue
        every = "; ".join(
            f"{cell_text} (inside `{unit}`, round-{record_n}.md)"
            for _n, (unit, record_n, cell_text, _loc) in sorted(rows_for.items())
        )
        lines.append(
            f"`{name}` in {f} would be at depth 2, and the attribution is "
            f"FILE-LEVEL: the range does not resolve which fix added it, so "
            f"every fix inside an earlier unit in {f} is a candidate — {every}."
        )
    if not lines:
        return
```

and its case, in `tests/test_the_fixes_close_the_record.py`:

```python
def test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one(repo):
    """#333's quiet direction. Round 1 names `alpha` only; finding 2 sits
    inside `beta`, which no earlier record names, and finding 2's commit is
    what adds the unit. The range resolves that, so the unit is depth 1 and
    the walk says nothing -- where the file-level answer refused it and the
    fallback message claimed a non-resolution that did not happen."""
    a = one_finding_inside_one_earlier_unit(repo)
    write(repo, "pair.py", PAIR_ALPHA_FIXED)
    c1 = commit(repo, "finding 1's fix, adding nothing")
    write(repo, "pair.py", PAIR_BOTH_FIXED + BETA_GUARD)
    c2 = commit(repo, "finding 2's fix, adding the unit")
    code, out, _record = close(
        repo, 2,
        fix_table(f"| 1 | fixed | {c1[:7]} |\n| 2 | fixed | {c2[:7]} |\n"),
        f"{a}..{c2}",
    )
    assert "depth 2" not in out, out
    assert code == 0, out
```

**Finding 4.** In `tests/test_the_fixes_close_the_record.py:1252-1253`:

```python
# of its own, outside this work item's six tickets, and it is written up in
# the stamped `# RIDER:` at `round_record.py#units_named_earlier` rather than
# repaired here.
```

**⬜ 5.** Give `depth_two` the pass rather than its result, so the guard runs
first. At the call site (`round_record.py:3622`):

```python
        lambda: unit_adders(reader, root, fixes),
```

and inside `depth_two`, under the existing early return:

```python
    named = units_named_earlier(reader, earlier)
    if not named or not added:
        return
    adders = adders() if callable(adders) else (adders or {})
```

**The frame documents.** No paste-ready fix, on purpose: the two sentences are
the framer's and a fix pass may not rewrite them. The sentence for the closing
memo is the whole of what that row asks for — *the corpus figure was corrected
to 211 of 212 everywhere it is load-bearing, and `plan.md` §Summary and
`spec.md` S16 still read 176.*

Needs a fix: yes — findings 1 and 2, the two reachable states where `close`
refuses a pair of records the generator itself wrote; and findings 3 and 4.

Loses a record or crashes: no — every refusal above lands with nothing on
disk changed, which is the property `close` is built around.

## Proof

Opened and read: `seal/specs/1789425391-…/{routing,spec,plan,questions,overview,survivors,changelog}.md`
and `phases/phase-{1..6}.md`; `seal/ledger/1789425391-…​.md`; `seal/ledger.md`
and `docs/review-chain-spec.md` over the branch diff; `seal/config.md`;
`seal/follow-up.md` (searched); issues #142, #333, #334, #335, #342, #395 with
their comments; `skills/code-review/scripts/round_record.py` at
`OPEN_WORD`/`OPEN_BOUNDARY`/`says_open`/`finding_number`/`verdict_rows`/
`inherited_rows`/`reach_forward`/`reach_back`/`units_named_earlier`/
`unit_adders`/`depth_two`/`close`/`last_record`/`seal`;
`skills/code-review/scripts/chain_check.py#verdict_of`;
`tests/test_a_finding_id_is_a_bare_integer.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_record_is_generated.py` (helpers);
`agents/sealer.md`, `agents/warden.md`, `templates/sdd-round.md`,
`skills/code-review/SKILL.md` over the branch diff;
`skills/evidence-check/scripts/evidence_check.py` at `claim_lines`,
`stated_names`, `tree_names`, `check_ledger`, `main`; `bin/test`;
`~/.claude/skills/writing-style/SKILL.md`.

Executed: the runs in `## Executed probes`. The clone, its virtualenv and
every probe file were deleted at the end of the round.
