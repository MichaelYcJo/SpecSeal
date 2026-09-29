# the walk leaves every inline HTML construct uncertain (#673) — questions for the planner

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**One row is a person's, Q1, and it does not block the build.** Its default
keeps what the tree already has, which is F's definition of *renderer hides*.
Q2 to Q5 are measurements, and the phase that meets each one runs it.

**Decided from the tree, so not reopened here.** Each is argued in `spec.md`
or `plan.md`'s Alternatives table, where the next reader can overturn it by
opening what the frame opened.

- The class is six constructs, H1 to H7 with the open tag split in two, from
  CommonMark 0.31.2 §6.6 and markdown-it-py 4.2.0's `HTML_TAG_RE`. It is not
  the report's three openers (`spec.md` §*The class, enumerated*).
- Counting all six as hidden is the inline half of what F's oracle already
  does for HTML blocks of every kind (`spec.md` §*Why the line is drawn at raw
  HTML*).
- Autolinks and code spans stay shown: a renderer displays both.
- The new shapes go in `FOUND`, never `ALPHABET` (the reviewer's executed
  floor).
- Two predicates, OR-ed, and `leaves_open` untouched.
- Sticky to a blank line, a fence or a comment block, with no closer followed
  across lines.
- The oracle's kind and its two helpers are renamed, and the ledger loses two
  anchors as `docs/the-evidence-ledger.md` prescribes.
- The oracle reads pieces at any token depth and lines at the top level.
- Only the config reader, and what reads through it, changes answer. The
  routing reader and the rider check read an uncertain line as live, which is
  what the walk told them before.
- `templates/config.md`'s sentence widens and is pinned (§14).
- The declaration case writes its closer as `a>`, because a `>` at a line
  start opens a block quote. That is why the reviewer's probe did not
  reproduce it.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does *a renderer hides* also cover text a renderer puts into a link's or an image's attribute, or does not emit at all? That is a link destination, a link title, an image description, and a link reference definition. **Why the tree cannot settle it:** F's frame defined the term as four places, and this work widens only the fourth, from an inline comment to all inline raw HTML, on grounds the tree holds (F's oracle already counts HTML blocks of every kind). No document says whether attribute text counts. The one block-level precedent points the other way without deciding it: a reference definition produces no token, so F's oracle has always called its lines shown, and nobody chose that. The shape it leaves: `[a](u "t` + U+2028 + "```" + U+2028 + a config table + `\n")`. There the base fences the rows, a browser displays none of them, and the walk and the oracle both call them shown, so `config_rows` reads `Mode`. It was read from CommonMark §6.3 and not executed | a person | **(a) Keep the definition (the default).** Nothing is built for it. The shape above reads as it does today, the same answer the oracle gives, so the property holds, and no committed file holds it. **(b) Widen it.** A separate work item: the walk calls a piece after `](`, `]:` or `![` uncertain, and a paragraph line after such a line pending, as it does for inline HTML. The oracle reads `link_open` and `image` attributes and the parser's `env["references"]` for the sentinel, and a line inside a multi-line title or definition becomes hidden. That costs claimed lines against the one-third floor, which nobody has measured, and a new `FOUND` family | (a). This work builds nothing for the family and says so in `spec.md` §*The class, enumerated* | ⬜ |
| Q2 | Does `test_the_walk_is_exact_somewhere` stay above its one-third floor with the sticky state and the seven new `FOUND` documents? **Why the tree cannot settle it:** a count over a generated corpus. The reviewer measured the three-document version green (278 passed across four modules), not the seven | a measurement | Above the floor: phase 2 records the count. Below it: a `FOUND` document is the smallest thing to drop, H6 or H7 first, because no reader row can start inside either. The floor is never lowered to make room | the reviewer's three-document result, until phase 2 counts | ⬜ |
| Q3 | Does any tracked `.md` file read differently through `config_rows` at `3fc0c5bd` and at HEAD, and does the walk's claimed-line count over them move? **Why the tree cannot settle it:** a run over the corpus. The reviewer measured the claimed count (24,009 of 68,819 for both walks), not `config_rows` | a measurement | No change: `spec.md` S8 holds, and the prompt budget in §*Failure direction* is empty for committed files. A change: the file is named in the phase record and the pull request, with what it read before and after | no change, which is what the reviewer's claimed-count run points to | ⬜ |
| Q4 | Does markdown-it-py 4.2.0 form an `html_inline` token for each new shape at every break its case uses? The shapes are H4 with the closer `a>`; H5 with `'`; H6 and H7, where the break stands as whitespace inside the tag; and the whole-line rows of S1. **Why the tree cannot settle it:** read from `html_re.py` (Python's `\s` takes all eight breaks), and not executed. The reviewer's H4 probe failed for a reason unrelated to the parser | a measurement | Formed: the case stands as `spec.md` writes it. Not formed: that oracle row or `FOUND` document is dropped and the phase record says why. The walk is uncertain there all the same, so nothing claims it. An S3 config case whose shape the parser does not hide is dropped too, because its docstring would say a renderer hides a row it shows | formed, as read | ⬜ |
| Q5 | With phase 1's oracle and the base walk, is the property module still green on the existing corpus, before any `FOUND` document is added? **Why the tree cannot settle it:** read, not run. No `ALPHABET` line or existing `FOUND` document puts a line start or a piece inside a multi-line non-comment construct (`[ref]: <x>` and `<br>` close on their own line; `<?php`, `<!DOCTYPE html>`, `<pre>` and `<script>` at a line start are HTML blocks). But the generated corpus is drawn, not listed | a measurement | Green: phase 1 closes alone, as planned. Red: the document it names is a real instance, and phase 2's walk change moves into phase 1 so no commit is red | green | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build.
- **a measurement** — a probe, a command or a count settles it.
- **the work** — unknowable at framing time; the phase that meets it decides
  it and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
