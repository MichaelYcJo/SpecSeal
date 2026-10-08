# 1791384161-the-plugin-directory-check-reads-the-directory — round 2 report

Verifying round at `b3c99c01b82c854354a73a97a7f6c427153f2c95`. The target is
round 1's fix range `f105d83b..fb256f54` and the record commit `b3c99c01`.
Every execution below ran in a `git clone --no-local` of the worktree at that
SHA, made in the session scratchpad and removed when the round ended.

## In short

All eight of round 1's findings are closed for the cases round 1 named. Each
fix leaves a narrower case of its own class open, and none of those needs a
fix before the release:

- round 1's finding 2 (the host allowance) → the new rule still admits a share
  link spelled with a port or an escaped slash (⬜ 1);
- round 1's finding 6 (`--root` traceback) → a manifest that parses but is not
  an object still ends in a traceback (⬜ 2), and the new case pins the exit
  code but not the line a person reads (⬜ 3);
- round 1's finding 8 (*or tag* dropped) → the closing line, the box and the
  changelog still say *tracked branch* only (⬜ 4);
- the paperwork → `overview.md` carries one row round 1's finding 7 made
  stale and one row that names the wrong clause (⬜ 5, a correction).

The three excused survivors are rightly left (the 🟢 row below says why).

## What the account claimed, and what I found

The hand-back claimed 9 pins red before the fixes. I reverted the command and
the two documents to `f105d83b` in the clone and ran the two modules that pin
them: 8 cases failed, among them every case round 1's fixes touched, and the
rest passed. The identifier case's red was shown in round 1's own probe.

The hand-back claimed `survivor-check` named 3 survivors, all excused. I ran
it with and without the exemption file. Without it, it names `plan.md:100`,
`spec.md:79` and `spec.md:186` and exits 1. With it, it exits 0. The file's
prose says *the three below* over two rows; one `spec.md` row's quote covers
both `spec.md` places, so the count is of places, not rows.

The hand-back said A10's letter is no longer met and that the departure is
recorded. `overview.md:20` records it, and the house rule's purpose is the
right ground for it.

## Round 1's findings, answered

**Round 1's finding 1 is closed.** The closing line
(`.github/scripts/plugin_directory_check.py:278`), the docstring, the box
(`docs/release-checklist.md:374`) and the changelog now say a version is
picked up without a resubmission and goes live by the publish setting, which
by default waits for somebody to select Publish. That matches the docs
sentence the orchestrator fetched on 2026-10-08 (read; I did not fetch it).
Both pins go red against `f105d83b` (executed).

**Round 1's finding 2 is closed for the forms it named.** A path other than
`/directory`, an address and a subdomain are each refused (executed). The
tracked tree holds the host in three forms, 29 bare, 2 under `/directory` and
6 under `/directory/manage`, and the module's own tree case is green, so the
rule admits every reference the tree carries (executed). What it still admits
is ⬜ 1.

**Round 1's finding 3 is closed.** The box heading and §6's opening no longer
say the command answers for the directory, and both are pinned. The pin goes
red against the old text (executed).

**Round 1's finding 4 is closed.** The fold's `Enforced by:` line and the
fixed-name paragraph name a marketplace file, and both are pinned (executed,
red against the old text).

**Round 1's finding 5 is closed.** The box reads *once went twenty-eight
days*, which is pinned.

**Round 1's finding 6 is closed for the case it named, and the exit is
consistent.** A missing manifest, a file given as the root, invalid JSON,
non-UTF-8 bytes and a manifest with no `name` each exit 2 through
`parser.error` (executed). That is the same path and the same two-line shape
argparse uses for an unknown flag: a usage line, then one `error:` line. It
matches `spec.md` §*Data & interfaces*, *2 for a malformed argument*, and the
docstring's *the only non-zero exit here is a malformed argument*. The new
case goes red against `f105d83b` (executed). What stays open is ⬜ 2 and ⬜ 3.

**Round 1's finding 7 is closed in `spec.md` and `questions.md`.** The overview
row that records the respelling still quotes the old phrase (⬜ 5).

**Round 1's finding 8 is closed.** The bullet says a curated catalog and a
nightly mirror, the third-reader sentence says *branch or tag*, and the
docstring was corrected in `fb256f54`. The same omission stands in three other
places (⬜ 4).

## The excused survivors are rightly left

`spec.md` and `plan.md` are the frame the owner approved, and editing them to
match the build would erase the record of what was approved. The frame also
carries the correct fact itself: `spec.md:36`, the first §*Vocabulary* fact,
already says a version that passes is published by the publish setting. So
the survivors are the frame shortening its own fact, not a fact nobody wrote
down. Nobody acts on `spec.md` after the release: `skills/settle/SKILL.md`
treats a retired spec as a place that instructs nobody.

Two sentences make this less clean than it looks, and both are paperwork:

- the same claim stands in paraphrase at `spec.md:169` (A5, *updates from the
  tracked branch on its own*) and `plan.md:101` (*a portal listing updates on
  its own*), which `survivor-check` did not match and nobody excused;
- the overview row that records the departure (`overview.md:21`) names
  §*Vocabulary*'s first fact as what the spec says, and says *the build
  shortened it*. The build now matches that fact. The clauses it departs from
  are §*Scope* item 1, item 2, A5 and §*Data & interfaces*, which the frame
  itself wrote with *on its own*.

A sealer checking A5 against the box finds A5 unmet and an overview row that
points at a clause the box satisfies. That is ⬜ 5.

## New findings

### ⬜ 1 The host rule admits a share link spelled with a port, an escaped slash or a query

`tests/test_no_real_identifiers.py:72`. The rule treats any text after the
host that does not start with `/` as the bare host, and it matches
`/directory` as a prefix rather than a path segment. A probe planted seven
spellings in a built tree and ran `domains_in` (executed). It refused only the
userinfo form and admitted these:

- the product host followed by `:443/share/0000`;
- the host followed by `\/share\/0000`, as JSON with escaped slashes writes it;
- the host followed by `?share=0000`;
- the host followed by `/directory-x/0000`;
- the host followed by `/directory/../share/0000`.

**Why it is ⬜ and not 🟡.** The tree holds none of these, and nothing here
writes a share link with a port or escaped slashes. The release ships no leak.
The comment above the rule says *allowed bare, or under the paths named for
it, and nowhere else*, and the code is wider than that sentence. A second
probe ran the rule in the fence below over the same plants and the whole
tracked tree: it refused the first four and admitted every reference in the
tree (executed). The `..` form stays admitted, which needs path normalising
and is not worth it.

### ⬜ 2 A manifest whose top level is not an object still ends in a traceback

`.github/scripts/plugin_directory_check.py:297`. `plugin_name` indexes the
parsed manifest with `["name"]`. A `plugin.json` holding `[]` or `null` raises
`TypeError`, which the new `except` does not catch, so the run ends in a
traceback and exit 1 (executed). That is round 1's finding 6 in another shape.
The error line the fix added says *has no readable plugin.json*, which covers
this case too. The default root never reaches it, because the repository's own
manifest is an object.

### ⬜ 3 The new case pins the exit code and not the line a person reads

`tests/test_the_plugin_directory_answers_the_box.py:384`. The docstring of
`test_a_root_with_no_manifest_is_a_malformed_argument` promises *one line
saying what is missing, not a traceback*, and the changelog says *exits 2 with
one line saying so*. The case asserts only `code == 2`. A later edit that
replaced `parser.error` with a silent `sys.exit(2)` would keep it green and
make the changelog sentence false. Contract §14 asks for the pin in the same
commit. The fence below also covers ⬜ 2's shape, and its `[]` case is red at
`b3c99c01`, as the ⬜ 2 probe shows.

### ⬜ 4 Three places still say *tracked branch* where the docs say *branch or tag*

`.github/scripts/plugin_directory_check.py:278`, `docs/release-checklist.md:375`
and `changelog.md:20` say a portal listing picks up each new version *from its
tracked branch*. Round 1's finding 8 corrected the same omission in the
third-reader sentence, and the docstring at line 29 already says *tracked
branch or tag*. For a branch-tracked listing nothing here is false. It is §12's
class left one coordinate short.

### ⬜ 5 The overview has a stale row and a row that names the wrong clause

A correction to the paperwork, not to the tool.

- `overview.md:17` says the three places *now say the company's mail domain*.
  Round 1's finding 7 changed them to *Anthropic's mail domain*.
- `overview.md:21` names §*Vocabulary*'s first fact as the clause departed
  from. The departure is from §*Scope* items 1 and 2, A5 and §*Data &
  interfaces*. A5 at `spec.md:169` and `plan.md:101` carry the claim in a
  paraphrase `survivor-check` did not match.
- `survivors.md:5` says *the three below* over two rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — a portal listing picks up a version without a resubmission and goes live by its publish setting | `.github/scripts/plugin_directory_check.py:278` | confirmed | read: the closing, the docstring, the box at `docs/release-checklist.md:374`, `changelog.md:20`; executed: both pins red against `f105d83b`, green at `b3c99c01` |
| 🟢 | round 1's finding 2 is closed — a path other than `/directory`, an address and a subdomain on the host are refused | `tests/test_no_real_identifiers.py:72` | confirmed | executed: the new case green, the module's tree case green over 37 references in three forms; residual spellings are ⬜ 1 |
| 🟢 | round 1's finding 3 is closed — the box heading and §6's opening no longer say the command answers for the directory | `docs/release-checklist.md:362` | confirmed | read; executed: the A5 box case red against `f105d83b` |
| 🟢 | round 1's finding 4 is closed — the fold's record line and the fixed-name paragraph name a marketplace file | `docs/branch-and-release.md:402` | confirmed | read; executed: both A8 cases red against `f105d83b` |
| 🟢 | round 1's finding 5 is closed — the day count reads *once went* | `docs/release-checklist.md:367` | confirmed | read; pinned in the A5 box case |
| 🟢 | round 1's finding 6 is closed — a missing or unreadable manifest is exit 2 through `parser.error`, the shape of every other argument error | `.github/scripts/plugin_directory_check.py:297` | confirmed | executed: absent, file-as-root, invalid JSON, non-UTF-8 and no `name` each exit 2 with a usage line and one error line; the new case red against `f105d83b`; residuals are ⬜ 2 and ⬜ 3 |
| 🟢 | round 1's finding 7 is closed — `spec.md` and `questions.md` say *Anthropic's mail domain* | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/spec.md:60` | confirmed | read; the overview row recording it is stale, ⬜ 5 |
| 🟢 | round 1's finding 8 is closed — the bullet says curated catalog and nightly mirror, and the third-reader sentence says *branch or tag* | `docs/branch-and-release.md:81` | confirmed | read; executed: the A7 case red against `f105d83b`; the same omission elsewhere is ⬜ 4 |
| 🟢 | the three excused survivors are rightly left as the approved frame | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/survivors.md` | confirmed | executed: survivor-check exit 1 with three places, exit 0 with the exemption; read: `spec.md:36` carries the right fact, settle treats a retired spec as instructing nobody |
| ⬜ 1 | The host rule admits a share link spelled with a port, an escaped slash or a query, and `/directory` matches as a prefix | `tests/test_no_real_identifiers.py:72` | open | executed probe: five such plants admitted; the proposed rule refuses four and keeps the tree clean |
| ⬜ 2 | A manifest whose top level is not an object ends in a `TypeError` traceback and exit 1 | `.github/scripts/plugin_directory_check.py:297` | open | executed probe: `[]` and `null` raise `TypeError`; the default root never reaches it |
| ⬜ 3 | The new `--root` case pins exit 2 and not the error line its docstring and the changelog promise | `tests/test_the_plugin_directory_answers_the_box.py:384` | open | read: the case asserts only the code; contract §14 |
| ⬜ 4 | The closing line, the box and the changelog say *tracked branch* where the docs say *branch or tag* | `.github/scripts/plugin_directory_check.py:278` | open | read; the docstring at line 29 and the third-reader sentence already say *branch or tag* |
| ⬜ 5 | `overview.md:17` still says *the company's mail domain*, `overview.md:21` names §*Vocabulary* instead of §*Scope* 1–2, A5 and §*Data & interfaces*, and `survivors.md:5` says three rows over two | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/overview.md:21` | open | read; a correction to the run's paperwork, outside `Needs a fix` |
| ❓ | That SpecSeal's listing is a Console listing, and that the Console page the command prints is where it appears | `docs/release-checklist.md:378` | ❓ out of verified scope | a logged-in page; the repository owner answers it (`overview.md` §*Not verified*), carried from round 1 |

## Paste-ready fixes

### ⬜ 1

```python
# The tail after a host that makes it a URL rather than the bare name: a
# path, an escaped path, a port, or a query or fragment with something in it.
URL_TAIL_RE = re.compile(r"(?::\d+)?(?:[/\\]|[?#]\S)")
```

```python
                for m in DOMAIN_RE.finditer(line):
                    d = m.group(0)
                    if d in ALLOWED_UNDER_PATHS:
                        rest = line[m.end() :]
                        mail = m.start() > 0 and line[m.start() - 1] == "@"
                        bare = URL_TAIL_RE.match(rest) is None
                        under = any(
                            re.match(re.escape(p) + r"(?![\w-])", rest)
                            for p in ALLOWED_UNDER_PATHS[d]
                        )
                        if not mail and (bare or under):
                            continue
                    elif any(d == a or d.endswith("." + a) for a in ALLOWED_DOMAINS):
                        continue
                    violations.append(f"{rel}:{i} {d}")
```

```python
            "share.md": f"a conversation at {PRODUCT_HOST}/share/0000\n",
            "port.md": f"https://{PRODUCT_HOST}:443/share/0000\n",
            "escaped.md": f'"{PRODUCT_HOST}\\/share\\/0000"\n',
            "prefix.md": f"{PRODUCT_HOST}/directory-x/0000\n",
            "mail.md": f"write to someone@{PRODUCT_HOST}\n",
            "sub.md": f"a host under it, docs.{PRODUCT_HOST}\n",
        },
    )
    found = sorted(v.split(":")[0] for v in domains_in(root))
    assert found == [
        "escaped.md", "mail.md", "port.md", "prefix.md", "share.md", "sub.md"
    ], domains_in(root)
```

### ⬜ 2

```python
    try:
        name = plugin_name(root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(
            f"--root {root} has no readable .claude-plugin/plugin.json: {error}"
        )
```

### ⬜ 3

```python
@pytest.mark.parametrize(
    "manifest",
    [None, b"{", b"[]", b"{}"],
    ids=["absent", "not JSON", "not an object", "no name"],
)
def test_a_root_with_no_manifest_is_a_malformed_argument(tmp_path, capsys, manifest):
    """Round 1's ⬜ 6. A `--root` holding no readable `.claude-plugin/plugin.json`
    is the author's mistake, so it takes argparse's exit 2 and one line saying
    what is missing, not a traceback and exit 1."""
    if manifest is not None:
        (tmp_path / ".claude-plugin").mkdir()
        (tmp_path / ".claude-plugin" / "plugin.json").write_bytes(manifest)
    mod = checker()
    with pytest.raises(SystemExit) as raised:
        mod.main(["--root", str(tmp_path)])
    assert raised.value.code == 2
    err = capsys.readouterr().err
    assert "has no readable .claude-plugin/plugin.json" in err, err
```

### ⬜ 4

```python
        "A portal listing picks up each new version from its tracked branch "
        "or tag without a resubmission and puts it live by its publish "
        "setting -- which by default waits for somebody to select Publish; a "
        "Console listing takes none until it is moved to the portal.",
```

```
      and the version that is live. It picks up each new version from its
      tracked branch or tag without a resubmission, and a version that passes
```

### ⬜ 5

```
| The frame's own files and the identifier sweep | ... | the three places now say *Anthropic's mail domain* and *the directory team's address*; meaning unchanged | ... |
| What a portal listing does with a new version (round 1, 🟡 1) | §*Scope* items 1 and 2, A5 and §*Data & interfaces*: a portal listing takes new versions from the tracked branch *on its own*; §*Vocabulary*'s first fact already carries the publish setting | the command, its docstring, the box and the changelog follow §*Vocabulary*: picked up without a resubmission, live by the publish setting, which by default waits for somebody to select Publish | `claude.com/docs/plugins/submit` §*Publish a passing version*, fetched 2026-10-08 |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q -p no:cacheprovider` over `tests/test_the_plugin_directory_answers_the_box.py`, `tests/test_no_real_identifiers.py` and `tests/test_the_release_tail_does_not_end_at_the_tag.py`, in the clone at `b3c99c01` | exit 0, 32 passed |
| the command and both documents checked out at `f105d83b` in the clone, then `bin/test` over the command's module and the release-tail module; restored after | exit 1, 8 failed and 18 passed: every pin round 1's fixes added or moved went red |
| a test_tmp probe in the clone, run once and deleted: seven host spellings through `domains_in`, and `main` over seven `--root` shapes with `fetch` stubbed | exit 0; five spellings admitted (⬜ 1); `[]` and `null` raise `TypeError` (⬜ 2); the other five root shapes exit 2 with a usage line and one error line |
| a test_tmp script outside the clone, run once and deleted: the rule in ⬜ 1's fence over twelve plants and every tracked file | exit 0; the six correct forms admitted, the six others refused, no tracked file refused |
| `bin/survivor-check --range f105d83b..HEAD`, without and with the exemption file | exit 1 naming `plan.md:100`, `spec.md:79` and `spec.md:186`; exit 0 with the exemption, three excused |
| `bin/evidence-check --strict .` in the clone | exit 0 |
| the full suite, repository-wide lint and typecheck | not yet — the sealer's, after the rounds settle |

Needs a fix: no

Loses a record or crashes: yes — ⬜ 2: a `plugin.json` whose top level is not
an object still ends in a `TypeError` traceback and exit 1. The default root
never reaches it.

Nothing this round found needs a fix. Once the orchestrator settles the crash
line above, what comes due is the sealer's spawn.

## Proof block

Files opened this round, at `b3c99c01`:

- `.github/scripts/plugin_directory_check.py` (docstring, `plugin_name`, `closing`, `main`)
- `tests/test_no_real_identifiers.py` (the allowlists, `domains_in`, the new case)
- `tests/test_the_plugin_directory_answers_the_box.py` (the argument cases)
- `tests/test_the_release_tail_does_not_end_at_the_tag.py` (the diff's hunks)
- `docs/release-checklist.md` §*6. After the merge*
- `docs/branch-and-release.md` (the diff's hunks)
- `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/`: `rounds/round-1.md`, `rounds/round-1-fixes.md`, `survivors.md`, `overview.md`, `spec.md` (lines 24–36, 57–61, 75–90, 165–210), `plan.md` lines 100–101, `questions.md` and `changelog.md` through the diff
- `seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md` through the diff
- `skills/code-review/orchestration.md` §*survivor-check*, `skills/settle/SKILL.md` (survivor lines), `templates/sdd-overview.md`
