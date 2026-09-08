# Feature Specification: every copy out of `raw` meets the hider question

<!-- seal/specs/1788873610-every-copy-out-of-raw-meets-the-hider-question/spec.md -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | between two designs that catch the same defect, the one that stops to ask a person is the more expensive. A guard asked of the record's own text catches every copy path without a person enumerating them |
| `skills/agent-contract/SKILL.md` §12 | the finding names `inherited_rows`; the fix is owed to every instance the same cause produces, and the cause is that nothing reads the record back |
| `skills/agent-contract/SKILL.md` §13 | *the two texts agree about where a hider is* is the assumption this branch removes for a third time. It is removed here by reading the artefact rather than by asserting the inputs |
| `skills/agent-contract/SKILL.md` §14 | a refusal naming a fence that closes is text a person reads and acts on, so the new message is documented and pinned in the same commit |
| `skills/agent-contract/SKILL.md` §5 | the ticket's three facts are claims with coordinates. Two reproduced; one did not, and §*Where the ticket is wrong* below says so |
| `CLAUDE.md` §*a change writes fragments* | the changelog entry and the ledger rows go to this work item's own fragments; `seal/ledger.md` F2 is re-verified in place because this change does not remove its anchors |

## Scope

**In.**

1. The hider question is asked of **every record `round_record.py` writes**,
   in the one function that writes one, before the bytes reach the disk.
2. A comment that opens inside a fenced block and closes outside it is
   refused by a message naming the comment, on every text that is asked the
   question.
3. Four documents are corrected, and the completeness argument they carry
   names the property rather than a count of copies.

**Out.**

- **The read-less half of the class.** A hider in a text the generator reads
  for named sections can make it read LESS than the text holds — an earlier
  record's verdict row it does not inherit, a fix row `close` reports the
  smith as never having written, a `New units` entry a depth walk does not
  see. None of the three puts a hider into a record, all three are refused
  loudly today (measured below), and the message each gives is about cell
  arithmetic rather than about a comment. `overview.md` §Not done carries it
  with its measurement and `seal/follow-up.md` names its answerer.
- **A whole-text hider question on an input read for named sections.** It
  would refuse a file this repository already has: the `` `<!--` `` in a code
  span at `seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1-fixes.md`
  blanks that file's tail and hides nothing `fix_table` reads.
- Any change to `reader.strip_comments`, which does not know a code span
  from prose. It is the shared reader, and the two sides of every comparison
  in this plugin agree only because they run the same passes.

## Where the ticket is wrong, measured

The ticket is a request and not an authority (`implement` §1). Two of its
three facts reproduce at `8114937`; the third does not.

| Ticket's claim | Measured at `8114937` |
|---|---|
| a comment straddling a copied block is refused by a message naming a fence that closes | **reproduced.** Exit 2, `a fenced block in the report is never closed`, and `blank_fences` over the report as written leaves no fence open |
| `inherited_rows` copies a hider out of an earlier record and the loss re-enters every later record of the chain | **not reproduced.** `inherited_rows` copies the `Location` cell alone. An opener there swallows the row's remaining pipes, the row reads as three cells, and the run is refused — loudly, with a message about cell arithmetic. An opener in a `Grounds` cell is never copied at all, and round 2's record came out clean, every section resolving |
| the same shape reaching a record from a report | **reproduced, and worse than the ticket's version.** A report whose `Grounds` cell opens a comment that closes on the line below is accepted, `new` **exits 0**, the record is written, and `## Executed probes`, `## Inherited coordinates` and `## Deferred` each resolve to **0 occurrences** through the shared reader while standing in the bytes. Nothing in the run says a word |

So the reachable silent loss is not `inherited_rows`' copy. It is that **no
copy path is asked about the record it lands in** — which is the property the
grid was reaching for and named by listing sources instead of the
destination.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| a copied cell takes half a comment | Given a report whose verdict row opens an HTML comment and closes it on the line below · When `new` runs · Then no record is written and the refusal names the comment, the slice and the closer | `tests/test_the_record_is_generated.py`, seen red at `8114937` where it exits 0 with the record written |
| a comment crosses a fence in the report | Given a fenced block holding `<!-- a note`, the block closed, and `-->` after it · When `new` runs · Then the refusal names the comment and not a fence | same module, seen red at `8114937` where the message reads `a fenced block in the report is never closed` |
| a comment crosses a fence in the round paragraph | the same text as `--asked` | same module, §12's other instance |
| a flag carries an opener | Given `--ran-by 'specseal:warden <!-- on a model'` · When `new` runs · Then no record is written | same module. No input check can see this one: the value never passed through a text |
| `close` reads back what it writes | Given `--broad-gate` carrying an opener · When `close` runs · Then the record is left as it was | `tests/test_the_fixes_close_the_record.py` |
| the completeness argument is checkable | Given the module's own source · When the AST is walked for every `open(..., "w")` · Then every one of them is inside the single function that asks the question first | `tests/test_the_record_is_generated.py`, over the module rather than over a list of names |
| an earlier record's hidden verdict row is not silent | Given a `round-1.md` corrected in place with an opener in a `Location` cell · When round 2 runs · Then no record is written | same module. Pins that the read-less half is loud, and its docstring names the message as deferred |

## Data & interfaces

No file format changes. `round_record.py` gains four units and one write
path:

| Unit | What it is |
|---|---|
| `open_hider(reader, text)` | which hider is still open at the end of `text` — `COMMENT`, `FENCE`, `STRADDLE`, or None. The comment first, for the reason it already had; `STRADDLE` is the third answer and is told from `FENCE` by asking the fence question of the raw text as well |
| `opens_at(reader, lines, blank)` | the 1-based line the still-open hider opens on, found by asking the reader's own pass of each prefix rather than by a second implementation of where a marker sits |
| `hiders_close(reader, text, messages)` | the refusal, in `messages`' words, with the coordinate appended |
| `write_record(reader, path, text)` | the one place a record is written, and it asks the question first |

The five existing hider messages keep their bytes, so every case and every
ledger anchor that names one stands. Five are added: two straddle messages
for the two texts that already ask, and three for a record.

## Open questions → questions.md

Q1 is the only one, and it is about released history rather than about the
code.
