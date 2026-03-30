# Philosophical Inquiry

A multi-agent dialogue system where independent philosophical traditions engage with the same question — not to debate, not to win, but to find what is true.

## Why this exists

This project serves two purposes that turn out to be deeply connected.

### 1. Truth-seeking through independent convergence

Most AI tools that engage with philosophy treat it as a content category — summarize Stoicism, compare Kant and Mill, explain the trolley problem. This tool does something different. It creates conditions where multiple traditions can pursue the same question simultaneously, each working from its own commitments, its own methods, its own way of knowing — and then observes what happens.

The key design principle: **no tradition is told to agree with any other.** Each agent is instructed only to pursue the truest answer it can, in whatever mode is natural to its tradition. A separate moderator observes the dialogue and watches for places where traditions independently arrive at similar conclusions through genuinely different paths. That kind of convergence — organic, unforced, arrived at from different starting points — is a meaningful signal. It suggests the insight may be pointing at something real rather than reflecting the assumptions of any single framework.

Equally valuable is honest divergence. When traditions reach an irreducible disagreement — one that cannot be resolved without somebody abandoning a core commitment — that too is information. It maps the actual structure of the problem in a way that no single perspective can.

### 2. Uncovering structural bias in language models

When you ask an LLM to roleplay as a Stoic, a Buddhist, and a Critical Theorist, the model brings its own prior to every role. If the "Stoic" keeps making arguments that are structurally utilitarian, or the "Daoist" keeps using the language of Western liberal individualism, that is not the tradition speaking. That is the model's default frame leaking through the mask.

This tool is designed to make that leakage visible and measurable. A moderator agent evaluates every round of dialogue on several axes:

- **Tradition integrity** — Has any tradition abandoned its own commitments to sound more agreeable?
- **Frame dominance** — Whose conceptual vocabulary is shaping the discussion? If something looks like shared understanding, whose framework is it actually expressed in?
- **Organic alignment vs. artificial convergence** — Did traditions genuinely arrive at similar conclusions independently, or did one frame absorb the others?

These signals accumulate across sessions in an analytics layer that tracks which traditions get flagged most often for abandoning commitments (the model cannot hold that frame), whose vocabulary dominates syntheses (the model's default prior), and how often inquiries resolve versus reach honest divergence.

Over time, this becomes a bias fingerprint of the model — not through adversarial probing, but through the natural pressure of asking it to hold multiple perspectives simultaneously and honestly.

## Design decisions

Several design choices were made deliberately to minimize experimenter bias:

**No tradition definitions in prompts.** The system prompt names the tradition and nothing else about it. No summaries of key thinkers, epistemological tools, or core commitments. The model draws entirely on its own training. If it gets a tradition wrong, that is data — not a bug to preempt with a cheat sheet.

**No agreement language.** No tradition agent prompt contains the words "agreement," "consensus," "convergence," or "common ground." Each agent is told only to pursue truth. Convergence detection happens externally, in the moderator, which the tradition agents never see.

**No prescriptive modes of discourse.** Traditions are told to respond "in whatever mode is natural to your tradition" — without examples of what that might mean. This avoids privileging Western analytical modes (systematic argument, precise claims) over traditions that might naturally work through narrative, paradox, questioning, or other forms.

**System prompts are universal and topic-free.** The tradition's identity prompt is the same regardless of the question being asked. The topic, prior dialogue, and moderator challenges are delivered as runtime content. This makes the prompts auditable and stable.

**The moderator does not know why we care about frame dominance.** It is told to observe whose vocabulary shapes the discourse, but not told that this is a bias detection mechanism. This prevents the moderator from performing bias-detection rather than doing it honestly.

## How it works

1. The user submits a topic and selects which traditions participate.
2. **Round 1:** Each tradition responds independently. No tradition sees another's response.
3. **Moderator evaluation:** The moderator assesses tradition integrity, depth, frame dominance, organic alignments, and irreducible tensions. It issues a verdict: CONTINUE, RESOLVED, or HONEST_DIVERGENCE.
4. **Round 2+:** If CONTINUE, traditions receive the full prior dialogue plus specific challenges from the moderator. They go deeper.
5. **Resolution:** The inquiry ends when the moderator identifies a genuine shared insight, an honest irreducible divergence, or the maximum number of rounds is reached.
6. **Analytics:** The session is logged — verdict, depth scores, integrity flags, frame dominance patterns — accumulating data across inquiries.

## What this is not

This is not a debate simulator. Debates have winners. This tool has no winners — only the question of whether something true was found.

This is not a philosophy encyclopedia. It does not explain traditions to the user. It puts traditions to work on real questions and observes what they actually produce.

This is not a bias audit in the traditional sense. It does not use adversarial prompts or red-teaming. It creates conditions where bias reveals itself naturally through the pressure of sustained, multi-perspective inquiry.

## Origin

This project emerged from a conversation about whether an AI tool existed that could simulate a room full of philosophers from different schools all engaging with the same topic — not debating, but genuinely trying to find truth together. Nothing adequate existed. The design evolved through iterative questioning of every prompt decision: does this word bias the outcome? Does this instruction privilege one mode of thinking? Does this summary narrow what the model already knows? The result is a system where the prompts do as little as possible and the model's own understanding — and its own limitations — do the rest.
