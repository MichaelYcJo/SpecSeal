# 1791384161-the-plugin-directory-check-reads-the-directory — review round 1

| Field | Value |
|---|---|
| Target SHA | a6a366ed73850240132aa1edebc5773fec76c768 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 875 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (a portal listing does not go live on its own under the default publish setting, and two tests pin the wider sentence), 🟡 2 (the host allowance admits per-person links, addresses and subdomains), 🟡 3 and 🟡 4 (four coordinates still state the class the work removes), 🟡 5 (a stale day count in the rewritten box) |
| Loses a record or crashes | yes — ⬜ 6 only: a `--root` with no plugin manifest ends in a traceback and exit 1. It is unchanged from the base, and the default root never reaches it |

- [ ] Pass

## What this round was asked

Round 1 of the build at a6a366ed, against `origin/release/v0.21.0`. The spawn named six things to attack: the command's every output line and exit code against `spec.md` §*Data & interfaces*, including what a failed or rate-limited GitHub read prints; the smith's declared divergence on A2 (`listed` became `an entry`, two assertions changed); the `claude.ai` widening of `tests/test_no_real_identifiers.py` against the house rule, and the company-mail-domain rewording in the frame files; every factual claim the checklist box and `docs/branch-and-release.md` make about the portal and the Console, against the docs pages the spec cites, and whether a test pins each; the four `Re-read ·` rows (S9, P1c, W4, O2) over the edited text; and the round's own axes. Facts arrived labelled: the orchestrator's `bin/test` over four modules (68 passed) and ruff over the four changed .py files were executed; the smith's 19 mutations, `evidence-check --strict`, `fold-check` and `unverified-check` were read.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The closing, the docstring, the box and the changelog say a portal listing takes new versions on its own; under the default publish setting a person selects Publish for every version, and two tests pin the wider sentence | `.github/scripts/plugin_directory_check.py:277` | open | `claude.com/docs/plugins/submit` §*Publish a passing version*, fetched 2026-10-08; the frame's own first fact carries the qualifier; also `docs/release-checklist.md:372`, `changelog.md:18`, the two pins at `tests/test_the_plugin_directory_answers_the_box.py:368` and `tests/test_the_release_tail_does_not_end_at_the_tag.py:173` |
| 🟡 2 | The `claude.ai` entry admits every path, address and subdomain on the host, including per-person share and artifact links, not only the portal | `tests/test_no_real_identifiers.py:29` | open | executed probe: three plants pass the current sweep and are refused by the path-qualified rule, with the tracked tree still green |
| 🟡 3 | §6's opening paragraph and the box heading still say the command answers for the directory | `docs/release-checklist.md:360` | open | lines 321–323 *each carries the command that answers it*; line 360 **The plugin directory's answer has been read** before the command; same class as the code-block comment the build fixed |
| 🟡 4 | The third-reader fold's `Enforced by:` line and the fixed-name paragraph call a marketplace file a plugin directory | `docs/branch-and-release.md:401` | open | line 401 contradicts the paragraph above it and names this repository, which neither file lists; lines 181–185 key a directory listing on the name, and the docs say a listing belongs to the repository folder |
| 🟡 5 | The box says one file *has gone* twenty-eight days without a commit | `docs/release-checklist.md:365` | open | executed `gh api`: newest commits 2026-10-07 and 2026-10-05 |
| ⬜ 6 | A `--root` with no plugin manifest exits 1 with a traceback, against *2 for a malformed argument* | `.github/scripts/plugin_directory_check.py:144` | open | executed: exit 1, `FileNotFoundError`; unchanged from the base |
| ⬜ 7 | *the company's mail domain* does not say whose, and the address is a team one, not a person's inbox | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/spec.md:60` | open | read; meaning of the respelling unchanged |
| ⬜ 8 | The bullet calls both files outputs of the review pipeline, and the third-reader sentence drops *or tag* | `docs/branch-and-release.md:81` | open | read; the official README calls itself curated, and the submit page says *tracked branch or tag* |
| 🟢 | A failed fetch or a rate limit is a report and never reads as an absent entry; exit 0 | `.github/scripts/plugin_directory_check.py:221` | confirmed | read: the error branch returns before `entry_for`; executed: the A7 cases green |
| 🟢 | The printed lines match `spec.md` §*Data & interfaces* | `.github/scripts/plugin_directory_check.py:212` | confirmed | read, line by line |
| 🟢 | A2 against the output contract: the output contract wins | `tests/test_the_plugin_directory_answers_the_box.py:485` | confirmed | A9 forbids *listed* on a marketplace file's line; the facts A2 names are asserted unchanged |
| 🟢 | The S9, P1c, W4 and O2 re-read rows hold at `a6a366ed` | `seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md` | confirmed | executed S9's grep, W4's two cases, the one-home module and `evidence-check --strict`; P1c and O2 read against the diff |
| 🟢 | The mail-domain respelling kept every sentence's meaning | `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/questions.md:36` | confirmed | read: the diff from `0fb6fd0c` replaces the name and nothing else |
| ❓ | That SpecSeal's listing is a Console listing, and that the Console page the command prints is where it appears | `docs/release-checklist.md:374` | ❓ out of verified scope | a logged-in page; the repository owner answers it (`overview.md` §*Not verified*) |

## Paste-ready fixes

```python
        "A portal listing picks up each new version from its tracked branch "
        "without a resubmission and puts it live by its publish setting -- "
        "which by default waits for somebody to select Publish; a Console "
        "listing takes none until it is moved to the portal.",
```
```
  - a plugin submitted at the developer portal picks up new versions from
    its tracked branch and nothing is resubmitted; a version that passes
    goes live by the plugin's publish setting, which by default waits for
    somebody to select Publish;
```
```
      listing is answered on the portal's Submissions page, with its status
      and the version that is live. It picks up each new version from its
      tracked branch without a resubmission, and a version that passes goes
      live by the listing's publish setting, which by default waits for
      somebody to select Publish (`claude.com/docs/plugins/submit`, §*Publish
      a passing version*). A Console listing is answered on the Console
```
```
- The release checklist's last box no longer says to resubmit (#858). On the
  developer portal a new version is picked up from the tracked branch without
  a resubmission and goes live by the listing's publish setting, and a listing
  made through the earlier Console form takes no new version until a person
  moves it to the portal, so the instruction was wrong for both.
```
```python
    assert "without a resubmission" in closing and "publish setting" in closing, (
        "the closing lines do not say a portal listing picks up new versions "
        "without a resubmission and goes live by its publish setting"
    )
```
```python
    assert "without a resubmission" in box and "publish setting" in box, (
        "the box does not say a portal listing picks up new versions without "
        "a resubmission and goes live by its publish setting"
    )
```
```python
# A host allowed bare, or under the paths named for it, and nowhere else. The
# developer portal sits under /directory on the product's own address, and it
# is the one page where the directory's state is readable -- to a person,
# since it answers a challenge page to any script (#858). The rest of that
# host carries people's own conversations, shares and artifacts, and an
# address at it is somebody's mail, so neither is allowed.
ALLOWED_UNDER_PATHS = {"claude" + ".ai": ("/directory",)}
```
```python
                for m in DOMAIN_RE.finditer(line):
                    d = m.group(0)
                    if d in ALLOWED_UNDER_PATHS:
                        rest = line[m.end() :]
                        mail = m.start() > 0 and line[m.start() - 1] == "@"
                        if not mail and (
                            not rest.startswith("/")
                            or rest.startswith(ALLOWED_UNDER_PATHS[d])
                        ):
                            continue
                    elif any(d == a or d.endswith("." + a) for a in ALLOWED_DOMAINS):
                        continue
                    violations.append(f"{rel}:{i} {d}")
```
```python
# Built from two halves, so no file quoting this one carries the host whole.
PRODUCT_HOST = "claude" + ".ai"


def test_the_product_host_is_allowed_bare_and_under_the_directory_only(tmp_path):
    """#858 let the product's own address in for the one page the plugin
    directory check names. A share link, an address and a subdomain on the
    same host are somebody's, and stay refused."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "ok.md": f"from a {PRODUCT_HOST} account, at {PRODUCT_HOST}/directory/manage\n",
            "share.md": f"a conversation at {PRODUCT_HOST}/share/0000\n",
            "mail.md": f"write to someone@{PRODUCT_HOST}\n",
            "sub.md": f"a host under it, docs.{PRODUCT_HOST}\n",
        },
    )
    found = sorted(v.split(":")[0] for v in domains_in(root))
    assert found == ["mail.md", "share.md", "sub.md"], domains_in(root)
```
```
- [ ] **The marketplace files and the directory's page have been read** —
```
```
directory to tell. Both are boxes now. The first carries the command that
answers it; the second carries the command that reads what a script can and
names the page that answers the rest — a box a reader cannot act on is the
same defect one layer up.
```
```
Enforced by: nothing — a record rather than a rule: it measures that a marketplace file pins a commit of each outside plugin's source repository. The rule it supports, that anything reaching `main` is a merge commit, is held outside the tree by the `main` ruleset.
```
```
install — and a marketplace file keys its entry on the same name, so a rename
reads there as the plugin having vanished rather than as the plugin having
moved. `.claude-plugin/plugin.json` holds the one copy; nothing else in the
tree should spell it, which is why `plugin_directory_check.py` reads the name
out of that file instead of carrying a literal.
```
```
      files sync on somebody else's schedule, one of the two once went
```
```python
    root = os.path.abspath(args.root)
    try:
        name = plugin_name(root)
    except (OSError, ValueError, KeyError) as error:
        parser.error(f"--root {root} has no readable .claude-plugin/plugin.json: {error}")
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q -p no:cacheprovider` over `tests/test_the_plugin_directory_answers_the_box.py`, `tests/test_the_release_tail_does_not_end_at_the_tag.py`, `tests/test_no_real_identifiers.py`, `tests/test_the_rules_claude_md_names_have_one_home.py`, `tests/test_no_passage_is_pasted_into_a_second_file.py`, `tests/test_a_folded_statement_names_what_enforces_it.py` and W4's two cases in `tests/test_the_release_seal_is_drawn.py`, in a `git clone --no-local` at `a6a366ed` | exit 0, 75 passed |
| `bin/evidence-check --strict .` in the same clone | exit 0; 6826 ok, 0 drifted, 0 broken |
| `grep -c "on the tag" docs/release-checklist.md` (S9's own check) | prints 0, exit 1 |
| `plugin_directory_check.py --root` an empty directory | exit 1, `FileNotFoundError` from `plugin_name` |
| `gh api repos/<repo>/commits`, newest three, for both marketplace repositories | newest commits 2026-10-07 (official) and 2026-10-05 (community) |
| the three documentation pages `claude.com/docs/directory/publish`, `claude.com/docs/directory/submission-status`, `claude.com/docs/plugins/submit`, fetched 2026-10-08 | the publish-setting section quoted in 🟡 1; the other facts in the box hold |
| a `test_tmp_*` probe in the clone (deleted after one run): the current sweep over three plants, then the path-qualified rule over the same plants and the tracked tree | exit 0, 2 passed: the current rule admits all three, the proposed rule refuses all three and the tree stays clean |
| the full suite, repository-wide lint and typecheck | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
