# 1788700685-two-value-shaped-odd-rows-end-the-report — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b0e4859 |
| Ran by | <the orchestrator fills this — the spawning session is the only party that knows> |

## What this phase was asked

Close the two crashes and pin them, and nothing of phase 2 — the ledger rows
and the changelog fragment belong to a different segment.

1. A naive stamp must not end the report. `parse_time` is the one place a
   string becomes a `datetime`, which is what makes it a funnel rather than a
   patch. `plan.md`'s accepted alternative is to **normalise** there — attach
   UTC, the assumption the file already makes when it rewrites a trailing `Z`
   — rather than to drop the row the way an unparseable one is dropped,
   because a transcript whose stamps are all naive would then report nothing
   where today it reports numbers that are internally consistent. State the
   assumption in the docstring.
2. A zero span must not end the report. `report`'s percentages divide by
   `data['span_s']`, which is `0.0` when a transcript's only paired call
   shares one timestamp. Print the block it can rather than dividing by it,
   and do not invent a percentage for a denominator of zero. Decide what a
   reader sees instead and say why here.
3. Cases for both, over synthetic transcripts, each seen red first, each
   asserting **both** the report and `--json` — the second arm because #175
   records the naive case as exiting 1 with stdout empty on both.

And: enumerate the class by decomposition rather than by listing the two
shapes the issue reported, and say what method was used and how it is known
to be complete rather than merely larger.

## What this phase found

### The handoff's two facts, opened

**`--json` does not take the same path for the two shapes, and the difference
decided the cases.** Measured at `6863669` over hand-built transcripts:

| Shape | Report | `--json` |
|---|---|---|
| naive stamp mixed with an aware one | exit 1, stdout empty | exit 1, stdout empty |
| span of zero | exit 1, **36 bytes** of stdout — the span line, then the crash | **exit 0** |

The naive shape dies in `load`/`analyse`, upstream of the `--json` branch, so
both arms lose everything. The zero span dies inside `report`, which `--json`
never calls — so `--json` survived it already. Its second arm therefore pins
that the guard stays in `report` and is not moved into `analyse`, where it
would change a number `--json` already emits correctly.

**Normalising at `parse_time` closes every site, and there are more of them
than `plan.md` counted.** Every `datetime` in the module is produced at that
one call, so nothing downstream can meet a naive value from another source —
verified by construction below, not assumed. The count in `plan.md`'s
Technical context ("four subtractions") is low on both halves:

- **six** subtractions, not four — `analyse`'s span, per-call sum, turn gap
  and family sum, plus two the list missed: the `exact`/`stripped` duration
  and `slowest`'s;
- **two orderings**, which the plan does not mention at all — `load`'s
  `calls.sort` and `analyse`'s `max(turn_end, ...)`. Mixing a naive stamp
  with an aware one raises on a comparison as readily as on a subtraction.

That second half is the finding, not a tally correction. **A transcript with
two calls dies in `load`'s sort, before `analyse` is entered at all**, so the
issue's framing — "`analyse`'s subtractions" — names the wrong function for
the commoner case, and a guard written at the reported crash site would have
left it standing. It is the same shape as #170's own round 2 finding, where a
list-valued tool name died in `analyse` and a `null` one died in `report`.
Measured: a one-call transcript raises at `analyse:224`, a two-call transcript
at `load:210`.

Also corrected: `report` had **three** divisions by `span_s`, not four. The
fourth site the plan counted is `idle > span_s * 0.1`, a multiplication, which
is safe at zero.

### What a reader sees instead of a percentage

A dash, and one line under the span saying why:

```
span          0.0m   (1 tool calls)
              every call shares one timestamp, so there is no span to take a share of
  command     0.0m   —
  model       0.0m   —   mean gap 0.0s
```

The reasoning behind each half.

**A dash rather than `0%` or an omitted column.** A share of a span of zero is
not zero and not a hundred; it does not exist, and both numbers would be read
as measurements. Dropping the column instead would leave the line looking like
an ordinary report with the percentage forgotten. The dash is unmistakably a
value this file declined to compute, and the times beside it are what was
actually measured.

**One line, because a dash alone poses a question it does not answer.** The
line is text a person reads and acts on, so it is pinned by name.

**The guard is on the span being POSITIVE, not on it being non-zero.** Zero is
the shape #175 measured; a negative span — a harness writing a result before
the call it answers — is the same undefined division with a sign on it, and a
percentage of a negative denominator is a number nobody can read. One
condition covers both, which is the class rather than the coordinate.

**One funnel, not two.** An early draft also guarded the idle block with
`span_s > 0 and …`. That was removed before the commit: `share` is the single
place that decides what a non-positive span means, and a second guard adds a
branch no case exercises. At a span of zero the idle condition (`0 > 0`) is
already false on its own.

### The enumeration, and why it is complete rather than merely larger

The class is *every arithmetic operand taken out of a transcript*. It was
enumerated **by construction on two independent axes**, each closed
mechanically, not by reading the file for suspicious lines.

**Axis 1 — the operations, closed by an AST walk over the module.** A script
listed every `BinOp`, `AugAssign` and `UnaryOp` carrying an arithmetic
operator, every `Compare` carrying an ordering operator, and every
`sort`/`sorted`/`max`/`min`/`sum` call: **56 sites**. Each was classified.
(The first walk returned 42 and missed `AugAssign` and `UnaryOp` entirely —
which is the argument for the method: the gap was found by re-deriving the
list, and would not have been found by reading harder.)

| Class | Sites | State |
|---|---|---|
| Neither operand comes from a transcript — lengths, literals, `os` facts | 30 | not in the class |
| A `usage` number | 4 | closed by `count` (#170's **type** axis) |
| A `datetime` — 6 subtractions, 2 orderings | 8 | **closed by this phase** at `parse_time` |
| Derived from `span_s` — 3 divisions and the idle guard | 4 | **closed by this phase** at `share` |
| A derived denominator other than `span_s` — `max(len(turns), 1)`, `len(gaps)`, `len(part)` | 3 | already guarded at each site, verified by reading |
| Comparisons of derived floats against literal thresholds | 7 | cannot raise on shape |

**Axis 2 — the values that can enter, closed by the reader's own surface.**
A value reaches any of those sites only through `load` or `token_totals`
reading a JSON row, and those two read exactly five fields: `timestamp`,
`message.usage.*`, `message.id`/`uuid`, `tool_use.id`/`tool_use_id`/`name`,
and `tool_use.input.command`. Every one has a funnel — `parse_time`, `count`,
`message_key`, the `isinstance(call_id, str)` guard, `tool_name`, and the
`isinstance(text, str)` fallback. So the class is enumerable as *fields that
enter* × *operations that consume them*, and neither factor is a judgment
call.

That is what makes the answer complete rather than merely larger than the
issue's two: both factors were derived from the file, and either one alone
would have missed something. The operator walk alone does not say which
operands are transcript-derived; the field list alone does not say the
`datetime` axis has an ordering half.

**Each axis then decomposes into type and value**, which is where the two
shapes of this work item come from and where the third came from:

| Axis | Type sub-axis | Value sub-axis |
|---|---|---|
| a number | not a number at all → `count` (#170) | a `float` that is not a quantity → **`NaN`/`Infinity`, open** |
| a `datetime` | naive beside aware → `parse_time` (**this phase**) | two stamps equal → span of zero → `share` (**this phase**) |

### The third operand shape, found by the method and left open

`json.loads` accepts the bare tokens `NaN`, `Infinity` and `-Infinity` by
default, and all three are `float` — so they pass `count`'s `isinstance` check
and reach the three `totals[...] +=` sites in `token_totals`. **Measured**: a
transcript whose `output_tokens` is `NaN` prints `output  nan` and exits 0.

It does not end the report, so `spec.md` scopes it out — that document's In
section is operands that end the report, and its Out section rules out making
the numbers *right*. But it is the exact failure `count`'s own docstring says
`bool` is excluded to prevent: a wrong number rather than a missing one. It is
filed where `seal/follow-up.md` says a coordinate-tied item belongs — a
`# RIDER:` at `count`, stamped, naming the one-line close (`math.isfinite`
beside the `isinstance`) so it reaches whoever next opens that function.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds `share` and the normalising return, and takes nothing out of the tree | none |
