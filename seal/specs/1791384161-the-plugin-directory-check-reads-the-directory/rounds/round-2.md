# 1791384161-the-plugin-directory-check-reads-the-directory — review round 2

| Field | Value |
|---|---|
| Target SHA | b3c99c01b82c854354a73a97a7f6c427153f2c95 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 875 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `38abbcc700a773fd8edd55db0968dfcf8de19f67..a8a315f863f5273fc63423cb129472aad713f1db`, 1 commit |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | yes — ⬜ 2: a `plugin.json` whose top level is not an object still ends in a `TypeError` traceback and exit 1. The default root never reaches it. |

- [x] Pass

## What this round was asked

Verifying round 2 of round 1's fixes, the range f105d83b..fb256f54 plus the closing record b3c99c01. The job was the answers: whether each of round 1's eight fixed verdicts is closed. The four units round 1's record names in New units (ALLOWED_UNDER_PATHS, PRODUCT_HOST, and the two new cases) were a finding surface. The spawn named three things to judge: whether the three survivors excused in survivors.md are rightly left as the approved frame; whether the ALLOWED_UNDER_PATHS rule refuses what round 1's 🟡 2 named and admits every claude.ai reference in the tracked tree; and whether --root's exit 2 is pinned and consistent with the command's other argument errors. Facts arrived labelled. Executed by the orchestrator: bin/test over three modules (32 passed), the 8-fixed close, and the docs fetch of the publish-setting wording. Read from the smith: 9 pins red before the fixes, 13 mutations red, evidence-check --strict and survivor-check at exit 0.

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
| ⬜ 1 | The host rule admits a share link spelled with a port, an escaped slash or a query, and `/directory` matches as a prefix | `tests/test_no_real_identifiers.py:72` | answered | a note, left as it stands: the rule refuses every form round 1's 🟡 2 named and every tracked reference passes; the port, escaped-slash, query and prefix spellings are a narrower case of the same class, recorded here and in the pull request body; executed probe: five such plants admitted; the proposed rule refuses four and keeps the tree clean |
| ⬜ 2 | A manifest whose top level is not an object ends in a `TypeError` traceback and exit 1 | `.github/scripts/plugin_directory_check.py:297` | answered | a note, left as it stands: only a hand-given `--root` whose `plugin.json` top level is `[]` or `null` reaches it, and the default root never does; recorded here and in the pull request body as a known limit; executed probe: `[]` and `null` raise `TypeError`; the default root never reaches it |
| ⬜ 3 | The new `--root` case pins exit 2 and not the error line its docstring and the changelog promise | `tests/test_the_plugin_directory_answers_the_box.py:384` | answered | a note, left as it stands: the case pins the exit code, and the error line is argparse's own `parser.error` shape, read by round 2 over five root shapes; read: the case asserts only the code; contract §14 |
| ⬜ 4 | The closing line, the box and the changelog say *tracked branch* where the docs say *branch or tag* | `.github/scripts/plugin_directory_check.py:278` | answered | a note, left as it stands: *tracked branch* is the docs' own name for the field when it holds a branch, and the docstring and the third-reader sentence already say *branch or tag*; read; the docstring at line 29 and the third-reader sentence already say *branch or tag* |
| ⬜ 5 | `overview.md:17` still says *the company's mail domain*, `overview.md:21` names §*Vocabulary* instead of §*Scope* 1–2, A5 and §*Data & interfaces*, and `survivors.md:5` says three rows over two | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/overview.md:21` | answered | corrected at a8a315f8 — a correction to the run's records (`overview.md`, `survivors.md`), outside `Needs a fix`; read; a correction to the run's paperwork, outside `Needs a fix` |
| ❓ | That SpecSeal's listing is a Console listing, and that the Console page the command prints is where it appears | `docs/release-checklist.md:378` | ❓ out of verified scope | a logged-in page; the repository owner answers it (`overview.md` §*Not verified*), carried from round 1 |

## Paste-ready fixes

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
```python
    try:
        name = plugin_name(root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(
            f"--root {root} has no readable .claude-plugin/plugin.json: {error}"
        )
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/plugin_directory_check.py:277` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_no_real_identifiers.py:29` | round 1's 🟡 2 — fixed |
| round-1 | `docs/release-checklist.md:360` | round 1's 🟡 3 — fixed |
| round-1 | `docs/branch-and-release.md:401` | round 1's 🟡 4 — fixed |
| round-1 | `docs/release-checklist.md:365` | round 1's 🟡 5 — fixed |
| round-1 | `.github/scripts/plugin_directory_check.py:144` | round 1's ⬜ 6 — fixed |
| round-1 | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/spec.md:60` | round 1's ⬜ 7 — fixed |
| round-1 | `docs/branch-and-release.md:81` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/scripts/plugin_directory_check.py:221` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/plugin_directory_check.py:212` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_plugin_directory_answers_the_box.py:485` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/questions.md:36` | round 1's 🟢 — confirmed |
| round-1 | `docs/release-checklist.md:374` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
