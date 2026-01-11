# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project "Recursive Language Models for Cross-Modal Inference".

## Papers
Total papers: 7 (See `papers/` directory)
- `alabdulmohsin_2025_recursive_inference.pdf`
- `carm_hierarchical_memory_2021.pdf`
- `multiscale_prompt_memory_2024.pdf`
- `nested_learning_2025.pdf`
- `online_cl_multiscale_distillation_2022.pdf`
- `zhang_2025_recursive_language_models.pdf`
- `zhou_2024_visual_icl.pdf`

## Datasets
| Name | Source | Task | Location |
|------|--------|------|----------|
| ScienceQA | HuggingFace | Multimodal Reasoning | `datasets/scienceqa/` |

## Code Repositories
| Name | Purpose | Location |
|------|---------|----------|
| RLM | Recursive Inference Impl | `code/rlm/` |
| Otter | Visual ICL Baseline | `code/otter/` |

## Resource Gathering Notes
- **Search Strategy**: Focused on official implementations of key papers and robust multimodal benchmarks.
- **Dataset Selection**: ScienceQA was selected for its reasoning complexity and multimodal nature.
- **Code Selection**: `alexzhang13/rlm` is the direct implementation of the core text-recursive method. `Otter` is a strong representative for visual ICL.

## Recommendations
1.  **Primary Experiment**: Apply RLM chunking strategies to the text lectures in ScienceQA, while using Otter's ICL capabilities to handle the image inputs.
2.  **Baselines**: Compare against standard LLaVA (zero-shot) and standard RLM (text-only, ignoring images).
