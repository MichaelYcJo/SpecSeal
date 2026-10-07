# the plugin directory check reads the directory — questions for the planner

<!-- seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is `automation`: nobody will be asked anything mid-run.** The
default of each row is what ships; the row exists so a person can overturn it
later, and so the next reader can tell a question that was decided from one
that was never met.

## What the ticket left open and the tree or a measurement answered

These were open in #858 and are not rows. `spec.md` §*Vocabulary* and
§*Grounding* hold each with its grounds.

- **Whether the directory is publicly readable in a form a script can
  observe** — no. Measured 2026-10-07 with six `curl` probes over three
  `claude.ai/directory` paths, with and without a browser user agent: HTTP
  403 and a challenge page each time. The docs index lists no API. So the
  box names the page a person checks, as the ticket's second branch says.
- **Whether an update reaches a listed plugin on its own** — #417's Q1,
  carried as the owner's for two releases. Read from the docs: on the portal,
  yes, from the tracked branch; a Console listing never takes a new version.
  The old instruction *resubmit* was wrong under both answers.
- **Whether the two GitHub files are the directory** — no, and not nothing:
  the community file's README calls itself a nightly mirror from the review
  pipeline and the official file's external entries come through the same
  submission link. They are the pipeline's public outputs, read as such.
- **Whether to keep the command** — yes. A box with no command is #386's
  measured failure, and the files' pin and ancestry answers are observed.
- **Whether to read the marketplace website or its sitemap** — no; a third
  catalog, 341 pages against 2,284 entries, SpecSeal in neither.
- **Whether `claude.ai` enters the identifier allowlist** — yes, deliberately,
  as the product's own address; `anthropic.com` does not, because the email
  stays on the docs page the box links.
- **Which kind of listing SpecSeal has today** — a Console listing, by the
  owner's reading of the Console page on 2026-10-07 in #858. The frame could
  not open that page (no login) and labels it as that reading, with its date.
- **Whether the box becomes a gate** — no, unchanged from #417: it reports
  and never fails.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Move SpecSeal's Console submission to the developer portal, or leave it where it is? The docs (`claude.com/docs/directory/publish` §*Move an earlier submission to the developer portal*, read 2026-10-07) say a Console listing *stays as it is* and gets none of what the portal adds — new versions scanned and served to the people who have the plugin, a status per submission, usage figures — and that the Console form is no longer supported. The move is: open **Plugin submissions** in the Console; where the submission has a **Withdraw** button, withdraw it and submit the plugin again at `claude.ai/directory/manage` from a claude.ai account; where it has no Withdraw button, email the address that page gives, to have it moved rather than resubmitted. Until it is withdrawn or moved, the portal can refuse the same repository with *Already submitted by another organization* | **a person** — the repository owner, who made the Console submission and holds the account the portal would use. Nothing in the tree or on any public page says which button the owner's submission shows | **move** — after the move, every merge to `main` is scanned and, once published, served on its own; the box's dated *Console* sentence is changed to *portal* in a one-line follow-up commit, and the portal's Submissions page becomes the page the releaser opens · **leave** — the listing stays as it is and no release reaches the directory through it; the box keeps saying so, dated, and the Console page stays the page the releaser opens | **leave, as of 2026-10-07, recorded in the box with its date and whose reading it is.** The build ships under this default and needs no change under the other answer except that one dated sentence, which the owner's own move is what triggers | ⬜ |
| Q2 | Is SpecSeal visible in the directory today — does a search inside Claude for *SpecSeal* find it? The Console page says *published*; the two marketplace files, mirrored nightly from the review pipeline, carry no entry three weeks on (0 of 315 and 0 of 2,284 on 2026-10-07); and the portal's own status table has a *Not live yet* state — *marked published, and nothing is listed yet* | **a measurement** — one search inside Claude by anyone with a Claude account. The frame could not run it: the directory answers a challenge page to any script and the brief forbids a login. It is not a person's judgment, only a person's browser | **found** — the Console listing is live at whatever version was submitted on 2026-09-16, and the box's Console sentence is exactly right · **not found** — *published* on the Console page is not *listed* in the directory, which strengthens Q1's *move* and changes nothing in what is built | Nothing is built differently either way. The box says that visibility is what the search inside Claude answers; `overview.md` §*Not verified* carries this row with its answerer | ⬜ |
| Q3 | Does rewriting the box and the release-tail bullet leave the pair (`docs/release-checklist.md`, `docs/branch-and-release.md`) sharing a run of words the paste ratchet counts, and if so is the fix a reword or a baseline row? | **the work** — phase 2, which writes both texts, is the first to know; the ratchet's rule is to share no run, and a baseline row is for copies the tree already held, not for new ones | **reword** — the two say one thing in two shapes, the bullet as the rule and the box as what to type · **baseline row** — refused by the ratchet's own docstring for a run this work introduces | reword; the phase record says what was shared and how it was split | ⬜ |

**Why Q1 survived the judging.** Everything else in #858 was a fact about a
page or a file and was read or measured. Q1 is an act on an account only the
owner holds, with a consequence the owner carries (a listing withdrawn is a
listing nobody can install until it is published again). The two answers do
not change what is built, which is why it does not block: the box carries the
default with its date, and the move is what changes it.

**Nothing here blocks the build.** No row has to be answered before phase 1
starts, and no row changes what any phase builds.
