# 1790174139-survivors-md-silences-what-it-quotes — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8dc9390c |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Give a deeper exemption file its owner (#304): `OWNER_DIR`'s tail reads the
`seal/specs/<id>` prefix at any depth, so the ownership test in
`whole_range` — unchanged — reaches a `survivors.md` one directory below the
layout and refuses it with `not yours` when the range touches nothing of
that work item. Case S7, seen red first, holding the layout position
unchanged as its other arm. S8: every regular expression in the module that
reads a path segment, enumerated from the source with what a deeper path
does to it, written here.

## What this phase found

**Seen red, executed at `95956de8`**, the case parametrised over two depths:
`test_a_declaration_one_directory_deeper_still_has_an_owner[deeper/]` —
`a declaration whose range touches nothing in its own work item excused the
run, at depth 'deeper/'; exit 0` — and the `[]` arm green, which is today's
behaviour at the layout position and is what the change must not move.
After: `69 passed` (67 after phase 2), exit 0 read directly; ruff on the two
files exit 0.

**S8 — every pattern in the module that reads a path, from the source
(`grep -n re.compile`, then every `split("/")`, `startswith`, `endswith`,
`basename` and `.match` on a path):**

| Pattern or reader | What it reads | What a deeper path does to it |
|---|---|---|
| `OWNER_DIR`, `(?:^|.*/)(seal/specs/[^/]+)/.+$` | the work item a `--exempt` file belongs to, off the file's own path | **The one whose tail stopped a segment short.** Was `/[^/]+$`: a file one level deeper matched nothing, had no owner, and was never asked the question. Now `.+$`, so the owner is the prefix at any depth. Not anchored at the start because `--exempt` paths may be absolute; a file outside any `seal/specs/<id>/` still has no owner and keeps the hand-run reach `whole_range` documents |
| `WORK_ITEM_DIR`, `^((?:seal/)?specs/[^/]+)/` | the work item directory a range path is under, for `retired_directories` | Anchored at the start and reads a prefix, so a deeper path matches and yields the same directory. Not a hole |
| `records_a_past_round` — `"rounds" in parts and "specs" in parts[: parts.index("rounds")]` | a round record or report, by segments | Any depth beneath `rounds/` matches, and a `rounds/` any depth below `specs/` matches. Unchanged |
| `records_a_past_state` — `inside == ["survivors.md"]` or `inside[0] == "phases"` | the class this work item widened, by the segments after `specs/<id>/` | `survivors.md` has to be directly under the work item directory: a deeper one is prose and stays in the sweep, on purpose — it is `OWNER_DIR`'s question, not this one's. Anything under `phases/` matches at any depth |
| `retired_directories` — `os.path.basename(directory)`, `path.startswith(d + "/")` | the directories a range retired, and the paths under them | Prefix tests; a deeper path under a retired directory is left out with it. Unchanged |
| `whole_range` — `path.startswith(owner.group(1) + "/")` | whether the range touches the declaring work item | Prefix test over the changed-file list, which is unfiltered by design (`NAMED_EXCEPTION`); a deeper changed path counts as touching. Unchanged |
| `exempted` — `target.endswith("/" + where.lstrip("/"))` | whether a row's path names the candidate | Suffix test, so a row written from another directory still holds. Unchanged |
| `RANGE_CELL`, `^[^\s|]+\.\.\.?[^\s|]+$` | the FIRST CELL of a row, to tell a range row from a path row | Reads a cell rather than a path; depth does nothing to it. **One observation outside this ticket**, recorded for the next reader: the pattern needs a non-space run on both sides of the dots, so `../notes.md` is a path as documented, but a path cell spelled `a/../b.md` matches it and is read as a range, which then prints under `unresolved` rather than silencing anything. Loud, and no row in the tree is spelled that way |
| `STRUCK`, `WORD`, `BLOCK`, `END` | text, never a path | — |

**The frame holds** for this phase: `OWNER_DIR`'s tail was as `spec.md`
§*Data & interfaces* describes, the `NAMED_EXCEPTION` list stays unfiltered,
and the ownership test needed no change. The pre-0.4.0 `specs/` root is left
out of `OWNER_DIR` as `spec.md` §*Out* says, with the comment above the
pattern now saying so.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
