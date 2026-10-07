# 1791384161-the-plugin-directory-check-reads-the-directory — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c4990707 |
| Ran by | unknown — the spawn prompt named the agent, `smith`, and not the model |

## What this phase was asked

`plan.md` phase 2: the box and the two policy sentences, with their pins. The
last box of `docs/release-checklist.md` §6 per `spec.md` §*Scope* item 2 —
*reports and never fails* kept; what the command reads, and that the directory
is readable from nowhere a script can reach; the portal's Submissions page and
the Console page, and which kind of listing each answers for; a portal listing
updates on its own; the dated Console sentence; the docs page for the move; no
*resubmit*; the open-question sentence gone. The release-tail bullet in
`docs/branch-and-release.md` per item 3, its `Enforced by:` line naming the new
A7 case. The third-reader paragraph names a marketplace file, keeps its
measurement and pinned phrases, and adds the directory as a reader of a
scanned commit. The box case stops pinning *Not listed* and *pinning an older
commit* and pins A5 and A6; one new case on the bullet for A7. Each pin seen
red. The box and the bullet share no run the paste ratchet counts (Q3).

## What this phase found

**Q3 answered by measurement: neither a reword nor a baseline row.** The box
and the bullet were written apart, the bullet as the rule and the box as what
to do at the release, and after c4990707 the pair shares **0** runs of 15
words (`WINDOW`), measured with the ratchet's own `shared_counts` over
`tree()`. `tests/test_no_passage_is_pasted_into_a_second_file.py` is green.

**The bullet's lead had to change, not only its body.** The bullet opened *The
plugin directory is read by a command that never fails a release*, which is
the claim this work withdraws. It now opens *The marketplace files are read by
a command that never fails a release, and the plugin directory by a person*,
and the new A7 case finds the bullet by that lead.

**The command block's comment was a fourth carrier of the guess.** §6's
command block annotated the command `# what the directory has`; it now reads
`# what the marketplace files hold`. `spec.md` §*Data & interfaces* did not
list it among the readers it removes; §12's class is every coordinate that
states the inference, so it went with the box.

**The third-reader sentence states the docs and stops there.** `spec.md` §*Scope*
item 3 and A8 call the directory *a fourth reader of a release-branch
commit*. What the docs say is that a portal submission is served from a
scanned commit of the branch it tracks; whether that is a release branch
depends on which branch a submission tracks, and a submission tracking `main`
is untouched by a squash of a release branch, because `main` takes a merge
commit. The sentence says the directory *holds a commit too* and names the
tracked branch, which is true for any branch; it does not call the commit a
release branch's. A8 leaves this sentence unpinned on purpose (*a fact from the
docs, not a rule*), so no pin moved for it.

**One pin is satisfied twice.** `"Console page" in box` is met by *A Console
listing is answered on the Console page* and again by the kind sentence's
*reading of the Console page*, so removing either alone leaves it green. The
kind sentence is pinned on its own by A6's case, and a box that dropped both
goes red; no break was run for the single removal.

**Seen red against the documents at the frame (§15), executed.** With the new
pins over the documents as they stood at 0fb6fd0c: 3 failed, 6 passed.

| Case | Said |
|---|---|
| `test_the_directory_box_says_it_never_fails_a_release` | *the box does not say what the command reads* |
| `test_the_directory_box_records_which_kind_of_listing_it_is_with_a_date` | *the box does not say which kind of listing SpecSeal's is* |
| `test_the_directory_check_reads_the_marketplace_files_and_not_the_directory` | *the release-tail statement has no bullet for the check* |

**Each later assertion seen red by a break, executed through
`bin/mutation-check`** at c4990707's text, over
`tests/test_the_release_tail_does_not_end_at_the_tag.py -k directory` with
`-p no:xdist`. Every one printed `red`:

| # | File | Break | Case that went red |
|---|---|---|---|
| D1 | checklist | *marketplace files on GitHub* loses *marketplace* | the A5 box case |
| D2 | checklist | *from nowhere a script can reach* → *from nowhere public* | the A5 box case |
| D3 | checklist | *Submissions page* → *Submissions view* | the A5 box case |
| D5 | checklist | *tracked branch on its own* loses *on its own* | the A5 box case |
| D6 | checklist | *until then.* → *until then, or resubmit.* | the A5 box case |
| D7 | checklist | the kind sentence loses *on 2026-10-07* | the A6 kind case |
| D8 | checklist | *reading of* → *view of* | the A6 kind case |
| D9 | checklist | *no new version until* → *a new version only after* | the A6 kind case |
| D10 | checklist | the kind sentence loses the docs page's path | the A6 kind case |
| D11 | checklist | *A portal listing* → *A Portal listing* | the A5 box case |
| B1 | policy | *reads the two marketplace files* → *reads two files* | the A7 bullet case |
| B2 | policy | *is not among its answers* → *is among its answers* | the A7 bullet case |

**A9, read.** `grep -n directory` over the command, its test module, the box
and the two policy sentences: every hit names the catalog people browse
inside Claude, and the GitHub files are *marketplace files* throughout.
`docs/branch-and-release.md`'s fixed-name paragraph (*a directory listing is
keyed on the same name*) is outside the two sentences and was left as it is.

**Verified by, executed.** `plan.md` names `uv run --frozen pytest`; the seven
modules it lists ran through `bin/test -q -p no:cacheprovider` at c4990707:
exit 0, 143 passed, 7 skipped. `uvx ruff check` and `uvx ruff format --check`
over the changed test module: exit 0 each.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the box's *Not listed means submitting it through the form the command names* and *resubmit through the same form* | none — `spec.md` §*Vocabulary*: on the portal nothing is resubmitted, and a Console listing takes no new version; the box now names the page for each kind |
| the box's *Whether an update reaches a listed plugin on its own … is an open question* | the box's portal and Console sentences, from `claude.com/docs/directory/publish` |
| the bullet's *says, per directory, whether the plugin is listed* and *Submitting or resubmitting is a person's act* | the rewritten bullet: the marketplace files as input, the directory's state *not among its answers*, *moving a Console listing to the developer portal, is a person's act* |
| the command block's comment `# what the directory has` | `# what the marketplace files hold` |
| the box case's pins on *Not listed* and *pinning an older commit* | `test_the_directory_box_says_it_never_fails_a_release` (A5) and `test_the_directory_box_records_which_kind_of_listing_it_is_with_a_date` (A6) |
