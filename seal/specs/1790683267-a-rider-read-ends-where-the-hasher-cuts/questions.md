# a rider read ends where the hasher cuts — questions for the planner

<!-- seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The ticket left these judgments open, and the
tree answered each of them. They are listed so nobody reopens them, each with
where its grounds are, so a reviewer can overturn one by opening the same
place.

## Decided from the tree

| # | Judgment | Answer | Grounds |
|---|---|---|---|
| J1 | Patch the reader's piece walk, or take the hasher's blocks | Take the hasher's blocks | plan.md §*Alternatives*, A. The walk has been patched twice, and each patch restated the hasher's rule |
| J2 | Leave `comment_blocks`' TEXT path in place, or remove it | Remove it, with the `gfm_places` flag only it read | plan.md §*Alternatives*, B against C. The docstring must change either way, so the same three rows are re-read either way (spec M10) |
| J3 | Remove `quoted_lines`' TEXT parameter too | No | spec §*Scope*, out. It is that unit's tested contract against the CommonMark oracle, and not about where a rider ends |
| J4 | How the fix pairs each start with its end | By index over `range(len(starts))`, with no length check | #682's comment, `write_block` at `7ffa520c`, and plan.md §*Technical context*: the ends are built from the starts, so a check could never fire. `itertools.pairwise` is refused on the floor's grounds |
| J5 | Correct G13's wording or re-read it | Re-read, wording kept | G's round 3, ⬜ 2: "G13's clause stays as written once the fix lands, and becomes true by construction". P5-1 and R1-1 take `Corrected` notes, because this item makes sentences in them false (plan.md §*Ledger*) |
| J6 | One case, or a second for the verdict | Two: the class case and the verdict case | `skills/agent-contract/SKILL.md` §14. The markdown shape's verdict moves from drifted to BROKEN, which a person reads |
| J7 | The 576-prefix differential as a case or as a probe | Inside the class case, seen red against a named mutant | It already held at the base (spec M5), so it guards the class rather than finding a defect, and §15 accepts a mutant for a case about agreement |
| J8 | Which commit the new cases are seen red at | `6321dbdc` | spec M1: its `rider_check.py` is `7ffa520c`'s, the reader round 3 measured apart from `write_block` |
| J9 | Where the fragment's bullet goes | `### Fixed` | The change removes a symptom G's fragment already calls a defect, and adds no gate that refuses more (spec §*Failure direction*) |
| J10 | Edit G's changelog fragment or spec | No | `skills/implement/SKILL.md` §6 keeps closed records, and `CLAUDE.md` gives each work item its own fragment |

## Rows still open

What is left is for a measurement or for the work. None of it blocks the
build, and the phase that meets each row answers it in its record.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Do all eight characters reproduce both shapes at `6321dbdc`? The reviewer and the orchestrator ran U+2028 alone | a measurement | Each red parameter is a case seen red. A parameter that is green at the base is a character the reader already handled, and the phase record says which one and why | Expect all sixteen red: `gfm_places` breaks a piece at each of the eight, and the step-over and the piece walk treat them alike (read) | ⬜ |
| Q2 | Which six whitespace prefixes and six suffixes S4 uses. Round 3's report gives the count and not the strings | the work | Any six whitespace strings including the empty one, fixed in the case so the count is reproducible | `""`, `" "`, `"  "`, `"\t"`, `" \t"`, `"\t "` for both | ⬜ |
| Q3 | How S5 compares two problems "the location aside". A problem's sentence may carry the rider's line number, which the break moves by one | the work | Compare severity and the sentence with the `rel:line` location removed, or compare severity and the stamp-state word alone. The phase record says which, and why it is enough to catch drifted against BROKEN | Severity plus the sentence with the location removed | ⬜ |
