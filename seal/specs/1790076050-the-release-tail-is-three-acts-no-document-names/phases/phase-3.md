# 1790076050-the-release-tail-is-three-acts-no-document-names — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `c8983b14` |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The directory box has an answer. `.github/scripts/plugin_directory_check.py`:
both public files, listed or not, the pinned commit, whether it is an ancestor
of `main`. Reports and exits 0 on absence and on a failed fetch. Verified by a
case over captured fixture JSON in both shapes — A6, A7 — with the fixtures
captured rather than fetched at test time, so the suite does not reach the
network.

**This phase was built before phase 2**, which `plan.md`'s phase 2 row
sanctions in as many words: the box's command exists from phase 3, "so phase 2
lands before it only if the box names the command it is about to gain;
otherwise run 3 before 2 and say so". This is the saying so. Building 3 first
lets phase 2's case assert the box names a command the tree actually has,
rather than a string somebody is about to make true.

## What this phase found

### The path both the ticket and `spec.md` give is 404

#417 says "the directory's `marketplace.json` is a public file in both
repositories" and `spec.md` §*Data & interfaces* inherits it. **Executed
2026-09-22**: `repos/<owner>/<repo>/contents/marketplace.json` is 404 in both;
the file is at `.claude-plugin/marketplace.json`. A reader at the ticket's path
would have reported *could not be read* at every release forever — which is A7
working perfectly and A6 answering nothing, the quietest way for this to be
useless. `test_it_reads_the_path_the_directories_actually_have` pins the
corrected path.

### An entry's `source` has four shapes and two of them pin nothing

`spec.md` states the shape as "`source.url` plus `source.sha`, measured today
over 310 official entries and 2,282 community ones". The counts reproduce
exactly. The shape does not hold for all of them — **executed 2026-09-22**:

| Shape | official / 310 | community / 2,282 |
|---|---|---|
| object with `source`, `url`, `sha` | 157 | 1,871 |
| the same plus `path` and `ref` | 96 | 397 |
| the same plus `path` | 5 | 6 |
| **a plain string** (`./plugins/<name>`), no url, no sha | **52** | **5** |
| object with `url` and `ref` and **no `sha`** | 0 | **3** |

So `entry["source"]["sha"]` raises on 57 entries today, in a file this
repository does not own and cannot hold steady. `pinned()` tolerates all four
and the three no-commit shapes are a parametrised case.

**The same measurement, rolled up the way `docs/branch-and-release.md` cites
it** — added in round 1's fix pass, because finding 2 was that the document
carried figures no record supported. Re-measured 2026-09-22, same files:

| Of official's 310 | count |
|---|---|
| `source` is an object, and every one carries a `url` | **258** |
| of those, carrying a `sha` | **258** — all of them |
| of those, carrying a `ref` | **96** |
| of those 96 refs, naming `main` or `master` | **91** |
| `source` is a plain string, pinning nothing | **52** |

The command, so the figures have a way to be re-derived rather than trusted:

```bash
gh api repos/<owner>/<directory>/contents/.claude-plugin/marketplace.json \
  -H "Accept: application/vnd.github.raw" |
python3 -c 'import json,sys
p=json.load(sys.stdin)["plugins"]
o=[e for e in p if isinstance(e.get("source"),dict)]
r=[e["source"]["ref"] for e in o if e["source"].get("ref")]
print(len(p), len(o), sum("url" in e["source"] for e in o),
      sum(bool(e["source"].get("sha")) for e in o), len(r),
      sum(x in ("main","master") for x in r))'
```

**What the document no longer claims, and why.** The sentence used to end
*exactly one of those 88 names a tag*. A `ref` in this file is a string;
nothing in the file says whether it is a tag or a branch, and settling it
would mean asking each of 96 source repositories. Of the five refs that are
not `main` or `master`, two carry a version (`v1.5.5`, `greptile--v1.2.3`) and
three are an ordinary branch name — so even a guess does not land on one. The
claim was dropped rather than re-derived, because it is not a fact this file
carries.

**Where the wrong figures came from**, since the class matters more than the
instance: 244, 88 and *exactly one names a tag* are #417's, measured
2026-09-16 over **296** entries. They were true of that file on that day and
were written into a sentence that says 310, beside this phase's own
measurement of the same file two weeks later. Two correct measurements of
different populations, joined into one sentence that is true of neither —
which is why the rolled-up figures now live here with the command beside them,
and the document cites this record instead of carrying loose numbers.

### It reads through `api.github.com`, and the allowlist is untouched

`plan.md` constraint 3 offers two ways past the raw-content host: extend
`ALLOWED_DOMAINS` consciously, or build the URL from an allowed host.
**Neither a raw host nor an allowlist change is needed.** The documented API
serves a public file's body at `repos/<owner>/<repo>/contents/<path>` with
`Accept: application/vnd.github.raw`, on `api.github.com` — a subdomain of
`github.com`, which `test_no_real_identifiers.py` already allows through its
`d.endswith("." + a)` arm. Spending the repository's own allowlist to read a
file the allowed host already serves would have bought nothing.

### The constraint refused its own wording, and so did the grounding row

Running `tests/test_no_real_identifiers.py` after phase 3 reported two lines,
**both of them the framer's**, neither of them code:

```
seal/specs/1790076050-…/plan.md:59 <the raw-content host>
seal/specs/1790076050-…/spec.md:27 <the raw-content host>
```

(The host's own name is elided here for the same reason the two sentences
were reworded: the sweep reads this file too, so quoting its output verbatim
reproduces the violation inside the record of the repair.)

Each sentence makes its point by spelling the host it is telling the reader
not to spell. The base does not carry the domain; `git log -S` names the frame
commit `99168a43` as where both entered, so this is the branch's red and the
branch's to clear.

The repair is the reworded sentence, not an extended allowlist: the allowlist
exists for a host something reads, and nothing here reads that one. Both
sentences keep every fact — which host is allowed, which is not, and what to
do if a raw one were ever needed — and say which host they mean instead of
writing it out. `overview.md` carries both sides quoted, as a divergence from
the frame.

### A third ancestry answer, which the acceptance rows do not have

A6 asks "whether that commit is an ancestor of `main`", which reads as two
values. There is a third: **this clone may not have the commit at all.** A
fresh or unfetched checkout answers *no* to `merge-base --is-ancestor` for
every sha, so folding the two together tells a reader to resubmit to the
portal because they had not run `git fetch`. `is_ancestor` returns `None` for
that and for a `ref` that does not resolve, and the report says *unknown here*
with the fetch to run.

### Executed once against the live directories

```
plugin 'specseal', against release/v0.13.1
official (anthropics/claude-plugins-official): 'specseal' is not listed, in 310 entries.
community (anthropics/claude-plugins-community): 'specseal' is not listed, in 2282 entries.
exit=0
```

Which confirms `spec.md` §*Judgments* 5 on the day: absent from both, and the
first answer the new box gives is *not listed*. Community's last push is
2026-08-25 — twenty-eight days, against the twenty-two #417 measured, which
strengthens rather than weakens the argument against gating on it.

### How each case was shown red (§15)

Eleven mutations, each removing one behaviour, the module re-run, the file
restored from a byte copy kept outside the tree. `13 passed` before and after.

| Mutation | Case that went red |
|---|---|
| the pinned commit dropped from the `listed,` line | `test_a_listed_entry_reports_its_pinned_commit` — **after the case was repaired; see below** |
| `not listed` stops saying over how many entries | `test_an_absent_entry_says_so_and_says_how_many_it_read` |
| the reader assumes `source` is an object with a `sha` | all three params of `test_an_entry_that_pins_no_commit_is_read_rather_than_raised_on` |
| a commit the clone lacks returns `False` instead of `None` | `test_a_commit_this_clone_does_not_have_is_not_called_unreachable` |
| the failed-fetch line stops saying it is not a reason to stop | `test_a_failed_fetch_is_a_report` |
| an unreadable payload raises instead of reporting | `test_a_payload_that_is_not_a_directory_is_a_report` |
| `main` returns 1 | both params of `test_the_run_exits_zero_on_absence_and_on_a_failed_fetch` |
| the run stops saying what it cannot answer | both params of the same case |
| the plugin name becomes a literal | `test_the_name_comes_from_the_manifest_rather_than_a_literal` |
| `MANIFEST` reverts to the root path the ticket names | `test_it_reads_the_path_the_directories_actually_have` |

**One mutation found nothing, which is the whole reason §15 exists.** Dropping
the pinned commit from the `listed,` line left
`test_a_listed_entry_reports_its_pinned_commit` **green**: the commit is
printed twice, once there and once inside the ancestry sentence below it, and
the case searched the whole report. It was a case that passed against the exact
defect it was written for. It now asserts on the first line alone — which is
the line the box is read for, since the ancestry sentence is absent whenever
the clone cannot answer — and the same mutation reds it.

### What a gate change owes (`CONTRIBUTING.md`)

This is not a gate, and saying so is the deliverable. **Failure direction:
none.** The only non-zero exit is argparse's 2 on a malformed argument, which
is the author's mistake rather than the directories'. **Prompt budget: zero** —
it is a command a person types at a checklist box, and it asks nothing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the literal raw-content host from `spec.md`'s grounding row and `plan.md`'s constraint 3 | the same two sentences, which now name the host by description; the fact they carry is unchanged and `overview.md` records both sides |
