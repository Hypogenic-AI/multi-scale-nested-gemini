# Research Plan: Multi-Scale Nested Learning for Hierarchical Memory Systems in Continual Learning

## Research Question
Can hierarchically nested memory systems (specifically using recursive summarization/chunking) reduce catastrophic forgetting and improve flexibility in Continual Learning (CL) tasks compared to flat or no-memory baselines?

## Background and Motivation
Continual Learning challenges models to learn a sequence of tasks without forgetting previous ones. Standard Large Language Models (LLMs) often struggle with this when fine-tuned, or run out of context window when using In-Context Learning (ICL) for long histories.
"Recursive Language Models" (RLM) propose managing infinite context via recursive chunking. "Nested Learning" suggests organizing memory at different scales.
We propose combining these ideas: using a recursive/hierarchical memory structure to store compressed representations (summaries) of past tasks, allowing the model to retain "gist" knowledge of previous domains (long-term memory) while processing current detailed data (short-term memory).

## Hypothesis Decomposition
1.  **H1**: A hierarchical memory system (storing recursive summaries of past data) will yield higher accuracy on *past* tasks (less forgetting) than a FIFO buffer of equal token size.
2.  **H2**: Hierarchical memory will maintain comparable performance on the *current* task.

## Proposed Methodology

### Approach
We will simulate a Continual Learning scenario using the **ScienceQA** dataset, split by subject (e.g., Natural Science, Social Science, Language Science).
We will use **In-Context Learning (ICL)** with a fixed context window constraint to simulate memory limits.
We will compare different strategies for populating the context window with "memory" from previous tasks.

### Experimental Steps
1.  **Data Prep**: Split ScienceQA into 3 sequential tasks based on "Subject" (e.g., Task 1: Natural Science, Task 2: Social Science, Task 3: Language Science).
2.  **Baseline 1 (No Memory)**: Predict on current task using only current task examples (N-shot).
3.  **Baseline 2 (Flat Memory)**: Fill context window with raw examples from current and previous tasks (FIFO/Random reservoir) up to token limit.
4.  **Method (Nested/Recursive Memory)**:
    *   Maintain a "Long-Term Memory" of previous tasks by recursively summarizing examples into high-level "rules" or "concepts".
    *   Fill context window with: [Summaries of Task 1] + [Summaries of Task 2] + [Raw Examples of Task 3].
5.  **Evaluation**: After each task phase, evaluate accuracy on ALL tasks (1, 2, 3) to measure current performance and backward transfer (forgetting).

### Baselines
*   **Zero-Shot**: No examples.
*   **Flat ICL**: Standard few-shot with examples drawn from history (random or recent), truncated by context limit.

### Evaluation Metrics
*   **Average Accuracy (ACC)**: Mean accuracy across all tasks encountered so far.
*   **Backward Transfer (BWT)**: Change in accuracy on old tasks after learning new ones. (Negative BWT = Forgetting).
*   **Token Usage**: Efficiency of the memory representation.

### Statistical Analysis Plan
*   Run experiments with 3 random seeds (shuffling example selection).
*   Compare ACC and BWT using t-tests.

## Expected Outcomes
*   **Flat ICL** will suffer from context overflow or recency bias (forgetting old tasks if they are pushed out).
*   **Nested Memory** will retain general performance on old tasks due to summaries, achieving better BWT.

## Timeline
*   **Phase 1 (Planning)**: Completed.
*   **Phase 2 (Implementation)**: Setup env, data loader for ScienceQA, CL loop, Memory classes (Flat, Nested). (1 hour)
*   **Phase 3 (Experiments)**: Run CL sequences (Biology -> Physics -> Chemistry etc) with GPT-4o (or available LLM). (1 hour)
*   **Phase 4 (Analysis)**: Aggregate logs, compute ACC/BWT, plot results. (30 min)
*   **Phase 5 (Reporting)**: Write REPORT.md. (30 min)

## Potential Challenges
*   **API Costs/Limits**: We will use a subset of ScienceQA (e.g., 50-100 samples per task) to keep costs manageable while showing trends.
*   **Summarization Quality**: If summaries are too vague, they won't help. We will use a "Harsh Critic" prompt to ensure high-quality rule extraction.

## Success Criteria
*   Successfully running the CL pipeline.
*   Demonstrating a measurable difference in Forgetting (BWT) between Flat and Nested memory.
