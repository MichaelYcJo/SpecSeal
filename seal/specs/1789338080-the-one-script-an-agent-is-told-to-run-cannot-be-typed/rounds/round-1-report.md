# Round 1 — the one script an agent is told to run cannot be typed

Target `8208928` on `fix/318-the-one-script-an-agent-is-told-to-run-cannot-be-typed`,
base `release/v0.11.4`, 24 files. No earlier round exists, so nothing is
inherited and nothing is carried.

## Stage 1 — spec compliance

Every property `spec.md` §Scope §In states is met, and I measured each one
rather than reading the account for it.

- **The wrapper pair.** Both files ship, `bin/round-record` is `100755` in the
  tree and its twin `100644`, matching all eleven siblings. Both are modelled
  on `bin/survivor-check` line for line.
- **The two typed forms.** Both are respelled, and no third one was left
  behind: no line of any `.md` under `agents/`, `skills/` or `templates/` shows
  `round_record.py` followed by a flag.
- **One locator in each of the nine documents.** All nine carry *both*
  accepted forms, not one. I also checked the redness claim independently: at
  `release/v0.11.4` all nine answer `reachable` false, so the pin was red
  against every one of them before the sweep, as `plan.md` phase 3 and
  §15 say.
- **The scope fence holds.** `round_record.py` and `chain_check.py` are
  untouched. No argument, output or verdict belonging to #309, #339, #340,
  #321, #323, #341, #273 or #353 moved on this branch.
- **`seal/ledger.md` is hashes alone.** Normalising every eight-hex anchor hash
  to a constant makes the branch's copy byte-identical to the base's. Eleven
  lines changed, one hash each, seven distinct anchors. The claim in
  `overview.md` is true as written.

So stage 1 has no finding. The five below are stage 2, and four of them are
about the pin — the part of this change that is supposed to outlive it.

## The class pin cannot fail for one of the twelve scripts it enumerates

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:124`.
`reachable` accepts the bare command as a locator, and `command_name` derives
that command by turning underscores into hyphens. For
`skills/implement/scripts/seal.py` the command is the single word `seal` — and
this repository's prose is made of that word. CLAUDE.md has a rule about it
(*a thing more than one party can have is named with whose*) and
`tests/test_one_word_one_meaning.py` exists because of it.

**Executed**: `reachable` answers true for `seal.py` against `agents/warden.md`,
`templates/sdd-round.md` and `skills/verify/SKILL.md` as they stand, none of
which names the script at all. On the synthetic line *The sealer takes the
seal. `seal.py` writes nothing.* it also answers true.

No case is wrong today, because no shipped document names `seal.py`. What is
wrong is that the case is unfalsifiable: the day somebody writes `seal.py`
into an agent's definition with no locator, this pin reports that document as
covered and the reader goes looking exactly as the four segments did. The
whole argument for the general form over the targeted one — Q1, answered by
the owner — is that the pin sees the next instance. For one of the twelve it
cannot.

The fix is four lines and costs nothing today: a command name with no hyphen
in it cannot be told from English, so those scripts are reachable by path
only. **Executed**: under the proposed reader all thirteen document/script
pairs stay green and the synthetic `seal.py` line goes red.

## The pin generalises two of the four assertions its model makes, not four

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:211`.
`plan.md` §*Where the wrapper pairs are pinned today* names
`tests/test_unverified_rows_close.py::test_the_wrapper_is_present_and_executable`
as *the four-assertion form (file, twin, exec bit, target exists)* and says
phase 3's pin *generalises it across the class*. The case asserts the file and
the twin. The executable bit is not asked.

**Executed**: the executable-bit assertion appears in four test modules, each
asking it of its own wrapper — `deferral-check`, `evidence-check`,
`round-record`, `unverified-check`. The other eight pairs have nobody asking.
All twelve are
`100755` in the tree today, so nothing is broken; a thirteenth committed
`100644` would satisfy this pin, resolve on PATH, and refuse with a permission
error.

`spec.md` §In item 4 only asks for *a `bin/` wrapper pair*, so the smith can
answer this with the spec rather than fix it. I am raising it because the
plan's own sentence promises the four and the branch delivers two, and one
extra assertion closes the gap.

## The classification's stated premise is wider than the property it asserts

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` says
`chain_check.py` is *named in four shipped documents and invoked in none of
them*. What `command_forms` actually asks is narrower and the file says so:
the script name followed by whitespace and a dash. A flag.

`templates/config.md:165` reads:

> The plugin's own checks (`evidence-check`, `unverified-check`,
> `chain_check.py`, `survivor-check`) follow it and are not part of the row.

That is a list of four things the sealer runs after the broad gate. Three are
bare commands a reader can type and the fourth is a filename. No flag follows
it, so the detector cannot see it — and it is in a template a user copies into
their own repository, which is the one document here with a reader outside an
agent. `docs/release-checklist.md:110` already shows the script as a bare
hyphenated command with a flag, for a name no wrapper answers to; that file is
out of scope by the spec and I am not raising it, but it is evidence that
*nobody is told to type it* is already less true than the classification
states.

Two repairs and they are not the same size. Narrowing the sentence to what is
asserted is in scope and changes nothing a user sees. Giving that line the
script's path is the honest locator and is the user-facing template change
`spec.md` §Out deliberately refused, so it is the owner's call rather than the
smith's.

## The warden's own definition names the script 48 lines before it says where it is

`agents/warden.md:138`. The locator landed at line 186. The document's first
mention is at 138, and there is a second at 182 — so a warden reading
top-down meets `round_record.py new` twice before anything tells it the file
exists.

`questions.md` Q4 answers *one reachable form per document, attached to or
beside its first mention*. `phases/phase-3.md` and `overview.md` both record
the divergence as the locator moving *one sentence later* in three files. For
`skills/implement/SKILL.md` and `templates/sdd-phase.md` that is fair. For
`agents/warden.md` it is 48 lines and two mentions, and the record does not
say so.

This matters more here than anywhere else in the sweep: three of the four
segments in the incident were `warden`, and this is the file they were reading.
The property `spec.md` asks for — at least once — is met, so this is fix or
justify rather than a spec failure.

The reason the locator could not go at 138 is real:
`tests/test_the_rules_have_one_owner.py:568` pins the substring
*`round_record.py new` copies it into the row of the same name*. It ends
before the word *in*, so a clause appended after `round-N.md` leaves it whole.
The fix below does that and stays inside the 88 columns
`tests/test_docs_line_wrap.py` holds this file to.

## A sentence this branch added names two rows where there is one

`skills/implement/SKILL.md:521` reads *The generator both rows name is …*. The
table above it has three rows. One of them, `round-N.md`, names the generator
(twice, as `round_record.py new` and `close`). The other two name the review
orchestrator. Under the other available reading — the two rows the implementer
acts on — neither names the generator either.

The locator itself is correct and reachable, so nothing breaks. It is a wrong
claim about the document's own structure, added by a branch whose subject is
agents drawing conclusions from what these documents say.

## Two corrections

**The invoker count in `NO_WRAPPER` is short.**
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` says
*All three places that DO invoke it*. Two more do:
`skills/verify/scripts/broad_gate.py:130` and
`skills/code-review/scripts/round_record.py:207` each build the path and run
it. Both carry the full path, so the substance — *reachable everywhere it is
reached* — holds; only the count is wrong, and it is a count a future reader
would use to decide whether to wrap.

**`seal/ledger.md`'s `Checked` column.** Eleven rows were re-read and
re-stamped and their dates did not move. This is disclosed in `overview.md`
§Not done and filed as #387, and its location is the shared ledger, so it is a
correction rather than a fix to commission.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The locator rule cannot fail for `seal.py`: its command name is the bare word `seal`, which every document in this repository contains | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:124` | open | **Executed** 2026-09-14: `reachable` answers true for `seal.py` against three documents that never name it, and against a synthetic line carrying no locator. No document names `seal.py` today, so no case is wrong — the case is unfalsifiable, which is what Q1's general form was chosen to prevent |
| 🟡 2 | The class pin asserts the file and the twin and not the executable bit, where `plan.md` says it generalises the four-assertion form | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:211` | open | **Executed** 2026-09-14: `X_OK` is asserted in four modules, each for its own wrapper; eight of the twelve pairs have nobody asking. All twelve are `100755` today. `spec.md` §In item 4 asks only for a pair, so this is answerable with the spec |
| 🟡 3 | `NO_WRAPPER` claims `chain_check.py` is *invoked in none of them*; what is asserted is *followed by a flag in none of them*, and `templates/config.md` lists it beside three bare commands | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` · `templates/config.md:165` | open | **Executed** 2026-09-14: every line of a shipped document naming `chain_check.py` printed and read; `templates/config.md:165` is a four-item list of checks the sealer runs, three typeable and one not, and `command_forms` cannot see it. Narrowing the sentence is in scope; adding the path to that line is the user-facing change `spec.md` §Out refused |
| 🟡 4 | `agents/warden.md` names the generator at line 138 and says where it is at 186 — two mentions and 48 lines later, in the file the incident's three `warden` segments were reading | `agents/warden.md:138` | open | **Executed** 2026-09-14: mention lines are 138, 182, 186, 290, 350, 379; the locator is at 186. `questions.md` Q4 answers *beside its first mention*, and `phases/phase-3.md` records the placement as *one sentence later*, which is true of the other two files and not of this one. `spec.md`'s stated property (at least once) is met |
| 🟡 5 | *The generator both rows name* — one row of that table names the generator, not two | `skills/implement/SKILL.md:521` | open | **Read** 2026-09-14: the table has three rows; `round-N.md` names the generator twice and the other two name the review orchestrator. The locator in the same sentence is correct, so nothing breaks |
| ⬜ 6 | *All three places that DO invoke it* undercounts: `skills/verify/scripts/broad_gate.py` and `skills/code-review/scripts/round_record.py` also invoke `chain_check.py` | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | open | **Executed** 2026-09-14: `git grep chain_check` over the tree outside `tests/` and `seal/`. Both carry the full path, so *reachable everywhere it is reached* holds and only the count is wrong |
| ⬜ 7 | Eleven `seal/ledger.md` rows were re-read and re-stamped and their `Checked` dates did not move | `seal/ledger.md` | answered | Disclosed in `overview.md` §Not done, measured there, and filed as #387. Its location is the shared ledger, so `agents/warden.md` §Role puts it outside `Needs a fix` |

## Executed probes

| What was run | Result |
|---|---|
| `reachable` from the new pin, applied to each of the nine documents as they stand at `release/v0.11.4` | false for all nine — the pin was red against every document before the sweep, independently of the branch's own account |
| `seal/ledger.md` at the base and at HEAD, every eight-hex anchor hash normalised to one constant, compared | byte-identical; 2110 lines both sides, 11 differing lines, exactly one hash change each, 7 distinct anchors |
| every line of every `.md` under `agents/`, `skills/`, `templates/` matched against `round_record.py` followed by whitespace and a dash | no hits — no typed form of the old spelling survives the respelling |
| the pin's two enumerations, printed | 12 scripts (11 wrapped, `chain_check.py` not), 43 documents, 13 wrapped document/script pairs, 4 unwrapped; all 13 carry both accepted forms |
| `reachable` for `skills/implement/scripts/seal.py` against three documents that do not name it, and against a synthetic line with no locator | true in all four — finding 🟡 1 |
| the same with the hyphen guard of paste-ready fix 1 applied | all 13 real pairs still green, synthetic `seal.py` line red |
| `git ls-tree HEAD bin/` | all twelve POSIX wrappers `100755`, all twelve twins `100644`; nothing is broken today |
| `pytest tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` in a clone at `8208928` | exit 0, 75 passed — three gates the orchestrator did not run that the branch's new prose and the new `bin/` pair could have turned red |
| the broad gate — the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's single act under `skills/agent-contract/SKILL.md` §2 and no segment here has taken it |

## Paste-ready fixes

🟡 1 — `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`,
replacing the body of `reachable` below its docstring:

```python
    command = command_name(script)
    # A command name with no hyphen in it is an ordinary English word --
    # `seal.py` answers to `seal` -- and this repository's prose is full of
    # it, so the bare-word form cannot tell a locator from a sentence. Those
    # scripts are reachable by path only, which is a reader that can fail.
    if "-" not in command:
        return script in text
    typed = re.search(rf"(?<![\w-]){re.escape(command)}(?![\w-])", text) is not None
    return typed or script in text
```

and a case beside the two readers that already guard this one:

```python
def test_a_one_word_command_name_is_not_a_locator():
    """`seal.py` answers to `seal`, and every document in this repository
    contains that word. Read as a locator it makes the rule unfalsifiable for
    that script, which is the one thing Q1's general form was chosen to
    prevent."""
    seal = "skills/implement/scripts/seal.py"
    assert not reachable("The sealer takes the seal after the rounds.", seal)
    assert reachable("It lives at `skills/implement/scripts/seal.py`.", seal)
```

🟡 2 — same file, appended to
`test_every_script_a_shipped_document_names_is_wrapped_or_classified` after
the twin assertion:

```python
    assert os.access(posix, os.X_OK), (
        f"`bin/{command}` ships without its executable bit, so the command "
        "resolves on PATH and then refuses. The form this generalises -- "
        "`tests/test_unverified_rows_close.py::test_the_wrapper_is_present_"
        "and_executable` -- asks for file, twin, exec bit and target"
    )
```

🟡 3 — same file, the first sentence of the `chain_check.py` row of
`NO_WRAPPER`, narrowed to what is asserted:

```python
        "Named in four shipped documents and shown with a flag in none of "
        "them -- which is what `test_an_unwrapped_script_is_shown_in_no_"
        "command_form` asserts, and the whole of it. A flag is the only "
        "sound tell in prose, so a bare mention in a list of checks is not "
        "caught: `templates/config.md` names it beside three commands. "
```

and, if the owner takes the user-facing half, `templates/config.md:165`:

```markdown
(`evidence-check`, `unverified-check`,
`skills/code-review/scripts/chain_check.py`, `survivor-check`)
```

🟡 4 — `agents/warden.md`, lines 138-139. The pinned substring ends before the
word `in`, so it survives whole; both new lines are under 88 columns:

```markdown
  `round_record.py new` copies it into the row of the same name in
  `round-N.md` — that generator is
  `skills/code-review/scripts/round_record.py`, typed as `round-record`. An
  answer the report format has no field for is a decision
```

🟡 5 — `skills/implement/SKILL.md:521`:

```markdown
The generator that row names is `skills/code-review/scripts/round_record.py`,
and the review orchestrator types it as `round-record`.
```

⬜ 6 — same file as 🟡 3, the invoker sentence of the same `NO_WRAPPER` row:

```python
        "Every place that invokes it carries its full path -- "
        "`.github/workflows/hygiene.yml`, `templates/hygiene.yml` and "
        "`docs/release-checklist.md` by hand, and "
        "`skills/verify/scripts/broad_gate.py` and this skill's own "
        "`round_record.py` in code -- so it is reachable everywhere it is "
        "reached. "
```

Needs a fix: yes — 🟡 1, 🟡 2, 🟡 3, 🟡 4 and 🟡 5. None of the five is a spec
failure; each is fix or justify, and 🟡 2 and the user-facing half of 🟡 3 are
answerable with `spec.md` as written.

Loses a record or crashes: no

Nothing here leaves a record outside the root and nothing crashes. The five
open findings are a gate weaker than its own plan claims and three sentences
that say something the tree does not.

## Proof

Opened at `8208928`: `spec.md`, `plan.md`, `questions.md`, `overview.md`,
`routing.md`, `changelog.md`, `phases/phase-2.md`, `phases/phase-3.md`,
`phases/phase-4.md`, `seal/ledger/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed.md`;
`bin/round-record`, `bin/round-record.cmd`, `bin/survivor-check`,
`bin/survivor-check.cmd`, `bin/test`;
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`,
`tests/test_the_record_is_generated.py` (the added block),
`tests/test_the_rules_have_one_owner.py` (the `GENERATOR_NAMED` block),
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py` (the `bin/`
enumeration cases); the full diff of `agents/sealer.md`, `agents/smith.md`,
`agents/warden.md`, `skills/code-review/SKILL.md`,
`skills/code-review/orchestration.md`, `skills/implement/SKILL.md`,
`skills/verify/SKILL.md`, `templates/sdd-phase.md`, `templates/sdd-round.md`
and `seal/ledger.md`; `templates/config.md` around line 165;
`docs/release-checklist.md` around line 100; `seal/config.md`.

Work done in a `git clone --no-local` at `8208928` with a `uv` virtual
environment of its own. Nothing was written in the checkout except this file,
and nothing was left behind in the clone that the clone did not build for
itself.
