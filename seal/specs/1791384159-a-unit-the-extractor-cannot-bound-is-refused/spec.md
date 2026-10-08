# Feature Specification: a unit the extractor cannot bound is refused (#870, #848)

<!-- seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* — "the major level is the enclosing unit", "an anchor degrades to `DRIFTED`, never to `BROKEN`. Only the major level can be broken" | A span that leaves a unit's body out is not the enclosing unit. Refusing it is `BROKEN` at the one level `BROKEN` is allowed, and it is never an `ok` read over lines nobody hashed |
| `docs/the-evidence-ledger.md` §*What the checker refuses, and what it says while refusing* | The refusal is a sentence a person reads: why the unit cannot be bounded, and which anchor to use instead |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* — "A BROKEN coordinate. Only where a released row carries it under the freeze does `--reverify` name it, with the `Corrected ·` repair, and exit 1" | What an installer with `Ledger frozen from` sees for a released row the new rule refuses: the repair already exists, and this work adds no second one |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a reader of more shapes and a refusal with a remedy on the line, the refusal is the one that never reads `ok` over code nobody re-read |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The stop cost is measured before the change ships (`questions.md` Q2, Q3), and the change names what it removes |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | This work writes `changelog.md` and `seal/ledger/<work-item-id>.md` in its own directory and edits no released file |
| `skills/evidence-check/SKILL.md` §*Resolving a unit without a parser*, §*What the region is*, §*Known limits* | The sentences this work rewrites: the indentation bound "lands on the closing brace in a brace language", and "a language-aware rule for what closes a block is the per-language parser this deliberately does not have" |
| #834's `spec.md` §*What the table says* (`origin/chore/834-every-reader-and-record-is-inventoried:seal/specs/1791382684-every-reader-and-record-is-inventoried/spec.md`) | The direction: prefer an owned or observed input that refuses the unknown over a guess that reads more shapes; name the input class of every reader; name what the change removes |

## Scope

**What is wrong, in one paragraph.** Every file that is not `.py` or `.md`
goes through one rule, `skills/evidence-check/scripts/evidence_check.py#generic_units`:
a declaration line, then every line until the next line at the same or lower
indentation. In a brace language the indentation is formatting, not
structure, and the rule ends the unit at the first line a formatter puts back
at the declaration's indent. That line is `): number {` for every multi-line
TypeScript signature Prettier writes (#848, executed: the span is lines 1–2
of a 5-line function), the `{` of an Allman-style C function (executed: the
span is the signature line alone), and `):` of a multi-line Python `def`
when the running interpreter cannot parse the file and `py_spans` falls
through to the same rule (executed: lines 1–3 of a 5-line function). In each
case the body is outside the hash, so a rewrite of the body reads `ok`, and
`--reverify` cannot notice because the hash it would write is the one already
there. The same direction shows in YAML: `on:` followed by `- push` at the
key's own indent bounds to the key line alone (executed), and the items are
outside the hash.

**In.**

1. **One bounding rule per suffix, in one table.** `resolve_unit`,
   `minor_region`, `file_units` and `content_matches` each test the suffix
   on their own today (inventory E16, four dispatches). One function answers
   which rule bounds a file, and the four read it. Its rows:

   | Suffix | Rule | Input class (the shape #835 asks for) | What it refuses |
   |---|---|---|---|
   | `.py`, `.pyi` | `ast` spans, as today | observed — the interpreter's own parse | a file the running interpreter cannot parse: `BROKEN`, naming the interpreter version. **No fall-through to any text rule.** |
   | `.md` | heading path, as today | owned locator over a person's document | zero or several matches, as today |
   | the brace list (below) | the bracket walk | a guess over an allow-listed language family, refusing what it cannot balance or lex to end of file | an unbalanced or unlexable file: `BROKEN`, saying so |
   | `.yml`, `.yaml` | the block rule: the line and every following line deeper than it, plus a `- ` item at the key's own indent | observed — YAML's block structure is its indentation | nothing new; a key with no node is a one-line span, as today |
   | any other suffix, and no suffix | none | — | a bare-symbol locator: `BROKEN`, "no bounding rule for `.rb`; anchor a quoted line instead" |

   A quoted locator (`path#"…"`) resolves by `text_regions` in every file as
   today: the contiguous run of non-blank lines is a structure the file
   itself shows, so it needs no rule and is the remedy every refusal names.

2. **The bracket walk, for brace languages.** From the declaration line, the
   checker reads the file as a bracket stream with comments and string
   literals blanked (`//`, `/* */`, `"…"`, `'…'`, `` `…` `` and the forms Q1
   adds per language). The unit ends at the first line whose end has every
   bracket opened since the declaration closed and whose next non-blank line
   is neither deeper than the declaration nor an opening `{`. That one
   sentence bounds the #848 shape (the `(` stays open across the parameter
   lines, then the `{` opens the body), the Allman shape (the parameter list
   closes on the signature line and the next line opens with `{`), a
   constant whose value continues on deeper-indented lines, and a one-line
   signature exactly as today. **The last line is left out of the span when,
   lexed, it holds nothing but closing brackets, `;` and `,`** — a closer
   carries no claim, and leaving it out keeps the hash of every row the old
   rule bounded right. That is what makes every `DRIFTED` an installer meets
   on upgrade a body the old span left out, with nothing in the same wave to
   re-stamp blind. Where the walk reaches end of file with a bracket open, or
   closes one nobody opened, or a string or comment never ends, the unit is
   refused.

   The brace list on day one is the languages the inventory's probe and #848
   named, and no more: `.ts .tsx .js .jsx .mjs .cjs .c .h .cc .cpp .hpp .cs
   .java .kt .kts .swift .go .rs`. A language joins the list only with the
   string and comment forms the walk blanks for it written down and a case
   for each (Q1).

3. **Python refuses, never guesses.** `resolve_unit` falls through to the
   text rule today when `py_spans` returns `None`. A `.py` file the
   interpreter cannot parse is `BROKEN` for every bare-symbol row citing it,
   with a line naming the interpreter version and the `SyntaxError`'s line,
   so a reader can tell a grammar mismatch from a missing file.

4. **The refusal is one reading, carried to every caller.** `judge` grades it
   `BROKEN` with the reason and the remedy on the line; `--reverify` writes
   nothing onto it and prints its line, as it does for every `BROKEN` row
   (`SKILL.md` §*Known limits*: "Silence there reads as a heal that
   happened"); `.github/scripts/rider_check.py#region_lines` and
   `skills/code-review/scripts/survivor_check.py`'s `resolves` read the same
   answer from `resolve_unit` and never a second reading of their own. A
   refused suffix yields no units to `file_units`, so the rename scan and
   `--migrate` name nothing there.

5. **What this removes.** The indentation bound for brace languages; the
   second spelling of the opener regex at `file_units` (inventory E18,
   L943), which now reads `generic_units`'s; the `SyntaxError` fall-through
   and its comment in `resolve_unit`; three of the four suffix dispatches;
   and three sentences a person reads — `SKILL.md`'s "lands on the closing
   brace in a brace language, because the brace sits at the declaration's
   own indent", the Known-limits bullet "a language-aware rule for what
   closes a block is the per-language parser this deliberately does not
   have", and the region table's row "a symbol elsewhere".

6. **What a person reads changes, so the documents and the pins change with
   it** (agent-contract §14): `SKILL.md` §*Resolving a unit without a
   parser*, §*What the region is*, §*Verdicts and what to do*'s `BROKEN` row
   and §*Known limits*; one paragraph under `docs/the-evidence-ledger.md`
   §*What the checker refuses, and what it says while refusing* with its
   `Enforced by:` line; this work item's `changelog.md` with the paragraph
   an installer needs (below); and the `generic_units`, `resolve_unit` and
   `file_units` docstrings stating their input class in #835's three words.

**Out, and why.**

- **Declaration shapes the opener never matched** — Go receiver methods
  `func (s *S) Name(`, generics `fn f<T>(` and `List<String> f(`, typed
  constants `let x: T = …` (the `:` with a modifier before the name is
  skipped on purpose), and `Class.method` outside `.py`. All read `BROKEN`
  today (inventory E17, probe executed), which is the loud direction; a
  quoted-line anchor works for each. Reading them would be a reader of more
  shapes, the design #834's table says did not converge. The caller may file
  them as one issue.
- **Shell, Ruby, Lua, Elixir, Haskell, TOML, JSON, `.cmd`, and files with
  no suffix** (`bin/*` here). Shell's `case` patterns close a `)` nobody
  opened and a heredoc carries anything; `end`-keyword languages have no
  bracket structure. Their bare symbols are refused with the remedy; their
  quoted lines resolve as today. This repository's own ledger cites none of
  them by bare symbol (measured: 24 `.yml` rows, 17 quoted and 7 bare; one
  `.cmd` row, quoted; nothing else outside `.py` and `.md`).
- **`.markdown` and `.mdx` on the heading rule** (inventory E16). They were
  never on it — a quoted heading there resolves as a paragraph today — so
  refusing their bare symbols changes no reading that was right.
- **The call-or-declaration judgment** (`STATEMENT_WORDS`, the resurrection
  flag, `bare_one_liner`). It decides which line declares; this work decides
  where the unit ends. The flag's consumers are untouched.
- **#867's readers** (`heading_level`, `ANCHOR_RE`, the config rows) and
  **#836's evidence** (what a row's claim is). The seams are in `plan.md`.
- **A per-language parser dependency.** `evidence-ci` vendors
  `evidence_check.py` alone, stdlib only, into a consumer's `tools/`; a
  dependency there is a second file to vendor and a grammar per language to
  version.

**What an installer sees on upgrade, and how the release says so.** The
plugin's commit hook `hooks/evidence-advisor.py` imports the checker by path,
so a plugin update reads the installer's ledger with the new rule at the next
commit; the CI copy under `tools/` changes only when `/specseal:evidence-ci`
is re-run (`skills/evidence-ci/SKILL.md` §*Updating later*). At either
moment: a row citing a brace-language unit whose body the old span left out
reads `DRIFTED` once, and the right act is to re-read that unit and then
`--reverify`, not to re-stamp blind; a row citing a bare symbol in a suffix
with no rule, or in a `.py` the interpreter cannot parse, reads `BROKEN` with
the remedy on its line, and under a freeze `--reverify` names the `Corrected
·` repair and exits 1; every other row keeps its hash and its verdict. The
work item's `changelog.md` carries this paragraph under `### Changed`, the
release gathers it into `changelog/0.21.0.md` and the GitHub Release, and
`SKILL.md` §*Known limits* keeps the day-one brace list where an installer
looks for it.

## User scenarios & acceptance *(mandatory)*

Each case is shown red against the tree before it is planted (agent-contract
§15), and the hand-back says how. Spans are 1-based and inclusive.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 #848's shape | Given `f.ts` holding `export function multiLine(` / `  opts: { a: number },` / `): number {` / `  return opts.a + 1` / `}`, when the row cites `f.ts#multiLine`, then the span is lines 1–4 and a body-only edit reads `DRIFTED` under `--strict` | the test case; #848's own reproduction script as a test, run against the tree |
| S2 one-line signatures keep their hash | Given the `BRACE` fixture of `tests/test_a_row_points_by_content.py`, when `handler`, `Box` and `open` resolve, then the spans are (3,8), (11,14), (12,13) as today, and `svc.js#handler`'s (4,5) too | the existing cases, unchanged |
| S3 Allman braces | Given `int add(int x)` / `{` / `  return x + 1;` / `}`, when `f.c#add` resolves, then the span is 1–3, not 1–1 | the test case |
| S4 an unbalanced file is refused | Given a `.ts` whose declaration opens a `{` that no line closes, or a line that closes one nobody opened, when a row cites its unit, then `BROKEN` with a line saying the walk could not bound it and naming the quoted-line remedy; `--reverify` writes nothing and prints the line | the test case, both readings |
| S5 no rule, no guess | Given `svc.rb` with `def render` / `  1` / `end`, when a row cites `svc.rb#render`, then `BROKEN` with "no bounding rule for `.rb`" and the remedy; when a row cites `svc.rb#"def render"`, then it resolves to the contiguous run as today | the test case |
| S6 Python refuses | Given a `.py` the running interpreter cannot parse that holds a multi-line `def f(` / `    a,` / `):` / `    return a`, when a row cites `#f`, then `BROKEN` naming the interpreter version and the error's line, and the hash of lines 1–2 is nowhere on the line; when the file parses, then nothing changes | the test case; the fixture carries one deliberate `SyntaxError` line |
| S7 YAML's compact sequence | Given `on:` / `- push` / `- pull_request` / `jobs:`, when a row cites `w.yml#on`, then the span is 1–3; and `.github/workflows/test.yml#pytest`, `#ledger` and `publish-release.yml#jobs` keep the spans they have today (executed 2026-10-07: 32–128, 146–164, 46–138) | the test case; `bin/evidence-check --strict .` on this branch reports no new `BROKEN` and no new `DRIFTED` against `main` |
| S8 one reading reaches every caller | Given a refused unit, when `rider_check.py` reads a rider anchored on it and `survivor_check.py` asks whether it resolves, then each gets the refusal from `resolve_unit` and neither re-derives it | `tests/test_a_rider_reaches_its_file.py`; a case that counts `resolve_unit`'s callers, as `test_judge_asks_resolve_unit…` does today at `tests/test_a_row_points_by_content.py:2883` |
| S9 one opener | Given `file_units` and `generic_units`, when the opener regex is searched for, then it is spelled once | a case that reads the module's source for the regex, or the one-word-one-meaning style of pin already in the suite |
| S10 one suffix table | Given the four units that dispatched on suffix, when `.endswith(".py")`/`(".md")` is searched for in the resolution path, then the table is the one place | a source-reading case over `resolve_unit`, `minor_region`, `file_units`, `content_matches` |
| S11 the documents say what the code does | Given `SKILL.md` and `docs/the-evidence-ledger.md`, when the sentences in *In* 5 are searched for, then they are gone, and the new paragraph carries an `Enforced by:` naming S1 and S5's cases | `tests/test_a_record_states_what_the_tree_has.py` and the hygiene tests the brief names |
| S12 the installer paragraph exists | Given `seal/specs/<this>/changelog.md`, when it is read, then it says the three things an installer sees and what to run, under `### Changed`, with no `## ` line | the fragment, read |

## Data & interfaces

- `bounding_rule(path) -> "ast" | "heading" | "brace" | "block" | None`, the one
  suffix table. `None` is the refusal for a bare-symbol locator.
- `resolve_unit(path, locator, text)` carries three facts in one reading: the
  places, the resurrection flag, and the refusal's reason or `None`. Its
  three callers are `judge`, `rider_check.py#region_lines` and
  `survivor_check.py`'s `resolves`; all three are in this repository and
  change in the same commit. The shape is Q4.
- `generic_units(lines, name, rule)` takes the rule that bounds the file
  (`"brace"` or `"block"`) and no longer infers it. The call-or-declaration
  half (the opener, `STATEMENT_WORDS`, `bare_one_liner`, the resurrection) is
  unchanged.
- The lexed bracket stream is memoised per distinct text, as `parsed_spans`
  is (`docs/the-evidence-ledger.md` §*What the checker refuses*, the
  one-parse paragraph), because a file many rows cite is walked once.
- Lines a person reads, pinned by a case each (§14): the `.rb` refusal, the
  unbalanced refusal, the Python refusal with its interpreter version.
- No change to `ANCHOR_RE`, the row grammar, the verdict vocabulary, the exit
  codes, `templates/evidence-check.yml`, or the vendored-copy test.

## Open questions → questions.md

Four rows: the brace list's per-language forms (the work), this repository's
stop cost (a measurement), a consuming repository's stop cost (a measurement),
and the shape `resolve_unit` returns (the work). None needs a person; the
head of `questions.md` lists what the tickets left open that the tree
answered.

Framed 2026-10-07 by framer, before the build.
