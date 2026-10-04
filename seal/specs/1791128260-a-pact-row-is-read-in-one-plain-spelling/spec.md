# Feature Specification: a pact row is read in one plain spelling (#759, redesigned)

<!-- seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#759. A `| Pact notify | always |` row that `seal/config.md` holds where
`hooks/config.py#config_rows` does not take it is read as the default,
`when the pact is touched`. Under `always`, `evidence-check --reverify` then
re-stamps a moved ledger row citing no clause and records no pact change,
and the re-stamp clears the drift that was the only trigger for the record.

The first work item for #759 (`1791119073-a-pact-row-outside-the-config-table-is-refused`,
PR #784) closed this by emulating what GFM renders as a pact item and holding
the emulation to cmark-gfm. Four review rounds each found spellings the
emulation missed, and the 3+ fix rule stopped it. **On 2026-10-05 the owner
chose the other shape: a pact row is read in one plain spelling, and any
other line that names a pact is refused.** That is the shape the 0.18.1
redesign of #739 took: one exact accepted shape, and everything else read
the conservative way. This work item builds that, and models no part of GFM.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-pact.md` §*How a signatory names the pact* | One reader answers both rows for every caller. A value that will not parse, or a row written twice, "has no value at all". A line naming a pact in any other spelling joins that list |
| `docs/the-pact.md` §*What this does not see*, the vendored paragraph (work item 1791076833) | A copy with no `hooks/` re-stamps a moved row citing no clause only where nothing in `seal/config.md` can make `Pact notify` mean `always`. After this work it reads the same lines by the same constant |
| `docs/the-pact.md` §*A signatory records a pact change* | The writer leaves a row (`LEFT`, exit 1) where the declaration will not read. `evidence_check.py#record_pact_changes` already does this for any refusal with `notify` None. This work only has to produce that state |
| `templates/config.md` §*Pact* | "A row that will not parse is refused in a sentence, never read as absent." This work says which spelling parses, and that every other line naming a pact is refused |
| `hooks/config.py#config_rows` docstring (#82 rounds 1 and 2), `#unfenced` (#429, #667) | The walk and its stop rule do not move. The walk is the one place a pact value is read from. Its fence and comment rule stays the walk's, and the new refusal does not consult it |
| `hooks/config.py#declared_pacts` docstring (round 1 of #647, white 5) | The pact reader is the one reader in this module that refuses rather than failing silent, on purpose. A refusal here is the designed loud state, not a new one |
| `tests/test_every_reader_ends_a_line_where_gfm_does.py` (#664) | Every `.splitlines(` in a reader unit has a census entry with its reason. A new one in a new unit takes reason `F`, as #784's did |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class by construction; pin every sentence a person reads; see each new case red |
| Owner's decision, 2026-10-05, recorded in `routing.md` §*Why this way* | One plain spelling is read, and any other pact-shaped line refuses. Prefer refusing loudly over modelling |

## The rule, decided by construction

### What is read: one plain spelling

**A pact row is a row `config_rows` takes whose item is exactly `Pact` or
exactly `Pact notify`.** "Exactly" is byte equality after the walk's own
handling of the cell, and nothing else:

- **Case.** `Pact`, capital P, the rest lower case. `pact notify`, `PACT`
  and `Pact Notify` are other spellings.
- **Inside the item.** `Pact notify` has one U+0020 between the words. Two
  spaces, a tab, a no-break space or any other character there is another
  spelling.
- **Around the item.** Whatever `CONFIG_ROW`'s `\s*` and the walk's
  `.strip()` take is taken, as today. A no-break space beside a pipe is read
  as today, because the walk then reads the right item and its value is
  honoured. Nothing is read as the default that way, so there is nothing to
  refuse.
- **The pipes and the place.** The walk's grammar, unchanged: a pipe at
  column 0, two cells, a closing pipe, in the first `| Item | Value |` table,
  before the walk's stop. Indentation, a block quote, a missing leading or
  closing pipe and a third cell are each a line the walk does not take.
- **The value.** Unchanged. `Pact` is split on `;` and each entry
  normalised; `Pact notify` is space-collapsed and lower-cased and checked
  against the vocabulary, as `pact_declaration` does today. One spelling is
  about the item. A value outside the vocabulary is already refused.

### What is refused: every other line that names a pact

**`pact_declaration` refuses each line of `seal/config.md` that names a pact
and is not a pact row read in the plain spelling.** The unit of the scan is a
line as `hooks/blocks.py#gfm_lines` cuts the file (`\n`, `\r\n`, `\r`).
That cut is already pinned to GFM's line endings by #664, and it is the
coarsest cut any reader here uses, so a word can only be whole on it where it
is whole on a finer one. Each line falls in exactly one of two cases:

1. **A line the walk took as a row.** The line holds no character
   `str.splitlines` ends a line at, and the walk took it whole. Only its
   **item** is read. An item that is exactly `Pact` or `Pact notify` is the
   plain spelling and is not refused. Any other item that names a pact is
   refused: `pact notify`, `` `Pact notify` ``, `**Pact**`, `Pact\|notify`,
   `Pact<U+200B>notify`. The value is not read, so `| Broad gate | bin/test
   -k pact |` and `| Reference specs | docs/pact |` stay silent.
2. **Every other line.** The whole line is read, and it is refused where it
   names a pact **and** holds a `|`. This covers a line the walk never
   reaches, a line in a fence or a comment, a line in a second table, and a
   line with a `str.splitlines`-only character in it, even where each of its
   pieces would be a plain row.

**A line names a pact** where the constant `PACT_WORD` finds the word in the
line as written, or in the line decoded. The decoded line is
`unicodedata.normalize("NFKC", html.unescape(line))`, two standard-library
calls and no grammar.

- `PACT_WORD` is the letters `p`, `a`, `c`, `t` in that order, any case,
  where any run of characters that are not letters may stand between two of
  them, and the `p` does not follow a letter. In Python:
  `re.compile(r"(?<![^\W\d_])p[\W\d_]*a[\W\d_]*c[\W\d_]*t", re.I)`.
- The look-behind is what keeps `impact` and `compact` silent.
- "Not letters between" is what reads markup, format characters, character
  references and code spans as nothing, without parsing any of them.
- Reading both the raw and the decoded line is a union, so the decode can
  only add refusals. `html.unescape` decodes more than CommonMark does (round
  4 of #784, yellow 3), and here that costs nothing: `Pact&notify` names a
  pact raw, whatever the decode makes of it.

**The `|` condition is the one structural exclusion, and it is not modelling.**
GFM separates a table row's cells by pipes. A line with no `|` is a single
cell at most, so it carries no value cell, and a pact row with no value is
the state the reader already reads (GFM spec §4.10, where a body line with no
pipe is one cell and the rest are inserted empty; `questions.md` Q2 measures
it against the cmark-gfm the suite pins). A `|` counts raw or decoded, again as a
union. Its cost, stated: a line that names a pact with no pipe in it, such as
`Pact notify: always` in prose, is read as nothing, which is what it is read
as today. Its gain: a signatory may write the word in a comment or a
paragraph of its own `seal/config.md` without being refused.

**Fences and HTML comments are read through.** A comment is not rendered and
a fence renders as code, so a pact row in either is an example to a person.
It is refused anyway, for two reasons:

- Exempting it would make the refusal depend on `hidden_lines`' fidelity to
  GFM's block grammar. That is the dependency this redesign exists to drop,
  and an unclosed fence there hides everything below it.
- Refusing it is the loud direction. The person deletes the example.

The walk still skips fenced and commented lines, unchanged, so a plain row in
a fence is never **read**. It is only refused.

**Refusing is not split by item.** #784 refused a stray `Pact notify` only
where a `Pact` value stood, because a notify row with no pact is ignored.
Telling a mangled notify line from a mangled `Pact` line needs the item read
through the markup, which is the modelling being dropped. A mangled `Pact`
line in a repository with no plain `Pact` row is the worse loss, because a
row citing that pact's clause is re-stamped with no record. So both refuse,
with or without a plain `Pact` row. A **plain** `Pact notify` row with no
`Pact` value is still ignored, as `templates/config.md` says.

**What a refusal does**, unchanged in every caller: `notify` is `None`.
`pacts` is what the plain `Pact` row parsed, or `[]`. One refusal sentence is
added per refused line. `record_pact_changes` leaves every moved row (`LEFT`,
exit 1), `pact-check` prints `REFUSED` and exits 2, and `chain-check` prints
a notice and its exit does not move.

### What this over-refuses, and what stays silent

Checked against everything that is, or is made into, a `seal/config.md`:

| Text | Read as a config by | Under this rule |
|---|---|---|
| This repository's `seal/config.md` | every reader | silent: no line names a pact (read) |
| The stub `seal mode` writes (`skills/implement/scripts/seal.py#NEW_CONFIG`) | every reader | silent: a comment and a `Mode` row (read) |
| The `## Broad gate` block `skills/config/SKILL.md` step 3 tells a session to copy below the live table (`templates/config.md` §*Broad gate* down to §*What is refused*) | every reader, once copied | silent: no word names a pact in it (read); S9 measures it |
| The two rows `skills/implement/orchestration.md` §*the pact* writes into a signatory, `Pact` and `Pact notify` as `when the pact is touched` | every reader | silent **where they are written into the table**. Written below copied prose, they are refused, where today they are silently not read. That is the defect closing, loudly |
| `templates/config.md` whole | **no code** reads it as a config (searched: every reader of `pact_declaration`, `declared_pacts` and `config_rows` takes `seal/config.md`; the tests read the template as text) | it would be refused: its `\| Row \| Value \| Absent \|` and `\| Value \| Recorded here \|` documentation tables name a pact with pipes. Nothing copies it whole, and a copy that did would be told which lines to remove. Its own first table, with `\| Pact \|  \|` and `\| Pact notify \|  \|`, is the plain spelling and silent |
| A fenced or commented example of a pact row, in a signatory's config | every reader | **refused** — the deliberate cost above |
| A walked non-pact row whose value names a pact | every reader | silent: only a walked row's item is read |
| `impact`, `compact`, `Impacted` anywhere | — | silent: the look-behind |
| A prose line or comment naming a pact with no `\|` | — | silent: the `\|` condition |
| A line naming a pact with a `\|`, in a repository that holds no pact | every reader | **refused**, and `--reverify` leaves every moved row until it is fixed. This is the price of not splitting by item, above. A repository that signs no pact has no reason to write such a line |

### What this does not catch, stated

**A letter that is not part of the word, put between its letters.** Examples
are a tag name in `P<b></b>act`, a link destination in `[P](x)act`, and an
undecoded entity name. Also a letter from another script that looks like a
Latin one, such as `Pаct` with U+0430. Catching them needs a grammar of the
markup or a confusables table, and both are modelling. None of them is a
spelling any round of #784 found. Each needs markup written inside a
four-letter word, or a deliberately different alphabet. A person who writes
`` `Pact notify` ``, `**Pact notify**`, `Pact<U+200B>notify` or
`[Pact notify](x)` is caught. `questions.md` Q1 puts this to the owner with
the default that it is documented and accepted.

## Scope

**In.**

1. `hooks/config.py`. `PACT_WORD`, a predicate that answers whether a line
   names a pact (raw or decoded, with the `|` condition), and the scan above
   inside `pact_declaration`. The scan needs the walk's line indices, so
   #784's `indexed_config_rows` is reused: `config_rows` becomes its
   projection, with byte-identical output. The refusal sentence names the
   line as written, with every whitespace character other than a space and
   every Cf character shown as `<U+XXXX>`. That rendering is #784's
   `stray_refusal`, reused. <!-- NAME NOT IN TREE: #784's, never ported -->
2. `skills/evidence-check/scripts/evidence_check.py#record_pact_changes`, the
   vendored branch (`config is None`). It uses the same constant, the same
   predicate and the same `gfm_lines` cut, held equal by a test. It has no
   walk, so it cannot tell the live table from any other line. It judges each
   line by the line's own shape instead (`CONFIG_ROW_RE`, already in the
   file). It is blind, and leaves a moved row citing no clause, where the
   file will not read, or where some line naming a pact with a `|` is
   neither:
   - a plain `| Pact | … |` row, nor
   - a plain `| Pact notify | … |` row,

   or where a plain `Pact` row and a plain `Pact notify` row both carry a
   value. Every vendored case on the base keeps its verdict (S12). The
   constant `NOTIFY_ROW_SHAPE` is replaced by `PACT_WORD`. A released ledger
   row cites `NOTIFY_ROW_SHAPE` (Data §*Ledger*).
3. **Delete** what #784 added and this replaces, wherever it reaches this
   branch: `PACT_ROW_SHAPE`, `shape_line` (both copies), `RAW_HTML`, <!-- NAME NOT IN TREE: #784's, never ported -->
   `TAG_END`, `_shaped_item`, `PACT_ITEMS`, the two-cut stray walk, and the <!-- NAME NOT IN TREE: #784's, never ported -->
   cmark-gfm oracle case. None of it is on the base (`94d7b2e0`), so in
   practice this means "do not port it". Port only what still holds:
   `indexed_config_rows`, the refusal rendering, the caller cases and the
   corpora.
4. The three callers change no code. Each gets an end-to-end case, as in
   #784: S6, S7, S8.
5. The documents, each sentence pinned (§14):
   - `docs/the-pact.md` §*How a signatory names the pact*: a new marked
     paragraph with its `Enforced by:` line.
   - `docs/the-pact.md` §*What this does not see*: the vendored paragraph's
     rule, and the stated blind side.
   - `templates/config.md` §*Pact*: the refused-row paragraph, and the
     `Absent` cell of `Pact notify`.
6. The regression corpus (S2) and the silent set (S4), generated from #784's
   generators. Round 4's spellings, which were never planted, are added from
   `rounds/round-4-report.md` on #784's branch.
7. Re-reads of the released ledger rows the change drifts, in this work
   item's fragment.

**Out.**

- **Every other `seal/config.md` row.** #784's spec §*The decision #759 left
  open: pact rows only* holds unchanged. No other reader's default destroys
  the evidence that would correct it, and the reasoning is not repeated here.
- **`config_rows`' stop rule and output**, and `unfenced` / `hidden_lines`.
  They are unchanged. The scan reads through what they hide.
- **`chain-check`'s and `pact-check`'s own wording around a refusal.** As in
  #784's spec §*Out*: the refusal sentence names the cause.
- **`evidence_check.py#vendored_config_rows`.** It reads `Ledger frozen from`
  alone.
- **The blind side above.** It is documented, not closed (Q1).
- **`templates/config.md` as a config.** Nothing reads it as one. It is not
  made silent, because that would need the code-span exemption that #784
  rounds 2–4 kept re-opening.

## User scenarios & acceptance *(mandatory)*

`URL` is `git@example.com:org/orders-api.git`. `CONFIG` is a table holding
`| Mode | shared |` and `| Pact | URL |`. "Refused" means `pact_declaration`
returns `notify` None and exactly one refusal per refused line, each the
sentence naming that line.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the plain spelling | `CONFIG` plus `\| Pact notify \| always \|` in the table. **Then** `notify == "always"`, no refusal. The same with the template's empty pair inside its table: `([], None, [])` | reader cases; they pass at the base and must keep passing |
| S2 the regression corpus | Every spelling of #784's generators, each as a row inside the table under `CONFIG` and again below a blank line. The generators are `STRAY_WAYS`, the S3 rows, `FORMAT_CHARACTERS` at three positions, `SPLITLINES_ONLY` inside a row, every member of `MARKUP` (`WRAPS` × items, `JOINS`, `SPLITS`) and the code-span rows. Add round 4's seven link spellings, `<!-->Pact notify<!-- -->`, `Pact&notify`, and the five backtick rows off the walk. **Then** each is refused | one parametrized case per generator. Each is seen red at the base, where every in-table and stray one reads the default |
| S3 no pact anywhere | No plain `Pact` row. A line naming a pact with a `\|` below the table, both `\| Pact \| URL \|` and `\| Pact notify \| always \|`. **Then** refused, `([], None, [sentence])`. A **plain** `\| Pact notify \| always \|` in the table with no `Pact` row: `([], None, [])`, as today | reader cases; the first is red at the base |
| S4 the silent set | Each of these, appended to `CONFIG`, gives no refusal and `notify` as the table says. Lines: `\| Broad gate \| bin/test -k pact \|` in the table; `impact` and `compact` in a piped prose line; `<!-- this repository signs the orders pact -->`; a prose line naming a pact with no pipe; a NBSP beside a pipe around a plain item. Files: this repository's `seal/config.md`; `NEW_CONFIG` filled with `Mode`; `NEW_CONFIG` plus the copied `## Broad gate` block | reader cases. The last three are read from the tree, not retyped |
| S5 read through | A plain `\| Pact notify \| always \|` in a closed fence, and in a closed HTML comment, below `CONFIG`. **Then** refused, and `notify` is None, not `always`: the walk still does not read it | reader cases; red at the base, where both are silent defaults |
| S6 the writer | `CONFIG`, a stray `\| Pact notify \| always \|` below a blank line, and a moved ledger row citing no clause. **When** `evidence-check --reverify --into …` runs. **Then** `LEFT` naming the refusal, exit 1, the ledger byte-identical, and no `seal/pact-changes/` | `tests/test_a_signatory_records_a_pact_change.py`; red at the base |
| S7 pact-check | S6's config at a signatory. **When** `pact-check` runs at the pact's repository. **Then** a `REFUSED` line carrying the sentence, and exit 2 | `tests/test_pact_check.py`; red at the base |
| S8 chain-check | S6's config. **When** `chain-check` runs. **Then** a notice carrying the sentence, and the exit unchanged | `tests/test_a_signatorys_ci_prints_its_pact.py`; red at the base |
| S9 the vendored copy | A copy with no `hooks/`. (a) Every S2 spelling under `CONFIG`: left, exit 1. (b) Every vendored case on the base keeps its verdict, including `\| Pact notify \| always \|` with no `Pact` row (re-stamps) and the template's empty pair (re-stamps) | the S2 corpus run through the vendored branch; red at the base for the corpus members its old shape misses; the base's vendored cases unchanged |
| S10 one rule | `hooks/config.py`'s and `evidence_check.py`'s `PACT_WORD` have equal `pattern` and `flags`. The two predicates answer equally on every S2 and S4 line | a case, seen red by editing either pattern or either predicate |
| S11 nothing else moves | Every existing case of the four pact modules, `tests/test_the_mode_question_is_asked_once.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` and the line-cut census passes, or is changed with its reason in the phase record (Q3) | those modules at the phase boundary |
| S12 the sentences | The refusal sentence, the new `docs/the-pact.md` paragraph, the vendored paragraph's rule and blind side, and `templates/config.md` §*Pact*'s refused-row sentence are each pinned | a pin per sentence, seen red with the sentence deleted |

## Data & interfaces

- **`hooks/config.py#pact_declaration(text)`** keeps `(pacts, notify,
  refusals)`. What is new: one refusal per refused line, in file order, after
  the doubled-`Pact` refusal and before the entry refusals. Where any
  line is refused, `notify` is None.
- **New names in `hooks/config.py`.** `PACT_WORD`; a predicate such as
  `names_a_pact(line)`; and `indexed_config_rows`, ported from #784, with
  `config_rows` as its projection. The scan's own unit name is the builder's.
  Its `.splitlines(` calls take a census entry, reason `F`.
- **The refusal sentence.** It names the line and says the one spelling.
  It reads after three prefixes: "a `Pact` row this CI does not verify: "
  in `chain-check`, `REFUSED <url> seal/config.md` in `pact-check`, and
  "the `Pact` rows will not read: " in the writer's `LEFT` line. So it opens
  lower-case with the quoted line and ends with no full stop. Read from
  `chain_check.py` and `pact_check.py` at the base. A text that fits all
  three:
  `` `<line>` names a pact and is not a `Pact` or `Pact notify` row in the one spelling read: write it as `| Pact | … |` or `| Pact notify | … |` inside the `| Item | Value |` table, or take it out of this file ``.
  The builder may reword it. S12 pins whatever ships.
- **`evidence_check.py`.** `PACT_WORD` and the predicate replace
  `NOTIFY_ROW_SHAPE`. The vendored branch reads `gfm_lines(said)`, which the
  file already has.
- **Ledger.** `seal/config.md` declares `Ledger frozen from`, so a released
  row is re-read in `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md`
  with `evidence-check --reverify --into … --checked <date>`. Rows citing the
  units this work edits, seen at framing (read):
  - `0.18.1.md`:168 C1 (`pact_declaration@d3dccc0e`, `record_pact_changes@42221904`,
    `NOTIFY_ROW_SHAPE@99e032de`);
  - `0.18.1.md`:170 and :201 (`templates/config.md#"## Pact"`, at hash 0fdeedac when framed);
  - `0.18.1.md`:175 (`record_pact_changes`);
  - `0.18.1.md`:228 (Re-read of P1, `pact_declaration`);
  - `0.18.0.md`:6 and :8;
  - the `config_rows` rows at `0.12.0.md`:105, `0.9.1.md`:120, `0.5.0.md`:107
    and :115, and `0.15.3.md`:13.

  **`NOTIFY_ROW_SHAPE` leaves the file.** So 168's coordinate on it is
  BROKEN, not drifted. The repair is the one `docs/the-evidence-ledger.md`
  §*A released row is read again in the branch's fragment* names for a unit
  that went away: a `Corrected ·` row re-pointing C1 at `PACT_WORD`. Write
  the exact repair `evidence-check` prints. `evidence-check` names the full
  drifted set at the build, and this list is what framing saw.
- **The sibling.** Work item E (PR #786) edits three places that border
  this work's:
  - `evidence_check.py#record_pact_changes`: its docstring and its `entries`
    loop. Not the vendored branch.
  - `docs/the-pact.md` §*A signatory records a pact change*. Not §*How a
    signatory names the pact* or §*What this does not see*.
  - `templates/config.md` §*Pact*'s `Pact notify decides` paragraph. Not
    the refused-row paragraph.

  Both items move `record_pact_changes`' hash, so whichever squashes second
  re-reads its rows again at the merged base. Neither edits the other's
  lines.

## Open questions → questions.md

One row only a person can answer (Q1, non-blocking, with its default). Two
measurement rows. One row for the work. The head of `questions.md` lists
what the tree decided, so nobody reopens it.

Framed 2026-10-05 by framer, before the build.
