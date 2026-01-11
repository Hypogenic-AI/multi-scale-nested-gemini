from datasets import load_dataset
import os

# Create directory
output_dir = "datasets/scienceqa"
os.makedirs(output_dir, exist_ok=True)

print(f"Downloading ScienceQA to {output_dir}...")
# ScienceQA is often hosted as "derek-thomas/ScienceQA" on HF
dataset = load_dataset("derek-thomas/ScienceQA")
dataset.save_to_disk(output_dir)
print("Download complete.")
