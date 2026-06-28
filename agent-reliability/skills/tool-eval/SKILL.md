---
name: tool-eval
description: >-
  Verifies the tools an agent or orchestrator depends on, by re-deriving a tool evaluation's
  real accuracy instead of trusting a single pass/fail score. Separates a formatting miss
  (a correct value scored wrong) from a real failure (a wrong value scored right), recomputes
  the expected answer from the raw inputs rather than a stored ground truth, and surfaces the
  silent-wrong cases a naive exact-match scorer rubber-stamps. Produces a reproducible
  tool-reliability receipt and keeps any model's qualitative feedback on tool naming, docs, or
  errors as a clearly labeled judge layer, never mixed into the number. Use this whenever
  someone runs a tool or function-calling eval and the score looks fine, when an agent's tool
  results are "mostly right," when a calculator, extractor, API, or MCP tool eval reports a
  pass rate you are about to trust, or when you suspect a scorer is grading format instead of
  value. Trigger on mentions of tool eval, function-calling accuracy, exact-match scoring,
  ground-truth mismatch, format false-negative, or a tool that "passes the eval." This is the
  tool-contract deep skill that production-autopsy hands off to. Every number must be verified,
  never asserted.
---

# Tool Eval

A tool is the contract between a deterministic system and a non-deterministic agent. When you
score that contract with exact string match against a stored ground truth, the score itself
becomes untrustworthy in two directions at once: it marks a correct answer wrong when the
formatting differs, and it marks a wrong answer right when the answer happens to match a ground
truth that is itself wrong. The headline number hides both.

This skill does not grade the tool with another model's opinion. It re-derives the tool's real
accuracy from the raw inputs, separates the formatting misses from the genuine failures, and
hands back a receipt anyone can rerun. The qualitative judge layer, whether the tool is well
named and well documented, is kept, but it stays labeled as an opinion and never enters the
number.

## How to run it

> Run tool-eval on this tool evaluation. Take the committed run transcript (tool calls, answers,
> stored ground truth) and score it three ways: naive exact match, normalized value match
> (strip currency, commas, whitespace, then compare the numbers), and a recompute from the raw
> inputs that ignores the stored ground truth. Report the three accuracies, the format-only
> mismatches (correct value, scored wrong), and the silent-wrong cases (scored right, value
> wrong). Keep any tool-quality feedback as a separate judge layer. Verify every number with
> runnable code and write a receipt that fails closed.

## Core commitments

- **Verified numbers only.** Every figure traces to a measurement produced by runnable code. No
  remembered or approximate values.
- **Score value, not string.** Exact match is the scorer that created the false negative. The
  object of study is whether the tool returned the right value, measured against the answer
  recomputed from the raw inputs, not against a stored string.
- **Recompute the ground truth.** A stored ground truth can be wrong. Where the task allows the
  answer to be recomputed from its inputs, do that, and treat any disagreement with the stored
  truth as a finding, not noise.
- **Judge and receipt are different layers.** A model's opinion on tool quality is useful
  commentary. It is never mixed into the reproducible accuracy.
- **Reproducibility is part of the deliverable.** The fixture regenerates from a fixed,
  model-free transcript. Report the compute envelope (here, none: standard library).
- **Never regenerate committed fixture data.** If the target already ships a committed
  transcript, treat it as immutable and re-derive against it as-is.

## The procedure

### Step 0 - Name the contract and the scorer

Write down what the tool is supposed to return (the value and its type), and how the existing
eval scores it. If the scorer is exact string match against a stored ground truth, you already
have your two suspect failure directions: format false-negatives and silent false-positives.

### Step 1 - Score naive, normalized, and by recompute

On the committed transcript, compute three accuracies side by side: naive exact match (the
existing scorer), normalized value match (parse the number, strip currency and separators, then
compare), and recompute-from-inputs (compute the expected answer from the raw operands and
compare the tool's value to that). The three numbers, and where they disagree, are the finding.

### Step 2 - Separate the slices

Partition the failures: format-only mismatches (naive marks wrong, but the value is correct
against the recompute), silent-wrong (naive marks right, but the value is wrong against the
recompute), and true errors (wrong by both). The dangerous slice is silent-wrong: the eval
passed it and it is incorrect.

### Step 3 - Keep the judge layer separate

If a model offers feedback on tool naming, documentation, or error messages, record it under a
clearly labeled judge section. It does not change the accuracy and is never folded into it.

### Step 4 - Write the receipt

Produce a `verify.py` that re-derives all three accuracies and the slice membership from the raw
transcript, imports nothing it cannot rerun, and exits non-zero if any committed number fails to
reproduce. Bundle the fixture so the whole thing regenerates with no model and no GPU.

## Report structure

```markdown
# [Tool] Tool-Eval Receipt

## Summary
One paragraph: the naive score, the real (recompute) score, and the headline finding (for
example, "the naive score clears a wrong answer and fails a correct one").

## Three scorers
Naive exact-match, normalized value, and recompute-from-inputs accuracy, side by side.

## The slices
Format-only mismatches, silent-wrong, and true errors, each by task id.

## The receipt
What verify.py re-derives, and confirmation that it fails closed on a tampered transcript.

## Judge layer (labeled, not scored)
Any qualitative tool-quality feedback, kept separate from the number.

## Open questions
What is not yet established, and the measurement that would resolve it.
```

## Guardrails

- **Exact match is a format test, not a correctness test.** Never report it as accuracy without
  the value-level number beside it.
- **A stored ground truth can be the thing that is wrong.** Recompute where you can; a tool that
  matches a wrong truth is still wrong.
- **Silent-wrong is the headline, not the footnote.** A wrong value that passes the eval is more
  dangerous than a correct value the eval failed.
- **Do not let the judge layer leak into the number.** Opinion about tool quality is not a
  measurement of tool correctness.

## Worked illustration

A calculator tool eval scores 0.750 by exact string match. Re-derived from the raw operands it
also scores 0.750, but on a different set of failing tasks: the naive scorer marks a correct
answer wrong because it carries a dollar sign and a comma, and marks a wrong answer right because
it matches a transposed, incorrect stored ground truth. Normalizing format alone lifts the number
to 0.875 by recovering the false negative, but it still cannot see the silent error, because that
failure is about truth, not format. The whole thing reproduces from the standard library with no
model and no GPU, and the verification script fails closed if a single number is tampered. The
full worked example is in
[agent-reliability-receipts](https://github.com/ByteStack-Labs/agent-reliability-receipts).
