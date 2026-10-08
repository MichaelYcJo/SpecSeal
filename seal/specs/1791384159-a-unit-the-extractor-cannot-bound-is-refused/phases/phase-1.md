# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cfcd630d |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 1: `bounding_rule(path)`; the four suffix dispatches read
it; `resolve_unit` carries a refusal reason in one reading (Q4) and the
callers unpack it; a `.py` that will not parse and a suffix with no rule are
`BROKEN` with the reason and the quoted-line remedy on the line; `--reverify`
prints and writes nothing. Brace suffixes and YAML still go through today's
`generic_units`. Cases S5, S6, S8, S10 red, then green. The spawn added: the
branch has merged `origin/release/v0.21.0`, so #867's `heading_rule` and
`markdown_lines` are what the `.md` arms call, and `plan.md` §*Seams* predates
them.

## What this phase found

**Q4's shape is a two-tuple that carries the refusal, not a three-tuple.**
`Resolution(places, resurrected, refused)` unpacks as the pair every caller
already read, with `refused` an attribute. Twenty-one call sites in six test
modules unpack the pair (`git grep "= ec.resolve_unit\|= checker.resolve_unit"
d611c1a0 -- tests/`), and
`resolve`'s docstring keeps the wrapper for "anything importing this module";
a three-tuple breaks every one of them for a fact a refused answer already
shows by having no places. A caller that never asks for the reason reads
nothing there, which is the direction a refusal wants. One reading still:
the reason comes back from the same call.

**There were four production callers, not three.** `read_citation` reads the
section a `Re-read ·` or `Corrected ·` row cites through `resolve_unit` too,
and a bare symbol there now reads the heading refusal rather than "the
section it names is gone". It reads `.refused` like `judge` and the rider
check; S8's case counts all five callers (`resolve` is the wrapper).

**A bare symbol in `.md` is refused.** The table names "heading" for `.md`,
which bounds a quoted heading path; a bare symbol there used to run the
indentation rule over markdown. No ledger row here cites one (measured: 1,964
`.md` coordinates, every one quoted), so the refusal changes no reading this
repository holds. Its sentence names the heading path as the anchor to use.

**#867's seams held without a conflict.** The `.md` arms already called
`markdown_lines` and `heading_level`; the table replaced the `endswith(".md")`
test in front of them and left their bodies alone.

**For phase 2:** `generic_units` still returns through `Resolution`, so the
bracket walk's refusal goes in its third field and `judge` already prints it.
`file_units` reads `rule is not None` for the brace and block arms; phase 2
narrows that when `generic_units` takes the rule.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `SyntaxError` fall-through in `resolve_unit` and its comment "The fallback survives only for the file ast cannot read at all" | `bounding_rule`'s docstring and `unbounded`'s Python sentence; `py_spans`' docstring now says the file is refused |
| `test_a_syntax_error_still_falls_back_to_the_text_rule` | `test_a_syntax_error_is_refused_rather_than_read_by_the_text_rule`, same fixture, the refusal pinned |
| Three of the four suffix tests (`resolve_unit`, `minor_region`, `file_units`, `content_matches` each spelled its own) | `bounding_rule`, read by all four; S10's case |
