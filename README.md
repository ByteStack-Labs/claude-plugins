# ByteStack Labs · Claude plugins

The ByteStack Labs marketplace for Claude Code. Open plugins for shipping AI that
holds up in production, not just in evaluation. Every published number reproduces
from runnable code.

Maintained by [ByteStack Labs](https://bytestacklabs.com).

## Why this exists

The job is moving from building to orchestrating. Reviewers now sit on top of AI agents
doing the execution, which means the output outnumbers the eyes that can read it. In that
shape the dangerous failure is not the loud one. It is the output that is well-formed and
wrong: it parses, it has the right shape, it raises no error, and it is simply incorrect,
which is exactly what a happy-path check, one written only for the inputs that behave as
expected, never inspects.

`agent-reliability` is the verification floor for that shape. It does not grade agent
output with another opinion. It re-derives the result from the raw data and fails closed,
erroring out instead of quietly passing, the moment a number does not reproduce. A judge
tells you an answer looks good. A self-test tells you it passed the checks someone already
thought to write. A receipt tells you the number reproduces, from raw data, for anyone,
every time. That last one is the thing an orchestrator cannot steer without, and it is
what these skills produce.

Why "done" is a claim and not a proof:
<https://www.bytestacklabs.dev/writing/your-loop-says-done>

## Add the marketplace

```
/plugin marketplace add ByteStack-Labs/claude-plugins
```

## Plugins

| Plugin                | What it does                                                                                                                                | Install                                            | Status  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------- |
| **agent-reliability** | Audit AI agents and ML systems that pass evaluation but fail in production. Skills: production-autopsy, tool-eval, calibration-guard, trajectory-eval. | `/plugin install agent-reliability@bytestack-labs` | shipped |

Install a plugin, then invoke its skills as `/<plugin>:<skill>`, for example
`/agent-reliability:production-autopsy`.

## Skills and receipts

Each skill ships as an installable skill. A receipt is that skill's own output, run
against a public fixture, a small test program built to carry one real flaw, and committed
so anyone can rerun it. Receipts live in
[agent-reliability-receipts](https://github.com/ByteStack-Labs/agent-reliability-receipts),
where the full "what is shipped and what is landing" table is maintained.

| Skill                  | Value                                                | What it proves                                                                                                                          | Public receipt                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **production-autopsy** | Find the silent production failure your eval cleared. | Where the eval stops matching production, which slice, a group of cases sharing one trait, carries the failure, and how much of the error is silent rather than loud. | shipped — `invoice-extraction` |
| **tool-eval**          | Tell a formatting miss from a real tool failure.     | Whether a tool eval's score is real: it separates a formatting miss (correct value marked wrong) from a silent failure (wrong value marked right), recomputing the answer from raw inputs rather than a stored ground truth. | shipped — `tool-eval` |
| **calibration-guard**  | Catch confident-but-wrong before it ships.           | Whether a model's stated confidence matches its real accuracy, and where it is overconfident.                                          | shipped — `calibration-guard`  |
| **trajectory-eval**    | Locate where a passing agent silently breaks.        | Whether a multi-step agent actually reaches the goal, and where in the trajectory it silently goes wrong.                              | landing                        |

Until a skill's receipt is public, treat its results as not-yet-reproducible and do
not cite them as proven. The discipline is the product: a number that has not shipped
a receipt is a claim, not a fact.

## Structure

```
claude-plugins/                       this marketplace
├── .claude-plugin/
│   └── marketplace.json              marketplace manifest (name: bytestack-labs)
├── README.md
├── LICENSE
└── agent-reliability/                arc 1 (plugin name: agent-reliability)
    ├── .claude-plugin/
    │   └── plugin.json
    ├── README.md
    ├── LICENSE
    └── skills/
        ├── production-autopsy/
        │   ├── SKILL.md
        │   └── scripts/
        │       └── finalize.py        deterministic placement + certification
        ├── tool-eval/
        │   └── SKILL.md
        ├── calibration-guard/
        │   └── SKILL.md
        └── trajectory-eval/
            └── SKILL.md
```

## Adding an arc

An arc is one plugin: a focused set of skills shipped together. A new arc is a new
top-level directory with its own `.claude-plugin/plugin.json`, plus an entry in
`marketplace.json`. The marketplace name stays `bytestack-labs`; each plugin name stays
distinct from it (this avoids the install-time name collision Claude Code hits when a
plugin name equals the marketplace name). No renames, no broken installs, no moved URLs.

## License

MIT. See [LICENSE](LICENSE).

---

ByteStack Labs builds production reliability for AI and ML systems. Every number
reproduces from runnable code, or it does not ship. <https://bytestacklabs.com>
