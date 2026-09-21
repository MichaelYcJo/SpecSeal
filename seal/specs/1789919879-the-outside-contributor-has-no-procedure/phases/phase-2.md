# 1789919879-the-outside-contributor-has-no-procedure — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b4cd6aad |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The hygiene step's refusal message, and the case in
`tests/test_the_release_check_watches_what_ships.py` that pins it — **written
first and seen red against the unfixed workflow**. The wording itself is Q7,
decided here against `plan.md` §*The design constraint the message has to
satisfy*: a contributor who lands on `main` by GitHub's default must come away
knowing the base branch is the problem, and the message must stay useful to
somebody genuinely cutting a release, for whom the old text was correct.

## What this phase found

### Q7, decided — the wording

```
::error::this PR changes what ships and leaves plugin.json at $old. If this
is the release pull request, move the version — an update keyed to it reaches
nobody. If this is a contribution, the base branch is the cause and not the
version: a pull request into main is a release here, and contributions go to
the open release/vX.Y.Z branch instead. Change the base rather than
plugin.json — see CONTRIBUTING.md, 'Opening a pull request'.
```

(One line in the file; wrapped here to fit.) Five decisions are in it, and
each has a case behind it:

- **Both causes, neither asserted.** `If this is …` twice. The step reads
  `base_ref = main` and nothing else, so it cannot know which reader it has,
  and a message that picks one is guessing in front of somebody already stuck.
- **The release case first.** That is the reader for whom the old message was
  already right, and `plan.md` fixes the order.
- **The branch named by convention.** `release/vX.Y.Z`, never a version. A CI
  message is the worst place for a fact that expires, and a release branch is
  deleted after its release. A case refuses any concrete
  `release/v\d+\.\d+\.\d+` in the line.
- **The wrong edit named explicitly**, `Change the base rather than
  plugin.json`. Naming two causes without saying which edit is wrong leaves
  #443's outcome available: a contributor edits the one file their change must
  not touch, and the edit does not fix the pull request either.
- **The cause and the fix inline, the document after.** A CI log is read by
  somebody who has not cloned the repository. A second hop is a second chance
  to stop, so `CONTRIBUTING.md` is cited and not relied on.

### The red run, against the unfixed workflow

`bin/test tests/test_the_release_check_watches_what_ships.py -q` with the new
cases present and the message untouched — exit 1, `5 failed, 30 passed`:

```
E       AssertionError: the refusal never mentions the base branch, so a contributor whose base is the cause is told only about a file they must not touch:
E         this PR changes what ships but leaves plugin.json at $old — an update keyed to the version will not reach anyone"
FAILED ... ::test_the_refusal_names_the_wrong_base_as_one_of_the_two_causes
FAILED ... ::test_the_refusal_still_serves_the_release_and_puts_it_first
FAILED ... ::test_the_refusal_asserts_neither_case
FAILED ... ::test_the_refusal_says_not_to_move_the_version_to_satisfy_it
FAILED ... ::test_the_refusal_names_the_document_that_holds_the_procedure
5 failed, 30 passed in 0.09s
```

After the message moved: `35 passed`. The sibling step's module,
`tests/test_a_release_cannot_ship_an_untrue_milestone.py`: `29 passed`.

### The A2 cases are green in both trees, so mutation is the only evidence

Two of the seven new cases pin what must **not** change — the closed base
guard and the `exit 1` after the refusal. A case that is green before and
after the edit proves nothing until it is broken, so each was mutated alone
and the tree restored from bytes kept in the scratchpad (never from HEAD).

**The first form of the guard case survived its mutation, and that is the
finding of this phase.** It was a regex from `then` to `exit 0 … fi` with
`re.S`, modelled on
`tests/test_a_release_cannot_ship_an_untrue_milestone.py#hygiene_step`. With
the guard's own `exit 0` and `fi` deleted the case still passed, because this
step holds a **second** `if … exit 0 … fi` — the `-z "$ships"` early return —
and `.*?` under `re.S` reached it. The precedent's own docstring warns about
exactly this mutation, and the borrowed shape was vulnerable to it here for a
reason the precedent's step does not have: a second `if` in the same step.

Rewritten to read the step by lines and assert the guard **closes before the
next `if`**, which is what *closed* means. Re-measured, each mutation applied
alone:

| Mutation | Result |
|---|---|
| unmutated | 1 passed |
| the guard's `exit 0` and its `fi` deleted | **1 failed** |
| only the `exit 0` deleted | **1 failed** |
| the condition replaced by `if false` | **1 failed** |
| restored | 1 passed |
| `exit 1` after the refusal changed to `exit 0` | **1 failed** (`test_the_refusal_still_fails_the_run`) |

`cmp` against the kept copy after every restore: identical.

### The four things a gate change owes (`CONTRIBUTING.md`)

- **A test seen red** — above, quoted from the run.
- **Failure direction: neither.** The condition, the exit codes and the set of
  refused pull requests are identical before and after. Only the text a
  refused author reads differs. Verified by the guard and `exit 1` cases
  above, and by re-parsing the workflow: `yaml.safe_load` over the edited file
  returns 13 steps and still finds `a change to what ships must move the
  version`.
- **Prompt budget: zero.** Nothing here puts a question in front of a person,
  in CI or in a session. The change removes a wrong instruction from a message
  a person was already reading.
- **Platform honesty.** The step is `shell: bash` on `ubuntu-latest` only.
  The cases read the workflow as text with Python's `re` and `str` — no
  process inspection and nothing platform-dependent, so they hold on the
  macOS and Windows legs of the suite as they do on ubuntu. The message
  itself was rendered through `bash` locally on darwin (`bash -n` exit 0, then
  run) to confirm the quoting survives: it holds one `$old` expansion, single
  quotes nested inside double quotes, and no backtick or `$(` that a shell
  would try to execute.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The old refusal text, `this PR changes what ships but leaves plugin.json at $old — an update keyed to the version will not reach anyone` | Nothing needs to own it: its whole content survives inside the new message's first half, which is the release reader's case. No other file quoted it — checked before deleting, and `survivor-check` over this branch's range is the standing verification |
