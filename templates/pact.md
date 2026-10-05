# Pact

<!-- seal/pact.md — the one copy of what two or more repositories keep
together (`docs/the-pact.md`). It lives in one of them, the pact's
repository, and every repository of a work item that keeps it is a
signer, that one included.

**What belongs here.** A sentence is contract when another repository's code
would be wrong if it changed. A sentence only this repository's code depends
on belongs in this repository's own documents, and a pact that collects those
is a pact every signer has to re-read for changes that were never theirs.

**The table below lists every OTHER signer** by its origin remote URL. The
pact's repository does not list itself: its own citations of a clause are
ordinary ledger coordinates, `seal/pact.md#"## Clause"@<hash>`, which its own
`evidence-check` reads. Each signer listed here names this repository in
its own `seal/config.md`, in a `Pact` row (`templates/config.md` §*Pact*).
`pact-check` refuses a relationship recorded on one side only.

**Every `##` heading below the table is a clause**, and a `###` under it
narrows inside it. A signer cites a clause as

    pact:<name>/"## Clause / ### Narrower"@<hash>

where `<name>` is the last path segment of this repository's normalised
origin URL and `<hash>` is `evidence-check`'s content hash of the clause's
region. A `SUPERSEDED` or `UNMATCHED` line from `pact-check` names the
clause's current hash, so a new citation can be written with `@00000000` and
corrected from its first report.

**A heading is an address.** Rewording a clause's prose is a change every
citing signer sees as `SUPERSEDED` and re-reads. Renaming its heading is a
change every one of them sees as `BROKEN`, and each has to re-coordinate.

The pact is written by the build at this repository, framed by this
repository's own spec, the way a policy document is edited. -->

| Signer |
|---|
| <the origin remote URL of another signer, one per row> |

## <a clause: what another repository's code depends on>

<the sentence that repository's code would be wrong without>
