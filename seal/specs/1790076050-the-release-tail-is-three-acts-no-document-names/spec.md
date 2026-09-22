# Feature Specification: the release tail is three acts no document names

<!-- seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/spec.md
     WHAT this work delivers and how we'll know. The policy documents in
     docs/ outrank this file; cite them, don't restate. -->

Three tickets, one branch, because all three are the same defect at three
coordinates: **an act the release performs, assigned to whoever is at the
keyboard, written into no document and read by no machine.** #386 is the
release note, #417 is the plugin directory, #450 is the `size: now` label the
tracker has never had.

The release this branch ships in runs the tail it specifies, so every step
below is performed by the run that merges it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* — verification through an automated workflow is the first goal, and between two designs that catch the same thing the one that stops to ask a person is the more expensive | Decides the checklist/workflow line for all three acts. A step written into a checklist is a step a person can skip, which is #386's entire measurement: three consecutive releases skipped one |
| `CONTRIBUTING.md` §*What a change to a gate must carry* — a test seen red, a stated failure direction, a prompt budget | Two of the three deliverables are CI steps, so each owes all three. The prompt budget for every one of them is **zero**: each runs on GitHub after a push, with nobody at a keyboard |
| `docs/branch-and-release.md` §*Cutting a release* — two things carry the version, and the tag is still the maintainer's to push because nothing in CI can do it for you | The tag stays a person's act. It is also the last act of the release, which is what makes it the trigger the release note can hang from |
| `docs/branch-and-release.md` §*Which button, for each direction* and §*What breaks when the last row is squashed* | Enumerates who points at a release-branch commit by SHA. #417 adds a reader from outside the repository, and that section is where the enumeration lives |
| `docs/release-checklist.md` §5 — the release pull request's title is `release: X.Y.Z — <the symptoms the release answers>` | The one written-down source for a release note's title. Measured below: it is **not** where the existing release names came from |
| `docs/issues-and-milestones.md` §*A label answers what it is about* | Specifies `size: now` in full — two states, the prefix argument, what its absence means. The doctrine is not rewritten; what is missing is the object it describes and the two sentences it never carried |
| `CLAUDE.md` §*A change writes fragments, never the shared file* | The changelog entry is `seal/specs/<work-item-id>/changelog.md` and any ledger row is `seal/ledger/<work-item-id>.md`. `CHANGELOG.md` and `seal/ledger.md` are not appended to |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | The plugin directory's repositories are real GitHub organisations. Their URLs belong in the script that reads them, not in prose; `tests/test_no_real_identifiers.py`'s `ALLOWED_DOMAINS` allows `github.com` and every subdomain of it, and is silent on the raw-content host GitHub serves file bodies from, so a raw URL extends the allowlist consciously or the script builds it from an allowed host. **This row's own wording was the first thing the sweep refused** — it named that host in prose, which is exactly what it is telling the reader not to do; the build reworded it and `overview.md` records both sides |

## Scope

### In

1. **A GitHub Release is published by a workflow, not by whoever remembers**
   (#386). Triggered by the tag push, which is the release's last manual act,
   from the `CHANGELOG.md` section that is already gathered, reviewed and on
   `main` by then.
2. **`docs/release-checklist.md` §6 stops ending at the tag** (#386, #417).
   Two boxes after the tag: the release note exists, and the plugin directory
   carries the version. Each box names the command that answers it.
3. **A command that answers the directory box** (#417). It reads both public
   directory files, says whether this plugin is listed, which commit each
   pins, and whether that commit is reachable from `main`. It reports; it
   never fails a release on somebody else's sync schedule.
4. **Two sentences `docs/branch-and-release.md` does not carry** (#417): the
   plugin's name is fixed once anybody has installed it by slug, and a commit
   pinned by an outside directory is a third reader of the merge-method rule,
   beside the rider stamps and the round records.
5. **`size: now` exists on the tracker, created by a workflow** (#450), and
   comes off an issue at the moment the release that carried it closes that
   issue — the moment a workflow already acts on.
6. **`docs/issues-and-milestones.md` gains the three sentences #450 says are
   missing**: where the sizing judgment is made, what removes a spent label,
   and that no backlog sweep is owed.
7. The fragments: `seal/specs/<work-item-id>/changelog.md`, and a
   `seal/ledger/<work-item-id>.md` row for anything this work verifies by
   opening code.

### Out

- **A check that refuses a release while the previous tag has no release
  note.** #386's own shape 3. It reads GitHub rather than the tree and fires
  one release too late by construction; the workflow in scope item 1 removes
  the condition it would report.
- **A gate keyed to the plugin directory's state.** #417 rejects it with a
  measurement — one of the two directory repositories went 22 days without a
  commit — and a red nobody can act on is the interruption the first goal is
  against.
- **Automating the directory submission.** The form is a person's act, once.
- **A `marketplace.json` of this repository's own.** Self-hosting is a
  different subject.
- **A second sizing level or a scale, and a gate that fails a pull request
  for a missing `size: now`.** `docs/issues-and-milestones.md` refuses the
  first and #450 refuses the second: sizing is a judgment, and a gate over it
  refuses honest work for an absent opinion.
- **A backlog sweep applying `size: now` to the open issues.** Grounds in
  §*Judgments this frame made* below.
- **Rewriting `docs/issues-and-milestones.md` §*A label answers what it is
  about*.** One sentence in it is reworded, for a reason stated below; the
  doctrine and the prefix argument stand.
- **Backfilling release notes for tags that have none.** #386 records that
  all twenty-three were backfilled on 2026-09-13. Nothing is owed here.
- **Touching `hooks/version-check.py` or what the tag means.** The tag is
  still what tells an installed session a version exists, and this work adds
  a second consumer of the tag without changing the first.
- **A new arm in `skills/verify/scripts/broad_gate.py`.** Nothing here adds a
  step to `hygiene.yml`'s `release` job, which is the only job
  `tests/test_the_gate_names_every_step_ci_runs.py` partitions.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The release note publishes itself | Given `main` carries a gathered `## X.Y.Z` section and the maintainer pushes `vX.Y.Z` · When the tag-triggered workflow runs · Then a GitHub Release named `X.Y.Z — <the symptoms>` exists at that tag with that section as its body | a case over the script with a fixture changelog and a stubbed `gh`; the live proof is the run that ships this branch |
| A2 | An existing note is never republished | Given a release already exists at `vX.Y.Z` · When the workflow runs again — a re-pushed tag, a re-run job · Then it prints that the release exists, writes nothing, and exits 0 | a case; #386 states this direction explicitly |
| A3 | A missing note goes red | Given `CHANGELOG.md` carries no `## X.Y.Z` section for the tag being pushed · When the workflow runs · Then the job fails and the message names the tag and the file it looked in | a case, seen red first (`CONTRIBUTING.md` §*What a change to a gate must carry*) |
| A4 | The title is the one a document specifies | Given the tagged commit's message carries the `release: X.Y.Z — <symptoms>` line `docs/release-checklist.md` §5 prescribes · When the note is created · Then the title is `X.Y.Z — <symptoms>`; and where no such line is readable, the title is the tag name and the job log says which it used | two cases, one per branch |
| A5 | §6 stops at neither the tag nor a sentence | Given a reader working down `docs/release-checklist.md` · When they pass the tag · Then two boxes follow, each carrying the command that answers it | a case asserting both boxes and both commands are in §6 |
| A6 | The directory report answers the box | Given the two public directory files · When the command runs · Then it says, per directory, whether this plugin is listed, which commit is pinned, and whether that commit is an ancestor of `main` | a case over captured fixture JSON in both shapes — listed and absent |
| A7 | The directory's state never fails a release | Given the plugin is absent from both directories, or a directory cannot be fetched · When the command runs · Then it reports and exits 0 | two cases. The only non-zero exit is a malformed argument, which is the author's |
| A8 | `docs/branch-and-release.md` names the third reader | Given §*What breaks when the last row is squashed*, which enumerates who points at those commits by SHA · When a reader looks for who else · Then an outside directory's pinned commit is in the enumeration, and the fixed-name sentence is beside it | a case over both sentences |
| A9 | The label exists without anybody remembering | Given a tracker missing a label this repository's documents specify · When the release reaches `main` · Then the reconcile step creates it with the description the document's own sentence gives, and says so | a case; the shape is `label_merged_on_release_branch.py`'s, which already creates `merged: X.Y.Z` this way |
| A10 | Reconciling is idempotent | Given every declared label already exists · When the step runs · Then it creates nothing and exits 0 | a case |
| A11 | A spent label comes off with the issue | Given an issue carrying `size: now` that a shipped pull request claimed · When the release reaches `main` and the closing workflow closes it · Then `size: now` is removed from that issue in the same act | a case; the issue closes either way, so a failed label write never leaves an issue open |
| A12 | The document says when the judgment is made and what removes it | Given a reader who wants to apply the label · When they read §*A label answers what it is about* · Then it says the judgment is made at filing and again when an issue moves milestone, that a spent label is removed by the workflow that closes the issue, and that no sweep of the standing backlog is owed | a case; `tests/test_a_release_is_sized_by_a_criterion.py` already pins three sentences of this section and one of them is reworded — see below |
| A13 | Nothing schedules from the label, and that stays readable | Given the reworded sentence · When a reader meets a stale `size: now` · Then they still learn that no automation schedules from it, and they additionally learn which workflow removes a spent one | the existing case, with its literal moved in the same commit (`agent-contract` §14) |

## Data & interfaces

- **New workflow**, `.github/workflows/publish-release.yml`: `on: push: tags:
  ['v*']`, `permissions: contents: write` and nothing else, one job, one step
  running the script below. It is not part of `hygiene.yml`'s `release` job,
  so `tests/test_the_gate_names_every_step_ci_runs.py`'s partition is
  untouched.
- **New script**, `.github/scripts/publish_release_note.py`: reads the tag
  from the environment the way its siblings read `BEFORE`/`AFTER`/`REPO`,
  parses `CHANGELOG.md` for the `## X.Y.Z — <date>` section, reads the tagged
  commit's message for the title line, and calls `gh release create` — or
  reports and exits 0 where the release already exists.
- **New script**, `.github/scripts/plugin_directory_check.py`: reads the two
  public directory files over HTTPS, matches this plugin's name from
  `.claude-plugin/plugin.json` rather than a literal, and prints one line per
  directory. The entry shape it reads is `source.url` plus `source.sha`,
  measured today over 310 official entries and 2,282 community ones.
- **New script**, `.github/scripts/tracker_labels.py`: holds the labels this
  repository's documents specify — name, colour, description, and the
  document that specifies each — with `--check` reporting and `--apply`
  creating what is missing. `size: now` is its first and, today, only row.
- **Changed**, `.github/workflows/close-issues-on-release.yml`: one step
  calling `tracker_labels.py --apply`. It already declares `issues: write`
  and already fires when `main` moves, so no permission and no trigger
  changes.
- **Changed**, `.github/scripts/close_issues_on_release.py#main`: the loop
  that closes an issue also removes `size: now` from it. It already knows
  exactly which issues shipped, which is the fact a person would otherwise
  have to reconstruct.
- No schema, no endpoint, no payload. Every new reader is a public file or
  the tracker API `gh` already reaches.

## Judgments this frame made, and what they rest on

These were open in the tickets and the tree answered them. They are recorded
here so nobody reopens them, and each can be overturned by opening what is
cited.

1. **#386 takes shape 2 — a workflow, not a checklist line.** The ticket's
   own argument plus the first goal. Shape 1 is the design that already
   failed: §6 has had the tag step for the repository's whole life and the
   tag gets done because `hooks/version-check.py` reads it, while the note
   has no reader in the tree at all.
2. **The trigger is the tag push, not the push to `main`.** The existing
   `close-issues-on-release.yml` fires when `main` moves, and at that moment
   the tag does not exist yet — `docs/release-checklist.md` §6 pushes it
   afterwards. A release note must name a tag, so hanging it from the `main`
   push would make the workflow create the tag, which
   `docs/branch-and-release.md` says is the maintainer's act.
3. **The title comes from the tagged commit's `release: X.Y.Z — <symptoms>`
   line, and #386's sentence about it is wrong.** The ticket says the title
   is "the release pull request's own, which a workflow can read from the
   merge commit's subject". Measured on the most recent release: the merge
   commit's **subject** is `Merge pull request #N from <owner>/release/vX.Y.Z`
   and the release title line is the **body's** second line. Measured
   further, the twenty-three hand-written release names are not the pull
   request titles either — the latest release's name and its pull request's
   title are two different sentences about two different things. So what is
   being automated is the convention `docs/release-checklist.md` §5 writes
   down, and not the one the owner typed by hand, because only the first is
   reproducible by anything.
4. **The changelog section is the body, and the changelog heading is not the
   title.** `## X.Y.Z — <date>` carries a date and no prose, so a title taken
   from it would drop the symptom line every existing release carries.
5. **The plugin is listed in neither directory as of today.** #417 measured
   absence on 2026-09-16 after the submission passed review; re-measured
   2026-09-22 against both files, still absent, and official has grown from
   296 entries to 310 in between. So the first answer the new checklist box
   gives is *not listed*, and the box has to say what to do in that state as
   well as in the stale-pin state.
6. **#417's open question does not block anything.** How an update reaches a
   listed plugin is not readable from any public file and is a person's to
   find out. It does not change what gets built: the box compares the pinned
   commit against the released one and says to resubmit through the portal
   when it is stale, which is the right instruction under either answer. It
   is a row in `questions.md` for the record, not a wait.
7. **#450's repair is to move the act to a machine, not to a ticket.** The
   ticket names the class — *an act assigned to a person has no queue this
   repository can read* — and proposes giving it a home on the tracker. A
   tracker row is another thing a person has to act on. The precedent one
   file over is better: `label_merged_on_release_branch.py` creates
   `merged: X.Y.Z` on the tracker from a workflow, with the `issues: write`
   the same job already holds. A label a document specifies is the same kind
   of object as a label a release needs.
8. **No backlog sweep.** `docs/issues-and-milestones.md`'s own argument for
   the label is that the sizing judgment is cheap at filing and expensive in
   a batch. A sweep of the standing backlog is the batch, performed once, by
   the party the label exists to spare. The document says so instead.
9. **A spent label is removed by the workflow that closes the issue.** That
   is the moment the document already names, and
   `close_issues_on_release.py#main` is already standing at it holding the
   list of issues that shipped.
10. **One pinned sentence is reworded, and its case moves with it.**
    `docs/issues-and-milestones.md` says **Nothing reads this label** and
    `tests/test_a_release_is_sized_by_a_criterion.py#test_the_label_is_two_states_and_nothing_reads_it` — NAME NOT IN TREE
    (review round 1's finding 4 renamed it to
    `test_the_label_is_two_states_and_nothing_schedules_from_it`, because a
    case named for the sentence it had stopped asserting is the coordinate a
    reader opens to check the claim)
    pins that literal. After item 9 something does read it — to remove a
    spent one. The sentence's purpose, stated in the case's own docstring, is
    that a reader must not think anything *schedules* from the label, and
    that stays true. So the sentence becomes a statement that nothing
    schedules from it, naming the one workflow that removes a spent one, and
    the case's literal moves in the same commit. `agent-contract` §14: a
    change to what a person reads documents it and pins it.
11. **The label's colour and description are not a question.** The
    description is the document's own sentence, the way
    `label_merged_on_release_branch.py#label_description` derives one; the
    colour joins the topic labels' family. Nothing turns on either, so the
    assumption is written here and the work continues.
12. **A failing hygiene step for a missing label was rejected.** It would be
    red on this very branch — no party in this run may create a label, since
    `skills/agent-contract/SKILL.md` §6 withholds posting from every agent —
    and it would have to be added to `broad_gate.py`'s partition as well.
    A reconcile step that performs the act costs neither.

## Open questions → questions.md

One row, and it is a person's. It does not block: the default continues and
is what ships.

Framed 2026-09-22 by framer, before the build.
