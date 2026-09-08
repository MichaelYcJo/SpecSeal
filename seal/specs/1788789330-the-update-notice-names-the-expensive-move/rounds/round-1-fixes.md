# 1788789330-the-update-notice-names-the-expensive-move — round 1 fixes

Target reviewed `0a9dfc5`. Fix commits `4780f7f`, `591a801` and the records
commit that carries this file.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `4780f7f` (the notice) and `591a801` (the eight document surfaces). The reload's claim now carries the scope the docstring and `skills/update/SKILL.md`'s table already had, in every surface a user reads |
| 2 | fixed | `4780f7f`. Reproduced first: both of round 1's survivors, run against the shipped case, came back green (exit 0 twice). The case now pins the reload claim's subject and scope and all three axes; five mutations, five killed |
| 3 | fixed | `4780f7f`. Took the shorter form. 707 → 620 characters, fourth line 347 → 260. The plan is unchanged and the code came back to it; `overview.md` §*Where spec and implementation diverged* carries the entry |
| 4 | answered | corrected at the records commit. The membership was right and the arithmetic was not: `spec.md` now measures at `86e140f` with `git grep`, states 37 distinct lines, 15 in class and 22 out, and reconciles row by row. Row 20 says twelve, row 22 names the three work items in full, and the row for this item's own `routing.md` is gone with the count that included it |
| 5 | answered | corrected at the records commit. The number has a source and it is not the experiment record: `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/questions.md` Q1 names `~/.claude/plugins/cache/specseal/specseal/0.5.0/skills/writing-style/SKILL.md` as the copy the sentinel was planted in. `overview.md` and `phases/phase-1.md` now cite that, and cite §*Method* and §*What it established* item 2 for the inference itself, which is where it actually rests |
| 6 | answered | Left as recorded, which is what the finding asks for. `hooks/ledger-migrate.py:4` is a module docstring, predates this branch, and ships no user-visible defect. Editing it here would widen a fix pass into a file the work item never touched, and the finding's own verdict is that naming it puts the decision on the record |
| 7 | fixed | `591a801`. `재시작하십시오` was the only 하십시오체 form in the file; the rewritten paragraph ends `재시작합니다` |

## What the re-enumeration found

Two properties were re-derived across the corpus **after** the fixes landed,
which is what round 1 was called for in the first place.

**Finding 1's property — a user-facing sentence that names the reload without
scoping it to the copy in force.** Ten runs name `/reload-plugins` outside
`seal/`, `tests/` and `CHANGELOG.md`. The report named four surfaces; the
re-run found **five** unscoped after those four were fixed, and four of the
five were shapes the report had not reached:

| Survivor | Verdict |
|---|---|
| `README.md` and `README.ko.md` command-table rows | **fixed.** Both said applying it comes after a reload or a restart, which presupposes a reload applies it |
| the two fenced by-hand comments, both editions | **fixed.** A one-line comment cannot carry the qualifier, so it points at the paragraph below rather than making a claim it has no room to scope |
| `README.ko.md`'s own paragraph | **fixed.** English carried the scope inside the claim's sentence; Korean carried it in the next one, opening `다만`. A reader who stops at the first sentence gets the unscoped version |

Four remain unscoped and all four are correctly out of the class: the two
editions of the experiment record (result 3 states *when* bodies are read — it
is the measurement, and rewriting it would be editing the evidence to match the
claim), the settling method in `skills/update/SKILL.md` §5 (it describes a run
to perform, explicitly under the newly installed version), and the same file's
*It does not restart or reload anything* (a statement that the procedure will
not type the command, making no claim about what a reload does).

**Finding 2's property — an assertion that passes on the presence of a word
rather than on what the sentence claims.** Enumerated by parsing every test
module for a function that obtains a runtime-rendered message (a hook's
`systemMessage`, `run_hook`, `notice()`, captured stdout) and asserts a string
literal is `in` it: **141 cases**. All but the notice's are assertions over
diagnostic and operational output — `both roots exist`, `not a readable zip`,
`present at HEAD and not here` — where the literal *is* the distinguishing
content and no false message carries it. The notice is the only place in this
repository where a test asserts against a message making an **evidential
claim**, which is the shape where a generic word (`measured`) survives a false
sentence. One instance, and it was the one the round found.

An earlier pass over the same question returned 244 by matching any variable
named `text`, which swept in prose assertions over documents read from disk.
Those are a different shape: the literal is the artifact, so presence is the
claim. The narrowing is recorded because the wider number is the one that
looks more thorough.

## Corrections to the report, verified before building on them

| Claim | What it is |
|---|---|
| The report's paste-ready regression test asserts `"out of that same copy" in doc` | **does not run as written.** [executed] `"out of that same copy" in module.__doc__` → `False`; the phrase straddles the docstring's line wrap at 18–19. The planted case normalises whitespace first, and says why in its own docstring |
| The banner's fourth line is 316 characters | **347.** [executed] `notice((0,7,1),(0,8,0))` → 707 characters over 4 lines, `[53, 107, 197, 347]`. The 707 total is right and finding 3's argument is unaffected |
| The 38 → 37 difference comes from an untracked `.venv` that `grep -r` reaches | **it does not.** [executed] `grep -rnI 'reload' .venv \| grep -vi preload` → 0 lines. The third hit was this work item's own `routing.md:18`, committed at `389ad12`, so the build's count included a line the branch had just written |
| The reviewer's shorter paste-ready block *"passes finding 2's assertions as written"* | **it would not have.** Its gap sentence opens `Hooks,` and the lookup was case-sensitive, so `next()` would raise instead of assert; and it says `install`, where the axis assertion looks for `installed`. The shipped notice and the shipped assertions were reconciled against each other by running them, and the lookup is lowered so a capitalised word cannot turn an assertion into an error |
