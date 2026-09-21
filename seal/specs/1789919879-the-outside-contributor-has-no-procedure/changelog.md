<!-- seal/specs/1789919879-the-outside-contributor-has-no-procedure/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The outside contributor had no procedure, and the gate that caught the
  first one named the wrong file** (#443). A first-time contributor opened a
  pull request against `main`, because nothing this repository showed a
  contributor said where a pull request goes: the contribution guide opened on
  how to run the suite, neither README carried the fact, and there was no pull
  request template. GitHub's default is the default branch, and nothing
  offered an alternative. The hygiene step then refused it with a message
  naming `.claude-plugin/plugin.json` and a version — correct for somebody
  cutting a release, and for a contributor an instruction to edit the one file
  their change must not touch.

  - **The refusal names both causes and asserts neither.** At the moment it
    refuses, the two readers are indistinguishable to the step: a release that
    forgot the version bump and a contribution filed against the wrong branch
    both arrive with `base_ref = main`. So the message states the release case
    first — that reader is who the old text was already right for — then the
    base-branch case, and it says which of the two edits is the wrong one
    (`Change the base rather than plugin.json`). The branch is named by
    convention, `release/vX.Y.Z`, never by a version number that expires with
    the branch it names.

    **The step's logic does not move.** The condition, the exit codes and the
    set of refused pull requests are identical before and after; only the text
    a refused author reads differs, which is the failure direction
    `CONTRIBUTING.md` §*What a change to a gate must carry* asks a gate change
    to state. Prompt budget: zero.

  - **`CONTRIBUTING.md` opens with the procedure**, above §*Running the
    checks*. Which branch to base on and how to find it without knowing
    today's version, why a wrong base is refused with a message about a
    version, and what a contribution is asked for.

    **The half that cannot be inferred is the exemption list.** This
    repository runs a spec-driven workflow on itself — work items, review
    rounds, an evidence ledger — and an outsider has every reason to assume
    all of it applies to them. None of it does: no `routing.md`, no `spec.md`
    or `plan.md`, no round record, no ledger row, no changelog fragment, no
    `overview.md`, no version bump, and no commit gate or worktree guard,
    which are hooks on a maintainer's machine. Each row names the CI step that
    would have asked and its own reason for not asking — three of them exit
    early on any base but `main`, and the rest run on every pull request and
    ask nothing of a branch that declared nothing — so the list reads as a
    consequence of the workflow rather than as a promise.

    **Two checks can still refuse a contribution**, and both are documented
    with what to do instead, which is to say so on the pull request rather
    than create anything under `seal/`. *Wording this branch removed is not
    still standing elsewhere* sends the author into a `survivors.md` they do
    not have. The `ledger` job is the second: drift under an anchor that still
    resolves is a warning, but an anchor that stops resolving — a heading
    renamed, a function removed — is exit 2, and the repair is a maintainer's
    for the same reason.

  - **A pull request template**, `.github/PULL_REQUEST_TEMPLATE.md`, carrying
    the base-branch fact in its own words. Its whole advantage is reaching
    somebody who opened no document, so it states the fact rather than only
    linking to it, and it sits on the same screen as the base dropdown it is
    about. The guidance is HTML comments: that is what a contributor reads
    while writing, it renders nothing into the posted pull request, and a
    maintainer therefore has nothing to delete each time.

  - **Both READMEs** state where a pull request goes and summarise the
    exemption list, ahead of the gate bar they already carried.

  - **The rationale says what the gate actually does.** A pull request into
    `main` is refused for leaving the version alone only when it touches what
    the plugin ships; one that touches nothing shipped gets a green run on the
    wrong base. The template and both READMEs say so, because a reader taught
    that the gate is what catches a wrong base draws the wrong conclusion from
    a green run. The rule is the branch, not the check.

  - **The branch-by-convention rule is pinned on every surface that carries
    it**, not only on the two it was first written on. `README.md`,
    `README.ko.md` and the pull request template each go red on a concrete
    `release/vX.Y.Z`, which is the single edit that would otherwise put a
    branch name into a document that outlives it.
