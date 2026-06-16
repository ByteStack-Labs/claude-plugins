---
name: calibration-guard
description: >-
  Detects and quantifies confidently-wrong behavior: where a model, classifier, agent, or LLM judge
  is highly confident and incorrect, and where the coupling between confidence and correctness breaks
  down under distribution shift. Measures calibration on the in-distribution set and again on the
  production distribution, builds reliability diagrams, reports expected calibration error and the
  high-confidence error rate, and produces a selective-prediction or escalation rule you can wire into
  monitoring. Use this whenever someone says a system is "confident but wrong," "sure of itself and
  failing," or "silently wrong," when accuracy looks fine but trust is eroding, when an LLM judge's
  scores stop tracking human labels, or when production errors arrive at high confidence with nothing
  flagging them. Trigger on mentions of calibration, reliability diagram, ECE, overconfidence, false
  reassurance, abstention, selective prediction, or confidence thresholds. This is the deep confidence
  workup that production-autopsy hands off to. Every number must be verified, never asserted.
---

# Calibration Guard

A system that fails loudly is recoverable: something downstream sees the error and reacts. A system
that is confidently wrong is dangerous, because nothing flags it. The prediction ships, the agent
acts, the report reassures, and the failure stays silent until it is expensive.

This skill measures one thing precisely: whether the system's confidence tracks its correctness, and
how that relationship breaks when the input distribution moves from evaluation to production. It does
not improve calibration. It proves the state of it, with numbers anyone can rerun, and hands back a
rule that catches the confident-wrong cases before they ship.

## How to run it

> Run calibration-guard on this system. Pick a confidence signal and a correctness signal, measure
> calibration on the eval distribution and again on production-realistic inputs, and report the
> reliability diagram, ECE, and the high-confidence error rate. Show how the gap between confidence on
> correct and confidence on incorrect predictions changes under the shift. Then give me a
> selective-prediction rule that catches the confident-wrong cases, with its precision and its
> coverage cost. Verify every number with runnable code.

## Core commitments

- **Verified numbers only.** Every figure traces to a measurement produced by runnable code. No
  remembered or approximate values.
- **Measure the coupling, not the accuracy.** Accuracy is the number that hid this failure. The
  object of study is the relationship between confidence and correctness, not either alone.
- **Calibration is a property of a distribution.** Always measure it on both the evaluation
  distribution and the production distribution. A single measurement tells you nothing about what
  happens when inputs move.
- **One calibration number hides per-slice miscalibration.** Decompose by slice before concluding.
- **Reproducibility is part of the deliverable.** Seed everything. Report the compute envelope.

## The procedure

### Step 0 - Define the confidence and correctness signals

Name both explicitly. Confidence proxies include token logprobs, sequence probability, softmax
maximum, verbalized confidence, an LLM judge's score, or ensemble agreement. Correctness needs a
ground truth or a trusted proxy: human labels, a downstream outcome, or a verified reference. State
which signal you are using and its limits, because the choice shapes every number that follows.

### Step 1 - Measure calibration on the in-distribution set

On the evaluation distribution, build the reliability diagram (confidence bins against empirical
accuracy), compute expected and maximum calibration error, and plot confidence histograms split by
correct versus incorrect predictions. This is the baseline coupling: how well confidence tracks
correctness when inputs look like the test set.

### Step 2 - Measure calibration under the production distribution

Recompute everything on production-realistic inputs, or on the shifted distribution where the failure
appears. The comparison between Step 1 and Step 2 is the finding, not either number alone.

### Step 3 - Quantify the decoupling and the confident-wrong rate

Report three things: the separation between mean confidence on correct predictions and mean confidence
on incorrect ones, and how that separation changes under the shift; the high-confidence error rate,
meaning the fraction of errors that arrive above a chosen confidence threshold; and the change in
calibration error. The signature failure mode is the correct-versus-incorrect confidence gap
narrowing, or accuracy collapsing while confidence holds steady. When that happens, nothing
downstream can tell a right answer from a wrong one by confidence alone.

### Step 4 - Build the confident-wrong detector

Turn the analysis into an operating rule. Define a threshold (on confidence, or on disagreement
between signals) for selective prediction: abstain, flag, or escalate to a human or a secondary check
when the rule fires. Report the rule's precision and recall for catching actual errors, and its
coverage cost, meaning how many correct predictions it needlessly holds back. This rule is the
deliverable that goes into monitoring. A diagnosis without it leaves the team knowing they are
confidently wrong but unable to catch it in flight.

### Step 5 - Package for reproducibility

Bundle the seeds, the evaluation and production input sets, the measurement scripts, and the
confidence and correctness extraction. Report the compute envelope so the team knows what it takes to
rerun.

## Report structure

```markdown
# [System] Calibration Report

## Summary
One paragraph: is it confidently wrong, by how much, and does it worsen under shift. Lead with the
high-confidence error rate.

## Signals
The confidence proxy and the correctness signal used, and their limits.

## Calibration: in-distribution
Reliability diagram, ECE and MCE, confidence split by correct vs incorrect.

## Calibration: production distribution
The same, recomputed under shift. The change is the finding.

## The decoupling
Confidence on correct vs incorrect, and how the gap moves. The high-confidence error rate.

## The detector
The selective-prediction or escalation rule, its precision and recall for catching errors, and the
coverage it costs.

## Reproducibility
Seeds, datasets, scripts, compute envelope.

## Open questions
What is not yet established, and the measurement that would resolve it.
```

## Guardrails

- **Calibration is point-in-time.** It decays as the distribution moves, so monitor it on a sample of
  live traffic over time. Measuring it once and trusting it is the mistake this skill exists to catch.
- **A single calibration number hides slice-level miscalibration.** Report by slice; a model can be
  well-calibrated on average and badly miscalibrated on the slice that matters.
- **The confidence proxy has limits.** Logprobs are not always available or meaningful, for example on
  post-hoc tuned models or LLM judges. Name the proxy and what it can and cannot tell you.
- **Do not conflate calibration with accuracy.** A model can be accurate and miscalibrated, or
  inaccurate and well-calibrated. They are different properties and need different fixes.
- **Recalibration is distribution-specific.** Temperature scaling and similar fixes recalibrate on one
  distribution and can fail on another. If you recommend a fix, test it on the production
  distribution, not the one you tuned it on.

## Worked illustration

A Qwen2.5-1.5B model fine-tuned for structured extraction scored 99.75% exact match on evaluation and
90.0% on production-realistic inputs under a shift in formatting distribution. The decisive finding
was not the ten-point accuracy drop. It was that the incorrect predictions came back at roughly 82%
confidence, nearly indistinguishable from the correct ones: the gap between confidence on correct and
incorrect predictions nearly doubled under the shift, in the wrong direction. The model was not
uncertain about its errors. It was confident on them, and nothing downstream could have known.
Reframing the problem from "ten percent less accurate" to "confidently wrong eight percent of the
time, with no signal" changed both its severity and its fix. Producing that reframing, with the
numbers behind it, is the job of this skill.
