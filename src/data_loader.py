from datasets import load_from_disk
import random

def get_data_stream(dataset_path="datasets/scienceqa", samples_per_task=50, test_samples=20):
    dataset = load_from_disk(dataset_path)
    train_full = dataset["train"]
    # We use validation set as our "test" set for this experiment to avoid using the hidden test set labels
    # Actually ScienceQA has test set with labels usually, but let's check. 
    # The 'dataset_dict.json' showed 'test'. 
    # But usually test sets in HF don't have answers. 
    # Let's check if 'test' has answers.
    
    # Check if 'answer' is in test
    if 'answer' in dataset['test'].column_names:
        test_full = dataset['test']
    else:
        test_full = dataset['validation']
        
    subjects = ['natural science', 'social science', 'language science']
    
    tasks = []
    
    for subject in subjects:
        # Filter train
        train_examples = [ex for ex in train_full if ex['subject'] == subject]
        # Filter test
        test_examples = [ex for ex in test_full if ex['subject'] == subject]
        
        # Subsample
        random.seed(42)
        random.shuffle(train_examples)
        random.shuffle(test_examples)
        
        task_train = train_examples[:samples_per_task]
        task_test = test_examples[:test_samples]
        
        tasks.append({
            "subject": subject,
            "train": task_train,
            "test": task_test
        })
        
    return tasks

def format_example(example, include_answer=True):
    # Text-only format
    q = example['question']
    choices = example['choices']
    formatted_choices = "\n".join([f"({i}) {c}" for i, c in enumerate(choices)])
    text = f"Question: {q}\nChoices:\n{formatted_choices}\n"
    
    # Add lecture/hint if available for context?
    # For training memory, we should include the full "experience" (Question + Answer + Explanation/Lecture)
    if include_answer:
        ans_idx = example['answer']
        ans_text = choices[ans_idx]
        lecture = example['lecture'] if example['lecture'] else ""
        solution = example['solution'] if example['solution'] else ""
        
        text += f"Answer: ({ans_idx}) {ans_text}\n"
        if lecture:
            text += f"Lecture: {lecture}\n"
        if solution:
            text += f"Explanation: {solution}\n"
            
    return text

if __name__ == "__main__":
    tasks = get_data_stream()
    for t in tasks:
        print(f"Task: {t['subject']}, Train: {len(t['train'])}, Test: {len(t['test'])}")
