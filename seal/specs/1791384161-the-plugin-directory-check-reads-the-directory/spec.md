# Feature Specification: the plugin directory check reads the directory

<!-- seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

**The command behind the last box of `docs/release-checklist.md` reads two
GitHub files and tells the releaser the plugin is "not listed" and to submit
it — about a directory it never read.** On 2026-10-07 the owner's Console page
showed the plugin published while the command said *not listed* in both files
(#858). The command's inputs are real and public, and its sentence about the
directory is a guess (#834, part 8 row 76). This work keeps the observation and
removes the guess: the command says what the two files hold and says that the
directory itself was not read, naming the page a person opens instead.

## Vocabulary — four things the word "directory" has been covering

The documents outside this repository use one word for several catalogs, and
the official marketplace file's own README calls itself a *Plugins Directory*.
`skills/writing-style/SKILL.md` §*여럿이 가질 수 있는 것은 누구 것인지 밝힌다*
is the rule; these are the names this work item uses in every file it touches.

| Name here | What it is | Readable by a script? |
|---|---|---|
| **the directory** | Anthropic's catalog of plugins that people browse inside Claude — claude.ai, the desktop and mobile apps, Cowork and Claude Code share it. Where a listing lives, and what the portal publishes to | **No.** Measured 2026-10-07: `claude.ai/directory`, `/directory/manage` and `/directory/plugins` each answer HTTP 403 with a challenge page titled *Just a moment...* to a plain client and to one carrying a browser user agent (six probes, `curl`). `claude.com/docs/llms.txt` lists no page describing an API for it |
| **the marketplace files** | the two public `.claude-plugin/marketplace.json` files on GitHub: the official one (315 entries on 2026-10-07) and the community one (2,284). Their READMEs, read the same day: the community file is *a read-only mirror … synced nightly from Anthropic's internal review pipeline*, every entry *submitted via claude.ai*; the official file's external-plugins folder takes entries through the same submission link. They are what `claude plugin marketplace add anthropics/<name>` installs from | **Yes**, through `api.github.com`, which is what the command reads today |
| **the portal** | `claude.ai/directory/manage`, the developer portal: a submission's status (Draft, Scanning, Needs changes, In review, Approved, Published, Not live yet, Delisted, Withdrawn) and, for a published plugin, which version is live | No — the owner's logged-in page |
| **the Console page** | `platform.claude.com/plugins/submissions`, the earlier submission form's page. The docs: *the earlier Claude Console form for plugin submissions is no longer supported*; a listing made there *stays as it is* and gets none of what the portal adds — new versions scanned and served, a status, usage figures | No — the owner's logged-in page |
| **the marketplace website** | `claude.com/marketplace/plugins` (what `claude.com/plugins/` redirects to): public, 341 plugin pages in its sitemap on 2026-10-07, 24 of them in the page's own HTML. The docs call it *the website where you browse plugins, connectors, partner products, and service partners* — a surface beside the directory, not the directory | Yes, as a website's HTML and sitemap — and **this work does not read it** (§*Scope*, Out) |

Three facts the docs give, each read on 2026-10-07 at
`claude.com/docs/directory/publish`, `claude.com/docs/plugins/submit` and
`claude.com/docs/directory/submission-status`:

- **On the portal, nothing is resubmitted.** *Merge to the tracked branch, and
  the directory picks up the commit, checks it, and publishes it.* A new
  version that passes is published according to the plugin's publish setting.
- **A Console listing never gets a new version.** Moving it is a person's act:
  *Withdraw*, then submit again at the portal — or, where there is no Withdraw
  button, email the address the publish page gives, to have it moved. Until
  then the portal can refuse the same repository with *Already submitted by
  another organization*.
- **Published is the only installable status**, and *Not live yet* is a
  status of its own: *marked published, and nothing is listed yet*.

**One more measurement, so the frame does not rest on the ticket's prose.**
The short link both READMEs still name as the submission form,
`clau.de/plugin-directory-submission`, answered HTTP 302 to
`claude.com/docs/directory/publish` on 2026-10-07 — a documentation page,
not a form. The command's constant named PORTAL carries that short link and
tells a reader to *submit through* it. (`.de` is outside the identifier
sweep's TLD list, which is how a real short-link domain sat in the tree
unseen.)

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a command that claims an answer it cannot observe and one that refuses the unknown and names the page, the first stops a person for nothing at every release and the second spends them once, at the page. Decides §*Scope* item 1 |
| #834's inventory, `inventory/8-evidence.md` row 76 on branch `chore/834-every-reader-and-record-is-inventoried` (`plugin_directory_check.py`, *"listed" inferred from two GitHub repos*, class reader-guess), and the brief every 0.21.0 frame was given from it | The design direction: keep the observed input, refuse what is not observed, and name what the frame removes. §*Data & interfaces* says the input class of every reader this work touches and lists the removals |
| `CONTRIBUTING.md` §*House rules*, *No real identifiers* — `tests/test_no_real_identifiers.py` enforces it; *extend its allowlist deliberately, never to make a test pass* | The page a person opens is `claude.ai/directory/manage`, and `claude.ai` is not in `ALLOWED_DOMAINS`. It enters deliberately, as the product's own address beside `claude.com` (*official docs this plugin is built against*), with the reason in the comment. The company's mail domain does not enter: the email address stays on the docs page the box links, so no document here carries a person's inbox |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The allowlist is a check CI runs. Direction: it allows one more domain, and the cheaper mistake is a fixture naming `claude.ai` by hand, which no example here has reason to write. The sweep's own can-fail case stays red. Prompt budget: zero |
| `docs/branch-and-release.md` §*Cutting a release*, the release-tail bullet *The plugin directory is read by a command that never fails a release* | The sentence that says the command answers *per directory, whether the plugin is listed* is the claim this work withdraws; the bullet is rewritten to say what the command reads and what it refuses to say. *Nothing fires it* and *Submitting … is a person's act* stay true |
| `docs/branch-and-release.md` §*What breaks when the last row is squashed*, the third-reader paragraph | Its measurement (258 of 310 entries carry a `sha`) is about a marketplace file and is still true; the paragraph names the file as what it is, and adds that the directory serves a scanned commit of the tracked branch — a fourth reader of a release-branch commit, from the docs. The three pinned phrases stay |
| `docs/release-checklist.md` §*6. After the merge*, the last box | The box is rewritten: what the command reads, the page a person opens per kind of listing, which kind SpecSeal's listing is and when that was read, and no *resubmit* |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | S9 (0.11.1), P1c (0.15.0) and W4 (0.18.0) anchor `docs/release-checklist.md#"## 6. After the merge"`, and W4 also `docs/branch-and-release.md#"## Cutting a release"`; both units move here. Their re-reads are `Re-read ·` rows in this work item's fragment, each written after the claim was read against the new text |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | `changelog.md` and the ledger fragment live in this directory; `changelog/0.13.1.md` and the released ledger files are history and are not edited |
| `agent-contract` §12, §14, §15 | The class is the inference, at every coordinate that states it (the command's two lines, its docstring, the box, the policy bullet, two test pins). A changed line a person reads is pinned in the same commit. Every moved or new pin is seen red against the text it replaces |
| Work item `1790076050-the-release-tail-is-three-acts-no-document-names` (#417; its directory has since been retired from the tree, so it is read in history at `f2943c04^`) — `spec.md` §*Judgments this frame made* 5 and 6, and `questions.md` Q1 | Its judgment 6 — *the box compares the pinned commit against the released one and says to resubmit … the right instruction under either answer* — rested on not knowing how an update reaches a listed plugin. The docs answer it now (above), and the instruction is wrong under both answers: on the portal nothing is resubmitted, and a Console listing takes no new version. Q1 of that item closes by reading, not by a person |

## Scope

### In

1. **The command stops saying what it did not read.** Per marketplace file it
   still says whether an entry under this plugin's name is there, how many
   entries it read, which commit an entry pins and whether that commit is an
   ancestor of `main` (three answers). What goes: the sentence *Submit it
   through …* on an absent entry, the sentence *resubmit through …* on a pin
   behind `main`, and the constant PORTAL both sentences name. What arrives: a
   closing block saying the directory itself was not read because no script
   can reach it, and naming the two pages a person opens — the portal's
   Submissions page for a portal listing, the Console page for a Console
   listing — with one line saying that a portal listing takes new versions
   from the tracked branch on its own.
2. **The box names the page, drops *resubmit*, and records which kind SpecSeal's
   listing is.** It keeps *reports and never fails*. It says what the command
   reads and what it cannot; which page answers *is it published, and at which
   version* for each kind of listing; that SpecSeal's listing is a Console
   listing, read on the Console page by the owner on 2026-10-07 — labelled as
   that reading, with its date, because nothing in the tree can see the move
   when it happens; that a Console listing takes no new version, so no release
   reaches the directory through it until it is moved; and where the move is
   documented (`claude.com/docs/directory/publish`, §*Move an earlier
   submission to the developer portal*). The open-question sentence about how
   an update reaches a listed plugin leaves: it is answered.
3. **The two policy sentences follow the box.** The release-tail bullet in
   `docs/branch-and-release.md` §*Cutting a release* says what the command
   reads (the marketplace files) and what it refuses to say (the directory's
   state), keeping *Nothing fires it; a person runs it at the checklist's box*
   and its *Enforced by:* line. The third-reader paragraph names a marketplace
   file as the reader that pins a commit, keeps its measurement and its three
   pinned phrases, and adds that the directory serves a scanned commit of the
   tracked branch.
4. **The vocabulary of §*Vocabulary* holds in every file this work touches** —
   the command (docstring and output), its test module, the box, the two policy
   sentences, the changelog fragment. *The directory* is the claude.ai one and
   nothing else; the GitHub files are *the marketplace files*.
5. **The pins move with the text they pin, in the same commit, each seen red.**
   `tests/test_the_plugin_directory_answers_the_box.py` loses the assertion that
   an absent entry's line names PORTAL and gains: an absent line names the file
   and its count and names no act; the run's closing lines say the directory was
   not read and name the two pages; the constant is gone.
   `tests/test_the_release_tail_does_not_end_at_the_tag.py`'s box case stops
   pinning *Not listed* and *pinning an older commit* and pins the new box:
   *reports and never fails*, the sentence that the directory is readable from
   nowhere a script can reach, the two pages by name, the kind sentence with a
   date, and the absence of *resubmit*.
6. **`claude.ai` enters `ALLOWED_DOMAINS`**, with a comment naming it as the
   product's own address — the one page where the directory's state is
   readable — and nothing else enters.
7. **The fragments.** `changelog.md` in this directory, and a ledger fragment
   carrying the `Re-read ·` rows for S9, P1c and W4 and any row this work earns
   (§*Data & interfaces* says what gets none).

### Out

- **Reading the directory.** Measured unreachable from a script (§*Vocabulary*).
  A reader that scraped a challenge-walled page would be red on somebody
  else's schedule, which is the gate #417 refused with a measurement.
- **Reading the marketplace website or its sitemap.** It is a third catalog —
  341 pages against 2,284 entries — with no documented relation to the
  directory, in a website's generated XML whose shape nobody here owns, and
  SpecSeal is in neither today (0 of 341, measured 2026-10-07). It would add a
  reader and change no answer. Named here so nobody re-proposes it without the
  counts.
- **Reading the portal or the Console page with the owner's session.** A
  credential in CI nobody asked for, for a page that is one person's.
- **Deleting the command.** A box with no command is the shape #386 measured
  being skipped three releases running, and what the command reads is a true
  observation: an entry's pin is the commit a Claude Code install from that
  marketplace carries, and the ancestry answer guards the squash rule.
- **Dropping the official file's read.** Considered: SpecSeal has no partner
  entry there. Kept: its README takes external plugins through the same
  submission link, so it is a second public output of the same pipeline, at
  one HTTPS call.
- **The move itself — withdrawing, resubmitting, emailing.** The owner's act,
  `questions.md` Q1. The frame works under either answer: the box's kind
  sentence is one dated line, and the build ships it as *Console*.
- **Reaching into released records.** `changelog/0.13.1.md`, the released
  ledger rows and the retired work item's records say what was true when
  written. The word *directory* in them stays.
- **`README.md`'s install lines and `.claude-plugin/marketplace.json`.** They
  install from this repository's own marketplace file. Unrelated.
- **A gate.** Unchanged from #417: the command reports and exits 0, and nothing
  fires it.
- **The siblings' units.** This work touches no file another 0.21.0 frame
  names (`chain_check`, `round_record`, `evidence_check`, `broad_gate`,
  `generic_units`, the hooks). The one shared document is
  `docs/release-checklist.md`'s §6, which #869 and #864 do not touch.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The command claims nothing about the directory | Given both marketplace files fetched, with or without an entry · When the run prints · Then no line says the plugin is or is not listed *in the directory*, no line names a submission or resubmission, the constant PORTAL does not exist, and the closing lines say the directory was not read and name the portal's Submissions page and the Console page, each by the kind of listing it answers for | cases over the module with its fetch replaced: `hasattr` on the constant is false; the joined output carries neither *submit* nor *resubmit*; the closing lines carry *was not read*, *Submissions* and *Console* |
| A2 | What a file holds is still observed, unchanged | Given an entry with a `sha` · When its line prints · Then it names the pinned commit and one of the three ancestry answers, as today | the existing cases of `tests/test_the_plugin_directory_answers_the_box.py`, green without edit |
| A3 | An absent entry says which file, how many, and no act | Given a file with no entry under the name · When its line prints · Then it says the name is not an entry in that file, over how many entries, and nothing follows telling the reader to do anything | a case: *not an entry* and the count on the line, and the line is the whole answer for that file |
| A4 | A failed read is still a report | Given a fetch that fails or a payload that is not a directory file · When the run prints · Then it reports and exits 0 | the existing A7 cases of #417, green without edit |
| A5 | The box names the page and drops *resubmit* | Given a reader at the last box of §6 · When they read it · Then it says the command reads the marketplace files and that the directory is readable from nowhere a script can reach; names the portal's Submissions page and the Console page and which kind of listing each answers for; says a portal listing updates from the tracked branch on its own; and nowhere says *resubmit* | the box case in `tests/test_the_release_tail_does_not_end_at_the_tag.py`, pins moved in the same commit, each seen red against the current box |
| A6 | The box records which kind SpecSeal's listing is, as a dated reading | Given the same box · When they read it · Then one sentence says SpecSeal's listing is a Console listing, read on the Console page by the owner on 2026-10-07, that such a listing takes no new version until it is moved, and where the move is documented | the same case: the kind word, a date in `YYYY-MM-DD` form on the same sentence, and the docs page's path |
| A7 | The policy bullet says what the command reads and refuses | Given `docs/branch-and-release.md`'s release-tail bullet · When read · Then it names the marketplace files as the input, says the directory's state is not among what it answers, and still says *Nothing fires it* | `test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag` stays green; one new assertion on the bullet, seen red |
| A8 | The third reader is named as what it is | Given §*What breaks when the last row is squashed* · When read · Then the paragraph says a marketplace file pins a commit of its source repository, keeps its 2026-09-22 measurement, and says the directory serves a scanned commit of the tracked branch | `test_an_outside_directory_is_in_the_enumeration` stays green; the added sentence is read, not pinned — it is a fact from the docs, not a rule |
| A9 | One vocabulary in every touched file | Given the command's docstring and output, its test module, the box and the two policy sentences · When read · Then *the directory* names the claude.ai catalog only and the GitHub files are *marketplace files* | read by the reviewer; `grep -n directory` over the five files, each hit checked |
| A10 | `claude.ai` is allowed deliberately | Given `ALLOWED_DOMAINS` · When read · Then it carries `claude.ai` with a comment naming the page it is for, and not the company's mail domain; the sweep's can-fail case still refuses a planted domain | `tests/test_no_real_identifiers.py`, whole module |
| A11 | Nothing restates a home | Given the command and its test module · When `tests/test_the_rules_claude_md_names_have_one_home.py` runs · Then both still name `CONTRIBUTING.md` and *House rules* for the identifiers rule, and the box and the bullet share no run of words the paste ratchet counts | that module and `tests/test_no_passage_is_pasted_into_a_second_file.py`, green |

## Data & interfaces

**The command's output, line by line.** `plugin 'specseal', against main`,
then per marketplace file one of: *could not be read — <why>* (two lines, as
today); *'<name>' is not an entry in <file> (<N> entries).* — one line, the
whole answer; *an entry, pinning <sha12> of <url>* followed by the ancestry
line (three forms, as today); *an entry, pinning no commit (source: …)*. Then
the closing block: the directory was not read and cannot be from a script;
the portal's Submissions page answers for a portal listing — status and the
version card; the Console page answers for a Console listing; a portal
listing takes new versions from the tracked branch on its own. Exit codes are
unchanged: 0 for every outcome, 2 for a malformed argument.

**Input class of every reader this work touches**, for #835's registry:

| Reader | Reads | Class | On the unknown |
|---|---|---|---|
| `fetch` | a public file through the documented contents API on `api.github.com` | observed | *could not be read*, exit 0 |
| `entry_for` and `pinned` | a marketplace file in somebody else's format, at the four `source` shapes measured 2026-09-22 (53 string-source entries of 315 today, 262 object) | observed, foreign format | a payload that is not a `plugins` list: *could not be read*; a shape with no `sha`: *pinning no commit* |
| `is_ancestor` | git plumbing in this clone | observed | the third answer, *unknown here* |
| the directory's state | **nothing** | refused — named as unread | the closing block names the page a person opens |
| which kind SpecSeal's listing is | the box's one dated sentence, the owner's reading | a person's record | the sentence carries its date and whose reading it is, so a reader can tell it has aged |

**What this work removes**, so the brief's question is answered in one place:
the constant PORTAL and the short link it holds; the two instructions that send
a reader to it; the docstring's two paragraphs saying no document tells how an
update reaches a listed plugin and pointing at #417's Q1; the box's three
sentences (*Not listed means submitting it…*, *resubmit through the same
form*, *Whether an update reaches a listed plugin on its own is readable from
nowhere public — it is an open question…*); the policy bullet's claim *per
directory, whether the plugin is listed*; the test pin on PORTAL and the two
box pins on *Not listed* and *pinning an older commit*. Seven readers of one
guess, and the guess with them.

**What deliberately gets no ledger row.** The measurement that the directory
is unreachable is about somebody else's server and has no anchor in this tree;
it is a dated sentence in the command's docstring and in this file. The
command's behaviour is pinned case for case by its own module, which is the
reason #417's fragment gave for the same choice. What earns a row is the
re-read of S9, P1c and W4, whose units this work moves.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline. The owner's
act — whether to move the Console listing to the portal — is Q1 there, and the
build ships under its default.

Framed 2026-10-07 by framer, before the build.
