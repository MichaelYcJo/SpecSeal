# 1791384161-the-plugin-directory-check-reads-the-directory — overview

📋 implement applied
· spec:     `spec.md` (Vocabulary, Grounding, Scope, A1–A11, Data & interfaces), `plan.md` (phases 1–3, Technical context), `questions.md` Q1–Q3; `docs/branch-and-release.md` §*Cutting a release* and §*Work accumulates on a release branch*; `docs/release-checklist.md` §*6. After the merge*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `CONTRIBUTING.md` §*House rules* through `tests/test_no_real_identifiers.py`
· evidence: `seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md` — four `Re-read ·` rows: S9 (`seal/releases/0.11.1.md`), P1c (`0.15.0.md`), W4 (`0.18.0.md`), O2 (`0.18.1.md`); no row for the command (`spec.md` §*Data & interfaces*)
· verified: executed — the touched modules through `bin/test`, 19 mutations through `bin/mutation-check`, the live run (exit 0), `evidence-check`, the three documentation pages fetched 2026-10-08; read — A9's vocabulary over the five texts; unverified — the rows below, and the full suite (the sealer's)

## Why this work exists

The release checklist's last command told the releaser the plugin was *not listed* and to submit it, about a directory it never read; it now says what the two marketplace files hold, says the directory was not read, and names the page a person opens.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The existing cases of the command's test module | A2: *the existing cases of `tests/test_the_plugin_directory_answers_the_box.py`, green without edit*. §*Data & interfaces*: an entry's line reads *an entry, pinning <sha12> of <url>*. The cases asserted `"listed" in head`, which the specified line cannot satisfy | the output contract; two assertions now read `"an entry"` / `"not an entry"`, and every fact A2 names is asserted as before | §*Vocabulary* and A9: *listed* is the directory's word, and a marketplace file's line saying it is the guess this work removes (`phases/phase-1.md`) |
| The frame's own files and the identifier sweep | §*Grounding*: the mail domain *does not enter*; `spec.md` and `questions.md` spelled that domain out three times, so the sweep stayed red after `claude.ai` entered | the three places said *the company's mail domain* after the build, and say *Anthropic's mail domain* since round 1's ⬜ 7; meaning unchanged | `tests/test_no_real_identifiers.py`, red at 0fb6fd0c before any edit |
| Which ledger families this work re-reads | `plan.md` phase 3 and `spec.md` §*Grounding* name S9, P1c and W4 | four: O2 (`seal/releases/0.18.1.md:368`) anchors `### Work accumulates on a release branch`, whose third-reader paragraph phase 2 changed | `evidence-check` named it DRIFTED after c4990707; its claim (the merge-method home) was read and holds |
| The third-reader sentence | §*Scope* item 3 and A8: the directory is *a fourth reader of a release-branch commit* | the sentence says the directory holds a scanned commit of the branch a submission tracks, and does not call it a release branch's | the docs say *the tracked branch*; a submission tracking `main` is not reached by a squash of a release branch (`phases/phase-2.md`) |
| Where the product host is allowed (round 1, 🟡 2) | A10: *`ALLOWED_DOMAINS` … carries `claude.ai`* | the host is in `ALLOWED_UNDER_PATHS` instead, allowed bare or under `/directory` only; a share link, an address and a subdomain on it are refused | a host-wide entry admitted per-person links; the house rule's purpose outranks A10's letter, and A10's *the sweep's can-fail case still refuses a planted domain* holds with three more plants |
| What a portal listing does with a new version (round 1, 🟡 1) | §*Scope* items 1–2, A5 and §*Data & interfaces*: a portal listing takes new versions *on its own*. §*Vocabulary*'s first fact, which the build now matches: *nothing is resubmitted … A new version that passes is published according to the plugin's publish setting* | the command, its docstring, the box and the changelog say the version is picked up without a resubmission and goes live by the publish setting, which by default waits for somebody to select Publish | `claude.com/docs/plugins/submit` §*Publish a passing version*, fetched 2026-10-08 |
| The command block's comment in §6 | §*Data & interfaces*' list of removals does not name it | `# what the directory has` became `# what the marketplace files hold` | §12: the class is every coordinate that states the inference |

## Not verified

| Item | Who must answer |
|---|---|
| Whether SpecSeal shows up in the directory today — a search for *SpecSeal* inside Claude (`questions.md` Q2). The box says this search is what answers it; no script can run it | the repository owner, with a Claude account in a browser |
| That the Console page the command prints, `platform.claude.com/plugins/submissions`, is the page the owner's Console listing appears on. The address is the docs' own link (fetched 2026-10-08); the page is behind a login nobody here has | the repository owner |

## Not done

The move of SpecSeal's Console listing to the developer portal: `questions.md` Q1 was answered *leave* by the owner on 2026-10-08, and the box records that listing as a Console listing with its date. A move changes that one dated sentence.

## Fed back into the spec

none — the divergences above are recorded here and in the phase records rather than edited into `spec.md`, except the three respellings of the mail domain, which change no clause.
