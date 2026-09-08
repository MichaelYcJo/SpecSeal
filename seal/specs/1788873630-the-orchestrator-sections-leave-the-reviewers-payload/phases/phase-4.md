# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | c24f9d1 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The narrow version of #265's part 2 only: the per-document sections of
`skills/writing-style/SKILL.md` that are not a reviewer's — 「PR 본문에만」,
「다른 팀에 답할 때」, 「사용자와의 대화에만」 — leave the reviewer's payload
while 「리뷰 코멘트에만」 stays. **No style gate in `round_record.py new`**,
and `writing-style` stays in every agent's `skills:` list. The Korean
per-document headings are the file's own surface and stay Korean.

## What this phase found

**3,688 characters is all four sections, to the character.** The ticket's §2
names four sections and calls all four *not a reviewer's*, which cannot be
right, because one of them is precisely a reviewer's — and the owner's answer
keeps that one. Measured: 「리뷰 코멘트에만」 554, 「PR 본문에만」 1,169,
「다른 팀에 답할 때」 1,084, 「사용자와의 대화에만」 881, and the four together
3,688 exactly. **So the recovery is 3,134 characters, not 3,688**, and the
554-character difference is the section the reviewer needs.

**The three are contiguous too**, lines 240–333, sitting between the section
that stays and 「English prose rules」.

**Two sentences pointed at a moved section as 「아래」.** 「먼저」 closes by
naming 「사용자와의 대화에만 해당하는 것」 as *the section below*, and the
`<!-- -->` comment under 「리뷰 코멘트에만」 opens with *아래 절들* meaning all
four. Both now name the file. A split whose only visible defect is the word
*below* is the defect a grep for section names does not find, because neither
sentence spells a heading the moved file holds.

**The frontmatter was deliberately left alone.** A skill's `description` is
injected into every session's skill listing, so a sentence added there to
name the new file would be paid by every session — against this work item's
own goal. A session that loads the skill reads the body, and the body carries
the pointer.

**What this half gives up, and it is `smith`'s.** `warden` loses nothing: the
one section it writes against stayed. `smith` keeps `writing-style` preloaded
and now reaches three of the four by a pointer when it writes a pull-request
body. That is a downgrade from guarantee to pointer for one agent, and it is
the trade the owner took rather than a gap this phase discovered — the
alternative is a mechanical style check, which #180 says is a question and
not a line to write.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| 「PR 본문에만 해당하는 것」, 「다른 팀에 답할 때」, 「사용자와의 대화에만 해당하는 것」 — 94 lines from `skills/writing-style/SKILL.md` | `skills/writing-style/outside-the-review.md`, verbatim |
| The two 「아래」 references, which named a section that is no longer below | rewritten in place to name `outside-the-review.md`; nothing left the tree |
