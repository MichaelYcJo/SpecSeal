# 1788789329-a-git-call-that-fails-reads-as-no-remote — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 64aa0c6 |
| Ran by | unknown — the spawn prompt named no model, and the template forbids a segment sourcing this from its own idea of what it is. The orchestrator that spawned this segment is the party that can fill it |

## What this phase was asked

Deliver the half of the fix that sits on the exporting machine: a helper that
can say *why* git did not answer, and a manifest that leaves out what it could
not read.

Specifically — `:322` and `:323` of `skills/implement/scripts/seal.py`,
`manifest_of`'s `remote` and `head`. The ticket's answer for this side is that
a field that could not be read should be **absent** rather than empty, so the
receiving machine can tell. The shape has to reuse the direction
`gitlinks_under_root` (`:1745`), `porcelain` (`:1365`) and `indexed` (`:1395`)
already take rather than becoming a fourth spelling of it.

## What this phase found

**`git config --get` exits 1 when the key is not set, so "non-zero is a
failure" is not the rule for that one command.** Measured 2026-09-07 against
git 2.50.1: an unset `remote.origin.url` gives `(1, '', '')` and a
`.git/config` git cannot parse gives `(128, '', 'fatal: bad config line 9 …')`.
That is what shaped `git_asked`'s `answered=(0,)` parameter — the one place a
caller can say which return codes count as an answer. Without it, `remote_url`
would have had to run its own `subprocess.run` and the promotion would have
bought nothing.

**`--default ""` would remove that special case and is not taken.** Measured
in the same run: `git config --default "" --get remote.origin.url` exits 0
with empty output when unset. It arrived in git 2.18 and nothing else this
plugin runs needs a git that new, so leaning on it would turn an old git into
a refusal on a path that works today.

**The unreadable case cannot be built out of a repository on disk, and phase 2
inherits that.** A `.git/config` broken badly enough to fail `git config
--get` also fails the `git rev-parse --show-toplevel` that resolves the root,
so the command stops one screen earlier with a different message — both exit
128, measured. A duplicated `url =` line does not work either: `--get` answers
with the last value at exit 0. So the cases inject the failure at
`subprocess.run`, one git question deep, and everything above that seam runs
for real. The helper `git_cannot_answer` in
`tests/test_the_records_can_be_carried_out_and_in.py` carries that reasoning
and phase 2's cases use it unchanged.

**`""` had to keep meaning *no remote*, and that decided the direction of the
whole change.** Twenty-two hand-built manifests in the export/import module
write `"remote": ""`. Making `""` the unreadable state would have edited all
twenty-two, and each edit is a chance to change what a case was pinning. The
design instead adds a third state — absent — which no existing fixture is in.

**One gate fired on this phase's own docstring.**
`tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one`
read `git 2.50.1` as a release timer, because 2.50.1 is above the running
0.9.0 by arithmetic. It is another product's version and the check has a
declaration for exactly that, already used once for this same file, so the
number stays and `VERSIONS_OF_ANOTHER_PRODUCT` gains a row. An exit code read
off an unnamed git is not a measurement.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `remote` and `head` keys' guarantee of being present in every manifest this build writes | `spec.md` §*Data & interfaces* now carries the three-state contract, and `manifest_of`'s own docstring carries it beside the code. The one reader of those fields, `import_` `:1039-1041`, already went through `manifest.get` and needed no change |
| `git()`'s `subprocess.run` body | `git_asked`, which `git()` now calls. No caller of `git()` changed |
