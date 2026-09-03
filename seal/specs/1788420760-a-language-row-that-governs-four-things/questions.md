# A language row that governs four things — questions

| # | Question | What was built, and why |
|---|---|---|
| Q1 | Does the posted review report follow the commit row or the record row? | **The commit row.** Posting and recording are separate acts producing different texts — `skills/code-review/SKILL.md:136` writes the files *right after posting*. A report is prose for whoever opens the pull request; a round record is half structure. |
| Q2 | Should `Record language` fall back to `Commit and pull request language` when absent? | **No.** `templates/config.md`'s rule is that an absent row is not an error and every item's default is what repositories got before the row existed. A row inheriting another's value breaks that sentence, and someone who set one did not ask for the second. |
| Q3 | Is renaming the first row worth the churn? | **Yes, and only now.** It ships in this release; renaming after means every repository that wrote the file has a key that no longer exists. The name has also understated the row since it shipped — it has always governed the commit subject and body. |
| Q4 | Should the row's value be checked against a list of languages? | **No.** The reader is a model choosing prose. A permitted-language list is a list somebody maintains, and an unrecognised value is not a failure mode anyone has met. |
