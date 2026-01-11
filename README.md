# Multi-Scale Nested Learning for Hierarchical Memory Systems

## Overview
This project investigates a **Nested Memory** architecture for Continual Learning. By recursively summarizing past tasks into high-level textual descriptions ("Long-Term Memory"), we enable Large Language Models (LLMs) to retain knowledge across sequential tasks without context window overflow, comparing this against a standard **Flat (FIFO)** memory baseline.

## Key Findings
- **Stability**: Nested Memory achieved **Zero Forgetting** on the first task, maintaining steady performance throughout the experiment.
- **Efficiency**: Summaries allowed the model to retain "gist" knowledge of all past tasks, whereas the Flat buffer could only hold the most recent task.
- **Performance**: Nested Memory outperformed Flat Memory in initial task acquisition (87% vs 73%).

## Reproduction
1.  **Setup Environment**:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install --python .venv numpy pandas tqdm openai tenacity scikit-learn datasets pillow matplotlib seaborn httpx
    ```
2.  **Run Experiment**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/experiment.py
    ```
3.  **Analyze Results**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/analyze_results.py
    ```

## Structure
- `src/`: Source code for data loading, memory logic, and experiment loop.
- `results/`: Output metrics and plots.
- `REPORT.md`: Full research report.
