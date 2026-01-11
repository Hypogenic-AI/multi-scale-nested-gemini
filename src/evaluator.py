from tqdm import tqdm
from src.data_loader import format_example

def evaluate(llm_client, memory_context, test_examples):
    correct = 0
    total = len(test_examples)
    
    for ex in tqdm(test_examples, desc="Evaluating"):
        # Format target (no answer)
        target_text = format_example(ex, include_answer=False)
        
        prompt = f"""Use the following context (Past Knowledge and Examples) to answer the question.
        
{memory_context}

New Question:
{target_text}

Please output only the answer index, e.g., "Answer: (0)".
"""
        messages = [{"role": "user", "content": prompt}]
        response = llm_client.complete(messages, max_tokens=10)
        
        # Parse response
        # Expected: "Answer: (0)" or just "(0)" or "0"
        ans_idx = ex['answer']
        
        # simple check
        prediction = -1
        for i in range(len(ex['choices'])):
            if f"({i})" in response or f"{i}" == response.strip():
                prediction = i
                break
        
        if prediction == ans_idx:
            correct += 1
            
    return correct / total if total > 0 else 0
