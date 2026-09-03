# The settings live in a file nobody opens — questions

| # | Question | What was built, and why |
|---|---|---|
| Q1 | Does the skill edit `config.md` itself, or always route? | **It edits rows with no side effect and routes the ones that have them.** The `Mode` row moves a folder, stages a commit and installs or removes a workflow file — that is `seal mode`'s work and reimplementing it in a skill would be a second copy nothing can mutation-test. |
| Q2 | Should first setup call this skill rather than asking its own questions? | **Not yet.** The bootstrap asks before there is a root to write into, so it cannot route to a command that reads one. Both name the same rows, and a case asserts they do; folding them into one is a later change with a real risk of the bootstrap losing its ordering. |
| Q3 | `/specseal:config` or `/specseal:settings`? | **`config`,** because the file is `config.md`. A door named differently from the room is one more thing to learn. |
| Q4 | Should it show rows that are absent? | **Yes, with their default.** A row a repository never set is the most likely one somebody wants to change, and a file that shows only what is present hides exactly those. |
