---
name: trajectory-eval
description: >-
  Evaluates whether an agent or a multi-step or multi-agent system actually completes the task, not
  just whether each step or the final answer looks right. Captures full trajectories (every step, tool
  call, and intermediate state), measures per-step success against end-to-end success, exposes the
  compounding-error curve where high per-step reliability still collapses over a long trajectory,
  attributes failures to the step that introduces them, and tests whether composing or chaining agents
  helps or hurts. Use this whenever an agent "works in the demo but fails with real users," passes its
  individual steps but fails the task overall, when multi-agent "synergy" is assumed rather than
  measured, for long-horizon or tool-using agents, or to benchmark agents head to head on real tasks.
  Trigger on mentions of agent reliability, tool calls, multi-step, multi-agent, orchestration,
  compounding errors, trajectory, long-horizon tasks, or agent evaluation. This is the agent depth
  that production-autopsy hands off to. Every number must be verified, never asserted.
---

# Trajectory Eval

An agent that passes every step's check can still fail the task. Errors compound: if each step is 95%
reliable, a ten-step task succeeds only about 60% of the time, and the gap widens fast as tasks get
longer. A final-answer eval hides this, because it scores the endpoint and ignores the path. A
per-step eval hides it too, because it scores steps in isolation and ignores how their errors
accumulate across the run.

This skill evaluates the whole trajectory: the steps, the tool calls, the intermediate states, and
the way failures propagate or get recovered. It measures where reliability actually leaks, and
whether chaining more agents into the system makes it better or just longer.

## How to run it

> Run trajectory-eval on this agent. Capture full trajectories on production-realistic tasks, measure
> per-step success against end-to-end success, and show the compounding curve. Attribute failures to
> the step that introduces them and say whether they cascade or recover. If the system chains or
> orchestrates agents, measure whether composition helps or hurts against a real baseline, with
> statistical validation. Test with tool failures and edge responses, not just the happy path. Verify
> every number with runnable code.

## Core commitments

- **Verified numbers only.** Every figure traces to a measurement produced by runnable code.
- **Evaluate the trajectory, not the endpoint and not the isolated step.** The final answer and the
  per-step score are the two numbers that hide compounding failure. The object of study is the path.
- **Measure compounding explicitly.** Connect per-step reliability to trajectory length to end-to-end
  success, rather than assuming the steps add up.
- **Test under realistic conditions.** Real tool responses, including failures and malformed outputs,
  not a curated happy path. A clean demo trace proves nothing.
- **Reproducibility is part of the deliverable.** Seed everything. Report the compute envelope.

## The procedure

### Step 0 - Define success at every level

Write down three definitions: final task success, per-step success, and the trajectory itself, meaning
the ordered steps, tool calls, and intermediate states. Decide what "correct" means at each level
before measuring, because the gap between these definitions is the entire investigation.

### Step 1 - Capture full trajectories

Instrument so every run leaves a complete trace: each step, the tool call and its response, the
intermediate state, and the final outcome. Run on production-realistic tasks, not the demo set. You
cannot attribute a failure you did not record.

### Step 2 - Measure per-step versus end-to-end, and the compounding curve

Report the per-step success rates and the end-to-end task success side by side. Then make the
compounding explicit: given the measured per-step reliability, what end-to-end success would you
expect at N steps, and how does the observed end-to-end compare. The gap between "the steps all look
fine" and "the task fails" is the headline of this skill.

### Step 3 - Attribute the failure across steps

For the failed trajectories, find the step that introduces the error and determine whether it cascades
downstream or gets recovered. Separate compounding failures, where small errors accumulate, from
single-point failures, where one broken step sinks the run. The two have different fixes, and treating
one as the other wastes the remediation.

### Step 4 - Test composition and synergy

If the system chains or orchestrates multiple agents, measure whether composition actually helps.
Compare the composed system against its parts on the same tasks, and state whether the synergy is
positive, zero, or negative, with statistical validation rather than a single run. Inject realistic
tool failures and edge responses to test whether the system recovers or collapses. "More agents
cooperate into better results" is a claim, not a measurement, until you have run this.

### Step 5 - Package for reproducibility

Bundle the seeds, the task set, the captured trajectories, and the measurement scripts. Report the
compute envelope so the team knows what it takes to rerun.

## Report structure

```markdown
# [System] Trajectory Evaluation

## Summary
One paragraph: does the agent complete the task, where reliability leaks, and whether composition
helps. Lead with the per-step versus end-to-end gap.

## Trajectories
What was captured, and on which tasks.

## Per-step vs end-to-end
The rates side by side, and the compounding curve.

## Failure attribution
Which steps introduce failures, and whether they cascade or recover.

## Composition and synergy
The composed system vs its parts, with statistical validation. Positive, zero, or negative.

## Reproducibility
Seeds, task set, captured traces, scripts, compute envelope.

## Open questions
What is not yet established, and the measurement that would resolve it.
```

## Guardrails

- **Final-answer accuracy hides trajectory failure.** Never conclude an agent is reliable from the
  endpoint alone. The same final answer can come from a clean path or a lucky recovery.
- **Per-step accuracy hides compounding.** Always connect step-level numbers to end-to-end success
  over a realistic trajectory length.
- **Synergy is usually assumed, not measured.** Chaining agents can produce zero or negative synergy.
  Measure it against a real baseline before claiming the composition earns its complexity.
- **A happy-path trace proves nothing.** Test with tool failures, malformed responses, and edge
  inputs, since that is where real trajectories break.
- **Report uncertainty.** Use confidence intervals and effect sizes, not single runs, especially when
  comparing agents or compositions head to head.

## Worked illustration

Three agent archetypes were put through stress testing, network-resilience analysis, and
ensemble-coordination measurement, all with proper statistical validation. The spread between
archetypes ran 66 to 73 points, and chaining them produced zero positive synergy: across every pattern the
composed system was no better than its parts, often worse, while each step could still pass its own check as
the trajectory degraded. The hype
held that more agents cooperate into better results. The trajectory held otherwise, and the number
proved it. Evaluating the path, rather than the final answer or the isolated step, is what surfaced
the difference.