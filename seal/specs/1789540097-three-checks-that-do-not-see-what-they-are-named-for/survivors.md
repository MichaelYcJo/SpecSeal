# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — survivors

<!-- Places `survivor-check` reported as still carrying wording this range
removed, and which are judged correct to leave standing. Each row quotes the
STANDING text, so the exemption stops holding as soon as that text changes.
Run: `bin/survivor-check --range <base>..HEAD --exempt <this file>`. -->

**Which rows are live depends on the range, and round 2's correction is that
the preamble used to claim of all three what was true of one.** Measured at
`64f36eee`:

| Range | What it reports with no exempt file |
|---|---|
| `27a2d403..HEAD` — the build's own range | exactly one place, `phases/phase-3.md:36` |
| `9087705b..HEAD` — round 2's fix range | exactly one place, `tests/test_waiver_decided_at_start.py:639` |

The `plan.md`, `spec.md` and `overview.md` rows below are reported by neither
today. They are kept because the decision each records is real and the
matcher's pairing moves whenever the corrected side is reworded — round 1's
fix pass changed `overview.md` and `phases/phase-6.md`, which is exactly what
stopped two of them being paired. A row that exempts nothing costs nothing
and is not a claim that anything was reported.

Every row is a record rather than an instruction. That is the distinction
this file is for: a record asserts a PAST state, which is what lets one sit
beside a contract at all. Only the first carries a correction beside the
standing text; the rest stand unchanged on purpose, and the Grounds say why.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/phases/phase-3.md` | `**The repair was itself held by nothing, and that is the shape this work item exists to repair.**` | **Live over `27a2d403..HEAD`.** The paragraph is phase 3's own finding and was true when written — hoisting the patterns is why the phase added a unit `plan.md` does not name. Round 1's 🔴 1 showed the repair incomplete rather than wrong, and the correction is appended in the same section, naming the round and the fix. Rewriting the paragraph would delete the reasoning that produced the defect, which is the one thing a phase record exists to keep |
| `tests/test_waiver_decided_at_start.py` | `definitions = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))` | **Live over `9087705b..HEAD`, and a false positive.** The two phrases it shares with the sweep round 2's fix changed — *definitions files for path*, *path root for* — are the idiom for walking a glob, not wording this range removed. It is also not the same defect: this case looks for `AskUserQuestion`, which `agents/smith.md` and `agents/framer.md` each contain once, so its loop body **does** execute on the committed corpus. Measured at `64f36eee`: 2 occurrences across the five definitions |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/plan.md` | `**No mutation, because nothing in the tree reads a docstring** — planting a reader is new mechanism aimed at the file `seal/follow-up.md` already holds open for the owner` | Round 1's 🟡 5 is right that this reason does not hold — the follow-up row is about a different act. `plan.md` is the **framer's** document and its Verified-by cells are the design the gate approved; a fix pass rewriting an approved contract after the fact erases what was actually approved. The reason that is true is in `phases/phase-6.md` §*What this phase found* and `overview.md` §*Not done*, both naming 🟡 5. Round 2 confirmed the reasoning |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/spec.md` | `**A case that pins the wrap module's documented numbers.** Nothing reads a docstring today; planting a reader is new mechanism aimed at the file the follow-up row already holds open.` | The same sentence one document over, and the same grounds. **Its own row, added at round 2's correction**: round 1's Grounds said one row covered both documents, and no row quoted `spec.md`, so a reader checking the claim found nothing. A row's Quote is its anchor, so a claim about two documents needs two |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/overview.md` | `**#422's window still crosses headings, and that is deliberate.**` | **A false positive of the similarity matcher**, reported while `phases/phase-6.md` still carried the text round 1 rewrote. The two phrases — *md out rules*, *out with grounds* — are both halves of *`spec.md` §\*Out\* rules it out with grounds*, which two unrelated paragraphs cite because they cite the same section. This paragraph is about the 140-character window crossing headings; the removed text was about pinning a docstring number |
