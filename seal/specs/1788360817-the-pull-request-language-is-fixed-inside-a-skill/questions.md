# the pull request language is fixed inside a skill — questions for the planner

<!-- seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here.

The owner approved the defaults in advance and was away for this session, so
every row was BUILT to its default. Overturning one is an edit to the skill's
text and to one test case; none of them reaches code. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Is `seal/config.md` created at first setup, beside the parity question? | **(a) never created — the skill says how** · one more file only where somebody wants a non-default, and no third question in the setup batch. Costs discoverability: nobody learns the row exists until they read the skill. **(b) created at setup, holding the default** · every repository carries a file restating what absence already means, and the setup batch grows a question whose answer is "English" for almost everyone | **(a)**. The issue makes it optional by construction — *"No file or no row means the default"* — and the discoverability cost is smaller than it looks: `commit-pr-convention` is read before every commit and every pull request, which is exactly the moment the question matters. The parity question needed setup because nothing else ever raises it | ⬜ built to (a) |
| Q2 | The mirror file is `pr.ko.md` today, meaning "the Korean one". Under this change the mirror is whatever language the config does not name. Rename, or re-read? | **(a) `pr.<lang>.md`, named for the mirror's OWN language** · `pr.ko.md` in an English repository, `pr.en.md` in a Korean one. Nothing is renamed, because the twelve files here are already correct under the new rule. **(b) a language-neutral name (`pr.mirror.md`)** · one name everywhere, twelve `git mv`s, and every round record, overview and design record that cites `pr.ko.md` by name goes stale | **(a)**. The name was never wrong — it was under-specified. Reading it as "the mirror's language" costs one sentence in the skill and moves no file, and it survives a repository with two mirrors | ⬜ built to (a) |
| Q3 | Does anything but the skill's text enforce the language? | **(a) the skill alone** · same mechanism as the prefix vocabulary, which no hook enforces either. **(b) a commit gate that judges the message's language** · nothing can do this without being wrong on names, identifiers and quoted English, and a gate that guesses is worse than none | **(a)**. The gate this repository would want is a language detector, and a false stop on a commit is the failure mode the whole hook design avoids | ⬜ built to (a) |
| Q4 | Should the row's value be a language name (`Korean`) or a code (`ko`)? | **(a) the English name** · a model reads it without a lookup table, and a person writing the file does not have to know ISO 639. **(b) the code** · shorter, and it is what the mirror's filename uses | **(a) for the row, (b) for the filename.** They are read by different things: the row by a model deciding what prose to write, the filename by a person scanning a directory. `pr.ko.md` is already the second and stays | ⬜ built to (a) |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
