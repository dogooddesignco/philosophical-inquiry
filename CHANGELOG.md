# Changelog

All notable changes to the Philosophical Inquiry tool, documented so future sessions understand the journey.

---

## [Unreleased] — 2026-03-30

### Initial Build
- Single-file HTML app (`philosophical_inquiry.html`) with embedded CSS and JS
- Python local proxy server (`server.py`) that routes API calls through the authenticated Claude CLI
- macOS double-click launcher (`Philosophical Inquiry.command`)
- Project brief (`philosophical_inquiry_brief.md`)

### Architecture: CLI Proxy
- **Problem:** Anthropic's API rejects OAuth tokens via direct browser requests ("OAuth authentication is currently not supported")
- **Solution:** Local Python HTTP server wraps `claude -p` (which IS authenticated via Max/Pro subscription) and returns responses in Messages API format
- Browser POSTs to `localhost:8766/api/messages` → server calls Claude CLI → returns result
- Also supports direct API key mode as a fallback

### Prompt Design — Multiple Iterations
The system prompts went through extensive revision to minimize experimenter bias:

1. **No tradition definitions in prompts.** The system prompt names the tradition and nothing else. The model draws entirely on its training. If it misrepresents a tradition, that's data.

2. **Traditions as lenses, not identities.** Early prompts had agents "defend" their tradition. Rewritten so agents use their tradition as a way of seeing, with loyalty to truth rather than to the tradition itself. Key line: *"Your loyalty is to what is true, not to the tradition itself. [Tradition] is how you see, not what you defend."*

3. **Removed Western analytical bias.** Caught that phrases like "more precise reasoning" and "useful" privileged Western analytical modes. Replaced with language about finding commonalities concealed by language, filling gaps, building a more coherent picture.

4. **No prescriptive modes.** Traditions told to respond "in whatever mode is natural to your tradition" — no examples given. Avoids privileging systematic argument over narrative, paradox, questioning, etc.

5. **Stripped diplomatic filler.** Agents instructed: *"Do not use diplomatic filler ('I appreciate...', 'That's a valid point...'). If you have nothing substantive to say about another position, say nothing about it."*

6. **Round 2+ prompts simplified.** Originally restated system prompt rules in the user message ("but shittier" — user's words). Stripped to just delivering prior dialogue + "Go deeper. Get closer to what is actually true."

### Moderator Design
- Moderator is invisible to tradition agents — observes but never speaks to them
- Evaluates: tradition integrity, depth vs. surface, frame dominance, organic alignment, irreducible tensions
- Verdicts: CONTINUE, FORMULATE, RESOLVED, HONEST_DIVERGENCE
- Does not know it is being used for bias detection — prevents performative bias-detection
- Higher bar for RESOLVED — requires a single coherent shared answer, not separate endorsements

### Joint Formulation Process
After traditions produce individual formulations, a three-step synthesis produces one final answer:
1. **Draft:** Moderator synthesizes all individual formulations into one coherent paragraph
2. **Review:** Each tradition reviews the draft (50-100 words) — flags omissions, distortions, glossed-over tensions
3. **Final:** Moderator incorporates relevant feedback and presents the definitive formulation

This replaced an earlier design where individual formulations were the endpoint, which felt scattered.

### Topic Screening
- Gatekeeper prompt runs before any tradition agents engage
- Accepts genuine philosophical/ethical/metaphysical/epistemological questions
- Rejects homework, task requests, prompt injection, nonsense, personal advice
- Non-adversarial approach: simply asks whether the topic is a genuine philosophical question

### Tradition Selection
Traditions organized into six categories with per-category toggles:

**Classical Philosophy:** Stoicism, Confucianism, Existentialism, Pragmatism, Phenomenology, Process Philosophy

**Contemplative & Metaphysical:** Buddhism, Madhyamaka, Daoism, Advaita Vedanta

**Ethical Frameworks:** Utilitarianism, Virtue Ethics, Deontology, Care Ethics

**Epistemology & Logic:** Pyrrhonian Skepticism, Nyaya, Empiricism, Rationalism

**Critical Methods:** Critical Theory, Deconstruction, Feminist Epistemology

**Scientific & Empirical:** Panpsychism, Relational Quantum Mechanics, Enactivism, Assembly Theory

Design decisions on tradition selection:
- Excluded traditions that reduce to "because authority says so" — each must have a deep, independent philosophical methodology
- Avoided traditions where model training data is too thin or too Westernized (e.g., Ubuntu philosophy flagged as risk of being filtered through Western liberal individualism)
- Added modern/scientific schools (panpsychism, RQM, enactivism, assembly theory) as genuine philosophical voices, not just data sources
- Critical Theory agent noted as potentially annoying in practice — system prompt adjusted to prevent any tradition from dominating through rhetorical urgency rather than substance

### History & Transcripts
- Verbatim transcripts saved to localStorage after each inquiry
- History tab with session list (topic, date, traditions, verdict)
- Full transcript reader: all rounds, responses, moderator assessments, synthesis
- Delete individual sessions

### Analytics
- Tracks across sessions: verdict distribution, average depth, average rounds
- Frame dominance tracking: which tradition's vocabulary most often shapes discourse
- Tradition integrity flags: how often each tradition is flagged for abandoning commitments
- Designed as a bias fingerprint of the model over time

### Bug Fixes
- **classList crash:** `showView('inquiry')` referenced non-existent `nav-inquiry` element. Fixed with null check and fallback.
- **Formulation loop:** Two bugs — (1) loop didn't stop at MAX_ROUNDS, (2) formulation round didn't terminate the loop. Fixed with explicit `break` conditions.
- **Font sizes:** Enforced 16px minimum throughout all text elements.
- **Port conflicts:** Preview server orphaned processes on port 8766. Killed with `lsof -ti :8766 | xargs kill -9`.

---

## Design Philosophy

This tool is not a debate simulator (no winners), not a philosophy encyclopedia (doesn't explain traditions), and not a traditional bias audit (no adversarial prompts). It creates conditions where bias reveals itself naturally through the pressure of sustained, multi-perspective inquiry. The prompts do as little as possible. The model's own understanding — and its own limitations — do the rest.
