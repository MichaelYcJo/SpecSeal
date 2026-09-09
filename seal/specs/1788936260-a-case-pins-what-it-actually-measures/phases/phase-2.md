# 1788936260-a-case-pins-what-it-actually-measures — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `8d53ca4` |
| Ran by | unknown — the spawn prompt carried no `Ran by` value, and this row is the spawning session's rather than the segment's own; the orchestrator fills it |

## What this phase was asked

The arm enumeration: an AST walk with #262's counting rule, **refusing node
types it does not know** rather than skipping them. Verified against a fixture
module whose arms are known by construction, plus the real module's 31 with
the per-function split.

Two conditions came with it, and both are about the same failure. §12 applies
to the enumeration itself — the class is *the arm shapes the walk recognises*,
and this is the thing whose enumeration going short IS the defect — so the
sweep is against the grammar rather than against the module being tested on.
And `questions.md` assumption 2: a walk that skips silently is the failure of
the thing it replaces, one level up.

## What this phase found

**The per-function split reproduces the handoff's number exactly, and the
walk finds one arm neither hand count had a row for.**

| Scope | Arms | #262's table | Handoff |
|---|---|---|---|
| `reader` | 5 | 5 | 5 |
| `is_closed` | 4 | 4 | 4 |
| `gh_segments` | 5 | 5 | 5 |
| `main` | **17** | 19 | 17 |
| `<module>` | **1** | — no row | — no row |
| total | **32** | 33 | 31 |

The 31 is confirmed by construction. The extra one is
`if __name__ == "__main__":`, which sits in no function, so a table with a row
per function had nowhere to put it. That is the enumeration going **long**,
which is the safe direction, and it is pinned rather than filed off:
attributing a module-level arm to the last function above it, or dropping it,
are both ways for the total to stop matching what the file holds.

#262's table of 33 is left as written (`questions.md` assumption 3).

**The counting rule that makes the two numbers comparable is `top-level
members, not flattened`, and it was not obvious.** `gh_segments`'s `while`
test is `i < len(toks) and (("=" in toks[i] and not toks[i].startswith("-"))
or os.path.basename(toks[i]) in WRAPPERS)`. Counting the top-level members of
the outer `BoolOp` gives 2 and the function gives 5, matching both hand
counts. Flattening recursively gives 4 and the function gives **7**. Either
rule is defensible in the abstract; only one keeps any number this checker
prints comparable with the ticket's, so it is pinned on the fixture and on the
real function.

**The refusal needs the tables to be TOTAL, or it fires on ordinary code.**
That is what turned §12's sweep into a real piece of work rather than a
gesture. This interpreter's `ast` has **122** constructors once the thirteen
ASDL sum types are removed, and every one of them is now either an arm shape
or a named non-arm with grounds. Two of them were nearly missed:

- **`Constant`.** Walking `ast.AST`'s subclass tree for LEAVES drops it,
  because the deprecated aliases `Num`, `Str`, `Bytes`, `NameConstant` and
  `Ellipsis` are its subclasses. It is the node type in nearly every parse, so
  a leaves-only enumeration would have left the refusal firing on the first
  literal in any module.
- **`Assert`.** Its test IS a test a mutation could flip, and #262's rule —
  which the measured 31 is counted under — does not count it. Counting it
  would move every per-function number away from the hand count the walk is
  checked against, so the exclusion is **declared** in `NOT_ARMS` where it can
  be overturned, rather than omitted and left to be rediscovered.

**What I refused, and it is the answer to §12's *say what you refused*.**
`For`/`AsyncFor` are excluded even though a `for`'s `orelse` is arguably an
arm — it runs unless something breaks. #262's rule does not count it and
`is_closed`'s `for path in records` is not among that function's four, so
counting it would part the walk from the number it is checked against.
`BoolOp` outside an arm's test is excluded because a boolean test is read
*through* it; counting it on its own is what would take `main` past 17
(`cwd = payload.get("cwd", "") or "."` is a value, not a branch). Both are
written into the classification with those grounds beside them.

**Two arm shapes were added beyond #262's four**, because the plan names them
as its own failure scenario: `match_case` (each alternative of a `MatchOr`
pattern, plus each top-level member of the guard) and `comprehension` (each
`if` guard). They change no count here — the module has neither — so the 31
is reproducible under four shapes and under six alike.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
