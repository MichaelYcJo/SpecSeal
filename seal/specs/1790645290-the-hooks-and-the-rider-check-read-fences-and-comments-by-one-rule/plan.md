# Implementation Plan: the hooks and the rider check read fences and comments by one rule (#667, #658)

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned, after the owner answered Q1 (a).

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Three readers decide what a person declared or wrote: `hooks/config.py` (every
Bash call, through `mode-gate` and `broad-gate`), `hooks/routing.py` (every commit,
through the commit gate, and at the pull request through `chain_check.py`), and
`.github/scripts/rider_check.py`. Each gets one reading, held in one stdlib module
under `hooks/`:

- a line inside a **fenced code block** or a **line-start HTML comment block**
  that closes is hidden, by CommonMark's own block rules for those two;
- nothing inline is modelled, so a code span or a mid-line opener moves nothing;
- a line whose context the walk does not model keeps the reader's base reading;
- a construct that never closes is not a construct.

The oracle comes first. A CommonMark parser that shares nothing with the walk says
which lines a renderer hides, and a property test holds each reader to two
things: it never leaves both the base reading and the renderer's, and it equals
the renderer wherever it claims to be exact. `spec.md` §*The reading* carries the
rule and its grounds; this file carries the order and the alternatives.

## Technical context

Read on 2026-09-29 at `3911a8cf`.

- `hooks/config.py#FENCE`, `#fence_map`, `#unfenced`, `#config_rows`, `#refusal`,
  `#refused_row`, `#declared_mode`. `fence_map` is the fence walk and `unfenced` its
  surviving lines. All three table walks read through `unfenced`, the third being
  `skills/implement/scripts/seal.py#table_span`. `seal.py#write_row`'s read-back
  guard asks `fence_map` for an unclosed fence to name.
- `skills/verify/scripts/broad_gate.py#fenced_row_at`, `#fenced_row`,
  `#fence_left_open`, `#missing_row`. `fenced_row_at` takes the complement of
  `unfenced`, so once comments are hidden too, that complement holds commented lines
  and the sentence "inside a code fence" would be wrong for them. It has to ask the
  walk which kind a line is.
- `hooks/routing.py#table_rows` reads every line that starts with `|` and has two
  cells, and `#parse` builds a `dict`, so the last row of a label wins.
  `sys.path.insert(0, <its own directory>)` is already its first act.
- `.github/scripts/rider_check.py#comment_blocks`: a block opens at a marker line
  whose stripped head is `<!--` (or `#` outside markdown), runs to `-->` or the next
  marker, and carries `in_html` across a block that ended at a second marker.
  `#region_lines` hashes the region with every block cut out.
- `skills/verify/scripts/unverified_check.py#fence_opener`, `#fence_closes`,
  `#fence_spans`: the delimiter rule. `tests/test_unverified_rows_close.py#test_the_fence_rule_agrees_with_the_config_reader`
  holds `hooks/config.py`'s copy to it over `FENCE_SHAPES`, and
  `#fenced_by_the_shared_rule` is exactly `hooks/config.py`'s base reading.
- `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` is a
  hand-written reference reading for `live_lines`. It models every `<!--` as inline
  raw HTML (it cites CommonMark 6.6), which is the wrong model for a comment block
  and one reason it is not the oracle here.
- `.github/scripts/run_tests.py#PACKAGES` is `("pytest", "pytest-xdist")`, and
  `#add_xdist` adds the second to a `.venv` it adopts. `.github/workflows/test.yml`
  runs `pip install pytest pytest-xdist` on three platforms at 3.12.
- 26 committed `routing.md` files and the template, none with a fence line, a
  mid-line `<!--`, an indented `<!--`, an unbalanced comment, or a pipe-line inside
  a comment. 8 of the 26 have no comment above the table. One line in
  `templates/sdd-routing.md` (the `<One or two sentences.` placeholder, below the
  table) begins with `<` and a letter. No markdown file under `RIDER_ROOTS` carries
  a rider. Read with `git grep`, `grep -c` and `awk`, not with the walk.

**What breaks in six months.** Somebody widens what the walk calls exact, say to
fences indented under a list item, without a generated document that holds a list.
The property test is only as good as its corpus, so the corpus's alphabet has to
hold every context the uncertainty table names, and a new widening has to add the
context it is about. The second failure is the oracle moving under the suite, and
the pin is what stops it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Chosen:** two block constructs by CommonMark's block rules, no inline state, the base reading wherever the walk is not exact, a construct that never closes is not one, checked by an independent parser | A context the uncertainty table misses is called exact. Half 2 of the property then disagrees with the oracle on a generated document, which is a red case and not a shipped defect, provided the corpus holds that context | Chosen. It is the only reading here that states in advance which lines it may change, and every line it changes is one the renderer agrees with |
| Fence first, then an inline-aware comment half (`1790635413` phases 6 and 8) | A fence line inside a comment above the table opens a fence that hides the declaration (round 2, 🟡 2). Code-span delimiters either side of the table hide it (round 1, 🟡 3) | Rejected, by execution in two rounds |
| Comment first, with code spans (`1790635413`'s round 2 fix) | An unclosed opener switches off every fence below it, so a fenced example answers (round 3, 🟡 1). A prose opener loses a rider (round 3, 🟡 2) | Rejected, by execution in round 3 |
| A fence-only rule in the hooks, as #658 proposes: adopt `fence_opener` / `fence_closes` and nothing else | `templates/sdd-routing.md`, 18 of the 26 committed `routing.md` files and `seal/config.md` open with a header comment above the table, and `seal.py`'s `NEW_CONFIG` writes one. A fence line inside that comment opens a fence that hides the table (round 2's shape). A version that stops being sure at the first comment reaches none of those files | Rejected. The hooks need comment state, but only the block kind |
| The hooks load `unverified_check.py#live_lines` by path | A hook would import a skill module on every Bash call (`hooks/config.py`'s docstring; `fence_opener`'s hook-path paragraph). `live_lines` also parks a line it is unsure of, which is a marker's safe direction and a hook's first failure direction: a `<!--` in prose that never closes parks every row below it, the live table included | Rejected |
| A construct that never closes runs to the end of the file in every reader, as CommonMark and `1790635413`'s routing and rider rules have it | A stray fence line above a routing table makes the gate ask where the base read a declaration. A lone backtick and a fence line above a rider lose the rider (round 3's `lone` flip) | Rejected: the first direction, twice. `hooks/config.py` keeps it because its base already does |
| Refuse loudly on an unclosed construct, as `1790635413`'s phase 9 made the release scripts do | `mode-gate` and the commit gate would stop a run on a file the base read. The release scripts refuse because they write the very text their own reader then reads; no reader here writes what it reads except `seal.py#write_row`, whose read-back guard already refuses | Rejected. No shape here needs a refusal: the base reading is always available and is the floor |
| A certain inline-comment rule, so a row inside a mid-paragraph comment is hidden too | Being sure needs the paragraph's extent and every code span in it, which is the ground all three rounds lost on. The base reads such a row, so leaving it is not worse | Rejected for this item; `spec.md` §*Scope* names the residual and its answerer |
| Oracle: a second hand-written reading, like `a_reading_from_the_commonmark_rules` or `1790635413`'s `hidden_by_the_shared_rule` | It shares a model with what it checks. Round 3: "The oracle cannot catch this, because it is built the same way" | Rejected |
| Oracle: the CommonMark specification's own examples for §4.5 and §4.6, vendored as data | Each rule is exercised once, and no example combines a stray opener, a fence and a comment, which is the kind of shape every round found. Its licence has not been read here | The fallback if Q1 is answered (b) |
| Keep the walk inside `hooks/config.py` and let `routing.py` and `rider_check.py` import that | Works. But `config.py` is the reader of one file's table, and the rider check would load a config reader to learn where a fence is | Rejected for the module's home, not for correctness |
| A copy of the walk in each reader, held by a parity test | Three copies of a rule is how the old readers came to disagree. `hooks/routing.py`'s docstring: "divergent copies is how half of them keep the old answer" | Rejected. Skills already load `hooks/config.py` and `hooks/routing.py` by path, so one module reaches every reader |

## Phases

Each phase is a vertical slice. Phases 3, 4 and 5 are independent of each other
once phase 2 lands.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The oracle, before any reader moves.** `markdown-it-py`, pinned to one version, as a test-only dependency: `.github/scripts/run_tests.py#PACKAGES`, an adopted `.venv` given it the way `#add_xdist` gives pytest-xdist, `.github/workflows/test.yml`'s install line, and `CONTRIBUTING.md` §*Running the checks*. A helper in `tests/` that says from the parser's tokens alone which lines a renderer hides: inside a fence, an indented code block, an HTML block, or an inline HTML comment. The shape table's *Renderer* column, checked against it (Q2). Waits on Q1; under Q1 (b) the helper is built over the vendored examples instead | the helper's cases over every shape in `spec.md` §*The shapes*; an assertion that the helper imports nothing from `hooks/`, `skills/` or `.github/scripts/`; where the oracle disagrees with the frame's *Renderer* column, the column is corrected in `overview.md` and the expected answer re-derived by `spec.md`'s rule | 3f37cecb |
| 2 | **The walk, with no reader on it yet.** A stdlib-only module under `hooks/`: fenced blocks and line-start comment blocks in one pass, closed only; the uncertainty mask for every context in `spec.md`'s table; the unclosed-fence opener it saw. The delimiter copy moves here from `hooks/config.py#FENCE`, or is read from there (Q5), and `unverified_check.py#fence_opener`'s docstring says where it lives. Property half 2: on the shape table and a seeded generated corpus, every line the walk calls exact is classed as the oracle classes it | the property case, seen red twice (§15): with the comment-block rule removed, and with a mid-line `<!--` allowed to open a comment; S3's parity case still green | |
| 3 | **The config reader on the walk.** `config_rows`, `refusal`, `unfenced` and `fence_map` read through it, with the fence-only reading on uncertain lines, so `seal.py#table_span` and `broad_gate.py` follow without a walk of their own. `broad_gate.py` tells a `Broad gate` line hidden in a comment from one in a fence, in a new sentence documented in `templates/config.md` and pinned; `#fence_left_open` and `seal.py#write_row`'s guard name only a fence the walk sees. `seal.py#HOOK_PURPOSES` and the copied-alone cases gain the new module. Property half 1 for this reader | C1 to C14, each marked red failing against `3911a8cf`'s `hooks/config.py`; S6, S7, S8, S15; the property case; S14's corpus measurement in the phase record | |
| 4 | **The routing reader on the walk.** `table_rows` skips the lines the walk hides and reads every other line as today. Its docstring and `parse`'s state the reading, and that R2 and R9 read as no declaration | R1 to R9, each marked red failing against `3911a8cf`'s `hooks/routing.py`; the property case for this reader; R10's measurement over the 26 committed files and the template, in the phase record | |
| 5 | **The rider check on the walk.** In a `.md` file, a marker line the walk places inside a fence that closes opens no rider and changes no `in_html` state. `#region_lines` follows through `comment_blocks`. Other file types unchanged | K1 to K7, each marked red failing against `3911a8cf`'s `rider_check.py`; K8's measurement over `RIDER_ROOTS`, in the phase record | |

Each phase writes its own rows into
`seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md`,
re-reads the existing rows its edit drifts where they live (`spec.md`
§*Data & interfaces* lists them), and adds its line to this work item's
`changelog.md`.

## Operational impact

- **A new test dependency**, if Q1 is answered (a): `markdown-it-py` and whatever it
  pulls in, pinned, installed by `bin/test` and by CI. The gates stay stdlib-only
  and a plugin user installs nothing new.
- **A new module under `hooks/`**, shipped with the plugin like `optin.py`. No
  change to `hooks/hooks.json`, no new hook, no new config row.
- **What reads differently in a repository that installs the plugin.** A
  `routing.md` or `config.md` row inside a fenced block or a line-start comment
  that closes is no longer read. A config table below a closed comment that quotes a
  fence line is now read where it was not. Everything else reads as before,
  including every file with a fence or comment that never closes.
- **Merge order.** #663 and #660 touch the same files (`spec.md` §*Data &
  interfaces*). Whichever lands first, the conflict is resolved hunk by hunk (Q6).
