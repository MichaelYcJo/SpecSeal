# 1788229400-every-branch-appends-to-the-same-two-files

Rows for the work item that closed #46 and #52.

A coordinate here names content, never a position: a symbol name where the
language has one, a distinctive line of text otherwise, and a hash of the
region under it. No row carries a line number or a commit, so nothing in one
goes stale for a reason unrelated to the claim it makes.

## A coordinate names content, not a position

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| An anchor resolves to a symbol span via the stdlib `ast`, or to a quoted line of text, and to nothing else | `skills/evidence-check/scripts/evidence_check.py#resolve@58939880`, `skills/evidence-check/scripts/evidence_check.py#py_spans@d0a9d678` | **Executed**: `handler`, `Box` and `Box.open` each resolve to their own span, decorators included, and a file that will not parse yields no symbols rather than a false match | 2026-09-01 | Decorators are in the span because a decorator carries behaviour. No dependency is added — `ast` ships with Python |
| A change inside the anchored region drifts; an edit that only moves the region does not | `skills/evidence-check/scripts/evidence_check.py#check_ledger@d3c038ca`, `skills/evidence-check/scripts/evidence_check.py#content_hash@5c2ba0ae` | **Executed against this repository's own ledger**, not only a fixture: inserting a statement into `_hides_a_commit` reports `1 drifted`, and inserting a line above everything in the same file leaves `34 ok` | 2026-09-01 | The second edit moved every line number in the file. Under the line-number scheme it was the case that read OK while pointing at the wrong lines |
| Trailing whitespace and blank lines are normalised away; indentation is not | `skills/evidence-check/scripts/evidence_check.py#normalise@e7d71707` | **Executed** at the unit and by mutation: normalising indentation too leaves a dedent silent, and that mutation turns exactly one case red | 2026-09-01 | In Python a dedent moves a statement out of the block it belonged to. A hash that shrugged at it would go quiet where the edit matters most |
| An ambiguous anchor is BROKEN, never a measurement | `skills/evidence-check/scripts/evidence_check.py#check_ledger@d3c038ca` | **Executed**: a line appearing twice reports `BROKEN … anchor is ambiguous — 2 places` and exits 2 | 2026-09-01 | With two places to look, an OK would be a claim about whichever one the code reached first |
| A markdown heading owns its section; a `#` comment in Python owns only its own block | `skills/evidence-check/scripts/evidence_check.py#text_regions@3f1f5b41` | **Executed**: `## A` runs past a nested `### A1` to the next `## B`, and the same bytes in a `.py` file are a comment run instead. Found by migrating the real ledger, where a 23-line comment block resolved to one line | 2026-09-01 | The level comparison survived a mutation until a nested heading was added to the fixture — the case had nothing to tell `k <= level` from `k is not None` |
| Re-verifying is a separate command, and the check never rewrites what it checks | `skills/evidence-check/scripts/evidence_check.py#reverify@959bd52b` | **Executed**: `--reverify` rewrites a drifted row's hash and names it; an ordinary run and a `--strict` run both leave the file byte-identical; a row whose anchor is gone is left alone | 2026-09-01 | A check that refreshed what it was checking would report OK for ever |

## The changelog fragments

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A fragment counts as gathered when its marker comment is in `CHANGELOG.md`, never by matching its text | `.github/scripts/gather_changelog.py#marker@b1e2b91c`, `.github/scripts/gather_changelog.py#fragments@3b0054db`, `.github/scripts/gather_changelog.py#ungathered@6c94ca94` | **Executed**: re-wording a released entry leaves `--check` green, and deleting the marker turns it red | 2026-09-01 | Matching the text works exactly once — the first copy-edit to a released entry would reopen its fragment forever |
| Gathering is idempotent and ordered by work item id | `.github/scripts/gather_changelog.py#fragments@3b0054db`, `.github/scripts/gather_changelog.py#ungathered@6c94ca94`, `.github/scripts/gather_changelog.py#section@e5fb4146`, `.github/scripts/gather_changelog.py#insert@c985894f` | **Executed**: a second run exits 1 with the entry present once, and the earlier id sorts above the later one in the written section | 2026-09-01 | The id is unix seconds, so the order is chronological and, more to the point, does not depend on the filesystem |
| The release pull request fails while a fragment is ungathered, and no other pull request runs the check | `.github/workflows/hygiene.yml#"echo "base is ${{ github.base_ref }} — fragments are gathered when the release reaches main"; exit 0"@0cb0ca06` | Read, not run — the branch condition is the same shape as the version-bump step above it at `:30`. The script's own two directions are executed | 2026-09-01 | On a feature pull request every fragment on the branch is legitimately ungathered, which is why the step skips itself |
