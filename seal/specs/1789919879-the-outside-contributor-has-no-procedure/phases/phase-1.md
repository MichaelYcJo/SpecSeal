# 1789919879-the-outside-contributor-has-no-procedure — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 7cf8dfec |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`CONTRIBUTING.md` gains the contributor procedure **above** `## Running the
checks`: which branch to base on and how to find it, what a contribution
costs, the exemption list grouped by CI step, and what to do when
`survivor-check` refuses. Plus the minimal pin Q6 decided.

## What this phase found

**The frame's precedent coordinate does not resolve, and the technique it
names does.** `plan.md`'s phase 1 row and `questions.md` Q6 both cite
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py#contributing_section`.
Executed `grep -rln contributing_section tests/` → no hits. The helper that
actually reads one `CONTRIBUTING.md` section to the next heading is
`running_the_checks()`, at line 670 of that same file, and the cases around it
are exactly the shape Q6 describes. So the frame is right about the precedent
and wrong about its name. The new pin is modelled on `running_the_checks()`,
and its docstring records the correction so the next reader of Q6 is not sent
looking for a function that does not exist.

**The pin binds the guard, not the prose.** Q6 asks for a minimal pin, and the
minimum that still has value is the sentence naming *why* the exemption list
is true: `exits 0 unless the base is `main``. A list of exemptions with no
guard named is a promise, and a new always-on CI step falsifies a promise with
every check still green — the failure `plan.md` §*The failure scenario of the
chosen approach* predicts. Pinning the guard phrase means the list cannot lose
its own reason while staying green. Every other case pins an identifier a
reader searches for (`routing.md`, `survivors.md`), never a sentence.

**The section names `plugin.json` on purpose, and a case pins that too.** The
contributor who needs this section arrives from a CI message about
`plugin.json`. A section that never repeats that word is a section they cannot
match to the message that sent them, however correct it is. This is the half
of A1 that lives outside phase 2's workflow change.

**Q1's decision was pinned in both directions.** The section names
`release/vX.Y.Z` and a case refuses any concrete `release/v\d+\.\d+\.\d+` in
the section — so the guide cannot be "helpfully" updated to today's branch
number, which is the edit that would make it false at the next release.

**Evidence that the case was red first** (§15, and `CONTRIBUTING.md`
§*What a change to a gate must carry* for the sibling phase). Run against the
tree before the section existed, `bin/test tests/test_the_contributor_has_a_procedure.py -q`:

```
E       ValueError: substring not found
tests/test_the_contributor_has_a_procedure.py:42: ValueError
FAILED ... ::test_the_procedure_is_the_first_section_of_the_guide
FAILED ... ::test_the_section_names_the_branch_by_convention_not_by_number
FAILED ... ::test_the_section_says_the_base_branch_is_what_the_refusal_is_about
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[routing.md]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[spec.md]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[plan.md]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[review round record]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[seal/ledger/]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[changelog.md]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[overview.md]
FAILED ... ::test_the_exemption_list_names_what_a_contribution_does_not_write[.claude-plugin/plugin.json]
FAILED ... ::test_the_exemption_list_says_which_guard_makes_it_true
FAILED ... ::test_the_section_warns_about_the_check_that_can_still_refuse
13 failed, 1 passed in 0.06s
```

Thirteen of fourteen red, and the one that passed is
`test_the_check_can_fail`, which asserts the reader raises on a guide with no
such section — it is the counterfeit guard and passing is its correct result
in both trees. After the section: `14 passed`.

**Neighbours, executed after the edit:** `test_docs_line_wrap` 23 passed (the
section is inside the 88-column limit at birth), `test_no_real_identifiers`
5 passed, `test_the_suite_has_a_command_that_is_cheap_twice` 58 passed — the
last one matters because its `running_the_checks()` finds its section by
`text.index("## Running the checks")`, and a new section inserted above it
would break that reader if it repeated the heading string.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds a section and a test module | none |
