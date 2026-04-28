# Cynefin Framework Reference

> Cynefin (Welsh: /kəˈnɛvɪn/ — "the place of your multiple belongings") is a sense-making framework developed by Dave Snowden. It holds that context determines appropriate action: the same response that is optimal in one domain is actively harmful in another.

All agents in this organization must classify the problem domain before selecting a response strategy. This file is the authoritative reference for that classification and the behaviors it requires.

---

## The Five Domains

### 1. Clear (Known Knowns)

**Character:** Cause-and-effect relationships are visible, stable, and understood by most participants. One right answer exists and is already documented.

**Protocol:** Sense → Categorize → Respond

- **Sense:** Observe the incoming situation
- **Categorize:** Match it to a recognized pattern
- **Respond:** Apply the established best practice

**Signals:**

- Proven procedure exists and reliably produces the correct output
- Team has handled this exact class of problem repeatedly
- Outcome of applying the procedure is predictable in advance
- Experts would universally agree on the correct approach
- Variability in inputs and outputs is low

**SDLC approach:** Automated pipelines, checklists, SOPs. Heavy automation. Human decision-making minimized. Definition of Done is binary.

**Software examples:** Deploying via an established CI/CD pipeline with passing tests. Running a documented migration script. Applying a canonical algorithm to a well-defined input. Provisioning from a validated infrastructure module.

**WARNING — The Clear→Chaotic Cliff:** The Clear domain is the most dangerous. Success breeds complacency. Complacency reduces environmental scanning. The boundary between Clear and Chaotic is a catastrophic cliff, not a gradual slope. There is no warning zone. Systems that have been stable under Clear practices can collapse into Chaos without advance notice when conditions change but practices do not.

Signals that the cliff is approaching:

- Increasing frequency of exceptions to standard procedures
- Growing reliance on undocumented workarounds
- Expert practitioners quietly doubting standard approaches
- Environmental conditions measurably different from when best practices were established
- Escalating effort required to apply standard procedures

Mitigations: Maintain active dissent channels. Periodically review whether best practices still fit current conditions. Treat exceptions as early warnings, not noise.

---

### 2. Complicated (Known Unknowns)

**Character:** Cause-and-effect relationships exist and are discoverable, but require expert analysis. Multiple valid solutions may exist; the goal is to identify a *good* practice, not necessarily the single best one.

**Protocol:** Sense → Analyze → Respond

- **Sense:** Observe and gather data
- **Analyze:** Apply expert knowledge, systematic investigation, or diagnostic tools
- **Respond:** Implement the selected solution from a range of good options

**Signals:**

- Problem is deterministic — given enough analysis, the answer is knowable
- Expert communities have established bodies of knowledge applicable here
- Multiple correct approaches exist, with articulable trade-offs
- Root cause analysis is feasible and productive
- Models and simulations yield useful predictions

**SDLC approach:** Architecture review, RFCs, design documents, expert gates. Kanban or sprint planning with well-defined stories. ADRs as first-class artifacts. TDD, peer review, static analysis.

**Software examples:** Diagnosing a performance regression in a known codebase. Selecting a message queue technology based on stated requirements. Designing a relational schema for a specified domain. Conducting a security audit against a known threat model.

---

### 3. Complex (Unknown Unknowns)

**Character:** Cause-and-effect relationships exist in retrospect but cannot be predicted in advance. The system is adaptive: actors and components change in response to each other, producing emergent behavior no analysis could have predicted. There are no right answers, only more or less useful patterns that emerge.

**Protocol:** Probe → Sense → Respond

- **Probe:** Run small, deliberate, safe-to-fail experiments to stimulate the system
- **Sense:** Observe the patterns that emerge
- **Respond:** Amplify beneficial patterns; dampen or terminate harmful ones

**Safe-to-fail probes** are not "safe enough to try" risk decisions. They are specifically designed to be small and bounded so that failure does not cascade. The emphasis is not on ensuring success — it is on allowing unhelpful ideas to fail in contained, tolerable ways. Run multiple probes in parallel; the emergent behavior may differ across variations.

**Signals:**

- Requirements will change as users interact with the solution
- The team has never done anything like this before
- Competing experts disagree on fundamental approach
- Outcome of proposed action is unknown until attempted
- Historical data is a weak predictor of future state
- Stakeholder needs shift as the solution evolves

**SDLC approach:** Scrum with genuine empirical process control. Hypothesis stories ("We believe X; we will build Y; we will know we were right when Z"). Feature flags, canary deployments, A/B testing. Outcome-based roadmaps. Evolutionary architecture, deferred decisions. Spike stories. No upfront Big Design.

**Software examples:** Building a product for a new market. Developing an ML system where model behavior cannot be predicted from architecture alone. Evolving a microservices architecture where coupling patterns are not yet stable. Platform API design where ecosystem consumers will shape what "correct" means.

---

### 4. Chaotic (Unknowable)

**Character:** Cause-and-effect relationships are non-existent or too tangled and fast-moving to seek before acting. There is no stable ground from which to probe or analyze. The imperative is to act to create order — any order — and then work with what emerges.

**Protocol:** Act → Sense → Respond

- **Act:** Take any action that reduces harm and establishes a foothold of stability; novel actions are often required
- **Sense:** Once the initial action has created some boundary, assess what has changed
- **Respond:** Use the information from sensing to move the situation toward Complex, where Probe-Sense-Respond can take over

**Acting first is not recklessness — it is the correct epistemic response to a system providing no coherent signal.**

**Signals:**

- Active system failure with unknown root cause
- Multiple simultaneous failures that prevent isolation
- Normal channels of communication and escalation are broken or overloaded
- Standard procedures do not apply or are making things worse
- Rapid, cascading change with no clear causal chain

**SDLC approach:** Incident command structure (ICS). Time-boxed triage. Rollback over fix-in-place when possible. Clear roles: Incident Commander, Communications Lead, Technical Lead. Communicate at cadence: brief, frequent, authoritative. Blameless postmortems after stabilization, not during.

**Software examples:** Production system down with unknown root cause and multiple alarms firing. Active security breach with unknown attack vector. Cascading database corruption across all replicas. Third-party dependency failure with no available substitute.

**Transition objective:** Move the situation to Complex as quickly as possible. Once any stable constraint exists, Probe-Sense-Respond can begin. Never skip directly to Clear.

---

### 5. Disorder (Unknown Which Domain Applies)

**Character:** It is genuinely unclear which of the four primary domains the situation inhabits. People in Disorder default to their habitual decision-making style, which may be wholly inappropriate.

**Protocol:** Decompose → Classify each part → Apply per-domain protocol

The "aporetic turn": find the lowest level of coherence in the situation and route each component out to the appropriate domain separately. Decompose aggressively until each piece has a clear domain signal.

**Failure mode in Disorder:** Defaulting to comfort.

- Bureaucrats perceive everything as Clear (apply the procedure)
- Engineers perceive everything as Complicated (let me analyze this)
- Innovators perceive everything as Complex (let's experiment)
- Crisis responders perceive everything as Chaotic (give me authority and time)

None of these defaults are reliable guides.

---

## Classification Heuristics

Use this decision sequence before choosing a response strategy.

### Tier 1: Immediate Disqualifiers

1. Is there an active system failure in progress with unknown cause? → **Chaotic**
2. Is it genuinely unclear which domain applies? → **Disorder** (decompose first)

### Tier 2: Clear Domain Tests

Apply all five. If all pass: **Clear**.

1. Has this class of problem been solved before with high consistency of outcome?
2. Does a well-established, documented procedure exist?
3. Would competent practitioners agree on the correct approach without significant deliberation?
4. Is the outcome of applying the procedure predictable in advance?
5. Is input/context variability low enough that the procedure applies without adaptation?

If any fail: proceed to Tier 3.

### Tier 3: Complicated vs. Complex

**Test A — Determinism:** If all relevant information were gathered and expert analysis applied, would a single correct (or clearly better) answer emerge?

- Yes → **Complicated**
- No (depends on emergent behavior, user adoption, market response) → **Complex**

**Test B — Hypothesis testability:** Can a hypothesis be formulated and tested without running the actual system?

- Yes (can reason about it, model it, analyze it) → **Complicated**
- No (must run the system to find out) → **Complex**

**Test C — Expert consensus:** Would domain experts analyzing the same information reach high agreement on approach?

- Yes → **Complicated**
- No (fundamentally different mental models) → **Complex**

### Signal Matrix

| Signal | Clear | Complicated | Complex | Chaotic |
|---|---|---|---|---|
| Team familiarity with this problem | Many times | Several times | Rarely/never | Never, or this form is new |
| Outcome predictability | Certain | High after analysis | Unknown until attempted | Unknowable |
| Expert agreement | Universal | High (with trade-offs) | Low (different models) | Experts bypassing analysis |
| Planning horizon | Long; upfront works | Medium; architecture valid | Short; incremental discovery | Immediate; minutes to hours |
| Primary artifact | Runbook / SOP | ADR / RFC / Design doc | Hypothesis / spike | Incident log / action item |
| Test approach | Comprehensive suites | TDD, static analysis | Hypothesis / A/B | Smoke tests; fix first |
| Role of best practices | Apply directly | Select and adapt | Potentially misleading | May be contraindicated |

---

## Common Misclassification Traps

**Complicated classified as Clear (most common):** Applying a best practice from a different context without adaptation. Cargo-cult engineering: copying the form of a solution without understanding the context that made it appropriate.

**Complex classified as Complicated:** Attempting to analyze your way to a solution in a situation that is inherently emergent. Writing extensive specifications for systems that will need to discover their own requirements through use. Classic symptom: analysis paralysis before a product has had any users.

**Clear classified as Complex:** Over-engineering stable, well-understood problems. Introducing unnecessary experimentation into work that should be automated and standardized. Wastes resources and introduces risk into areas that should be risk-free.

**Chaotic classified as Complicated:** The war-room failure mode. Attempting structured root-cause analysis during an active, escalating incident. Meanwhile the outage deepens. Stabilize first; analyze after.

---

## Response Calibration by Domain

**Clear response pattern:**

- High confidence, direct recommendation
- Reference the applicable best practice or standard
- No hedging beyond known exceptions
- Offer to automate or template

**Complicated response pattern:**

- Present structured analysis of the option space
- Identify trade-offs for the specific context
- Make a recommendation with explicit reasoning
- Acknowledge alternative approaches and why they rank lower
- Invite expert review of the analysis

**Complex response pattern:**

- Acknowledge inherent uncertainty; do not fake confidence
- Frame the engagement as a probe, not a solution
- Propose multiple small experiments rather than a single recommended approach
- Specify observable signals that will distinguish between hypotheses
- Commit to iteration

**Chaotic response pattern:**

- Prioritize stabilization over understanding
- Provide the fastest path to "less bad" even if imperfect
- Communicate clearly about what is known vs. unknown
- Explicitly defer root-cause analysis: "Resolve the immediate situation; investigate after"
- Flag the transition point: "Once stable, apply Complicated protocol"

**Disorder response pattern:**

- Do not attempt to answer the full question as stated
- Explicitly name the classification problem
- Decompose into sub-questions with clearer domain signals
- Route each sub-question to the appropriate domain protocol

---

## Liminal Zones

**CO-CO (Complex → Complicated):** The transitional space where Scrum actually lives. Problems are held in managed uncertainty (still exploratory, but with enough constraint to produce consistent output) until patterns emerge that can be stabilized into repeatable processes. The sprint is the constraint; the retrospective is the sensing mechanism; the backlog is the adaptive response. Key principle: delay commitment to a Complicated-domain solution until you have evidence of authentic repeatability.

**CO-CH (Complex → Chaotic):** Deliberate loosening of constraints to create space for innovation. Hackathons, innovation labs, chaos engineering in controlled environments. A bounded, time-limited intervention — not a permanent state.

---

## Cynefin and the SDLC Gates

The Architect agent classifies the incoming request in Gate 1. That classification propagates through all subsequent gates and determines:

| Classification | ADR depth | Security review focus | Engineering approach | Gate rigor |
|---|---|---|---|---|
| Clear | Lightweight (reference standard) | Verify compliance with known controls | Follow established patterns | Fast-track; automated checks |
| Complicated | Full ADR with trade-off analysis | STRIDE threat model | Expert implementation with tests | All gates at full depth |
| Complex | Probe-design document | Threat model with emergent risk flags | Spike → iterate | All gates + iteration loops |
| Chaotic | Stabilization brief | Immediate threat containment | Emergency path | Compressed gates; human sign-off required |
