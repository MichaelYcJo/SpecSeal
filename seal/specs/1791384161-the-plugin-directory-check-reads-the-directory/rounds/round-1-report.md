# 1791384161-the-plugin-directory-check-reads-the-directory — round 1 report

Reviewer: warden, round 1, at `a6a366ed73850240132aa1edebc5773fec76c768`
(executed: `git rev-parse HEAD` in the worktree and in the round's clone).
Diff: `origin/release/v0.21.0...a6a366ed`, 17 files. No earlier round exists,
so nothing was carried from a round record.

## How the findings relate

The command no longer guesses about the directory, and that part is right.
What is left is a set of sentences the work rewrote or sat beside:

1. The new sentence it added in place of *resubmit*, that a portal listing
   takes new versions *on its own*, is wider than the documentation. Under the
   default publish setting a person selects **Publish** for every version.
   Two tests pin the wider sentence (🟡 1).
2. Two coordinates in §6 of the checklist, and two in the policy document,
   still say the command answers for the directory or use *directory* for a
   marketplace file. They are the same class as the four the build removed,
   left in place (🟡 3, 🟡 4).
3. The rewritten box keeps one stale fact (🟡 5).
4. The allowlist entry admits more of the host than the one page the command
   names (🟡 2).

The command's output, its exit code on a failed fetch, the A2 judgment and the
four ledger re-reads hold (🟢 rows below).

## Findings

### 🟡 1 — A portal listing does not take new versions "on its own" under the default publish setting

`.github/scripts/plugin_directory_check.py:277` prints *A portal listing takes
new versions from its tracked branch on its own*. The docstring says the same
at lines 28–30. The box says *takes each new version from its tracked branch
on its own* at `docs/release-checklist.md:372`, and `changelog.md:18–19` says
it too. Two assertions pin the phrase:
`tests/test_the_plugin_directory_answers_the_box.py:368` and
`tests/test_the_release_tail_does_not_end_at_the_tag.py:173`.

The documentation says otherwise. `claude.com/docs/plugins/submit`,
§*Publish a passing version*, fetched 2026-10-08, says: *A version that passes
every check isn't live until it's published.* It lists the publish settings,
and the first is *An Anthropic reviewer publishes each version: the default.
For every version that passes, you select **Publish** and a reviewer publishes
it.* Only the two other settings let later versions go live by themselves.
§*Update a published plugin* on the same page closes with *A new version that
passes is published according to the plugin's publish setting.*
`claude.com/docs/directory/submission-status` says the **Approved** card names
who publishes: *an Anthropic reviewer, you, or the directory by itself.*

The frame had this right. `spec.md` §*Vocabulary*, first fact: *A new version
that passes is published according to the plugin's publish setting.* The
build dropped the qualifier. `phases/phase-3.md` says the build fetched the
publish page and read *Updates without resubmitting*; the publish-setting
section is on the submit page, which the phase record does not list.

Why it matters: the box is what a releaser reads once the listing moves to the
portal, which is the change `questions.md` Q1 anticipates. Under the default
setting, a releaser told *on its own* waits for a version that sits at
**Approved** until somebody presses **Publish**. No release would reach the
directory, which is the exact failure the box exists to catch.

What *is* true is the half the work needed: nothing is resubmitted. The fix
keeps that half and states the publish step.

### 🟡 2 — The `claude.ai` allowance admits the host's per-person links, not only the portal

`tests/test_no_real_identifiers.py:29` adds `claude.ai` to `ALLOWED_DOMAINS`.
`domains_in` accepts a match that equals an allowed host or ends with `.` plus
one. So the entry admits three things the comment does not name:

- every path on that host, including a conversation's share link, a chat and
  a published artifact. Each of those names one person's content;
- an address at that host, because the pattern matches the host after an `@`;
- every subdomain of it.

The house rule (`CONTRIBUTING.md` §*House rules*, *No real identifiers*) says
to extend the allowlist *deliberately*. The frame's grounding row argued from
fixtures: *the cheaper mistake is a fixture naming `claude.ai` by hand, which
no example here has reason to write*. It did not weigh records. Sessions in
this repository produce links on that host routinely (an artifact published
from a review or a handoff is one), and a round record or report that quotes
one is a tracked file. Before this change such a link turned the sweep red.
After it, the sweep passes it.

Executed (probe, deleted): with the entry as built, a tracked file holding a
share link on that host, one holding an address at it, and one naming a
subdomain all pass the sweep. With the path-qualified allowance below, all
three are refused and the whole tracked tree at `a6a366ed` still passes. Every
use of the host in the tree today is the bare name or a path under
`/directory`, so the narrower rule costs no rewording.

### 🟡 3 — §6 still says the command answers for the directory

The box heading at `docs/release-checklist.md:360` reads **The plugin
directory's answer has been read** — followed by the command. That is the
shape of the box above it, where the command after the dash is the answer.
The section's opening paragraph at lines 321–323 says so outright: *Both are
boxes now, and each carries the command that answers it*. One of the two acts
it names is *telling the plugin directory*, which the command does not read.

`spec.md` §*Scope* item 4 asks for the vocabulary to hold in every file the
work touches, and agent-contract §12 asks for every coordinate of the class.
The build found a fourth carrier in this section, the code block's comment,
and fixed it (`phases/phase-2.md`). These two were left. A releaser ticks a
box by its heading. Here the heading still tells them the command gave them
the directory's answer.

### 🟡 4 — The policy document still calls a marketplace file "a plugin directory" in two places

`docs/branch-and-release.md:401` is the `Enforced by:` line of the fold whose
third-reader paragraph this work rewrote. It says the record *measures that a
plugin directory pins a commit of this repository*. The paragraph above it
now says the measurement was over *one marketplace file's 310 entries*. The
measurement also never covered this repository: SpecSeal has no entry in
either file. The line contradicts the paragraph it closes.

Lines 181–185 of the same section say *a directory listing is keyed on the
same name, so a rename reads there as the plugin having vanished*, and call
the command *the directory check*. Under the work's vocabulary *the directory*
is the catalog inside Claude. The documentation says a listing there belongs
to the repository folder (`claude.com/docs/directory/publish`, *the first
organization to submit a given repository folder holds that listing*). It
also says the listed name *follows the version that's live*
(`claude.com/docs/plugins/submit`). A marketplace file is what keys an entry
on the name, and the command's own docstring says a rename shows there as
*not an entry*. `phases/phase-2.md` left this paragraph out because it was
*outside the two sentences*. It is in the touched file and states the class.

Both coordinates sit in §*Work accumulates on a release branch*, which the
P1c and O2 re-read rows anchor, so the fix re-stamps those two.

### 🟡 5 — The rewritten box keeps a day count that is false today

`docs/release-checklist.md:365–366` says *one of the two has gone twenty-eight
days without a commit*, with no date. Executed 2026-10-08 through
`gh api repos/<repo>/commits`: the official repository's newest commit is
2026-10-07 and the community repository's is 2026-10-05. The docstring dates
the same figure (*by the time this was first written*). The box was rewritten
by this work and kept the present-tense version. The decision it supports
still holds without it, and one word makes it true.

### ⬜ 6 — A `--root` with no plugin manifest is a traceback, not exit 2

Executed: `plugin_directory_check.py --root <an empty directory>` exits 1 and
prints `FileNotFoundError` from `plugin_name`
(`.github/scripts/plugin_directory_check.py:144`). `spec.md` §*Data &
interfaces* says *0 for every outcome, 2 for a malformed argument*. The
docstring says *The only non-zero exit here is a malformed argument*. This is
unchanged from the base (`plugin_name` is the same function there). The
default `--root` is the repository itself, so the releaser at the box never
reaches it.

### ⬜ 7 — "the company's mail domain" does not say whose

`spec.md:60` and `:174`, and `questions.md:36`, replaced the spelled domain
with *the company's mail domain*. The meaning is unchanged (read: the diff of
those lines from `0fb6fd0c`). But this repository has two companies a reader
could mean, and its rule on whose (`skills/writing-style/SKILL.md`, the
section `CLAUDE.md` links) asks for the owner to be named. The same row also
says the address is *a person's inbox*; the documentation gives a team
address.

### ⬜ 8 — Two policy sentences state the sources a little wider than they are

`docs/branch-and-release.md:81` calls both files *public outputs of the
directory's review pipeline*. Only the community README says that (*synced
nightly from Anthropic's internal review pipeline*). The official README
calls itself *a curated directory* that partners submit to for inclusion.
`docs/branch-and-release.md:169–170` says the directory serves *a scanned
commit of the branch the submission tracks*; the submit page says *the
tracked branch or tag*. Neither changes what anyone does.

## The account, checked

- **Claimed** (`overview.md`): the three documentation facts were opened by
  the build too. **Found:** true for the two pages `phases/phase-3.md` names.
  The publish setting, on the third page, is where 🟡 1 comes from.
- **Claimed** (`phases/phase-2.md`): A9 checked every *directory* hit in the
  five texts. **Found:** true inside the five, and the class reaches two lines
  of §6 and two of the policy section that the count left out (🟡 3, 🟡 4).
- **Claimed** (`phases/phase-1.md`, `phases/phase-2.md`): each new pin was
  seen red, with 19 mutations. Read, not re-run. The moved pins in 🟡 1 are
  the ones D5 and M5 broke. They went red, and they pin a sentence that is too
  wide.
- **Claimed** (spawn prompt): `bin/test` over four modules printed 68 passed.
  Re-run here over a wider narrow set: 75 passed, exit 0.

## Attack items, answered

1. **Output and exit code against §*Data & interfaces*.** Read: the header,
   the two-line *could not be read*, the one-line absent entry, both entry
   forms with the three ancestry lines, and the closing block all match.
   A failed fetch or a rate limit (`HTTPError` 403 or 429 from
   `api.github.com`) returns from `fetch` as `HTTP <code>`. `line` takes the
   error branch before it looks for an entry
   (`.github/scripts/plugin_directory_check.py:221–226`). So a failure never
   reads as *not an entry*, and the run exits 0. The one exit outside the
   contract is ⬜ 6.
2. **A2 against the output contract.** The output contract should win, and
   did. A2's *as today* is about the pinned commit and the ancestry answers,
   and those assertions are unchanged. Keeping `"listed" in head` would keep
   the directory's word on a marketplace file's line, which A9 forbids. The
   divergence row is honest. It counts two assertions; the four renamed cases
   are recorded in `phases/phase-1.md`, and `.test_durations` keeps four stale
   keys, which `CONTRIBUTING.md` accepts as an imbalance only.
3. **The allowlist.** 🟡 2. The respelling of the mail domain kept every
   sentence's meaning (⬜ 7 is about naming, not truth).
4. **Facts about the portal and the Console.** Against the three pages,
   fetched 2026-10-08: *Submissions page* with status and live version,
   Console page address (the docs link it as **Plugin submissions**), a Console
   listing *stays as it is*, the move section's title, Withdraw or email, and
   *Not live yet* all hold. *On its own* does not (🟡 1). The day count is
   stale (🟡 5). Pinned: the box's kinds, pages, *on its own*, no
   *resubmit*, the dated kind sentence; the bullet's *two marketplace files*,
   *not among its answers*, *Nothing fires it*. Not pinned: the day count,
   *Whether it shows up at all…*, the bullet's *prints the page a person
   opens* and *moving a Console listing … is a person's act*, and the
   third-reader sentence (unpinned on purpose, A8).
5. **The four re-read rows.** Each holds over the edited text. S9: executed,
   `grep -c "on the tag" docs/release-checklist.md` prints 0, exit 1, and
   neither trigger nor input moved. P1c: read, the closer's paragraphs in both
   documents are outside the diff. W4: executed, its two cited cases green,
   and the seal bullet and the `Enforced by:` line's S2 case are untouched.
   O2: read, the merge-method table is outside the diff, and
   `tests/test_the_rules_claude_md_names_have_one_home.py` ran green. The
   fixes for 🟡 1, 🟡 3, 🟡 4 and 🟡 5 move those anchors again.
6. **Own axes.** 🟡 3, 🟡 4, ⬜ 6, ⬜ 8.

## Regression tests to plant

- `tests/test_no_real_identifiers.py`: the case in fix 2, which plants a share
  link, an address and a subdomain on the product host and expects all three
  refused, and a bare mention and a `/directory` path allowed. Seen red by the
  probe: the current rule passes all three plants.
- `tests/test_the_plugin_directory_answers_the_box.py:368` and
  `tests/test_the_release_tail_does_not_end_at_the_tag.py:173`: the *on its
  own* pins move to *without a resubmission* and *publish setting* (fix 1).
  Each should be seen red against the text at `a6a366ed` before it is
  committed.

## Facts for the evidence ledger

- The publish-setting fact is about somebody else's documentation and has no
  anchor in this tree. It belongs as a dated sentence beside the other three
  in the command's docstring, as `spec.md` §*Data & interfaces* decided for the
  others.
- The fixes for 🟡 1, 🟡 3 and 🟡 5 change `docs/release-checklist.md`
  §*6. After the merge*, and 🟡 4 changes §*Work accumulates on a release
  branch*. The S9, P1c, W4 and O2 rows in this work item's fragment drift and
  are re-read again in the fix pass.

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

## Paste-ready fixes

### 🟡 1 — the publish step, in all four places and both pins

`.github/scripts/plugin_directory_check.py`, the last string of `closing()`
(lines 277–278):

```python
        "A portal listing picks up each new version from its tracked branch "
        "without a resubmission and puts it live by its publish setting -- "
        "which by default waits for somebody to select Publish; a Console "
        "listing takes none until it is moved to the portal.",
```

The same file's docstring, first bullet of the three facts (lines 28–30):

```
  - a plugin submitted at the developer portal picks up new versions from
    its tracked branch and nothing is resubmitted; a version that passes
    goes live by the plugin's publish setting, which by default waits for
    somebody to select Publish;
```

`docs/release-checklist.md`, lines 371–373 up to *answered on the Console*:

```
      listing is answered on the portal's Submissions page, with its status
      and the version that is live. It picks up each new version from its
      tracked branch without a resubmission, and a version that passes goes
      live by the listing's publish setting, which by default waits for
      somebody to select Publish (`claude.com/docs/plugins/submit`, §*Publish
      a passing version*). A Console listing is answered on the Console
```

`changelog.md`, the box entry's second sentence:

```
- The release checklist's last box no longer says to resubmit (#858). On the
  developer portal a new version is picked up from the tracked branch without
  a resubmission and goes live by the listing's publish setting, and a listing
  made through the earlier Console form takes no new version until a person
  moves it to the portal, so the instruction was wrong for both.
```

`tests/test_the_plugin_directory_answers_the_box.py:368–371`:

```python
    assert "without a resubmission" in closing and "publish setting" in closing, (
        "the closing lines do not say a portal listing picks up new versions "
        "without a resubmission and goes live by its publish setting"
    )
```

`tests/test_the_release_tail_does_not_end_at_the_tag.py:173–176`:

```python
    assert "without a resubmission" in box and "publish setting" in box, (
        "the box does not say a portal listing picks up new versions without "
        "a resubmission and goes live by its publish setting"
    )
```

### 🟡 2 — allow the product host bare and under `/directory` only

`tests/test_no_real_identifiers.py`: remove the `claude.ai` entry and its
comment from `ALLOWED_DOMAINS`, and add after the tuple:

```python
# A host allowed bare, or under the paths named for it, and nowhere else. The
# developer portal sits under /directory on the product's own address, and it
# is the one page where the directory's state is readable -- to a person,
# since it answers a challenge page to any script (#858). The rest of that
# host carries people's own conversations, shares and artifacts, and an
# address at it is somebody's mail, so neither is allowed.
ALLOWED_UNDER_PATHS = {"claude" + ".ai": ("/directory",)}
```

`domains_in`, the inner loop:

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

The case, beside the other can-fail cases:

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

### 🟡 3 — §6's heading and opening paragraph

`docs/release-checklist.md:360`:

```
- [ ] **The marketplace files and the directory's page have been read** —
```

`docs/release-checklist.md:322–323`, from *directory to tell.*:

```
directory to tell. Both are boxes now. The first carries the command that
answers it; the second carries the command that reads what a script can and
names the page that answers the rest — a box a reader cannot act on is the
same defect one layer up.
```

### 🟡 4 — the fold line and the fixed-name paragraph

`docs/branch-and-release.md:401`:

```
Enforced by: nothing — a record rather than a rule: it measures that a marketplace file pins a commit of each outside plugin's source repository. The rule it supports, that anything reaching `main` is a merge commit, is held outside the tree by the `main` ruleset.
```

`docs/branch-and-release.md:181–185`, from *install —*:

```
install — and a marketplace file keys its entry on the same name, so a rename
reads there as the plugin having vanished rather than as the plugin having
moved. `.claude-plugin/plugin.json` holds the one copy; nothing else in the
tree should spell it, which is why `plugin_directory_check.py` reads the name
out of that file instead of carrying a literal.
```

### 🟡 5 — the day count, made historical

`docs/release-checklist.md:365`:

```
      files sync on somebody else's schedule, one of the two once went
```

### ⬜ 6 — a root with no manifest is a malformed argument

`.github/scripts/plugin_directory_check.py`, `main()`:

```python
    root = os.path.abspath(args.root)
    try:
        name = plugin_name(root)
    except (OSError, ValueError, KeyError) as error:
        parser.error(f"--root {root} has no readable .claude-plugin/plugin.json: {error}")
```

Needs a fix: yes — 🟡 1 (a portal listing does not go live on its own under
the default publish setting, and two tests pin the wider sentence), 🟡 2 (the
host allowance admits per-person links, addresses and subdomains), 🟡 3 and
🟡 4 (four coordinates still state the class the work removes), 🟡 5 (a stale
day count in the rewritten box)
Loses a record or crashes: yes — ⬜ 6 only: a `--root` with no plugin manifest
ends in a traceback and exit 1. It is unchanged from the base, and the default
root never reaches it

## Proof block

Opened in this round, at `a6a366ed` unless named otherwise:

- `.github/scripts/plugin_directory_check.py` (whole), and its base version's
  `plugin_name` line through `git show`
- `tests/test_the_plugin_directory_answers_the_box.py` (diff),
  `tests/test_the_release_tail_does_not_end_at_the_tag.py` (lines 1–140,
  141–332), `tests/test_no_real_identifiers.py` (lines 1–140),
  `tests/conftest.py` (`build_tracked_tree`)
- `docs/release-checklist.md` (lines 300–385), `docs/branch-and-release.md`
  (lines 55–105, 150–190, 385–404, and its heading and marker map),
  `CONTRIBUTING.md` (§*House rules* bullet, lines 184–200)
- `seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/`:
  `spec.md`, `questions.md`, `overview.md`, `routing.md`, `handoff.md`,
  `plan.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`,
  `changelog.md`
- `seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md`;
  the S9 row in `seal/releases/0.11.1.md`, P1c in `seal/releases/0.15.0.md`,
  W4 in `seal/releases/0.18.0.md`, O2 in `seal/releases/0.18.1.md`
- `tests/test_a_folded_statement_names_what_enforces_it.py` (its def and
  marker lines)
- issue #858 (`gh issue view`), both marketplace READMEs and their commit
  lists (`gh api`), and the three documentation pages named above

The round's clone and every probe leaving were removed before this report was
handed over.
