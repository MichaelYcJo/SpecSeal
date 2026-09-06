# Feature Specification: a refusal stays a sentence when the virtualenv cannot be written to

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `.github/scripts/run_tests.py` module docstring — *every failure here is a sentence rather than a traceback* | The property this work restores; it is the module's own stated contract and the test module has a section named for it |
| `skills/agent-contract/SKILL.md` §12 (enumerate the class) | `hide_from_git` is the only place this module writes to the working tree, so the class is closed by construction rather than by a list |
| `CLAUDE.md` § *A ledger coordinate names content* | R2's guarantee is stated over exits; the caveat goes in the same change, or the ledger says something the code does not |

## Scope

**In.**
- The unwritable-`.venv` path: a sentence naming the path and what it means for `git status`, never a traceback.
- The caveat on `seal/ledger.md`'s R2 row, whose guarantee — *invisible to git on every exit of `ensure`* — is false on exactly this path.
- The reach-vocabulary case in `tests/test_the_fixes_name_their_surface.py`, which pins three constants and cannot see a sixth value `call_sites` could return.

**Out.**
- Any behaviour change to the refusals themselves. The floor refusal, the build refusal and the no-pytest refusal keep their wording and their exit codes; what changes is that the ignore's failure no longer replaces them with a traceback.
- Making the ignore succeed. A read-only `.venv` is the operator's; the runner says what it could not do and carries on.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The refusal survives an unwritable `.venv` | Given a `.venv` holding an interpreter and a `pytest` script, `pyvenv.cfg` reading `version = 3.11.9`, the directory `chmod 555`; when `bin/test` runs; then the floor refusal prints, a sentence names the ignore it could not write, and the process exits with the refusal's own code and no traceback | A case that runs the runner against that fixture and asserts stderr and the exit code, seen red first |
| The sentence says what it costs the reader | Given the same; when the sentence prints; then it names the path and says the directory will appear in `git status` | The same case, asserting the wording (contract §14) |
| A writable `.venv` is unchanged | Given an ordinary `.venv`; when the runner exits by any path; then `.venv/.gitignore` is written exactly as before and nothing extra prints | The six existing `hide_from_git` cases staying green |
| The vocabulary case notices a new reach value | Given a sixth value added to `call_sites`' returnable set; when the suite runs; then a case goes red, or the limit is written down beside the case | Either a case derived from the function's own returnable set, or a written limit with grounds |

## Data & interfaces

No CLI change, no exit-code change. One guard inside an existing unit, one sentence, and one ledger caveat.

## Open questions → questions.md

Whether the sentence goes to stderr beside the refusal or to stdout is settled by the module's existing habit — every refusal in `ensure` writes to stderr — and needs nobody.
