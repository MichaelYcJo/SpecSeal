# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 0011e870 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 2: the lexer (comments, strings, template literals, char
literals; the forms per language from Q1), memoised per text; the depth walk
with the Allman clause and the deeper-continuation clause; the closer-only
last line left out; imbalance and an unterminated literal refused; the
day-one list; `file_units` on `generic_units`'s opener; the shell-shaped
fixture of `test_a_multi_line_declaration_with_a_bare_name_is_still_sure`
re-fixtured in a brace language; #848's reproduction as a case. Cases S1,
S2, S3, S4, S9 red, then green.

## What this phase found

**Q1 is (b), one row per family, and the table lives in `_literal_at`'s
docstring.** Nine families cover the eighteen suffixes (`BRACE_FAMILY`). Each
row is the forms of the language's own grammar: JS template literals with
`${…}` holes, the C23 digit separator `1'000`, C++ `R"d(…)d"` with its
prefixes, Java text blocks, C#'s verbatim, interpolated, verbatim-interpolated
and raw strings with `""`/`{{`/`}}` doubling, Kotlin and Swift holes, Swift
`#"…"#`, Go's backtick raw string, Rust's raw strings, multi-line strings,
char literals and lifetimes, and nested block comments in Rust, Swift and
Kotlin. A C++ raw string whose delimiter is malformed is the one form the
walk names and cannot read; every line from it down is refused.

**Forms not lexed, and why each is loud.** JS regex literals and JSX text
are not lexed; C# raw strings' holes are read as content; C preprocessor
branches are read as code. A bracket that these leave open reaches end of
file and is refused; an apostrophe in JSX text opens a `'` string its line
never closes, which is refused. What stays silent is only a mis-read that
re-balances by accident, the six-month scenario `plan.md` names.

**A stray CLOSER inside a body does not mislead the walk, and a stray
OPENER always refuses.** Measured by mutating each form: with `}` inside
every form, eight of the form mutations survived, because the body's deeper
lines carry the walk past an early close and the closer-only last line is
left out either way. The fixtures now hold opening brackets, and every form
mutation goes red.

**`generic_units` takes the family as well as the rule.** `spec.md` §*Data &
interfaces* gives `generic_units(lines, name, rule)`; the walk cannot lex
without knowing which family's `'` is a char, a string or a lifetime. It is
`generic_units(lines, name, rule, family=None)`, `family` read from
`brace_family(path)` beside `bounding_rule`.

**One candidate the walk cannot bound refuses the answer.** A refusal among
the candidates `generic_units` would choose from (the unblocked ones, or the
resurrected ones where none is unblocked) refuses the whole reading; a span
beside it would be a choice among places nobody bounded. A blocked call site
that refuses does not refuse a declaration that resolves.

**The colon judgment had two copies and is now `generic_units`' alone.**
`file_units` lists every name the shared opener matches and lets
`generic_units` decide which match declares; its own copy of the colon test
survived mutation, because `generic_units` re-judged every name it listed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The indentation loop in `generic_units` for brace languages | `brace_span`; YAML's half is `block_span`, unchanged until phase 3 |
| The opener's second spelling in `file_units` (inventory E18) | `declaration_opener`, asked for `\w+` there and for one escaped name in `generic_units`; S9's case |
| The colon test's copy in `file_units` | `opens_declaration`, called by `generic_units` |
| The shell fixture of `test_a_multi_line_declaration_with_a_bare_name_is_still_sure` | a TypeScript class method, the same property |
