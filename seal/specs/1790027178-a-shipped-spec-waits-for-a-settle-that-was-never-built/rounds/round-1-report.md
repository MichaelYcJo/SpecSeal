# Round 1 — `settle`

Target SHA `0adf3ed3345cf33574dfa0ab011ad7d2584d9230`, branch
`feat/458-the-shipped-specs-are-sediment-no-check-reads`, base
`origin/release/v0.13.0`. HEAD was at the target SHA and the tree was clean
when this round started. Reviewed in a `git clone --no-local` at that SHA.

## How the findings hang together

One cause produces the first two. `settle --retire` removes a directory on one
condition — a `<!-- specs/<id> -->` line in some `.md` under `docs/` — and the
test for that line is weaker than the thing it is standing in for. It reads a
marker inside a fenced code block as a fold, and it reads a marker in a file
under `docs/` that is not a policy document as a fold. Both were reached with
the guard unsatisfied, and a work item's directory was removed in each.

Findings 3 to 5 are all the report telling a reader something the tree does not
say: that a repository in local mode has no work items, that an item the guard
is holding is waiting to be retired, and that nothing was ever folded when the
markers are still sitting in `docs/`.

Finding 6 is the interlock the spec rests on with nothing holding it in place.

---

## 🔴 1 · A marker inside a fenced code block removes the directory

`skills/verify/scripts/unverified_check.py:85` — `FOLD_MARKER`, read at `:636`
inside `folded_items`, which `skills/settle/scripts/settle.py:364` loads and
`:458` acts on with `shutil.rmtree`.

**Executed.** A fixture repository with one released work item and a `docs/`
document containing this:

````markdown
Each folded sentence carries its comment:

```markdown
<!-- specs/1788302682-the-release-check-never-watched-bin -->
`bin/` ships, so a change to a wrapper moves the version.
```
````

`settle --retire` printed `removed seal/specs/1788302682-…/` and exited 0. No
policy document had absorbed anything.

**Why it matters.** This is the feature's only safety property. `spec.md` G2
and `skills/settle/SKILL.md` §4 both rest on the same sentence — nothing is
removed without a policy having absorbed it, and the marker is the proof. A
fenced block is a quotation, so the proof is satisfied by a document that
quotes the convention instead of following it.

**The shape is the project's own.** `skills/settle/SKILL.md:88-92` documents
the marker with a fenced block carrying a real released work item id,
`1788302682-the-release-check-never-watched-bin`. Copy that example into any
`docs/` document — which is what a session writing the fold's policy prose is
being shown — and that work item retires itself. Nothing under `docs/` carries
such a line today, so the defect is reachable rather than live.

The defence that was written covers the other shape. `unverified_check.py:78-82`
argues the line anchor, and
`tests/test_settle_reads_before_it_removes.py:255` and
`tests/test_unverified_rows_close.py`'s case of the same name both pin the
**inline** quotation — `` `<!-- specs/… -->` `` inside a sentence. Neither
writes a fence.

**Related, same reader, and named here rather than as its own finding**: the
regex has no fence awareness anywhere, so a marker inside a longer HTML comment
block — a commented-out draft section — is also read on its own line.

---

## 🟡 2 · A marker in a file under `docs/` that is no policy reads as a fold

`skills/verify/scripts/unverified_check.py:604-637` — `folded_items` walks all
of `docs/` recursively.

**Executed.** A marker placed in `docs/experiments/2026-09-03-a-note.md` made
`settle --retire` remove the work item's directory, exit 0.

`docs/experiments/` is this repository's scratch area — four files, two of them
a README pair, none of them a policy document. `spec.md` G2 fixes the
destination as a flat `docs/`: *merging into a document that already exists and
creating one only for a new area*, and `skills/settle/SKILL.md:82` spells it
*`docs/` is flat — there is no `docs/policy/` directory*. The fold never writes
below the top level, so the reader should not read below it either.

The docstring at `:613-619` argues the scope correctly for the tree as a whole
and then does not apply it inside `docs/`: *widening the scan to the whole tree
would let a marker anywhere … excuse a removal nothing absorbed*. A note in an
experiments directory is that marker anywhere.

---

## 🟡 3 · In local mode `settle` says the repository has no work items

`skills/settle/scripts/settle.py:497-504`, against `:508-515`.

**Executed.** A repository with `seal/specs/<id>/` under
`$(git rev-parse --git-common-dir)/seal/` and nothing at `<repo>/seal/`:

```
settle: /tmp/a-local-mode-repo has no seal/specs/ — nothing was read. This
command folds work items, and a repository with none has nothing to settle.
```

Exit 2. The repository had a work item; the command looked in one of the two
places a `seal/` root lives.

**Two things are wrong and they are separable.**

- **The root is not resolved.** `under(root, SPECS)` is `<root>/seal/specs`
  and nothing else. `skills/agent-contract/SKILL.md` §16 and
  `docs/one-root-by-lifetime.md` both fix the resolution as `<root>/seal/`
  then `<git-common-dir>/seal/`, and this repository has one resolver for it,
  `hooks/optin.py#home_at`. `skills/evidence-check/scripts/evidence_check.py#seal_home`
  is a shipped script three directories below `hooks/` reaching it the same
  way `settle.py` could.
- **The sentence written for local mode is unreachable.** `:509-515` carries
  it — *In local mode the root is never committed, so no ref holds the
  directories and there is nothing this can call released* — behind the
  `--released-at` refusal. The `seal/specs/` check at `:498` fires first and
  always, so that sentence cannot be printed in the case it was written for.

**This contradicts the memo.** `overview.md` §*Not verified* says of local mode
*The refusal for that case is read from the code and its message was written
for it*. The message exists; the path to it does not. That is the claim I
checked and it does not hold.

Which of the two fixes is right is a judgment: resolving the root and then
refusing is the behaviour §16 describes, and refusing at `:498` with an honest
sentence is cheaper. The fix below takes the first, because the second leaves
`settle` the one shipped command that does not know where a `seal/` root lives.

---

## 🟡 4 · An item the guard is holding is reported as waiting to be retired

`skills/settle/scripts/settle.py:376-382` — `survey` tests `folded` before
`held` — and `:426`.

**Executed.** One work item with a fold marker in `docs/` and one open row in
its `evidence-todo.md`:

```
released and unfolded: 0 work items in 0 segments, 0 ungrouped, 0 skipped

folded already, waiting to be retired — `settle --retire`:
    1788302682-the-release-check-never-watched-bin
```

`0 skipped`, and the item is named under the heading that tells the reader to
run `--retire`. `--retire` then refuses it and exits 1.

`spec.md` G3 says such an item is **skipped and named**, never folded. The
report names it as the opposite. A session following
`skills/settle/SKILL.md` §1 reads three lists beside the grouped items — *the
ones an open `evidence-todo.md` row is holding* — and this item is in neither
that list nor the count.

The retirement itself is correct: `retire()` re-reads `open_items` at `:447`
and keeps the directory. What is wrong is only what the reader is told first.

---

## 🟡 5 · After a successful retirement the next run says nothing was ever folded

`skills/settle/scripts/settle.py:450-456`.

**Executed.** A fixture with two work items, one marked. `settle --retire`
removed it and exited 0. The next `settle --retire`:

```
nothing to retire: no released work item carries a `<!-- specs/<id> -->`
marker in docs/, so none of them has been folded yet.
```

Exit 1. The marker is still in `docs/` and the fold did happen — the directory
it named is simply gone, so `survey` no longer lists the item at all. Two
states share one message: *nobody has folded anything* and *everything folded
has been retired*, and the second is the state the release checklist's step 2b
leaves behind every time it is followed.

The exit code carries the same conflation. The script's own docstring at `:52`
says exit 1 means *a retirement was asked for and something refused it*.
Nothing refused this one.

---

## 🟡 6 · `open_rows` is duplicated with nothing holding the two copies in step

`skills/settle/scripts/settle.py:218-260` against
`.github/scripts/fold_ledger.py:210-244`, with `SEPARATOR_RE` and `DRAINED_RE`
at `settle.py:138-139` and `fold_ledger.py:83-84`.

**Read.** The two are the same algorithm to the character, including the
`split("\n")` comment about U+2028. The divergence is deliberate and the
grounds are right: `SHIPS` in
`tests/test_the_release_check_watches_what_ships.py:38-45` is
`skills · agents · hooks · templates · bin · .claude-plugin`, so `.github/` is
not something a user's repository has, and a shipped command may not import
from it. `settle.py:231-236` states that.

What is missing is the pin. `grep -rn open_rows tests/` finds four assertions
and all four are `settle.open_rows`; nothing compares the two implementations.
`spec.md` §*One interlock does hold* makes the release guard's safety rest on
exactly this agreement — *the only directories a fold removes are ones the
guard was never holding* — and that sentence is true only while the two
readers answer the same way.

**The same file already does this correctly one copy over.** `FLOOR` is copied
from `round_record.py` for the same reason, and
`tests/test_a_script_says_which_interpreter_it_needs.py:433` holds it against
the runner's, with `:621-635` extending the family to `settle`. One copy in
this file is pinned and the other is not.

---

## ⬜ 7 · A stray space in a printed line

`skills/verify/scripts/unverified_check.py:862` prints
`<!-- specs/{id} --> , so what this recorded as unverified was absorbed`.
The space before the comma reaches the hygiene workflow's output. No test pins
the sentence, so nothing would catch it changing either.

---

## ⬜ 8 · The memo still lists the `Ran by` cells as unverified

`overview.md:81` names *the `Ran by` cell of all six phase records, which reads
`unknown — <why>`* as a row nobody answered. Commit `0adf3ed3` — the target SHA
itself — answered all six: every `phases/phase-N.md` now reads `` `specseal:smith`
on Opus 5 (1M context) ``. The row outlived its own fix by one commit.

---

## ⬜ 9 · `CLAUDE.md`'s fragment rule does not cover the case this branch was in

`CLAUDE.md` §*a change writes fragments, never the shared file* permits
touching `seal/ledger.md` for one case: *A branch that removes code an existing
`seal/ledger.md` row cites must touch that file to leave the ledger true.* This
branch removed nothing — it **edited** seven units that rows cite, which drifts
them, and `broad-gate` runs `evidence-check --strict` where drift is exit 2.

The act was right (see the confirmation below). The rule as written does not
name it, which is the same gap the rule's own history records: a branch in this
position finds no reading that permits the only correct act. `CONTRIBUTING.md`
carries the same sentence and would move with it.

---

## What I checked and found sound

**The framer's floor table is accurate.** `spec.md` §*The ticket's headline
claim is false* was the one correction I was told is load-bearing, and I opened
every row rather than three:

| Claimed | Found |
|---|---|
| `test_chain_check_at_the_pull_request.py:2649`, `:2825` | `assert len(records) > 200` at both lines, over `os.walk(ROOT/seal/specs)` |
| `test_a_finding_id_is_a_bare_integer.py:752` | `assert len(paths) > 100, "the corpus is … the case is vacuous"` |
| `test_the_set_a_work_item_always_has.py` | two non-empty globs, `:342` and `:347` |
| `test_the_record_is_held_to_the_floor_and_the_depth.py` | `:1249-1252`, a named directory by epoch prefix |
| `test_the_reopening_is_one.py` | `:324-326`, the same shape |
| `test_routing_is_recorded.py` | `:499` — `assert found, "no declarations found -- the check would pass vacuously"` |
| `test_release_hygiene.py` | `:1346` — `assert items, "no work item under seal/specs/ carries a routing.md"` |
| `test_the_pull_request_language_is_the_repositorys.py` | `:229` — `assert mirrors, "no mirror files at all — this case is blind"` |

Eight modules carry floors against the claimed *at least six*, which
understates rather than overstates. I scanned `tests/` independently for reads
of the real corpus and found fourteen modules, the same fourteen. No overcount
and no undercount.

**The eleven ledger re-stamps are real re-reads.** Each names the specific edit
that drifted its row and why the claim survives it — *`main` gained a fourth
list*, *`COVERED` gained one entry and one comment*, *the `docs/` row of the
layout table was reworded in both READMEs* — and each is checkable against this
branch's diff. I checked four against the code and all four matched. One, S7,
was re-verified by execution with its output quoted. This is not the
`--reverify` hazard `seal/follow-up.md` names; nothing here was stamped without
being opened.

**The A10 dry run reproduces exactly.** Executed by me at the target SHA:
`81 work items in 37 segments, 16 ungrouped, 0 skipped`, `1 unreleased`, and
the 16 split `14 (no ledger row) · 2 (tests only)`. 0.08 s. Every figure in
`overview.md` §*The dry run* is the run's own.

**The divergence from `plan.md`'s `fold_ledger.py` reuse is sound** on the
grounds given — see finding 6 for the half that is not.

**Both language editions moved together.** `README.md`/`README.ko.md` (skills
count and the cheat-sheet row), `docs/one-root-by-lifetime.md`/`.ko.md` (the
dated section, six decision rows in each), `seal/README.md` and
`templates/seal-README.md` byte-identical. `docs/release-checklist.md` and
`docs/review-handoff-protocol.md` have no Korean twin in this tree.

**A7 holds.** Executed: `/usr/bin/python3` (3.9.6) refused at entry, exit 2,
with the version, the path and the remedy; `python3.12` ran the report.

**The tie-break is deterministic.** Two coordinates in two files gave the
path-order winner, repeatably.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A fold marker inside a fenced code block satisfies the removal guard, and the skill's own example is that shape with a real work item id | `skills/verify/scripts/unverified_check.py:85` · `:636` | open | executed — `settle --retire` removed the directory, exit 0 |
| 2 | 🟡 A marker in a non-policy file under `docs/` satisfies the guard; the walk is recursive where the fold is flat | `skills/verify/scripts/unverified_check.py:604` | open | executed — a marker in `docs/experiments/` removed the directory |
| 3 | 🟡 In local mode the root is not resolved and the refusal written for local mode is unreachable | `skills/settle/scripts/settle.py:497` · `:508` | open | executed — "a repository with none has nothing to settle" against a repository with one |
| 4 | 🟡 An item the evidence-todo guard is holding is reported as waiting to be retired, and counted `0 skipped` | `skills/settle/scripts/settle.py:377` · `:426` | open | executed — `spec.md` G3 says skipped and named |
| 5 | 🟡 After a complete retirement the next run reports that nothing was ever folded, at exit 1 | `skills/settle/scripts/settle.py:450` | open | executed — markers still in `docs/`; docstring `:52` says exit 1 is a refusal |
| 6 | 🟡 `open_rows` is duplicated into the shipped script with no test holding the two copies in step, while `FLOOR` in the same file is pinned | `skills/settle/scripts/settle.py:218` · `.github/scripts/fold_ledger.py:210` | open | read — the interlock in `spec.md` rests on the two agreeing |
| 7 | ⬜ A space before a comma in a printed line, unpinned | `skills/verify/scripts/unverified_check.py:862` | open | read |
| 8 | ⬜ The memo lists the six `Ran by` cells as unverified; `0adf3ed3` answered them | `overview.md:81` | open | read — all six cells name `specseal:smith` |
| 9 | ⬜ `CLAUDE.md`'s ledger exception names removal only; this branch's case was drift-by-edit | `CLAUDE.md` §*a change writes fragments, never the shared file* | open | read |
| 🟢 confirmation | The framer's population-floor table, all eight modules | `spec.md` §*The ticket's headline claim is false* | confirmed | each coordinate opened; independent scan found the same fourteen |
| 🟢 confirmation | The eleven `seal/ledger.md` re-stamps were real re-reads, not `--reverify` stamping | `seal/ledger.md` | confirmed | four checked against the branch's diff; S7 re-verified by execution |
| 🟢 confirmation | The A10 dry-run figures | `overview.md` §*The dry run over this repository's own 97* | confirmed | executed — 81/37/16/0, 14 + 2, reproduced exactly |
| 🟢 confirmation | The grounds for diverging from `plan.md`'s `fold_ledger.py` reuse | `overview.md` §*Where spec and implementation diverged* | confirmed | `SHIPS` excludes `.github/` |
| 🟢 confirmation | Both language editions carry the same corrections | `README*.md` · `docs/one-root-by-lifetime*.md` | confirmed | read, diffed side by side |
| 🟢 confirmation | A7, the interpreter floor | `skills/settle/scripts/settle.py:95` | confirmed | executed at 3.9.6 and 3.12.9 |
| ❓ scope | The broad gate | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers |

## Executed probes

| What was run | Result |
|---|---|
| `settle --retire` against a fixture whose `docs/` document carries the marker inside a ```` ```markdown ```` fence | `removed seal/specs/1788302682-…/`, exit 0 — finding 1 |
| `settle --retire` against a fixture whose marker sits in `docs/experiments/2026-09-03-a-note.md` | directory removed, exit 0 — finding 2 |
| `settle` against a fixture whose `seal/` sits under the common git directory | exit 2, "has no seal/specs/ … a repository with none has nothing to settle" — finding 3 |
| `settle` then `settle --retire` against a fixture with a marker and one open `evidence-todo.md` row | listing said "waiting to be retired" and `0 skipped`; retire kept it, exit 1 — finding 4 |
| `settle --retire` twice against a fixture with one marked and one unmarked item | first removed the marked one at exit 0; second said "none of them has been folded yet", exit 1 — finding 5 |
| `settle --released-at origin/main` over this repository at the target SHA | `81 work items in 37 segments, 16 ungrouped, 0 skipped`, 1 unreleased, 14 + 2, 0.08 s — A10 reproduced |
| `settle` under `/usr/bin/python3` (3.9.6) and `/opt/homebrew/bin/python3.12` (3.12.9) | exit 2 with the floor sentence; exit 0 with the report — A7 |
| `settle.segment_of` over two coordinates in two files, via the command | `aaa/a.py`, the path-order winner |
| the six changed test modules, `uvx ruff check`, `uvx ruff format --check` | not run in this round — the orchestrator executed them at this SHA and handed the result over |
| the broad gate — full suite, repository-wide lint and typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

Every probe ran in a `git clone --no-local` at the target SHA, against
throwaway fixture repositories built and removed by one script. The probe file
and its fixtures are deleted.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `settle` against a second real repository | already deferred in `overview.md` §*Not verified* | the repository owner, the next time the plugin is used elsewhere |
| whether the six population floors are still six after a fold | already deferred in `overview.md` §*Not verified* | the work item that folds this repository's own 97 |

## Paste-ready fixes

Finding 1 — strip fenced blocks before the marker scan, in
`skills/verify/scripts/unverified_check.py`. Add beside `FOLD_MARKER` at `:85`:

```python
DOCS = "docs"
FOLD_MARKER = re.compile(r"^<!-- specs/(\S+) -->$", re.M)
# A fence is a quotation, and the one document a session reads before it folds
# — `skills/settle/SKILL.md` §2 — shows the marker inside one, with a real
# released work item id. Copy that example into a `docs/` document and the
# line anchor below reads it as a fold, so `settle --retire` removes a
# directory no policy absorbed. `hooks/config.py` shipped this class once and
# `evidence_check` still carries it: the anchor says the marker stands alone
# on its line, never that the line is prose.
FENCE = re.compile(r"^(?P<fence>```+|~~~+).*?(?:^(?P=fence)`*\s*$|\Z)", re.M | re.S)


def outside_fences(text):
    """`text` with every fenced block blanked, line count preserved."""
    return FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
```

and at `:636`, inside `folded_items`:

```python
            found.update(FOLD_MARKER.findall(outside_fences(text)))
```

Finding 2 — read only the top level of `docs/`, which is where the fold
writes. Replace the walk at `:629-636` of the same file:

```python
    for name in sorted(os.listdir(top)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(top, name)
        if not os.path.isfile(path):
            continue
        # The top level only. `spec.md` G2 and `skills/settle/SKILL.md` fix
        # the destination as a flat `docs/` — merge into a document that
        # exists, create one only for a new area, no `docs/policy/`. A fold
        # never writes below this level, so a marker below it is somebody's
        # notes: `docs/experiments/` is four scratch files, and one of them
        # holding a quoted marker excused a removal nothing absorbed.
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        found.update(FOLD_MARKER.findall(outside_fences(text)))
    return found
```

Finding 3 — resolve the root the way every other shipped script does.
In `skills/settle/scripts/settle.py`, beside `READER` at `:120`:

```python
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
OPTIN = os.path.join(HERE, "..", "..", "..", "hooks", "optin.py")
```

and replace the `seal/specs/` check at `:498-504`:

```python
    # `<root>/seal/` then `<git-common-dir>/seal/`, through the one resolver,
    # the way `evidence_check.py#seal_home` reaches it from the same depth.
    # Without this a local-mode repository was told it had no work items while
    # holding ninety-eight, and the sentence written for local mode — in the
    # `--released-at` refusal below — could never be printed, because this
    # check fired first and always.
    home = load(OPTIN, "specseal_optin").home_at(root)
    specs = os.path.join(home, "specs") if home else under(root, SPECS)
    if not os.path.isdir(specs):
        sys.stderr.write(
            f"settle: {root} has no {SPECS}/ at either place — nothing was read. "
            "This command folds work items, and a repository with none has "
            "nothing to settle.\n"
        )
        return 2
```

`SPECS` is used to build disk paths in `work_items`, `open_items`,
`coordinates` and `retire`, so the resolved `specs` has to be threaded through
those four rather than left as a local. The repo-relative `SPECS` stays as it
is for the strings the report prints. In local mode the run then reaches the
`--released-at` refusal at `:508`, which is the sentence that was written for
it — and that refusal is the right answer there, because nothing removed from
an uncommitted root can be recovered.

Finding 4 — test the guard before the fold record, in `survey` at `:376-382`:

```python
    for work_item_id in survey["released"]:
        # The guard first. `spec.md` G3 says an item with an open row is
        # skipped AND NAMED, never folded — and an item that is both folded
        # and held was being named under "waiting to be retired", which is
        # the opposite instruction, while the summary counted it `0 skipped`.
        # `retire()` reads `open_items` again and keeps it either way; what
        # this fixes is what the reader is told before running anything.
        if work_item_id in held:
            survey["skipped"].append((work_item_id, held[work_item_id]))
            continue
        if work_item_id in folded:
            survey["folded"].append(work_item_id)
            continue
```

Finding 5 — tell the two states apart, in `retire` at `:447-456`:

```python
    held = open_items(root)
    refused = [i for i in found["folded"] if i in held]
    removable = [i for i in found["folded"] if i not in held]
    if not removable and not refused:
        # Two states, and they used to share one sentence. A marker in `docs/`
        # whose directory is already gone leaves `survey` nothing to list, so
        # a second run reported that nothing had ever been folded — the one
        # thing the tree plainly contradicts, and the state every run of
        # `docs/release-checklist.md` step 2b ends in.
        marked = load(READER, "specseal_unverified_reader").folded_items(root)
        if marked:
            out.write(
                f"nothing left to retire: {len(marked)} work item"
                f"{plural(len(marked))} carry a `<!-- specs/<id> -->` marker "
                "in docs/ and none of them still has a directory under "
                f"{SPECS}/. The fold is complete.\n"
            )
            return 0
        out.write(
            "nothing to retire: no released work item carries a "
            "`<!-- specs/<id> -->` marker in docs/, so none of them has been "
            "folded yet. `settle` alone says which ones are waiting for one.\n"
        )
        return 1
```

Finding 6 — pin the two copies. A new case in
`tests/test_settle_reads_before_it_removes.py`, next to the other `open_rows`
assertions at `:318`:

```python
def test_the_guard_is_the_same_reader_as_the_release_folds():
    """`settle.py` carries its own `open_rows` because `.github/` is not on
    the list of what the plugin ships, so a shipped command may not import
    from it. `spec.md` §*One interlock does hold* then rests on the two
    answering alike — the only directories a fold removes are ones the
    release guard was never holding — and nothing held them together. The
    floor in the same file is pinned this way already."""
    import ast

    def source_of(path, name):
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == name:
                return ast.dump(ast.parse(ast.unparse(node)))
        raise AssertionError(f"{path} has no {name}")

    fold = os.path.join(ROOT, ".github", "scripts", "fold_ledger.py")
    mine = os.path.join(ROOT, "skills", "settle", "scripts", "settle.py")
    assert source_of(mine, "open_rows") == source_of(fold, "open_rows"), (
        "settle.py#open_rows and fold_ledger.py#open_rows have diverged. They "
        "are one rule in two files on purpose; a fold that reads an open row "
        "differently from the release guard removes a directory the guard was "
        "holding"
    )
    for const in ("SEPARATOR_RE", "DRAINED_RE"):
        assert getattr(settle, const).pattern == getattr(
            fold_ledger_module(), const
        ).pattern, f"{const} differs between the two readers"
```

Needs a fix: yes — findings 1 through 6. Findings 1 and 2 are the fold's only
safety property; 3 to 5 are what the command tells a reader; 6 is the pin the
interlock in `spec.md` assumes.
Loses a record or crashes: yes — finding 1 removes a work item's directory
under `seal/specs/` with no policy document having absorbed it, which is the
one loss `skills/settle/SKILL.md` §4 says nothing can undo. The removal is
recoverable from git until the fold branch commits, and the fold's next act is
that commit.

## Proof block

Opened in this round:
`seal/specs/1790027178-…/{spec,plan,questions,routing,overview}.md` and
`phases/phase-1.md`, `phase-2.md`;
`skills/settle/SKILL.md`; `skills/settle/scripts/settle.py`; `bin/settle`;
`bin/settle.cmd`; `skills/verify/scripts/unverified_check.py`;
`.github/scripts/gather_changelog.py`; `.github/scripts/fold_ledger.py`;
`hooks/optin.py#home_at`; `skills/evidence-check/scripts/evidence_check.py#seal_home`;
`skills/code-review/scripts/round_record.py#common_dir_of`;
`tests/test_settle_reads_before_it_removes.py`;
`tests/test_a_script_says_which_interpreter_it_needs.py`;
`tests/test_unverified_rows_close.py`;
`tests/test_the_release_check_watches_what_ships.py#SHIPS`;
`tests/test_chain_check_at_the_pull_request.py:2640-2830`;
`tests/test_a_finding_id_is_a_bare_integer.py:745-760`;
`tests/test_the_set_a_work_item_always_has.py:325-350`;
`tests/test_the_record_is_held_to_the_floor_and_the_depth.py:1240-1255`;
`tests/test_the_reopening_is_one.py:315-330`;
`tests/test_routing_is_recorded.py:480-525`;
`tests/test_release_hygiene.py:1155-1180`, `:1340-1350`;
`tests/test_the_pull_request_language_is_the_repositorys.py:220-245`;
`tests/test_waiver_decided_at_start.py:785-805`; `ruff.toml`;
the branch diff of `seal/ledger.md`, `README.md`, `README.ko.md`,
`docs/one-root-by-lifetime.md`, `docs/one-root-by-lifetime.ko.md`,
`docs/release-checklist.md`, `docs/review-handoff-protocol.md`,
`seal/README.md`, `templates/seal-README.md`, `skills/implement/SKILL.md`.

Not opened: `tests/test_docs_line_wrap.py`,
`tests/test_chain_hooks_hardening.py` beyond its corpus reads,
`tests/test_the_changelog_is_gathered_at_release.py`,
`phases/phase-3.md` through `phase-6.md`, `changelog.md`,
`seal/ledger/1790027178-….md`.
