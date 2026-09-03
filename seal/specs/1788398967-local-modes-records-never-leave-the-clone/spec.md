# Feature Specification: local mode's records never leave the clone

<!-- seal/specs/1788398967-local-modes-records-never-leave-the-clone/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §"Shared or local" → *Local mode gets an export/import pair* | The four bullets are the contract: what the zip holds, that import never overwrites, that the pair is the mode switch, and the one reminder |
| `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself" | `seal/` at `<repo>/seal/` or `<git-common-dir>/seal/` is both the opt-in and the mode. No config key, so the command reads the mode the same way every gate does |
| `seal/README.md` §"Export rules — drain before closing" | A different sense of *export* already lives in the root. This work must not make the word ambiguous — see Scope |
| `CONTRIBUTING.md` §"Hooks stay local and quiet" | A hook may not write outside the repository. This is not a hook: a person types it and names where the zip goes. The distinction is why the default output sits beside the clone rather than inside it |

## Scope

**In.** One command, `seal`, with two subcommands and one flag:

- `seal export` — write the local-mode root to a zip, with a manifest.
- `seal export --check` — print the one-line reminder, write nothing.
- `seal import <zip>` — merge a zip's records into this clone's root, never
  overwriting anything.

Plus `bin/seal` and `bin/seal.cmd` (the POSIX/Windows wrapper pair every
shipped command has), one new helper in `hooks/optin.py` so both modes'
roots have a single address, and the documents that already promise this
pair.

**Out.**

- Uploading anywhere. Where the copy goes is the user's business
  (`docs/one-root-by-lifetime.md`: "Nothing is uploaded anywhere").
- Syncing, merging file contents, or resolving a collision. A copy is not a
  sync; last copy wins is the user's call, made by reading the two files.
- Deleting anything. Neither subcommand removes a file from the root.
- Running `evidence-check`. Import names it; it does not run it.
- A `settle` step, retention, or any change to what a release folds.

**The word "export" now has two senses in this repository, and they are not
merged.** `seal/README.md`'s *Export rules* are about draining an open list
into its durable home before a work item closes — nothing to do with a zip.
This document uses **export** for the zip only, and every message this
command prints says *zip* or names the file, so a reader never has to guess
which sense is meant.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given a local-mode repository, when `seal export` runs, then a zip is written outside the working tree, named `seal-<repo>-<date>.zip`, holding `manifest.json` and every file of the root under `seal/` | `tests/test_the_records_can_be_carried_out_and_in.py` — read the zip's namelist |
| S2 | Given session state (`specseal-implementer`, `specseal-worktree-choice/`, `specseal-reviewed`, `specseal-parity`, `specseal-scratch`, a lease file) beside the root in the git dir, when `seal export` runs, then no member of the zip names any of them | S2 case: build all six, export, assert the namelist |
| S3 | Given a symbolic link inside the root pointing at session state beside it, when `seal export` runs, then the link is skipped, its path is reported, and the target's bytes are not in the zip | S3 case, skipped where symlinks are not permitted |
| S4 | Given a local-mode repository with a remote and a HEAD, when `seal export` runs, then `manifest.json` names the remote URL, the HEAD SHA, the mode, the UTC timestamp, the format number, and a digest per work item | S4 case: read the manifest out of the zip |
| S5 | Given a zip whose records are absent from this clone, when `seal import` runs, then each file is added at its path under the root and counted as added | S5 case |
| S6 | Given a file already at that path with different bytes, when `seal import` runs, then the incoming copy lands beside it as `<name>.incoming<ext>` — `ledger/<id>.incoming.md` beside `ledger/<id>.md` — the existing file is byte-identical to before, and the collision is reported | S6 case: compare bytes before and after |
| S7 | Given a file already at that path with identical bytes, when `seal import` runs, then nothing is written for it and it is counted as identical | S7 case: importing the same zip twice writes nothing the second time |
| S8 | Given a collision whose `.incoming` sibling already exists with different bytes, when `seal import` runs, then the copy lands as `<name>.incoming-2<ext>`, and nothing is ever overwritten | S8 case |
| S9 | When `seal import` runs, then it asks no question — it reports and exits — and it prints the `evidence-check` command as the next step | S9 case: run with stdin closed, read stdout |
| S10 | Given a local-mode repository, when `seal import --into shared` runs, then `<repo>/seal/` is created and the records land there; the reverse holds for `--into local` | S10 case, both directions |
| S11 | Given both roots already exist, when `seal import` runs — with `--into shared`, with `--into local`, or with neither — then it refuses, names both paths and which one the gates read, and writes nothing | S11 case, all three spellings |
| S12 | Given a shared-mode repository, when `seal export` runs, then it writes no zip, exits 1, and names the mode, the committed path, and the `mv` command that switches to local mode | S12 case |
| S13 | Given a local-mode repository and a manifest of the last export, when `seal export --check` runs, then it prints exactly `N work items changed since the last export` and nothing else, and writes nothing | S13 case: compare stdout to the exact line |
| S14 | Given no manifest of a last export, when `seal export --check` runs, then it prints one line saying how many work items are here and that no export has happened | S14 case |
| S15 | Given a shared-mode repository, when `seal export --check` runs, then it prints one line saying the records are committed and exits 0 — a release script that always runs it never fails on it | S15 case |
| S16 | Given a repository that is not opted in, when either subcommand runs, then it exits 1 naming both places `seal/` is looked for | S17-family case |
| S17 | Given a path that is not a zip, or a zip that is truncated, when `seal import` runs, then it exits 1 naming the file, and the root is untouched | S17 case: assert the root's file list is unchanged |
| S18 | Given a zip whose manifest names another repository's remote, when `seal import` runs, then it refuses, prints both URLs, names `--allow-other-repo`, and writes nothing — and with that flag it proceeds | S18 case, both halves |
| S19 | Given a zip holding a member named `../escape.md`, `/etc/passwd`, `C:\x`, `a\..\..\b`, or a symlink entry, when `seal import` runs, then it refuses the whole zip before writing anything, naming the member | S19 case, one per shape |
| S19b | Given a zip whose members declare more bytes unpacked than a root of records holds, when `seal import` runs, then it refuses before writing anything | S19b case: a 408 KB zip declaring 400 MB |
| S19c | Given a destination where any path a member would take is a symbolic link — a directory above it, or the record's own name — when `seal import` runs, then it refuses the whole zip, naming the path | S19c case, the leaf and a directory |
| S19d | Given a destination where the `.incoming` name a collision falls back to is a symbolic link, when `seal import` runs, then the copy lands past it, inside the root, and nothing is written through it | S19d case, and a case handing the write that name directly |
| S17b | Given a zip whose central directory is well formed and one member's data does not match its checksum, when `seal import` runs, then it refuses before writing any record | S17b case: corrupt the second of two records |
| S17c | Given a zip holding a member this build cannot read at all — encrypted, or compressed by a method it has no decompressor for — when `seal import` runs, then it prints a line of its own rather than a traceback, and writes nothing | S17c case: the compression method set to 99 |
| S19e | Given a zip whose members and the root together need a name as both a file and a directory, when `seal import` runs, then it refuses before writing any record | S19e case, both sides: the clash inside the zip, and the clash against the root |
| S19f | Given a zip holding more members than a root of records has files, when `seal import` runs, then it refuses before writing any record | S19f case: one over the bound |
| S19g | Given a name that becomes taken between the moment the import chooses it and the moment it writes, when `seal import` runs, then that record is named in the report rather than dropped, and the run still exits 0 | S19g case: the write handed the name a raced check would hand it |
| S17d | Given a directory in the root the copy cannot write into, or a disk with no room, when `seal import` runs, then it stops with a line of its own saying a second run finishes the copy | S17d case: a directory with its write bit cleared |
| S1b | Given a symbolic link at the name the export writes through — the zip's own name or its `.partial` — when `seal export` runs, then nothing is written through it: the temporary name refuses, and the zip's name is treated as taken | S1b case, both names |
| S20 | Given a zip with no `manifest.json`, or one whose `format` is a number this build does not know, when `seal import` runs, then it exits 1 saying so | S20 case |

## Data & interfaces

### The zip

```
seal-<repo>-<date>.zip
├── manifest.json          format, mode, remote, head, exported_at, items
└── seal/                  every file of the root, at its path under it
    ├── README.md  ledger.md  follow-up.md  parity.md  config.md
    ├── ledger/<work-item-id>.md
    └── specs/<work-item-id>/…
```

`<repo>` is the repository directory's basename with anything outside
`[A-Za-z0-9._-]` replaced by `-`; `<date>` is the UTC day, `%Y-%m-%d`. The
file is never overwritten: a second export on the same day writes
`seal-<repo>-<date>-2.zip`.

**What is never in it.** Everything beside the root in the git directory —
the smith mark (`specseal-implementer`), the worktree choices
(`specseal-worktree-choice/`), the review and parity marks
(`specseal-reviewed`, `specseal-parity`), the throwaway opt-out
(`specseal-scratch`), any lease file, and the last-export manifest
(`specseal-last-export.json`). The root being its own directory is what makes
this structural rather than a list to maintain — the export walks the root
and nothing else. A symbolic link is the one way out of that, so links are
skipped and reported rather than followed.

### `manifest.json`

| Field | Holds |
|---|---|
| `format` | `1`. An import refuses a number it does not know rather than guessing at fields |
| `mode` | `"local"` or `"shared"` — where the root sat at export |
| `remote` | `origin`'s fetch URL, or `""` when the repository has no `origin` |
| `head` | the HEAD SHA at export, or `""` in a repository with no commit |
| `exported_at` | UTC, `%Y-%m-%dT%H:%M:%SZ` |
| `items` | `{work item id: digest}` — what the reminder compares against |

`remote` and `head` are the manifest's whole reason for existing: they are
what lets an import say *this zip is from another repository* instead of
merging one project's records into another's.

### The digest, and the seam it must not have

A work item's digest covers every file under `seal/specs/<id>/` **and**
`seal/ledger/<id>.md` when it exists — the two places one work item writes.
It is SHA-256 over, for each file in sorted order, its `/`-joined path
relative to the root, a NUL, the byte length, a NUL, and the bytes.

**One walker produces both lists.** The files the zip holds and the files the
digest covers come from the same function, and a test asserts the zip's
member list equals what that function yields. A check assembled from two
enumerations drifts at the seam: the manifest would then record what one of
them saw and the reminder would compare against what the other one sees, and
the difference would read as a changed work item.

The same rule fixes the symlink case. Links are excluded by the walker, so
they are absent from the zip and from the digest together; excluding them in
one place only would make every export of a repository holding one report a
change that nothing made.

### The reminder's state

`<git-common-dir>/specseal-last-export.json` holds the manifest of the last
export, written after the zip is complete. It sits beside the root rather
than inside it for the reason everything else there does: it is this
machine's state, not a record, and nothing that leaves this clone should
carry it.

`N` counts work items whose digest differs from the manifest's, plus those
present now and absent from it, plus those in it and absent now. Root-level
files (`ledger.md`, `follow-up.md`, `config.md`, `parity.md`) are **not**
counted — the line the design specifies says *work items*, and Q1 in
`questions.md` is where that gap is recorded rather than silently widened.

### Exit codes

| Code | Meaning |
|---|---|
| 0 | the zip was written · the import finished · `--check` printed its line |
| 1 | nothing was written, and the message says why |

There is no third code. Every refusal in this document is a 1 with a message
naming the file, the path, or the flag that gets past it.

## Fail directions

Each of these is a state the command must recognise, and the direction it
fails in is stated because a wrong refusal costs a message and a wrong
acceptance costs records.

| State | What happens | Why that direction |
|---|---|---|
| No `seal/` at either place | exit 1, naming both places | A command that created a root on its own would pick the mode for the user, which is the one question first setup exists to ask |
| `.git/specseal-scratch` present | exit 1, naming the marker | The repository is declared throwaway. Saying so beats exporting records from a fixture |
| Shared mode, `seal export` | exit 1, naming the mode, the path, and the `mv` that switches to local | A zip of committed files is a second copy that nothing keeps current, and git already carries the first. The message answers the question the user was really asking |
| The output path is inside the working tree | written, with a warning naming the risk | The default is never inside the tree; a path the user named is the user's call, and refusing it would make `--output` a suggestion |
| Not a zip, or truncated | exit 1, root untouched | `zipfile.BadZipFile` and a short read are the same answer to the user: this file is not a copy of anything |
| A member escapes the root | the whole zip is refused before a byte is written | Every member's name is validated first, and one bad member refuses the archive rather than the member: a zip carrying one is not a zip to take a partial copy from. See *What `extractall` does and does not do* below — this is defence that does not depend on a standard-library sanitiser |
| A member is a symlink entry | the whole zip is refused, naming it | A link written into the root is a way to reach outside it on the NEXT export, which is the loop the export's own link handling closes from the other end |
| Any path inside the destination root is a symbolic link — a directory above the member, or the member's own name | the whole zip is refused, naming it | This is the way a member still lands outside the root, and it is the clone's own state rather than the zip's — so the person removes the link and gets a complete copy, instead of a partial one now. The leaf counts: a link named `ledger/w1.md` whose target does not exist reads as absent, so the member is called ADDED and `open()` follows the link out (measured 2026-09-03, round 1) |
| A member declares more bytes unpacked than a root of records holds | the whole zip is refused, naming the member and the limit | Each member is read whole, and the zip is another machine's file: the declared size is the sender's choice, not this root's contents. Measured 2026-09-03: 408 KB on disk declaring 400 MB wrote 419 MB and took as much memory, in 0.2 s |
| A zip declares more bytes unpacked in total than a root of records holds | the whole zip is refused, naming the total and the limit | Twenty members each under the member limit is still more than this command will read. Summed before the manifest is parsed, because that read is unbounded too: the manifest is exempt from the member limit, so a 400 MB one took 400 MB of memory before anything refused it |
| A member's data does not match its checksum | the whole zip is refused, naming the member | `read` raises on a bad CRC, and the write loop used to meet that with records already on disk and no line of this command's own printed. Every other refusal here happens before the first byte |
| A member is encrypted, or compressed by a method this build cannot read | the whole zip is refused, naming the member | `testzip` catches a bad checksum itself and answers with the name; these two leave it as `RuntimeError` and `NotImplementedError`, and reached the console as tracebacks where every other refusal here prints a line of its own |
| A name has to be a directory for the zip and is a file — in the zip, or already in the root | the whole zip is refused, naming the path | `os.makedirs` raises on it mid-write, with the records before it on disk. The sender needs to corrupt nothing, only to name two members that way, and the root's own contents raise it too |
| A zip holds more members than a root of records has files | the whole zip is refused, naming the count | Both size bounds count bytes, and a member declaring zero bytes passes the member one and adds nothing to the total |
| The `.incoming` name a collision falls back to is a symbolic link | that name is treated as taken, the copy lands at the next one, and the import exits 0 | The member's own name is refused because losing the record is the alternative. Here there IS a next name, so stepping past the link keeps the copy and writes nothing through it |
| A name the export would write through is a symbolic link — the zip's name or its `.partial` | nothing is written through it: the temporary name refuses the export, and the zip's name is taken so the zip lands at the next | The `.partial` name is predictable and beside the clone, so a link there took every record outside it at exit 0. There is no benign reading of that name; the zip's own name a person may well have made a link, so it is stepped past rather than refused |
| Something is already at the export's temporary name | the export refuses and **leaves it there** | The cleanup that removes a half-written archive is for a name this call created. It used to run on the refusal too, so a link, somebody's file, or a concurrent export's zip in flight was removed by the run that had just declined to touch it |
| A record's name is taken between the moment it is chosen and the moment it is written | that record is named in the report and the rest of the copy finishes | The report used to read `0 files added`, which a person reads as an empty zip rather than as a name something took in between |
| A directory in the root cannot be written into, or the disk is full | the copy stops with a line naming what the filesystem said | The one failure that cannot happen before the first byte. This command overwrites nothing, so a second run finishes the copy — which is what the message says |
| The manifest names another remote | exit 1 printing both URLs and naming `--allow-other-repo` | Merging another project's records is silent corruption spread across files keyed by id; a refusal is one flag away from being wrong and costs a message |
| Both roots exist | exit 1, naming both and which the gates read | Writing into one while the other exists leaves a dead root the hooks never read, which is worse than a stop |
| A collision that already has an `.incoming` sibling | numbered, never overwritten | Losing the second copy silently is the only outcome worse than a file with a long name |

### What `extractall` does and does not do

This document said, before the code was written, that `ZipFile.extractall` is
the classic path-traversal sink. **Measured on 2026-09-03 under CPython 3.13
and 3.12, that is false**: `extractall` strips `..` segments and a leading
`/` from a member's name, and writes a symbolic-link entry as an ordinary
file. A zip of `seal/../../escaped.md` extracted into `<dest>/seal` wrote
`<dest>/seal/escaped.md` and nothing outside.

What actually disqualifies it, in the order that matters:

1. **It overwrites.** That is the one rule this command exists to keep, and
   it settles the question on its own.
2. It writes members this format has no place for. `a\..\..\b.md` landed in
   the destination as a literal file on POSIX.
3. **It follows a symbolic link already in the destination** — and so does
   a plain `open()`. A zip of `specs/<id>/spec.md` extracted into a root
   whose `specs` is a link wrote through it. This is the escape that
   measured, so it is the one the command checks for, before writing
   anything. Not directories alone: round 1 measured a broken link named
   `ledger/w1.md` taking a record outside the root at exit 0, because
   `os.path.exists` follows a link and reports a broken one absent.

The name validation stays regardless. A defence that holds only while a
standard-library sanitiser keeps its current shape is not a defence this
work can claim, and a refusal naming the member says what happened where a
silent sanitise leaves a file under a name nobody chose.

### How two remote URLs are compared

The URL is normalised before comparison: the scheme is dropped, a `user@`
prefix is dropped, the scp-style `host:path` colon becomes `/` **only when
the original carried no scheme** (so a port in `https://host:8443/x` is left
alone), a trailing `.git` and a trailing `/` are dropped, and the result is
lowercased. So `git@example.com:org/repo.git` and
`https://example.com/org/repo` are one repository.

Guessing wrongly in the accepting direction would need two different
repositories to normalise to the same host and path, which is the same
repository. Guessing wrongly in the refusing direction costs a message that
names the flag. That asymmetry is why normalisation is done at all rather
than comparing the strings.

## Open questions → questions.md

Q1 (what the reminder counts) and Q2 (whether `seal` should grow further
subcommands) live there, each with the default this work builds to.
