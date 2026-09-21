# 1789919879-the-outside-contributor-has-no-procedure — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 282db265 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`README.md` §*Contributing* and `README.ko.md` §*기여* point at the procedure,
in both editions.

## What this phase found

**Pointing at it is not enough, and the section was already proof of that.**
Both editions carried the gate bar and a bare *see `CONTRIBUTING.md`*, and
that is the state a contributor met before #443 — a link is a second hop, and
the fact that would have saved the contribution never appeared on either page.
So each edition now states the base-branch fact inline, ahead of the gate bar,
and cites the section for the rest. Same judgment as `plan.md`'s rejected
alternative *a refusal that only cites `CONTRIBUTING.md`*, one surface over.

**The exemption list is summarised rather than linked**, because it is the
half of the procedure nobody can infer. A reader who never opens
`CONTRIBUTING.md` should still come away knowing this repository's own
workflow is not theirs.

**The Korean edition is written as Korean, not as a translation.** The
`writing-style` skill's §*영어를 옮길 때는 구조를 버리고 뜻만 가져온다* is the
rule; concretely, the English sentence *GitHub's default base is the wrong one*
has an inanimate subject that reads badly in Korean, so the Korean says what a
person meets instead. Terms match the vocabulary `README.ko.md` already uses —
근거 대조표 for the ledger, 작업 항목 for a work item, 라운드 기록 for a round
record — rather than new coinages for this section.

**The heading in the citation stays English in both editions.** `README.ko.md`
cites §*Opening a pull request* untranslated, because it is the name of a
heading a reader has to find in an English file. A translated section name is
a name that matches nothing on the page it sends them to.

**Executed:**

| Command | Result |
|---|---|
| `bin/test tests/test_docs_line_wrap.py -q` | 24 passed — both editions inside 88 display columns, Hangul counted double |
| `bin/test tests/test_one_word_one_meaning.py -q` | 18 passed |
| `bin/test tests/test_no_document_names_the_old_roots.py -q` | 16 passed |
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q` | 33 passed, 7 skipped |
| `git diff --name-only` before committing | names `README.md` and `README.ko.md` — A7, and the hygiene workflow's both-READMEs warning stays silent |

The last three are not this phase's own module. They read documents
repository-wide, and this phase adds prose to two documents, which is the
phase-boundary rule in `agent-contract` §2: the module you touched and the
ones it touches. The full suite is not run here and is the sealer's.

**One instruction declined, recorded here as well as in the hand-back.** The
session's auto-mode reminder asked for file changes to be made through Bash
(`sed`, heredocs) rather than the `Edit` tool. `agent-contract` §9 requires
the `Edit` tool wherever the environment allows it, for two reasons that both
apply here: an edit must be able to fail, and a Bash command line is something
the commit gate reads. Every edit in all five phases went through `Edit` or
`Write`; the two places a script edited files — the mutation loops and the
commit-cell backfill — assert their substitution matched, per the same section.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The bare *See [CONTRIBUTING.md](./CONTRIBUTING.md).* sentence closing §*Contributing*, and its Korean twin | Nothing: both editions still cite the file, now naming the section inside it. The citation was not deleted, it was given a destination |
