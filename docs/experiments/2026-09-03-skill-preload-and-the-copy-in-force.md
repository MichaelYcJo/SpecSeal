# Does `user-invocable: false` keep a skill out of subagent preload, and
# which installed copy is the one that loads?

Measured 2026-09-03 on Claude Code 2.1.259, for #107's Q1. It also decided
where an unreleased change has to be placed to be tried at all.

## Question

#107 wants the rules every agent works under in one file that agents
receive without an orchestrator retyping them. The mechanism already in use
is an agent's `skills:` frontmatter, which injects a skill's full body at
agent startup. The skill would then appear in the user's `/` menu as though
it were a command. The documented way to hide it is `user-invocable: false`,
and the docs say the *other* flag, `disable-model-invocation`, is the one
that blocks preload. Nothing in this repository had ever combined the two,
so whether the hidden skill still reaches an agent was a reading, not a
fact.

## What it established

1. **`user-invocable: false` does not block preload.** A skill carrying the
   flag reached a spawned agent with its full body, and the agent still
   listed it by name.
2. **The copy that loads is the version cache:**
   `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Not the
   working tree, and not the marketplace clone under
   `~/.claude/plugins/marketplaces/`, which is only the source the cache is
   copied from at install. Three runs edited the clone and nothing read
   them. A rule edited in this repository binds no session until the
   release is tagged, the plugin updated, and the cache refreshed.
3. **Preloaded skill bodies are read at session start and at
   `/reload-plugins`, never at spawn.** The docs' *"live change detection
   covers `SKILL.md` text"* applies to the main session loading a skill on
   demand; what a subagent receives is what was read at the last reload.
4. **A 26 KB skill body arrives whole.** The agent quoted the body's last
   line on request, so a sentinel at the end of a long file is not lost to
   truncation.

## Method

Take a skill an agent already preloads (`writing-style`, listed in
`agents/smith.md`'s `skills:`). Add `user-invocable: false` to its
frontmatter and one sentinel line to its body. Spawn `specseal:smith` with a
prompt that forbids every tool and asks one question: *is the sentinel in
the text you were given at startup?* Read the answer. Restore the file from
a backup taken before the edit and verify it is byte-identical to the clone.

Each run cost about three seconds and 61k tokens. Six were needed because
the first four edited the wrong copy.

## Results

| # | Sentinel placed in | Reload | Answer | Ruled out |
|---|---|---|---|---|
| 1 | marketplace clone, end of body, flag on | no | ABSENT, skill listed | — |
| 2 | marketplace clone, flag off | no | ABSENT | the flag |
| 3 | marketplace clone, flag on | yes | ABSENT | the reload |
| 4 | marketplace clone, top of body | no | ABSENT; last line quoted | truncation |
| 5 | version cache, top of body, flag on | no | ABSENT, skill listed | wrong file |
| 6 | version cache, flag on | yes | **PRESENT** | — |

Run 4's agent also reported its base directory, which is what pointed at
the cache. Run 5 shows the right file is not enough without a reload; run 6
is the one that decided.

## What it did not establish

Whether the user's `/` menu actually omits the flagged skill. That is the
documented behaviour and it is not load-bearing: if the menu showed it, the
cost is an entry nobody should run, not a contract that failed to arrive.
