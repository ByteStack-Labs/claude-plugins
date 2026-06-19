# ByteStack Labs · Claude plugins

The ByteStack Labs marketplace for Claude Code. Open plugins for shipping AI that holds up in
production, not just in evaluation. Each plugin is a focused "arc": a set of skills distilled from
real, public diagnostics. Every number reproducible.

Maintained by [ByteStack Labs](https://bytestacklabs.com).

## Add the marketplace

```
/plugin marketplace add ByteStack-Labs/claude-plugins
```

## Plugins

| Plugin | What it does | Install | Status |
| --- | --- | --- | --- |
| **agent-reliability** | Audit AI agents and ML systems that pass evaluation but fail in production. Skills: production-autopsy, calibration-guard, trajectory-eval. | `/plugin install agent-reliability@bytestack-labs` | shipped |

Install a plugin, then invoke its skills as `/<plugin>:<skill>`, for example
`/agent-reliability:production-autopsy`.

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
        ├── calibration-guard/
        │   └── SKILL.md
        └── trajectory-eval/
            └── SKILL.md
```

## Adding an arc

A new arc is a new top-level directory with its own `.claude-plugin/plugin.json`, plus an entry in
`marketplace.json`. The marketplace name stays `bytestack-labs`; each plugin name stays distinct from
it (this avoids the install-time name collision Claude Code hits when a plugin name equals the
marketplace name). No renames, no broken installs, no moved URLs.

## License

MIT. See [LICENSE](./LICENSE).
