# Week 4 Guideline Counterexamples: Requirements

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

## Guidelines

### Guideline 1: Use Different Chats for Different Contexts [1]. Design a structured context prompt, but avoid using the same prompt for different context problems.

**Description:** The requirement always specifies that developers must design structured context prompts to achieve the goals based on the constraints, stakeholders, and evaluation criteria. In a prompt-based interaction, it is essential to enforce context isolation by mandating the use of separate conversational contexts (i.e., distinct chats) for different problem domains, thereby preventing context leakage, implicit assumption carryover, and requirement contamination across tasks.

**Reasoning:** Empirical studies on prompt patterns and task-specific templates demonstrate that structured, high–information-density prompts enhance the quality of large language model (LLM) outputs for requirements engineering tasks by minimizing boilerplate responses and promoting consistent structure. These advantages are contingent upon maintaining all prompt instructions within a single, well-defined context [6]. Task-scoped prompts mitigate misdirection and prevent unintended information leakage, resulting in more accurate and consistent outputs [5]. Conversely, introducing out-of-context questions increases the likelihood of LLMs generating inconsistent or incorrect responses, indicating a failure in contextual reasoning. In requirements engineering, this phenomenon is comparable to merging requirements from disparate systems into a single specification, which creates ambiguity, hidden conflicts, and diminished traceability, thereby reducing the overall quality of the resulting artifacts.

**Example:**

Task: Write requirements for an online shopping system.

Poor Prompt:
- Act as a requirement engineer.
- Write functional requirements for an online shopping system.
- Also, explain how machine learning improves health care systems.
- What is the history and impact of the Second World War in today's world?

The output of these mixed-context prompts is hard to evaluate and yields inconsistent results.

Good prompt:
- Act as a requirement engineer
- Write functional and non-functional requirements for an online shopping system.
- List types of customers, products, and goals.
- List assumptions and out-of-scope items

Here, all instructions align with one system, and the output is consistent. This guideline is true for all types of example problems.

---

### Guideline 2: MVP (Minimum Viable Product) Requirement List [2, 3, 4]

**Description:**

Label every single user story with:
- M - Must Have
- S - Should Have
- C - Could Have
- W - Won't Have

**Reasoning:**

The ideal Requirement Engineering (RE) practices are often not a linear, waterfall-like process. The clients are not always clear on what they want, and in which cases, even if they do, the requirements are often misinterpreted and/or misunderstood [2]. Previous studies have shown that Software Engineering Success is a complicated, multi-dimensional spectrum that involves far more than just meeting explicit client requirements [3]. As a core component of a software project's success, client satisfaction requires the software development team to ensure the stakeholders are on the same page [3]. Thus, it's not sufficient to just reach a consensus between the software development team and coding agents by using RFC-2119 modal verbs. It's always important to synchronize the software development teams' perception of the Minimum Viable Product with the client. The modal verbs SHALL/SHOULD/MAY are not enough to manage clients' expectations. It's important and necessary to push back on the customer's unreasonable expectations, especially during the early phases, to avoid the huge expectation gap at delivery time. One of the state-of-the-art practices for requirement analysis and expectation management is the MoSCoW method [4], which not only unifies "Must Have", "Should Have", "Could Have", and "Won't Have", but also helps provide a structured framework for negotiating project scope when resources—be the time, budget, or technical capacity—are finite.

**Example**

(AI Usage Declaration: Refined from the output of Gemini 3, with prompt "Generate a good prompt imitating a user prompting LLM to do software engineering requirement analysis using the MoSCoW method.")

```
You are an experienced Software Requirement Engineer determining the Minimum Viable Product (MVP) for {Project Name/Description}. To ensure full alignment between the development team and stakeholders and to avoid an expectation gap at delivery, I need to categorize our User Stories using the MoSCoW method.
Please analyze the following requirements and generate a structured list. For every item, assign a priority label (M, S, C, or W) and provide a brief 'Reasoning' to justify its placement based on {Time/Budget/Technical} constraints.
Categorization Rules:
- M (Must Have): Non-negotiable core functionality. Without these, the product is not viable.
- S (Should Have): Important but not vital for the initial launch.
- C (Could Have): Desirable 'bonus' features that will be included only if resources permit.
- W (Won't Have): Explicitly excluded from this release to protect the project scope.
Input Requirements / User Stories:
{user stories}
```

---

### Guideline 3: Task-Defined Output Format

**Description:** When the task explicitly requests labels only (e.g., F/N, Yes/No), binary answers, or other brief structured output, do not require justification or explanation. Use "avoid yes/no without explanation" only when the task asks for reasoning, analysis, or rationale. The task specification is the source of truth; the guideline must yield when the task forbids elaboration.

**Reasoning:** Requiring justification when the task specifies labels-only output causes a format violation and produces the wrong deliverable, even when classifications are correct. For traceability matrices, tickboxes, dashboards, or other format-strict artifacts, extra prose makes the output unusable. Empirical work on prompt patterns shows that structured prompts improve consistency, but that consistency must align with the task's required output format. Overriding explicit task constraints (e.g., "no justifications") with a generic guideline (e.g., "always explain") leads to incorrect artifacts and violates the principle of matching the prompt to the intended deliverable.

**Example:**

Task: Does the design satisfy the security requirement? Answer only Yes or No.

Poor Prompt:
- Does the design satisfy the requirement? Provide reasoning - do not give only Yes or No without explanation.

The output adds reasoning when the task asks for Yes/No only.

Good prompt:
- Does the design satisfy the requirement? Answer only Yes or No

The output here would match the task.

---


## References

[1] Min, Sewon, et al. "Rethinking the role of demonstrations: What makes in-context learning work?." arXiv preprint arXiv:2202.12837 (2022).

[2] Ralph, Paul. 'The Illusion of Requirements in Software Development'. Requirements Engineering, vol. 18, no. 3, Sept. 2013, pp. 293–296, https://doi.org/10.1007/s00766-012-0161-4.

[3] Ralph, Paul, and Paul Kelly. 'The Dimensions of Software Engineering Success'. Proceedings of the 36th International Conference on Software Engineering, Association for Computing Machinery, 2014, pp. 24–35, https://doi.org/10.1145/2568225.2568261. ICSE 2014.

[4] Kravchenko, Tatiana, Tatiana Bogdanova, and Timofey Shevgunov. "Ranking requirements using MoSCoW methodology in practice." Computer Science Online Conference. Cham: Springer International Publishing, 2022.

[5] Ronanki, K., Cabrero-Daniel, B., Horkoff, J., & Berger, C. (2024). Requirements engineering using generative ai: Prompts and prompting patterns. In Generative AI for effective software development (pp. 109-127). Cham: Springer Nature Switzerland.

[6] Santos, S., Breaux, T., Norton, T., Haghighi, S., & Ghanavati, S. (2024, June). Requirements satisfiability with in-context learning. In 2024 IEEE 32nd International Requirements Engineering Conference (RE) (pp. 168-179). IEEE.
