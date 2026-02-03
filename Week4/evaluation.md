# Week 4 Guideline Counterexamples: Requirements

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

## Evaluation

### Problem A_1: Requirement Validation, Risk, and Missing NFRs (privacy, compliance, and accessibility) check

**Example Bad Solution guideline 1 provided in the class**

## Sources
- Stakeholder interview transcripts in Exercise_A/docs/transcripts:
  - customer_support.md
  - finance.md
  - engineering.md

<span style="color:red">(Contaminated) This also covers “smart parking” occupancy prediction requirements.</span>

<span style="color:red">(Contaminated) Stakeholders require a Calendar AI Assistant for scheduling meetings.</span>

## Stakeholder summaries (quick)

1. **Customer Support:**
    - **Ambiguous/inconsistent**
      - “Context retention” is vague: how long is a session and what should be remembered?
      - “Personalized” is vague: based only on chat context or also customer/account info?
      - “Fast” is vague: no latency target.
    - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
      - What’s the minimum acceptable behavior (e.g., never ask for email twice in one session)?
      - How long should a session last (15/30/60 minutes)?
      - Is it acceptable to escalate to a human after 2 failed turns?
      - Accessibility: do you need screen-reader friendly formatting or simpler language mode?

---

2. **Finance**
    - **Ambiguous/inconsistent**
      - “40% reduction” baseline is unclear (total monthly spend vs cost/session).
      - “Minor UX regression” is unclear (how much CSAT drop is ok?).
    - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
      - Which metric is the true goal: total spend, cost/session, or cost/resolved case?
      - What is the maximum allowed temporary cost increase during a pilot?
      - What is the maximum acceptable temporary increase in escalations or drop in CSAT?
      - Any vendor constraints: data residency, security certifications, compliance requirements?

---

3. **Software Engineering**
    - **Ambiguous/inconsistent**
      - “Better model” is not defined by metrics (what is success?).
      - Memory approach is not specified (summary vs full transcript vs retrieval).
    - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
      - Define success metrics + thresholds (cost/session, p95 latency, CSAT, escalation rate).
      - Provide an effort estimate (FTE-weeks) for memory, caching, adapter layer, and pilot.
      - What is the rollback plan and target rollback time?
      - Privacy: how will you redact PII and set retention/deletion for session memory and logs?

---

**Example Good Solution with Guideline**

1. **Customer Support:**
   - **Ambiguous/inconsistent**
     - "Context retention" is not defined (how long is a session? what exactly is remembered?).
     - "Personalized" is not defined (conversation-only vs using account/profile data).
     - Faster response not quantified (no latency target).
   - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
     - What is the minimum memory behavior you need (e.g., never ask for email twice in one session)?
     - Is a "handoff to human" acceptable after N failed turns (e.g., after 2)?
     - What data must never be requested or stored (PII rules), and do you have accessibility needs (screen reader-friendly formatting, simpler language, multilingual)?

2. **Finance**
   - **Ambiguous/inconsistent**
     - "40% reduction" baseline is unclear (total monthly spend vs cost/session).
     - "Minor UX regressions" are not defined (how much CSAT drop/escalation increase is acceptable?).
   - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
     - Which metric is the real target: total spend, cost/session, or cost/resolved case (and what is the baseline)?
     - Are you open to a hybrid routing approach (cheap model for FAQs, premium only when needed) if it meets cost goals?
     - Any non-negotiable compliance/security constraints that could affect vendor choice (data residency, SOC2, retention/audit)?

3. **Software Engineering**
   - **Ambiguous/inconsistent**
     - "Better" is not defined (which metrics and thresholds decide success?).
     - Memory design not specified (what is stored, where, and for how long?).
     - Latency targets not stated.
   - **Targeted follow-up questions (contradictions, alternatives, missing NFRs)**
     - What are the go/no-go metrics for a pilot (cost/session, p95 latency, CSAT, escalation rate) and thresholds?
     - Can we improve memory without switching vendors (summaries, retrieval, caching), and what is the effort estimate?
     - What is the privacy/compliance plan (PII redaction, retention, deletion requests) and accessibility plan (readability, multilingual, screen reader compatibility)?

---

### Problem B_1: Requirement Classification

**Task Description:**

To classify requirements as either F (Functional) or NF (Non-Functional) and producing only a 2-column table: ID | (F or N). No justifications, no explanation, no reflection.

**Starter Code:**

There is no starter code for this task. Related file in `artifacts/requirements_R1-R4.md` has requirements that have to be classified as either Functional or Non-Functional by producing a 2-column table in a file named "req_classification_ans.md" under the same artifacts folder.

**Example Solution with Guidelines:**

**Problem:** Classification of Requirements

**Example Good Solution:**

| ID | F or N |
| --- | --- |
| R1 | F |
| R2 | N |
| R3 | F |
| R4 | N |

This solution correctly classifies all requirements and provides only the labels as requested. No justifications are included, matching the task requirement for a labels-only output suitable for traceability matrices or tickboxes.

**Example Bad Solution:**

| ID | F or N |
| :-- | :-- |
| R1 | F |
| R2 | N |
| R3 | F |
| R4 | N |

---

Justifications

- R1 — Functional: Booking appointments online is a specific system capability (a behavior the system must provide) and thus an FR.
- R2 — Non‑Functional: Encrypting stored patient data is a security constraint on how data is handled, describing a quality/property rather than a discrete feature.
- R3 — Functional: Sending reminders via email and SMS is an explicit action the system must perform, i.e., a functional behavior.
- R4 — Non‑Functional (ambiguous): It reads like a usability/usability-quality requirement (NFR) demanding a user-friendly interface for elderly users; it could be read as a feature if interpreted as a distinct UI tailored view, but I'll classify it as N given the phrasing and typical usability NFR interpretation.

**Format Violation:** The task explicitly asks for "labels only" with "No justification, no explanation, no reflection." This solution adds justifications, violating the task specification. Even though the classifications are correct, the output format is wrong for a traceability matrix or tickbox.

**Evaluation:**

- **Good:** Correctly classifies all requirements as F or N and provides only the labels in a 2-column table format. No justifications or explanations are included, matching the task requirement for labels-only output.
- **Satisfactory:** Correctly classifies most requirements but may include minor justification or explanations, or has one incorrect classification.
- **Bad:** Incorrectly classifies multiple requirements, or adds justification/explanation when the task explicitly requires labels only, violating the task specification.

---

### Problem C 1: Requirement Backlog Construction

**Example Good Solution:**

(AI Declaration: Generated by Copilot GPT-5 mini using prompt """ Customer Personas - Based on the requirement interviews, please analyze who the targeted users of this app are, and create at least 3 detailed Customer Personas. For each persona, please include the Persona, Archetype, Core Needs, and Pain Points. """ and then manually refined.)

1. **Persona: Curious Casual (Maya, 28)**
   - **Archetype:** Casual Learner / Everyday Explorer
   - **Core Needs:**
     - Quick, reliable identification of everyday objects.
     - Immediate, one-tap access to a readable Wikipedia article.
     - Low friction and beautiful UI.
     - Optional privacy controls (on-device processing).
     - Fast recognition (<2s ideally).
   - **Pain Points:**
     - Slow or flaky recognition.
     - Confusing results or low-confidence guesses.
     - Unclear privacy/what happens to images.
     - Poor mobile UX or long page loads.

2. **Persona: DIY Tinkerer (Liam, 34)**
   - **Archetype:** Hobbyist Maker / Weekend Repairer
   - **Core Needs:**
     - Detailed component-level information (schematics, part names).
     - Plausible "see-through" overlays to learn internals.
     - Ability to save/export diagrams and annotations.
     - Community corrections and sources for deeper learning.
   - **Pain Points:**
     - Superficial or incorrect internals (hallucinated overlays).
     - Lack of downloadable/authoritative schematics.
     - Limited ability to contribute fixes.
     - Unreliable recognition for uncommon items.

3. **Persona: Field Technician (Priya, 41)**
   - **Archetype:** Professional Technician / Engineer
   - **Core Needs:**
     - Authoritative, high-accuracy recognition.
     - Verified technical specs and part references.
     - Low latency and high availability in the field.
     - Offline or edge processing options.
     - Auditability and license/attribution for schematics.
   - **Pain Points:**
     - Hallucinated or non-authoritative data that could cause misdiagnosis.
     - Legal/licensing gaps for schematics.
     - Unacceptable latency or downtime.
     - Limited integrations with existing tools/workflows.

4. **Persona: Aesthetic Sharer (Noah, 22)**
   - **Archetype:** Style-driven Social Creator / Personalizer
   - **Core Needs:**
     - Instant phone-case colour and texture detection to auto-generate matching backgrounds and shareable wallpapers.
     - Beautiful synthesized gradients and patterns.
     - Easy sharing to social apps.
     - Fun "bespoke theming" onboarding.
   - **Pain Points:**
     - Inconsistent or inaccurate colour sampling.
     - Poor synthesis of textures/patterns.
     - Forced manual colour-sample steps.
     - Limited export/share options or poor image quality for social posts.

**Example Bad Solution:**

(AI Declaration: Generated by Gemini 3 using prompt """ Generate some very general and intentionally bad user personas for the following requirement interview transcripts + {transcripts} """ and then manually refined.)

**Persona name:** Gary

**Short bio:** Gary is a 32–48-year-old urban male, married with two kids, who uses the latest flagship phone, loves gadgets, and checks his phone 250 times per day. He has a bachelor's degree, lives in a large apartment, shops online, and prefers brands with blue logos.

**Persona name:** Barry

**Short bio:** Barry is a 29–33-year-old product influencer living in a trendy loft in Brooklyn. He has an MBA from a top-20 school, a curated capsule wardrobe, three designer tote bags, and exactly 12,400 followers across social platforms. He only uses the latest flagship phones at the moment they launch (and always in "Pro" colors). Barry travels first-class and expects instant gratification from technology; he never reads privacy policies and always accepts default permissions because he "trusts modern apps."

**Evaluation:**

- **Good:** Demonstrates a deep understanding of the persona, their archetype, core needs, and pain points. Clearly articulates how these personas impact the requirements.
- **Satisfactory:** Demonstrates basic understanding of the persona. But lack one or more aspects of the archetype, core needs, or pain points.
- **Bad:**
  - Including data that doesn't impact how they use the product.
  - Assuming the user knows exactly how to use the software.
  - Focusing only on what they do, not why they do it.
  - The personas are too generic, trying to make one persona represent everyone.

---

### Problem C 2 - 5: Requirement MVP Construction

**Example Good Solutions:**

**1. Core Recognition & Wiki Integration**

(AI Declaration: Generated by Gemini 3 using prompt """ 1. Backlog Generation - Use the same chat in Copilot, extract clear and actionable User Stories from the provided transcripts. Each one of the user stories should be in the form:
"As a [role/persona], I want to [interact with the app in a specific way] so that [a goal could be achieved]."
And interrelated stories should be in the same functional category,
2. Minimum Viable Product (MVP) - Use the same chat, apply the MoSCoW Prioritization method, and label each user story with a priority label:
- Must Have (M)
- Should Have (S)
- Could Have (C)
- Won't Have (W)
3. Story Point - Use a different chat, analyze the story points of each user story, and label each user story with a story point label from below:
- 1: Everything is known about this user story. It has no other dependencies, and should be less than 2 hours' work.
- 2: Almost everything is known. There are almost no dependencies, and it will be half a day's work.
- 3: Something is known about this user story. It has some dependencies and will take up to 2 days.
- 5: Almost nothing is known about this user story. It has a few dependencies and will take a few days.
- 8: Nothing is known about this user story. It has more than a few dependencies, and will take around a week.
- 13: Nothing is known about this user story. It has unknown dependencies and will take more than a week.
4. Acceptance Criteria - Use a different chat, define a sequence of step-by-step paths the user would navigate from the initial given state of the app to the desired outcome of each user story. + {transcripts} """ and then manually refined.)

| User Story # | Description | Story Points | MoSCoW | Acceptance Criteria |
|-------------|-------------|--------------|--------|-------------------|
| 1.01 | As a casual learner, I want to point my camera at an object and have it identified so that I can automatically land on its specific Wikipedia paragraph. | 3 | M | Given: The app is open with the camera active and a clear view of a common object (e.g., a spoon). When: The user centers the object in the viewfinder, and the AI identifies it with high confidence. Then: The app must automatically launch the in-app browser and scroll directly to the relevant descriptive paragraph on the localized Wikipedia page. |
| 1.02 | As a user, I want the identification process to take less than 0.5 seconds so that the experience feels magical and instantaneous. | 5 | S | Given: The user is on a standard high-speed mobile network or Wi-Fi. When: An object is captured in the camera frame. Then: The time elapsed from "Image Capture" to "Identity Displayed" must be <= 0.5 seconds. Then: The UI must maintain a smooth frame rate during this transition to ensure a "theatrical" and "magical" feel. |
| 1.03 | As a researcher, I want the app to generate a "micro-article" if a Wikipedia page doesn't exist so that I still get immediate context about the object. | 8 | C | Given: The AI identifies an object (e.g., a specific prototype) that does not have an existing Wikipedia entry. When: The retrieval engine confirms a 404 or "Page Not Found" status from the Wiki API. Then: The app must trigger a Large Language Model (LLM) to synthesize a brief, accurate introduction based on identified visual metadata. Then: The generated text must be clearly labeled as "AI-Generated Insight" and include an option for the user to "Submit to Wikipedia". |

**2. Advanced Visual Features**

| User Story # | Description | Story Points | MoSCoW | Acceptance Criteria |
|-------------|-------------|--------------|--------|-------------------|
| 2.01 | As a tech enthusiast, I want a "see-through" visual overlay of internal components (e.g., CPU, RAM) so that I can understand the inner workings of my devices. | 13 | W | Given: The user points the camera at a supported closed device (e.g., a specific laptop or smartphone model). When: The AI identifies the specific make and model. Then: The app must render a "theatrical" AR overlay showing a 3D exploded schematic of the internal components (CPU, RAM, battery) aligned with the physical object. Then: The UI must display an animation of "electrons flowing" or heat maps to create the intended "wow factor". |
| 2.02 | As a style-conscious user, I want the app background to automatically detect and match my phone case's color/texture so the UI feels bespoke. | 13 | W | Given: The user has opted into "Bespoke Theming" during onboarding. When: The user provides a reference image of their phone case (the "case selfie"). Then: The app must analyze and sample the color, texture (e.g., fabric weave), and sheen of the case. Then: The app background must automatically morph to a synthesized matching wallpaper that includes the case's specific gradients or patterns. |

**3. Support & Error Handling**

| User Story # | Description | Story Points | MoSCoW | Acceptance Criteria |
|-------------|-------------|--------------|--------|-------------------|
| 3.01 | As a user, I want to see the top three identification guesses with confidence scores if the AI is uncertain so that I can manually select the correct one. | 2 | M | Given: The AI's primary identification confidence score for an object is below the "Automatic Redirection" threshold (e.g., < 85%). When: The recognition process completes. Then: Instead of redirecting to Wikipedia, the app must display an "Ambiguity View" showing three cards representing the top three guesses. Then: Each card must display the object name and its corresponding confidence percentage (e.g., "Mug - 72%"). When: The user taps one of the cards. Then: The app immediately navigates to the Wikipedia page for that specific selection. |
| 3.02 | As an unsatisfied user, I want a "Report wrong result" flow so that I can help improve the AI's accuracy for future scans. | 3 | M | Given: The app has incorrectly identified an object or the user is on a Wikipedia page that doesn't match their physical object. When: The user taps the "Report wrong result" button. Then: A simple feedback overlay appears, allowing the user to suggest the correct name or select a category. When: The user submits the report. Then: The app must bundle the original image, the AI's guessed label, and the user's feedback, then upload it to the "Failure Case" database. Then: The user must receive a confirmation message (e.g., "Thanks! This helps WikiLens get smarter."). |

**4. Privacy & Accessibility**

| User Story # | Description | Story Points | MoSCoW | Acceptance Criteria |
|-------------|-------------|--------------|--------|-------------------|
| 4.01 | As a privacy-conscious user, I want an option to opt out of server-side logging so that my scanned images are not stored on the cloud. | 3 | M | Given: The user navigates to the "Privacy" section of the app settings. When: The user toggles the "Server-side Logging" switch to the OFF position. Then: Any subsequent images sent to the cloud for recognition must be deleted immediately after the identification result is returned. Then: The system must ensure that these images are not added to the 30-day retention pool or the manual curation pipeline. |
| 4.02 | As a non-English speaker, I want the app to support my native language (top 5 markets) so that I can use the tool effectively regardless of my location. | 5 | S | Given: The app is being used in one of the top five markets (English, Spanish, Mandarin, Hindi, Arabic). When: The user selects their preferred language in the system settings or app settings. Then: All UI elements (buttons, onboarding, error messages) must be displayed in that language. Then: When an object is identified, the app must automatically retrieve and display the Wikipedia entry from that language's specific Wiki subdomain (e.g., es.wikipedia.org). |

**Evaluation:**

- **Good:**
  - Interconnected user stories are grouped into the same category.
  - Each user story is specific to a single, actionable, and testable subtask.
  - Clearly identified that being able to "see through" objects using the camera is an unrealistic requirement, and have correctly labelled it as "Won't Have".
  - Clearly identified that being able to match the screen's background colour with the phone case's colour is an unrealistic requirement, and have correctly labelled it as "Won't Have".
  - The story point is aligned with the task's level of difficulty.
  - Acceptance Criteria is a clear path from the given state of a user story to the desired consequence of a user story.
- **Satisfactory:** Most of the criteria above are met, there are 1-3 points missing or being too coarse.
- **Bad:** Most of the criteria above are not met, most points are either missing or too coarse.

---


## References

[1] Min, Sewon, et al. "Rethinking the role of demonstrations: What makes in-context learning work?." arXiv preprint arXiv:2202.12837 (2022).

[2] Ralph, Paul. 'The Illusion of Requirements in Software Development'. Requirements Engineering, vol. 18, no. 3, Sept. 2013, pp. 293–296, https://doi.org/10.1007/s00766-012-0161-4.

[3] Ralph, Paul, and Paul Kelly. 'The Dimensions of Software Engineering Success'. Proceedings of the 36th International Conference on Software Engineering, Association for Computing Machinery, 2014, pp. 24–35, https://doi.org/10.1145/2568225.2568261. ICSE 2014.

[4] Kravchenko, Tatiana, Tatiana Bogdanova, and Timofey Shevgunov. "Ranking requirements using MoSCoW methodology in practice." Computer Science Online Conference. Cham: Springer International Publishing, 2022.

[5] Ronanki, K., Cabrero-Daniel, B., Horkoff, J., & Berger, C. (2024). Requirements engineering using generative ai: Prompts and prompting patterns. In Generative AI for effective software development (pp. 109-127). Cham: Springer Nature Switzerland.

[6] Santos, S., Breaux, T., Norton, T., Haghighi, S., & Ghanavati, S. (2024, June). Requirements satisfiability with in-context learning. In 2024 IEEE 32nd International Requirements Engineering Conference (RE) (pp. 168-179). IEEE.
