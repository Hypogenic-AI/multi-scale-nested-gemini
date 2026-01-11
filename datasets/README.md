# Downloaded Datasets

This directory contains datasets for the research project. Data files are NOT committed to git due to size.

## Dataset 1: ScienceQA

### Overview
- **Source**: [HuggingFace - derek-thomas/ScienceQA](https://huggingface.co/datasets/derek-thomas/ScienceQA)
- **Task**: Multimodal Multiple Choice Question Answering
- **Features**: Image context, Text context, Lecture, Explanation
- **Splits**: Train, Validation, Test

### Download Instructions

**Using HuggingFace (Script provided):**
```bash
python download_scienceqa.py
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/scienceqa")
```

### Sample Data
ScienceQA examples contain:
- `question`: The text question.
- `choices`: Multiple choice options.
- `answer`: Correct answer index.
- `image`: PIL Image object (if applicable).
- `lecture`: Relevant background knowledge.
- `explanation`: Reasoning for the answer.
