from datasets import load_from_disk
import json

def explore():
    try:
        dataset = load_from_disk("datasets/scienceqa")
        print("Keys:", dataset.keys())
        train = dataset["train"]
        print("Columns:", train.column_names)
        print("Example 0:", train[0])
        
        subjects = set(train["subject"])
        print("Unique Subjects:", subjects)
        
        topics = set(train["topic"])
        print("Unique Topics (first 10):", list(topics)[:10])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore()
