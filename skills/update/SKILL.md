---
name: update
description: Update the plugin to the newest release and say what changed — runs both commands in the right order, then names the entries you are getting.
disable-model-invocation: true
---

# /specseal:update — take the release, and see what is in it

Two commands in a fixed order, and one thing neither of them does: tell you
what you are getting. Running them by hand answers "you are now on <version>",
which is a number, not a reason to reload or restart.

## Procedure

**1. Record what is running.** Read the `version` from
`$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json`. This is the version this
session actually loaded, which is the one the user is comparing against.

**2. Refresh the marketplace, then install.**

```bash
claude plugin marketplace update specseal
claude plugin update specseal@specseal
```

Both, in that order. The first pulls the marketplace clone; the second
installs from it. Running only the second reports *already at the latest
version* against whatever the clone last knew — the failure is silent and
looks like success.

If the second command reports it is already current, say so and stop. Nothing
arrived, so there is nothing to load and neither move below is needed.

**3. Name what changed.** Read `CHANGELOG.md` from the refreshed marketplace
clone — `~/.claude/plugins/marketplaces/specseal/CHANGELOG.md` — and summarize
every entry between the old version and the new one, oldest first. Lead each
with what it changes for the user, not with the release number.

Two kinds deserve to be called out on their own line, because a user who skips
them gets surprised later:

- **behavior that changes without being asked for** — a new gate, a gate that
  fires where it did not, anything that writes to their tree
- **anything they have to do** — a path that moved, a setting that was renamed,
  a compatibility fallback with an expiry

**4. Take the preset block if it moved.** The markers decide what is safe here.
Everything between `<!-- specseal:start -->` and `<!-- specseal:end -->` is
preset-owned and everything outside it is the user's, so replacing the region
cannot touch a line they wrote. `install.sh` relies on that boundary and so
does `preset-setup`, which replaces an older block without asking and diffs
only the remainder.

`claude plugin update` installs agents, skills, and hooks and never opens
`CLAUDE.md`, so without this step a release changes a rule while the
always-loaded file keeps stating the old one. Measured on this repository: the
block changed in two of thirteen releases, and the first went four releases
before anyone noticed.

```bash
diff <(sed -n '/specseal:start/,/specseal:end/p' ~/.claude/plugins/marketplaces/specseal/templates/claude-md-block.md) \
     <(sed -n '/specseal:start/,/specseal:end/p' ~/.claude/CLAUDE.md)
```

`templates/claude-md-block.md` is the block's one source; the plugin
repository's own `CLAUDE.md` carries a generated copy, held identical to it
in CI, and is not what to diff against.

Compare the scope that holds the block — `./CLAUDE.md` instead when the project
owns it.

| Result | What happens |
|---|---|
| No difference | nothing is said; the block is current |
| The block differs | back up to `CLAUDE.md.bak`, replace the marker region, and name the rules that arrived. No question is asked, because the markers already say those bytes were never the user's |
| No block on the machine | they never installed the preset. Say so and stop — writing one in is an install, and an update is what was asked for |

One case still needs a person. If a rule that just arrived also appears in the
user's own text outside the markers, the file now states it twice, and the copy
to remove is theirs. Name the overlap and point at `/specseal:preset-setup`,
which classifies it and proposes the deletion through an approved diff.

**5. Name both moves, cheapest first, and say what each one is known to do.**
It is safe to finish what you are doing either way: the running session keeps
the version it started with, because the old directory stays in the plugin
cache and `$CLAUDE_PLUGIN_ROOT` still resolves to it. Nothing is half-updated
and nothing breaks mid-session.

Then say what loads it. The two moves cost very different things — one ends
the session you are in and the other does not — so they are worth telling
apart, and the evidence behind them is not the same either:

| Move | What it is known to do | On what evidence |
|---|---|---|
| `/reload-plugins` | re-reads preloaded skill bodies out of the copy in force, which is what a spawned agent is handed | **measured.** Run 6 of `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md`: a sentinel in the version cache came back PRESENT after a reload, and ABSENT in run 5 without one |
| the same command, for anything else — hooks, agent definitions, or moving a running session onto a newly installed version | unknown | **not measured.** The experiment touched none of the three, and its sentinel sat in the *running* version's own directory, so it shows a re-read of the copy already loaded and nothing about picking up a new one |
| restarting Claude Code | starts a session on the newly installed version, with its skills, hooks and agent definitions | the move with no open question |

Say *not measured* rather than *not needed*. The difference is the whole
value of the row: a user told the reload is insufficient stops using it, and
a user told it covers everything gets a half-loaded plugin with no way to
tell.

What would settle the middle row, for whoever wants it settled: plant a
sentinel in a hook and in an `agents/*.md` under the newly installed version
in `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, type
`/reload-plugins` without restarting, then trigger the hook's event and spawn
the agent. That is run 6's own method, one artifact over.

## What this does not do

**It does not restart or reload anything.** Both are the user's to type.
Ending a session is their call and their unfinished work is in it — and a
built-in CLI command is not a skill, so `/reload-plugins` is not something
this procedure can invoke on their behalf either. Naming the cheaper move and
running it are different acts, and only the first is this command's job.

**It does not delete anything the user wrote.** The preset block is replaced
inside its markers, which is the whole of what the plugin owns. An overlap with
their own text outside the markers is reported, never resolved — that deletion
goes through `preset-setup`'s approved diff.

**It does not decide the update is wanted.** If a release changes behavior the
user relies on, the summary in step 3 is where they find that out — which is
why the summary comes with the update rather than after it.

## Output

```
Updated: <old> → <new>            (or: already on <version>, nothing to do)

What you are getting:
- <what changes for the user> (<version>)
- ...

Needs action:                     (omit when there is none)
- <what moved, what to set, what expires when>

To load it: /reload-plugins re-reads the skill bodies a spawned agent is
handed, out of the copy this session is already on. That is what was measured
and it is the whole of it. Nobody has measured whether a reload reaches hooks,
agent definitions, or <new> itself, so restart for those. Either way this
session keeps running <old> until you do, so nothing is half-applied.
```
