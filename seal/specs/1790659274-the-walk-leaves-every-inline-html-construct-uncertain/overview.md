# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show goes here. -->

## Why this work exists

A piece of a line inside CDATA, a processing instruction, a declaration or a
tag its line left open was claimed live, so the config reader could read a
`Mode` row neither its base reading nor a renderer shows; the walk and the
oracle now treat all six kinds of inline raw HTML as they treated a comment
(#673, #667 round 3's 🟡 1 and 🟡 2, ⬜ 4).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How `leaves_html_open` reads several openers | `spec.md` §*The class, enumerated*: "Where the walk finds an opener the parser does not honour … the walk reports it open, which errs only toward uncertain … Where two constructs nest in the text, the walk reads left to right and skips what an earlier construct holds, which is also what the parser does." The code asks every opener whether an end follows it | code | Executed (`<scratchpad>/1790659274/nest.py`): an opener the parser does not honour can find its end inside a real construct, and reading on from there steps over the real opener. `x` + `` `<?` `` + ` <![CDATA[ a ?> b` + LS + a fence run and a config table + `]]>` gives `[("Mode", "shared")]` with the round 3 draft, and the oracle hides every piece; the same with `<b c` and with `\<?` in front. Both FOUND documents and an S4 assertion pin it, red with the draft. The cost is one claimed line in 577 tracked files over the draft |
| What the pending state asks after a comment's `-->` | `spec.md` §*The reading after this work*: "After a comment the pending state ends at `-->` as it does now, and the text after that `-->` is asked both questions again." The code asks the whole pending line for a non-comment opener, and a line that has one ends at a blank line or a block, never at `-->` | code | The comment that left the paragraph pending may be one the parser never formed (a `<!--` in a code span), and then an opener before the `-->` is real and the `-->` is text. `x` + `` `<!--` `` + ` a`, `b <? c --> d`, `e ?> f`: the parser hides `e ?> f` and the draft claimed it live. A FOUND document and an S5 assertion pin it, red with the draft |
| How the oracle finds a piece inside a closing tag | `spec.md` S2 names H7; §*Data & interfaces* says `_starts_in_inline_html` "looks for the sentinel". A run of letters cannot stand between a closing tag's name and its `>` | code: a second mark, a run of Unicode spaces, tried after the letters | Executed (`<scratchpad>/1790659274/q4.py`): letters found H2 to H6 at all eight breaks and H7 at none; spaces found all. Spec silent on the mark's characters |
| S8's claimed-line half | `spec.md` S8: "the walk's claimed lines over the same files are the same count" and "The reviewer measured 24,009 of 68,819 claimed for both walks" | measured and recorded: the count moves | The reviewer's 68,819 is the property module's corpus, not the tracked files. Over the 577 tracked `.md` files the walk claims 72,155 lines at HEAD against 72,440 at `3fc0c5bd`, 285 fewer, in 23 files, mostly changelogs and round reports that quote `<?`, `<!` or a tag in prose; the round 3 draft costs 284. The half S8 exists for holds: `config_rows` reads the same rows in all 577 at both commits |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the whole tree (`unverified`; phases ran the property, config, routing, rider and template modules only) | the orchestrator, by spawning the sealer once after the review rounds settle |
| The eight breaks on Windows: the change is string processing, and CI's `windows-latest` leg is the only run on that platform | CI's `windows-latest` leg at the pull request |

## Not done

The link and image attribute family (`spec.md` §*The class, enumerated*, third
table) is left, as Q1's default (a) says: a person answers whether *a renderer
hides* widens to it. Work item 1790645290's `changelog.md` still says "after a
`<!--` in the middle of a line"; that fragment describes what #667 shipped, and
this work item's own fragment says what #673 widened.

## Fed back into the spec

none — `spec.md` is left as framed; the divergences above are recorded here and
in `phases/phase-2.md`.
