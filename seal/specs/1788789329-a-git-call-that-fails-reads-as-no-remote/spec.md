# Feature Specification: a git call that fails reads as no remote

<!-- seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

Ticket #111. `git()` in `skills/implement/scripts/seal.py` answers `""` for
every failure — an `OSError`, a timeout, a non-zero exit — and four of its
five call sites read that `""` as a fact about the repository rather than as
a failure to answer. The sharpest of them switches off the refusal that keeps
another project's records out of this root.

## Grounding

This repository has no `docs/policies/` root, so the SDD set is the root of
judgment. Two documents outrank this file all the same, and one prior spec
governs the fields being changed.

| Clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §*What each mode gives up* | `seal export` / `seal import` are the only way local-mode records reach another machine, so a refusal here is the last gate before two projects' records key into one root |
| `seal/specs/1788398967-local-modes-records-never-leave-the-clone/spec.md` §`manifest.json` | The prior contract for the `remote` and `head` fields. **This work supersedes two of its rows** — see *What this supersedes* below |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Every URL in the new cases is `example.com` |

### What this supersedes

The #81 spec's `manifest.json` table reads:

| Field | Holds (as #81 wrote it) |
|---|---|
| `remote` | `origin`'s fetch URL, or `""` when the repository has no `origin` |
| `head` | the HEAD SHA at export, or `""` in a repository with no commit |

Both rows have exactly two states where the machine writing them has three,
and the third state is what this work item exists for: **the question could
not be answered.** #81 was right about what the fields mean when git answers;
it had no spelling for git not answering, so the export froze `""` into the
zip and the importing machine read it as a fact.

The #81 records are left as they stand — they are the record of what was
decided then, and rewriting a shipped work item's spec would make it a record
of nothing. The new contract is the table under *Data & interfaces* here.

## Scope

**In.** Every call site of `git()` in `skills/implement/scripts/seal.py`
whose caller cannot tell `""`-because-absent from `""`-because-unanswerable —
enumerated below, all five of them. The refusal, its flag, its message; the
manifest's two fields and every reader of them; the sentence
`other_worktrees` is owed. The user-facing documentation of the new flag in
both READMEs, and the cases that pin all of it.

**Out.** `porcelain`, `indexed`, `tracked`, `gitlinks_under_root` and the two
`git add` sites already read their own return code and each already draws the
line this work is about; rewriting them to go through the new helper is a
refactor this ticket did not ask for. `hooks/optin.py`'s own subprocess calls
are a different module with different callers.

## The class, enumerated by construction

**Method.** The class is *every call site of `git()` in `seal.py`*. A call
site is the function's name followed by `(`, so `grep -n 'git(' <file>`
names every one of them by construction rather than by reading. It returns
nine hits; three are prose about `git()` inside a comment or a docstring
(`:1571`, `:1748`, `:1981`) and one is the definition (`:139`), leaving five.
A call reached through a reference (`f = git`) would escape that grep, so
`grep -n '\bgit\b'` was run as the cross-check and shows no such binding.

Coordinates are at `86e140f`, before this work item's first edit.

| # | Line | Caller | What the caller reads `""` as | Can it tell? | Disposition |
|---|---|---|---|---|---|
| 1 | `:322` | `manifest_of`, the `remote` field | "the exporting clone has no `origin`" | **no** | **fixed** — the field is absent when the question could not be answered |
| 2 | `:323` | `manifest_of`, the `head` field | "the exporting clone has no commit" | **no** | **fixed** — the field is present only when a SHA was actually read |
| 3 | `:947` | `import_`, `here` | "this clone has no remote, so the other-repository check does not apply" | **no** | **fixed** — an unanswerable question refuses, with a flag of its own |
| 4 | `:953` | `import_`, the refusal message | "this clone is " — printed blank inside a refusal | **no** | **fixed** — the value read at `:947` is reused, so the second call goes away entirely |
| 5 | `:1476` | `other_worktrees` | "this clone has no other worktrees" | **no** | **safe** — the note is advisory, nothing is lost and nothing is claimed falsely. It gains the sentence saying the silence is by design |

**The real count is five call sites, not four.** The ticket said *"four are
left"* and listed `:322`, `:323`, `:947` and `:1476`; it did not count
`:953`, the second `git()` inside the refusal message. Four of the five need
a behaviour change and one needs a sentence, so *four* is also the count of
sites that change — but it is a different four from the ticket's, and the
partition matters: `:953` is a call site inside a refusal, and a refusal that
prints a blank where it promised a URL is the failure mode of this whole
ticket appearing in the message that reports it.

## The judgment the owner made, and what it costs

**An unreadable remote refuses**, and the escape is a flag of its own rather
than `--allow-other-repo`. Answered by the repository owner before the first
edit, in the batch `routing.md` records.

The grounds are the ticket's own sentence: *"there is no remote"* and *"the
question could not be answered"* are different facts. Routing both past one
flag would merge them again at the only place a user acts on the distinction
— a person typing `--allow-other-repo` is saying *I know these two spellings
are one repository*, which is a claim about two URLs they have both read. A
person whose git just timed out has read neither and is saying something
else: *import anyway, without the check*.

What refusing costs, stated rather than left to be found: a transient git
failure — a held `index.lock`, a `.git/config` mid-edit, a timeout on a slow
filesystem — now stops an import that would previously have proceeded. The
message names the git failure's own cause, so the ordinary answer is to run
it again; the flag is for a machine where the failure is not transient.

### The flag is `--allow-unreadable-remote`

Three names were weighed.

| Name | Why not |
|---|---|
| `--allow-other-repo` (reuse) | Merges the two facts again, which is the thing the owner's answer refuses |
| `--no-remote-check` | Names the mechanism, not the fact. It reads as *switch the check off*, which is also what a user with a genuinely different remote would reach for — and that is `--allow-other-repo`'s job |
| `--allow-unreadable-remote` | **Chosen.** Names the fact the user is accepting, mirrors `--allow-other-repo`'s `--allow-<what you are accepting>` shape, and cannot be misread as covering a remote that was read and differed |

## The rule the new helper applies, and why it is one rule

`git config --get remote.origin.url` **exits 1 with nothing on either stream
when the key is not set**, which is a repository with no remote and not a
failure to answer. Measured 2026-09-07 against git 2.50.1:

```
config --get, no remote:            (1, '', '')
config --get, broken config file:   (128, '', 'fatal: bad config line 9 in file .git/config')
rev-parse HEAD, unborn:             (128, 'HEAD', "fatal: ambiguous argument 'HEAD'...")
```

So the rule is: **exit 0 means git answered; exit 1 from `config --get` means
the key is not set; everything else is the question going unanswered.** That
is the same direction `porcelain` (`:1365`), `indexed` (`:1395`) and
`gitlinks_under_root` (`:1745`) already take, stated by the last of them as
*the unanswerable question refuses*.

`--default ""` was measured too and would collapse the unset case into exit 0
with empty output, removing the one special case. It is not taken: `--default`
arrived in git 2.18, and nothing else this plugin runs needs a git that new.
Depending on it would turn an old git into a refusal on a path that works
today, which is a compatibility break bought for one line of tidiness.

## The shape, and why it is not a fourth spelling of an existing one

`gitlinks_under_root` runs `subprocess.run` itself and returns
`(entries | None, why)` because `git()` cannot say *why*. `porcelain` does the
same with a list. Writing a third such body here would be the fourth spelling
of one idea.

Instead the shape is **promoted into one place**: `git_asked(root, *args)`
returns `(stdout stripped, "")` or `(None, why)`, and `git()` becomes a
one-line wrapper over it that turns `None` into `""`. There is then exactly
one `subprocess.run` for the general case, `git()`'s contract is unchanged
for every caller that is right to ignore the distinction, and the two callers
that need it ask through `remote_url` and `head_sha`, which are `git_asked`
plus the one fact each command's exit codes carry.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | An unreadable remote refuses the import | Given a clone whose `.git/config` git cannot parse, when `seal import <zip>` runs, then it exits 1, writes nothing, names git's own message, and names `--allow-unreadable-remote` | case: broken `.git/config`, assert exit 1, `bad config line` in the output, and the root still empty |
| S2 | The flag lets it through | Given the same clone, when `seal import <zip> --allow-unreadable-remote` runs, then the records are written and it exits 0 | same fixture, with the flag |
| S3 | A repository genuinely without a remote still imports | Given a clone with no `origin`, when `seal import <zip>` runs, then it exits 0 and writes the records | case: no `git remote add`, assert exit 0 |
| S4 | `--allow-other-repo` does not cover an unreadable remote | Given the broken-config clone, when `seal import <zip> --allow-other-repo` runs, then it still refuses | the two flags are separate opt-ins |
| S5 | A zip whose manifest records no remote refuses | Given a zip whose `manifest.json` has no `remote` key, when `seal import` runs, then it refuses and says the exporting machine could not read one | hand-built zip with the key omitted |
| S6 | A manifest recording an empty remote still imports | Given a zip whose `manifest.json` has `"remote": ""`, when `seal import` runs, then it exits 0 | the exporting repository genuinely had no `origin`; this is the state every existing hand-built fixture is in |
| S7 | The export omits a remote it could not read | Given a clone whose `.git/config` git cannot parse, when `seal export` runs, then `manifest.json` has no `remote` key | read the manifest out of the zip, assert `"remote" not in manifest` |
| S8 | The export records an empty remote it could read | Given a clone with no `origin`, when `seal export` runs, then `manifest.json` has `"remote": ""` | assert the key is present and empty |
| S9 | The export omits a HEAD it could not read | Given a repository with no commit, when `seal export` runs, then `manifest.json` has no `head` key | supersedes #81's S-case asserting `head == ""` |
| S10 | The refusal for another repository prints the URL it actually read | Given a zip from another repository, when `seal import` runs, then both URLs are printed and neither is blank | the value read once is the value printed |
| S11 | `other_worktrees` says its silence is deliberate | — | the docstring names it; `tests/test_docs_line_wrap.py` and the reader tests stay green |
| S12 | Both flags are documented where a person looks | Given `README.md` and `README.ko.md`, then each names `--allow-unreadable-remote` and what it accepts | grep; `tests/test_the_pull_request_language_is_the_repositorys.py` keeps the two READMEs paired |

## Data & interfaces

`manifest.json`, format `1` — unchanged number, because no field moved and no
name changed. What changed is that two fields may now be **absent**, and
absence is a state a format-1 reader already handles: `import_` reads both
through `manifest.get(...)` and `read_manifest` checks only the object and
its `format`.

| Field | Holds |
|---|---|
| `remote` | `origin`'s fetch URL; `""` when the repository has no `origin`; **absent when git could not answer** |
| `head` | the HEAD SHA at export; **absent when git could not answer**, which includes a repository with no commit |

`head` has no empty state any more. `git rev-parse HEAD` prints a SHA when it
succeeds and exits non-zero otherwise, so *present* and *a SHA was read* are
now the same thing.

**Every reader of the manifest**, enumerated the same way — `grep -n
'manifest' skills/implement/scripts/seal.py` plus `grep -rn 'manifest'
hooks/ .github/ skills/ --include='*.py'`, which returns nothing outside
`seal.py`:

| Reader | Reads | Absence is |
|---|---|---|
| `import_` `:947-961` | `remote` | **new behaviour** — refuses unless the flag is passed |
| `import_` `:1039-1041` | `head`, `exported_at` | already handled: `manifest.get` → `None` → `isinstance(head, str)` is false → the closing line does not print |
| `check()` via `read_state` `:2086` | `items` only | not affected; the reminder never reads `remote` or `head` |
| `read_manifest` `:732` | `format` only | not affected |

The new command-line surface:

```
seal import <zip> [--into shared|local] [--allow-other-repo]
                  [--allow-unreadable-remote]
```

`--allow-unreadable-remote`: *import although the remote could not be read on
one side or the other*.

## Open questions → questions.md

The one open judgment the ticket named was answered by the repository owner
before the first edit and is recorded in `routing.md` and above. Nothing else
needs a person; `questions.md` records that and the assumptions taken in
writing.
