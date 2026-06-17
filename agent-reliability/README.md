# agent-reliability

**Teach your coding agent to ship AI that survives production, not just the demo.**

A set of Claude skills for the reliability of ML models and agents. They encode the failure modes
that do not show up in evaluation and only appear once real users and real load arrive: the model
that is confidently wrong, the eval set that never covered production, the agent whose steps each
pass while the whole trajectory degrades.

Built and maintained by [ByteStack Labs](https://bytestacklabs.com). Every skill here comes from a
real, public diagnostic, not a whiteboard.

It ships three skills:

- `production-autopsy`, the start-here triage. It reproduces and quantifies the failure, then points
  you to the right depth tool.
- `calibration-guard`, for systems that are confidently wrong. It measures where confidence and
  correctness come apart.
- `trajectory-eval`, for agents that degrade over multiple steps. It finds the step that introduces
  the failure.

## Why skills for production reliability

Coding agents now write most of the plumbing: they instrument apps, run experiments, wire up tools,
and build interfaces. They are very good at making a system pass its tests and demo cleanly. They are
not good at the part that actually decides whether you keep your customers: making it hold up with
real inputs, real users, and real concurrency.

That gap, between "the eval passed" and "it works in production," is where these skills live. An
agent with a benchmark and a trace viewer still needs to know what to look for. A model that scores
99.75% offline can be wrong 10% of the time in the field, and stay confident the whole way down.
These skills tell the agent what to measure, how to reproduce the failure, and how to prove the root
cause with numbers anyone can rerun.

## Install

The commands below run inside a Claude Code session, not in your terminal. Start a session first:

```bash
claude
```

Then, at the Claude Code prompt:

```
/plugin marketplace add ByteStack-Labs/claude-plugins
/plugin install agent-reliability@bytestack-labs
/reload-plugins
```

That is the whole install. If the commands do not appear right away, quit and run `claude` again; a
fresh start loads installed plugins.

## What you will see

A couple of moments look like problems but are not:

- Before you reload, running a skill returns "Unknown command." The plugin installs but does not load
  until you reload or relaunch.
- When you run a skill, it asks what system to point at and what symptom you are chasing before it
  does anything. That is the skill scoping the work first, by design.

## Run it

Point a skill at a real system: a path to a repo, a file of predictions or trajectories, or a live
endpoint with sample traffic. When asked, name the target and the symptom.

Start with the audit:

```
/agent-reliability:production-autopsy
```

It triages the failure and hands off: `calibration-guard` when the system is confidently wrong,
`trajectory-eval` when an agent breaks down over steps. You can also call those directly:

```
/agent-reliability:calibration-guard
/agent-reliability:trajectory-eval
```

Or point your agent at it in plain language:

> Install the agent-reliability plugin from github.com/ByteStack-Labs/claude-plugins, then run
> production-autopsy on my deployed system. Treat the eval set and the production behavior as separate
> distributions, reproduce the failure on production-realistic inputs, and verify every number with
> runnable code.

## The skills

Start with **production-autopsy**. It frames the eval-to-production gap, reproduces the failure,
quantifies it by slice, tests calibration under distribution shift, isolates root cause by ablation,
and returns a prioritized report. From there it hands off to the deeper skills below.

| Skill                | What it does                                                                          | Status |
| -------------------- | ------------------------------------------------------------------------------------- | ----- |
| **production-autopsy** | Start here. Audit a live system, reproduce and quantify the failure, return a prioritized root-cause report | shipped |
| **calibration-guard**  | Find where the system is confident and wrong, the failures an accuracy score hides    | shipped |
| **trajectory-eval**    | Evaluate the whole agent path, catching errors that compound across tool calls while each step passes | shipped |
| **coverage-audit**     | Check whether your test set actually covers your live input distribution               | planned |
| **load-readiness**     | Verify latency and throughput under real concurrency before production traffic         | planned |
| **drift-watch**        | Monitor model and judge agreement decay on live traffic over time                      | planned |

These skills encode failure modes that generalize across projects. Skills grounded in your stack,
your domain, and your data will outperform them. Start here, then write your own.

## Where these come from

Each skill is distilled from a public diagnostic you can read and rerun:

- **The format-fragility autopsy** (backs production-autopsy): an extractor at 100% exact match on
  evaluation drops to about 86% on the same fields with shifted formatting. The saved per-shift slices
  show order-preserving changes survive while field-moving ones collapse: it learned layout, not
  meaning. Runs with no model and no GPU, every number reproducible.
  [agent-reliability-examples](https://github.com/ByteStack-Labs/agent-reliability-examples)
- **The agents reality check** (backs trajectory-eval): a 73-point spread between agents, and zero
  positive synergy when chained. [ai-agents-reality-check](https://github.com/Cre4T3Tiv3/ai-agents-reality-check)
- **Throughput under real load** (the verified-numbers ethos): validated GFLOPS on constrained
  hardware, not quoted ones. [jetson-orin-matmul-analysis](https://github.com/Cre4T3Tiv3/jetson-orin-matmul-analysis)

calibration-guard ships the same methodology; its worked demonstration, a fixture that emits a real
confidence signal, is the next example landing in agent-reliability-examples.


## If it is your system that is failing

These skills let your team run the diagnostic. If you would rather have it run for you, end to end,
with a verified report you can act on, that is the ByteStack Labs Production ML Autopsy.

Bring us the situation: [bytestacklabs.com](https://bytestacklabs.com) ·
[book 30 minutes](https://calendly.com/jesse-bytestacklabs/30min)

## License

MIT. See [LICENSE](./LICENSE).