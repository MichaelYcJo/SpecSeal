# 1788789330-the-update-notice-names-the-expensive-move — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <filled at the commit that closes this phase> |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Both READMEs move with the text, English and Korean, in one commit —
`README.md:266`, `:311`, `:318` and `README.ko.md:257`, `:302`, `:309`. The
handoff added the Korean three itself: the ticket names none of them, and its
`README.md:318` had drifted off the hit list entirely.

## What this phase found

**The Korean edition is where the change is easiest to get wrong, and it is not
about translation.** `README.ko.md:302` said `적용은 재시작 후이고` — *applying
it comes after a restart* — inside the same sentence that reassures the reader
nothing is half-applied. Carrying the new fact by editing that clause in place
would have produced exactly the English-shaped sentence `writing-style` §영어를
옮길 때는 구조를 버리고 뜻만 가져온다 forbids: a long insertion between the
subject and its particle. The clause was split into its own paragraph instead,
which is also what the English needed for a different reason — three facts do
not fit on the end of a sentence about safety.

**A code comment is a place that tells a user what to do, and the wrap test
cannot see it.** `README.md:318` and `README.ko.md:309` are inside fenced
blocks, which `tests/test_docs_line_wrap.py::prose_lines` skips by design. Both
carried `# then restart` / `# 그다음 재시작`, and both are as much an
instruction as the paragraph above them. A reader who copies the block gets the
comment with it. Nothing would have caught leaving them.

**The grep was re-run over the whole corpus after the edits, not just over what
was edited.** Fourteen `restart`/`재시작` hits remain across the four files and
every one of them now sits beside the reload; the fifteenth,
`README.md:446`, is the `seal mode` sentence that was never in the class.
This is the check the handoff asked for by name, and it found nothing — which
is the outcome worth recording, because the alternative reading of a silent
re-run is that it was not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `README.md:311`'s *"Restart to load it; the session you are in keeps…"* | split in place: the *nothing is half-applied* half stays in the paragraph above, the loading half becomes its own paragraph |
| `README.ko.md:302`'s `적용은 재시작 후이고` | the same split, for the same clause |
| `# then restart` and `# 그다음 재시작` in both by-hand blocks | replaced in place; nothing else carried them |
