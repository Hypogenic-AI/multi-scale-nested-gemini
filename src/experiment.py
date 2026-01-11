import json
import os
import numpy as np
from src.data_loader import get_data_stream
from src.llm_client import LLMClient
from src.memory import FlatMemory, NestedMemory
from src.evaluator import evaluate

def run_experiment():
    # Setup
    tasks = get_data_stream(samples_per_task=40, test_samples=15) # Slightly reduced for speed
    client = LLMClient()
    
    # 2000 chars ~ 500 tokens. 
    # 40 examples * 200 chars/ex = 8000 chars. 
    # If limit is 2000, we can hold ~10 examples.
    # So FlatMemory will forget quickly.
    LIMIT_CHARS = 3000 
    
    memories = {
        "Flat": FlatMemory(limit_chars=LIMIT_CHARS),
        "Nested": NestedMemory(limit_chars=LIMIT_CHARS)
    }
    
    results = {
        "Flat": [],
        "Nested": []
    }
    
    # Run for each memory type
    for mem_name, memory in memories.items():
        print(f"\n=== Running {mem_name} Memory ===")
        
        task_accuracies = [] # List of [Acc_Task0, Acc_Task1, ...] at each step
        
        for i, task in enumerate(tasks):
            print(f"--- Task {i}: {task['subject']} ---")
            
            # 1. Training (Add examples)
            memory.add_examples(task['train'])
            
            # 2. Evaluation (on all tasks seen so far)
            current_step_accs = {}
            context = memory.retrieve()
            # print(f"DEBUG Context ({mem_name}):\n{context[:200]}...\n[Length: {len(context)}]\n")
            
            for j in range(i + 1): # Evaluate on Task 0, 1, ... i
                eval_task = tasks[j]
                acc = evaluate(client, context, eval_task['test'])
                current_step_accs[f"Task_{j}_{eval_task['subject']}"] = acc
                print(f"Eval Task {j}: {acc:.2f}")
                
            results[mem_name].append({
                "step": i,
                "accuracies": current_step_accs
            })
            
            # 3. Commit (Transition to next task)
            memory.commit_task(task['subject'], client)
            
    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/metrics.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("Experiment Complete. Results saved.")

if __name__ == "__main__":
    run_experiment()
